"""
Title Handler - Converts style.title to Markdown headings.

Heading level is determined by (in order of precedence):
1. style.level (absolute): Directly sets heading level 1-6
2. style.level_offset (relative): Adds offset to layer-based level
3. Node layer (default): Layer 0 → H1, Layer 1 → H2, etc.
"""

from ..models import FlowStyle
from .registry import StyleHandler


class TitleHandler(StyleHandler):
    """
    Handles style.title parameter.
    
    Emits a Markdown heading in the PRE phase based on:
    - The title text from style.title
    - The heading level determined by:
      1. style.level (absolute, overrides layer)
      2. style.level_offset (relative, adds to layer-based level)
      3. node.layer (default, clamped to H6)
    
    Example:
        style.title="Welcome" at layer 0 → "# Welcome\n"
        style.title="Details" at layer 1 → "## Details\n"
        style.title="Step" with level=3 → "### Step\n"
        style.title="Sub" at layer 1 with level=+2 → "#### Sub\n" (H4 = layer 1 + 1 + 2)
    """
    
    # Maximum heading level in Markdown
    MAX_HEADING_LEVEL = 6
    
    def apply_pre(self, style: FlowStyle, layer: int) -> str:
        """
        Generate heading markup for style.title.
        
        Args:
            style: The node's style parameters.
            layer: The node's nesting depth (0 = root).
            
        Returns:
            Markdown heading string, or empty string if no title.
        """
        # WARNING-002: Check for empty or whitespace-only titles
        if not style.title or not style.title.strip():
            return ""
        
        # WARNING-003: Replace newlines with spaces to prevent invalid headings
        clean_title = style.title.replace('\n', ' ').strip()
        
        # If after cleaning the title is empty, return empty
        if not clean_title:
            return ""
        
        # Determine heading level with precedence:
        # 1. Absolute level (style.level) - overrides everything
        # 2. Relative offset (style.level_offset) - added to layer-based level
        # 3. Layer-based (default) - layer 0 → H1, layer 1 → H2, etc.
        heading_level = self._calculate_heading_level(style, layer)
        
        # Build heading: "# Title\n" or "## Title\n" etc.
        hashes = "#" * heading_level
        return f"{hashes} {clean_title}\n"
    
    def _calculate_heading_level(self, style: FlowStyle, layer: int) -> int:
        """
        Calculate the heading level based on style parameters and layer.
        
        Precedence:
        1. style.level (absolute) - if set, use directly
        2. style.level_offset (relative) - add to layer-based level
        3. Layer-based default - layer + 1
        
        Args:
            style: The node's style parameters.
            layer: The node's nesting depth (0 = root).
            
        Returns:
            Heading level clamped to 1-6.
        """
        if style.level is not None:
            # Absolute level: use directly, clamp to valid range
            heading_level = style.level
        elif style.level_offset is not None:
            # Relative offset: layer-based level + offset
            # WARNING-001: Clamp layer to minimum 0 to prevent negative base
            base_level = max(layer + 1, 1)
            heading_level = base_level + style.level_offset
        else:
            # Default: layer-based (layer 0 → H1, layer 1 → H2)
            # WARNING-001: Clamp layer to minimum 0
            heading_level = max(layer + 1, 1)
        
        # Clamp to valid Markdown heading range H1-H6
        return min(max(heading_level, 1), self.MAX_HEADING_LEVEL)
