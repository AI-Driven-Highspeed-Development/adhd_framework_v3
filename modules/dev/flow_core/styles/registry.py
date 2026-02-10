"""
Style Registry - Orchestrates style handlers for Flow compilation.

The registry manages four compilation phases:
- PRE: Content emitted before node content (headings)
- PER_ITEM: Transform individual items before join (lists)
- WRAP: Content transformation on joined string (blockquotes, codefences)
- POST: Content emitted after node content (dividers)

Phase order: PRE → (compile items) → PER_ITEM → join → WRAP → POST
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from ..models import FlowStyle


class StyleHandler(ABC):
    """
    Abstract base class for style handlers.
    
    Handlers implement one or more phases:
    - apply_pre: Emit content before node content
    - apply_per_item: Transform individual items before join
    - apply_wrap: Transform the joined content string
    - apply_post: Emit content after node content
    
    Not all handlers need to implement all phases.
    Default implementations return empty string or passthrough.
    """
    
    def apply_pre(self, style: FlowStyle, layer: int) -> str:
        """
        Generate content to prepend before node content.
        
        Args:
            style: The node's style parameters.
            layer: The node's nesting depth (0 = root).
            
        Returns:
            String to prepend, or empty string.
        """
        return ""
    
    def apply_post(self, style: FlowStyle, layer: int) -> str:
        """
        Generate content to append after node content.
        
        Args:
            style: The node's style parameters.
            layer: The node's nesting depth (0 = root).
            
        Returns:
            String to append, or empty string.
        """
        return ""
    
    def apply_per_item(self, style: FlowStyle, items: List[str], layer: int) -> List[str]:
        """
        Transform individual content items before joining.
        
        This phase operates on the List[str] of compiled items BEFORE join,
        preserving semantic boundaries. Ideal for list formatting where
        multi-line items need to remain as single list entries.
        
        Args:
            style: The node's style parameters.
            items: List of compiled content items (each may be multi-line).
            layer: The node's nesting depth (0 = root).
            
        Returns:
            Transformed list of items. Default: passthrough.
        """
        return items
    
    def apply_wrap(self, style: FlowStyle, content: str, layer: int) -> str:
        """
        Transform the compiled content.
        
        Args:
            style: The node's style parameters.
            content: The already-compiled content string.
            layer: The node's nesting depth (0 = root).
            
        Returns:
            Transformed content string.
        """
        return content


class StyleRegistry:
    """
    Registry that manages and applies style handlers.
    
    Built-in handlers:
    - TitleHandler: style.title → heading (PRE phase)
    - DividerHandler: style.divider → horizontal rule (POST phase)
    - ListStyleHandler: style.list → list formatting (PER_ITEM phase)
    
    Phases are applied in order:
    1. PRE - before content (headings)
    2. (content items compiled by caller into List[str])
    3. PER_ITEM - transform individual items (lists)
    4. (items joined into string)
    5. WRAP - transform joined content (blockquotes)
    6. POST - after content (dividers)
    """
    
    def __init__(self) -> None:
        """Initialize the registry with built-in handlers."""
        self._handlers: List[StyleHandler] = []
        self._register_builtin_handlers()
    
    def _register_builtin_handlers(self) -> None:
        """Register the default style handlers."""
        # Import here to avoid circular imports
        from .title_handler import TitleHandler
        from .divider_handler import DividerHandler
        from .list_handler import ListStyleHandler
        from .wrapper_handler import WrapperHandler
        
        self._handlers = [
            TitleHandler(),
            DividerHandler(),
            ListStyleHandler(),
            WrapperHandler(),
        ]
    
    def register_handler(self, handler: StyleHandler) -> None:
        """
        Register a custom style handler.
        
        Args:
            handler: The handler instance to register.
        """
        self._handlers.append(handler)
    
    def apply_pre(self, style: Optional[FlowStyle], layer: int) -> str:
        """
        Apply all PRE phase handlers.
        
        Args:
            style: The node's style parameters (may be None).
            layer: The node's nesting depth.
            
        Returns:
            Concatenated PRE output from all handlers.
        """
        if style is None:
            return ""
        
        results = []
        for handler in self._handlers:
            result = handler.apply_pre(style, layer)
            if result:
                results.append(result)
        
        return "".join(results)
    
    def apply_post(self, style: Optional[FlowStyle], layer: int) -> str:
        """
        Apply all POST phase handlers.
        
        Args:
            style: The node's style parameters (may be None).
            layer: The node's nesting depth.
            
        Returns:
            Concatenated POST output from all handlers.
        """
        if style is None:
            return ""
        
        results = []
        for handler in self._handlers:
            result = handler.apply_post(style, layer)
            if result:
                results.append(result)
        
        return "".join(results)
    
    def apply_per_item(
        self,
        style: Optional[FlowStyle],
        items: List[str],
        layer: int
    ) -> List[str]:
        """
        Apply all PER_ITEM phase handlers.
        
        This phase operates on List[str] BEFORE join, preserving semantic
        boundaries for multi-line content items.
        
        Args:
            style: The node's style parameters (may be None).
            items: List of compiled content items.
            layer: The node's nesting depth.
            
        Returns:
            Items after all PER_ITEM transformations.
        """
        if style is None:
            return items
        
        result = items
        for handler in self._handlers:
            result = handler.apply_per_item(style, result, layer)
        
        return result
    
    def apply_wrap(
        self,
        style: Optional[FlowStyle],
        content: str,
        layer: int
    ) -> str:
        """
        Apply all WRAP phase handlers.
        
        Args:
            style: The node's style parameters (may be None).
            content: The compiled content to transform.
            layer: The node's nesting depth.
            
        Returns:
            Content after all WRAP transformations.
        """
        if style is None:
            return content
        
        result = content
        for handler in self._handlers:
            result = handler.apply_wrap(style, result, layer)
        
        return result
