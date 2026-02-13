---
name: mcp-module-dev
description: "MCP server implementation workflow for ADHD modules. Covers FastMCP separation of concerns, required file structure, controller patterns, pyproject configuration, UV module invocation, STDIO-safe logging, and tool naming. Use this skill when building or updating MCP server modules (*_mcp.py), implementing MCP tools, or setting up MCP controller patterns."
---

# MCP Module Development

A guide for building MCP (Model Context Protocol) server modules within the ADHD Framework using the FastMCP pattern.

## When to Use
- Creating a new MCP server module
- Adding tools to an existing MCP module
- Implementing controller patterns for MCP business logic
- Configuring pyproject.toml for an MCP module
- Troubleshooting MCP server invocation or import issues

## Prerequisites
Load the **`module-dev`** skill first for general module patterns (imports, anti-hallucination rules, layer taxonomy, verification checklist). This skill covers MCP-specific concerns only.

---

## MCP Design Principles

1. **Separation of Concerns**: `*_mcp.py` is a thin wrapper — ALL business logic lives in `*_controller.py`
2. **STDIO-Safe Logging**: NEVER use `print()` — it corrupts JSON-RPC transport. Use `Logger` from `logger_util`
3. **UV Module Invocation**: MCP servers MUST be invoked as Python modules via `uv run`, never as direct scripts
4. **Controller Returns Dicts**: All controller methods return `dict[str, Any]` with `{"success": bool, ...}` pattern
5. **Tool Naming**: Use `snake_case` for all MCP tool names (MCP spec requirement)
6. **Docstrings Drive Schema**: FastMCP auto-generates tool schemas from function docstrings and type hints

---

## MCP Implementation SOP

### Step 1: Scaffold the Module
- Use `adhd_mcp` create_module tool with `is_mcp=True`
- This creates the MCP-specific files: `<name>_mcp.py`, `refresh.py`(or `refresh_full.py`), plus standard module files

### Step 2: Implement the Controller (`*_controller.py`)
- Class-based with `__init__(workspace_root: str | Path | None = None)`
- All methods return `dict[str, Any]` with `{"success": bool, ...}` pattern
- Use `Logger` for all logging — never `print()`
- Provide a module-level `get_<name>_controller()` singleton function

```python
from logger_util import Logger
from config_manager import ConfigManager

log = Logger(name="MyController", verbose=False)

class MyController:
    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self._cm = ConfigManager(workspace_root=workspace_root)

    def my_operation(self, arg: str) -> dict[str, Any]:
        """Perform the operation."""
        log.info(f"Running operation with {arg}")
        return {"success": True, "result": "done"}

def get_my_controller() -> MyController:
    """Module-level singleton accessor."""
    global _controller
    if _controller is None:
        _controller = MyController()
    return _controller

_controller: MyController | None = None
```

### Step 3: Implement the MCP Server (`*_mcp.py`)
- Import `FastMCP` and the controller
- Each `@mcp.tool()` function should be **under 10 lines** — delegate to controller
- Use lazy controller initialization via `_get_controller()`

```python
from mcp.server.fastmcp import FastMCP
from my_module.my_controller import MyController

mcp = FastMCP(name="my-module", instructions="Description of this MCP server")
_controller: MyController | None = None

def _get_controller() -> MyController:
    global _controller
    if _controller is None:
        _controller = MyController()
    return _controller

@mcp.tool()
def my_tool(arg: str) -> dict:
    """Tool description becomes MCP schema description.

    Args:
        arg: Description of this argument
    """
    return _get_controller().my_operation(arg)

def main() -> None:
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

### Step 4: Configure pyproject.toml
- Set `mcp = true` in `[tool.adhd]`
- Add `"mcp>=1.1.0"` to dependencies
- See [assets/pyproject-mcp-template.toml](assets/pyproject-mcp-template.toml) for the full template

### Step 5: Set Up refresh_full.py
- Creates the MCP entry in `.vscode/mcp.json` during `adhd refresh`
- Registers the UV module invocation command

### Step 6: Verify Invocation
```bash
# ✅ Correct: invoke as module via uv
uv run python -m my_module.my_module_mcp

# ❌ Wrong: direct script execution (breaks imports)
python modules/dev/my_module/my_module_mcp.py
```

---

## UV Invocation Pattern

MCP servers MUST be invoked as modules via uv for proper import resolution:

```bash
uv run python -m <module_name>.<mcp_file_name>
```

For MCP client configuration (Claude Desktop, VS Code, etc.):
```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "-m", "my_module.my_module_mcp"],
      "cwd": "./"
    }
  }
}
```

---

## Docstring-Driven Schema

FastMCP auto-generates the tool schema from your code:

| Source | Maps To |
|--------|---------|
| Function docstring (first line) | Tool description |
| Type hints on parameters | Argument types in schema |
| `Args:` section in docstring | Argument descriptions |
| Return type hint | Response type |

```python
@mcp.tool()
def search_files(pattern: str, max_results: int = 10) -> dict:
    """Search for files matching a glob pattern.

    Args:
        pattern: Glob pattern to match against file paths
        max_results: Maximum number of results to return
    """
    return _get_controller().search_files(pattern, max_results)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Putting business logic in `*_mcp.py` | Move to `*_controller.py` — MCP file is a thin wrapper |
| Using `print()` in MCP server | Use `Logger` from `logger_util` (stderr-safe) |
| Running MCP as direct script | Use `uv run python -m module.file` invocation |
| Tool functions exceeding 10 lines | Extract logic to controller methods |
| Missing docstrings on tools | Add docstring — it drives the MCP schema |
| Returning raw values instead of dicts | Controller methods return `{"success": bool, ...}` |
| Missing type hints on tool parameters | Add type hints — FastMCP uses them for schema |

---

## Reference Material

- **MCP file structure details**: See [references/mcp-file-structure.md](references/mcp-file-structure.md)
- **MCP pyproject.toml template**: See [assets/pyproject-mcp-template.toml](assets/pyproject-mcp-template.toml)
- **General module patterns**: Load the `module-dev` skill
- **MCP specification**: https://modelcontextprotocol.io/docs/develop/build-server
