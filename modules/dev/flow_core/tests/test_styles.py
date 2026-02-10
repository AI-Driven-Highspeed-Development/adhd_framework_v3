"""
Tests for Flow Language Style System

Comprehensive tests covering:
- style.title at layers 0, 1, 2, 6, 10 (verify H6 clamping)
- style.divider emission (---)
- style.list bullet variant
- style.list numbered variant
- style.list task variant
- style.list task-done variant
- Nested lists (verify auto-indent)
- Mixed content (strings + FlowNodes) in lists
- Empty lines in list content
- Invalid list type fallback (silent passthrough)
- Style phase ordering (PRE → CONTENT → WRAP → POST)
"""

import pytest

from flow_core.tokenizer import Tokenizer
from flow_core.parser import Parser, parse
from flow_core.resolver import Resolver, resolve
from flow_core.compiler import Compiler, compile_resolved
from flow_core.flow_controller import compile_flow
from flow_core.models import FlowStyle
from flow_core.styles import (
    StyleRegistry,
    StyleHandler,
    TitleHandler,
    DividerHandler,
    ListStyleHandler,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def style_registry():
    """Provide a StyleRegistry instance."""
    return StyleRegistry()


@pytest.fixture
def title_handler():
    """Provide a TitleHandler instance."""
    return TitleHandler()


@pytest.fixture
def divider_handler():
    """Provide a DividerHandler instance."""
    return DividerHandler()


@pytest.fixture
def list_handler():
    """Provide a ListStyleHandler instance."""
    return ListStyleHandler()


def full_pipeline(source: str) -> str:
    """Helper to run full pipeline: tokenize → parse → resolve → compile."""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(source)
    ast = parse(tokens)
    resolved = resolve(ast)
    return compile_resolved(resolved)


# =============================================================================
# Title Handler Tests
# =============================================================================


class TestTitleHandler:
    """Tests for TitleHandler (style.title → Markdown heading)."""
    
    def test_title_layer_0(self, title_handler):
        """Test title at layer 0 → H1."""
        style = FlowStyle(title="Welcome")
        result = title_handler.apply_pre(style, layer=0)
        
        assert result == "# Welcome\n"
    
    def test_title_layer_1(self, title_handler):
        """Test title at layer 1 → H2."""
        style = FlowStyle(title="Section")
        result = title_handler.apply_pre(style, layer=1)
        
        assert result == "## Section\n"
    
    def test_title_layer_2(self, title_handler):
        """Test title at layer 2 → H3."""
        style = FlowStyle(title="Subsection")
        result = title_handler.apply_pre(style, layer=2)
        
        assert result == "### Subsection\n"
    
    def test_title_layer_5(self, title_handler):
        """Test title at layer 5 → H6 (maximum)."""
        style = FlowStyle(title="Deep")
        result = title_handler.apply_pre(style, layer=5)
        
        assert result == "###### Deep\n"
    
    def test_title_layer_6_clamped(self, title_handler):
        """Test title at layer 6 → H6 (clamped to maximum)."""
        style = FlowStyle(title="Very Deep")
        result = title_handler.apply_pre(style, layer=6)
        
        # Should clamp to H6, not H7
        assert result == "###### Very Deep\n"
        assert result.count("#") == 6
    
    def test_title_layer_10_clamped(self, title_handler):
        """Test title at layer 10 → H6 (clamped)."""
        style = FlowStyle(title="Extremely Deep")
        result = title_handler.apply_pre(style, layer=10)
        
        assert result == "###### Extremely Deep\n"
    
    def test_no_title(self, title_handler):
        """Test that no title returns empty string."""
        style = FlowStyle(title=None)
        result = title_handler.apply_pre(style, layer=0)
        
        assert result == ""
    
    def test_empty_title(self, title_handler):
        """Test that empty title returns empty string."""
        style = FlowStyle(title="")
        result = title_handler.apply_pre(style, layer=0)
        
        assert result == ""
    
    def test_title_in_full_compilation(self):
        """Test title in full compilation pipeline."""
        source = """
@out
|style.title=<<Document Title>>
|<<<Content here.>>>|.
"""
        result = full_pipeline(source)
        
        assert "# Document Title" in result
        assert "Content here." in result


# =============================================================================
# Divider Handler Tests
# =============================================================================


class TestDividerHandler:
    """Tests for DividerHandler (style.divider → horizontal rule)."""
    
    def test_divider_true(self, divider_handler):
        """Test divider=True emits horizontal rule."""
        style = FlowStyle(divider=True)
        result = divider_handler.apply_post(style, layer=0)
        
        assert "---" in result
    
    def test_divider_false(self, divider_handler):
        """Test divider=False emits nothing."""
        style = FlowStyle(divider=False)
        result = divider_handler.apply_post(style, layer=0)
        
        assert result == ""
    
    def test_divider_default(self, divider_handler):
        """Test default (no divider) emits nothing."""
        style = FlowStyle()
        result = divider_handler.apply_post(style, layer=0)
        
        assert result == ""
    
    def test_divider_layer_independent(self, divider_handler):
        """Test divider output is independent of layer."""
        style = FlowStyle(divider=True)
        
        result_0 = divider_handler.apply_post(style, layer=0)
        result_5 = divider_handler.apply_post(style, layer=5)
        
        # Both should have same divider
        assert result_0 == result_5
    
    def test_divider_in_full_compilation(self):
        """Test divider in full compilation pipeline."""
        source = """
@out
|style.divider=<<true>>
|<<<Section content>>>|.
"""
        result = full_pipeline(source)
        
        assert "Section content" in result
        assert "---" in result


# =============================================================================
# List Handler Tests - Bullet
# =============================================================================


class TestListBullet:
    """Tests for ListStyleHandler with bullet variant."""
    
    def test_bullet_single_item(self, list_handler):
        """Test bullet list with single item."""
        style = FlowStyle(list_type="bullet")
        items = ["Item one"]
        result = list_handler.apply_per_item(style, items, layer=0)
        
        assert "\n".join(result) == "- Item one"
    
    def test_bullet_multiple_items(self, list_handler):
        """Test bullet list with multiple items."""
        style = FlowStyle(list_type="bullet")
        items = ["Alpha", "Beta", "Gamma"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        lines = joined.split("\n")
        assert lines[0] == "- Alpha"
        assert lines[1] == "- Beta"
        assert lines[2] == "- Gamma"
    
    def test_bullet_in_compilation(self):
        """Test bullet list in full compilation."""
        source = """
@out
|style.list=<<bullet>>
|@a |<<<First item>>>|.
|@b |<<<Second item>>>|.
|@c |<<<Third item>>>|.
|.
"""
        result = full_pipeline(source)
        
        assert "- First item" in result
        assert "- Second item" in result
        assert "- Third item" in result


# =============================================================================
# List Handler Tests - Numbered
# =============================================================================


class TestListNumbered:
    """Tests for ListStyleHandler with numbered variant."""
    
    def test_numbered_single_item(self, list_handler):
        """Test numbered list with single item."""
        style = FlowStyle(list_type="numbered")
        items = ["First"]
        result = list_handler.apply_per_item(style, items, layer=0)
        
        assert "\n".join(result) == "1. First"
    
    def test_numbered_multiple_items(self, list_handler):
        """Test numbered list with multiple items."""
        style = FlowStyle(list_type="numbered")
        items = ["One", "Two", "Three"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        lines = joined.split("\n")
        assert lines[0] == "1. One"
        assert lines[1] == "2. Two"
        assert lines[2] == "3. Three"
    
    def test_numbered_in_compilation(self):
        """Test numbered list in full compilation."""
        source = """
@out
|style.list=<<numbered>>
|@a |<<<Step one>>>|.
|@b |<<<Step two>>>|.
|@c |<<<Step three>>>|.
|.
"""
        result = full_pipeline(source)
        
        assert "1. Step one" in result
        assert "2. Step two" in result
        assert "3. Step three" in result


# =============================================================================
# List Handler Tests - Task
# =============================================================================


class TestListTask:
    """Tests for ListStyleHandler with task variant."""
    
    def test_task_single_item(self, list_handler):
        """Test task list with single unchecked item."""
        style = FlowStyle(list_type="task")
        items = ["Todo item"]
        result = list_handler.apply_per_item(style, items, layer=0)
        
        assert "\n".join(result) == "- [ ] Todo item"
    
    def test_task_multiple_items(self, list_handler):
        """Test task list with multiple unchecked items."""
        style = FlowStyle(list_type="task")
        items = ["Task A", "Task B", "Task C"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        lines = joined.split("\n")
        assert lines[0] == "- [ ] Task A"
        assert lines[1] == "- [ ] Task B"
        assert lines[2] == "- [ ] Task C"
    
    def test_task_in_compilation(self):
        """Test task list in full compilation."""
        source = """
@out
|style.list=<<task>>
|@a |<<<Design API>>>|.
|@b |<<<Write tests>>>|.
|@c |<<<Deploy>>>|.
|.
"""
        result = full_pipeline(source)
        
        assert "- [ ] Design API" in result
        assert "- [ ] Write tests" in result
        assert "- [ ] Deploy" in result


# =============================================================================
# List Handler Tests - Task-Done
# =============================================================================


class TestListTaskDone:
    """Tests for ListStyleHandler with task-done variant."""
    
    def test_task_done_single_item(self, list_handler):
        """Test task-done list with single checked item."""
        style = FlowStyle(list_type="task-done")
        items = ["Completed item"]
        result = list_handler.apply_per_item(style, items, layer=0)
        
        assert "\n".join(result) == "- [x] Completed item"
    
    def test_task_done_multiple_items(self, list_handler):
        """Test task-done list with multiple checked items."""
        style = FlowStyle(list_type="task-done")
        items = ["Done A", "Done B", "Done C"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        lines = joined.split("\n")
        assert lines[0] == "- [x] Done A"
        assert lines[1] == "- [x] Done B"
        assert lines[2] == "- [x] Done C"
    
    def test_task_done_in_compilation(self):
        """Test task-done list in full compilation."""
        source = """
@out
|style.list=<<task-done>>
|@a |<<<Completed feature A>>>|.
|@b |<<<Completed feature B>>>|.
|.
"""
        result = full_pipeline(source)
        
        assert "- [x] Completed feature A" in result
        assert "- [x] Completed feature B" in result


# =============================================================================
# List Handler Tests - Nested Lists and Indentation
# =============================================================================


class TestListIndentation:
    """Tests for list auto-indentation based on layer."""
    
    def test_layer_0_no_indent(self, list_handler):
        """Test layer 0 has no indentation."""
        style = FlowStyle(list_type="bullet")
        items = ["Item"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        assert joined == "- Item"
        assert not joined.startswith(" ")
    
    def test_layer_1_indent_2_spaces(self, list_handler):
        """Test layer 1 has 2 spaces indentation."""
        style = FlowStyle(list_type="bullet")
        items = ["Nested"]
        result = list_handler.apply_per_item(style, items, layer=1)
        
        assert "\n".join(result) == "  - Nested"
    
    def test_layer_2_indent_4_spaces(self, list_handler):
        """Test layer 2 has 4 spaces indentation."""
        style = FlowStyle(list_type="bullet")
        items = ["Deep"]
        result = list_handler.apply_per_item(style, items, layer=2)
        
        assert "\n".join(result) == "    - Deep"
    
    def test_layer_3_indent_6_spaces(self, list_handler):
        """Test layer 3 has 6 spaces indentation."""
        style = FlowStyle(list_type="numbered")
        items = ["Very deep"]
        result = list_handler.apply_per_item(style, items, layer=3)
        
        assert "\n".join(result) == "      1. Very deep"
    
    def test_nested_list_compilation(self):
        """Test nested lists in full compilation pipeline."""
        source = """
@out
|style.list=<<bullet>>
|@child1
 |style.list=<<bullet>>
 |@a |<<<Nested A>>>|.
 |@b |<<<Nested B>>>|.
 |.
|.
"""
        result = full_pipeline(source)
        
        # Child at layer 1 should have 2-space indent
        assert "  - Nested A" in result
        assert "  - Nested B" in result


# =============================================================================
# List Handler Tests - Mixed Content
# =============================================================================


class TestListMixedContent:
    """Tests for lists with mixed content types."""
    
    def test_list_with_node_refs(self):
        """Test list containing node references."""
        source = """
@item1 |<<<First>>>|.
@item2 |<<<Second>>>|.
@out
|style.list=<<bullet>>
|$item1|$item2|.
"""
        result = full_pipeline(source)
        
        assert "- First" in result
        assert "- Second" in result
    
    def test_list_with_nested_nodes(self):
        """Test list containing nested node definitions."""
        source = """
@out
|style.list=<<numbered>>
|@a |<<<Alpha>>>|.
|@b |<<<Beta>>>|.
|@c |<<<Gamma>>>|.
|.
"""
        result = full_pipeline(source)
        
        assert "1. Alpha" in result
        assert "2. Beta" in result
        assert "3. Gamma" in result


# =============================================================================
# List Handler Tests - Empty Lines
# =============================================================================


class TestListEmptyLines:
    """Tests for empty line handling in lists."""
    
    def test_empty_lines_skipped(self, list_handler):
        """Test that empty items are filtered out."""
        style = FlowStyle(list_type="bullet")
        # With per_item semantics, empty strings in the list are filtered
        items = ["First", "", "Second", "", "Third"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        # Empty items should be filtered, leaving only 3 items
        assert "- First" in joined
        assert "- Second" in joined
        assert "- Third" in joined
        assert len(result) == 3  # Only non-empty items
    
    def test_leading_empty_lines_skipped(self, list_handler):
        """Test that leading empty items don't create list items."""
        style = FlowStyle(list_type="bullet")
        items = ["", "", "First", "Second"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        # Should not start with empty items
        assert joined.startswith("- First")


# =============================================================================
# List Handler Tests - Multi-Line Items (PER_ITEM phase fix)
# =============================================================================


class TestListMultiLineItems:
    """Tests for multi-line content items in lists.
    
    This is the key feature enabled by the PER_ITEM phase:
    Each content item may contain multiple lines. The first line
    gets the marker, subsequent lines get continuation indent.
    """
    
    def test_multiline_bullet_item(self, list_handler):
        """Test bullet list with multi-line item."""
        style = FlowStyle(list_type="bullet")
        items = ["Line A\nLine B"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        # First line gets marker, second gets continuation indent
        assert joined == "- Line A\n  Line B"
    
    def test_multiline_numbered_item(self, list_handler):
        """Test numbered list with multi-line item."""
        style = FlowStyle(list_type="numbered")
        items = ["Line A\nLine B\nLine C"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        # "1. " is 3 chars, so continuation indent is 3 spaces
        assert joined == "1. Line A\n   Line B\n   Line C"
    
    def test_multiline_task_item(self, list_handler):
        """Test task list with multi-line item."""
        style = FlowStyle(list_type="task")
        items = ["Main task\nSub-detail"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        # "- [ ] " is 6 chars, so continuation indent is 6 spaces
        assert joined == "- [ ] Main task\n      Sub-detail"
    
    def test_multiple_multiline_items(self, list_handler):
        """Test list with multiple multi-line items."""
        style = FlowStyle(list_type="bullet")
        items = ["Alpha\nBeta", "Gamma\nDelta"]
        result = list_handler.apply_per_item(style, items, layer=0)
        joined = "\n".join(result)
        
        lines = joined.split("\n")
        assert lines[0] == "- Alpha"
        assert lines[1] == "  Beta"
        assert lines[2] == "- Gamma"
        assert lines[3] == "  Delta"
    
    def test_multiline_with_layer_indent(self, list_handler):
        """Test multi-line item at layer 1 has proper indentation."""
        style = FlowStyle(list_type="bullet")
        items = ["Line A\nLine B"]
        result = list_handler.apply_per_item(style, items, layer=1)
        joined = "\n".join(result)
        
        # Layer 1 = 2 spaces base + "- " marker, continuation = 4 spaces total
        assert joined == "  - Line A\n    Line B"
    
    def test_numbered_wide_index_continuation(self, list_handler):
        """Test numbered list with 2-digit index has correct continuation indent."""
        style = FlowStyle(list_type="numbered")
        # Create 10 items to get to "10. " marker (4 chars)
        items = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "Line1\nLine2"]
        result = list_handler.apply_per_item(style, items, layer=0)
        
        # Last item is #10, marker is "10. " (4 chars)
        last_item = result[-1]
        lines = last_item.split("\n")
        assert lines[0] == "10. Line1"
        assert lines[1] == "    Line2"  # 4 spaces for continuation


# =============================================================================
# List Handler Tests - Invalid Type
# =============================================================================


class TestListInvalidType:
    """Tests for invalid list type handling."""
    
    def test_invalid_type_passthrough(self, list_handler):
        """Test that invalid list type passes items through unchanged."""
        style = FlowStyle(list_type="invalid_type")
        items = ["Some content"]
        result = list_handler.apply_per_item(style, items, layer=0)
        
        # Should pass through unchanged (silent fallback)
        assert result == ["Some content"]
    
    def test_none_type_passthrough(self, list_handler):
        """Test that None list type passes items through."""
        style = FlowStyle(list_type=None)
        items = ["Unchanged content"]
        result = list_handler.apply_per_item(style, items, layer=0)
        
        assert result == ["Unchanged content"]


# =============================================================================
# Style Phase Ordering Tests
# =============================================================================


class TestStylePhaseOrdering:
    """Tests for correct style phase ordering (PRE → CONTENT → WRAP → POST)."""
    
    def test_title_before_content(self):
        """Test that title (PRE) appears before content."""
        source = """
@out
|style.title=<<Heading>>
|<<<Body text>>>|.
"""
        result = full_pipeline(source)
        
        # Title should appear before content
        title_pos = result.find("# Heading")
        content_pos = result.find("Body text")
        
        assert title_pos < content_pos
    
    def test_divider_after_content(self):
        """Test that divider (POST) appears after content."""
        source = """
@out
|style.divider=<<true>>
|<<<Body text>>>|.
"""
        result = full_pipeline(source)
        
        # Divider should appear after content
        content_pos = result.find("Body text")
        divider_pos = result.find("---")
        
        assert content_pos < divider_pos
    
    def test_list_wraps_content_not_title(self):
        """Test that list (WRAP) transforms content but not PRE/POST."""
        source = """
@out
|style.title=<<My List>>
|style.list=<<bullet>>
|@a |<<<Item A>>>|.
|@b |<<<Item B>>>|.
|.
"""
        result = full_pipeline(source)
        
        # Title should NOT have list marker
        assert "- # My List" not in result
        # But content should
        assert "- Item A" in result
        assert "- Item B" in result
        # And title should still exist
        assert "# My List" in result
    
    def test_full_style_ordering(self):
        """Test all phases in correct order."""
        source = """
@out
|style.title=<<Section>>
|style.divider=<<true>>
|style.list=<<numbered>>
|@a |<<<First>>>|.
|@b |<<<Second>>>|.
|.
"""
        result = full_pipeline(source)
        
        # Find positions
        title_pos = result.find("# Section")
        item1_pos = result.find("1. First")
        item2_pos = result.find("2. Second")
        divider_pos = result.find("---")
        
        # Verify ordering
        assert title_pos >= 0, "Title not found"
        assert item1_pos >= 0, "Item 1 not found"
        assert item2_pos >= 0, "Item 2 not found"
        assert divider_pos >= 0, "Divider not found"
        
        assert title_pos < item1_pos, "Title should be before items"
        assert item1_pos < item2_pos, "Items should be in order"
        assert item2_pos < divider_pos, "Divider should be after items"


# =============================================================================
# StyleRegistry Tests
# =============================================================================


class TestStyleRegistry:
    """Tests for StyleRegistry orchestration."""
    
    def test_registry_has_handlers(self, style_registry):
        """Test that registry is initialized with handlers."""
        # Should have built-in handlers registered
        assert style_registry is not None
    
    def test_registry_apply_pre(self, style_registry):
        """Test registry apply_pre aggregates all handlers."""
        style = FlowStyle(title="Test")
        result = style_registry.apply_pre(style, layer=0)
        
        assert "# Test" in result
    
    def test_registry_apply_post(self, style_registry):
        """Test registry apply_post aggregates all handlers."""
        style = FlowStyle(divider=True)
        result = style_registry.apply_post(style, layer=0)
        
        assert "---" in result
    
    def test_registry_apply_wrap(self, style_registry):
        """Test registry apply_wrap is passthrough when no wrap handlers apply."""
        style = FlowStyle(list_type="bullet")
        content = "Item"
        result = style_registry.apply_wrap(style, content, layer=0)
        
        # List formatting is now in apply_per_item, not apply_wrap
        # apply_wrap should be passthrough for now
        assert result == "Item"
    
    def test_registry_apply_per_item(self, style_registry):
        """Test registry apply_per_item transforms items for list formatting."""
        style = FlowStyle(list_type="bullet")
        items = ["Item"]
        result = style_registry.apply_per_item(style, items, layer=0)
        
        assert "\n".join(result) == "- Item"
    
    def test_registry_null_style(self, style_registry):
        """Test registry handles None style gracefully."""
        result_pre = style_registry.apply_pre(None, layer=0)
        result_post = style_registry.apply_post(None, layer=0)
        result_wrap = style_registry.apply_wrap(None, "content", layer=0)
        result_per_item = style_registry.apply_per_item(None, ["item"], layer=0)
        
        assert result_pre == ""
        assert result_post == ""
        assert result_wrap == "content"
        assert result_per_item == ["item"]


# =============================================================================
# Integration Tests
# =============================================================================


class TestStyleIntegration:
    """Integration tests combining multiple style features."""
    
    def test_nested_styled_nodes(self):
        """Test nested nodes with different styles."""
        source = """
@out
|style.title=<<Main Document>>
|@section1
 |style.title=<<First Section>>
 |<<<Section 1 content>>>|.
|@section2
 |style.title=<<Second Section>>
 |style.divider=<<true>>
 |<<<Section 2 content>>>|.
|.
"""
        result = full_pipeline(source)
        
        # Should have H1 for main
        assert "# Main Document" in result
        # H2 for children (layer 1)
        assert "## First Section" in result
        assert "## Second Section" in result
        # Content should be present
        assert "Section 1 content" in result
        assert "Section 2 content" in result
        # Divider only after section 2
        assert result.count("---") == 1
    
    def test_list_with_styled_items(self):
        """Test list containing styled child nodes."""
        source = """
@out
|style.list=<<bullet>>
|@item1
 |style.title=<<Feature A>>
 |<<<Description of A>>>|.
|@item2
 |style.title=<<Feature B>>
 |<<<Description of B>>>|.
|.
"""
        result = full_pipeline(source)
        
        # List items should contain styled content
        # The item wrapper applies to the whole compiled output
        assert "Feature A" in result
        assert "Feature B" in result
        assert "Description of A" in result
        assert "Description of B" in result


# =============================================================================
# Title Handler Regression Tests (WARNING-001, WARNING-002, WARNING-003)
# =============================================================================


class TestTitleHandlerRegression:
    """Regression tests for title handler edge cases (WARNING-001/002/003)."""
    
    def test_negative_layer_clamped_to_h1(self, title_handler):
        """WARNING-001: Negative layer should produce H1, not broken heading."""
        style = FlowStyle(title="Test")
        
        # Negative layer should clamp to H1 (1 hash)
        result = title_handler.apply_pre(style, layer=-1)
        assert result == "# Test\n", f"Expected '# Test\\n', got {repr(result)}"
        
        result = title_handler.apply_pre(style, layer=-5)
        assert result == "# Test\n", f"Expected '# Test\\n', got {repr(result)}"
        
        result = title_handler.apply_pre(style, layer=-100)
        assert result == "# Test\n", f"Expected '# Test\\n', got {repr(result)}"
    
    def test_whitespace_only_title_returns_empty(self, title_handler):
        """WARNING-002: Whitespace-only title should return empty string."""
        # Various whitespace-only titles
        whitespace_titles = ["   ", "\t", "\n", "  \t\n  ", "\t\t\t"]
        
        for ws_title in whitespace_titles:
            style = FlowStyle(title=ws_title)
            result = title_handler.apply_pre(style, layer=0)
            assert result == "", f"Whitespace title {repr(ws_title)} should return empty, got {repr(result)}"
    
    def test_newlines_in_title_replaced_with_spaces(self, title_handler):
        """WARNING-003: Newlines in title should be replaced with spaces."""
        style = FlowStyle(title="Line1\nLine2")
        result = title_handler.apply_pre(style, layer=0)
        
        # Should be a single line heading with space
        assert result == "# Line1 Line2\n", f"Expected '# Line1 Line2\\n', got {repr(result)}"
    
    def test_multiple_newlines_in_title(self, title_handler):
        """Multiple newlines should all be replaced with spaces."""
        style = FlowStyle(title="A\nB\nC\nD")
        result = title_handler.apply_pre(style, layer=0)
        
        assert result == "# A B C D\n", f"Expected '# A B C D\\n', got {repr(result)}"
    
    def test_newlines_with_whitespace_title_normalized(self, title_handler):
        """Title with newlines and extra whitespace should be normalized."""
        style = FlowStyle(title="  Title\nSubtitle  ")
        result = title_handler.apply_pre(style, layer=0)
        
        # Leading/trailing whitespace stripped, newline replaced
        assert result == "# Title Subtitle\n", f"Expected '# Title Subtitle\\n', got {repr(result)}"
    
    def test_only_newline_title_returns_empty(self, title_handler):
        """Title that is only newlines should return empty."""
        style = FlowStyle(title="\n\n\n")
        result = title_handler.apply_pre(style, layer=0)
        
        assert result == "", f"Only-newline title should return empty, got {repr(result)}"
    
    def test_negative_layer_integration(self):
        """Integration test: Negative layer in compiled flow."""
        # This tests the edge case of somehow getting negative layers
        # (shouldn't happen normally, but defensive coding is good)
        from flow_core.models import FlowNode, FlowParams, ResolvedFlowFile
        
        node = FlowNode(
            id="test",
            layer=-5,  # Negative layer
            params=FlowParams(style=FlowStyle(title="NegativeTest")),
            content=["content"]
        )
        
        resolved = ResolvedFlowFile(
            nodes={"test": node},
            out_node=node,
            dependency_order=["test"]
        )
        
        result = compile_resolved(resolved)
        
        # Should have H1 heading, not broken output
        assert "# NegativeTest" in result
        assert result.startswith("# NegativeTest\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
