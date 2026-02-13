---
name: module-dev
description: "Module implementation workflow for ADHD Framework Python modules. Covers mandatory pre-reads, anti-hallucination constraints, module structure, naming conventions, layer taxonomy, tests vs playground decisions, and verification checklist. Use this skill when creating or modifying module code, scaffolding new modules, or understanding ADHD module architecture."
---

# Module Development

A guide for building and modifying ADHD Framework Python modules following established patterns and conventions.

## When to Use
- Creating a new ADHD module from scratch
- Modifying existing module code
- Adding files to a module (tests, playground, configs)
- Understanding module file structure or naming conventions
- Checking pre-coding verification requirements

> **MCP Modules**: When implementing an MCP module (any module with `mcp = true` in `[tool.adhd]`), load the **`mcp-module-dev`** skill for MCP-specific patterns after reading this skill.

---

## Core Principles

1. **Anti-Hallucination First**: Never invent imports, APIs, or utilities. Search the codebase before writing.
2. **Use Existing Infrastructure**: Logger, ConfigManager, ADHDError, and module creation tools exist—use them.
3. **Separation of Concerns**: Each module has a single responsibility. Don't duplicate utilities across modules.
4. **Package Imports Only**: All imports use package imports via uv editable installs. No `sys.path.insert()`.
5. **No Manual Module Creation**: Always use `adhd_mcp` create_module tool for scaffolding.

---

## Pre-Coding Verification Checklist

Before writing **any** module code, complete these checks:

- [ ] **Read mandatory instructions**: `adhd_framework_context.instructions.md`, `logger_util.instructions.md`, `config_manager.instructions.md`, `exceptions.instructions.md`
- [ ] **Search for existing utilities**: Use `grep_search` or `semantic_search` before creating new helpers
- [ ] **Read source of modules you're calling**: Never guess API signatures — read the actual source file
- [ ] **Confirm module doesn't already exist**: Check `modules/` directory tree

---

## Module Development SOP

### Step 1: Plan the Module
- Determine the module's **single responsibility**
- Choose the correct **layer**: foundation, runtime, or dev
- Choose the correct **name suffix** (see [module-structure.md](references/module-structure.md))
- Decide: Does this need MCP? If yes, also load the `mcp-module-dev` skill

### Step 2: Scaffold with Tools
- **Use `adhd_mcp` create_module tool** — never create module files manually
- Confirm details before creation:
  - Create remote repo? Default: **No**
  - Public or private? Default: **Private**
  - Org name? Must be specified if creating remote repo (verify spelling with `adhd_mcp`)

### Step 3: Implement Core Logic
- Use **package imports** (no `sys.path.insert()`):
  ```python
  from logger_util import Logger
  from config_manager import ConfigManager
  from exceptions_core import ADHDError
  ```
- Use `Logger` — **never** `print()` (especially in MCP servers)
- Use `ConfigManager` for all path and config access — **never** hardcode paths
- Use `ADHDError` for operational errors
- Add **type hints** on all functions

### Step 4: Configure pyproject.toml
- See [pyproject-template.toml](assets/pyproject-template.toml) for the canonical template
- Set correct `[tool.adhd] layer` value
- Declare workspace dependencies in `[tool.uv.sources]`

### Step 5: Add Tests or Playground
- Use the decision tree below to choose the right location
- See the `testing` skill for full conventions

### Step 6: Verify Before Completion
Run the final verification checklist (below).

---

## Tests vs Playground Decision

| I want to... | Use |
|--------------|-----|
| Validate code works correctly | `tests/` |
| Explore how an API works | `playground/` |
| Create a demo for users | `playground/` |
| Regression protection | `tests/` |
| Quick prototype | `playground/` |
| CI/CD integration | `tests/` |

**Rule**: If it should run in CI → `tests/`. If it's for humans to explore → `playground/`.

---

## Import Patterns

```python
# ✅ Correct: package imports via uv editable installs
from logger_util import Logger
from config_manager import ConfigManager
from exceptions_core import ADHDError

# ❌ Wrong: sys.path manipulation
import sys
sys.path.insert(0, "../../foundation/logger_util")

# ❌ Wrong: relative imports across module boundaries
from ..foundation.logger_util import Logger
```

---

## Anti-Hallucination Rules

| Rule | Why |
|------|-----|
| **NEVER invent imports** | Search codebase first with `grep_search` or `semantic_search` |
| **NEVER guess API signatures** | Read the source file of the module you're calling |
| **NEVER create utilities that exist** | Check `modules/` directory first |
| **NEVER use `print()` in MCP servers** | Corrupts JSON-RPC. Use `Logger` from `logger_util` |
| **NEVER hardcode paths** | Use `ConfigManager` for all path resolution |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Creating module files manually | Use `adhd_mcp` create_module tool |
| Using `print()` for logging | Use `Logger` from `logger_util` |
| Hardcoding file paths | Use `ConfigManager` |
| Missing type hints | Add type hints to all function signatures |
| Circular imports | Restructure — use dependency injection or lazy imports |
| Guessing API parameters | Read the actual source module before calling |
| Creating a new utility without checking | Search `modules/` first for existing implementations |

---

## Final Verification Checklist

Before marking module work complete:

- [ ] Using package imports (no `sys.path.insert`)
- [ ] Using `Logger`, not `print()`
- [ ] Using `ConfigManager` for paths/config
- [ ] Using `ADHDError` for operational errors
- [ ] No circular imports
- [ ] Type hints on all functions
- [ ] `pyproject.toml` has correct `[tool.adhd]` layer
- [ ] Workspace dependencies declared in `[tool.uv.sources]`

---

## Reference Material

- **Module anatomy and file roles**: See [references/module-structure.md](references/module-structure.md)
- **pyproject.toml template**: See [assets/pyproject-template.toml](assets/pyproject-template.toml)
- **Testing conventions**: Load the `testing` skill
- **MCP-specific patterns**: Load the `mcp-module-dev` skill
