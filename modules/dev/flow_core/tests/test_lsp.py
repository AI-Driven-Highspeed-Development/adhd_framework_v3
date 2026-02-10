"""
Tests for Flow Language LSP Server

Comprehensive tests covering:
- FlowLanguageServer initialization
- Position conversion (1-based to 0-based)
- Node completion generation
- Diagnostic conversion from FlowError
- Document parsing and caching
- Go-to-definition
- Hover information
- Document symbols
"""

import pytest
from unittest.mock import MagicMock, patch

from lsprotocol import types as lsp
from pygls.workspace import TextDocument

from flow_core.flow_lsp import (
    FlowLanguageServer,
    _flow_error_to_diagnostic,
    _get_node_ref_at_position,
    _get_node_content_preview,
)
from flow_core.errors import FlowError, ParserError
from flow_core.models import FlowNode, NodeRef, Position


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def lsp_server():
    """Provide a FlowLanguageServer instance."""
    return FlowLanguageServer()


@pytest.fixture
def mock_document():
    """Provide a mock TextDocument with sample FLOW source."""
    # Valid FLOW syntax with multiple nodes
    source = """@header |<<<Welcome to the test>>>|.

@main |<<<Hello, this is the main content.>>>|$header|.

@footer |<<<Footer text>>>|^main|."""
    
    doc = MagicMock(spec=TextDocument)
    doc.uri = "file:///test/sample.flow"
    doc.source = source
    doc.version = 1
    return doc


@pytest.fixture
def simple_document():
    """Provide a minimal valid FLOW document."""
    source = "@out |<<<Hello world>>>|."
    doc = MagicMock(spec=TextDocument)
    doc.uri = "file:///test/simple.flow"
    doc.source = source
    doc.version = 1
    return doc


# =============================================================================
# FlowLanguageServer Initialization Tests
# =============================================================================


class TestServerInitialization:
    """Tests for FlowLanguageServer initialization."""
    
    def test_server_creation(self, lsp_server):
        """Test that server initializes correctly."""
        assert lsp_server is not None
        assert lsp_server.name == "flow-lsp"
        assert lsp_server.version == "0.1.0"
    
    def test_server_has_logger(self, lsp_server):
        """Test that server has a logger instance."""
        assert lsp_server.logger is not None
    
    def test_server_has_empty_cache(self, lsp_server):
        """Test that server starts with empty file cache."""
        assert lsp_server._file_cache == {}
    
    def test_server_has_tokenizer(self, lsp_server):
        """Test that server has a tokenizer instance."""
        assert lsp_server._tokenizer is not None
    
    def test_server_has_parser(self, lsp_server):
        """Test that server has a parser instance."""
        assert lsp_server._parser is not None
    
    def test_server_has_resolver(self, lsp_server):
        """Test that server has a resolver instance."""
        assert lsp_server._resolver is not None


# =============================================================================
# URI/Path Conversion Tests
# =============================================================================


class TestPathConversion:
    """Tests for file path/URI conversion."""
    
    def test_file_uri_to_path(self, lsp_server):
        """Test converting file:// URI to Path."""
        uri = "file:///home/user/test.flow"
        path = lsp_server.get_file_path(uri)
        assert str(path) == "/home/user/test.flow"
    
    def test_plain_path_unchanged(self, lsp_server):
        """Test that plain paths are handled correctly."""
        plain = "/home/user/test.flow"
        path = lsp_server.get_file_path(plain)
        assert str(path) == "/home/user/test.flow"


# =============================================================================
# Position Conversion Tests (1-based to 0-based)
# =============================================================================


class TestPositionConversion:
    """Tests for position conversion between LSP (0-based) and Flow (1-based)."""
    
    def test_flow_error_position_converted(self):
        """Test that FlowError line/column are converted to 0-based."""
        error = FlowError("Test error", line=5, column=10)
        diagnostic = _flow_error_to_diagnostic(error)
        
        # LSP is 0-based, so line 5 -> 4, column 10 -> 9
        assert diagnostic.range.start.line == 4
        assert diagnostic.range.start.character == 9
    
    def test_flow_error_position_zero_clamped(self):
        """Test that position is clamped to 0 for line/column 0."""
        error = FlowError("Test error", line=0, column=0)
        diagnostic = _flow_error_to_diagnostic(error)
        
        # Should clamp to 0, not go negative
        assert diagnostic.range.start.line == 0
        assert diagnostic.range.start.character == 0
    
    def test_flow_error_position_first_line(self):
        """Test conversion for line 1 (first line)."""
        error = FlowError("Test error", line=1, column=1)
        diagnostic = _flow_error_to_diagnostic(error)
        
        # Line 1 -> 0, column 1 -> 0
        assert diagnostic.range.start.line == 0
        assert diagnostic.range.start.character == 0


# =============================================================================
# Diagnostic Conversion Tests
# =============================================================================


class TestDiagnosticConversion:
    """Tests for converting FlowError to LSP Diagnostic."""
    
    def test_basic_flow_error_conversion(self):
        """Test converting a basic FlowError to diagnostic."""
        error = FlowError("Syntax error", line=10, column=5)
        diagnostic = _flow_error_to_diagnostic(error)
        
        assert diagnostic is not None
        assert "Syntax error" in diagnostic.message
        assert diagnostic.severity == lsp.DiagnosticSeverity.Error
        assert diagnostic.source == "flow"
    
    def test_parser_error_conversion(self):
        """Test converting a ParserError (subclass) to diagnostic."""
        error = ParserError("Unexpected token", line=3, column=15)
        diagnostic = _flow_error_to_diagnostic(error)
        
        assert diagnostic is not None
        assert "Unexpected token" in diagnostic.message
        assert diagnostic.range.start.line == 2  # 0-based
        assert diagnostic.range.start.character == 14  # 0-based
    
    def test_diagnostic_has_range(self):
        """Test that diagnostic has proper range."""
        error = FlowError("Test error", line=5, column=10)
        diagnostic = _flow_error_to_diagnostic(error)
        
        assert diagnostic.range is not None
        assert diagnostic.range.start is not None
        assert diagnostic.range.end is not None
        # End should be slightly after start for visual highlighting
        assert diagnostic.range.end.character > diagnostic.range.start.character


# =============================================================================
# Document Parsing Tests
# =============================================================================


class TestDocumentParsing:
    """Tests for document parsing and caching."""
    
    def test_parse_valid_document(self, lsp_server, simple_document):
        """Test parsing a valid FLOW document."""
        flow_file = lsp_server.parse_document(simple_document)
        
        assert flow_file is not None
        assert "out" in flow_file.nodes
    
    def test_parsed_document_is_cached(self, lsp_server, simple_document):
        """Test that parsed document is cached."""
        flow_file = lsp_server.parse_document(simple_document)
        
        assert simple_document.uri in lsp_server._file_cache
        cached = lsp_server.get_cached_file(simple_document.uri)
        assert cached is not None
        cached_file, node_positions = cached
        assert cached_file == flow_file
    
    def test_get_all_node_ids(self, lsp_server, mock_document):
        """Test getting all node IDs from a parsed document."""
        lsp_server.parse_document(mock_document)
        node_ids = lsp_server.get_all_node_ids(mock_document.uri)
        
        assert "header" in node_ids
        assert "main" in node_ids
        assert "footer" in node_ids
    
    def test_get_all_node_ids_empty_for_unparsed(self, lsp_server):
        """Test that unparsed documents return empty node set."""
        node_ids = lsp_server.get_all_node_ids("file:///nonexistent.flow")
        assert node_ids == set()


# =============================================================================
# Node Reference Detection Tests
# =============================================================================


class TestNodeRefDetection:
    """Tests for detecting node references at cursor position."""
    
    def test_detect_backward_ref(self):
        """Test detecting $node_id reference."""
        source = "This is a $header reference."
        doc = MagicMock(spec=TextDocument)
        doc.source = source
        
        # Position on 'h' of 'header' (column 11, 0-based)
        position = lsp.Position(line=0, character=11)
        node_id = _get_node_ref_at_position(doc, position)
        
        assert node_id == "header"
    
    def test_detect_forward_ref(self):
        """Test detecting ^node_id reference."""
        source = "Forward ref to ^main here."
        doc = MagicMock(spec=TextDocument)
        doc.source = source
        
        # Position on 'm' of 'main' (column 16, 0-based)
        position = lsp.Position(line=0, character=16)
        node_id = _get_node_ref_at_position(doc, position)
        
        assert node_id == "main"
    
    def test_detect_ref_with_slot(self):
        """Test detecting node reference with slot accessor."""
        source = "Using $parent.slot value"
        doc = MagicMock(spec=TextDocument)
        doc.source = source
        
        # Position on 'p' of 'parent' (column 7, 0-based)
        position = lsp.Position(line=0, character=7)
        node_id = _get_node_ref_at_position(doc, position)
        
        # Should return just the base node ID
        assert node_id == "parent"
    
    def test_no_ref_at_position(self):
        """Test that None is returned when not on a reference."""
        source = "Plain text without references."
        doc = MagicMock(spec=TextDocument)
        doc.source = source
        
        position = lsp.Position(line=0, character=5)
        node_id = _get_node_ref_at_position(doc, position)
        
        assert node_id is None
    
    def test_ref_at_line_end(self):
        """Test detecting reference at end of line."""
        source = "Reference at end $last"
        doc = MagicMock(spec=TextDocument)
        doc.source = source
        
        # Position on 'l' of 'last' (column 18, 0-based)
        position = lsp.Position(line=0, character=18)
        node_id = _get_node_ref_at_position(doc, position)
        
        assert node_id == "last"


# =============================================================================
# Go-to-Definition Tests
# =============================================================================


class TestGoToDefinition:
    """Tests for go-to-definition functionality."""
    
    def test_find_local_node_definition(self, lsp_server, mock_document):
        """Test finding definition of a locally defined node."""
        lsp_server.parse_document(mock_document)
        
        result = lsp_server.find_node_definition(mock_document.uri, "header")
        
        assert result is not None
        uri, position = result
        assert uri == mock_document.uri
        assert position.line >= 1  # 1-based
    
    def test_find_nonexistent_node_returns_none(self, lsp_server, mock_document):
        """Test that nonexistent node returns None."""
        lsp_server.parse_document(mock_document)
        
        result = lsp_server.find_node_definition(mock_document.uri, "nonexistent")
        
        assert result is None
    
    def test_find_definition_unparsed_document(self, lsp_server):
        """Test finding definition in unparsed document returns None."""
        result = lsp_server.find_node_definition("file:///unknown.flow", "any")
        
        assert result is None


# =============================================================================
# Node Content Preview Tests
# =============================================================================


class TestNodeContentPreview:
    """Tests for node content preview generation."""
    
    def test_preview_string_content(self):
        """Test preview of simple string content."""
        node = FlowNode(id="test")
        node.content = ["Hello, world!"]
        
        preview = _get_node_content_preview(node)
        
        assert "Hello, world!" in preview
    
    def test_preview_with_node_ref(self):
        """Test preview includes node reference notation."""
        node = FlowNode(id="test")
        ref = NodeRef(id="other", is_forward=False)
        node.content = ["Start ", ref, " end"]
        
        preview = _get_node_content_preview(node)
        
        assert "$other" in preview
    
    def test_preview_with_forward_ref(self):
        """Test preview includes forward reference notation."""
        node = FlowNode(id="test")
        ref = NodeRef(id="next", is_forward=True)
        node.content = [ref]
        
        preview = _get_node_content_preview(node)
        
        assert "^next" in preview
    
    def test_preview_empty_node(self):
        """Test preview of empty node."""
        node = FlowNode(id="empty")
        node.content = []
        
        preview = _get_node_content_preview(node)
        
        assert "_Empty node_" in preview
    
    def test_preview_truncation(self):
        """Test that long content is truncated."""
        node = FlowNode(id="long")
        node.content = ["A" * 200]  # Very long content
        
        preview = _get_node_content_preview(node, max_length=50)
        
        assert "..." in preview
        assert len(preview.replace("```\n", "").replace("\n```", "")) < 100


# =============================================================================
# Integration Tests (Document Operations)
# =============================================================================


class TestDocumentOperations:
    """Integration tests for document-level operations."""
    
    def test_parse_and_retrieve_nodes(self, lsp_server, mock_document):
        """Test full parse and node retrieval workflow."""
        # Parse
        flow_file = lsp_server.parse_document(mock_document)
        assert flow_file is not None
        
        # Retrieve node IDs
        node_ids = lsp_server.get_all_node_ids(mock_document.uri)
        assert len(node_ids) == 3
        
        # Find each definition
        for node_id in ["header", "main", "footer"]:
            result = lsp_server.find_node_definition(mock_document.uri, node_id)
            assert result is not None, f"Definition not found for {node_id}"
    
    def test_cache_invalidation_on_change(self, lsp_server, mock_document):
        """Test that cache is updated on document change."""
        # Initial parse
        lsp_server.parse_document(mock_document)
        assert mock_document.uri in lsp_server._file_cache
        
        # Simulate document change with new version
        mock_document.version = 2
        mock_document.source = "@new_node |<<<New content>>>|."
        
        # Re-parse
        flow_file = lsp_server.parse_document(mock_document)
        
        # Cache should be updated
        cached = lsp_server.get_cached_file(mock_document.uri)
        assert cached is not None
        cached_file, _ = cached
        assert "new_node" in cached_file.nodes


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestErrorHandling:
    """Tests for error handling in LSP operations."""
    
    def test_parse_invalid_document(self, lsp_server):
        """Test parsing invalid FLOW document."""
        doc = MagicMock(spec=TextDocument)
        doc.uri = "file:///test/invalid.flow"
        doc.source = "@invalid syntax without proper closing"
        doc.version = 1
        
        flow_file = lsp_server.parse_document(doc)
        
        # Should return None for parse failure
        assert flow_file is None
    
    def test_get_cached_nonexistent_file(self, lsp_server):
        """Test getting cached file that doesn't exist."""
        cached = lsp_server.get_cached_file("file:///nonexistent.flow")
        
        assert cached is None
    
    def test_node_ref_out_of_bounds_line(self):
        """Test node ref detection with out-of-bounds line."""
        doc = MagicMock(spec=TextDocument)
        doc.source = "Single line"
        
        # Line 10 doesn't exist (only line 0)
        position = lsp.Position(line=10, character=0)
        result = _get_node_ref_at_position(doc, position)
        
        assert result is None


# =============================================================================
# Main Entry Point
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
