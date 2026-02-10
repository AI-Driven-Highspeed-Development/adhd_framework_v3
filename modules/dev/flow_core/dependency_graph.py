"""
Flow Core Dependency Graph

Directed graph of node dependencies ($, ^, imports) for the Flow language.
Supports tiered visibility filtering and export to DOT, Mermaid, and JSON formats.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Set
from pathlib import Path
import json
import hashlib
import re


class Tier:
    """Visibility tiers for dependency graph filtering.
    
    Level 0 (STRUCTURAL): Imports, top-level nodes, assignments, @out entry.
                          Shows slot badges but hides slot internals.
    Level 1 (DETAILED): Includes slot definitions, bindings, content sources.
    """
    STRUCTURAL = 0  # Default - overview with slot badges
    DETAILED = 1    # Full detail including slot internals


class EdgeType:
    """Edge types for the dependency graph."""
    BACKWARD_REF = "backward"    # $ref - backward reference
    FORWARD_REF = "forward"      # ^ref - forward reference  
    IMPORT = "import"            # +./path - import dependency
    SLOT = "slot"                # $node.slot - slot reference
    CONTEXT_REF = "context_ref"  # ++path - runtime file reference


def _make_display_name(name: str, source_dir: Optional[Path]) -> str:
    """
    Convert an absolute path or node name to a short display name.
    
    For file paths: returns relative path from source_dir or just the filename.
    For node IDs: returns the node ID as-is.
    
    Args:
        name: The node name or file path to convert.
        source_dir: The directory of the main source file (for relative paths).
        
    Returns:
        A short, readable display name.
    """
    # Check if it looks like an absolute path
    if name.startswith('/') or (len(name) > 2 and name[1] == ':'):
        path = Path(name)
        if source_dir is not None:
            try:
                # Try to make it relative to source directory
                rel_path = path.relative_to(source_dir)
                return str(rel_path)
            except ValueError:
                pass
        # Fall back to just the filename
        return path.name
    return name


@dataclass(frozen=True)
class DependencyGraph:
    """
    Directed graph of node dependencies ($, ^, imports).
    
    Immutable dataclass that captures the full dependency structure of a Flow
    compilation unit, including cross-file imports and references.
    
    Attributes:
        nodes: All node IDs in the graph
        edges: Edges as (from_id, to_id, edge_type) tuples
        files: All involved .flow files (source + imports)
        
    Properties:
        file_refs: Computed from context_ref edges - all ++path references
    """
    nodes: frozenset[str]
    edges: frozenset[tuple[str, str, str]]
    files: frozenset[Path]
    
    @property
    def file_refs(self) -> frozenset[Path]:
        """
        Get all ++path file references, computed from context_ref edges.
        
        Returns:
            Frozenset of Path objects for all external file references.
        """
        return frozenset(
            Path(to_id) for _, to_id, edge_type in self.edges 
            if edge_type == EdgeType.CONTEXT_REF
        )
    
    def dependents(self, node_id: str) -> Set[str]:
        """
        Get nodes that depend on this node (reverse lookup).
        
        Args:
            node_id: The node to find dependents for.
            
        Returns:
            Set of node IDs that reference this node.
        """
        return {from_id for from_id, to_id, _ in self.edges if to_id == node_id}
    
    def dependencies(self, node_id: str) -> Set[str]:
        """
        Get nodes that this node depends on.
        
        Args:
            node_id: The node to find dependencies for.
            
        Returns:
            Set of node IDs that this node references.
        """
        return {to_id for from_id, to_id, _ in self.edges if from_id == node_id}
    
    def edges_from(self, node_id: str) -> Set[tuple[str, str, str]]:
        """Get all edges originating from a node."""
        return {edge for edge in self.edges if edge[0] == node_id}
    
    def edges_to(self, node_id: str) -> Set[tuple[str, str, str]]:
        """Get all edges pointing to a node."""
        return {edge for edge in self.edges if edge[1] == node_id}
    
    def to_dot(
        self,
        tier: int = 0,
        node_badges: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Export to Graphviz DOT format.
        
        Args:
            tier: Visibility tier (0=structural, 1=detailed). At tier 0,
                  slot edges are hidden and badges shown.
            node_badges: Optional dict mapping node_id to badge string
                        (e.g., {"main": "[3 slots]"}). Used at tier 0.
        
        Returns:
            DOT format string suitable for Graphviz rendering.
        """
        # Determine source directory for relative paths
        source_dir = sorted(self.files)[0].parent if self.files else None
        node_badges = node_badges or {}
        
        # Filter edges based on tier
        filtered_edges = self.edges
        if tier == Tier.STRUCTURAL:
            # At structural level, hide slot edges
            filtered_edges = frozenset(
                e for e in self.edges if e[2] != EdgeType.SLOT
            )
        
        lines = ["digraph FlowDependencies {"]
        lines.append("    rankdir=TB;")
        lines.append("    node [shape=box];")
        lines.append("")
        
        # Add nodes
        for node in sorted(self.nodes):
            # Skip file paths at tier 0 unless they're import targets
            if tier == Tier.STRUCTURAL and node.startswith('/'):
                # Check if this file is an import target
                is_import_target = any(
                    e[1] == node and e[2] == EdgeType.IMPORT
                    for e in filtered_edges
                )
                if not is_import_target:
                    continue
            
            # Convert to display name and escape special characters
            display_name = _make_display_name(node, source_dir)
            badge = node_badges.get(node, "")
            if badge:
                display_name = f"{display_name} {badge}"
            safe_name = display_name.replace('"', '\\"')
            lines.append(f'    "{safe_name}";')
        
        lines.append("")
        
        # Add edges with labels
        edge_styles = {
            EdgeType.BACKWARD_REF: 'color="blue"',
            EdgeType.FORWARD_REF: 'color="green" style="dashed"',
            EdgeType.IMPORT: 'color="orange" style="bold"',
            EdgeType.SLOT: 'color="purple"',
            EdgeType.CONTEXT_REF: 'color="red" style="dotted"',
        }
        
        for from_id, to_id, edge_type in sorted(filtered_edges):
            safe_from = _make_display_name(from_id, source_dir).replace('"', '\\"')
            safe_to = _make_display_name(to_id, source_dir).replace('"', '\\"')
            style = edge_styles.get(edge_type, "")
            label = f'label="{edge_type}"'
            lines.append(f'    "{safe_from}" -> "{safe_to}" [{label} {style}];')
        
        lines.append("}")
        return "\n".join(lines)
    
    def to_mermaid(
        self,
        tier: int = 0,
        node_badges: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Export to Mermaid flowchart format.
        
        Args:
            tier: Visibility tier (0=structural, 1=detailed). At tier 0,
                  slot edges are hidden and badges shown.
            node_badges: Optional dict mapping node_id to badge string
                        (e.g., {"main": "[3 slots]"}). Used at tier 0.
        
        Returns:
            Mermaid format string suitable for markdown embedding.
        """
        # Determine source directory for relative paths
        source_dir = sorted(self.files)[0].parent if self.files else None
        node_badges = node_badges or {}
        
        # Filter edges based on tier
        filtered_edges = self.edges
        if tier == Tier.STRUCTURAL:
            # At structural level, hide slot edges
            filtered_edges = frozenset(
                e for e in self.edges if e[2] != EdgeType.SLOT
            )
        
        lines = ["flowchart TB"]

        # Mermaid node IDs must be simple identifiers; file paths and other
        # punctuation will break parsing. We sanitize aggressively and de-dupe.
        used_ids: set[str] = set()
        id_map: dict[str, str] = {}
        display_map: dict[str, str] = {}  # original name -> display name

        def _escape_label(label: str) -> str:
            # Use quoted labels to allow characters like '/', '.', ':' safely.
            # Mermaid understands escaped quotes in labels.
            return (
                label
                .replace("\\", "\\\\")
                .replace('"', "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "")
            )

        def _get_display(name: str, include_badge: bool = False) -> str:
            """Get display name for a node (cached)."""
            if name not in display_map:
                display_map[name] = _make_display_name(name, source_dir)
            display = display_map[name]
            if include_badge:
                badge = node_badges.get(name, "")
                if badge:
                    display = f"{display} {badge}"
            return display

        def _make_id(name: str) -> str:
            if name in id_map:
                return id_map[name]

            display = _get_display(name)
            base = re.sub(r"[^0-9A-Za-z_]", "_", display)
            base = re.sub(r"_+", "_", base).strip("_")
            if not base:
                base = "node"
            if not re.match(r"[A-Za-z_]", base[0]):
                base = f"n_{base}"

            candidate = base
            if candidate in used_ids:
                digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]
                candidate = f"{base}_{digest}"
            while candidate in used_ids:
                digest = hashlib.sha1((name + candidate).encode("utf-8")).hexdigest()[:8]
                candidate = f"{base}_{digest}"

            used_ids.add(candidate)
            id_map[name] = candidate
            return candidate

        def _ensure_node_decl(name: str, include_badge: bool = True) -> None:
            safe_id = _make_id(name)
            display = _get_display(name, include_badge=include_badge)
            # Declare every node explicitly to avoid Mermaid auto-declaring
            # unknown IDs (which can differ between renderers).
            lines.append(f'    {safe_id}["{_escape_label(display)}"]')

        # Add nodes
        for node in sorted(self.nodes):
            # Skip file paths at tier 0 unless they're import targets
            if tier == Tier.STRUCTURAL and node.startswith('/'):
                is_import_target = any(
                    e[1] == node and e[2] == EdgeType.IMPORT
                    for e in filtered_edges
                )
                if not is_import_target:
                    continue
            _ensure_node_decl(node, include_badge=(tier == Tier.STRUCTURAL))
        
        # Add edges with different arrow styles
        arrow_styles = {
            EdgeType.BACKWARD_REF: "-->",    # solid arrow
            EdgeType.FORWARD_REF: "-.->",    # dotted arrow
            EdgeType.IMPORT: "==>",          # thick arrow
            EdgeType.SLOT: "-->",            # solid arrow
            EdgeType.CONTEXT_REF: "-..->",   # double-dotted arrow (file ref)
        }
        
        for from_id, to_id, edge_type in sorted(filtered_edges):
            if from_id not in id_map:
                _ensure_node_decl(from_id, include_badge=(tier == Tier.STRUCTURAL))
            if to_id not in id_map:
                _ensure_node_decl(to_id, include_badge=(tier == Tier.STRUCTURAL))
            safe_from = _make_id(from_id)
            safe_to = _make_id(to_id)
            arrow = arrow_styles.get(edge_type, "-->")
            lines.append(f"    {safe_from} {arrow}|{edge_type}| {safe_to}")
        
        return "\n".join(lines)
    
    def to_json(
        self,
        tier: int = 0,
        node_badges: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Export to JSON format.
        
        Args:
            tier: Visibility tier (0=structural, 1=detailed). At tier 0,
                  slot edges are hidden and badges included.
            node_badges: Optional dict mapping node_id to badge string.
        
        Returns:
            JSON string with nodes, edges, files, and file_refs.
        """
        # Determine source directory for relative paths
        source_dir = sorted(self.files)[0].parent if self.files else None
        node_badges = node_badges or {}
        
        # Filter edges based on tier
        filtered_edges = self.edges
        if tier == Tier.STRUCTURAL:
            filtered_edges = frozenset(
                e for e in self.edges if e[2] != EdgeType.SLOT
            )
        
        # Build nodes list with optional badges
        nodes_list = []
        for n in sorted(self.nodes):
            # Skip file paths at tier 0 unless they're import targets
            if tier == Tier.STRUCTURAL and n.startswith('/'):
                is_import_target = any(
                    e[1] == n and e[2] == EdgeType.IMPORT
                    for e in filtered_edges
                )
                if not is_import_target:
                    continue
            display = _make_display_name(n, source_dir)
            badge = node_badges.get(n, "") if tier == Tier.STRUCTURAL else ""
            nodes_list.append({"id": display, "badge": badge} if badge else display)
        
        data = {
            "tier": tier,
            "nodes": nodes_list,
            "edges": [
                {
                    "from": _make_display_name(from_id, source_dir),
                    "to": _make_display_name(to_id, source_dir),
                    "type": edge_type
                }
                for from_id, to_id, edge_type in sorted(filtered_edges)
            ],
            "files": [_make_display_name(str(f), source_dir) for f in sorted(self.files)],
            "file_refs": [_make_display_name(str(f), source_dir) for f in sorted(self.file_refs)],
        }
        return json.dumps(data, indent=2)
    
    @classmethod
    def empty(cls) -> "DependencyGraph":
        """Create an empty dependency graph."""
        return cls(
            nodes=frozenset(),
            edges=frozenset(),
            files=frozenset(),
        )
    
    @classmethod
    def merge(cls, *graphs: "DependencyGraph") -> "DependencyGraph":
        """
        Merge multiple dependency graphs into one.
        
        Used for cross-file graph merging when imports are involved.
        
        Args:
            graphs: Variable number of DependencyGraph instances to merge.
            
        Returns:
            A new DependencyGraph containing the union of all inputs.
        """
        all_nodes: Set[str] = set()
        all_edges: Set[tuple[str, str, str]] = set()
        all_files: Set[Path] = set()
        
        for graph in graphs:
            all_nodes.update(graph.nodes)
            all_edges.update(graph.edges)
            all_files.update(graph.files)
        
        return cls(
            nodes=frozenset(all_nodes),
            edges=frozenset(all_edges),
            files=frozenset(all_files),
        )
