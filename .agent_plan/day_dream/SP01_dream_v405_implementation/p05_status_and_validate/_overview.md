---
name: p05_status_and_validate
type: system
magnitude: Standard
status: TODO
origin: .agent_plan/day_dream/DREAM_v4.05.md
last_updated: 2026-02-13
depends_on:
  - p04_parsing_and_simple_commands
---

# p05 — P0: Status Dashboard & Validation Engine

## Purpose

Implement the two heavyweight P0 commands: `dream status` (aggregated sprint dashboard) and `dream validate` (comprehensive gate validation). These build on the parsing infrastructure from p04 and complete the P0 walking skeleton.

## Children

| Name | Type | Magnitude | Status | Description |
|------|------|-----------|--------|-------------|
| 01_dream_status_command.md | Task | Light | ⏳ [TODO] | Implement `dream status` — sprint dashboard with emergency/active/blocked |
| 02_dream_validate_core.md | Task | Standard | ⏳ [TODO] | Implement `dream validate` — frontmatter, Module Index, State Delta checks |
| 03_dream_validate_dag.md | Task | Light | ⏳ [TODO] | Implement `dream validate` — DAG cycle detection, bidirectional consistency |

## Integration Map

```
01_dream_status ────────────────────► P0 dashboard complete
02_dream_validate_core ──► 03_dream_validate_dag ──► P0 validation complete
```

Status is independent. Validate is split: core checks first, then DAG checks layered on top.

## Reading Order

1. 01_dream_status_command.md — independent
2. 02_dream_validate_core.md — independent of status, prerequisite for DAG
3. 03_dream_validate_dag.md — depends on 02 (extends validate)
