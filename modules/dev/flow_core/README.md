# Flow Core

Domain-specific language compiler for composable AI prompts.

## Overview

- Compiles Flow DSL source code into Markdown through a four-stage pipeline: tokenize → parse → resolve → compile.
- Supports hierarchical node composition with backward (`$`), forward (`^`), and file (`++`) references.
- Provides both a `FlowController` class for granular stage access and convenience functions for one-call compilation.

## Features

- Four-stage pipeline with individually accessible stages.
- Node definitions (`@name`), references (`$name`, `^name`), imports (`+./path.flow`), and assignments.
- String blocks with trim (`<<<...>>>`) and preserve (`<<...>>`) modes.
- Style system with pluggable handlers (titles, lists, blockquotes, code fences, dividers).
- Dependency graph with tiered visibility and DOT/Mermaid/JSON export.
- Incremental import resolution with circular dependency detection.
- LSP server for editor integration via `pygls`.
- Detailed error hierarchy with line/column positions.

## Quickstart

```python
from flow_core import compile_flow

source = """
@greeting |<<<Hello, World!>>>|.
@out |$greeting|.
"""
print(compile_flow(source))
# Hello, World!
```

```python
from flow_core import FlowController
from pathlib import Path

controller = FlowController()
markdown = controller.compile_file(Path("docs/intro.flow"))
```

## API

```python
# Convenience functions
def compile_flow(source: str, logger: Optional[Logger] = None) -> str: ...
def compile_flow_file(file_path: Path, logger: Optional[Logger] = None) -> str: ...

# Main controller
class FlowController:
    def __init__(self, logger: Optional[Logger] = None): ...
    def tokenize(self, source: str) -> List[Token]: ...
    def parse(self, tokens: List[Token]) -> FlowFile: ...
    def resolve(self, flow_file: FlowFile, base_path: Optional[Path] = None, source_path: Optional[str] = None) -> ResolvedFlowFile: ...
    def compile(self, resolved: ResolvedFlowFile, require_out: bool = True) -> str: ...
    def compile_source(self, source: str, base_path: Optional[Path] = None, require_out: bool = True) -> str: ...
    def compile_file(self, file_path: Path, require_out: bool = True) -> str: ...

# Pipeline stages
class Tokenizer:
    def __init__(self, logger: Optional[Logger] = None): ...
    def tokenize(self, source: str) -> List[Token]: ...

class Parser:
    def __init__(self, logger: Optional[Logger] = None): ...
    def parse(self, tokens: List[Token]) -> FlowFile: ...

class Resolver:
    def __init__(self, logger: Optional[Logger] = None): ...
    def resolve(self, flow_file: FlowFile, base_path: Optional[Path] = None, source_path: Optional[str] = None) -> ResolvedFlowFile: ...

class Compiler:
    def __init__(self, logger: Optional[Logger] = None): ...
    def compile(self, resolved: ResolvedFlowFile, require_out: bool = True) -> str: ...

# Dependency graph
class DependencyGraph:
    """Directed graph of node dependencies with tiered visibility and export to DOT, Mermaid, JSON."""

# Models (data classes): Token, TokenType, FlowNode, FlowFile, ResolvedFlowFile, FlowParams, FlowStyle, etc.
# Errors: FlowError, TokenizerError, ParserError, ResolverError, CompilerError, and specific subtypes.
```

## Notes

- The `@out` node is the entry point for compilation. If missing and `require_out=True`, a `MissingOutNodeError` is raised.
- Import paths in `.flow` files are resolved relative to the importing file's directory.
- Flow files under `_lib/` directories are shared fragments intended for import, not standalone compilation.
- See [manual.md](manual.md) for full Flow DSL syntax reference.

## Requirements & prerequisites

- `exceptions-core` — ADHD exception hierarchy
- `logger-util` — structured logging
- `pygls>=1.0.0` — Language Server Protocol framework (for LSP server)
- `lsprotocol>=2023.0.0` — LSP type definitions (for LSP server)

## Troubleshooting

- **`MissingOutNodeError`**: Ensure your `.flow` file defines an `@out` node as the compilation entry point, or pass `require_out=False`.
- **`CircularDependencyError`**: Check for cycles in `$`/`^` references or `+` imports. Use `DependencyGraph` export to visualize the dependency structure.
- **`ImportFileNotFoundError`**: Verify the import path is correct and relative to the importing file's directory.
- **`UnclosedStringError`**: Ensure `<<<` blocks are closed with `>>>` and `<<` blocks with `>>`.
- **LSP not starting**: Confirm `pygls` and `lsprotocol` are installed. The LSP server is in `flow_lsp.py`.
- **Import errors**: Run `uv sync` from the project root to install all workspace dependencies.

## Module structure

```
flow_core/
├─ __init__.py           # public exports (__all__)
├─ flow_controller.py    # main controller and convenience functions
├─ tokenizer.py          # Stage 1: source → tokens
├─ parser.py             # Stage 2: tokens → AST (FlowFile)
├─ resolver.py           # Stage 3: AST → resolved AST
├─ compiler.py           # Stage 4: resolved AST → Markdown
├─ models.py             # data classes (Token, FlowNode, FlowFile, etc.)
├─ errors.py             # error hierarchy
├─ dependency_graph.py   # dependency graph with DOT/Mermaid export
├─ flow_lsp.py           # Language Server Protocol integration
├─ flow_cli.py           # CLI entry point
├─ manual.md             # Flow DSL syntax reference
├─ refresh.py            # CLI refresh entry point
├─ styles/               # style handlers (title, list, divider, wrapper)
├─ tests/                # unit tests
├─ playground/           # exploration scripts
└─ pyproject.toml        # package metadata and dependencies
```

## See also

- Instruction Core — uses Flow Core for `.flow` compilation and instruction sync
- Logger Util — structured logging
- Exceptions Core — base exception hierarchy
