---
project: "Layered Refresh System"
status: DONE
last_updated: "2026-02-06"
---

# 80 - Implementation Plan

> Part of [Layered Refresh System Blueprint](./00_index.md)

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

## 🏗️ Implementation

**Goal:** *"Dependency-ordered refresh with tiered script support."*

**Duration:** 3-5 days

### Exit Gate

- [x] `adhd refresh` → modules execute in dependency order (topo-sorted by declared deps)
- [x] `adhd refresh --full` → runs both `refresh.py` and `refresh_full.py` (where present) per module
- [x] Log output shows ordered execution list before running
- [x] Existing behavior preserved for modules with only `refresh.py`

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ✅ | Create `refresh_order.py` with `sort_modules_for_refresh()` using `graphlib.TopologicalSorter` — pure dependency sort across all modules (no layer grouping) | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Filter ADHD module deps from external deps in `pyproject.toml` dependencies — reuses `_package_name_to_module_name()` from `dependency_walker.py` | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Modify `ModulesController.refresh()` to use dependency-ordered list and support `full` flag — dependency ordering, silent skip, error continuation | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Add tiered script discovery: detect `refresh_full.py` alongside `refresh.py`, run both on `--full` | `modules_controller_core/` | `[KNOWN]` |
| ✅ | Add `--full` / `-f` flag to argparse refresh subcommand | `adhd_framework.py` / `admin_cli.py` | `[KNOWN]` |
| ✅ | Write unit tests for `sort_modules_for_refresh()` — 12 tests in `test_refresh_order.py`, all passing | `modules_controller_core/tests/` | `[KNOWN]` |

### Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ✅ 6 tasks (within reasonable scope)
- ✅ All `[KNOWN]` difficulty

### Target Folder Structure

```
modules/foundation/modules_controller_core/
├── refresh_order.py              (NEW)
├── modules_controller.py         (MODIFIED — refresh() uses ordered list + tiered scripts)
└── tests/
    └── test_refresh_order.py     (NEW)

adhd_framework.py                 (MODIFIED — --full flag wiring)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd refresh 2>&1 \| head -20` | Log shows `exceptions_core` and `logger_util` refreshing before `cli_manager`. Dev modules appear after foundation modules. Order respects declared dependencies. |
| `adhd refresh --full` on a module with `refresh_full.py` | Log shows both "Refreshing X..." and "Running full refresh for X..." |
| `adhd refresh` (without `--full`) on same module | Only `refresh.py` runs — no mention of `refresh_full.py` |

### Completion Checklist

- [x] Exit gate commands run successfully
- [x] All tasks marked ✅
- [x] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [x] Manual verification steps pass — post-check validated by HyperSan

---

## ⚠️ Error Handling Implementation

### Error Types

| Error Class | When Raised | Recovery |
|-------------|-------------|----------|
| `subprocess.CalledProcessError` | Refresh script exits non-zero | Log error, continue to next module |

> **Assumption:** The dependency graph is acyclic. Circular dependencies are validated and rejected at module-add/sync time (`adhd s` / `uv sync`), NOT at refresh time. By the time `adhd refresh` runs, the graph is guaranteed valid. Cycle detection is **out of scope** for this blueprint.
>
> **Not an error:** Modules without `refresh.py` or `refresh_full.py` are silently skipped. Most modules won't have refresh scripts — this is normal, not an error or warning condition.

### Logging Requirements

| Level | When | Example |
|-------|------|---------|
| ERROR | Refresh script fails (non-zero exit) | `"refresh.py failed for cli_manager: exit code 1"` |
| INFO | Module refreshed | `"Refreshing cli_manager..."`, `"Running full refresh for cli_manager..."` |
| DEBUG | Computed execution order | `"Refresh order: [exceptions_core, logger_util, ...]"` |

> **Silent skip:** Modules without `refresh.py` (or `refresh_full.py` on `--full`) produce NO log output. They are simply not mentioned.

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-06 | Pure dependency topo sort (not layer-first) | Layer alone is insufficient — modules within a layer have required ordering | User correction |
| 2026-02-06 | No staleness detection | `refresh.py` is a custom script, no generic change detection possible | User correction |
| 2026-02-06 | `refresh_full.py` naming for heavy tier | Self-documenting, backward-compatible, maps to `--full` CLI flag | HyperDream |
| 2026-02-06 | Single implementation phase | Not complex enough for multi-phase | User correction |
| 2026-02-06 | `refresh.py` and `refresh_full.py` are OPTIONAL | Most modules won't have refresh scripts. Missing = silent skip, no warning. | User correction |
| 2026-02-06 | Cycle detection out of scope for refresh | Circular deps validated at module-add/sync time. Refresh assumes acyclic graph. | User correction |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| Parallel tier execution | 2026-02-06 | No proven need. Sequential is fast enough for current module count. |
| Staleness detection (mtime/hash/`.refresh_stamp`) | 2026-02-06 | `refresh.py` is a custom script — no generic way to detect staleness. |
| `refresh_strategy` field (always/lazy/manual) | 2026-02-06 | Removed with staleness detection. No need for strategy when all scripts always run. |
| Layer-first grouping before topo sort | 2026-02-06 | Dependencies are the only ordering primitive. Layer grouping was incorrect. |
| `--module <name>` single-target flag | 2026-02-06 | Already exists in current codebase. |
| TTL-based expiry | 2026-02-06 | No real-world demand. |

---

## 🔬 Exploration Log

N/A — No active explorations. All items marked `[KNOWN]`.

---

**← Back to:** [Index](./00_index.md)
