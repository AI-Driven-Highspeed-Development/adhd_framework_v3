"""
Flow CLI - Command-line interface for Flow language operations.

Provides commands for tokenizing, parsing, resolving, compiling, and
analyzing Flow files including dependency graph visualization.

Commands:
    tokenize    - Tokenize a Flow file and display tokens
    parse       - Parse a Flow file and show AST structure
    resolve     - Resolve a Flow file and show resolved structure
    compile     - Compile a Flow file to Markdown
    graph       - Export dependency graph (DOT, JSON, Mermaid)
    validate    - Validate a Flow file with multi-error reporting
    impact      - Show all nodes affected if a given node changes
    usages      - Find all references to a node across files
    rename      - Rename a node across all files (dry-run by default)
    stats       - Show complexity metrics for a Flow file
    lsp         - Start the FLOW Language Server Protocol (LSP) server
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict, Set

from logger_util import Logger
from .flow_controller import FlowController
from .dependency_graph import DependencyGraph, EdgeType
from .errors import FlowError
from .models import FlowNode, NodeRef
from .resolver import Resolver, resolve_with_graph, validate_with_errors
from .tokenizer import Tokenizer
from .parser import Parser


# =============================================================================
# Result Helper
# =============================================================================

def _print_result(result: dict) -> int:
    """Print result as JSON and return exit code."""
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("success", True) else 1


# =============================================================================
# Handler Functions (cli_manager compatible)
# =============================================================================

def tokenize_command(args: argparse.Namespace) -> int:
    """
    Tokenize a Flow file and display the tokens.
    
    Args:
        args: Namespace with 'file' and optional 'verbose' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    verbose = getattr(args, 'verbose', False)
    logger = Logger(name="FlowCLI")
    
    try:
        controller = FlowController(logger=logger)
        tokens = controller.tokenize_file(Path(file_path))
        
        token_list = []
        for token in tokens:
            if verbose:
                token_list.append({
                    "type": token.type.name,
                    "value": token.value,
                    "line": token.line,
                    "column": token.column,
                })
            else:
                token_list.append({
                    "type": token.type.name,
                    "value": token.value,
                })
        
        return _print_result({
            "success": True,
            "file": file_path,
            "token_count": len(tokens),
            "tokens": token_list,
        })
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def parse_command(args: argparse.Namespace) -> int:
    """
    Parse a Flow file and display the AST structure.
    
    Args:
        args: Namespace with 'file' and optional 'verbose' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    verbose = getattr(args, 'verbose', False)
    logger = Logger(name="FlowCLI")
    
    try:
        controller = FlowController(logger=logger)
        path = Path(file_path)
        
        # Tokenize
        tokens = controller.tokenize_file(path)
        
        # Parse
        flow_file = controller.parse(tokens)
        
        result = {
            "success": True,
            "file": file_path,
            "nodes": list(flow_file.nodes.keys()),
            "import_count": len(flow_file.imports),
            "assignment_count": len(flow_file.assignments),
            "has_out": flow_file.out_node is not None,
        }
        
        if verbose:
            result["node_details"] = {
                node_id: {
                    "content_count": len(node.content),
                    "slot_count": len(node.slots),
                }
                for node_id, node in flow_file.nodes.items()
            }
        
        return _print_result(result)
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def resolve_command(args: argparse.Namespace) -> int:
    """
    Resolve a Flow file and display resolved structure.
    
    Args:
        args: Namespace with 'file' and optional 'verbose' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    verbose = getattr(args, 'verbose', False)
    logger = Logger(name="FlowCLI")
    
    try:
        controller = FlowController(logger=logger)
        path = Path(file_path)
        
        # Tokenize and parse
        tokens = controller.tokenize_file(path)
        flow_file = controller.parse(tokens)
        
        # Resolve
        resolved = controller.resolve(flow_file, base_path=path.parent, source_path=str(path))
        
        result = {
            "success": True,
            "file": file_path,
            "nodes": list(resolved.nodes.keys()),
            "dependency_order": resolved.dependency_order,
            "file_refs": resolved.file_refs,
            "has_out": resolved.out_node is not None,
        }
        
        if verbose:
            result["node_details"] = {
                node_id: len(resolved.nodes[node_id].content)
                for node_id in resolved.dependency_order
            }
        
        return _print_result(result)
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def compile_command(args: argparse.Namespace) -> int:
    """
    Compile a Flow file to Markdown.
    
    Args:
        args: Namespace with 'file' and optional 'output' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    output = getattr(args, 'output', None)
    logger = Logger(name="FlowCLI")
    
    try:
        controller = FlowController(logger=logger)
        path = Path(file_path)
        
        # Full compilation pipeline
        markdown = controller.compile_file(path)
        
        if output:
            output_path = Path(output)
            output_path.write_text(markdown, encoding="utf-8")
            return _print_result({
                "success": True,
                "file": file_path,
                "output": output,
                "message": f"Compiled {file_path} -> {output}"
            })
        else:
            # Direct markdown output (not JSON) for piping
            print(markdown)
        
        return 0
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def graph_command(args: argparse.Namespace) -> int:
    """
    Export dependency graph in DOT, JSON, or Mermaid format.
    
    Args:
        args: Namespace with 'file', optional 'format', and optional 'tier' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    format_type = getattr(args, 'format', 'mermaid')
    tier = getattr(args, 'tier', 0)
    logger = Logger(name="FlowCLI")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Flow file not found: {file_path}")
        
        # Read and parse
        source = path.read_text(encoding="utf-8")
        tokenizer = Tokenizer(logger=logger)
        tokens = tokenizer.tokenize(source)
        parser = Parser(logger=logger)
        flow_file = parser.parse(tokens)
        
        # Resolve with graph
        resolved, graph = resolve_with_graph(
            flow_file, 
            base_path=path.parent,
            source_path=str(path),
            logger=logger
        )
        
        # Build node badges for structural tier
        node_badges = {}
        if tier == 0:
            for node_id, node in resolved.nodes.items():
                if node.slot_badge:
                    node_badges[node_id] = node.slot_badge
        
        # Export in requested format (direct output for piping)
        if format_type == "dot":
            print(graph.to_dot(tier=tier, node_badges=node_badges))
        elif format_type == "json":
            print(graph.to_json(tier=tier, node_badges=node_badges))
        elif format_type == "mermaid":
            print(graph.to_mermaid(tier=tier, node_badges=node_badges))
        else:
            return _print_result({
                "success": False,
                "error": f"Unknown format: {format_type}. Use 'dot', 'json', or 'mermaid'."
            })
        
        return 0
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})

def validate_command(args: argparse.Namespace) -> int:
    """
    Validate a Flow file with multi-error reporting.
    
    Reports all validation errors found, not just the first one.
    
    Args:
        args: Namespace with 'file' attribute.
        
    Returns:
        Exit code (0 for valid, 1 for errors).
    """
    file_path = args.file
    logger = Logger(name="FlowCLI")
    errors: List[str] = []
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        # Read and tokenize
        source = path.read_text(encoding="utf-8")
        
        try:
            tokenizer = Tokenizer(logger=logger)
            tokens = tokenizer.tokenize(source)
        except FlowError as e:
            errors.append(f"Tokenizer: {e}")
            # Can't continue without tokens
            return _print_result({"success": False, "file": file_path, "errors": errors})
        
        # Parse
        try:
            parser = Parser(logger=logger)
            flow_file = parser.parse(tokens)
        except FlowError as e:
            errors.append(f"Parser: {e}")
            # Can't continue without AST
            return _print_result({"success": False, "file": file_path, "errors": errors})
        
        # Semantic validation (multi-error)
        semantic_errors = validate_with_errors(
            flow_file,
            base_path=path.parent,
            source_path=str(path),
            logger=logger,
        )
        for e in semantic_errors:
            errors.append(f"Resolver: {e}")
        
        # If we got here with no errors, validation passed
        if not errors:
            return _print_result({
                "success": True,
                "file": file_path,
                "message": f"✓ {file_path} is valid",
                "node_count": len(flow_file.nodes),
                "has_out": flow_file.out_node is not None,
            })
        else:
            return _print_result({"success": False, "file": file_path, "errors": errors})
        
    except Exception as e:
        return _print_result({"success": False, "error": f"Unexpected error: {e}"})


def inspect_command(args: argparse.Namespace) -> int:
    """
    Inspect a specific node's structure with optional slot details.
    
    Args:
        args: Namespace with 'file', 'node', and optional 'slots' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    node_name = args.node
    show_slots = getattr(args, 'slots', False)
    logger = Logger(name="FlowCLI")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        # Parse and resolve
        source = path.read_text(encoding="utf-8")
        tokenizer = Tokenizer(logger=logger)
        tokens = tokenizer.tokenize(source)
        parser = Parser(logger=logger)
        flow_file = parser.parse(tokens)
        
        # Check if node exists
        if node_name not in flow_file.nodes:
            return _print_result({
                "success": False,
                "error": f"Node @{node_name} not found",
                "available_nodes": list(flow_file.nodes.keys()),
            })
        
        node = flow_file.nodes[node_name]
        
        # Build result
        result = {
            "success": True,
            "file": file_path,
            "node": {
                "id": node.id,
                "layer": node.layer,
                "slot_count": node.slot_count,
                "slot_badge": node.slot_badge,
                "content_count": len(node.content),
                "params": {
                    "mutable": node.params.mutable,
                    "remutate": node.params.remutate,
                },
            },
        }
        
        # Add style info if present
        if node.params.style:
            style = node.params.style
            result["node"]["style"] = {
                "title": style.title,
                "divider": style.divider,
                "list_type": style.list_type,
                "wrap": style.wrap,
                "tag": style.tag,
                "summary": style.summary,
                "level": style.level,
                "level_offset": style.level_offset,
            }
        
        # Add slot details if requested
        if show_slots and node.slots:
            result["node"]["slots"] = {}
            for slot_id, slot_node in node.slots.items():
                slot_info = {
                    "id": slot_node.id,
                    "layer": slot_node.layer,
                    "content_count": len(slot_node.content),
                    "slot_count": slot_node.slot_count,
                }
                # Show content types
                content_types = []
                for item in slot_node.content:
                    if isinstance(item, str):
                        content_types.append("string")
                    elif hasattr(item, '__class__'):
                        content_types.append(item.__class__.__name__)
                slot_info["content_types"] = content_types
                result["node"]["slots"][slot_id] = slot_info
        
        # Add content overview
        content_types = []
        for item in node.content:
            if isinstance(item, str):
                content_types.append("string")
            elif hasattr(item, '__class__'):
                content_types.append(item.__class__.__name__)
        result["node"]["content_types"] = content_types
        
        return _print_result(result)
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def debug_command(args: argparse.Namespace) -> int:
    """
    Debug command for tracing slot mutations and insertions.
    
    Currently a stub - full mutation logging deferred to Phase 2.
    
    Args:
        args: Namespace with 'file' and optional 'trace_slots' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    trace_slots = getattr(args, 'trace_slots', False)
    logger = Logger(name="FlowCLI")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        # Parse and resolve
        source = path.read_text(encoding="utf-8")
        tokenizer = Tokenizer(logger=logger)
        tokens = tokenizer.tokenize(source)
        parser = Parser(logger=logger)
        flow_file = parser.parse(tokens)
        
        if trace_slots:
            # Collect all nodes with slots and any assignments
            nodes_with_slots = {}
            for node_id, node in flow_file.nodes.items():
                if node.slots:
                    nodes_with_slots[node_id] = {
                        "slot_count": node.slot_count,
                        "slots": list(node.slots.keys()),
                    }
            
            # Collect assignments (these show slot mutations)
            assignments = []
            for assignment in flow_file.assignments:
                assignments.append({
                    "target": assignment.target,
                    "source": assignment.source,
                    "position": {
                        "line": assignment.position.line if assignment.position else 0,
                        "column": assignment.position.column if assignment.position else 0,
                    }
                })
            
            return _print_result({
                "success": True,
                "file": file_path,
                "trace_slots": True,
                "nodes_with_slots": nodes_with_slots,
                "assignments": assignments,
                "note": "Full mutation logging deferred to Phase 2",
            })
        else:
            return _print_result({
                "success": True,
                "file": file_path,
                "message": "Use --trace-slots to trace slot mutations",
                "node_count": len(flow_file.nodes),
                "assignment_count": len(flow_file.assignments),
            })
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


# =============================================================================
# P2 Semantic Tooling Commands
# =============================================================================


def _collect_transitive_dependents(
    graph: "DependencyGraph", 
    node_id: str, 
    visited: Optional[Set[str]] = None
) -> Set[str]:
    """
    Recursively collect all nodes that depend on the given node.
    
    Args:
        graph: The dependency graph to traverse.
        node_id: The starting node to find dependents for.
        visited: Set of already visited nodes (to prevent cycles).
        
    Returns:
        Set of all node IDs that transitively depend on this node.
    """
    if visited is None:
        visited = set()
    
    if node_id in visited:
        return set()
    
    visited.add(node_id)
    
    direct_dependents = graph.dependents(node_id)
    all_dependents: Set[str] = set()
    
    for dep in direct_dependents:
        if dep not in visited:
            all_dependents.add(dep)
            all_dependents.update(_collect_transitive_dependents(graph, dep, visited))
    
    return all_dependents


def _is_node_id(name: str) -> bool:
    """
    Check if a name is a Flow node ID (not a file path or context ref).
    
    Node IDs are simple identifiers without path separators.
    
    Args:
        name: The name to check.
        
    Returns:
        True if this looks like a node ID, False if it looks like a path.
    """
    # File paths contain / or \ or start with . or have extensions
    if '/' in name or '\\' in name:
        return False
    if name.startswith('.'):
        return False
    # Check for file extensions (e.g., .md, .txt, .flow)
    if '.' in name and len(name.split('.')[-1]) <= 5:
        return False
    return True


def _get_node_source_file(graph: "DependencyGraph", node_id: str) -> Optional[str]:
    """
    Get the source file for a node by looking at import edges.
    
    Args:
        graph: The dependency graph.
        node_id: The node to find the source for.
        
    Returns:
        The source file path if found, None otherwise.
    """
    # Check if the node itself is a file path
    if node_id.startswith('/') or (len(node_id) > 2 and node_id[1] == ':'):
        return node_id
    
    # Look for import edges that point to this file
    for from_id, to_id, edge_type in graph.edges:
        if edge_type == EdgeType.IMPORT and from_id == node_id:
            # The 'to_id' is the file this node imports from
            return to_id
    
    # Default to first file in the graph if available
    if graph.files:
        return str(sorted(graph.files)[0])
    
    return None


def impact_command(args: argparse.Namespace) -> int:
    """
    Show all nodes that would be affected if a given node changes.
    
    Performs recursive traversal to find all transitive dependents.
    
    Args:
        args: Namespace with 'file' and 'node' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    node_id = args.node
    logger = Logger(name="FlowCLI")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        # Parse and resolve with graph
        source = path.read_text(encoding="utf-8")
        tokenizer = Tokenizer(logger=logger)
        tokens = tokenizer.tokenize(source)
        parser = Parser(logger=logger)
        flow_file = parser.parse(tokens)
        
        resolved, graph = resolve_with_graph(
            flow_file,
            base_path=path.parent,
            source_path=str(path),
            logger=logger
        )
        
        # Check if node exists
        if node_id not in graph.nodes:
            return _print_result({
                "success": False,
                "error": f"Node '{node_id}' not found in dependency graph",
                "available_nodes": sorted([n for n in graph.nodes if _is_node_id(n)]),
            })
        
        # Collect direct and transitive dependents
        direct_dependents = graph.dependents(node_id)
        all_dependents = _collect_transitive_dependents(graph, node_id)
        
        # Build affected list with source files
        affected = []
        for dep_id in sorted(all_dependents):
            source_file = _get_node_source_file(graph, dep_id)
            entry = {"node": dep_id, "direct": dep_id in direct_dependents}
            if source_file:
                # Use relative path if possible
                try:
                    rel_path = Path(source_file).relative_to(path.parent)
                    entry["file"] = str(rel_path)
                except ValueError:
                    entry["file"] = source_file
            affected.append(entry)
        
        return _print_result({
            "success": True,
            "file": file_path,
            "target_node": node_id,
            "direct_impact_count": len(direct_dependents),
            "total_impact_count": len(all_dependents),
            "affected": affected,
            "message": f"If '{node_id}' changes, {len(all_dependents)} node(s) would be affected",
        })
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except (IsADirectoryError, PermissionError, UnicodeDecodeError) as e:
        return _print_result({"success": False, "error": f"Cannot read file: {e}"})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def usages_command(args: argparse.Namespace) -> int:
    """
    Find all references to a node across files.
    
    Uses graph.edges_to() to find all nodes that reference the target.
    
    Args:
        args: Namespace with 'file' and 'node' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    node_id = args.node
    logger = Logger(name="FlowCLI")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        # Parse and resolve with graph
        source = path.read_text(encoding="utf-8")
        tokenizer = Tokenizer(logger=logger)
        tokens = tokenizer.tokenize(source)
        parser = Parser(logger=logger)
        flow_file = parser.parse(tokens)
        
        resolved, graph = resolve_with_graph(
            flow_file,
            base_path=path.parent,
            source_path=str(path),
            logger=logger
        )
        
        # Check if node exists
        if node_id not in graph.nodes:
            return _print_result({
                "success": False,
                "error": f"Node '{node_id}' not found in dependency graph",
                "available_nodes": sorted([n for n in graph.nodes if _is_node_id(n)]),
            })
        
        # Get all edges pointing to this node
        edges_to_node = graph.edges_to(node_id)
        
        # Build usage list grouped by reference type
        usages: List[Dict] = []
        for from_id, to_id, edge_type in sorted(edges_to_node):
            source_file = _get_node_source_file(graph, from_id)
            entry = {
                "referencing_node": from_id,
                "ref_type": edge_type,
            }
            if source_file:
                try:
                    rel_path = Path(source_file).relative_to(path.parent)
                    entry["file"] = str(rel_path)
                except ValueError:
                    entry["file"] = source_file
            usages.append(entry)
        
        return _print_result({
            "success": True,
            "file": file_path,
            "target_node": node_id,
            "usage_count": len(usages),
            "usages": usages,
            "message": f"Found {len(usages)} reference(s) to '{node_id}'",
        })
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except (IsADirectoryError, PermissionError, UnicodeDecodeError) as e:
        return _print_result({"success": False, "error": f"Cannot read file: {e}"})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def rename_command(args: argparse.Namespace) -> int:
    """
    Rename a node across all files.
    
    Performs regex-based rename: ($|^)old_id\\b → \\1new_id
    Dry-run by default, use --apply to actually write changes.
    
    Args:
        args: Namespace with 'file', 'old_id', 'new_id', and optional 'apply' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    old_id = args.old_id
    new_id = args.new_id
    apply_changes = getattr(args, 'apply', False)
    logger = Logger(name="FlowCLI")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        # Validate new_id format using Python's identifier rules (supports unicode)
        if not new_id.isidentifier():
            return _print_result({
                "success": False,
                "error": f"Invalid new identifier '{new_id}'. Must be a valid Python identifier.",
            })
        
        # Parse and resolve with graph to get all files
        source = path.read_text(encoding="utf-8")
        tokenizer = Tokenizer(logger=logger)
        tokens = tokenizer.tokenize(source)
        parser = Parser(logger=logger)
        flow_file = parser.parse(tokens)
        
        resolved, graph = resolve_with_graph(
            flow_file,
            base_path=path.parent,
            source_path=str(path),
            logger=logger
        )
        
        # Check if old_id exists
        if old_id not in graph.nodes:
            return _print_result({
                "success": False,
                "error": f"Node '{old_id}' not found in dependency graph",
                "available_nodes": sorted([n for n in graph.nodes if _is_node_id(n)]),
            })
        
        # Check if new_id already exists
        if new_id in graph.nodes:
            return _print_result({
                "success": False,
                "error": f"Node '{new_id}' already exists. Cannot rename to existing node.",
            })
        
        # Pattern to match references and definitions
        # Matches: @old_id, $old_id, ^old_id (with word boundary)
        ref_pattern = re.compile(r'([@$^])' + re.escape(old_id) + r'\b')
        
        # Collect all files to process (use resolved paths to avoid duplicates)
        resolved_path = path.resolve()
        files_to_check: List[Path] = [resolved_path]
        seen_files: Set[Path] = {resolved_path}
        for f in graph.files:
            resolved_f = f.resolve() if f.exists() else f
            if resolved_f not in seen_files and resolved_f.exists():
                files_to_check.append(resolved_f)
                seen_files.add(resolved_f)
        
        # Find and optionally apply changes
        changes: List[Dict] = []
        total_refs = 0
        
        for check_path in files_to_check:
            try:
                file_source = check_path.read_text(encoding="utf-8")
            except Exception:
                continue
            
            # Find all matches in this file
            file_refs = []
            new_lines = []
            modified = False
            
            for line_num, line in enumerate(file_source.split('\n'), start=1):
                matches = list(ref_pattern.finditer(line))
                if matches:
                    for match in matches:
                        file_refs.append({
                            "line": line_num,
                            "column": match.start() + 1,
                            "old_text": match.group(0),
                            "new_text": match.group(1) + new_id,
                        })
                        total_refs += 1
                    # Replace in line
                    new_line = ref_pattern.sub(r'\g<1>' + new_id, line)
                    new_lines.append(new_line)
                    modified = True
                else:
                    new_lines.append(line)
            
            if file_refs:
                rel_path = str(check_path)
                try:
                    rel_path = str(check_path.relative_to(path.parent))
                except ValueError:
                    pass
                
                changes.append({
                    "file": rel_path,
                    "refs_updated": len(file_refs),
                    "refs": file_refs,
                })
                
                # Apply changes if requested
                if apply_changes and modified:
                    check_path.write_text('\n'.join(new_lines), encoding='utf-8')
        
        result = {
            "success": True,
            "file": file_path,
            "old_id": old_id,
            "new_id": new_id,
            "files_affected": len(changes),
            "total_refs_updated": total_refs,
            "applied": apply_changes,
            "changes": changes,
        }
        
        if apply_changes:
            result["message"] = f"Renamed '{old_id}' → '{new_id}' across {len(changes)} file(s), {total_refs} reference(s) updated"
        else:
            result["message"] = f"Dry-run: would rename '{old_id}' → '{new_id}' across {len(changes)} file(s), {total_refs} reference(s). Use --apply to execute."
        
        return _print_result(result)
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except (IsADirectoryError, PermissionError, UnicodeDecodeError) as e:
        return _print_result({"success": False, "error": f"Cannot read file: {e}"})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def _calculate_max_nesting(node: FlowNode, current_depth: int = 0) -> int:
    """
    Calculate maximum nesting depth of a node.
    
    Args:
        node: The FlowNode to analyze.
        current_depth: Current nesting level.
        
    Returns:
        Maximum nesting depth found.
    """
    max_depth = current_depth
    
    # Check slots
    for slot_node in node.slots.values():
        slot_depth = _calculate_max_nesting(slot_node, current_depth + 1)
        max_depth = max(max_depth, slot_depth)
    
    # Check nested nodes in content
    for item in node.content:
        if isinstance(item, FlowNode):
            nested_depth = _calculate_max_nesting(item, current_depth + 1)
            max_depth = max(max_depth, nested_depth)
    
    return max_depth


def _count_refs_in_node(node: FlowNode) -> int:
    """
    Count the number of references ($, ^) in a node's content.
    
    Args:
        node: The FlowNode to analyze.
        
    Returns:
        Number of references found.
    """
    count = 0
    for item in node.content:
        if isinstance(item, NodeRef):
            count += 1
        elif isinstance(item, FlowNode):
            count += _count_refs_in_node(item)
    
    # Also check slots
    for slot_node in node.slots.values():
        count += _count_refs_in_node(slot_node)
    
    return count


def _estimate_tokens(source: str) -> int:
    """
    Estimate token count using char/4 heuristic.
    
    Args:
        source: The source text.
        
    Returns:
        Estimated token count.
    """
    return len(source) // 4


def stats_command(args: argparse.Namespace) -> int:
    """
    Show complexity metrics for a Flow file.
    
    Calculates: token count, node count, reference count, max nesting, import count.
    
    Args:
        args: Namespace with 'file' and optional 'format' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    file_path = args.file
    output_format = getattr(args, 'format', 'json')
    logger = Logger(name="FlowCLI")
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        source = path.read_text(encoding="utf-8")
        
        # Tokenize and parse
        tokenizer = Tokenizer(logger=logger)
        tokens = tokenizer.tokenize(source)
        parser = Parser(logger=logger)
        flow_file = parser.parse(tokens)
        
        # Calculate metrics
        total_nodes = len(flow_file.nodes)
        import_count = len(flow_file.imports)
        assignment_count = len(flow_file.assignments)
        token_estimate = _estimate_tokens(source)
        
        # Per-node metrics
        node_stats: Dict[str, Dict] = {}
        total_refs = 0
        max_nesting = 0
        total_slot_count = 0
        
        for node_id, node in flow_file.nodes.items():
            node_refs = _count_refs_in_node(node)
            node_nesting = _calculate_max_nesting(node)
            node_slots = node.slot_count
            
            total_refs += node_refs
            max_nesting = max(max_nesting, node_nesting)
            total_slot_count += node_slots
            
            # Estimate node content size (char count / 4)
            content_chars = 0
            for item in node.content:
                if isinstance(item, str):
                    content_chars += len(item)
            
            node_stats[node_id] = {
                "layer": node.layer,
                "slot_count": node_slots,
                "ref_count": node_refs,
                "nesting_depth": node_nesting,
                "content_tokens": content_chars // 4,
            }
        
        # Build result
        result = {
            "success": True,
            "file": file_path,
            "metrics": {
                "token_estimate": token_estimate,
                "node_count": total_nodes,
                "import_count": import_count,
                "assignment_count": assignment_count,
                "total_refs": total_refs,
                "total_slots": total_slot_count,
                "max_nesting_depth": max_nesting,
                "has_out": flow_file.out_node is not None,
            },
            "node_stats": node_stats,
        }
        
        if output_format == "table":
            # Print as table format (human-readable)
            print(f"Flow File Statistics: {file_path}")
            print("=" * 60)
            print(f"  Token estimate (chars/4):  {token_estimate:,}")
            print(f"  Node count:                {total_nodes}")
            print(f"  Import count:              {import_count}")
            print(f"  Assignment count:          {assignment_count}")
            print(f"  Total references:          {total_refs}")
            print(f"  Total slots:               {total_slot_count}")
            print(f"  Max nesting depth:         {max_nesting}")
            print(f"  Has @out:                  {'Yes' if flow_file.out_node else 'No'}")
            print()
            print("Per-Node Statistics:")
            print("-" * 60)
            print(f"  {'Node':<20} {'Layer':>6} {'Slots':>6} {'Refs':>6} {'Depth':>6}")
            print("-" * 60)
            for node_id, stats in sorted(node_stats.items()):
                print(f"  {node_id:<20} {stats['layer']:>6} {stats['slot_count']:>6} {stats['ref_count']:>6} {stats['nesting_depth']:>6}")
            return 0
        else:
            return _print_result(result)
        
    except FileNotFoundError as e:
        return _print_result({"success": False, "error": str(e)})
    except (IsADirectoryError, PermissionError, UnicodeDecodeError) as e:
        return _print_result({"success": False, "error": f"Cannot read file: {e}"})
    except FlowError as e:
        return _print_result({"success": False, "error": f"Flow error: {e}"})


def validate_unused_command(args: argparse.Namespace) -> int:
    """
    Validate a Flow file and warn about unused (orphan) nodes.
    
    Detects dead code: nodes defined but never referenced.
    
    Args:
        args: Namespace with 'file' attribute.
        
    Returns:
        Exit code (0 for valid, 1 for errors/warnings).
    """
    file_path = args.file
    warn_unused = getattr(args, 'warn_unused', False)
    logger = Logger(name="FlowCLI")
    errors: List[str] = []
    warnings: List[str] = []
    
    try:
        path = Path(file_path)
        
        if not path.exists():
            return _print_result({"success": False, "error": f"Flow file not found: {file_path}"})
        
        # Read and tokenize
        source = path.read_text(encoding="utf-8")
        
        try:
            tokenizer = Tokenizer(logger=logger)
            tokens = tokenizer.tokenize(source)
        except FlowError as e:
            errors.append(f"Tokenizer: {e}")
            return _print_result({"success": False, "file": file_path, "errors": errors})
        
        # Parse
        try:
            parser = Parser(logger=logger)
            flow_file = parser.parse(tokens)
        except FlowError as e:
            errors.append(f"Parser: {e}")
            return _print_result({"success": False, "file": file_path, "errors": errors})
        
        # Semantic validation (multi-error)
        semantic_errors = validate_with_errors(
            flow_file,
            base_path=path.parent,
            source_path=str(path),
            logger=logger,
        )
        for e in semantic_errors:
            errors.append(f"Resolver: {e}")
        
        # Check for unused nodes if requested
        unused_nodes: List[str] = []
        if warn_unused and not errors:
            # Resolve with graph to analyze dependencies
            resolved, graph = resolve_with_graph(
                flow_file,
                base_path=path.parent,
                source_path=str(path),
                logger=logger
            )
            
            # Find all defined nodes (excluding @out)
            defined_nodes = set(flow_file.nodes.keys())
            if 'out' in defined_nodes:
                defined_nodes.remove('out')
            
            # Find all referenced nodes (nodes that are targets of edges)
            referenced_nodes: Set[str] = set()
            for from_id, to_id, edge_type in graph.edges:
                # Only count references within the graph (not file paths)
                if not to_id.startswith('/') and edge_type in [EdgeType.BACKWARD_REF, EdgeType.FORWARD_REF, EdgeType.SLOT]:
                    referenced_nodes.add(to_id)
            
            # Also consider nodes referenced via @out
            if flow_file.out_node:
                # The out node itself uses all its content nodes
                def collect_refs_from_node(node: FlowNode) -> Set[str]:
                    refs: Set[str] = set()
                    for item in node.content:
                        if isinstance(item, NodeRef):
                            refs.add(item.id.split('.')[0])  # Handle slot refs
                        elif isinstance(item, FlowNode):
                            refs.update(collect_refs_from_node(item))
                    for slot_node in node.slots.values():
                        refs.update(collect_refs_from_node(slot_node))
                    return refs
                
                referenced_nodes.update(collect_refs_from_node(flow_file.out_node))
            
            # Find orphan nodes
            unused_nodes = sorted(defined_nodes - referenced_nodes - {'out'})
            
            for orphan in unused_nodes:
                warnings.append(f"Unused node: @{orphan} is defined but never referenced")
        
        # Build result
        if not errors and not warnings:
            return _print_result({
                "success": True,
                "file": file_path,
                "message": f"✓ {file_path} is valid",
                "node_count": len(flow_file.nodes),
                "has_out": flow_file.out_node is not None,
            })
        elif errors:
            return _print_result({
                "success": False, 
                "file": file_path, 
                "errors": errors,
                "warnings": warnings if warnings else None,
            })
        else:
            # Warnings only
            return _print_result({
                "success": True,
                "file": file_path,
                "message": f"✓ {file_path} is valid with {len(warnings)} warning(s)",
                "node_count": len(flow_file.nodes),
                "has_out": flow_file.out_node is not None,
                "warnings": warnings,
                "unused_nodes": unused_nodes,
            })
        
    except Exception as e:
        return _print_result({"success": False, "error": f"Unexpected error: {e}"})


def lsp_command(args: argparse.Namespace) -> int:
    """
    Start the FLOW Language Server Protocol (LSP) server.
    
    Args:
        args: Namespace with 'tcp', 'host', 'port' attributes.
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    from .flow_lsp import start_server
    
    logger = Logger(name="FlowCLI")
    
    try:
        transport = "tcp" if getattr(args, 'tcp', False) else "stdio"
        host = getattr(args, 'host', '127.0.0.1')
        port = getattr(args, 'port', 2087)
        
        logger.info(f"Starting FLOW LSP server ({transport})")
        if transport == "tcp":
            logger.info(f"Listening on {host}:{port}")
        
        start_server(
            transport=transport,
            host=host,
            port=port,
            logger=logger,
        )
        return 0
    except Exception as e:
        return _print_result({"success": False, "error": f"LSP server error: {e}"})


# =============================================================================
# CLI Registration (cli_manager integration)
# =============================================================================

def register_cli() -> None:
    """Register flow_core commands with CLIManager."""
    from cli_manager import CLIManager, ModuleRegistration, Command, CommandArg
    
    cli = CLIManager()
    cli.register_module(ModuleRegistration(
        module_name="flow_core",
        short_name="flow",
        description="Flow language compiler - tokenize, parse, resolve, compile, graph, validate",
        commands=[
            Command(
                name="tokenize",
                help="Tokenize a Flow file and display tokens",
                handler="flow_core.flow_cli:tokenize_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--verbose", short="-v", action="store_true", help="Show detailed token info"),
                ],
            ),
            Command(
                name="parse",
                help="Parse a Flow file and show AST structure",
                handler="flow_core.flow_cli:parse_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--verbose", short="-v", action="store_true", help="Show detailed AST info"),
                ],
            ),
            Command(
                name="resolve",
                help="Resolve a Flow file and show resolved structure",
                handler="flow_core.flow_cli:resolve_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--verbose", short="-v", action="store_true", help="Show detailed resolution info"),
                ],
            ),
            Command(
                name="compile",
                help="Compile a Flow file to Markdown",
                handler="flow_core.flow_cli:compile_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--output", short="-o", help="Output file path"),
                ],
            ),
            Command(
                name="graph",
                help="Export dependency graph (DOT, JSON, Mermaid)",
                handler="flow_core.flow_cli:graph_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--format", short="-f", default="mermaid", 
                              choices=["dot", "json", "mermaid"], help="Output format"),
                    CommandArg(name="--tier", short="-t", default="0",
                              choices=["0", "1"], help="Visibility tier (0=structural, 1=detailed)"),
                ],
            ),
            Command(
                name="validate",
                help="Validate a Flow file with multi-error reporting",
                handler="flow_core.flow_cli:validate_unused_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--warn-unused", action="store_true",
                              help="Warn about nodes defined but never referenced (dead code)"),
                ],
            ),
            Command(
                name="inspect",
                help="Inspect a specific node's structure with optional slot details",
                handler="flow_core.flow_cli:inspect_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="node", help="Node name to inspect (without @)"),
                    CommandArg(name="--slots", short="-s", action="store_true", 
                              help="Show detailed slot information"),
                ],
            ),
            Command(
                name="debug",
                help="Debug command for tracing slot mutations",
                handler="flow_core.flow_cli:debug_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--trace-slots", action="store_true",
                              help="Trace slot mutations and insertions"),
                ],
            ),
            Command(
                name="impact",
                help="Show all nodes affected if a given node changes",
                handler="flow_core.flow_cli:impact_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="node", help="Node name to analyze impact for (without @)"),
                ],
            ),
            Command(
                name="usages",
                help="Find all references to a node across files",
                handler="flow_core.flow_cli:usages_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="node", help="Node name to find usages for (without @)"),
                ],
            ),
            Command(
                name="rename",
                help="Rename a node across all files (dry-run by default)",
                handler="flow_core.flow_cli:rename_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="old_id", help="Current node name (without @)"),
                    CommandArg(name="new_id", help="New node name (without @)"),
                    CommandArg(name="--apply", action="store_true",
                              help="Actually apply the rename (default is dry-run)"),
                ],
            ),
            Command(
                name="stats",
                help="Show complexity metrics for a Flow file",
                handler="flow_core.flow_cli:stats_command",
                args=[
                    CommandArg(name="file", help="Path to the .flow file"),
                    CommandArg(name="--format", short="-f", default="json",
                              choices=["json", "table"], help="Output format"),
                ],
            ),
            Command(
                name="lsp",
                help="Start the FLOW Language Server Protocol (LSP) server",
                handler="flow_core.flow_cli:lsp_command",
                args=[
                    CommandArg(name="--tcp", action="store_true",
                              help="Use TCP transport instead of stdio"),
                    CommandArg(name="--host", default="127.0.0.1",
                              help="Host for TCP mode (default: 127.0.0.1)"),
                    CommandArg(name="--port", type="int", default=2087,
                              help="Port for TCP mode (default: 2087)"),
                ],
            ),
        ],
    ))


if __name__ == "__main__":
    register_cli()
