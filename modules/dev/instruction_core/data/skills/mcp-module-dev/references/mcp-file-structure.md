# MCP File Structure Reference

Detailed breakdown of file roles, controller patterns, and FastMCP usage in ADHD MCP modules.

---

## Required File Structure

Every MCP module lives under `modules/<layer>/<module_name>/` and contains these files:

```
modules/<layer>/<module_name>/
├── __init__.py               # Exports, package entry point
├── pyproject.toml            # Module metadata (mcp = true in [tool.adhd])
├── <name>_mcp.py             # FastMCP server: tool decorators ONLY
├── <name>_controller.py      # Business logic: ALL implementation here
├── refresh_full.py           # Registers MCP entry in .vscode/mcp.json
├── README.md                 # Human-readable documentation
├── tests/                    # Unit tests (optional)
└── playground/               # Interactive exploration (optional)
```

Additional files as needed: `models.py`, `helpers.py`, `constants.py`, etc.

---

## File Role Details

### `<name>_mcp.py` — MCP Server (Thin Wrapper)

This file contains **ONLY**:
- `FastMCP` instance creation
- `@mcp.tool()` decorated functions (under 10 lines each)
- Lazy controller initialization via `_get_controller()`
- `main()` function calling `mcp.run(transport="stdio")`

**What does NOT belong here:**
- Business logic, validation, file I/O
- Complex data transformations
- State management
- Direct database or API calls

### `<name>_controller.py` — Business Logic (All Implementation)

This file contains **ALL** the actual logic:
- Class-based: `class <Name>Controller`
- Constructor: `__init__(self, workspace_root: str | Path | None = None)`
- All methods return `dict[str, Any]` with `{"success": bool, ...}` pattern
- Uses `Logger` for logging, `ConfigManager` for paths/config
- Module-level singleton: `get_<name>_controller()` function

### `refresh_full.py` — MCP Registration

Runs during `adhd refresh` to:
- Register the MCP server entry in `.vscode/mcp.json`
- Set up the UV module invocation command
- Register any config templates

### `__init__.py` — Package Entry Point

Exports the controller and any public API:
```python
from .my_controller import MyController, get_my_controller

__all__ = ["MyController", "get_my_controller"]
```

---

## Controller Pattern

### Class Structure

```python
from __future__ import annotations
from typing import Any
from pathlib import Path

from logger_util import Logger
from config_manager import ConfigManager
from exceptions_core import ADHDError

log = Logger(name="MyController", verbose=False)


class MyController:
    """Controller for my_module MCP operations."""

    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self._cm = ConfigManager(workspace_root=workspace_root)

    def list_items(self) -> dict[str, Any]:
        """List all available items."""
        try:
            items = self._do_list()
            return {"success": True, "count": len(items), "items": items}
        except ADHDError:
            raise
        except Exception as e:
            log.error(f"Failed to list items: {e}")
            return {"success": False, "error": str(e)}

    def _do_list(self) -> list[dict]:
        """Internal: actual listing logic."""
        # Implementation here
        return []


# Module-level singleton
_controller: MyController | None = None


def get_my_controller(workspace_root: str | Path | None = None) -> MyController:
    """Get or create the singleton controller instance."""
    global _controller
    if _controller is None:
        _controller = MyController(workspace_root=workspace_root)
    return _controller
```

### Return Value Convention

All controller methods return dicts following this pattern:

```python
# Success
{"success": True, "data": ..., "count": ...}

# Failure
{"success": False, "error": "Human-readable error message"}

# List results
{"success": True, "count": 5, "items": [...]}
```

---

## FastMCP Server Pattern

### Minimal MCP Server

```python
from mcp.server.fastmcp import FastMCP
from my_module.my_controller import MyController

mcp = FastMCP(name="my-module", instructions="What this MCP server does")
_controller: MyController | None = None


def _get_controller() -> MyController:
    """Lazy controller initialization."""
    global _controller
    if _controller is None:
        _controller = MyController()
    return _controller


@mcp.tool()
def list_items() -> dict:
    """List all available items.

    Returns:
        dict with count and items array
    """
    return _get_controller().list_items()


@mcp.tool()
def get_item(name: str) -> dict:
    """Get a specific item by name.

    Args:
        name: The name of the item to retrieve
    """
    return _get_controller().get_item(name)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
```

---

## CLI Registration (Optional)

MCP modules may also register CLI commands for terminal access:

```python
# In <name>_cli.py
import argparse
from my_module.my_controller import get_my_controller


def handler_list(args: argparse.Namespace) -> int:
    """CLI handler for list command."""
    controller = get_my_controller()
    result = controller.list_items()
    if result["success"]:
        for item in result["items"]:
            print(item["name"])  # print() is OK in CLI, NOT in MCP
        return 0
    print(f"Error: {result['error']}")
    return 1
```

**Note**: `print()` is acceptable in CLI handlers (they use terminal, not STDIO transport). It is **forbidden** in `*_mcp.py` and `*_controller.py` files.
