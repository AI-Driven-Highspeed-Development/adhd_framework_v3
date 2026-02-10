"""
Wrapper Handler - Wraps content in structural containers.

Supports multiple wrapper types for the WRAP phase:
- xml: Wraps in XML-style tags (<tag>...</tag>)
- codeblock: Wraps in Markdown code fence (```lang ... ```)
- blockquote: Prefixes each line with "> "
- details: Wraps in HTML <details> disclosure element

This handler operates in the WRAP phase, transforming the joined content
string after all items have been compiled and concatenated.
"""

from ..models import FlowStyle
from .registry import StyleHandler


class WrapperHandler(StyleHandler):
    """
    Handles style.wrap parameter.
    
    Wraps compiled content in structural containers based on style.wrap value.
    Uses style.tag and style.summary as secondary parameters.
    
    Wrapper types:
        - 'xml': Wraps in XML tags. Uses style.tag for tag name (default: 'section').
                 Example: style.wrap=xml|style.tag=rules → <rules>...</rules>
        
        - 'codeblock': Wraps in Markdown code fence. Uses style.tag for language.
                       Example: style.wrap=codeblock|style.tag=python → ```python ... ```
        
        - 'blockquote': Prefixes each line with "> ".
                        Example: style.wrap=blockquote → > line1\n> line2
        
        - 'details': Wraps in HTML <details> element. Uses style.summary for summary text.
                     Example: style.wrap=details|style.summary=Click to expand → 
                              <details><summary>Click to expand</summary>...</details>
    
    Phase: WRAP (operates on joined content string)
    """
    
    # Valid wrapper types
    VALID_WRAP_TYPES = {"xml", "codeblock", "blockquote", "details"}
    
    def apply_wrap(self, style: FlowStyle, content: str, layer: int) -> str:
        """
        Wrap content in structural container.
        
        Args:
            style: The node's style parameters.
            content: The already-compiled content string.
            layer: The node's nesting depth (unused for wrapping).
            
        Returns:
            Wrapped content string, or unchanged content if no wrap specified.
        """
        if style.wrap is None:
            return content
        
        wrap_type = style.wrap.lower()
        
        if wrap_type == "xml":
            return self._wrap_xml(content, style.tag)
        
        elif wrap_type == "codeblock":
            return self._wrap_codeblock(content, style.tag)
        
        elif wrap_type == "blockquote":
            return self._wrap_blockquote(content)
        
        elif wrap_type == "details":
            return self._wrap_details(content, style.summary)
        
        # Unknown wrap type - passthrough with no modification
        return content
    
    def _wrap_xml(self, content: str, tag: str | None) -> str:
        """
        Wrap content in XML-style tags.
        
        Args:
            content: Content to wrap.
            tag: Tag name (defaults to 'section' if None).
            
        Returns:
            Content wrapped in <tag>...</tag>.
        """
        tag_name = tag or "section"
        # Ensure tag name is valid (alphanumeric + underscore/hyphen)
        tag_name = self._sanitize_tag_name(tag_name)
        return f"<{tag_name}>\n{content}\n</{tag_name}>"
    
    def _wrap_codeblock(self, content: str, lang: str | None) -> str:
        """
        Wrap content in Markdown code fence.
        
        Args:
            content: Content to wrap.
            lang: Language identifier (can be empty for no syntax highlighting).
            
        Returns:
            Content wrapped in ```lang ... ```.
        """
        language = lang or ""
        return f"```{language}\n{content}\n```"
    
    def _wrap_blockquote(self, content: str) -> str:
        """
        Prefix each line with "> " for blockquote formatting.
        
        Args:
            content: Content to format.
            
        Returns:
            Content with each line prefixed by "> ".
        """
        if not content:
            return "> "
        
        lines = content.split('\n')
        quoted_lines = [f"> {line}" for line in lines]
        return '\n'.join(quoted_lines)
    
    def _wrap_details(self, content: str, summary: str | None) -> str:
        """
        Wrap content in HTML <details> disclosure element.
        
        Args:
            content: Content to wrap.
            summary: Summary text for collapsed state (defaults to 'Details').
            
        Returns:
            Content wrapped in <details><summary>...</summary>...</details>.
        """
        summary_text = summary or "Details"
        return f"<details>\n<summary>{summary_text}</summary>\n\n{content}\n\n</details>"
    
    def _sanitize_tag_name(self, tag: str) -> str:
        """
        Sanitize XML tag name to contain only valid characters.
        
        Args:
            tag: Raw tag name.
            
        Returns:
            Sanitized tag name (alphanumeric, underscore, hyphen only).
        """
        # Remove any characters that aren't alphanumeric, underscore, or hyphen
        sanitized = ''.join(
            c for c in tag 
            if c.isalnum() or c in ('_', '-')
        )
        # Ensure non-empty
        return sanitized or "section"
