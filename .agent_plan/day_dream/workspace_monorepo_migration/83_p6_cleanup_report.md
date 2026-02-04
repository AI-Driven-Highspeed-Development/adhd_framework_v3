# 83 - P6 Deprecated Code Removal — Report

> Part of [Workspace Monorepo Migration Blueprint](./00_index.md)

---

## Execution Summary

| Field | Value |
|-------|-------|
| **Date** | 2026-02-03 |
| **Strategy** | Parallel San identification → Arch removal → Validation |
| **Sans Deployed** | 5 (uv_migrator, modules_controller, creators, CLI, other modules) |

---

## Identification Results

| San | Modules | HIGH | MEDIUM | LOW |
|-----|---------|------|--------|-----|
| San-1 | uv_migrator_core | 0 | 3 | 3 |
| San-2 | modules_controller_core | 2 | 4 | 4 |
| San-3 | module_creator + project_creator | 2 | 2 | 1 |
| San-4 | adhd_mcp + adhd_framework | 0 | 7 | 4 |
| San-5 | Other modules | 0 | 2 | 1 |

---

## Items Removed

### HIGH Severity (Already Removed in Prior Sessions)

| ID | Module | Item | Status |
|----|--------|------|--------|
| HIGH-1 | modules_controller_core | `_parse_init_yaml_content()` | Already removed |
| HIGH-2 | modules_controller_core | `_create_init_yaml()` | Already removed |
| HIGH-3 | project_creator_core | `deprecated_templates.py` | Already removed |
| HIGH-4 | project_creator_core | Dead template machinery | Already removed |

### MEDIUM Severity (Removed This Session)

| ID | Module | Item | Status |
|----|--------|------|--------|
| MEDIUM-2 | modules_controller_core | `MISSING_REPO_URL` orphaned issue code | ✅ Removed |
| MEDIUM-4 | yaml_reading_core | `requirements.txt` legacy file | ✅ Deleted |
| MEDIUM-5 | questionary_core | `requirements.txt` legacy file | ✅ Deleted |
| MEDIUM-6 | root | Empty `app.py` file | ✅ Deleted |
| MEDIUM-7 | adhd_framework.py | `--fix`/`--format` placeholder flags | ✅ Removed |

### Items Already Clean (Not Found)

| ID | Item | Notes |
|----|------|-------|
| MEDIUM-1 | `INVALID_MODULE_REQUIREMENTS` | Already removed |
| MEDIUM-3 | `_singularize_folder()` | Already removed |

---

## Items Deferred (LOW Severity)

| ID | Module | Item | Reason |
|----|--------|------|--------|
| LOW-1 | uv_migrator_core | `_generate_source_url()` deprecated | Keep for potential future migrations |
| LOW-2 | adhd_mcp | `types` param → `folders` rename | API change, defer to v4.0 |
| LOW-3 | cli_manager | sys.path manipulation | Needs more testing |

---

## Validation Results

| Check | Result |
|-------|--------|
| **Test Suite** | 16/16 passed |
| **adhd refresh** | Completes without errors |
| **Grep checks** | All remaining "deprecated" matches are valid (docs, tests, migration tooling) |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total candidates identified** | 14 |
| **Removed this session** | 5 |
| **Already removed** | 6 |
| **Deferred (LOW)** | 3 |

---

## Files Deleted

1. `cores/yaml_reading_core/requirements.txt`
2. `cores/questionary_core/requirements.txt`
3. `app.py`

---

## Code Modified

| File | Change |
|------|--------|
| `cores/modules_controller_core/validation_issues.py` | Removed orphaned issue code |
| `adhd_framework.py` | Removed placeholder CLI flags |

---

**← Back to:** [Implementation Plan](./80_implementation.md) | [Blueprint Index](./00_index.md)
