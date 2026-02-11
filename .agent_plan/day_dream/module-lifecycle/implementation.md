---
project: "Module Lifecycle"
current_phase: 0
phase_name: "Prerequisites"
status: TODO
last_updated: "2026-02-11"
---

# Implementation Plan

> Part of [Module Lifecycle](./_overview.md) · ⏳ [TODO]

<!--
⚠️  CODE EXAMPLES WARNING ⚠️
Examples in this document are ILLUSTRATIVE, not PRESCRIPTIVE.
The implementation agent (HyperArch) will determine actual details
based on current codebase state.
-->

---

## ⚙️ Phase 0: Prerequisites ⏳

**Goal:** *"Build the foundation pieces needed by both remove and update: reverse dep lookup + pyproject patcher remove"*

**Duration:** ■□□□ Light (1 slot)

**Walking Skeleton:** NOT NEEDED — Two isolated utility functions, testable independently.

### Exit Gate

- [ ] `DependencyWalker.get_reverse_deps(module_name)` returns correct dependents
- [ ] `pyproject_patcher.remove_from_root_pyproject(package_name, project_root)` cleans both deps and uv.sources
- [ ] Both functions have unit tests

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|---------|
| ⏳ | Add `get_reverse_deps()` to DependencyWalker | `modules_controller_core/dependency_walker.py` | `[KNOWN]` | [reverse-dep-lookup](./p0-prerequisites/reverse-dep-lookup.md) |
| ⏳ | Add `remove_from_root_pyproject()` to pyproject_patcher | `module_adder_core/pyproject_patcher.py` | `[KNOWN]` | [pyproject-patcher-remove](./p0-prerequisites/pyproject-patcher-remove.md) |
| ⏳ | Unit tests for both functions | `tests/` in respective modules | `[KNOWN]` | P0 |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ✅ 3 tasks (under limit)
- ✅ All `[KNOWN]` difficulty

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd deps <module-that-has-dependents>` then check reverse | Shows which modules depend on it |
| Add then remove a test dep from pyproject.toml via function | pyproject.toml returns to original state |

---

## 🔧 Phase 1: Core Commands ⏳

**Goal:** *"Implement `adhd remove` and `adhd update` commands with safety features"*

⚡ GIT CHECKPOINT — commit before this phase (new classes + CLI wiring)

**Duration:** ■■■□ Heavy (3 slots)

**Walking Skeleton:** NEEDED — Cross-module integration: CLI → controller → patcher → walker → uv sync → workspace regen. Prove the plumbing works with a stub remove before adding full logic.

### Exit Gate

- [ ] `adhd remove <name>` works end-to-end with safety checks
- [ ] `adhd update <name>` works end-to-end with atomic swap
- [ ] Dry-run mode works for both commands
- [ ] Reverse-dep warning triggers correctly
- [ ] Rollback on update failure is verified

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|---------|
| ⏳ | Create `ModuleRemover` class | `module_adder_core/module_remover.py` | `[KNOWN]` | [remove-command](./p1-core-commands/remove-command.md) |
| ⏳ | Create `ModuleUpdater` class with atomic swap | `module_adder_core/module_updater.py` | `[KNOWN]` | [update-command](./p1-core-commands/update-command.md) |
| ⏳ | Implement dry-run mode for remove + update | Both classes | `[KNOWN]` | [safety-features](./p1-core-commands/safety-features.md) |
| ⏳ | Implement backup + rollback for update | `ModuleUpdater` | `[KNOWN]` | [safety-features](./p1-core-commands/safety-features.md) |
| ⏳ | Wire `remove` command in `adhd_framework.py` | `adhd_framework.py` | `[KNOWN]` | [remove-command](./p1-core-commands/remove-command.md) |
| ⏳ | Wire `update` command in `adhd_framework.py` | `adhd_framework.py` | `[KNOWN]` | [update-command](./p1-core-commands/update-command.md) |
| ⏳ | Integration tests for remove + update | `tests/` | `[KNOWN]` | P1 |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd remove some-module --dry-run` | Shows preview of changes without modifying anything |
| `adhd remove some-module` | Prompts for confirmation, removes cleanly |
| `adhd update some-module --dry-run` | Shows what would change |
| Kill `adhd update` mid-swap | .bak directory still exists, workspace recoverable |

---

## 🏗️ Phase 2: Batch Operations ⏳

**Goal:** *"Add `--layer` flag to `adhd update` for batch module updates"*

**Duration:** ■□□□ Light (1 slot)

### Exit Gate

- [ ] `adhd update --layer dev` updates all dev-layer modules
- [ ] `adhd update --layer runtime` is rejected with clear error
- [ ] `--continue-on-error` works for batch

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|---------|
| ⏳ | Add `--layer` flag parsing to update command | `adhd_framework.py` | `[KNOWN]` | [batch-operations](./p2-batch-operations/batch-update-command.md) |
| ⏳ | Implement batch update logic in `ModuleUpdater` | `module_adder_core/module_updater.py` | `[KNOWN]` | [batch-operations](./p2-batch-operations/batch-update-command.md) |
| ⏳ | Add controller-level runtime layer guard | `ModuleUpdater` | `[KNOWN]` | [batch-operations](./p2-batch-operations/batch-update-command.md) |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd update --layer dev --dry-run` | Lists all dev modules and what would change |
| `adhd update --layer runtime` | Error: "Runtime modules are project-specific, update individually" |

---

## 📝 Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-11 | Swap pattern for update (not remove+re-add) | Avoids failure window |
| 2026-02-11 | Extend `module_adder_core`, defer rename | Functional value now > cosmetic rename risk |
| 2026-02-11 | `init.yaml` excluded from all operations | Legacy mechanism |
| 2026-02-11 | Controller-level `--layer runtime` guard | Defense in depth, not just CLI validation |
| 2026-02-11 | Walking skeleton for P1 | Cross-module integration (CLI → controller → patcher → walker → uv → workspace) |

---

**← Back to:** [Module Lifecycle Overview](./_overview.md)
