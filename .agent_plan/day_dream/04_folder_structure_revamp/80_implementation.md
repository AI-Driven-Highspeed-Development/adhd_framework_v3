---
project: "Folder Structure Revamp"
current_phase: 5
phase_name: "Physical Migration"
status: COMPLETE
last_updated: "2026-02-05"
---

# 80 - Implementation Plan

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

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

## ⚡ Migration Strategy

**Big Bang Migration**: All phases will be completed before the framework is used.

- ❌ No backward compatibility with legacy folder structure (`cores/`, `managers/`, etc.)
- ❌ No dual-scanning of old and new directories
- ✅ Code targets END STATE only (`modules/foundation/`, `modules/runtime/`, `modules/dev/`)
- ✅ Simpler implementation, less code, fewer edge cases

---

## 🦴 Phase 0: modules_controller_core

**Goal:** *"Make discovery work with modules/ structure — all other phases depend on this"*

**Duration:** 2-3 days (HARD LIMIT)

**Spec:** [02_migration_modules_controller.md](./02_migration_modules_controller.md)

### Exit Gate

- [x] `discover_modules()` returns modules from `modules/foundation/`, `modules/runtime/`, `modules/dev/`
- [x] `layer_from_path()` correctly returns "foundation", "runtime", or "dev"

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ✅ | Update `module_enums.py` — new paths | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Rewrite discovery in `modules_controller.py` | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Add `layer_from_path()` function | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Update `module_filter.py` — remove type | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Remove dead issue codes | `modules_controller_core/` | `[KNOWN]` |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- Max 5 tasks ✅

### Target Folder Structure (P0)

```
cores/modules_controller_core/
├── __init__.py             (MODIFIED - exported new constants/functions)
├── module_enums.py         (MODIFIED - layer constants, layer_from_path())
├── modules_controller.py   (MODIFIED - dual discovery: legacy + modules/)
├── module_filter.py        (MODIFIED - accepts layer folder names)
├── module_issues.py        (MODIFIED - renamed issue codes)
└── tests/
    └── test_layer_discovery.py  (CREATED - 22 new tests)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Create `modules/foundation/test_mod/` with pyproject.toml | Discovered with layer="foundation" |
| Create `modules/runtime/test_plugin/` | Discovered with layer="runtime" |
| Create `modules/dev/test_util/` | Discovered with layer="dev" |

### P0 Completion Checklist

- [x] Exit gate commands run successfully
- [x] All tasks marked ✅
- [x] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [x] ≤5 tasks total
- [x] Manual verification steps pass (89 tests passing)

---

## 🏗️ Phase 1: module_creator_core

**Goal:** *"Wizard asks layer + MCP, routes to correct paths"*  
**Duration:** 1-2 days

**Spec:** [03_migration_module_creator.md](./03_migration_module_creator.md)

### Exit Gate

- [x] `adhd create module test` → asks layer question, creates in `modules/`

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ✅ | Update wizard questions | `module_creator_core/` | `[KNOWN]` |
| ✅ | Update routing logic | `module_creator_core/` | `[KNOWN]` |
| ✅ | Remove `SINGULAR_TO_FOLDER` | `module_creator_core/` | `[KNOWN]` |
| ✅ | Fix template `{module_type}` bug | `module_creator_core/` | `[KNOWN]` |
| ✅ | Update pyproject.toml template | `module_creator_core/` | `[KNOWN]` |

### Target Folder Structure (P1)

```
cores/module_creator_core/
├── module_creation_wizard.py  (MODIFIED)
├── module_creator.py          (MODIFIED)
└── templates/
    └── pyproject.toml.template (MODIFIED)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd create module test_mod` | Asks layer, MCP questions |
| Select "foundation" layer | Creates in `modules/foundation/test_mod/` |
| Select "runtime" layer | Creates in `modules/runtime/test_mod/` |
| Select "dev" layer | Creates in `modules/dev/test_mod/` |

### P1 Completion Checklist

- [x] Exit gate command runs successfully
- [x] All tasks marked ✅
- [x] Manual verification steps pass

### P1 Results (LEAN)

| Metric | Value |
|--------|-------|
| Lines Deleted | ~67 |
| Lines Added | ~36 |
| **Net Change** | **-45 lines** ✅ |

**Files Modified:** `module_creator.py`, `module_creation_wizard.py`, 4 templates, `adhd_controller.py`, `adhd_mcp.py`

---

## 🏗️ Phase 2: project_creator_core

**Goal:** *"New projects scaffold modules/ structure"*  
**Duration:** 1 day

**Spec:** [04_migration_project_creator.md](./04_migration_project_creator.md)

### Exit Gate

- [x] `adhd init new_project` → creates `modules/foundation/`, `modules/runtime/`, `modules/dev/`

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ✅ | Update `PROJECT_DIRECTORIES` | `project_creator_core/` | `[KNOWN]` |
| ✅ | Remove `_infer_folder_from_name()` | `project_creator_core/` | `[KNOWN]` |
| ✅ | Update `pyproject.toml.template` | `project_creator_core/` | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd init test_project` | Creates `modules/`, `modules/foundation/`, `modules/runtime/`, `modules/dev/` |
| Check `test_project/pyproject.toml` | Has `members = ["modules/**"]` |

### P2 Completion Checklist

- [x] Exit gate command runs successfully
- [x] All tasks marked ✅
- [x] Manual verification steps pass

### P2 Results (LEAN)

| Metric | Value |
|--------|-------|
| Lines Deleted | ~32 |
| Lines Added | ~13 |
| **Net Change** | **-19 lines** ✅ |

**Files Modified:** `project_creator.py`, `pyproject.toml.template`, `.gitignore.template`, `README.md`, `readme.md.template`

---

## 🏗️ Phase 3: adhd_mcp + CLI

**Goal:** *"External interfaces use layer filtering"*  
**Duration:** 1 day

**Spec:** [05_migration_adhd_mcp_cli.md](./05_migration_adhd_mcp_cli.md)

### Exit Gate

- [x] `list_modules(layers=["foundation"])` → returns foundation modules only
- [x] `adhd modules --layers runtime` → works

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ✅ | Update `adhd_mcp.py` tool definition | `adhd_mcp/` | `[KNOWN]` |
| ✅ | Update `adhd_controller.py` filtering | `adhd_mcp/` | `[KNOWN]` |
| ✅ | Update `adhd_cli.py` arguments | `adhd_mcp/` | `[KNOWN]` |
| ✅ | Update `test_mcp_tools.py` tests | `adhd_mcp/` | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| MCP: `list_modules(layers=["foundation"])` | Returns only foundation modules |
| CLI: `adhd modules --layers runtime` | Lists runtime modules only |

### P3 Completion Checklist

- [x] Exit gate commands run successfully
- [x] All tasks marked ✅
- [x] Manual verification steps pass

### P3 Results (LEAN)

| Metric | Value |
|--------|-------|
| Lines Deleted | ~40 |
| Lines Added | ~20 |
| **Net Change** | **-20 lines** ✅ |

**Files Modified:** `adhd_mcp.py`, `adhd_controller.py`, `adhd_cli.py`, `test_mcp_tools.py`

**API Changes:**
- MCP: `types` → `layers`, `include_cores` removed
- CLI: `--types` → `--layers`, `--include-cores` removed
- Output: `folder` → `layer` field

---

## 🏗️ Phase 4: Instruction Files

**Goal:** *"All instructions use modules/** patterns"*  
**Duration:** 1 day

**Spec:** [06_migration_instructions.md](./06_migration_instructions.md)

### Exit Gate

- [x] `grep -r "cores/" .github/instructions/` → no matches
- [x] Instructions apply to files in `modules/`

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ✅ | Update `adhd_framework_context.instructions.md` | `.github/instructions/` | `[KNOWN]` |
| ✅ | Update `modules.init.yaml.instructions.md` | `.github/instructions/` | `[KNOWN]` |
| ✅ | Update 9 applyTo patterns | `.github/instructions/` | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `grep -r "cores/" .github/instructions/` | No matches (agent files excepted) |
| Open `modules/foundation/config_manager/config_manager.py` | Config instructions apply |

### P4 Completion Checklist

- [x] Exit gate commands run successfully
- [x] All tasks marked ✅
- [x] Manual verification steps pass

### P4 Results (LEAN)

| Metric | Value |
|--------|-------|
| Files Modified | 10 |
| Pattern Updates | 9 applyTo patterns simplified |
| Content Updates | Project structure, type→layer, import paths |
| **Net Change** | **~0 lines** (patterns simplified) ✅ |

**Files Modified:**
- `cli_manager.instructions.md` - applyTo + templates
- `config_manager.instructions.md` - applyTo + imports
- `exceptions.instructions.md` - applyTo
- `logger_util.instructions.md` - applyTo + imports
- `mcp_development.instructions.md` - applyTo + paths + imports
- `module_development.instructions.md` - applyTo + content
- `module_instructions.instructions.md` - applyTo + templates
- `modules.init.yaml.instructions.md` - applyTo + type→layer
- `modules_readme.instructions.md` - applyTo
- `adhd_framework_context.instructions.md` - project structure

---

## 🏗️ Phase 5: Physical Migration

**Goal:** *"All modules physically in modules/ structure"*  
**Duration:** 2-3 days

**Spec:** [07_migration_existing_modules.md](./07_migration_existing_modules.md)

### Exit Gate

- [x] `ls modules/foundation/` → shows 15 foundation modules
- [x] `ls cores/` → directory doesn't exist
- [x] All imports use package-based format (stale imports fixed)

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ✅ | Create modules/ structure | root | `[KNOWN]` |
| ✅ | git mv foundation modules | root | `[KNOWN]` |
| ✅ | git mv dev modules | root | `[KNOWN]` |
| ✅ | git mv runtime modules | root | `[KNOWN]` |
| ✅ | Delete legacy folders | root | `[KNOWN]` |
| ✅ | Update import paths | all | `[KNOWN]` |
| ✅ | Run full test suite | all | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `ls modules/foundation/` | Shows 15 foundation modules |
| `ls cores/` | Directory doesn't exist |
| `adhd modules` | Lists all modules from new paths |
| `python -m pytest` | All tests pass |

### P5 Completion Checklist

- [x] Exit gate commands run successfully
- [x] All tasks marked ✅
- [x] Manual verification steps pass
- [x] Legacy folders deleted (cores/, managers/, utils/, plugins/, mcps/)
- [x] All stale imports fixed

### P5 Results (LEAN)

| Metric | Value |
|--------|-------|
| Modules Migrated | 16 |
| Legacy Folders Deleted | 5 |
| Stale Imports Fixed | 5 files |
| **Net Change** | **Clean modules/ structure** ✅ |

**New Structure:**
```
modules/
├── foundation/  (15 modules)
│   ├── exceptions_core/
│   ├── logger_util/
│   ├── config_manager/
│   ├── cli_manager/
│   ├── temp_files_manager/
│   ├── modules_controller_core/
│   ├── module_creator_core/
│   ├── project_creator_core/
│   ├── creator_common_core/
│   ├── instruction_core/
│   ├── github_api_core/
│   ├── workspace_core/
│   ├── questionary_core/
│   ├── uv_migrator_core/
│   └── yaml_reading_core/
├── runtime/
│   └── .gitkeep
└── dev/
    └── adhd_mcp/
```

---

## ⚠️ Error Handling Implementation

N/A — This is a migration, not new feature development. Existing error handling patterns remain unchanged.

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-04 | Remove `type` entirely | Subjective debates → objective layer | User |
| 2026-02-04 | Symmetric layer folders (Option C) | Scalability for 30+ modules, reduced cognitive load | User |
| 2026-02-04 | `layer` required in pyproject | External module portability | User |
| 2026-02-04 | `mcp = true` flag | Clear MCP identification | User |
| 2026-02-04 | No backward compatibility | Internal tooling, not public API | User |
| 2026-02-04 | No legacy compatibility during migration | Framework won't be used until all 6 phases complete; dual-structure support adds unnecessary complexity | User |

See [90_decision_log.md](./90_decision_log.md) for full rationale.

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| Automatic migration script | — | Too complex for internal tooling |
| Backward compat shim | — | Not needed for internal tooling |
| Layer dependency validation | — | Deferred to future feature |

---

## 📊 Overall Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| P0: modules_controller_core | 5 | ✅ [DONE] |
| P1: module_creator_core | 5 | ✅ [DONE] |
| P2: project_creator_core | 3 | ✅ [DONE] |
| P3: adhd_mcp + CLI | 4 | ✅ [DONE] |
| P4: Instruction Files | 3 | ✅ [DONE] |
| P5: Physical Migration | 7 | ✅ [DONE] |
| **Total** | **27** | **✅ 100% COMPLETE (27/27)** |

---

## 🎉 Migration Complete

**Date:** 2026-02-05

The Folder Structure Revamp has been successfully completed!

**Summary:**
- **16 modules** migrated to the new `modules/` structure
- **5 legacy folders** removed (`cores/`, `managers/`, `utils/`, `plugins/`, `mcps/`)
- **All imports** updated to package-based format
- **All tests** passing

The ADHD Framework now uses a clean, symmetric layer-based folder structure:
- `modules/foundation/` — Core infrastructure (15 modules)
- `modules/runtime/` — Runtime plugins (ready for future use)
- `modules/dev/` — Development tools (1 module: adhd_mcp)

---

**← Back to:** [Index](./00_index.md)
