"""
List Style Handler - Transforms content into Markdown lists.

Supports four static list types (chosen at authoring time):
- bullet: "- Item"
- numbered: "1. Item"
- task: "- [ ] Item" (unchecked checkbox)
- task-done: "- [x] Item" (checked checkbox)

Auto-indentation based on node layer:
- Layer 0 → no indent
- Layer 1 → 2 spaces
- Layer 2 → 4 spaces
- etc.

Multi-line item handling:
- Each content item may contain multiple lines
- First line gets the marker, subsequent lines get continuation indent
- Example: "Line A\nLine B" → "- Line A\n  Line B"

Nested list handling:
- Lines already formatted as list items are preserved and indented
- This allows parent lists to contain child lists without double-formatting

Phase: PER_ITEM (operates on List[str] BEFORE join)
- Preserves semantic boundaries for multi-line items
- Wrap phase would incorrectly split by \n, losing item context
"""

import re
from typing import List

from ..models import FlowStyle
from .registry import StyleHandler


class ListStyleHandler(StyleHandler):
    """
    Handles style.list parameter.
    
    Transforms content items into Markdown list items in the PER_ITEM phase.
    Each content item becomes a list entry with proper marker and indentation.
    
    Marker types:
        - 'bullet': "-" (2 chars with space)
        - 'numbered': "1.", "2.", "10." (index-dependent width)
        - 'task': "- [ ]" (6 chars with space)
        - 'task-done': "- [x]" (6 chars with space)
    
    Note: These are STATIC markers chosen at authoring time.
    There is no runtime logic to determine completion state.
    The author explicitly chooses 'task' or 'task-done'.
    
    Multi-line item handling:
        For items with multiple lines, the marker is prepended to the first
        line, and subsequent lines receive continuation indent matching the
        marker width.
        
        Example: "Line A\nLine B" with bullet → "- Line A\n  Line B"
    
    Nested list handling:
        Items that already start with a list marker (from nested child lists)
        are preserved as-is and only indented. This prevents double-formatting.
    """
    
    # Indent per layer level (Markdown convention)
    INDENT_PER_LAYER = "  "  # 2 spaces
    
    # Valid list types
    VALID_LIST_TYPES = {"bullet", "numbered", "task", "task-done"}
    
    # Regex to detect if a line already has a list marker
    # Matches: "- ", "1. ", "- [ ] ", "- [x] " etc. (after optional leading whitespace)
    _LIST_MARKER_PATTERN = re.compile(
        r'^(\s*)'  # Leading whitespace (captured for preservation)
        r'(?:'
        r'-\s'                    # Bullet: "- "
        r'|\d+\.\s'               # Numbered: "1. ", "12. ", etc.
        r'|-\s\[[x ]\]\s'         # Task: "- [ ] " or "- [x] "
        r')'
    )
    
    def apply_per_item(
        self, style: FlowStyle, items: List[str], layer: int
    ) -> List[str]:
        """
        Transform content items into list items.
        
        Operates BEFORE join, preserving semantic boundaries for multi-line items.
        
        Args:
            style: The node's style parameters.
            items: List of compiled content items (each may be multi-line).
            layer: The node's nesting depth (for auto-indent calculation).
            
        Returns:
            List of items with list markers prepended and continuation indent applied.
        """
        if not style.list_type:
            return items
        
        # Validate list type
        if style.list_type not in self.VALID_LIST_TYPES:
            return items
        
        # Calculate base indentation: 2 spaces per layer level
        base_indent = "  " * layer
        
        result: List[str] = []
        item_index = 0
        
        for item in items:
            # Skip empty items
            if not item.strip():
                continue
            
            # Check if item is already a list (from nested child compilation)
            # If the first non-empty line has a marker, it's nested list output
            first_line = item.split("\n")[0] if item else ""
            if self._is_already_list_item(first_line):
                # Preserve existing formatting, just add outer indent to all lines
                indented_lines = [
                    f"{base_indent}{line}" if line.strip() else line
                    for line in item.split("\n")
                ]
                result.append("\n".join(indented_lines))
                continue
            
            # Generate marker based on list type and index
            marker = self._get_marker(style.list_type, item_index)
            marker_width = self._get_marker_width(style.list_type, item_index)
            cont_indent = base_indent + " " * marker_width
            
            # Split item into lines for multi-line handling
            lines = item.split("\n")
            formatted_lines: List[str] = []
            
            # First line gets the marker
            formatted_lines.append(f"{base_indent}{marker} {lines[0]}")
            
            # Subsequent lines within the same item get continuation indent
            for line in lines[1:]:
                if line.strip():
                    formatted_lines.append(f"{cont_indent}{line}")
                else:
                    # Preserve empty lines within item
                    formatted_lines.append("")
            
            result.append("\n".join(formatted_lines))
            item_index += 1
        
        return result
    
    def _is_already_list_item(self, line: str) -> bool:
        """
        Check if a line already has a list marker.
        
        This prevents double-formatting when nested lists are compiled.
        
        Args:
            line: The line to check.
            
        Returns:
            True if line already starts with a list marker.
        """
        return bool(self._LIST_MARKER_PATTERN.match(line))
    
    def _get_marker(self, list_type: str, index: int) -> str:
        """
        Generate list marker based on type and item index.
        
        Args:
            list_type: One of 'bullet', 'numbered', 'task', 'task-done'.
            index: Zero-based index of the item in the list.
            
        Returns:
            The marker string (e.g., "-", "1.", "- [ ]", "- [x]").
        """
        if list_type == "bullet":
            return "-"
        elif list_type == "numbered":
            return f"{index + 1}."
        elif list_type == "task":
            return "- [ ]"
        elif list_type == "task-done":
            return "- [x]"
        else:
            # Fallback (should never happen if validation works)
            return "-"
    
    def _get_marker_width(self, list_type: str, index: int) -> int:
        """
        Get the width of the marker including trailing space.
        
        Used for continuation indent calculation on multi-line items.
        
        Marker widths:
            - bullet: 2 chars ("- ")
            - numbered: index-dependent ("1. " = 3, "10. " = 4, "100. " = 5)
            - task: 6 chars ("- [ ] ")
            - task-done: 6 chars ("- [x] ")
        
        Args:
            list_type: One of 'bullet', 'numbered', 'task', 'task-done'.
            index: Zero-based index (affects numbered width).
            
        Returns:
            Number of characters for the marker plus trailing space.
        """
        if list_type == "bullet":
            return 2  # "- "
        elif list_type == "numbered":
            # Calculate width: digits + ". " (2 chars for ". ")
            number = index + 1
            return len(str(number)) + 2  # "1. " = 3, "10. " = 4, etc.
        elif list_type in ("task", "task-done"):
            return 6  # "- [ ] " or "- [x] "
        else:
            return 2  # Default to bullet width
