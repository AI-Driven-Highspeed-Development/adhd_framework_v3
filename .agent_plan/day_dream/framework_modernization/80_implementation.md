---
project: "Framework Modernization (Post-UV)"
current_phase: 3
phase_name: "Deprecation & Cleanup"
status: COMPLETE
last_updated: "2026-02-02"
p0_complete: "2026-02-02"
p1_complete: "2026-02-02"
p2_complete: "2026-02-02"
p2_5_complete: "2026-02-02"
p3_complete: "2026-02-02"
---

# 80 - Implementation Plan

> Part of [Framework Modernization Blueprint](./00_index.md)

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

## 🦴 Phase 0: Walking Skeleton

**Goal:** *"New projects and modules can be created with UV-native pyproject.toml"*

**Duration:** 1 week (HARD LIMIT)

### Exit Gate

- [x] `adhd new-project` creates a project with pyproject.toml (no init.yaml)
- [x] `adhd create-module --type core` creates a module with pyproject.toml
- [x] `uv sync` works immediately after either operation

### Tasks

| Status | Task | Module | Difficulty | Doc Ref |
|--------|------|--------|------------|---------|
| ✅ | Replace `_write_init_yaml()` with `_write_pyproject_toml()` + embed templates | `project_creator_core/` | `[KNOWN]` | [03](./03_feature_project_creation.md) |
| ✅ | **REMOVE** template cloning logic, generate from embedded constants | `project_creator_core/` | `[KNOWN]` | [03](./03_feature_project_creation.md) |
| ✅ | Replace `_write_init_yaml()` with `_write_pyproject_toml()` + embed templates | `module_creator_core/` | `[KNOWN]` | [04](./04_feature_module_creation.md) |
| ✅ | Remove `_initialize_project()` call to ProjectInit, use `uv sync` | `project_creator_core/` | `[KNOWN]` | [03](./03_feature_project_creation.md) |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ✅ Max 5 tasks (consolidated to 4)
- ✅ All tasks `[KNOWN]` difficulty

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd new-project test-project` | Creates `test-project/pyproject.toml` with workspace config |
| `cd test-project && uv sync` | Installs dependencies, no errors |
| `adhd create-module --type core` in project | Creates `cores/new_module/pyproject.toml` |
| `uv sync` after module creation | Module becomes importable |

> ✅ **Verification Status:** All P0 verification steps passed successfully on 2026-02-02.
> - Project creation produces working UV workspace with embedded templates
> - Module creation produces importable module with pyproject.toml
> - Wizards simplified (no template selection, no preload prompts)

### P0 Completion Checklist

- [x] Exit gate commands run successfully
- [x] All tasks marked ✅
- [x] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [x] ≤5 tasks total
- [x] Manual verification steps pass

> 📄 **Implementation Details:** See [Embedded Template Implementation](./assets/02_embedded_templates_implementation.asset.md) for the detailed design documentation of the file-based template approach.

---

## 🏗️ Phase 1: Core Workflow Migration

**Goal:** *"All day-to-day workflows work with UV (init, refresh, list)"*  
**Duration:** 2 weeks

### Exit Gate

- [x] `adhd init` effectively runs `uv sync`
- [x] `adhd refresh` discovers modules from pyproject.toml
- [x] `adhd list` reads module info from pyproject.toml

### Tasks

| Status | Task | Module | Difficulty | Doc Ref |
|--------|------|--------|------------|---------|
| ✅ | Simplify `init_project()` to call `uv sync` | `adhd_framework.py` | `[KNOWN]` | - |
| ✅ | Update `scan_all_modules()` to read pyproject.toml | `modules_controller_core/` | `[KNOWN]` | [06](./06_feature_refresh_modernization.md) |
| ✅ | Update `list_modules()` to use new scanner | `adhd_framework.py` | `[KNOWN]` | - |
| ✅ | Add `--sync` flag to refresh command | `adhd_framework.py` | `[KNOWN]` | [06](./06_feature_refresh_modernization.md) |
| ✅ | Remove bootstrap logic (~200 LOC) | `adhd_framework.py` | `[KNOWN]` | [02](./02_architecture.md) |
| ✅ | Configure CLI as entry point in pyproject.toml | Root `pyproject.toml` | `[KNOWN]` | [07](./07_feature_cli_entry_points.md) |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd init` | Runs `uv sync` under the hood |
| `adhd list` | Shows all modules from workspace |
| `adhd refresh` | Runs refresh.py scripts, discovers modules |
| `adhd refresh --sync` | Runs `uv sync` then refresh.py scripts |
| `uv run adhd --help` | CLI works via entry point |

### P1 Completion Checklist

- [x] Exit gate commands run successfully
- [x] Bootstrap code removed from adhd_framework.py
- [x] CLI installable via `uv sync`
- [x] Manual verification steps pass

> ✅ **Verification Status:** All P1 verification steps passed successfully on 2026-02-02.
> - `adhd init` runs `uv sync` (tested)
> - `adhd list` shows 16 modules from pyproject.toml
> - `adhd refresh --sync` runs `uv sync` then refresh scripts
> - `uv run adhd --help` shows CLI via entry point
> - ~170 LOC bootstrap code removed
> - UVNotFoundError handling added for robustness

### Implementation Notes

**Additional Work Done (beyond original tasks):**

| Item | Module | Notes |
|------|--------|-------|
| `UVNotFoundError` exception | `exceptions_core/` | New exception class for UV-not-found scenarios |
| Workspace member dependencies | Root `pyproject.toml` | Added all 16 workspace members as dependencies |
| Fixed `os` import | `adhd_framework.py` | Missing import for `os.getcwd()` |
| Fixed `workspace_core` import | `adhd_framework.py` | Corrected import path |
| Added `workspace-core` dependency | `modules_controller_core/pyproject.toml` | Required for module scanning |

**Pre-existing Issues Noted (not P1 scope):**

| Issue | Location | Status | Notes |
|-------|----------|--------|-------|
| Relative import error | `instruction_core/refresh.py` | ✅ FIXED | Fixed in `adhd_framework.py`'s `_run_refresh_script()` method. Now detects relative imports and runs scripts as modules (`python -m`) with proper PYTHONPATH. |

---

## 📡 Phase 2: ~~Polish & Template Updates~~ Documentation

**Goal:** *"Documentation updated"*  
**Duration:** 1 week

> **DEPRECATED:** External template repos have been eliminated. Templates are now embedded directly in creator modules (YAGNI). This phase is reduced to documentation updates only.

### Tasks

| Status | Task | Module | Difficulty | Doc Ref |
|--------|------|--------|------------|---------|
| 🚫 | ~~Update project template repos with pyproject.toml~~ | ~~External repos~~ | `[CUT]` | ~~[08](./08_feature_template_updates.md)~~ |
| 🚫 | ~~Update .gitignore in templates for UV~~ | ~~Templates~~ | `[CUT]` | ~~[08](./08_feature_template_updates.md)~~ |
| 🚫 | ~~Update README templates with UV commands~~ | ~~Templates~~ | `[CUT]` | ~~[08](./08_feature_template_updates.md)~~ |
| ✅ | Document module inclusion patterns | Docs | `[KNOWN]` | [05](./05_feature_module_inclusion.md) |
| ✅ | Update framework README with UV workflow | `README.md` | `[KNOWN]` | - |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| ~~Check project template~~ | **N/A** - Templates embedded in creator code |
| Check creator embedded templates | Has `data/templates/` folder with `.template` files |
| Check README | References `uv sync`, not `adhd init` |

> ✅ **Verification Status:** All P2 verification steps passed successfully on 2026-02-02.
> - Module inclusion patterns documented in framework README.md
> - README expanded from ~17 to ~117 lines with comprehensive UV workflow
> - Includes workspace structure, module system, and usage examples

---

## 🔧 Phase 2.5: Developer Experience Commands

**Goal:** *"CLI commands for migration, sync, and health checks available"*  
**Duration:** 1 week

> **Rationale:** Before P3's aggressive cleanup (deleting init.yaml, removing legacy modules), provide CLI tools for users to migrate, validate, and sync their environments. These commands de-risk P3 and improve developer experience.

### Exit Gate

- [x] `adhd migrate` converts init.yaml to pyproject.toml
- [x] `adhd sync` runs `uv sync` (consolidates existing `init` functionality)
- [x] `adhd doctor` validates module health and reports issues

### Tasks

| Status | Task | Module | Difficulty | Doc Ref |
|--------|------|--------|------------|---------|
| ✅ | Create `migrate_module()` logic for init.yaml → pyproject.toml | `modules_controller_core/` | `[KNOWN]` | [09](./09_feature_init_yaml_sunset.md) |
| ✅ | Register `adhd migrate` CLI command | `adhd_framework.py` | `[KNOWN]` | [09](./09_feature_init_yaml_sunset.md) |
| ✅ | Add `--dry-run` and `--keep` flags to migrate | `adhd_framework.py` | `[KNOWN]` | [09](./09_feature_init_yaml_sunset.md) |
| ✅ | Rename/consolidate `init` → `sync` command | `adhd_framework.py` | `[KNOWN]` | - |
| ✅ | Create `doctor_check()` health validation logic | `modules_controller_core/` | `[KNOWN]` | - |
| ✅ | Register `adhd doctor` CLI command | `adhd_framework.py` | `[KNOWN]` | - |
| ✅ | Doctor: validate pyproject.toml exists and is parseable | `modules_controller_core/` | `[KNOWN]` | - |
| ✅ | Doctor: check for orphaned init.yaml files | `modules_controller_core/` | `[KNOWN]` | [09](./09_feature_init_yaml_sunset.md) |
| ⏳ | Doctor: validate workspace member dependencies | `modules_controller_core/` | `[EXPERIMENTAL]` | Deferred to P3+ |

### P2.5 Hard Limits

- ✅ Max 1 `[EXPERIMENTAL]` item (dependency validation may have edge cases)
- ❌ No `[RESEARCH]` items
- ✅ Commands should work in < 5 seconds for typical projects

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd migrate --dry-run` | Shows what would be converted, no changes made |
| `adhd migrate` | Converts init.yaml to pyproject.toml, deletes old file |
| `adhd migrate --keep` | Converts but keeps init.yaml as backup |
| `adhd sync` | Runs `uv sync`, shows success/error |
| `adhd doctor` | Reports module health: ✅ healthy, ⚠️ warnings, ❌ errors |
| `adhd doctor` (with init.yaml present) | Shows deprecation warning for init.yaml |

### Command Specifications

#### `adhd migrate`

```
Usage: adhd migrate [OPTIONS]

Migrate init.yaml modules to pyproject.toml format.

Options:
  --dry-run    Show what would be migrated without making changes
  --keep       Keep init.yaml after migration (for backup)
  --module     Migrate specific module only (default: all)

Exit codes:
  0 = Success (all migrated)
  1 = Partial failure (some modules failed)
  2 = Total failure (no modules migrated)
```

#### `adhd sync`

```
Usage: adhd sync [OPTIONS]

Synchronize project dependencies using uv.

Options:
  --frozen     Don't update lockfile (pass to uv sync --frozen)

Note: This consolidates the previous 'adhd init' functionality.
      'adhd init' remains as alias for backwards compatibility.
```

#### `adhd doctor`

```
Usage: adhd doctor [OPTIONS]

Check module health and report issues.

Options:
  --fix        Attempt to fix simple issues (e.g., formatting)
  --json       Output in JSON format for tooling

Checks performed:
  ✅ pyproject.toml exists and is valid TOML
  ✅ [project] section has name and version
  ✅ No orphaned init.yaml files (deprecation warning)
  ✅ Module is registered in workspace members
  ⚠️  Dependencies are resolvable (experimental)
```

### P2.5 Completion Checklist

- [x] Exit gate commands run successfully
- [x] All tasks marked ✅ (except 1 `[EXPERIMENTAL]` deferred)
- [x] No `[RESEARCH]` items
- [x] ≤1 `[EXPERIMENTAL]` item (deferred to P3+)
- [x] Manual verification steps pass

> ✅ **Verification Status:** All P2.5 verification steps passed successfully on 2026-02-02.
> - `adhd migrate --dry-run` shows migration candidates without changes
> - `adhd migrate` converts init.yaml to pyproject.toml
> - `adhd migrate --keep` preserves init.yaml as backup
> - `adhd sync` runs `uv sync` successfully
> - `adhd doctor` reports module health with ✅/⚠️/❌ indicators
> - Deprecation warnings shown for orphaned init.yaml files
> - `[EXPERIMENTAL]` workspace deps validation deferred (edge cases need research)

---

## 🧹 Phase 3: Deprecation & Cleanup

**Goal:** *"init.yaml removed, legacy code deleted"*  
**Duration:** 2 weeks (including grace period)

> **Prerequisite:** P2.5 must be complete. The `migrate`, `sync`, and `doctor` commands allow users to prepare their environments before this destructive phase.

### Tasks

| Status | Task | Module | Difficulty | Doc Ref |
|--------|------|--------|------------|---------|
| ✅ | Add deprecation warnings for init.yaml | `modules_controller_core/` | `[KNOWN]` | [09](./09_feature_init_yaml_sunset.md) |
| ✅ | Migrate all 14 modules' init.yaml to pyproject.toml | All modules | `[KNOWN]` | [09](./09_feature_init_yaml_sunset.md) |
| ✅ | Delete project_init_core (582 LOC) | `cores/` | `[KNOWN]` | [02](./02_architecture.md) |
| 🚫 | ~~Delete workspace_core (122 LOC)~~ | `cores/` | `[CUT]` | Still used by `adhd workspace` command |
| 🚫 | ~~Audit yaml_reading_core, delete if orphaned~~ | `cores/` | `[CUT]` | Active consumers: adhd_mcp, uv_migrator |
| ✅ | Delete all init.yaml files (15 files) | Everywhere | `[KNOWN]` | [09](./09_feature_init_yaml_sunset.md) |
| ✅ | **DELETE** `project/data/templates/` folder if exists | `project/` | `[KNOWN]` | N/A - folder didn't exist |
| 🚫 | ~~Remove init.yaml reading code~~ | `modules_controller_core/` | `[CUT]` | Needed for `adhd migrate` command |
| ✅ | **Make `repo_url` optional** for internal modules | `modules_controller_core/` | `[KNOWN]` | - |
| ✅ | **Update MCP instructions** for UV invocation pattern | `mcp_development.instructions.md` | `[KNOWN]` | - |
| 🚫 | ~~Remove `init` command alias~~ | `adhd_framework.py` | `[CUT]` | Kept as backward compat alias |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `find . -name "init.yaml"` | No results (root init.yaml deleted) |
| `grep -r "init.yaml" --include="*.py"` | Only migration-related code references (intentional) |
| `adhd list` | Works without init.yaml |
| `adhd refresh` | Works without init.yaml |

> ✅ **Verification Status:** P3 verification passed on 2026-02-02.
> - Root `init.yaml` deleted successfully
> - `project_init_core` directory removed entirely (582 LOC deleted)
> - `adhd req` and `adhd update-framework` commands removed (UV-superseded)
> - `repo_url` now optional in ModulesController
> - `workspace_core` retained: still used by `adhd workspace` command
> - `yaml_reading_core` retained: active consumers (adhd_mcp, uv_migrator)
> - `init` command kept as backward compat alias → `sync`
> - Init.yaml reading code kept in modules_controller for `adhd migrate` support

### P3 Completion Checklist

- [x] `project_init_core` deleted
- [x] Root `init.yaml` deleted
- [x] UV-superseded commands removed (`adhd req`, `adhd update-framework`)
- [x] `repo_url` made optional
- [x] MCP instructions updated for UV invocation
- [ ] `workspace_core` retained (still actively used)
- [ ] `yaml_reading_core` retained (has active consumers)
- [ ] `init` command retained (backward compat alias)

---

## 📊 Impact Summary

### Lines of Code

| Metric | Before | After Phase 3 |
|--------|--------|---------------|
| adhd_framework.py | 474 | ~250 |
| modules_controller_core | 576 | ~400 (kept migrate support) |
| project_init_core | 582 | 0 (deleted) |
| workspace_core | 122 | 122 (retained - still used) |
| yaml_reading_core | ~150 | ~150 (retained - active consumers) |
| **Total reduction** | | **~600 LOC** |

> **Note:** Actual LOC reduction lower than estimated. `workspace_core` and `yaml_reading_core` retained due to active usage. Init.yaml reading code kept for migration support.

### Files Eliminated

| File Type | Count | After Phase 3 |
|-----------|-------|---------------|
| init.yaml (root) | 1 | 0 |
| project_init_core (directory) | 1 | 0 |
| Per-module requirements.txt | ~14 | 0 |
| **Total files** | ~16 | 0 |

---

## ⚠️ Error Handling Implementation

### Error Types

| Error Class | When Raised | Recovery |
|-------------|-------------|----------|
| `UVNotFoundError` | UV not installed | Show install instructions |
| `PyprojectNotFoundError` | Missing pyproject.toml | Suggest migration |
| `WorkspaceConfigError` | Invalid workspace config | Show example |

### Logging Requirements

| Level | When | Example |
|-------|------|---------|
| ERROR | UV command fails | `"uv sync failed: {stderr}"` |
| WARNING | init.yaml found | `"Deprecated: init.yaml found, run 'adhd migrate-to-uv'"` |
| INFO | Operation success | `"✅ Module created successfully"` |

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-01 | Use Hatchling as build backend | Simple, UV-compatible | HyperDream |
| 2026-02-01 | Grace period for init.yaml | Allow migration time | HyperDream |
| 2026-02-01 | Project-local CLI over global | Safer versioning | HyperDream |
| 2026-02-01 | **Embed templates in creator modules** | External repos were YAGNI - never needed non-default templates | HyperDream |
| 2026-02-01 | **Eliminate `project/data/templates/` folder** | No template copying needed, simpler architecture | HyperDream |
| 2026-02-02 | **File-based templates over string constants** | Better readability, easier editing, cleaner diffs | HyperArch |
| 2026-02-02 | **Local `data/templates/` folders in creators** | Templates co-located with creator code, no external dependencies | HyperArch |
| 2026-02-02 | **P1 complete - core workflow migration done** | All 6 tasks complete, ~170 LOC bootstrap removed, CLI entry point working | HyperArch |
| 2026-02-02 | **P2 complete - documentation updated** | README expanded 17→117 lines, module inclusion patterns documented | HyperArch |
| 2026-02-02 | **Added P2.5 phase for DX commands** | `migrate`, `sync`, `doctor` commands de-risk P3 cleanup. Separates tool creation from destructive deletion. | HyperDream |
| 2026-02-02 | **`repo_url` optional for internal modules** | UV workspace model doesn't require separate repo URLs for monorepo modules. Flagging as error creates noise. Defer to P3 implementation. | HyperDream |
| 2026-02-02 | **MCP invocation via `uv run python -m`** | Module invocation pattern required for proper path/import resolution in UV workspace. Document in `mcp_development.instructions.md`. | HyperDream |
| 2026-02-02 | **P3: Retain `workspace_core`** | Still actively used by `adhd workspace` command. Deletion would break existing functionality. | HyperArch |
| 2026-02-02 | **P3: Retain `yaml_reading_core`** | Active consumers: adhd_mcp, uv_migrator_core, modules_controller. Not orphaned. | HyperArch |
| 2026-02-02 | **P3: Keep `init` as alias** | Backward compatibility for users expecting `adhd init`. Maps to `adhd sync`. | HyperArch |
| 2026-02-02 | **P3: Keep init.yaml reading code** | Required for `adhd migrate` command to function. Will deprecate when all users migrated. | HyperArch |
| 2026-02-02 | **P3 complete - deprecation & cleanup done** | project_init_core deleted, root init.yaml removed, UV-superseded commands removed, repo_url made optional | HyperArch |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| External template repos | 2026-02-01 | YAGNI - never needed non-default templates, embedded templates are simpler |
| `project/data/templates/` folder | 2026-02-01 | No longer needed - templates embedded in creator code |
| 08_feature_template_updates.md (as feature) | 2026-02-01 | Converted to deprecation doc - external templates eliminated |
| Template cloning logic | 2026-02-01 | Replaced by local `data/templates/` folder with `.template` files |
| `creator_common_core` module | 2026-02-02 | Templates embedded in creator modules - marked `DEPRECATED_P3` |
| `preload_sets` config | 2026-02-02 | Projects start empty - no preload template selection needed |
| Template selection UI | 2026-02-02 | Single embedded template per type - simplified wizards |

---

## 🔬 Exploration Log

| Date | Topic | Status | Synthesized To |
|------|-------|--------|----------------|
| 2026-02-01 | UV Impact Analysis | SYNTHESIZED | 06_impact_analysis.md |

---

**← Back to:** [09 - Feature: init.yaml Sunset](./09_feature_init_yaml_sunset.md)
