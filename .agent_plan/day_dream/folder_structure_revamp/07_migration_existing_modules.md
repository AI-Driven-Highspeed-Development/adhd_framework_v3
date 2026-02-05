# 07 - Migration: Existing Modules

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  cores/exceptions_core/        │  modules/foundation/           │
│  managers/cli_manager/         │       exceptions_core/         │
│  utils/logger_util/            │       logger_util/             │
│  mcps/adhd_mcp/                │       config_manager/          │
│       ↓                        │       cli_manager/             │
│  💥 Scattered across 6 dirs    │       ...all framework modules │
│                                │  modules/runtime/              │
│                                │       (empty in framework)     │
│                                │  modules/dev/                  │
│                                │       hyper_red_core/          │
│                                │       adhd_mcp/                │
└────────────────────────────────┴────────────────────────────────┘
```

> **Key Insight**: This repo is the ADHD Framework "factory" — it creates projects, it doesn't ship as a product. All framework infrastructure modules are **foundation**. Runtime modules only appear in **generated projects** where users add app-specific logic.

### 🎯 One-Liner

> Physically move all existing modules to the new `modules/` structure using git mv for clean history.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Module locations | ❌ 6 scattered folders | ✅ Unified modules/ |
| Git history | Preserved with git mv | Preserved with git mv |
| Import paths | Will need updates | Will need updates |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Physically migrate all existing modules to new locations

**Priority:** P5 (Final Phase)  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Move all modules using `git mv`
- Update `pyproject.toml` workspace members
- Delete empty legacy folders
- Update any hardcoded import paths

**Out of Scope:**
- Renaming modules
- Refactoring module internals

---

## 📋 Module Migration Map

> **Framework Repo Context**: The ADHD Framework is a "factory" for generating projects. It will never "ship" as a product itself. Therefore:
> - **All framework infrastructure** = Foundation (they ARE the framework)
> - **Dev tooling** = Dev (testing utilities, red team tools)
> - **Runtime** = Empty here (only exists in generated projects)

### Foundation Layer → `modules/foundation/`

All framework modules go here because they ARE the framework infrastructure:

| Current Path | New Path | Rationale |
|--------------|----------|-----------|
| `cores/exceptions_core/` | `modules/foundation/exceptions_core/` | True zero deps |
| `utils/logger_util/` | `modules/foundation/logger_util/` | Core logging |
| `managers/config_manager/` | `modules/foundation/config_manager/` | Configuration management |
| `managers/cli_manager/` | `modules/foundation/cli_manager/` | Framework CLI infrastructure |
| `managers/temp_files_manager/` | `modules/foundation/temp_files_manager/` | Framework utility |
| `cores/modules_controller_core/` | `modules/foundation/modules_controller_core/` | Framework's module discovery |
| `cores/module_creator_core/` | `modules/foundation/module_creator_core/` | Framework's module creation |
| `cores/project_creator_core/` | `modules/foundation/project_creator_core/` | Framework's project generation |
| `cores/creator_common_core/` | `modules/foundation/creator_common_core/` | Shared creator utilities |
| `cores/instruction_core/` | `modules/foundation/instruction_core/` | Framework's instruction management |
| `cores/github_api_core/` | `modules/foundation/github_api_core/` | GitHub integration |
| `cores/yaml_reading_core/` | `modules/foundation/yaml_reading_core/` | YAML utilities |
| `cores/workspace_core/` | `modules/foundation/workspace_core/` | Workspace utilities |
| `cores/questionary_core/` | `modules/foundation/questionary_core/` | Interactive prompts |
| (all other cores) | `modules/foundation/{name}/` | Framework infrastructure |
| (all plugins) | `modules/foundation/{name}/` | Framework infrastructure |
| (all utils except dev) | `modules/foundation/{name}/` | Framework infrastructure |

> **Note**: All foundation modules only import from other foundation modules, never from runtime or dev. They form a DAG.

### Dev Layer → `modules/dev/`

| Current Path | New Path | Rationale |
|--------------|----------|-----------|
| `cores/hyper_red_core/` | `modules/dev/hyper_red_core/` | Dev-time testing only |
| `mcps/adhd_mcp/` | `modules/dev/adhd_mcp/` | MCP server for AI agents during development |
| Any test utilities | `modules/dev/` | Dev-time only |

### Runtime Layer → `modules/runtime/`

**⚠️ Empty in Framework Repo**

| Current Path | New Path |
|--------------|----------|
| *(none)* | *(none — created empty)* |

> **Why empty?** The ADHD Framework is a "factory" that generates projects. Runtime modules are app-specific — they only exist in **generated projects** where users add their own business logic, API handlers, plugins, etc.
>
> **In generated projects**, users will add runtime modules like:
> - `modules/runtime/my_api_handler/`
> - `modules/runtime/data_processor/`
> - `modules/runtime/custom_plugin/`

---

## 🔧 Implementation Details

### 1. Create New Directory Structure

```bash
mkdir -p modules/foundation
mkdir -p modules/runtime  # Empty in framework repo, but folder exists
mkdir -p modules/dev
```

### 2. Move Foundation Modules (ALL Framework Infrastructure)

```bash
# Core infrastructure (true zero deps first)
git mv cores/exceptions_core modules/foundation/
git mv utils/logger_util modules/foundation/
git mv managers/config_manager modules/foundation/

# CLI and utility infrastructure
git mv managers/cli_manager modules/foundation/
git mv managers/temp_files_manager modules/foundation/

# Framework controller/creator modules
git mv cores/modules_controller_core modules/foundation/
git mv cores/module_creator_core modules/foundation/
git mv cores/project_creator_core modules/foundation/
git mv cores/creator_common_core modules/foundation/

# Framework utility cores
git mv cores/instruction_core modules/foundation/
git mv cores/github_api_core modules/foundation/
git mv cores/yaml_reading_core modules/foundation/
git mv cores/workspace_core modules/foundation/
git mv cores/questionary_core modules/foundation/

# MCPs (framework tooling)
git mv mcps/adhd_mcp modules/dev/adhd_mcp/

# All remaining cores (framework infrastructure)
for core in cores/*/; do
    [ -d "$core" ] && git mv "$core" modules/foundation/
done

# All plugins (framework infrastructure)
for plugin in plugins/*/; do
    [ -d "$plugin" ] && git mv "$plugin" modules/foundation/
done

# All remaining utils (framework infrastructure)
for util in utils/*/; do
    [ -d "$util" ] && git mv "$util" modules/foundation/
done
```

### 3. Move Dev Modules

```bash
git mv cores/hyper_red_core modules/dev/
# Any other dev-only utilities
```

### 4. Runtime Layer

```bash
# Nothing to move — runtime is empty in framework repo
# The folder exists for generated projects to use
touch modules/runtime/.gitkeep
```

### 5. Delete Empty Legacy Folders

```bash
rmdir cores managers plugins utils mcps project 2>/dev/null || true
```

### 6. Update Root pyproject.toml

```toml
[tool.uv.workspace]
members = [
    "modules/**",
]
```

### 7. Update Import Paths

Search and replace in all Python files:

```python
# OLD
from cores.exceptions_core import ...
from managers.cli_manager import ...
from utils.logger_util import ...
from mcps.adhd_mcp import ...

# NEW
from modules.foundation.exceptions_core import ...
from modules.foundation.cli_manager import ...
from modules.foundation.logger_util import ...
from modules.dev.adhd_mcp import ...  # Dev layer (MCP for development)
```

---

## ⚠️ Risk: Import Path Updates

**Scope:** Every Python file that imports from another module needs updating.

**Mitigation Strategy:**
1. Run `grep -r "from cores\." --include="*.py"` to find all imports
2. Use sed or IDE refactoring for bulk updates
3. Run tests after each batch of changes

**Estimated import update count:** ~100-200 lines across project

---

## ✅ Acceptance Criteria

- [ ] All modules physically moved to correct locations
- [ ] Git history preserved for all files
- [ ] Empty legacy folders deleted
- [ ] Root pyproject.toml updated
- [ ] All import paths updated
- [ ] All tests pass after migration
- [ ] Module discovery finds all modules

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| All previous phases (P0-P4) | internal | Must complete first | Discovery + creation must work first |

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Create modules/ directory structure | `[KNOWN]` | ⏳ [TODO] |
| Move foundation modules (ALL framework infrastructure) | `[KNOWN]` | ⏳ [TODO] |
| Move dev modules | `[KNOWN]` | ⏳ [TODO] |
| Create empty runtime folder with .gitkeep | `[KNOWN]` | ⏳ [TODO] |
| Delete empty legacy folders | `[KNOWN]` | ⏳ [TODO] |
| Update root pyproject.toml | `[KNOWN]` | ⏳ [TODO] |
| Update all import paths | `[KNOWN]` | ⏳ [TODO] |
| Run full test suite | `[KNOWN]` | ⏳ [TODO] |
| Commit with descriptive message | `[KNOWN]` | ⏳ [TODO] |

---

## 🧪 Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `ls modules/foundation/` | Shows framework infrastructure modules (exceptions_core, logger_util, config_manager, cli_manager, etc.) |
| `ls modules/runtime/` | Empty (only .gitkeep) — runtime modules are added in generated projects |
| `ls modules/dev/` | Shows hyper_red_core, adhd_mcp, and any test utilities |
| `ls cores/ managers/ utils/` | Directories don't exist |
| `adhd modules` | Lists all modules from new paths |
| `python -c "from modules.foundation.logger_util import ..."` | Import works |
| `python -c "from modules.foundation.cli_manager import ..."` | Import works |

---

## 📜 Git Commit Message Template

```
refactor: migrate to unified modules/ structure

BREAKING: All modules moved from 6 legacy folders to modules/

Key insight: ADHD Framework = "factory" for generating projects.
All framework infrastructure is foundation, runtime is empty here.

Migration map:
- cores/ → modules/foundation/ (framework infrastructure)
- managers/ → modules/foundation/ (framework infrastructure)
- plugins/ → modules/foundation/ (framework infrastructure)  
- utils/ → modules/foundation/ (framework infrastructure)
- mcps/adhd_mcp → modules/dev/ (MCP for development)
- cores/hyper_red_core → modules/dev/ (testing tooling)

Layer structure:
- modules/foundation/* = framework infrastructure modules
- modules/runtime/* = empty (for generated projects)
- modules/dev/* = dev-time tooling (adhd_mcp, hyper_red_core)

All import paths updated accordingly.
```

---

## ✅ Migration Validation Checklist

### Physical Migration
- [ ] All modules in correct locations
- [ ] No modules left in legacy folders
- [ ] Git history intact

### Functional
- [ ] Module discovery works
- [ ] All imports resolve
- [ ] All tests pass

### Traceability
- [ ] Implements [01_feature_new_structure.md](./01_feature_new_structure.md)
- [ ] Depends on P0-P4 completion

---

**← Back to:** [Index](./00_index.md) | **Prev:** [06 - Instructions](./06_migration_instructions.md) | **Next:** [80 - Implementation](./80_implementation.md)
