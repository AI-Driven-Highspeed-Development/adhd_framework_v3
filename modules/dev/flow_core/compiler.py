"""
Flow Language Compiler (Stage 4)

Transforms a resolved FlowFile AST into Markdown output by traversing
nodes depth-first and applying style transformations.

Key responsibilities:
- Iterative AST traversal starting from @out node (avoids recursion limit)
- Content emission (strings, resolved references, file refs)
- Style application via StyleRegistry (pre/per_item/wrap/post phases)
- Whitespace handling (trim vs preserve modes)
- Layer-based heading generation

Compilation phases per node:
1. PRE: Emit before content (headings via style.title)
2. CONTENT: Compile all content items into List[str]
3. PER_ITEM: Transform individual items BEFORE join (lists via style.list)
4. JOIN: Combine items into single string
5. WRAP: Transform joined content (blockquotes, codefences)
6. POST: Emit after content (dividers via style.divider)

Usage:
    >>> from flow_core.compiler import Compiler
    >>> compiler = Compiler()
    >>> markdown = compiler.compile(resolved_flow_file)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Set

from logger_util import Logger
from .models import (
    ResolvedFlowFile,
    FlowNode,
    NodeRef,
    FileRef,
    ContentItem,
    FlowStyle,
    FlowParams,
    StringContent,
)
from .errors import MissingOutNodeError
from .styles import StyleRegistry


class Compiler:
    """
    Compiles a resolved FlowFile AST to Markdown output.
    
    The compiler performs depth-first traversal starting from the @out node,
    applying style handlers at each node to produce formatted Markdown.
    
    Compilation phases per node:
    1. PRE: Emit pre-content (headings via style.title)
    2. CONTENT: Compile content items into List[str]
    3. PER_ITEM: Transform individual items (lists via style.list)
    4. JOIN: Combine items into single string
    5. WRAP: Transform joined content (blockquotes, codefences)
    6. POST: Emit post-content (dividers via style.divider)
    """
    
    def __init__(self, logger: Optional[Logger] = None) -> None:
        """
        Initialize the compiler.
        
        Args:
            logger: Optional logger instance for debugging.
        """
        self.logger = logger or Logger(name="FlowCompiler")
        self._style_registry = StyleRegistry()
        self._nodes: dict[str, FlowNode] = {}
        self._visited: Set[str] = set()  # For debugging/cycle detection
    
    def compile(
        self,
        resolved: ResolvedFlowFile,
        require_out: bool = True
    ) -> str:
        """
        Compile a resolved FlowFile to Markdown.
        
        Args:
            resolved: The resolved FlowFile AST from the resolver.
            require_out: If True, raise error when @out is missing.
                        If False, return empty string for libraries.
            
        Returns:
            The compiled Markdown string.
            
        Raises:
            MissingOutNodeError: If require_out=True and no @out node exists.
        """
        self._nodes = resolved.nodes
        self._visited = set()
        
        self.logger.debug(f"Compiling FlowFile with {len(self._nodes)} nodes")
        
        # Check for @out entry point
        if resolved.out_node is None:
            if require_out:
                raise MissingOutNodeError(resolved.source_path or "")
            else:
                self.logger.debug("No @out node, returning empty (library mode)")
                return ""
        
        # Compile starting from @out
        result = self._compile_node(resolved.out_node)
        
        self.logger.debug(f"Compilation complete: {len(result)} chars")
        return result
    
    def _compile_node(self, node: FlowNode, _compilation_stack: Optional[Set[str]] = None) -> str:
        """
        Compile a single node to Markdown using iterative approach.
        
        Uses an explicit work stack to avoid Python recursion limits for deep chains.
        This allows compilation of 500+ node chains without RecursionError.
        
        Applies style phases:
        1. PRE: Emit before content (headings)
        2. CONTENT: Compile all content items into List[str]
        3. PER_ITEM: Transform individual items (lists) - preserves item boundaries
        4. JOIN: Combine items into single string
        5. WRAP: Transform joined content (blockquotes) - only content, not pre/post
        6. POST: Emit after content (dividers)
        
        Args:
            node: The FlowNode to compile.
            _compilation_stack: Internal set tracking nodes currently being compiled
                               for cycle detection. Do not pass externally.
            
        Returns:
            Compiled Markdown string for this node.
        """
        # Use iterative approach with explicit work stack to avoid recursion limit
        # Each frame holds the state for compiling one node
        
        @dataclass
        class CompileFrame:
            """State for compiling a single node."""
            node: FlowNode
            content_idx: int = 0            # Current content item index
            content_outputs: List[str] = field(default_factory=list)  # Collected content
            join_hints: List[str] = field(default_factory=list)  # Separator between items
            pre: str = ""                   # PRE phase result
            in_compilation: bool = False    # Have we added to compilation_stack?
        
        # Initialize compilation stack for cycle detection
        if _compilation_stack is None:
            _compilation_stack = set()
        
        def _add_output(frame: CompileFrame, item: str) -> None:
            """Add an item to content_outputs with join-hint tracking."""
            if not item:
                return
            if frame.content_outputs:
                prev = frame.content_outputs[-1]
                # Check closer_trim on previous item, opener_trim on current item
                prev_closer = getattr(prev, 'closer_trim', None)
                curr_opener = getattr(item, 'opener_trim', None)
                # Inline if either adjacent boundary says "preserve"
                if prev_closer is False or curr_opener is False:
                    frame.join_hints.append("")
                else:
                    frame.join_hints.append("\n")
            frame.content_outputs.append(item)
        
        # Stack of frames (simulates call stack)
        work_stack: List[CompileFrame] = [CompileFrame(node=node)]
        result_stack: List[str] = []  # Results to return to parent frames
        
        while work_stack:
            frame = work_stack[-1]
            current_node = frame.node
            
            # First time visiting this frame: check cycle, emit PRE
            if not frame.in_compilation:
                # BLOCKER-001/002: Detect circular references
                if current_node.id in _compilation_stack:
                    self.logger.warning(f"Circular reference detected: @{current_node.id}")
                    work_stack.pop()
                    result_stack.append(f"[CIRCULAR: @{current_node.id}]")
                    continue
                
                # Add to stack for cycle detection
                _compilation_stack.add(current_node.id)
                frame.in_compilation = True
                
                self._visited.add(current_node.id)
                self.logger.debug(f"Compiling @{current_node.id} (layer={current_node.layer})")
                
                # Phase 1: PRE - emit before content (headings)
                style = current_node.params.style if current_node.params else None
                frame.pre = self._style_registry.apply_pre(style, current_node.layer) or ""
            
            # Process content items one at a time
            content = current_node.content
            
            # If there's a result from a child compilation, collect it
            if result_stack and frame.content_idx > 0:
                child_result = result_stack.pop()
                if child_result:
                    _add_output(frame, child_result)
            
            # Process next content item
            while frame.content_idx < len(content):
                item = content[frame.content_idx]
                frame.content_idx += 1
                
                if isinstance(item, str):
                    # String content - add directly (StringContent is a str subclass)
                    if item:
                        _add_output(frame, item)
                
                elif isinstance(item, FileRef):
                    # File reference - emit literal path
                    if item.path:
                        _add_output(frame, item.path)
                
                elif isinstance(item, NodeRef):
                    # Reference to another node - need to compile it
                    target_node = self._resolve_node_ref(item)
                    if target_node is None:
                        _add_output(frame, f"[MISSING: ${item.id}]")
                    else:
                        # Push frame for target node and continue later
                        work_stack.append(CompileFrame(node=target_node))
                        break  # Exit loop to process child first
                
                elif isinstance(item, FlowNode):
                    # Nested node - push frame to compile it
                    work_stack.append(CompileFrame(node=item))
                    break  # Exit loop to process child first
                
                else:
                    self.logger.warning(f"Unknown content item type: {type(item)}")
            else:
                # All content items processed - finalize this node
                style = current_node.params.style if current_node.params else None
                
                parts: List[str] = []
                
                # Add PRE output
                if frame.pre:
                    parts.append(frame.pre)
                
                # Phase 3: PER_ITEM - transform individual items BEFORE join
                # This preserves semantic boundaries for multi-line content items
                content_items = self._style_registry.apply_per_item(
                    style, frame.content_outputs, current_node.layer
                )
                
                # Phase 4: JOIN - combine items with boundary-aware joining
                # Use join_hints if they align with content_items count
                if (
                    content_items
                    and len(frame.join_hints) == len(content_items) - 1
                ):
                    join_parts: List[str] = [content_items[0]]
                    for idx, ci in enumerate(content_items[1:]):
                        join_parts.append(frame.join_hints[idx])
                        join_parts.append(ci)
                    content_str = "".join(join_parts)
                else:
                    # Fallback: standard newline joining
                    content_str = "\n".join(content_items) if content_items else ""
                
                # Phase 5: WRAP - transform content ONLY (not pre/post)
                wrapped_content = self._style_registry.apply_wrap(style, content_str, current_node.layer)
                if wrapped_content:
                    parts.append(wrapped_content)
                
                # Phase 6: POST - emit after content (dividers)
                post = self._style_registry.apply_post(style, current_node.layer)
                if post:
                    parts.append(post)
                
                # Combine all parts
                result = "".join(parts)
                
                # Remove from compilation stack
                _compilation_stack.discard(current_node.id)
                
                # Pop this frame and push result
                work_stack.pop()
                result_stack.append(result)
        
        # Return the final result
        return result_stack[0] if result_stack else ""
    
    def _resolve_node_ref(self, ref: NodeRef) -> Optional[FlowNode]:
        """
        Resolve a node reference to its target node.
        
        Args:
            ref: The NodeRef to resolve.
            
        Returns:
            The target FlowNode, or None if not found.
        """
        # Parse the reference ID (may be "id" or "id.slot")
        parts = ref.id.split(".")
        node_id = parts[0]
        slot_path = parts[1:] if len(parts) > 1 else []
        
        # Look up the node
        target_node = self._nodes.get(node_id)
        if target_node is None:
            self.logger.error(f"Node not found during compile: ${ref.id}")
            return None
        
        # Navigate to slot if specified
        for slot_name in slot_path:
            if slot_name in target_node.slots:
                target_node = target_node.slots[slot_name]
            else:
                self.logger.error(f"Slot not found during compile: {slot_name}")
                return None
        
        return target_node


# =============================================================================
# Module-Level Compile Functions
# =============================================================================


def compile_resolved(
    resolved: ResolvedFlowFile,
    require_out: bool = True,
    logger: Optional[Logger] = None
) -> str:
    """
    Compile a resolved FlowFile to Markdown.
    
    This is the main entry point for compilation.
    
    Args:
        resolved: The resolved FlowFile AST.
        require_out: If True, raise error when @out is missing.
        logger: Optional logger instance.
        
    Returns:
        Compiled Markdown string.
        
    Raises:
        MissingOutNodeError: If require_out=True and no @out node.
    
    Example:
        >>> from flow_core.resolver import resolve
        >>> from flow_core.compiler import compile_resolved
        >>> resolved = resolve(flow_file)
        >>> markdown = compile_resolved(resolved)
    """
    compiler = Compiler(logger=logger)
    return compiler.compile(resolved, require_out=require_out)
