# Module Structure Reference

Detailed anatomy of an ADHD Framework module, naming conventions, and layer taxonomy.

---

## Module File Structure

Every ADHD module lives under `modules/<layer>/<module_name>/` and contains these files:

| File | Required | Purpose |
|:-----|:---------|:--------|
| `__init__.py` | Yes | Package entry point, exports public API |
| `pyproject.toml` | Yes | Module metadata: name, version, dependencies, `[tool.adhd]` layer/mcp config |
| `README.md` | Yes | Human-readable documentation |
| `refresh.py` / `refresh_full.py` | Yes | Re-runnable setup logic (register configs, CLI commands, MCP entries) |
| `.config_template` | No | Default config schema — defines keys the module reads from ConfigManager |
| `<name>.instructions.md` | No | AI context for agents working on this module (recommended) |
| `data/` | No | Module-specific data files (pushed to module repo) |
| `tests/` | No | Unit tests (pytest). Optional for <200 LOC, recommended for complex modules |
| `playground/` | No | Interactive exploration. NOT production code. Demo scripts, API experiments |

### File Roles Explained

**`__init__.py`** — Exports the module's public interface. Other modules import from here:
```python
from my_module import MyController, my_helper_function
```

**`pyproject.toml`** — Declares the module as a uv workspace member. Contains:
- `[project]` — name (kebab-case), version, description, dependencies
- `[tool.adhd]` — layer assignment, MCP flag
- `[tool.uv.sources]` — workspace dependency declarations
- `[build-system]` — always hatchling

**`refresh.py` / `refresh_full.py`** — Runs during `adhd refresh` to register module resources:
- Config templates → project `.config` file
- CLI commands → CLI manager
- MCP entries → `.vscode/mcp.json`

**`data/`** — For module-repo data ONLY (gets pushed to the module's git repo). For project-specific data, use `path` in `.config` which conventionally points to `project/data/<module_name>/`.

---

## Module Naming Conventions

Module directory names use `snake_case` with a descriptive suffix indicating purpose:

| Suffix | Purpose | Example |
|:-------|:--------|:--------|
| `_core` | Core logic, foundational capability | `flow_core`, `exceptions_core` |
| `_manager` | Manages a resource or lifecycle | `config_manager`, `cli_manager` |
| `_util` | Utility functions, helpers | `logger_util` |
| `_plugin` | Optional extension, add-on capability | `git_plugin` |
| `_mcp` | MCP server module (has `mcp = true`) | `adhd_mcp`, `dream_mcp` |

### Package Name vs Directory Name

| Context | Format | Example |
|:--------|:-------|:--------|
| Directory name | `snake_case` | `config_manager` |
| `pyproject.toml` `name` | `kebab-case` | `config-manager` |
| Python imports | `snake_case` | `from config_manager import ConfigManager` |
| `[tool.uv.sources]` keys | `kebab-case` | `config-manager = { workspace = true }` |

---

## Layer Taxonomy

Modules are organized into three layers based on their role:

| Layer | Path | Purpose | Dependencies |
|:------|:-----|:--------|:-------------|
| `foundation` | `modules/foundation/` | Core infrastructure — logging, config, exceptions | Minimal; no runtime/dev deps |
| `runtime` | `modules/runtime/` | Application logic — CLI, workspace management | May depend on foundation |
| `dev` | `modules/dev/` | Developer tools — MCP servers, module creators, instruction management | May depend on foundation + runtime |

### Layer Rules
- **Foundation** modules must NOT depend on runtime or dev modules
- **Runtime** modules may depend on foundation but NOT dev modules
- **Dev** modules may depend on foundation and runtime modules
- All modules at any layer may depend on external PyPI packages

---

## Tests vs Playground

| Folder | Scope | Purpose | Persistence |
|--------|-------|---------|-------------|
| `<module>/tests/` | Single module | Unit tests, module-isolated tests | Permanent (git-tracked) |
| `<module>/playground/` | Single module | API exploration, usage demos | Semi-permanent (git-tracked) |
| `tests/` (project) | Cross-module | Integration tests, E2E workflows | Permanent (git-tracked) |
| `playground/` (project) | Cross-module | Interactive exploration, demos | Semi-permanent (git-tracked) |

### Naming Conventions in playground/
- `demo.py` — Primary demonstration script
- `explore_*.py` — Exploration scripts (e.g., `explore_api.py`)
- No formal test structure required — these are for humans

### Test Conventions in tests/
- Follow pytest conventions: `test_*.py` files, `test_*` functions
- Run with: `pytest <module>/tests/`
- Load the `testing` skill for full pytest conventions and patterns
