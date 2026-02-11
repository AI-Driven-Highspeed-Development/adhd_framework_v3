# P0: Prerequisites

> ⏳ **[TODO]** — Build the foundation pieces needed by both remove and update commands.

---

## Purpose

Before implementing the remove and update commands, two foundational capabilities must exist: reverse dependency lookup (to warn before removing a module that other modules depend on) and pyproject.toml removal (the reverse of the existing add operation). These are isolated utility functions that can be built and tested independently.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| [02_reverse_dep_lookup.md](./02_reverse_dep_lookup.md) | Task | ⏳ [TODO] | Add `get_reverse_deps()` to `DependencyWalker` |
| [01_pyproject_patcher_remove.md](./01_pyproject_patcher_remove.md) | Task | ⏳ [TODO] | Add `remove_from_root_pyproject()` to `pyproject_patcher` |

## Integration Map

Both tasks are independent — no cross-dependency. They are consumed by P1's `ModuleRemover` and `ModuleUpdater`.

## Reading Order

1. [02_reverse_dep_lookup.md](./02_reverse_dep_lookup.md) — Foundation for safety checks
2. [01_pyproject_patcher_remove.md](./01_pyproject_patcher_remove.md) — Foundation for cleanup
