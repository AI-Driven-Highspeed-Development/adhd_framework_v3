---
applyTo: "modules/**/*_mcp.py"
---

# MCP Server Development Guidelines

## Goals
- Standardize MCP server development using FastMCP pattern.
- Ensure clean separation between API layer (`*_mcp.py`) and business logic (`*_controller.py`).
- Guide agents to build consistent, maintainable MCP servers.

## Rules

### 1. **File Structure**: Every MCP MUST have these core files:
```
modules/<layer>/<module_name>/
├── __init__.py           # Exports, path setup, auto-refresh
├── pyproject.toml        # Module metadata (UV workspace member)
├── <name>_mcp.py         # FastMCP server: tool decorators ONLY
├── <name>_controller.py  # Business logic: all implementation here
├── refresh_full.py       # Module refresh logic for creating entry into .vscode/mcp.json
├── tests/                # Unit tests (optional)
└── playground/           # Interactive exploration (optional)
```
Add additional files as needed (e.g., `models.py`, `helpers.py`, `constants.py`).

### 2. **pyproject.toml Configuration**:
```toml
[project]
name = "adhd-mcp"
version = "0.0.1"
description = "ADHD Framework MCP: adhd_mcp"
requires-python = ">=3.11"
dependencies = [
    "mcp>=1.1.0",
    # ... workspace dependencies
]

[tool.adhd]
layer = "runtime"  # foundation | runtime | dev
mcp = true         # Required for MCP servers

[tool.uv.sources]
# Declare workspace dependencies
logger-util = { workspace = true }
# ... other workspace members

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 3. **UV Invocation Pattern** (CRITICAL):
MCPs MUST be invoked as modules via UV for proper import resolution:
```bash
# Correct invocation pattern:
uv run python -m adhd_mcp.adhd_mcp # module_name.mcp_server_file_name

# For Claude Desktop / MCP Client configuration:
{
  "mcpServers": {
    "adhd": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "-m", "adhd_mcp.adhd_mcp"],
      "cwd": "./"
    }
  }
}

# NEVER use direct script execution (breaks imports):
# ❌ python modules/runtime/adhd_mcp/adhd_mcp.py
# ❌ ./modules/runtime/adhd_mcp/adhd_mcp.py
```

### 4. **Separation of Concerns**:
- `*_mcp.py`: Thin wrapper. Contains ONLY `@mcp.tool()` decorators that delegate to controller.
- `*_controller.py`: All business logic, file I/O, validation, state management.
- NEVER put implementation logic in `*_mcp.py`—keep it under 10 lines per tool.

### 5. **FastMCP Setup** (in `*_mcp.py`):
```python
from mcp.server.fastmcp import FastMCP
from modules.<layer>.<module>.<name>_controller import <Name>Controller

mcp = FastMCP(name="<name>", instructions="<description>")
_controller: <Name>Controller | None = None

def _get_controller() -> <Name>Controller:
    global _controller
    if _controller is None:
        _controller = <Name>Controller()
    return _controller

@mcp.tool()
def my_tool(arg: str) -> dict:
    """Docstring becomes tool description. Args in docstring for schema."""
    return _get_controller().my_tool(arg)

def main() -> None:
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

### 6. **Controller Pattern** (in `*_controller.py`):
- Class-based with `__init__(workspace_root: str | Path | None = None)`.
- All methods return `dict[str, Any]` with `{"success": bool, ...}` pattern.
- Use `Logger` from `utils.logger_util` for logging.
- Provide module-level `get_<name>_controller()` singleton function.

### 7. **CLI Registration** (`*_cli.py`):
- Import: `from modules.runtime.cli_manager import CLIManager, ModuleRegistration, Command, CommandArg`
- Handler signature: `def handler_name(args: argparse.Namespace) -> int:`
- Handler path: `"modules.<layer>.<module>.<base>_cli:<function_name>"`
- Use `_get_controller()` singleton pattern for controller access.
- Return `int` (0 = success, non-zero = error).

### 8. **Logging**: NEVER use `print()` in STDIO-based MCP servers—corrupts JSON-RPC. Use:
```python
from modules.foundation.logger_util import Logger
log = Logger(name="<ControllerName>", verbose=False)
log.info("Safe logging to stderr")
```

### 9. **Tool Naming**: Follow MCP spec—use `snake_case` for tool names.

### 10. **Docstrings**: Required for every tool. FastMCP auto-generates schema from:
- Function docstring → tool description
- Type hints → argument types
- Docstring `Args:` section → argument descriptions

## External Documentation
- MCP Server Guide: https://modelcontextprotocol.io/docs/develop/build-server
- Core concepts: Resources (file-like data), Tools (LLM-callable functions), Prompts (templates)
