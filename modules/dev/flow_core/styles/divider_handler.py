"""
Divider Handler - Emits horizontal rule after content.

When style.divider=true, appends a Markdown horizontal rule (---).
"""

from ..models import FlowStyle
from .registry import StyleHandler


class DividerHandler(StyleHandler):
    """
    Handles style.divider parameter.
    
    Emits a Markdown horizontal rule (---) in the POST phase
    when style.divider is True.
    
    Example:
        style.divider=true → content followed by "\n---\n"
    """
    
    def apply_post(self, style: FlowStyle, layer: int) -> str:
        """
        Generate horizontal rule for style.divider.
        
        Args:
            style: The node's style parameters.
            layer: The node's nesting depth (unused for dividers).
            
        Returns:
            Markdown horizontal rule, or empty string if divider not set.
        """
        if not style.divider:
            return ""
        
        # Emit horizontal rule with surrounding newlines
        return "\n---\n"
