---
name: p06_advanced_workflows
type: system
magnitude: Standard
status: TODO
origin: .agent_plan/day_dream/DREAM_v4.05.md
last_updated: 2026-02-13
depends_on:
  - p05_status_and_validate
---

# p06 — P1: Advanced Workflows

## Purpose

Implement the four P1 commands that harden enforcement under stress: `dream impact` (DAG walk), `dream history` (module change log), `dream emergency` (priority escalation), and `dream archive` (plan archival). These build on the DAG traversal and frontmatter parsing infrastructure from P0 phases.

## Children

| Name | Type | Magnitude | Status | Description |
|------|------|-----------|--------|-------------|
| 01_dream_impact_command.md | Task | Standard | ⏳ [TODO] | Implement `dream impact` — DAG walk, transitive deps, affected modules |
| 02_dream_history_command.md | Task | Trivial | ⏳ [TODO] | Implement `dream history` — module change history from State Deltas |
| 03_dream_emergency_archive.md | Task | Standard | ⏳ [TODO] | Implement `dream emergency` + `dream archive` — mutating workflows |

## Integration Map

```
01_dream_impact ──────────► read-only P1 complete
02_dream_history ─────────► read-only P1 complete
03_dream_emergency_archive ► mutating P1 complete
```

All three tasks are parallel-safe — no shared writes between commands.

## Reading Order

1. 01_dream_impact_command.md — independent (heaviest, read first)
2. 02_dream_history_command.md — independent, lightest
3. 03_dream_emergency_archive.md — independent (mutating commands grouped)
