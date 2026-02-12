# ADHD MCP

Minimal, context-efficient MCP server exposing ADHD framework capabilities for AI decision-making.

## Overview
- Provides 8 tools for project introspection, module management, and git operations
- Designed for fewer, smarter tools that inform AI agents rather than automating tasks
- Delegates business logic to specialized controllers (AdhdController, GitController, ContextController)

## Features
- **Project introspection** – `get_project_info` returns project metadata from root init.yaml
- **Module listing** – `list_modules` with optional layer filtering and import scanning
- **Module deep-dive** – `get_module_info` returns imports, git status, and dependency analysis
- **Module scaffolding** – `create_module` creates new modules with optional GitHub repo
- **Context file discovery** – `list_context_files` finds instructions, agents, and prompts
- **Flow compilation manifest** – `get_compilation_manifest` reads compiled_manifest.json
- **Skills listing** – `list_skills` scans available agent skills with descriptions
- **Git operations** – `git_modules` supports status, diff, pull, and push across modules

## Quickstart

```bash
# Run the MCP server
python -m adhd_mcp.adhd_mcp
```

```python
# Tool usage examples (called via MCP protocol)
get_project_info()
list_modules(layers=["foundation"], with_imports=True)
get_module_info("config_manager")
create_module(name="my_tool", layer="dev")
list_context_files(file_type="instruction")
get_compilation_manifest()
list_skills()
git_modules(action="status")
git_modules(action="push", module_name="logger_util", commit_message="fix: typo")
```

## API

```python
# MCP Tools (8 total)

@mcp.tool()
def get_project_info() -> dict: ...

@mcp.tool()
def list_modules(
    layers: list[str] | None = None,
    with_imports: bool = False,
) -> dict: ...

@mcp.tool()
def get_module_info(module_name: str) -> dict: ...

@mcp.tool()
def create_module(
    name: str,
    layer: str,
    is_mcp: bool = False,
    create_repo: bool = False,
    owner: str | None = None,
) -> dict: ...

@mcp.tool()
def list_context_files(
    file_type: str | None = None,
    include_modules: bool = True,
) -> dict: ...

@mcp.tool()
def get_compilation_manifest() -> dict: ...

@mcp.tool()
def list_skills() -> dict: ...

@mcp.tool()
def git_modules(
    action: str = "status",       # status | diff | pull | push
    module_name: str | None = None,
    layers: list[str] | None = None,
    commit_message: str | None = None,
) -> dict: ...
```

## Notes
- The server uses `FastMCP` from the `mcp` package with stdio transport.
- `AdhdController` is lazily initialized on first tool call.
- Git push requires `commit_message`; call `git_modules(action="diff")` first to inspect changes.
- CLI commands (`adhd refresh`, `adhd workspace`) are not wrapped — agents call them directly.

## Requirements & prerequisites
- `logger-util`
- `config-manager`
- `modules-controller-core`
- `module-creator-core`
- `github-api-core`
- `creator-common-core`
- `exceptions-core`
- `instruction-core`
- `pyyaml>=6.0`
- `mcp>=1.1.0`

## Troubleshooting
- **MCP server fails to start** – ensure `mcp>=1.1.0` is installed and the venv is activated.
- **Tool returns `module_not_found`** – check module name spelling; use `list_modules()` to see available names.
- **`init.yaml` not found error from `get_project_info`** – ensure the root `init.yaml` exists in the project root.
- **Git push fails** – verify `commit_message` is provided and the module has a configured remote.

## Module structure

```
adhd_mcp/
├─ __init__.py              # exports mcp server instance
├─ adhd_mcp.py              # FastMCP server with 8 tool decorators
├─ adhd_controller.py       # business logic for project/module tools
├─ context_controller.py    # instructions/agents/prompts scanning
├─ git_controller.py        # git status/diff/pull/push operations
├─ adhd_cli.py              # CLI command registration
├─ helpers.py               # import scanning and git utilities
├─ refresh_full.py          # module refresh script
├─ pyproject.toml           # module metadata
├─ requirements.txt         # MCP-specific dependencies
├─ README.md                # this file
└─ tests/                   # unit tests
```

## See also
- Modules Controller Core – module discovery and management used by all tools
- Instruction Core – context file scanning for `list_context_files`
- Module Creator Core – scaffolding logic for `create_module`
- GitHub API Core – repository creation for `create_module`