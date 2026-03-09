---
applyTo: "modules/**"
---

# Module Structure Reference

Detailed file anatomy, naming formats, and dependency rules for ADHD Framework modules.
For layer taxonomy and role suffixes, see `adhd_framework_context.instructions.md`.

## File Structure

Every module lives under `modules/<layer>/<module_name>/`:

| File | Required | Purpose |
|:-----|:---------|:--------|
| `__init__.py` | Yes | Package entry point, exports public API |
| `pyproject.toml` | Yes | Metadata: name, version, deps, `[tool.adhd]` layer/mcp config |
| `README.md` | Yes | Human-readable documentation |
| `refresh.py` / `refresh_full.py` | Yes | Re-runnable setup (register configs, CLI commands, MCP entries) |
| `.config_template` | No | Default config schema — keys the module reads from ConfigManager |
| `<name>.instructions.md` | No | AI context for agents working on this module |
| `data/` | No | Module-specific data files (pushed to module repo) |
| `tests/` | No | Unit tests (pytest). Optional for <200 LOC |
| `playground/` | No | Interactive exploration. NOT production code |

## File Roles

**`__init__.py`** — Exports the module's public interface. Other modules import from here:
```python
from my_module import MyController, my_helper_function
```

**`pyproject.toml`** — Declares the module as a uv workspace member:
- `[project]` — name (kebab-case), version, description, dependencies
- `[tool.adhd]` — layer assignment, MCP flag
- `[tool.uv.sources]` — workspace dependency declarations
- `[build-system]` — always hatchling

**`refresh.py` / `refresh_full.py`** — Runs during `adhd refresh`:
- Config templates → project `.config` file
- CLI commands → CLI manager
- MCP entries → `.vscode/mcp.json`

**`data/`** — For module-repo data ONLY. For project-specific data, use `path` in `.config` which points to `project/data/<module_name>/`.

## Package Name vs Directory Name

| Context | Format | Example |
|:--------|:-------|:--------|
| Directory name | `snake_case` | `config_manager` |
| `pyproject.toml` `name` | `kebab-case` | `config-manager` |
| Python imports | `snake_case` | `from config_manager import ConfigManager` |
| `[tool.uv.sources]` keys | `kebab-case` | `config-manager = { workspace = true }` |

## Layer Dependency Rules

- **Foundation** modules must NOT depend on runtime or dev modules
- **Runtime** modules may depend on foundation but NOT dev modules
- **Dev** modules may depend on foundation and runtime modules
- All modules at any layer may depend on external PyPI packages

## Tests vs Playground

| Folder | Scope | Purpose | Persistence |
|:-------|:------|:--------|:------------|
| `<module>/tests/` | Single module | Unit tests, module-isolated | Permanent (git-tracked) |
| `<module>/playground/` | Single module | API exploration, demos | Semi-permanent (git-tracked) |
| `tests/` (project) | Cross-module | Integration tests, E2E | Permanent (git-tracked) |
| `playground/` (project) | Cross-module | Interactive exploration | Semi-permanent (git-tracked) |

**Rule**: CI → `tests/`. Human exploration → `playground/`.

### Naming in playground/
- `demo.py` — Primary demonstration script
- `explore_*.py` — Exploration scripts (e.g., `explore_api.py`)
- No formal test structure required

### Naming in tests/
- Follow pytest conventions: `test_*.py` files, `test_*` functions
- Run with: `pytest <module>/tests/`
