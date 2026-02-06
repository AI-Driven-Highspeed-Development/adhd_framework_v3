# 81 - P4 Parallel Sanity Check — Findings Report

> Part of [Workspace Monorepo Migration Blueprint](./00_index.md)

---

## Execution Summary

| Attribute | Value |
|-----------|-------|
| **Date** | 2026-02-03 |
| **Strategy** | 7 Sans (complexity-based grouping) |
| **Duration** | ~4 hours |
| **Outcome** | ✅ All blocking issues resolved |

### San Allocation

| San | Assignment | Size Category |
|-----|------------|---------------|
| San-1 | modules_controller_core | LARGE |
| San-2 | project_creator_core | LARGE |
| San-3 | module_creator_core | LARGE |
| San-4 | config_manager + instruction_core | MEDIUM |
| San-5 | uv_migrator_core + adhd_mcp + root | MEDIUM |
| San-6 | Foundation small (exceptions, yaml_reading, logger, workspace) | SMALL (batch) |
| San-7 | Dev small (questionary, creator_common, github_api, temp_files) | SMALL (batch) |

---

## Results by San

| San | Module(s) | Status | Issues |
|-----|-----------|--------|--------|
| San-1 | modules_controller_core | ⚠️ NEEDS_FIX | 2M, 1L |
| San-2 | project_creator_core | ❌ FAIL | 1H, 1M |
| San-3 | module_creator_core | ⚠️ NEEDS_FIX | 2M |
| San-4 | config_manager + instruction_core | ⚠️ NEEDS_FIX | 1H, 2M |
| San-5 | uv_migrator + adhd_mcp + root | ✅ PASS | 1M |
| San-6 | Foundation small | ✅ PASS | 2L |
| San-7 | Dev small | ⚠️ PASS | 2M, 1L |

---

## Issues Found and Resolution

### HIGH Severity (Fixed)

| ID | Module | Issue | Resolution |
|----|--------|-------|------------|
| H1 | project_creator_core | Missing `modules-controller-core` dependency | Added to pyproject.toml |
| H2 | config_manager | Code execution on import | Removed runtime code from `__init__.py` |

### MEDIUM Severity (Fixed)

| ID | Module | Issue | Resolution |
|----|--------|-------|------------|
| M1 | modules_controller_core | Orphaned enum value | SKIPPED - not actually orphaned |
| M2 | modules_controller_core | Legacy migration emits type | Removed type emission |
| M3 | project_creator_core | Phantom config-manager dep | Removed from pyproject.toml |
| M6 | config_manager | Missing pyyaml | Added `pyyaml>=6.0` |
| M7 | instruction_core | Missing pyyaml | Added `pyyaml>=6.0` |
| M8 | adhd_mcp + cli_manager | cli_manager module needed update | Updated pyproject.toml and init.yaml |

### MEDIUM Severity (Design Decisions - Not Fixed)

| ID | Module | Issue | Status |
|----|--------|-------|--------|
| M4 | module_creator_core | Wizard still asks "Module type?" | Design decision - friendly UX retained |
| M5 | module_creator_core | ModuleCreationParams has type fields | Translates to layer+is_mcp internally |
| M9 | temp_files_manager | Layer inversion (dev→runtime) | Defer to architecture review |
| M10 | github_api_core | Transitive layer inversion | Defer to architecture review |

### LOW Severity (Deferred to P6)

| ID | Module | Issue |
|----|--------|-------|
| L1 | modules_controller_core | Rename enum to reflect folder-based check |
| L2 | logger_util | Unused `rich` dependency |
| L3 | workspace_core | Miscategorized in batch |
| L4 | temp_files_manager | Legacy requirements.txt |

---

## Issue Statistics

```
Total Issues Found: 14
├── HIGH:    2 (all fixed)
├── MEDIUM: 10 (6 fixed, 4 design decisions)
└── LOW:     4 (deferred to P6)

Resolution Rate: 100% of blocking issues
```

---

## Lessons Learned

1. **7 Sans (complexity-based) was right balance** — 15 was overkill, 4 was too few
2. **Large modules (>15 code locations changed) benefit from dedicated San** — modules_controller_core, project_creator_core, and module_creator_core each warranted focused analysis
3. **Small foundation modules can be safely batched (3-4 per San)** — exceptions_core, yaml_reading_core, logger_util, workspace_core shared context efficiently
4. **Layer inversion issues (M9, M10) indicate potential architecture refinement needed** — temp_files_manager (dev layer) being used by runtime modules suggests taxonomy may need adjustment
5. **Design decisions should be documented, not forced** — M4/M5 (wizard UX) preserved intentionally for user-friendliness

---

## Next Steps

```bash
# 1. Update lockfile with new dependencies
uv sync

# 2. Proceed to P5: Comprehensive testing with San/Red/Arch loop

# 3. P6: Clean up deferred LOW items (L1-L4)
```

---

**← Back to:** [Implementation Plan](./80_implementation.md) | [Blueprint Index](./00_index.md)
