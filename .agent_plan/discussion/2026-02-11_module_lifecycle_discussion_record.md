# Discussion Record

| Field        | Value                                      |
| ------------ | ------------------------------------------ |
| Topic        | Module Remove & Update CLI Command Design  |
| Date         | 2026-02-11                                 |
| Participants | HyperDream, HyperArch, HyperSan           |
| Rounds       | 2                                          |
| Status       | Consensus ✅                                |

---

## Round 1: PROPOSE

**HyperDream**: Single `adhd mod` command group with symmetric add ↔ remove lifecycle. Update = remove + re-add. Batch guard is architectural. CLI naming under `adhd mod add/remove/update`. Dependency safety via DependencyWalker.

**HyperArch**: Remove reverses module_adder pipeline. ~70% infrastructure exists. Key risk: atomicity — if re-add fails after remove, module is gone. Proposes lightweight backup (snapshot 3 files). Reverse dep lookup non-negotiable.

**HyperSan**: TWO BLOCKERS: (1) DependencyWalker only walks forward, no reverse lookup exists. (2) pyproject_patcher is add-only. Also: dry-run mode, dependency-ordered batch execution, cleanup checklist (pyproject.toml, .code-workspace, uv.lock).

## Round 1: CHALLENGE

**HyperDream**: Conceded San's blockers are real P0 prerequisites, reframed as ~30-line scope work. Proposed dry-run-first approach for P0.

**HyperArch**: Agreed with San's blockers. Challenged Dream's "just re-clone" dismissal of rollback. Proposed lightweight backup of 3 mutable files.

**HyperSan**: Partially conceded blockers can be within implementation scope. Introduced swap pattern (copy new first, swap, delete old) to avoid failure window. Reverse dep must be first deliverable.

## Round 1: SYNTHESIZE — 2 ACCEPT, 1 REJECT

HyperSan REJECTED with 3 issues:

1. CLI naming inconsistency (`adhd mod remove` vs existing flat `adhd add`)
2. init.yaml is legacy, shouldn't be in backup list
3. `--layer all` contradicts runtime hard-block semantics

---

## Round 2: Revised SYNTHESIZE — All 3 ACCEPT

### Final Consensus

| #   | Decision      | Detail                                                                             |
| --- | ------------- | ---------------------------------------------------------------------------------- |
| 1   | CLI naming    | Flat: `adhd remove`, `adhd update`, `adhd update --layer dev\|foundation`          |
| 2   | Prerequisites | Reverse dep lookup + pyproject_patcher remove path (within P0)                     |
| 3   | Remove        | Reverse of add: unregister pyproject.toml, remove uv.sources, delete dir, uv sync |
| 4   | Update        | Swap pattern: clone new → validate → swap dirs → clean old                         |
| 5   | Safety        | Dry-run preview, lightweight backup (pyproject.toml, .code-workspace), confirmation|
| 6   | Batch         | `--layer dev\|foundation` explicit, runtime hard-blocked at controller level       |
| 7   | Cleanup       | pyproject.toml, uv.sources, module dir, uv sync, workspace regen via `adhd workspace` |
| 8   | Ownership     | Extend module_adder_core (rename to module_lifecycle_core deferred)                |

---

## Key Insights

- **Swap pattern** (San) avoids failure window of naive remove+re-add
- **init.yaml is legacy** — excluded from all operations
- **Runtime guard** at controller level, not just CLI
- **No `--layer all`** — explicit layer selection prevents accidents
- **Naming debt** (module_adder_core → module_lifecycle_core) documented for future
