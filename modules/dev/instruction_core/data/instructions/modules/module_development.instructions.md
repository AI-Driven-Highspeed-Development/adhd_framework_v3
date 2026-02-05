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

- Templates exist for a reason—use them.

### Path Handling (MANDATORY)
Every `__init__.py` and `refresh.py` MUST include at the top:
```python
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.getcwd()
sys.path.insert(0, project_root)
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
| `__init__.py` | Exports, path setup, auto-refresh triggers |
| `init.yaml` | Module metadata: name, version, description, requirements, testing scope |
| `refresh.py` | Re-runnable setup logic (register configs, CLI, etc.) |
| `README.md` | Human-readable documentation |
| `.config_template` | Default config schema (optional) |
| `requirements.txt` | PyPI dependencies ONLY (not ADHD modules) |
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

See `testing_folders.instructions.md` for full decision tree.

## Verification Checklist
Before marking module work complete:
- [ ] Path handling in `__init__.py` and `refresh.py`
- [ ] Using `Logger`, not `print()`
- [ ] Using `ConfigManager` for paths/config
- [ ] Using `ADHDError` for operational errors
- [ ] No circular imports
- [ ] Type hints on all functions
- [ ] `refresh.py` is re-runnable (idempotent)