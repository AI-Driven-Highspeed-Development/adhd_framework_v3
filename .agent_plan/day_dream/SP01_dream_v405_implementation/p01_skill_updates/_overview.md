---
name: p01_skill_updates
type: system
magnitude: Light
status: DONE
origin: .agent_plan/day_dream/SP01_dream_v405_implementation/_overview.md
last_updated: 2026-02-13
---

# p01 — Skill Updates

## Purpose

Rewrite three skill files to match DREAM v4.05 conventions. Each skill is an independent task — all three can execute in parallel. Requires p00 to complete first so `_templates/` paths are valid.

**Depends on:** p00_foundation (template paths must be renamed before skills can reference `_templates/`).

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_update_dream_planning_skill.md | Task | ✅ [DONE] | Rewrite dream-planning skill (items #7-9 from §14.1) |
| 02_update_day_dream_skill.md | Task | ✅ [DONE] | Rewrite day-dream skill (items #1-5 from §14.1) |
| 03_update_writing_templates_skill.md | Task | ✅ [DONE] | Update writing-templates skill (item #6 from §14.1) |

## Acceptance Criteria

- [x] `dream-planning` SKILL.md uses 8-slot magnitude scale, full frontmatter schema, no `plan.yaml` references
- [x] `day-dream` SKILL.md references `_templates/`, includes dependency/invalidation/knowledge-gap rules, Module Index gate, Plan Types (SP/PP)
- [x] `writing-templates` SKILL.md references `_templates/` paths throughout
- [x] All three skills cross-reference each other correctly
- [x] Synced copies in `instruction_core/data/skills/` match `.github/skills/` (handled by p02 or refresh)

## Integration Map

All three tasks are independent skill rewrites. Combined output: three v4.05-aligned skill files that cross-reference each other correctly.

## Reading Order

All three tasks are independent — execute in any order or parallel.
