---
project: "UV Migration"
current_phase: 2
phase_name: "Complete"
status: DONE
last_updated: "2026-02-01"
progress: "P0 ✅ P1 ✅ - Both phases complete"
---

# 80 - Implementation Plan

> Part of [UV Migration Blueprint](./00_index.md)

<!-- 
⚠️  CODE EXAMPLES & FOLDER STRUCTURES WARNING ⚠️
════════════════════════════════════════════════════════════════════════════════
Examples in this document are ILLUSTRATIVE, not PRESCRIPTIVE.

• Folder structures show INTENT, actual paths may differ
• Commands show CONCEPT, actual syntax depends on tooling
• Task descriptions are GOALS, not step-by-step instructions

The implementation agent (HyperArch) will determine actual file locations,
command syntax, and implementation details based on current codebase state.
════════════════════════════════════════════════════════════════════════════════
-->

---

## 📊 Status Legend

| Icon | Status | Meaning |
|------|--------|---------|
| ⏳ | `[TODO]` | Not started |
| 🔄 | `[WIP]` | In progress |
| ✅ | `[DONE]` | Complete |
| 🚧 | `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 | `[CUT]` | Removed from scope |

---

## 🏗️ Phase 0: Core Migration

**Goal:** *"Generate pyproject.toml for all modules, eliminate ALL sys.path.insert() hacks, migrate to package imports"*

**Duration:** 1-2 weeks

### Exit Gate

- [x] Every module has pyproject.toml with `[tool.adhd]` ✅ *(16/16 - all modules complete)*
- [x] Root pyproject.toml exists with workspace config ✅
- [x] `uv sync` succeeds from clean clone ✅
- [x] **ZERO `sys.path.insert()` in any module** (grep returns 0 matches) ✅ *Verified 2026-02-01*
- [x] **All imports use package names** (no `from managers.x import`, only `from x import`) ✅ *Verified 2026-02-01*
- [x] `python -m session_manager` works from any directory ✅

### Tasks

| Status | Task | Module | Difficulty | Notes |
|--------|------|--------|------------|-------|
| ✅ | Create root pyproject.toml with workspace config | Root | `[KNOWN]` | `[tool.uv.workspace]` |
| ✅ | Generate pyproject.toml for each module | All modules | `[KNOWN]` | ✅ 16/16 complete |
| ✅ | Add `[tool.adhd]` section (type, repo_url) | All modules | `[KNOWN]` | ✅ 16/16 complete |
| ✅ | Add `[project.optional-dependencies]` for dev | Root | `[KNOWN]` | dev deps in root pyproject.toml |
| ✅ | **DELETE all `sys.path.insert()` hacks** | All modules | `[KNOWN]` | ✅ ZERO matches in grep |
| ✅ | **Migrate imports to package names** | All modules | `[KNOWN]` | ✅ Using `from logger_util import`, etc. |
| ✅ | Verify import graph matches pyproject.toml deps | Validation | `[KNOWN]` | ✅ Cross-checked actual imports |
| ✅ | Test `uv sync` from clean clone | Validation | `[KNOWN]` | ✅ CI/CD compatible |

### Target Folder Structure (P0)

```
pyproject.toml              (NEW - root workspace config)

cores/exceptions_core/
├── init.yaml               (UNCHANGED - will be deprecated in future)
├── pyproject.toml          (NEW - with [tool.adhd] + sources mapping)
├── __init__.py             (NEW - explicit relative imports)
└── adhd_exceptions.py      (MODIFIED - remove sys.path.insert!)

managers/session_manager/
├── __init__.py             (MODIFIED - explicit relative imports)
├── init.yaml               (UNCHANGED)
├── pyproject.toml          (NEW - with [tool.adhd] + sources mapping)
└── session_manager.py      (MODIFIED - imports become: from config_manager import...)

utils/logger_util/
├── __init__.py             (NEW - explicit relative imports)
├── init.yaml               (UNCHANGED)
├── pyproject.toml          (NEW - with sources mapping)
└── logger.py               (MODIFIED)

# ... same pattern for all modules
```

### pyproject.toml Config Pattern (CORRECT)

```toml
# ⚠️ WRONG - causes namespace pollution:
# [tool.hatch.build.targets.wheel]
# packages = ["."]
# ↑ This flattens files to top-level (e.g., `logger.py` becomes `from logger import`)

# ✅ CORRECT - wraps files in namespace:
[tool.hatch.build.targets.wheel]
only-include = ["."]

[tool.hatch.build.targets.wheel.sources]
"" = "module_name"  # Maps ALL files INTO this namespace
# ↑ This wraps files (e.g., `logger.py` becomes `from module_name.logger import`)
```

### Import Changes Example

```python
# ═══════════════════════════════════════════════════════════════════
# BEFORE (old path-hack style)
# ═══════════════════════════════════════════════════════════════════
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.getcwd()
sys.path.insert(0, project_root)  # ← THIS HACK MUST DIE

from managers.session_manager.session_manager import SessionManager
from managers.config_manager import ConfigManager
from logger import Logger  # ← WRONG: bare file import (namespace pollution)

# ═══════════════════════════════════════════════════════════════════
# AFTER (UV workspace with proper namespacing)
# ═══════════════════════════════════════════════════════════════════
# External package imports (other workspace members)
from session_manager import SessionManager      # Package namespace
from config_manager import ConfigManager        # Package namespace
from logger_util import Logger                  # Package namespace (NOT bare `logger`)

# For specific submodules within a package:
from session_manager.session_manager import SessionManager
from logger_util.logger import Logger

# ═══════════════════════════════════════════════════════════════════
# INSIDE __init__.py files (explicit relative imports)
# ═══════════════════════════════════════════════════════════════════
# cores/exceptions_core/__init__.py
from .adhd_exceptions import (  # ← Dot prefix = relative import
    ADHDException,
    ModuleNotFoundError,
    # ... etc
)

# utils/logger_util/__init__.py
from .logger import Logger  # ← Exports Logger at package level
```

> **Key Insight:** The package name (e.g., `logger_util`) is determined by the
> `[tool.hatch.build.targets.wheel.sources]` mapping, NOT the folder name.

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `rm -rf .venv && uv sync` | All deps installed, no errors |
| `grep -r "sys.path.insert" cores/ managers/ utils/` | **0 matches** |
| `python -c "from session_manager import SessionManager"` | Import succeeds |
| `cd managers/session_manager && python -m session_manager` | Works (standalone execution) |
| `cd /tmp && python -c "from config_manager import ConfigManager"` | Import succeeds |

### P0 Completion Checklist

- [x] Exit gate criteria met ✅ *(6/6 done)*
- [x] All tasks marked ✅ *(8/8 done)*
- [x] **ZERO path hacks remaining** (verified by grep) ✅ *2026-02-01*
- [x] Manual verification steps pass ✅

> **P0 COMPLETE** — All 16 modules migrated to UV workspace with proper `sources` mapping and namespace config.

---

## � Lessons Learned (P0 Implementation)

> **Updated:** 2026-02-01 — Discoveries during actual implementation

### 1. `packages = ["."]` Causes Namespace Pollution ❌

**Initial Approach (WRONG):**
```toml
[tool.hatch.build.targets.wheel]
packages = ["."]
```

**Problem:** This flattens all files to top-level modules:
- `logger.py` becomes importable as `from logger import Logger`
- `api.py` becomes `from api import ...`
- Conflicts with stdlib/other packages, namespace pollution

**Fixed Approach (CORRECT):**
```toml
[tool.hatch.build.targets.wheel]
only-include = ["."]

[tool.hatch.build.targets.wheel.sources]
"" = "logger_util"  # Wraps all files in this namespace
```

**Result:** Files are properly namespaced:
- `logger.py` becomes `from logger_util.logger import Logger`
- Package-level `__init__.py` can re-export: `from logger_util import Logger`

### 2. Explicit Relative Imports in `__init__.py` ✅

All `__init__.py` files must use **explicit relative imports**:

```python
# ✅ CORRECT
from .logger import Logger
from .adhd_exceptions import ADHDException

# ❌ WRONG (would look for external package)
from logger import Logger
```

### 3. Package Name ≠ Folder Name

The importable package name is determined by the `sources` mapping, not the filesystem:

| Folder Path | sources Mapping | Import As |
|-------------|-----------------|----------|
| `utils/logger_util/` | `"" = "logger_util"` | `from logger_util import` |
| `cores/github_api_core/` | `"" = "github_api_core"` | `from github_api_core import` |

### 4. Grep Patterns for Validation

```bash
# Find remaining path hacks (should return 0)
grep -rn "sys.path.insert" --include="*.py" | grep -v __pycache__

# Find incorrect bare imports (should return 0 after migration)
grep -rn "^from logger import\|^from api import\|^from adhd_exceptions import" \
  --include="*.py" | grep -v __pycache__

# Verify correct namespace imports
grep -rn "^from logger_util import\|^from github_api_core import" \
  --include="*.py" | grep -v __pycache__
```

### 5. UV Sync Dependency Resolution

When `uv sync` runs, workspace members are:
1. Built as wheels using hatch
2. Installed into `.venv` as editable packages
3. Available for import by their `[tool.hatch.build.targets.wheel.sources]` name

---

## �🛠️ Phase 1: UV Migrator Tool

**Goal:** *"Create `adhd migrate` CLI command for automated pyproject.toml generation"*

**Duration:** 3-5 days

### Exit Gate

- [x] `adhd migrate <module>` generates pyproject.toml ✅
- [x] `adhd migrate --all` migrates all modules ✅
- [x] `adhd migrate --dry-run` previews without writing ✅
- [x] Conversion preserves all init.yaml metadata ✅

### Tasks

| Status | Task | Module | Difficulty | Notes |
|--------|------|--------|------------|-------|
| ✅ | Create `uv_migrator_core` module structure | cores/ | `[KNOWN]` | ✅ Standard module layout |
| ✅ | Implement `parse_init_yaml()` | uv_migrator_core | `[KNOWN]` | ✅ Read init.yaml |
| ✅ | Implement `parse_requirements_txt()` | uv_migrator_core | `[KNOWN]` | ✅ Read requirements.txt |
| ✅ | Implement `github_url_to_package_name()` | uv_migrator_core | `[KNOWN]` | ✅ URL → package name |
| ✅ | Implement `convert_requirements()` | uv_migrator_core | `[KNOWN]` | ✅ Classify deps |
| ✅ | Implement `generate_pyproject_toml()` | uv_migrator_core | `[KNOWN]` | ✅ Template generation |
| ✅ | Create CLI command registration | uv_migrator_core | `[KNOWN]` | ✅ `adhd migrate` CLI ready |
| ✅ | Add `--dry-run` flag | uv_migrator_core | `[KNOWN]` | ✅ Preview mode |
| ✅ | Add `--all` flag | uv_migrator_core | `[KNOWN]` | ✅ Batch migration |
| ✅ | Add `--no-overwrite` flag | uv_migrator_core | `[KNOWN]` | ✅ Skip existing |
| ✅ | Write tests | tests/ | `[KNOWN]` | ✅ Conversion verification |

### Module Structure

```
cores/uv_migrator_core/
├── __init__.py
├── init.yaml
├── pyproject.toml
├── uv_migrator_core.py   # Main controller
├── migrator.py           # Conversion logic
├── templates.py          # pyproject.toml templates
├── README.md
└── requirements.txt      # tomlkit
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd migrate session_manager` | pyproject.toml created |
| `adhd migrate session_manager --dry-run` | Output printed, no file created |
| `adhd migrate --all` | All modules have pyproject.toml |
| `adhd migrate --all --no-overwrite` | Existing files untouched |
| Compare init.yaml version with output | Values match |

### P1 Completion Checklist

- [x] Exit gate criteria met ✅
- [x] All tasks marked ✅ *(11/11 done)*
- [x] Manual verification steps pass ✅
- [x] Tests pass ✅

> **P1 COMPLETE** — uv_migrator_core reviewed and fixed to P1 compliance. All functions implemented, CLI ready.

---

## 📋 Full Task Checklist

### Phase 0: Core Migration
- [x] Create root pyproject.toml with workspace config ✅
- [x] Generate pyproject.toml for each module (use `sources` mapping!) ✅ *(16/16 complete)*
- [x] Add `[tool.adhd]` section to all modules ✅ *(16/16 complete)*
- [x] Add `[project.optional-dependencies]` for dev ✅
- [x] DELETE all `sys.path.insert()` hacks ✅
- [x] Migrate imports to package names ✅
- [x] Verify import graph matches pyproject.toml deps ✅
- [x] Test `uv sync` from clean clone ✅

### Phase 1: UV Migrator Tool
- [x] Create `uv_migrator_core` module structure ✅
- [x] Implement `parse_init_yaml()` ✅
- [x] Implement `parse_requirements_txt()` ✅
- [x] Implement `github_url_to_package_name()` ✅
- [x] Implement `convert_requirements()` ✅
- [x] Implement `generate_pyproject_toml()` ✅
- [x] Create CLI command registration ✅
- [x] Add `--dry-run` flag ✅
- [x] Add `--all` flag ✅
- [x] Add `--no-overwrite` flag ✅
- [x] Write tests ✅

---

## 🎉 Completion Notes

**Date:** 2026-02-01

### P0: Core Migration — COMPLETE ✅

- **16 modules** migrated to UV workspace with proper namespace configuration
- All modules have `pyproject.toml` with correct `[tool.hatch.build.targets.wheel.sources]` mapping
- **ZERO** `sys.path.insert()` hacks remaining
- All imports use proper package namespaces (`from logger_util import`, not `from logger import`)

### P1: UV Migrator Tool — COMPLETE ✅

- `uv_migrator_core` module reviewed and fixed to match P1 requirements
- All core functions implemented: `parse_init_yaml()`, `parse_requirements_txt()`, `convert_requirements()`, `generate_pyproject_toml()`
- CLI interface ready with `--dry-run`, `--all`, and `--no-overwrite` flags

### Key Fixes Applied

| Issue | Fix |
|-------|-----|
| `packages = ["."]` caused namespace pollution | Changed to `sources` mapping: `"" = "module_name"` |
| Bare file imports (`from logger import`) | Explicit relative imports in `__init__.py`: `from .logger import` |
| Missing workspace member | `uv_migrator_core` added to root `pyproject.toml` workspace members |

### What's Ready for Production

1. ✅ UV workspace fully configured and functional
2. ✅ All modules importable by package name
3. ✅ `uv sync` works from clean clone
4. ✅ Migration tooling ready for future modules

---

## 🔗 Post-Migration: What's Next

After this blueprint is complete, the following blueprints can proceed:

| Blueprint | Dependency | What It Adds |
|-----------|------------|--------------|
| Layer Taxonomy | pyproject.toml exists | `[tool.adhd].layer` field |
| Dependency Closure Tool | Layer taxonomy | `adhd deps --closure` command |
| CLI Migration | UV migration | New `adhd` CLI entry point |
| init.yaml Deprecation | All above | Delete init.yaml files |

These are tracked in the `production_time_module_cut` blueprint.

---

**← Back to:** [Feature: UV Migrator Tool](./04_feature_uv_migrator_tool.md) | **Index:** [00_index.md](./00_index.md)
