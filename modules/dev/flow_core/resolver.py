"""
Flow Language Resolver (Stage 3)

Validates semantic correctness of the AST and produces a resolved version
where all references can be directly traversed. Handles:
- Backward/forward reference validation
- Circular dependency detection
- Import file loading and merging
- Assignment application (deep copy semantics)
- Topological ordering for deterministic compilation
"""

import copy
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum, auto

from logger_util import Logger
from .models import (
    FlowFile,
    FlowNode,
    NodeRef,
    FileRef,
    ImportNode,
    Assignment,
    ResolvedFlowFile,
    Position,
    ContentItem,
)
from .dependency_graph import DependencyGraph, EdgeType
from .errors import (
    FlowError,
    ResolverError,
    UndefinedNodeError,
    UndefinedSlotError,
    CircularDependencyError,
    ImportFileNotFoundError,
    CircularImportError,
    DuplicateNodeError,
)


class VisitState(Enum):
    """Node visit states for cycle detection."""
    UNVISITED = auto()
    VISITING = auto()  # Currently in the DFS path
    VISITED = auto()   # Fully processed


class Resolver:
    """
    Semantic analyzer and resolver for the Flow language.
    
    Takes a FlowFile AST from the parser and produces a ResolvedFlowFile
    with all references validated, imports merged, and dependencies ordered.
    """
    
    def __init__(self, logger: Optional[Logger] = None) -> None:
        """
        Initialize the resolver.
        
        Args:
            logger: Optional logger instance for debugging.
        """
        self.logger = logger or Logger(name="FlowResolver")
        
        # Resolution state (reset per resolve call)
        self._symbol_table: Dict[str, FlowNode] = {}
        self._node_positions: Dict[str, Position] = {}
        self._node_source_files: Dict[str, str] = {}  # node_id -> source file path
        self._node_order: List[str] = []  # Order nodes appear in file (for backward ref check)
        self._file_refs: List[str] = []
        self._import_stack: List[str] = []  # For circular import detection
        self._base_path: Optional[Path] = None
        
        # Dependency graph state (P1)
        self._graph_edges: Set[Tuple[str, str, str]] = set()  # (from_id, to_id, edge_type)
        self._graph_files: Set[Path] = set()  # All involved .flow files
        self._graph_file_refs: Set[Path] = set()  # All ++path references
        
        # Error collection mode (for validate_with_errors)
        self._collect_errors: bool = False
        self._errors: List[FlowError] = []
    
    def _reset_state(self, base_path: Optional[Path] = None) -> None:
        """Reset all resolution state for a new resolve/validate call."""
        self._symbol_table = {}
        self._node_positions = {}
        self._node_source_files = {}
        self._node_order = []
        self._file_refs = []
        self._import_stack = []
        self._base_path = base_path or Path.cwd()
        
        # Reset graph state (P1)
        self._graph_edges = set()
        self._graph_files = set()
        self._graph_file_refs = set()
        
        # Reset error collection
        self._collect_errors = False
        self._errors = []
    
    def _record_error(self, error: FlowError) -> bool:
        """
        Record an error - either raise immediately or collect for later.
        
        Args:
            error: The FlowError to record.
            
        Returns:
            True if in collect mode (caller should continue), False otherwise (unreachable).
            
        Raises:
            FlowError: If not in collect mode, raises the error immediately.
        """
        if self._collect_errors:
            self._errors.append(error)
            return True
        raise error
    
    def _create_child_resolver(self, child_base_path: Path) -> "Resolver":
        """
        Create a child resolver for processing imports.
        
        Shares the import stack and dependency graph state with the parent,
        but has independent symbol table and node tracking.
        
        Args:
            child_base_path: Base path for the child resolver.
            
        Returns:
            A new Resolver configured for import processing.
        """
        child = Resolver(logger=self.logger)
        child._symbol_table = {}
        child._node_positions = {}
        child._node_source_files = {}
        child._node_order = []
        child._file_refs = []
        child._import_stack = list(self._import_stack)  # Copy stack
        child._base_path = child_base_path
        
        # Share dependency graph state so transitive imports contribute
        child._graph_edges = self._graph_edges
        child._graph_files = self._graph_files
        child._graph_file_refs = self._graph_file_refs
        
        # Share error collection mode
        child._collect_errors = self._collect_errors
        child._errors = self._errors  # Share error list
        
        return child
    
    def resolve(
        self,
        flow_file: FlowFile,
        base_path: Optional[Path] = None,
        source_path: Optional[str] = None
    ) -> ResolvedFlowFile:
        """
        Resolve a FlowFile AST into a fully validated ResolvedFlowFile.
        
        Args:
            flow_file: The parsed FlowFile AST.
            base_path: Base directory for resolving import paths.
            source_path: Path to the source .flow file (for error messages).
            
        Returns:
            ResolvedFlowFile with all references resolved.
            
        Raises:
            UndefinedNodeError: Reference to non-existent node.
            UndefinedSlotError: Reference to non-existent slot.
            CircularDependencyError: Cycle detected in node references.
            ImportFileNotFoundError: Import file not found.
            CircularImportError: Circular import detected.
            DuplicateNodeError: Duplicate node ID across imports.
        """
        # Reset state
        self._reset_state(base_path)
        self._collect_errors = False
        self._errors = []
        
        source_str = source_path or str(self._base_path / "<source>")
        self.logger.debug(f"Resolving FlowFile from {source_str}")
        
        # Track source file in graph
        if source_path:
            self._import_stack.append(str(Path(source_path).resolve()))
            self._graph_files.add(Path(source_path).resolve())
        
        # Step 1: Process imports FIRST (so imported nodes count as "above" local nodes)
        self._process_imports(flow_file.imports)
        
        # Step 2: Build symbol table from local nodes (AFTER imports)
        self._build_symbol_table(flow_file, source_str)
        
        # Step 3: Validate all references and build graph edges
        self._validate_references()
        
        # Step 4: Apply assignments (deep copy semantics)
        self._apply_assignments(flow_file.assignments)
        
        # Step 5: Detect reference cycles (DFS with states)
        # Step 6: Compute topological order
        dependency_order = self._compute_topological_order()
        
        # Step 7: Collect file refs from all nodes
        self._collect_file_refs()
        
        # Build result
        out_node = self._symbol_table.get("out")
        
        resolved = ResolvedFlowFile(
            nodes=dict(self._symbol_table),  # Copy
            out_node=out_node,
            dependency_order=dependency_order,
            file_refs=self._file_refs,
            source_path=source_path,
        )
        
        self.logger.debug(f"Resolved: {resolved}")
        return resolved
    
    # =========================================================================
    # Step 1: Build Symbol Table
    # =========================================================================
    
    def _build_symbol_table(self, flow_file: FlowFile, source_path: str) -> None:
        """
        Build the initial symbol table from local nodes.
        
        Tracks node order for backward reference validation.
        """
        for node_id, node in flow_file.nodes.items():
            if node_id in self._symbol_table:
                # Duplicate - get existing position
                existing_pos = self._node_positions.get(node_id)
                existing_file = self._node_source_files.get(node_id, "")
                new_pos = node.position or Position(0, 0)
                self._record_error(DuplicateNodeError(
                    node_id=node_id,
                    first_line=existing_pos.line if existing_pos else 0,
                    first_column=existing_pos.column if existing_pos else 0,
                    second_line=new_pos.line,
                    second_column=new_pos.column,
                    first_file=existing_file,
                    second_file=source_path,
                ))
                continue  # Skip duplicate in collect mode
            
            self._symbol_table[node_id] = node
            self._node_positions[node_id] = node.position or Position(0, 0)
            self._node_source_files[node_id] = source_path
            self._node_order.append(node_id)
            
            self.logger.debug(f"Registered node @{node_id}")
    
    # =========================================================================
    # Step 2: Process Imports
    # =========================================================================
    
    def _process_imports(self, imports: List[ImportNode]) -> None:
        """
        Process import statements, loading and merging external files.
        
        - Recursively resolves transitive imports
        - Detects circular imports
        - Skips external @out nodes
        - Applies import selectors and renames
        - Tracks import files for dependency graph (P1)
        """
        for import_node in imports:
            self._process_single_import(import_node)
    
    def _process_single_import(self, import_node: ImportNode) -> None:
        """Process a single import statement."""
        import_path = import_node.path
        pos = import_node.position or Position(0, 0)
        
        # Resolve relative path
        resolved_path = self._resolve_import_path(import_path)
        resolved_str = str(resolved_path)
        
        # Check file exists
        if not resolved_path.exists():
            self._record_error(ImportFileNotFoundError(
                import_path=import_path,
                resolved_path=resolved_str,
                line=pos.line,
                column=pos.column,
            ))
            return  # Can't continue without the file
        
        # Check for circular import
        if resolved_str in self._import_stack:
            chain = self._import_stack + [resolved_str]
            self._record_error(CircularImportError(
                chain=chain,
                line=pos.line,
                column=pos.column,
            ))
            return  # Can't continue with circular import

        # Track explicit import edge in dependency graph (P1)
        if self._import_stack:
            importer_file = self._import_stack[-1]
            self._graph_edges.add((importer_file, resolved_str, EdgeType.IMPORT))
        
        self.logger.debug(f"Processing import: {import_path} -> {resolved_str}")
        
        # Track imported file in graph (P1)
        self._graph_files.add(resolved_path)
        
        # Push to import stack
        self._import_stack.append(resolved_str)
        
        try:
            # Load and parse the imported file
            imported_file = self._load_flow_file(resolved_path)
            
            # Create child resolver with shared state
            imported_resolver = self._create_child_resolver(resolved_path.parent)
            
            # Build symbol table for imported file
            imported_resolver._build_symbol_table(imported_file, resolved_str)
            
            # Process transitive imports
            imported_resolver._process_imports(imported_file.imports)
            
            # Merge imported nodes into our symbol table
            self._merge_imported_nodes(
                imported_resolver._symbol_table,
                imported_resolver._node_positions,
                imported_resolver._node_source_files,
                import_node,
                resolved_str,
            )
            
        finally:
            # Pop from import stack
            self._import_stack.pop()
    
    def _resolve_import_path(self, import_path: str) -> Path:
        """Resolve a relative import path to absolute."""
        # Remove leading ./ if present
        if import_path.startswith("./"):
            import_path = import_path[2:]
        
        return (self._base_path / import_path).resolve()
    
    def _load_flow_file(self, file_path: Path) -> FlowFile:
        """Load and parse a .flow file."""
        from .tokenizer import Tokenizer
        from .parser import Parser
        
        self.logger.debug(f"Loading flow file: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        
        tokenizer = Tokenizer(logger=self.logger)
        tokens = tokenizer.tokenize(source)
        
        parser = Parser(logger=self.logger)
        return parser.parse(tokens)
    
    def _merge_imported_nodes(
        self,
        imported_nodes: Dict[str, FlowNode],
        imported_positions: Dict[str, Position],
        imported_files: Dict[str, str],
        import_node: ImportNode,
        source_file: str,
    ) -> None:
        """
        Merge imported nodes into the symbol table.
        
        - Skips @out nodes from imports
        - Applies selectors (if specified)
        - Applies renames (if specified)
        - Raises DuplicateNodeError on collision
        """
        # Determine which nodes to import
        if import_node.selectors:
            # Import only specific nodes
            nodes_to_import = import_node.selectors
        else:
            # Import all nodes except @out
            nodes_to_import = [nid for nid in imported_nodes.keys() if nid != "out"]
        
        for original_name in nodes_to_import:
            if original_name not in imported_nodes:
                # Referenced node doesn't exist in import
                pos = import_node.position or Position(0, 0)
                self._record_error(UndefinedNodeError(
                    ref_id=original_name,
                    line=pos.line,
                    column=pos.column,
                    constraint_msg=f"not found in '{import_node.path}'",
                ))
                continue  # Skip this node in collect mode
            
            # Apply rename if specified
            local_name = import_node.renames.get(original_name, original_name)
            
            # Check for collision
            if local_name in self._symbol_table:
                existing_pos = self._node_positions.get(local_name)
                existing_file = self._node_source_files.get(local_name, "")
                imported_pos = imported_positions.get(original_name, Position(0, 0))
                self._record_error(DuplicateNodeError(
                    node_id=local_name,
                    first_line=existing_pos.line if existing_pos else 0,
                    first_column=existing_pos.column if existing_pos else 0,
                    second_line=imported_pos.line,
                    second_column=imported_pos.column,
                    first_file=existing_file,
                    second_file=source_file,
                ))
                continue  # Skip this node in collect mode
            
            # Deep copy the node (to avoid mutation issues)
            imported_node = copy.deepcopy(imported_nodes[original_name])
            
            # Update ID if renamed
            if local_name != original_name:
                imported_node.id = local_name
            
            # Add to symbol table
            self._symbol_table[local_name] = imported_node
            self._node_positions[local_name] = imported_positions.get(
                original_name, Position(0, 0)
            )
            self._node_source_files[local_name] = source_file
            self._node_order.append(local_name)
            
            self.logger.debug(f"Imported @{original_name} as @{local_name} from {source_file}")
    
    # =========================================================================
    # Step 3: Validate References
    # =========================================================================
    
    def _validate_references(self) -> None:
        """
        Validate all node references in the symbol table.
        
        - $ref (backward): Must be defined ABOVE in file
        - ^ref (forward): Must exist ANYWHERE in file
        - $a.slot: Both a and a.slot must exist
        
        Also builds dependency graph edges (P1).
        """
        for node_id in self._node_order:
            node = self._symbol_table[node_id]
            node_index = self._node_order.index(node_id)
            self._validate_node_refs(node, node_id, node_index)
    
    def _validate_node_refs(
        self, node: FlowNode, from_node_id: str, node_index: int
    ) -> None:
        """Validate all references within a node and collect graph edges."""
        # Validate content references
        for item in node.content:
            if isinstance(item, NodeRef):
                self._validate_single_ref(item, from_node_id, node_index)
            elif isinstance(item, FileRef):
                # Track file refs for graph (P1)
                self._graph_file_refs.add(Path(item.path))
            elif isinstance(item, FlowNode):
                # Nested node - validate recursively
                self._validate_node_refs(item, from_node_id, node_index)
        
        # Validate slot references
        for slot_name, slot_node in node.slots.items():
            self._validate_node_refs(slot_node, from_node_id, node_index)
    
    def _validate_single_ref(
        self, ref: NodeRef, from_node_id: str, referencing_node_index: int
    ) -> None:
        """
        Validate a single node reference and add edge to graph.
        
        Args:
            ref: The NodeRef to validate.
            from_node_id: The node containing this reference.
            referencing_node_index: Index of the node containing this reference.
        """
        pos = ref.position or Position(0, 0)
        ref_id = ref.id
        
        # Check for slot reference (e.g., $a.slot)
        if "." in ref_id:
            self._validate_slot_ref(ref_id, ref.is_forward, pos, from_node_id, referencing_node_index)
            return
        
        # Simple node reference
        if ref_id not in self._symbol_table:
            self._record_error(UndefinedNodeError(
                ref_id=ref_id,
                line=pos.line,
                column=pos.column,
                is_forward=ref.is_forward,
            ))
            return  # Can't validate further without the node
        
        # Check backward reference constraint
        if not ref.is_forward:
            # $ref must be defined ABOVE the referencing node
            target_index = self._node_order.index(ref_id) if ref_id in self._node_order else -1
            
            if target_index >= referencing_node_index:
                self._record_error(UndefinedNodeError(
                    ref_id=ref_id,
                    line=pos.line,
                    column=pos.column,
                    is_forward=False,
                    constraint_msg="backward reference ($) must reference node defined above",
                ))
                # Continue to add edge even if error in collect mode
        
        # Add edge to dependency graph (P1)
        edge_type = EdgeType.FORWARD_REF if ref.is_forward else EdgeType.BACKWARD_REF
        self._graph_edges.add((from_node_id, ref_id, edge_type))
    
    def _validate_slot_ref(
        self,
        ref_id: str,
        is_forward: bool,
        pos: Position,
        from_node_id: str,
        referencing_node_index: int
    ) -> None:
        """Validate a slot reference like $a.slot and add edge to graph."""
        parts = ref_id.split(".", 1)
        node_id = parts[0]
        slot_name = parts[1] if len(parts) > 1 else ""
        
        # Check node exists
        node_exists = node_id in self._symbol_table
        if not node_exists:
            self._record_error(UndefinedNodeError(
                ref_id=node_id,
                line=pos.line,
                column=pos.column,
                is_forward=is_forward,
            ))
            # Can't check slot if node doesn't exist
            return
        
        # Check backward constraint for the node part
        if not is_forward:
            target_index = self._node_order.index(node_id) if node_id in self._node_order else -1
            if target_index >= referencing_node_index:
                self._record_error(UndefinedNodeError(
                    ref_id=node_id,
                    line=pos.line,
                    column=pos.column,
                    is_forward=False,
                    constraint_msg="backward reference ($) must reference node defined above",
                ))
                # Continue to check slot in collect mode
        
        # Check slot exists
        if slot_name:
            target_node = self._symbol_table[node_id]
            if slot_name not in target_node.slots:
                self._record_error(UndefinedSlotError(
                    node_id=node_id,
                    slot_name=slot_name,
                    line=pos.line,
                    column=pos.column,
                ))
                # Continue to add edge in collect mode
        
        # Add edge to dependency graph (P1) - slot references use SLOT type
        self._graph_edges.add((from_node_id, node_id, EdgeType.SLOT))
    
    # =========================================================================
    # Step 4: Apply Assignments
    # =========================================================================
    
    def _apply_assignments(self, assignments: List[Assignment]) -> None:
        """
        Apply slot assignments with deep copy semantics.
        
        For $parent.slot = $child:
        - Deep copy child node into parent.slots[slot]
        """
        for assignment in assignments:
            self._apply_single_assignment(assignment)
    
    def _apply_single_assignment(self, assignment: Assignment) -> None:
        """Apply a single assignment."""
        pos = assignment.position or Position(0, 0)
        target = assignment.target  # e.g., "main.greeting"
        source = assignment.source  # e.g., "greeting"
        
        # Parse target
        if "." not in target:
            self._record_error(ResolverError(
                f"Assignment target must include slot: ${target} (expected $node.slot)",
                line=pos.line,
                column=pos.column,
            ))
            return  # Can't continue without valid target format
        
        target_parts = target.split(".", 1)
        target_node_id = target_parts[0]
        target_slot = target_parts[1]
        
        # Validate target node exists
        if target_node_id not in self._symbol_table:
            self._record_error(UndefinedNodeError(
                ref_id=target_node_id,
                line=pos.line,
                column=pos.column,
            ))
            return  # Can't continue without target node
        
        # Validate source node exists
        if source not in self._symbol_table:
            self._record_error(UndefinedNodeError(
                ref_id=source,
                line=pos.line,
                column=pos.column,
            ))
            return  # Can't continue without source node
        
        target_node = self._symbol_table[target_node_id]
        source_node = self._symbol_table[source]
        
        # Validate target slot exists (assignments can create slots or override existing)
        # According to spec: "Assignment to non-existent slot" -> UndefinedSlotError
        if target_slot not in target_node.slots:
            self._record_error(UndefinedSlotError(
                node_id=target_node_id,
                slot_name=target_slot,
                line=pos.line,
                column=pos.column,
            ))
            return  # Can't continue without valid slot
        
        # Deep copy source into target slot
        self.logger.debug(f"Applying assignment: ${target} = ${source}")
        target_node.slots[target_slot] = copy.deepcopy(source_node)
    
    # =========================================================================
    # Step 5 & 6: Cycle Detection and Topological Order
    # =========================================================================
    
    def _compute_topological_order(self) -> List[str]:
        """
        Detect cycles and compute topological order using DFS.
        
        Uses three-state coloring:
        - UNVISITED: Not yet processed
        - VISITING: Currently in DFS path (cycle if revisited)
        - VISITED: Fully processed
        
        Returns:
            List of node IDs in topological order (dependencies first).
            
        Raises:
            CircularDependencyError: If a cycle is detected (in fail-fast mode).
        """
        visit_state: Dict[str, VisitState] = {
            node_id: VisitState.UNVISITED for node_id in self._symbol_table
        }
        result: List[str] = []
        cycle_found: bool = False
        
        def dfs(node_id: str, path: List[str]) -> None:
            """DFS traversal with cycle detection."""
            nonlocal cycle_found
            
            # In collect mode, skip if we already found a cycle (to avoid duplicates)
            if cycle_found and self._collect_errors:
                return
            
            state = visit_state[node_id]
            
            if state == VisitState.VISITED:
                return
            
            if state == VisitState.VISITING:
                # Found a cycle - find where the cycle starts
                cycle_start = path.index(node_id)
                cycle_chain = path[cycle_start:] + [node_id]
                node = self._symbol_table.get(node_id)
                pos = node.position if node else Position(0, 0)
                cycle_found = True
                self._record_error(CircularDependencyError(
                    chain=cycle_chain,
                    line=pos.line if pos else 0,
                    column=pos.column if pos else 0,
                ))
                return  # Don't continue in this branch
            
            # Mark as visiting
            visit_state[node_id] = VisitState.VISITING
            current_path = path + [node_id]
            
            # Visit all dependencies (referenced nodes)
            node = self._symbol_table.get(node_id)
            if node:
                deps = self._get_node_dependencies(node)
                for dep_id in deps:
                    if dep_id in self._symbol_table:
                        dfs(dep_id, current_path)
            
            # Mark as visited and add to result
            visit_state[node_id] = VisitState.VISITED
            result.append(node_id)
        
        # Process all nodes
        for node_id in self._symbol_table:
            if visit_state[node_id] == VisitState.UNVISITED:
                dfs(node_id, [])
        
        # Result is in reverse post-order (dependencies first)
        return result
    
    def _get_node_dependencies(self, node: FlowNode) -> Set[str]:
        """
        Get all node IDs that a node depends on.
        
        Includes references in content and slots.
        """
        deps: Set[str] = set()
        
        def collect_refs(items: List[ContentItem]) -> None:
            for item in items:
                if isinstance(item, NodeRef):
                    # Extract base node ID (handle $a.slot case)
                    ref_id = item.id.split(".")[0] if "." in item.id else item.id
                    deps.add(ref_id)
                elif isinstance(item, FlowNode):
                    collect_refs(item.content)
                    for slot_node in item.slots.values():
                        collect_refs(slot_node.content)
        
        collect_refs(node.content)
        for slot_node in node.slots.values():
            collect_refs(slot_node.content)
        
        return deps
    
    # =========================================================================
    # Step 7: Collect File Refs
    # =========================================================================
    
    def _collect_file_refs(self) -> None:
        """Collect all ++path file references from nodes into _file_refs."""
        seen: Set[str] = set()
        for node in self._symbol_table.values():
            for path in self._get_node_file_refs(node):
                if path not in seen:
                    seen.add(path)
                    self._file_refs.append(path)
    
    def _get_node_file_refs(self, node: FlowNode) -> Set[str]:
        """Get all file ref paths from a single node (recursive)."""
        refs: Set[str] = set()
        
        def collect(items: List[ContentItem]) -> None:
            for item in items:
                if isinstance(item, FileRef):
                    refs.add(item.path)
                elif isinstance(item, FlowNode):
                    collect(item.content)
                    for slot_node in item.slots.values():
                        collect(slot_node.content)
        
        collect(node.content)
        for slot_node in node.slots.values():
            collect(slot_node.content)
        
        return refs
    
    # =========================================================================
    # Dependency Graph Building (P1)
    # =========================================================================
    
    def build_dependency_graph(self) -> DependencyGraph:
        """
        Build and return the dependency graph from current resolution state.
        
        Should be called after resolve() has been called.
        
        Returns:
            DependencyGraph with nodes, edges, and files.
            file_refs is computed from context_ref edges.
        """
        # Convert file_refs to context_ref edges
        # Each file ref creates an edge from the node containing it to the file path
        context_edges = set()
        for node_id in self._symbol_table:
            node = self._symbol_table[node_id]
            for file_ref_path in self._get_node_file_refs(node):
                context_edges.add((node_id, str(file_ref_path), EdgeType.CONTEXT_REF))
        
        all_edges = self._graph_edges | context_edges

        graph_nodes: Set[str] = set(self._symbol_table.keys())

        # Include file nodes so import edges and context refs render cleanly
        # in DOT/Mermaid exports.
        graph_nodes.update(str(p) for p in self._graph_files)

        # Ensure endpoints of any non-node edges are present as nodes too.
        # (e.g., file paths from CONTEXT_REF and IMPORT)
        for from_id, to_id, _ in all_edges:
            graph_nodes.add(from_id)
            graph_nodes.add(to_id)

        return DependencyGraph(
            nodes=frozenset(graph_nodes),
            edges=frozenset(all_edges),
            files=frozenset(self._graph_files),
        )

    # =========================================================================
    # Multi-Error Validation (P1)
    # =========================================================================

    def validate_with_errors(
        self,
        flow_file: FlowFile,
        base_path: Optional[Path] = None,
        source_path: Optional[str] = None,
    ) -> List[FlowError]:
        """Validate a FlowFile and collect multiple semantic errors.

        This does NOT change resolve() semantics (which raise-first). This is a
        best-effort validator intended for CLI `validate`.

        Returns:
            List of FlowError instances (may be empty).
        """
        # Reset state and enable error collection mode
        self._reset_state(base_path)
        self._collect_errors = True
        self._errors = []
        
        source_str = source_path or str(self._base_path / "<source>")
        
        # Track source file in graph
        if source_path:
            self._import_stack.append(str(Path(source_path).resolve()))
            self._graph_files.add(Path(source_path).resolve())
        
        # Run the same resolution steps as resolve(), but errors are collected
        # Step 1: Process imports
        self._process_imports(flow_file.imports)
        
        # Step 2: Build symbol table
        self._build_symbol_table(flow_file, source_str)
        
        # Step 3: Validate references
        self._validate_references()
        
        # Step 4: Apply assignments
        self._apply_assignments(flow_file.assignments)
        
        # Step 5: Cycle detection
        self._compute_topological_order()
        
        return self._errors
    
    def resolve_with_graph(
        self,
        flow_file: FlowFile,
        base_path: Optional[Path] = None,
        source_path: Optional[str] = None
    ) -> Tuple[ResolvedFlowFile, DependencyGraph]:
        """
        Resolve a FlowFile and return both the resolved file and dependency graph.
        
        Convenience method that combines resolve() and build_dependency_graph().
        
        Args:
            flow_file: The parsed FlowFile AST.
            base_path: Base directory for resolving import paths.
            source_path: Path to the source .flow file.
            
        Returns:
            Tuple of (ResolvedFlowFile, DependencyGraph).
        """
        resolved = self.resolve(flow_file, base_path, source_path)
        graph = self.build_dependency_graph()
        return resolved, graph


# =============================================================================
# Public API
# =============================================================================


def resolve(
    flow_file: FlowFile,
    base_path: Optional[Path] = None,
    source_path: Optional[str] = None,
    logger: Optional[Logger] = None
) -> ResolvedFlowFile:
    """
    Resolve a FlowFile AST into a fully validated ResolvedFlowFile.
    
    This is the main entry point for the resolver stage.
    
    Args:
        flow_file: The parsed FlowFile AST from the parser.
        base_path: Base directory for resolving import paths.
        source_path: Path to the source .flow file.
        logger: Optional logger instance.
        
    Returns:
        ResolvedFlowFile with all references validated.
        
    Raises:
        UndefinedNodeError: Reference to non-existent node.
        UndefinedSlotError: Reference to non-existent slot.
        CircularDependencyError: Cycle detected in node references.
        ImportFileNotFoundError: Import file not found.
        CircularImportError: Circular import detected.
        DuplicateNodeError: Duplicate node ID across imports.
    
    Example:
        >>> from flow_core.tokenizer import tokenize
        >>> from flow_core.parser import parse
        >>> from flow_core.resolver import resolve
        >>> tokens = tokenize("@greeting |<<<Hello!>>>|.\n@out |$greeting|.")
        >>> ast = parse(tokens)
        >>> resolved = resolve(ast)
        >>> print(resolved.dependency_order)
        ['greeting', 'out']
    """
    resolver = Resolver(logger=logger)
    return resolver.resolve(flow_file, base_path=base_path, source_path=source_path)


def resolve_with_graph(
    flow_file: FlowFile,
    base_path: Optional[Path] = None,
    source_path: Optional[str] = None,
    logger: Optional[Logger] = None
) -> Tuple[ResolvedFlowFile, DependencyGraph]:
    """
    Resolve a FlowFile AST and return both resolved file and dependency graph.
    
    Args:
        flow_file: The parsed FlowFile AST from the parser.
        base_path: Base directory for resolving import paths.
        source_path: Path to the source .flow file.
        logger: Optional logger instance.
        
    Returns:
        Tuple of (ResolvedFlowFile, DependencyGraph).
    
    Example:
        >>> from flow_core.resolver import resolve_with_graph
        >>> resolved, graph = resolve_with_graph(ast)
        >>> print(graph.to_mermaid())
    """
    resolver = Resolver(logger=logger)
    return resolver.resolve_with_graph(flow_file, base_path=base_path, source_path=source_path)


def validate_with_errors(
    flow_file: FlowFile,
    base_path: Optional[Path] = None,
    source_path: Optional[str] = None,
    logger: Optional[Logger] = None,
) -> List[FlowError]:
    """Validate a FlowFile and collect multiple semantic errors.

    Intended for CLI `validate` and tooling that wants best-effort reporting.
    """
    resolver = Resolver(logger=logger)
    return resolver.validate_with_errors(flow_file, base_path=base_path, source_path=source_path)
