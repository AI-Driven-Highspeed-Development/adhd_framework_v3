"""
Flow Core Style System

Provides pluggable style handlers for transforming compiled content.

Architecture:
    StyleRegistry orchestrates four phases:
    - PRE: Emit content before node (e.g., headings)
    - PER_ITEM: Transform individual items before join (e.g., lists)
    - WRAP: Transform final content (e.g., wrappers, blockquotes)
    - POST: Emit content after node (e.g., dividers)

Handlers:
    - TitleHandler: style.title → Markdown heading
    - DividerHandler: style.divider → Horizontal rule
    - ListStyleHandler: style.list → List formatting
    - WrapperHandler: style.wrap → Structural containers (xml, codeblock, etc.)

Usage:
    >>> from flow_core.styles import StyleRegistry
    >>> registry = StyleRegistry()
    >>> pre = registry.apply_pre(style, layer)
    >>> # ... compile content ...
    >>> post = registry.apply_post(style, layer)
    >>> result = registry.apply_wrap(style, content, layer)
"""

from .registry import StyleRegistry, StyleHandler
from .title_handler import TitleHandler
from .divider_handler import DividerHandler
from .list_handler import ListStyleHandler
from .wrapper_handler import WrapperHandler

__all__ = [
    "StyleRegistry",
    "StyleHandler",
    "TitleHandler",
    "DividerHandler",
    "ListStyleHandler",
    "WrapperHandler",
]
