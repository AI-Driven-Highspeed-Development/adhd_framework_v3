"""
dream_mcp - MCP Module

Dream management MCP server for day-dream planning artifacts.
Provides status, validation, and maintenance tools for ADHD planning workflows.

Usage as MCP Server:
    python -m dream_mcp.dream_mcp

Refresh to register in .vscode/mcp.json:
    python adhd_framework.py refresh --module dream_mcp
"""

from .dream_mcp import mcp

__all__ = [
    'mcp'
]
