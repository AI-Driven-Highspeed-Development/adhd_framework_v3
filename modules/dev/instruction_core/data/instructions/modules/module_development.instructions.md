---
applyTo: "modules/**/*.py"
---

# Module Development Guidelines

## Goals
- Prevent hallucination by enforcing existing patterns.
- Ensure all modules integrate correctly with framework infrastructure.
- Standardize module creation and development.

## CRITICAL: Mandatory Reading Before ANY Module Work
Before writing or modifying module code, READ these instruction files:
1. `adhd_framework_context.instructions.md` - Framework structure and philosophy
2. `logger_util.instructions.md` - Logging (NEVER use `print()` in MCPs)
3. `config_manager.instructions.md` - Configuration access patterns
4. `exceptions.instructions.md` - Error handling (ADHDError vs standard exceptions)

## Module Creation Rules

### DO NOT Create Modules Manually
- **Use the module creation tools**: `adhd_mcp` provides `create_module` tool.
- **Confirm details**: Public vs private, self account / org name, always check the org name correct spelling with `adhd_mcp` before pushing.
- **Default options**: If user did not specify the following, use these defaults: 
  1. Create remote repo on Github or not? Do not create.
  2. Public or private? Private.
  3. Org name? No default, must be specified if creating remote repo.

- Templates exist for a reason—use them.

### Path Handling
All imports use package imports via uv editable installs. No `sys.path.insert()` needed:
```python
# v3 pattern: direct package imports
from logger_util import Logger
from config_manager import ConfigManager
from exceptions_core import ADHDError
```

## Anti-Hallucination Rules

1. **NEVER invent imports**: Search codebase first. Use `grep_search` or `semantic_search`.
2. **NEVER guess API signatures**: Read the source file of the module you're calling.
3. **NEVER create utilities that exist**: Check `modules/` first.
4. **NEVER use print() in MCP servers**: Corrupts JSON-RPC. Use `Logger` from `logger_util`.
5. **NEVER hardcode paths**: Use `ConfigManager` for paths.

## Module File Structure
Every module MUST include these core files:

| File | Purpose |
|:---|:---|
| `__init__.py` | Exports, package entry point |
| `pyproject.toml` | Module metadata: name, version, dependencies, `[tool.adhd]` layer/mcp config |
| `refresh.py` | Re-runnable setup logic (register configs, CLI, etc.) |
| `README.md` | Human-readable documentation |
| `.config_template` | Default config schema (optional) |
| `<name>.instructions.md` | AI context for this module (optional but recommended) |
| `data/` | Module-specific data files (optional) |
| `tests/` | Unit tests (pytest). **Optional** for <200 LOC, recommended for complex modules. Run with `pytest <module>/tests/`. |
| `playground/` | Interactive exploration. NOT production code. Demo scripts, API experiments. Naming: `demo.py`, `explore_*.py`. |

**NOTE**: `data/` is for module repo data ONLY (will push to repo). Use `path` in `.config` for project-specific data, conventionally under `project/data/<module_name>/`.

## When to Use tests/ vs playground/

| I want to... | Use |
|--------------|-----|
| Validate code works correctly | `tests/` |
| Explore how an API works | `playground/` |
| Create a demo for users | `playground/` |
| Regression protection | `tests/` |
| Quick prototype | `playground/` |
| CI/CD integration | `tests/` |

**Rule**: If it should run in CI → `tests/`. If it's for humans to explore → `playground/`.

See the `testing` skill for full decision tree.

## Verification Checklist
Before marking module work complete:
- [ ] Using package imports (no `sys.path.insert`)
- [ ] Using `Logger`, not `print()`
- [ ] Using `ConfigManager` for paths/config
- [ ] Using `ADHDError` for operational errors
- [ ] No circular imports
- [ ] Type hints on all functions
- [ ] `refresh.py` is re-runnable (idempotent)