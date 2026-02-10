"""
Flow Core - A domain-specific language compiler for composable AI prompts.

This module provides the tokenizer, parser, resolver, and compiler for the Flow
language, enabling hierarchical composition of prompt fragments with node references.

Pipeline:
    Source → Tokenizer → Parser → Resolver → Compiler → Markdown

Usage:
    >>> from flow_core import compile_flow
    >>> source = '''
    ... @greeting |<<<Hello, World!>>>|.
    ... @out |$greeting|.
    ... '''
    >>> print(compile_flow(source))
    Hello, World!
"""

from .models import (
    Token,
    TokenType,
    Position,
    FlowParams,
    FlowStyle,
    FlowLLMStrategy,
    FlowNode,
    NodeRef,
    FileRef,
    ImportNode,
    Assignment,
    FlowFile,
    ContentItem,
    StringContent,
    ResolvedFlowFile,
)
from .dependency_graph import DependencyGraph, EdgeType, Tier
from .tokenizer import Tokenizer
from .parser import Parser, parse
from .resolver import Resolver, resolve, resolve_with_graph
from .compiler import Compiler, compile_resolved
from .flow_controller import FlowController, compile_flow, compile_flow_file
from .errors import (
    FlowError,
    TokenizerError,
    UnclosedStringError,
    ParserError,
    UnexpectedTokenError,
    DuplicateNodeError,
    ResolverError,
    UndefinedNodeError,
    UndefinedSlotError,
    CircularDependencyError,
    ImportFileNotFoundError,
    CircularImportError,
    CompilerError,
    MissingOutNodeError,
)

__all__ = [
    # Token types
    "Token",
    "TokenType",
    # AST nodes
    "Position",
    "FlowParams",
    "FlowStyle",
    "FlowLLMStrategy",
    "FlowNode",
    "NodeRef",
    "FileRef",
    "ImportNode",
    "Assignment",
    "FlowFile",
    "ContentItem",
    "StringContent",
    "ResolvedFlowFile",
    # Dependency Graph (P1)
    "DependencyGraph",
    "EdgeType",
    # Tokenizer
    "Tokenizer",
    # Parser
    "Parser",
    "parse",
    # Resolver
    "Resolver",
    "resolve",
    "resolve_with_graph",
    # Compiler
    "Compiler",
    "compile_resolved",
    # Controller
    "FlowController",
    "compile_flow",
    "compile_flow_file",
    # Errors
    "FlowError",
    "TokenizerError",
    "UnclosedStringError",
    "ParserError",
    "UnexpectedTokenError",
    "DuplicateNodeError",
    "ResolverError",
    "UndefinedNodeError",
    "UndefinedSlotError",
    "CircularDependencyError",
    "ImportFileNotFoundError",
    "CircularImportError",
    "CompilerError",
    "MissingOutNodeError",
]
