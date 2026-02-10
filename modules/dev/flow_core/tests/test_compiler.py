"""
Tests for Flow Language Compiler

Comprehensive tests covering:
- Basic compilation (simple @out node)
- Nested nodes compilation
- Node references ($ref) resolution
- File references (++path) literal emission
- MissingOutNodeError when no @out
- Library mode (require_out=False) returns empty for no @out
- Trim/preserve whitespace modes
- Slot reference compilation ($id.slot)
- Full pipeline integration (parse → resolve → compile)
"""

import pytest
import tempfile
from pathlib import Path

from flow_core.tokenizer import Tokenizer
from flow_core.parser import Parser, parse
from flow_core.resolver import Resolver, resolve
from flow_core.compiler import Compiler, compile_resolved
from flow_core.flow_controller import compile_flow, compile_flow_file
from flow_core.models import (
    FlowFile,
    FlowNode,
    NodeRef,
    FileRef,
    FlowParams,
    FlowStyle,
    ResolvedFlowFile,
)
from flow_core.errors import (
    MissingOutNodeError,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def compiler():
    """Provide a compiler instance."""
    return Compiler()


def full_pipeline(source: str) -> str:
    """Helper to run full pipeline: tokenize → parse → resolve → compile."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(source)
    ast = parse(tokens)
    resolved = resolve(ast)
    return compile_resolved(resolved)


def full_pipeline_with_base(source: str, base_path: Path) -> str:
    """Helper with custom base path for imports."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(source)
    ast = parse(tokens)
    resolved = resolve(ast, base_path=base_path)
    return compile_resolved(resolved)


# =============================================================================
# Basic Compilation Tests
# =============================================================================


class TestBasicCompilation:
    """Tests for basic compiler functionality."""
    
    def test_minimal_out_node(self):
        """Test compiling a minimal @out node with string content."""
        source = "@out |<<<Hello, World!>>>|."
        result = full_pipeline(source)
        
        assert result.strip() == "Hello, World!"
    
    def test_out_node_multiline(self):
        """Test compiling @out with multiline content."""
        source = """@out 
|<<<Line one
Line two
Line three>>>|."""
        result = full_pipeline(source)
        
        assert "Line one" in result
        assert "Line two" in result
        assert "Line three" in result
    
    def test_empty_out_node(self):
        """Test compiling @out with no content."""
        source = "@out |."
        result = full_pipeline(source)
        
        assert result == ""
    
    def test_out_with_multiple_strings(self):
        """Test @out with multiple string content items."""
        source = "@out |<<<First>>>|<<<Second>>>|<<<Third>>>|."
        result = full_pipeline(source)
        
        # Strings should be joined with newlines
        lines = result.strip().split("\n")
        assert "First" in lines
        assert "Second" in lines
        assert "Third" in lines


# =============================================================================
# Node Reference Tests
# =============================================================================


class TestNodeReferences:
    """Tests for compiling node references ($ref)."""
    
    def test_simple_backward_reference(self):
        """Test compiling a simple backward reference."""
        source = """
@greeting |<<<Hello>>>|.
@out |$greeting|.
"""
        result = full_pipeline(source)
        
        assert result.strip() == "Hello"
    
    def test_multiple_references(self):
        """Test compiling multiple references in sequence."""
        source = """
@first |<<<Alpha>>>|.
@second |<<<Beta>>>|.
@out |$first|$second|.
"""
        result = full_pipeline(source)
        
        assert "Alpha" in result
        assert "Beta" in result
    
    def test_chained_references(self):
        """Test compiling chained references (A → B → C)."""
        source = """
@a |<<<Deep>>>|.
@b |$a|.
@c |$b|.
@out |$c|.
"""
        result = full_pipeline(source)
        
        assert result.strip() == "Deep"
    
    def test_reference_with_surrounding_content(self):
        """Test reference mixed with string content."""
        source = """
@name |<<<World>>>|.
@out |<<<Hello, >>>|$name|<<<!!!>>>|.
"""
        result = full_pipeline(source)
        
        # Each content item on its own line
        assert "Hello," in result
        assert "World" in result
        assert "!!!" in result


# =============================================================================
# Nested Node Tests
# =============================================================================


class TestNestedNodes:
    """Tests for compiling nested node definitions."""
    
    def test_inline_nested_node(self):
        """Test compiling inline nested nodes."""
        source = """
@out
|@child |<<<Nested content>>>|.
|.
"""
        result = full_pipeline(source)
        
        assert result.strip() == "Nested content"
    
    def test_deeply_nested_nodes(self):
        """Test compiling deeply nested structures."""
        source = """
@out
|@level1
 |@level2
  |@level3 |<<<Deep>>>|.
  |.
 |.
|.
"""
        result = full_pipeline(source)
        
        assert "Deep" in result
    
    def test_multiple_nested_siblings(self):
        """Test multiple sibling nested nodes."""
        source = """
@out
|@child1 |<<<First>>>|.
|@child2 |<<<Second>>>|.
|@child3 |<<<Third>>>|.
|.
"""
        result = full_pipeline(source)
        
        assert "First" in result
        assert "Second" in result
        assert "Third" in result


# =============================================================================
# File Reference Tests
# =============================================================================


class TestFileReferences:
    """Tests for compiling file references (++path)."""
    
    def test_file_reference_literal_emission(self):
        """Test that file refs emit their path as literal."""
        source = "@out |++./docs/readme.md|."
        result = full_pipeline(source)
        
        # In P0.5, file refs emit the path literally
        assert "./docs/readme.md" in result
    
    def test_multiple_file_references(self):
        """Test multiple file references."""
        source = "@out |++./file1.md|++./file2.md|."
        result = full_pipeline(source)
        
        assert "./file1.md" in result
        assert "./file2.md" in result


# =============================================================================
# Slot Reference Tests
# =============================================================================


class TestSlotReferences:
    """Tests for compiling slot references ($id.slot)."""
    
    def test_simple_slot_reference(self):
        """Test compiling a simple slot reference."""
        source = """
@parent
|@header |<<<Header Content>>>|.
|@body |<<<Body Content>>>|.
|.
@out |$parent.header|.
"""
        result = full_pipeline(source)
        
        assert result.strip() == "Header Content"
    
    def test_slot_reference_nested(self):
        """Test slot reference with content from nested slot."""
        source = """
@container
|@section
 |<<<Section Content>>>|.
|.
@out |$container.section|.
"""
        result = full_pipeline(source)
        
        assert result.strip() == "Section Content"


# =============================================================================
# Missing @out Tests
# =============================================================================


class TestMissingOut:
    """Tests for handling missing @out node."""
    
    def test_missing_out_raises_error(self):
        """Test that missing @out raises MissingOutNodeError."""
        source = """
@helper |<<<I'm a helper>>>|.
@utility |<<<I'm a utility>>>|.
"""
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(source)
        ast = parse(tokens)
        resolved = resolve(ast)
        
        with pytest.raises(MissingOutNodeError):
            compile_resolved(resolved, require_out=True)
    
    def test_library_mode_no_error(self):
        """Test that library mode (require_out=False) returns empty string."""
        source = """
@helper |<<<I'm a helper>>>|.
@utility |<<<I'm a utility>>>|.
"""
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(source)
        ast = parse(tokens)
        resolved = resolve(ast)
        
        result = compile_resolved(resolved, require_out=False)
        
        assert result == ""


# =============================================================================
# Whitespace Handling Tests
# =============================================================================


class TestWhitespace:
    """Tests for whitespace trim/preserve modes."""
    
    def test_trim_whitespace(self):
        """Test that <<<>>> trims whitespace."""
        source = "@out |<<<   trimmed   >>>|."
        result = full_pipeline(source)
        
        # Leading/trailing whitespace should be trimmed
        assert result.strip() == "trimmed"
    
    def test_preserve_whitespace(self):
        """Test that <<>> preserves whitespace."""
        source = "@out |<<   preserved   >>|."
        result = full_pipeline(source)
        
        # Whitespace should be preserved
        assert "   preserved   " in result


# =============================================================================
# Pipeline Integration Tests
# =============================================================================


class TestPipelineIntegration:
    """Tests for full pipeline integration."""
    
    def test_compile_flow_function(self):
        """Test the compile_flow() convenience function."""
        source = """
@greeting |<<<Hello from FLOW!>>>|.
@out |$greeting|.
"""
        result = compile_flow(source)
        
        assert result.strip() == "Hello from FLOW!"
    
    def test_compile_flow_with_styles(self):
        """Test compile_flow with style parameters."""
        source = """
@out
|style.title=<<Welcome>>
|<<<This is the content.>>>|.
"""
        result = compile_flow(source)
        
        # Should have H1 heading (layer 0)
        assert "# Welcome" in result
        assert "This is the content." in result
    
    def test_compile_flow_file_function(self):
        """Test the compile_flow_file() convenience function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            flow_file = Path(tmpdir) / "test.flow"
            flow_file.write_text("""
@greeting |<<<Hello from file!>>>|.
@out |$greeting|.
""")
            
            result = compile_flow_file(str(flow_file))
            
            assert result.strip() == "Hello from file!"
    
    def test_compile_with_imports(self):
        """Test compilation with import statements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create library file
            lib_file = Path(tmpdir) / "lib.flow"
            lib_file.write_text("""
@helper |<<<Imported helper>>>|.
""")
            
            # Create main file that imports library
            main_file = Path(tmpdir) / "main.flow"
            main_file.write_text(f"""
+{lib_file} |.

@out |$helper|.
""")
            
            result = compile_flow_file(str(main_file))
            
            assert "Imported helper" in result


# =============================================================================
# Complex Scenarios
# =============================================================================


class TestComplexScenarios:
    """Tests for complex compilation scenarios."""
    
    def test_mixed_content_types(self):
        """Test node with mixed content types."""
        source = """
@ref_target |<<<Referenced>>>|.
@out
|<<<String content>>>|$ref_target|++./path/to/file.md|.
"""
        result = full_pipeline(source)
        
        assert "String content" in result
        assert "Referenced" in result
        assert "./path/to/file.md" in result
    
    def test_reference_to_styled_node(self):
        """Test reference to a node with styles."""
        source = """
@styled
|style.title=<<Section>>
|<<<Section content>>>|.
@out |$styled|.
"""
        result = full_pipeline(source)
        
        # The styled node's title should be included
        assert "# Section" in result
        assert "Section content" in result
    
    def test_forward_reference(self):
        """Test forward reference (^ref) compilation."""
        source = """
@first |^second|.
@second |<<<Forward referenced>>>|.
@out |$first|.
"""
        result = full_pipeline(source)
        
        assert "Forward referenced" in result


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_empty_string_content(self):
        """Test node with empty string content."""
        source = "@out |<<<>>>|."
        result = full_pipeline(source)
        
        assert result == ""
    
    def test_special_characters_in_content(self):
        """Test content with special Markdown characters."""
        source = "@out |<<<# Not a heading\n*not bold*\n`not code`>>>|."
        result = full_pipeline(source)
        
        # Content should be passed through as-is
        assert "# Not a heading" in result
        assert "*not bold*" in result
        assert "`not code`" in result
    
    def test_unicode_content(self):
        """Test compilation with Unicode content."""
        source = "@out |<<<你好世界 🌍 λ→β>>>|."
        result = full_pipeline(source)
        
        assert "你好世界" in result
        assert "🌍" in result
        assert "λ→β" in result
    
    def test_large_content(self):
        """Test compilation with large content."""
        large_content = "X" * 10000
        source = f"@out |<<<{large_content}>>>|."
        result = full_pipeline(source)
        
        assert len(result.strip()) == 10000
        assert result.strip() == large_content


# =============================================================================
# Cycle Detection Regression Tests (BLOCKER-001, BLOCKER-002, BLOCKER-003)
# =============================================================================


class TestCycleDetectionRegression:
    """Regression tests for cycle detection fixes (BLOCKER-001/002/003)."""
    
    def test_self_reference_no_recursion_error(self):
        """BLOCKER-001: Self-reference should not cause RecursionError."""
        # Create AST directly to test compiler cycle detection
        from flow_core.models import FlowNode, FlowParams, ResolvedFlowFile, NodeRef
        
        loop_node = FlowNode(
            id="loop",
            layer=0,
            content=[NodeRef(id="loop", is_forward=False)],  # Self-reference
        )
        
        out_node = FlowNode(
            id="out",
            layer=0,
            content=[NodeRef(id="loop", is_forward=False)],
        )
        
        resolved = ResolvedFlowFile(
            nodes={"loop": loop_node, "out": out_node},
            out_node=out_node,
            dependency_order=["loop", "out"],
        )
        
        # Should not raise RecursionError
        result = compile_resolved(resolved)
        
        # Should emit CIRCULAR marker for the self-reference
        assert "[CIRCULAR: @loop]" in result
    
    def test_mutual_reference_no_recursion_error(self):
        """BLOCKER-002: Mutual reference should not cause RecursionError."""
        from flow_core.models import FlowNode, FlowParams, ResolvedFlowFile, NodeRef
        
        a_node = FlowNode(
            id="a",
            layer=0,
            content=[NodeRef(id="b", is_forward=False)],
        )
        b_node = FlowNode(
            id="b",
            layer=0,
            content=[NodeRef(id="a", is_forward=False)],
        )
        out_node = FlowNode(
            id="out",
            layer=0,
            content=[NodeRef(id="a", is_forward=False)],
        )
        
        resolved = ResolvedFlowFile(
            nodes={"a": a_node, "b": b_node, "out": out_node},
            out_node=out_node,
            dependency_order=["a", "b", "out"],
        )
        
        # Should not raise RecursionError
        result = compile_resolved(resolved)
        
        # Should emit CIRCULAR marker at some point in the cycle
        assert "[CIRCULAR:" in result
    
    def test_deep_chain_no_recursion_error(self):
        """BLOCKER-003: Deep chains should not hit Python recursion limit."""
        from flow_core.models import FlowNode, FlowParams, ResolvedFlowFile, NodeRef
        
        # Create a chain of 500 nodes (well beyond default recursion limit)
        nodes = {}
        order = []
        
        for i in range(500):
            if i == 0:
                nodes[f"n{i}"] = FlowNode(id=f"n{i}", layer=0, content=["Start"])
            else:
                nodes[f"n{i}"] = FlowNode(
                    id=f"n{i}",
                    layer=0,
                    content=[NodeRef(id=f"n{i-1}", is_forward=False)],
                )
            order.append(f"n{i}")
        
        out_node = FlowNode(
            id="out",
            layer=0,
            content=[NodeRef(id="n499", is_forward=False)],
        )
        nodes["out"] = out_node
        order.append("out")
        
        resolved = ResolvedFlowFile(
            nodes=nodes,
            out_node=out_node,
            dependency_order=order,
        )
        
        # Should not raise RecursionError
        result = compile_resolved(resolved)
        
        # Should contain the start content
        assert "Start" in result
    
    def test_three_node_cycle_no_recursion_error(self):
        """Three node cycle (A→B→C→A) should emit CIRCULAR marker."""
        from flow_core.models import FlowNode, FlowParams, ResolvedFlowFile, NodeRef
        
        a_node = FlowNode(id="a", layer=0, content=[NodeRef(id="b", is_forward=False)])
        b_node = FlowNode(id="b", layer=0, content=[NodeRef(id="c", is_forward=False)])
        c_node = FlowNode(id="c", layer=0, content=[NodeRef(id="a", is_forward=False)])
        out_node = FlowNode(id="out", layer=0, content=[NodeRef(id="a", is_forward=False)])
        
        resolved = ResolvedFlowFile(
            nodes={"a": a_node, "b": b_node, "c": c_node, "out": out_node},
            out_node=out_node,
            dependency_order=["a", "b", "c", "out"],
        )
        
        result = compile_resolved(resolved)
        
        # Should contain CIRCULAR marker
        assert "[CIRCULAR:" in result
    
    def test_diamond_dependency_no_false_positive(self):
        """Diamond shape (A→B,C; B→D; C→D) should NOT trigger false circular detection."""
        from flow_core.models import FlowNode, FlowParams, ResolvedFlowFile, NodeRef
        
        d_node = FlowNode(id="d", layer=0, content=["Shared"])
        b_node = FlowNode(id="b", layer=0, content=[NodeRef(id="d", is_forward=False)])
        c_node = FlowNode(id="c", layer=0, content=[NodeRef(id="d", is_forward=False)])
        a_node = FlowNode(id="a", layer=0, content=[NodeRef(id="b", is_forward=False), NodeRef(id="c", is_forward=False)])
        out_node = FlowNode(id="out", layer=0, content=[NodeRef(id="a", is_forward=False)])
        
        resolved = ResolvedFlowFile(
            nodes={"a": a_node, "b": b_node, "c": c_node, "d": d_node, "out": out_node},
            out_node=out_node,
            dependency_order=["d", "b", "c", "a", "out"],
        )
        
        result = compile_resolved(resolved)
        
        # Should NOT contain CIRCULAR marker (diamond is not a cycle)
        assert "[CIRCULAR:" not in result
        # Shared content should appear twice (once per path)
        assert result.count("Shared") == 2


# =============================================================================
# Inline Substitution Tests (StringContent boundary-aware joining)
# =============================================================================


class TestInlineSubstitution:
    """Tests for inline substitution via preserve-closer / preserve-opener boundaries."""

    def test_inline_ref_between_preserve_strings(self):
        """Preserve-closer on left and preserve-opener on right → inline join.

        |<<<Welcome! >>|$ref|<< How are you?>>>|
        should produce "Welcome! Hello! How are you?"
        (no newlines between the parts).
        """
        source = (
            '@greeting |<<<Hello!>>>|.\n'
            '@out |<<<Welcome! >>|$greeting|<< How are you?>>>|.\n'
        )
        result = full_pipeline(source)
        assert result.strip() == "Welcome! Hello! How are you?"

    def test_all_preserve_inline(self):
        """All-preserve strings → inline join between all parts."""
        source = (
            '@a |<<<Alpha>>>|.\n'
            '@out |<<First >>|$a|<< Last>>|.\n'
        )
        result = full_pipeline(source)
        # <<First >> preserves trailing space; << Last>> preserves leading space
        assert result.strip() == "First Alpha Last"

    def test_mixed_preserve_trim_boundaries(self):
        """Mixed: preserve-closer on left, trim-opener on right → inline because left preserve wins."""
        source = (
            '@val |<<<42>>>|.\n'
            '@out |<<<The answer is >>|$val|<<<.>>>|.\n'
        )
        result = full_pipeline(source)
        # <<<...>> = trim opener, preserve closer → left boundary is preserve → inline
        # <<<.>>> = trim both → right boundary is trim
        # Between val-result and ".", join is: val has no metadata (plain str),
        # "." has opener_trim=True → both sides neutral/trim → newline
        # But between "The answer is " and val-result:
        #   left is StringContent(closer_trim=False) → inline
        assert "The answer is 42" in result

    def test_trim_trim_stays_block(self):
        """Trim-trim boundaries → newline-joined (existing behavior preserved)."""
        source = '@out |<<<First>>>|<<<Second>>>|<<<Third>>>|.\n'
        result = full_pipeline(source)
        lines = result.strip().split("\n")
        assert lines == ["First", "Second", "Third"]

    def test_inline_multiple_refs(self):
        """Multiple refs chained inline via preserve boundaries."""
        source = (
            '@name |<<<World>>>|.\n'
            '@punct |<<<!!!>>>|.\n'
            '@out |<<<Hello, >>|$name|<< >>|$punct|.\n'
        )
        result = full_pipeline(source)
        # "Hello, " (closer_trim=False) + "World" → inline
        # "World" + " " (opener_trim=False) → inline
        # " " (closer_trim=False) + "!!!" → inline
        assert result.strip() == "Hello, World !!!"

    def test_inline_with_file_ref(self):
        """File ref between preserve-closer strings should also be inline."""
        source = '@out |<<<See >>|++./readme.md|<< for details.>>>|.\n'
        result = full_pipeline(source)
        assert result.strip() == "See ./readme.md for details."

    def test_single_preserve_item(self):
        """Single preserve-string item should compile identically to trim."""
        source = '@out |<<  Hello  >>|.\n'
        result = full_pipeline(source)
        assert result == "  Hello  "

    def test_preserve_opener_after_trim_closer(self):
        """Trim-closer followed by preserve-opener → inline because opener is preserve."""
        source = '@out |<<<A>>>|<<B>>|.\n'
        result = full_pipeline(source)
        # A has closer_trim=True, B has opener_trim=False → inline (opener preserve wins)
        assert result.strip() == "AB"

    def test_preserve_closer_before_trim_opener(self):
        """Preserve-closer followed by trim-opener → inline because closer is preserve."""
        source = '@out |<<<A>>|<<<B>>>|.\n'
        result = full_pipeline(source)
        # A has closer_trim=False → inline
        assert result.strip() == "AB"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
