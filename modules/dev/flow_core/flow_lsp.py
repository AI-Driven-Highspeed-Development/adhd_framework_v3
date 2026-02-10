"""
Flow Language LSP Server (P2.6)

Provides Language Server Protocol support for FLOW files:
- Diagnostics: Real-time error reporting
- Completion: Autocomplete for $node_id references (trigger on $)
- Go-to-Definition: Jump to node definitions

Usage:
    python -m flow_core.flow_lsp
    # Or via CLI:
    python flow_cli.py lsp [--tcp|--stdio] [--port 2087]

Protocol: LSP 3.17
Library: pygls >= 1.0.0
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Dict, List, Set
from urllib.parse import unquote

from lsprotocol import types as lsp
from pygls.lsp.server import LanguageServer
from pygls.workspace import TextDocument

from logger_util import Logger
from .tokenizer import Tokenizer
from .parser import Parser
from .resolver import Resolver, validate_with_errors
from .models import FlowFile, FlowNode, Position, NodeRef
from .errors import FlowError


# =============================================================================
# LSP Server Configuration
# =============================================================================

FLOW_LANGUAGE_ID = "flow"
SERVER_NAME = "flow-lsp"
SERVER_VERSION = "0.1.0"


class FlowLanguageServer(LanguageServer):
    """
    Language Server for the FLOW language.
    
    Provides diagnostics, completion, and go-to-definition support.
    Maintains a cache of parsed files for efficient incremental updates.
    """
    
    def __init__(self, logger: Optional[Logger] = None) -> None:
        super().__init__(name=SERVER_NAME, version=SERVER_VERSION)
        self.logger = logger or Logger(name="FlowLSP")
        
        # Cache for parsed files: uri -> (version, FlowFile, node_positions)
        self._file_cache: Dict[str, tuple[int, FlowFile, Dict[str, Position]]] = {}
        
        # Tokenizer, parser, resolver instances
        self._tokenizer = Tokenizer(logger=self.logger)
        self._parser = Parser(logger=self.logger)
        self._resolver = Resolver(logger=self.logger)
    
    def get_file_path(self, uri: str) -> Path:
        """Convert a file URI to a Path."""
        if uri.startswith("file://"):
            return Path(unquote(uri[7:]))
        return Path(uri)
    
    def _cache_flow_file(
        self, uri: str, version: int, flow_file: FlowFile
    ) -> Dict[str, Position]:
        """
        Build node positions map and cache the parsed FlowFile.
        
        Args:
            uri: The document URI.
            version: The document version.
            flow_file: The parsed FlowFile object.
            
        Returns:
            Dictionary mapping node IDs to their positions.
        """
        node_positions: Dict[str, Position] = {}
        for node_id, node in flow_file.nodes.items():
            if node.position:
                node_positions[node_id] = node.position
        
        self._file_cache[uri] = (version, flow_file, node_positions)
        return node_positions
    
    def parse_document(self, document: TextDocument) -> Optional[FlowFile]:
        """
        Parse a document and cache the result.
        
        Returns None if parsing fails.
        """
        try:
            source = document.source
            tokens = self._tokenizer.tokenize(source)
            flow_file = self._parser.parse(tokens)
            
            # Cache the result
            self._cache_flow_file(document.uri, document.version, flow_file)
            
            return flow_file
        except FlowError as e:
            self.logger.debug(f"Parse error in {document.uri}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected parse error in {document.uri}: {e}")
            return None
    
    def get_cached_file(self, uri: str) -> Optional[tuple[FlowFile, Dict[str, Position]]]:
        """Get a cached FlowFile if available."""
        if uri in self._file_cache:
            _, flow_file, node_positions = self._file_cache[uri]
            return flow_file, node_positions
        return None
    
    def get_all_node_ids(self, uri: str) -> Set[str]:
        """
        Get all available node IDs for a document.
        
        Includes both local nodes and imported nodes.
        """
        cached = self.get_cached_file(uri)
        if cached:
            flow_file, _ = cached
            return set(flow_file.nodes.keys())
        return set()
    
    def find_node_definition(
        self, uri: str, node_id: str
    ) -> Optional[tuple[str, Position]]:
        """
        Find the definition location of a node.
        
        Args:
            uri: The document URI to search from.
            node_id: The node ID to find (without $ or ^ prefix).
            
        Returns:
            Tuple of (uri, Position) if found, None otherwise.
        """
        cached = self.get_cached_file(uri)
        if cached:
            flow_file, node_positions = cached
            
            # Check local nodes first
            if node_id in node_positions:
                return uri, node_positions[node_id]
            
            # TODO: Handle imported nodes by resolving imports
            # For now, only handle local definitions
        
        return None


# =============================================================================
# Create Server Instance
# =============================================================================

server = FlowLanguageServer()


# =============================================================================
# Document Synchronization
# =============================================================================

@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: FlowLanguageServer, params: lsp.DidOpenTextDocumentParams) -> None:
    """Handle document open event."""
    document = ls.workspace.get_text_document(params.text_document.uri)
    ls.logger.debug(f"Document opened: {params.text_document.uri}")
    
    # Parse and publish diagnostics
    _publish_diagnostics(ls, document)


@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: FlowLanguageServer, params: lsp.DidChangeTextDocumentParams) -> None:
    """Handle document change event."""
    document = ls.workspace.get_text_document(params.text_document.uri)
    ls.logger.debug(f"Document changed: {params.text_document.uri}")
    
    # Reparse and publish diagnostics
    _publish_diagnostics(ls, document)


@server.feature(lsp.TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls: FlowLanguageServer, params: lsp.DidCloseTextDocumentParams) -> None:
    """Handle document close event."""
    uri = params.text_document.uri
    ls.logger.debug(f"Document closed: {uri}")
    
    # Clear cache
    if uri in ls._file_cache:
        del ls._file_cache[uri]
    
    # Clear diagnostics
    ls.publish_diagnostics(uri, [])


# =============================================================================
# Diagnostics
# =============================================================================

def _publish_diagnostics(ls: FlowLanguageServer, document: TextDocument) -> None:
    """
    Parse document and publish diagnostics.
    
    Collects errors from tokenizer, parser, and resolver stages.
    """
    diagnostics: List[lsp.Diagnostic] = []
    uri = document.uri
    source = document.source
    
    try:
        # Stage 1: Tokenize
        tokens = ls._tokenizer.tokenize(source)
        
        # Stage 2: Parse
        flow_file = ls._parser.parse(tokens)
        
        # Cache the successful parse
        ls._cache_flow_file(uri, document.version, flow_file)
        
        # Stage 3: Validate semantics
        file_path = ls.get_file_path(uri)
        errors = validate_with_errors(
            flow_file,
            base_path=file_path.parent,
            source_path=str(file_path),
            logger=ls.logger,
        )
        
        for error in errors:
            diagnostics.append(_flow_error_to_diagnostic(error))
    
    except FlowError as e:
        # Tokenizer or parser error
        diagnostics.append(_flow_error_to_diagnostic(e))
    except Exception as e:
        # Unexpected error - report at beginning of file
        diagnostics.append(lsp.Diagnostic(
            range=lsp.Range(
                start=lsp.Position(line=0, character=0),
                end=lsp.Position(line=0, character=1),
            ),
            message=f"Internal error: {e}",
            severity=lsp.DiagnosticSeverity.Error,
            source="flow-lsp",
        ))
    
    ls.publish_diagnostics(uri, diagnostics)


def _flow_error_to_diagnostic(error: FlowError) -> lsp.Diagnostic:
    """Convert a FlowError to an LSP Diagnostic."""
    # LSP uses 0-based line numbers, FlowError uses 1-based
    line = max(0, error.line - 1)
    column = max(0, error.column - 1)
    
    return lsp.Diagnostic(
        range=lsp.Range(
            start=lsp.Position(line=line, character=column),
            end=lsp.Position(line=line, character=column + 10),  # Approximate span
        ),
        message=str(error),
        severity=lsp.DiagnosticSeverity.Error,
        source="flow",
    )


# =============================================================================
# Completion
# =============================================================================

@server.feature(
    lsp.TEXT_DOCUMENT_COMPLETION,
    lsp.CompletionOptions(
        trigger_characters=["$", "^"],
        resolve_provider=False,
    ),
)
def completion(
    ls: FlowLanguageServer, params: lsp.CompletionParams
) -> Optional[lsp.CompletionList]:
    """
    Provide completion suggestions for node references.
    
    Triggers on '$' for backward references and '^' for forward references.
    """
    document = ls.workspace.get_text_document(params.text_document.uri)
    position = params.position
    
    # Get the current line text
    lines = document.source.split("\n")
    if position.line >= len(lines):
        return None
    
    current_line = lines[position.line]
    
    # Check if we're completing a node reference
    # Look backwards from cursor position to find $ or ^
    char_pos = position.character
    if char_pos > len(current_line):
        char_pos = len(current_line)
    
    prefix_text = current_line[:char_pos]
    
    # Find the trigger character and partial id
    match = re.search(r'([$^])([a-zA-Z_][a-zA-Z0-9_]*)?$', prefix_text)
    if not match:
        return None
    
    trigger = match.group(1)
    partial_id = match.group(2) or ""
    
    ls.logger.debug(f"Completion triggered: trigger={trigger}, partial={partial_id}")
    
    # Get available node IDs
    node_ids = ls.get_all_node_ids(document.uri)
    
    # Filter by partial match
    completions: List[lsp.CompletionItem] = []
    for node_id in sorted(node_ids):
        if node_id.startswith(partial_id):
            # Determine completion kind based on trigger
            is_forward = trigger == "^"
            kind = lsp.CompletionItemKind.Reference
            
            # Calculate the range to replace (including the partial id typed)
            start_char = char_pos - len(partial_id)
            
            completions.append(lsp.CompletionItem(
                label=node_id,
                kind=kind,
                detail=f"{'Forward' if is_forward else 'Backward'} reference to @{node_id}",
                insert_text=node_id,
                text_edit=lsp.TextEdit(
                    range=lsp.Range(
                        start=lsp.Position(line=position.line, character=start_char),
                        end=lsp.Position(line=position.line, character=char_pos),
                    ),
                    new_text=node_id,
                ),
            ))
    
    return lsp.CompletionList(is_incomplete=False, items=completions)


# =============================================================================
# Go-to-Definition
# =============================================================================

@server.feature(lsp.TEXT_DOCUMENT_DEFINITION)
def goto_definition(
    ls: FlowLanguageServer, params: lsp.DefinitionParams
) -> Optional[lsp.Location]:
    """
    Jump to the definition of a node reference.
    
    Works with $node_id and ^node_id references.
    """
    document = ls.workspace.get_text_document(params.text_document.uri)
    position = params.position
    
    # Get the node reference at the cursor position
    node_id = _get_node_ref_at_position(document, position)
    if not node_id:
        ls.logger.debug("No node reference found at position")
        return None
    
    ls.logger.debug(f"Looking up definition for: {node_id}")
    
    # Find the definition
    result = ls.find_node_definition(document.uri, node_id)
    if not result:
        ls.logger.debug(f"Definition not found for: {node_id}")
        return None
    
    def_uri, def_pos = result
    
    # Convert to LSP Location (0-based line numbers)
    return lsp.Location(
        uri=def_uri,
        range=lsp.Range(
            start=lsp.Position(line=def_pos.line - 1, character=def_pos.column - 1),
            end=lsp.Position(line=def_pos.line - 1, character=def_pos.column - 1 + len(node_id) + 1),  # +1 for @
        ),
    )


def _get_node_ref_at_position(
    document: TextDocument, position: lsp.Position
) -> Optional[str]:
    """
    Extract the node ID from a reference at the given position.
    
    Returns the node ID (without $ or ^ prefix) if the cursor is on a reference.
    """
    lines = document.source.split("\n")
    if position.line >= len(lines):
        return None
    
    line = lines[position.line]
    char = position.character
    
    # Find all node references in the line: $id or ^id
    # Also handle $id.slot syntax
    pattern = r'([$^])([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)'
    
    for match in re.finditer(pattern, line):
        start = match.start()
        end = match.end()
        
        # Check if cursor is within this reference
        if start <= char <= end:
            full_id = match.group(2)
            # Return just the base node ID (before any dot)
            return full_id.split(".")[0]
    
    return None


# =============================================================================
# Hover (Bonus Feature)
# =============================================================================

@server.feature(lsp.TEXT_DOCUMENT_HOVER)
def hover(
    ls: FlowLanguageServer, params: lsp.HoverParams
) -> Optional[lsp.Hover]:
    """
    Show hover information for node references and definitions.
    """
    document = ls.workspace.get_text_document(params.text_document.uri)
    position = params.position
    lines = document.source.split("\n")
    
    if position.line >= len(lines):
        return None
    
    line = lines[position.line]
    char = position.character
    
    # Check for node definition @id
    def_pattern = r'@([a-zA-Z_][a-zA-Z0-9_]*)'
    for match in re.finditer(def_pattern, line):
        start = match.start()
        end = match.end()
        if start <= char <= end:
            node_id = match.group(1)
            cached = ls.get_cached_file(document.uri)
            if cached:
                flow_file, _ = cached
                if node_id in flow_file.nodes:
                    node = flow_file.nodes[node_id]
                    content_preview = _get_node_content_preview(node)
                    slots_info = f"Slots: {list(node.slots.keys())}" if node.slots else "No slots"
                    
                    return lsp.Hover(
                        contents=lsp.MarkupContent(
                            kind=lsp.MarkupKind.Markdown,
                            value=f"**Node @{node_id}**\n\nLayer: {node.layer}\n\n{slots_info}\n\n{content_preview}",
                        ),
                        range=lsp.Range(
                            start=lsp.Position(line=position.line, character=start),
                            end=lsp.Position(line=position.line, character=end),
                        ),
                    )
    
    # Check for node reference $id or ^id
    ref_pattern = r'([$^])([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)'
    for match in re.finditer(ref_pattern, line):
        start = match.start()
        end = match.end()
        if start <= char <= end:
            prefix = match.group(1)
            full_id = match.group(2)
            base_id = full_id.split(".")[0]
            
            ref_type = "Forward reference" if prefix == "^" else "Backward reference"
            
            cached = ls.get_cached_file(document.uri)
            if cached:
                flow_file, _ = cached
                if base_id in flow_file.nodes:
                    node = flow_file.nodes[base_id]
                    content_preview = _get_node_content_preview(node)
                    
                    return lsp.Hover(
                        contents=lsp.MarkupContent(
                            kind=lsp.MarkupKind.Markdown,
                            value=f"**{ref_type}** to `@{base_id}`\n\n{content_preview}",
                        ),
                        range=lsp.Range(
                            start=lsp.Position(line=position.line, character=start),
                            end=lsp.Position(line=position.line, character=end),
                        ),
                    )
            
            return lsp.Hover(
                contents=lsp.MarkupContent(
                    kind=lsp.MarkupKind.Markdown,
                    value=f"**{ref_type}** to `@{base_id}`",
                ),
                range=lsp.Range(
                    start=lsp.Position(line=position.line, character=start),
                    end=lsp.Position(line=position.line, character=end),
                ),
            )
    
    return None


def _get_node_content_preview(node: FlowNode, max_length: int = 100) -> str:
    """Get a preview of node content for hover display."""
    content_parts: List[str] = []
    
    for item in node.content:
        if isinstance(item, str):
            # Truncate long strings
            text = item.strip()
            if len(text) > max_length:
                text = text[:max_length] + "..."
            content_parts.append(text)
        elif isinstance(item, NodeRef):
            prefix = "^" if item.is_forward else "$"
            content_parts.append(f"`{prefix}{item.id}`")
    
    if not content_parts:
        return "_Empty node_"
    
    preview = " ".join(content_parts)
    if len(preview) > max_length:
        preview = preview[:max_length] + "..."
    
    return f"```\n{preview}\n```"


# =============================================================================
# Document Symbols
# =============================================================================

@server.feature(lsp.TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def document_symbols(
    ls: FlowLanguageServer, params: lsp.DocumentSymbolParams
) -> Optional[List[lsp.DocumentSymbol]]:
    """
    Provide document outline with node definitions.
    """
    document = ls.workspace.get_text_document(params.text_document.uri)
    cached = ls.get_cached_file(document.uri)
    
    if not cached:
        # Try to parse
        ls.parse_document(document)
        cached = ls.get_cached_file(document.uri)
        if not cached:
            return None
    
    flow_file, node_positions = cached
    symbols: List[lsp.DocumentSymbol] = []
    
    for node_id, node in flow_file.nodes.items():
        pos = node_positions.get(node_id) or Position(1, 1)
        
        # Determine symbol kind
        if node_id == "out":
            kind = lsp.SymbolKind.Module  # Entry point
        elif node.slots:
            kind = lsp.SymbolKind.Class  # Node with slots
        else:
            kind = lsp.SymbolKind.Function  # Regular node
        
        # Create symbol range (approximate - just the definition line)
        line = max(0, pos.line - 1)
        col = max(0, pos.column - 1)
        
        symbol = lsp.DocumentSymbol(
            name=f"@{node_id}",
            kind=kind,
            range=lsp.Range(
                start=lsp.Position(line=line, character=col),
                end=lsp.Position(line=line, character=col + len(node_id) + 1),
            ),
            selection_range=lsp.Range(
                start=lsp.Position(line=line, character=col),
                end=lsp.Position(line=line, character=col + len(node_id) + 1),
            ),
            detail=node.slot_badge if node.slots else None,
        )
        
        # Add slot children
        if node.slots:
            children: List[lsp.DocumentSymbol] = []
            for slot_id, slot_node in node.slots.items():
                slot_pos = slot_node.position or pos
                slot_line = max(0, slot_pos.line - 1)
                slot_col = max(0, slot_pos.column - 1)
                
                children.append(lsp.DocumentSymbol(
                    name=f".{slot_id}",
                    kind=lsp.SymbolKind.Field,
                    range=lsp.Range(
                        start=lsp.Position(line=slot_line, character=slot_col),
                        end=lsp.Position(line=slot_line, character=slot_col + len(slot_id) + 1),
                    ),
                    selection_range=lsp.Range(
                        start=lsp.Position(line=slot_line, character=slot_col),
                        end=lsp.Position(line=slot_line, character=slot_col + len(slot_id) + 1),
                    ),
                ))
            symbol.children = children
        
        symbols.append(symbol)
    
    return symbols


# =============================================================================
# Server Entry Point
# =============================================================================

def start_server(
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 2087,
    logger: Optional[Logger] = None,
) -> None:
    """
    Start the FLOW LSP server.
    
    Args:
        transport: Connection type ('stdio' or 'tcp').
        host: Host for TCP mode (default: 127.0.0.1).
        port: Port for TCP mode (default: 2087).
        logger: Optional logger instance.
    """
    if logger:
        server.logger = logger
        # Propagate logger to internal instances
        server._tokenizer = Tokenizer(logger=logger)
        server._parser = Parser(logger=logger)
        server._resolver = Resolver(logger=logger)
    
    server.logger.info(f"Starting FLOW LSP server ({transport})")
    
    if transport == "tcp":
        server.logger.info(f"Listening on {host}:{port}")
        server.start_tcp(host, port)
    else:
        server.start_io()


def main() -> None:
    """CLI entry point for the LSP server."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FLOW Language Server Protocol (LSP) Server"
    )
    parser.add_argument(
        "--tcp",
        action="store_true",
        help="Use TCP transport instead of stdio",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for TCP mode (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=2087,
        help="Port for TCP mode (default: 2087)",
    )
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default="info",
        help="Logging level (default: info)",
    )
    
    args = parser.parse_args()
    
    # Configure logger
    logger = Logger(name="FlowLSP")
    
    transport = "tcp" if args.tcp else "stdio"
    start_server(
        transport=transport,
        host=args.host,
        port=args.port,
        logger=logger,
    )


if __name__ == "__main__":
    main()
