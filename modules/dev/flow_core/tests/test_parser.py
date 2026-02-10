"""
Tests for Flow Language Parser

Comprehensive tests covering:
- Simple node parsing
- Nodes with parameters
- Nodes with content (strings, refs)
- Nested slots
- Import statements (with selectors, renames)
- Assignments
- Error cases
"""

import pytest

from flow_core.tokenizer import Tokenizer
from flow_core.parser import Parser, parse
from flow_core.models import (
    Token,
    TokenType,
    FlowFile,
    FlowNode,
    NodeRef,
    FileRef,
    ImportNode,
    Assignment,
    FlowParams,
    FlowStyle,
    FlowLLMStrategy,
)
from flow_core.errors import (
    ParserError,
    UnexpectedTokenError,
    DuplicateNodeError,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def tokenizer():
    """Provide a tokenizer instance."""
    return Tokenizer()


@pytest.fixture
def parser():
    """Provide a parser instance."""
    return Parser()


def tokenize_and_parse(source: str) -> FlowFile:
    """Helper to tokenize and parse in one step."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(source)
    return parse(tokens)


# =============================================================================
# Simple Node Parsing Tests
# =============================================================================


class TestSimpleNodes:
    """Tests for basic node parsing."""
    
    def test_minimal_node(self):
        """Test parsing a minimal node with just content."""
        source = "@out |<<<Hello>>>|."
        ast = tokenize_and_parse(source)
        
        assert "out" in ast.nodes
        assert ast.out_node is not None
        assert ast.out_node.id == "out"
        assert ast.out_node.layer == 0
        assert len(ast.out_node.content) == 1
        assert ast.out_node.content[0] == "Hello"
    
    def test_node_with_multiline_content(self):
        """Test node with multiline string content."""
        source = """@greeting 
|<<<
Hello, World!
How are you?
>>>|."""
        ast = tokenize_and_parse(source)
        
        assert "greeting" in ast.nodes
        node = ast.nodes["greeting"]
        assert len(node.content) == 1
        assert "Hello, World!" in node.content[0]
        assert "How are you?" in node.content[0]
    
    def test_multiple_nodes(self):
        """Test parsing multiple node definitions."""
        source = """
@greeting |<<<Hello!>>>|.
@farewell |<<<Goodbye!>>>|.
@out |$greeting|$farewell|.
"""
        ast = tokenize_and_parse(source)
        
        assert len(ast.nodes) == 3
        assert "greeting" in ast.nodes
        assert "farewell" in ast.nodes
        assert "out" in ast.nodes
    
    def test_empty_node(self):
        """Test parsing a node with no content."""
        source = "@empty |."
        ast = tokenize_and_parse(source)
        
        assert "empty" in ast.nodes
        assert ast.nodes["empty"].content == []
    
    def test_node_position_tracking(self):
        """Test that node position is tracked correctly."""
        source = "@node |<<<test>>>|."
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["node"]
        assert node.position is not None
        assert node.position.line == 1
        assert node.position.column == 1


# =============================================================================
# Node Parameters Tests
# =============================================================================


class TestNodeParameters:
    """Tests for node parameter parsing."""
    
    def test_style_title_parameter(self):
        """Test parsing style.title parameter."""
        source = '@heading |style.title=<<My Title>>|<<<Content>>>|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["heading"]
        assert node.params.style is not None
        assert node.params.style.title == "My Title"
    
    def test_mutable_parameter(self):
        """Test parsing mutable parameter."""
        source = '@dynamic |mutable=true|<<<Content>>>|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["dynamic"]
        assert node.params.mutable is True
    
    def test_remutate_parameter(self):
        """Test parsing remutate parameter."""
        source = '@dynamic |mutable=true|remutate=true|<<<Content>>>|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["dynamic"]
        assert node.params.mutable is True
        assert node.params.remutate is True
    
    def test_llm_strategy_instruction(self):
        """Test parsing llm_strategy.instruction parameter."""
        source = '@mutable |llm_strategy.instruction=<<Generate creative text>>|<<<Placeholder>>>|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["mutable"]
        assert node.params.llm_strategy is not None
        assert node.params.llm_strategy.instruction == "Generate creative text"
    
    def test_multiple_parameters(self):
        """Test node with multiple parameters."""
        source = '@complex |style.title=<<Title>>|mutable=true|<<<Content>>>|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["complex"]
        assert node.params.style.title == "Title"
        assert node.params.mutable is True


# =============================================================================
# Node Content Tests
# =============================================================================


class TestNodeContent:
    """Tests for different content types in nodes."""
    
    def test_string_content(self):
        """Test simple string content."""
        source = '@node |<<<Hello World>>>|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["node"]
        assert len(node.content) == 1
        assert node.content[0] == "Hello World"
    
    def test_node_reference_content(self):
        """Test $ref node reference in content."""
        source = """
@greeting |<<<Hello>>>|.
@out |$greeting|.
"""
        ast = tokenize_and_parse(source)
        
        out = ast.nodes["out"]
        assert len(out.content) == 1
        assert isinstance(out.content[0], NodeRef)
        assert out.content[0].id == "greeting"
        assert out.content[0].is_forward is False
    
    def test_forward_reference_content(self):
        """Test ^ref forward reference in content."""
        source = """
@out |^greeting|.
@greeting |<<<Hello>>>|.
"""
        ast = tokenize_and_parse(source)
        
        out = ast.nodes["out"]
        assert len(out.content) == 1
        assert isinstance(out.content[0], NodeRef)
        assert out.content[0].id == "greeting"
        assert out.content[0].is_forward is True
    
    def test_file_reference_content(self):
        """Test ++path file reference in content."""
        # Use << >> to preserve trailing space
        source = '@node |<<See: >>|++./docs/readme.md|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["node"]
        assert len(node.content) == 2
        assert node.content[0] == "See: "
        assert isinstance(node.content[1], FileRef)
        assert node.content[1].path == "./docs/readme.md"
    
    def test_mixed_content(self):
        """Test node with mixed content types."""
        # Use << >> to preserve trailing/leading spaces
        source = """
@greeting |<<<Hello>>>|.
@message |<<Welcome! >>|$greeting|<< Please see >>|++./guide.md|.
"""
        ast = tokenize_and_parse(source)
        
        msg = ast.nodes["message"]
        assert len(msg.content) == 4
        assert msg.content[0] == "Welcome! "
        assert isinstance(msg.content[1], NodeRef)
        assert msg.content[2] == " Please see "
        assert isinstance(msg.content[3], FileRef)
    
    def test_dotted_reference(self):
        """Test $parent.slot dotted reference."""
        source = '@out |$main.greeting|.'
        ast = tokenize_and_parse(source)
        
        out = ast.nodes["out"]
        assert len(out.content) == 1
        assert isinstance(out.content[0], NodeRef)
        assert out.content[0].id == "main.greeting"


# =============================================================================
# Nested Slots Tests
# =============================================================================


class TestNestedSlots:
    """Tests for nested slot parsing."""
    
    def test_simple_slot(self):
        """Test parsing a node with a slot."""
        source = """
@main
|@greeting |.
|.
"""
        ast = tokenize_and_parse(source)
        
        main = ast.nodes["main"]
        assert "greeting" in main.slots
        slot = main.slots["greeting"]
        assert slot.id == "greeting"
        assert slot.layer == 1  # Parent is layer 0, slot is layer 1
    
    def test_slot_with_content(self):
        """Test slot with its own content."""
        source = """
@main
|@greeting |<<<Hello!>>>|.
|.
"""
        ast = tokenize_and_parse(source)
        
        slot = ast.nodes["main"].slots["greeting"]
        assert len(slot.content) == 1
        assert slot.content[0] == "Hello!"
    
    def test_nested_slots(self):
        """Test deeply nested slots."""
        source = """
@out
|@section
 |@subsection
  |<<<Deep content>>>|.
 |.
|.
"""
        ast = tokenize_and_parse(source)
        
        out = ast.nodes["out"]
        assert out.layer == 0
        
        section = out.slots["section"]
        assert section.layer == 1
        
        subsection = section.slots["subsection"]
        assert subsection.layer == 2
        assert subsection.content[0] == "Deep content"
    
    def test_multiple_slots(self):
        """Test node with multiple slots."""
        source = """
@main
|@header |.
|@body |.
|@footer |.
|.
"""
        ast = tokenize_and_parse(source)
        
        main = ast.nodes["main"]
        assert len(main.slots) == 3
        assert "header" in main.slots
        assert "body" in main.slots
        assert "footer" in main.slots
    
    def test_slot_in_content_list(self):
        """Test that slots appear in content list too."""
        source = """
@main
|<<<Before>>>
|@middle |<<<Middle content>>>|.
|<<<After>>>
|.
"""
        ast = tokenize_and_parse(source)
        
        main = ast.nodes["main"]
        assert len(main.content) == 3
        assert main.content[0] == "Before"
        assert isinstance(main.content[1], FlowNode)
        assert main.content[1].id == "middle"
        assert main.content[2] == "After"


# =============================================================================
# Import Tests
# =============================================================================


class TestImports:
    """Tests for import statement parsing."""
    
    def test_simple_import(self):
        """Test basic import statement."""
        source = "+./utils.flow |."
        ast = tokenize_and_parse(source)
        
        assert len(ast.imports) == 1
        imp = ast.imports[0]
        assert imp.path == "./utils.flow"
        assert imp.selectors == []
        assert imp.renames == {}
    
    def test_import_with_selectors(self):
        """Test import with specific node selectors."""
        source = "+./utils.flow |$helper|$utils|."
        ast = tokenize_and_parse(source)
        
        imp = ast.imports[0]
        assert imp.path == "./utils.flow"
        assert imp.selectors == ["helper", "utils"]
    
    def test_import_with_rename(self):
        """Test import with renamed node."""
        source = "+./other.flow |@local_name|. = $external_name|."
        ast = tokenize_and_parse(source)
        
        imp = ast.imports[0]
        assert imp.path == "./other.flow"
        assert "external_name" in imp.selectors
        assert imp.renames == {"external_name": "local_name"}
    
    def test_import_with_multiple_renames(self):
        """Test import with multiple renames."""
        source = "+./lib.flow |@a|. = $x|@b|. = $y|."
        ast = tokenize_and_parse(source)
        
        imp = ast.imports[0]
        assert imp.renames == {"x": "a", "y": "b"}
        assert set(imp.selectors) == {"x", "y"}
    
    def test_multiple_imports(self):
        """Test multiple import statements."""
        source = """
+./first.flow |.
+./second.flow |$node|.
"""
        ast = tokenize_and_parse(source)
        
        assert len(ast.imports) == 2
        assert ast.imports[0].path == "./first.flow"
        assert ast.imports[1].path == "./second.flow"
    
    def test_import_position_tracking(self):
        """Test that import position is tracked."""
        source = "+./file.flow |."
        ast = tokenize_and_parse(source)
        
        imp = ast.imports[0]
        assert imp.position is not None
        assert imp.position.line == 1


# =============================================================================
# Assignment Tests
# =============================================================================


class TestAssignments:
    """Tests for assignment statement parsing."""
    
    def test_simple_assignment(self):
        """Test basic assignment statement."""
        source = """
@main |@slot|.|.
@content |<<<Hello>>>|.
$main.slot = $content
"""
        ast = tokenize_and_parse(source)
        
        assert len(ast.assignments) == 1
        assign = ast.assignments[0]
        assert assign.target == "main.slot"
        assert assign.source == "content"
    
    def test_multiple_assignments(self):
        """Test multiple assignment statements."""
        source = """
@main |@a|.|@b|.|.
@x |<<<X>>>|.
@y |<<<Y>>>|.
$main.a = $x
$main.b = $y
"""
        ast = tokenize_and_parse(source)
        
        assert len(ast.assignments) == 2
        assert ast.assignments[0].target == "main.a"
        assert ast.assignments[0].source == "x"
        assert ast.assignments[1].target == "main.b"
        assert ast.assignments[1].source == "y"
    
    def test_assignment_position_tracking(self):
        """Test that assignment position is tracked."""
        source = """
@main |@slot|.|.
@content |<<<Hi>>>|.
$main.slot = $content
"""
        ast = tokenize_and_parse(source)
        
        assign = ast.assignments[0]
        assert assign.position is not None
        assert assign.position.line == 4


# =============================================================================
# Layer Calculation Tests
# =============================================================================


class TestLayerCalculation:
    """Tests for node layer depth calculation."""
    
    def test_top_level_layer(self):
        """Test that top-level nodes are layer 0."""
        source = "@out |<<<Content>>>|."
        ast = tokenize_and_parse(source)
        
        assert ast.nodes["out"].layer == 0
    
    def test_nested_layer_increment(self):
        """Test that nested slots increment layer."""
        source = """
@out
|@l1
 |@l2
  |@l3|.
 |.
|.
|.
"""
        ast = tokenize_and_parse(source)
        
        out = ast.nodes["out"]
        assert out.layer == 0
        
        l1 = out.slots["l1"]
        assert l1.layer == 1
        
        l2 = l1.slots["l2"]
        assert l2.layer == 2
        
        l3 = l2.slots["l3"]
        assert l3.layer == 3


# =============================================================================
# Anonymous Node Tests
# =============================================================================


class TestAnonymousNodes:
    """Tests for anonymous node parsing."""
    
    def test_anonymous_node(self):
        """Test parsing anonymous node @_."""
        source = "@out |@_|<<<Anonymous content>>>|.|."
        ast = tokenize_and_parse(source)
        
        out = ast.nodes["out"]
        assert len(out.content) == 1
        anon = out.content[0]
        assert isinstance(anon, FlowNode)
        assert anon.id.startswith("_anon_")
    
    def test_anonymous_node_unique_ids(self):
        """Test that multiple anonymous nodes get unique IDs."""
        source = """
@out
|@_|<<<First>>>|.
|@_|<<<Second>>>|.
|.
"""
        ast = tokenize_and_parse(source)
        
        out = ast.nodes["out"]
        assert len(out.content) == 2
        
        first = out.content[0]
        second = out.content[1]
        assert first.id != second.id
        assert first.id.startswith("_anon_")
        assert second.id.startswith("_anon_")


# =============================================================================
# Error Cases Tests
# =============================================================================


class TestParserErrors:
    """Tests for parser error handling."""
    
    def test_duplicate_node_error(self):
        """Test error on duplicate node definition."""
        source = """
@greeting |<<<Hello>>>|.
@greeting |<<<Hi>>>|.
"""
        with pytest.raises(DuplicateNodeError) as exc_info:
            tokenize_and_parse(source)
        
        error = exc_info.value
        assert error.node_id == "greeting"
        assert error.first_line == 2
        assert error.second_line == 3
    
    def test_unexpected_token_error(self):
        """Test error on unexpected token."""
        source = "@node | = invalid |."  # = without proper context
        
        with pytest.raises(UnexpectedTokenError):
            tokenize_and_parse(source)
    
    def test_missing_dot_end(self):
        """Test error when |. is missing."""
        source = "@node |<<<Content>>>"  # Missing |.
        
        with pytest.raises((UnexpectedTokenError, ParserError)):
            tokenize_and_parse(source)
    
    def test_unexpected_top_level_token(self):
        """Test error on unexpected top-level token."""
        source = "= unexpected"
        
        with pytest.raises((UnexpectedTokenError, ParserError)):
            tokenize_and_parse(source)


# =============================================================================
# FlowFile Structure Tests
# =============================================================================


class TestFlowFileStructure:
    """Tests for overall FlowFile structure."""
    
    def test_empty_file(self):
        """Test parsing empty file."""
        source = ""
        ast = tokenize_and_parse(source)
        
        assert ast.imports == []
        assert ast.nodes == {}
        assert ast.assignments == []
        assert ast.out_node is None
    
    def test_library_file_no_out(self):
        """Test parsing library file without @out."""
        source = """
@helper |<<<Helper content>>>|.
@utils |<<<Utils content>>>|.
"""
        ast = tokenize_and_parse(source)
        
        assert len(ast.nodes) == 2
        assert ast.out_node is None
    
    def test_full_flow_file(self):
        """Test parsing a complete FLOW file with all features."""
        source = """
# A complete FLOW file example
+./utils.flow |$helper|.

@greeting |style.title=<<Hello>>|<<<Welcome!>>>|.

@main
|@header|.
|@body|.
|.

$main.header = $greeting

@out |$main|.
"""
        ast = tokenize_and_parse(source)
        
        # Check imports
        assert len(ast.imports) == 1
        assert ast.imports[0].path == "./utils.flow"
        
        # Check nodes
        assert "greeting" in ast.nodes
        assert "main" in ast.nodes
        assert "out" in ast.nodes
        
        # Check slots
        assert "header" in ast.nodes["main"].slots
        assert "body" in ast.nodes["main"].slots
        
        # Check assignments
        assert len(ast.assignments) == 1
        assert ast.assignments[0].target == "main.header"
        
        # Check out node
        assert ast.out_node is not None
        assert ast.out_node.id == "out"


# =============================================================================
# Integration with Tokenizer Tests
# =============================================================================


class TestTokenizerIntegration:
    """Tests for parser integration with tokenizer."""
    
    def test_parse_with_comments(self):
        """Test that comments are properly skipped."""
        source = """
# This is a comment
@node |<<<Content>>>|.
# Another comment
"""
        ast = tokenize_and_parse(source)
        
        assert len(ast.nodes) == 1
        assert "node" in ast.nodes
    
    def test_parse_preserves_whitespace_in_strings(self):
        """Test that string content whitespace is preserved."""
        source = '@node |<<\n  Indented\n  Content\n>>|.'
        ast = tokenize_and_parse(source)
        
        content = ast.nodes["node"].content[0]
        assert "  Indented" in content
        assert "  Content" in content


# =============================================================================
# Edge Case Tests (Gap Coverage)
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and gap coverage identified by HyperSan."""
    
    def test_chained_dotted_assignment(self):
        """Test chained dotted assignment ($a.b.c = $d)."""
        source = """
@container
|@section
 |@header |.
 |.
|.

@greeting |<<<Hello>>>|.

$container.section.header = $greeting

@out |$container|.
"""
        ast = tokenize_and_parse(source)
        
        assert len(ast.assignments) == 1
        assignment = ast.assignments[0]
        assert assignment.target == "container.section.header"
        assert assignment.source == "greeting"
    
    def test_node_with_only_params_no_content(self):
        """Test node with parameters but no content."""
        source = '@styled |style.title=<<Section Title>>|mutable=true|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["styled"]
        assert node.params.style is not None
        assert node.params.style.title == "Section Title"
        assert node.params.mutable is True
        assert node.content == []
    
    def test_unknown_parameter_silent_ignore(self):
        """Test that unknown parameters are silently ignored."""
        source = '@node |unknown_param=<<value>>|custom.setting=<<x>>|<<<Content>>>|.'
        ast = tokenize_and_parse(source)
        
        # Should parse successfully without raising an error
        node = ast.nodes["node"]
        assert len(node.content) == 1
        assert node.content[0] == "Content"
        # Known params remain default
        assert node.params.mutable is False
        assert node.params.style is None
    
    def test_deeply_nested_file_ref_path(self):
        """Test deeply nested file reference paths."""
        source = '@node |<<<See: >>>|++../../../very/deep/nested/path/to/file.md|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["node"]
        assert len(node.content) == 2
        assert isinstance(node.content[1], FileRef)
        assert node.content[1].path == "../../../very/deep/nested/path/to/file.md"
    
    def test_mixed_string_trim_and_preserve_in_same_node(self):
        """Test mixing STRING_TRIM (<<<>>>) and STRING_PRESERVE (<<>>) in same node."""
        source = '@node |<<<Trimmed>>>|<<  Preserved  >>|<<<Also Trimmed>>>|.'
        ast = tokenize_and_parse(source)
        
        node = ast.nodes["node"]
        assert len(node.content) == 3
        assert node.content[0] == "Trimmed"
        assert node.content[1] == "  Preserved  "  # Whitespace preserved
        assert node.content[2] == "Also Trimmed"


# =============================================================================
# Run Tests
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
