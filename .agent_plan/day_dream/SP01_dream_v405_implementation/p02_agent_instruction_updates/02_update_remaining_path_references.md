---
task: p02_02
title: Update Remaining Path References
status: DONE
difficulty: "[KNOWN]"
---

# Update Remaining Path References

## Scope

Sweep all remaining files outside of skills (handled by p01) and flows/agents (handled by p02_01) that reference the old `templates/` path. Update to `_templates/`.

## Specific Changes

### Synced Skill Copies (instruction_core/data/skills/)

| # | File | Refs | Notes |
|---|------|------|-------|
| 1 | `modules/dev/instruction_core/data/skills/writing-templates/SKILL.md` | 5 | Mirror of `.github/skills/` — update or re-sync |
| 2 | `modules/dev/instruction_core/data/skills/day-dream/SKILL.md` | 1 | Mirror of `.github/skills/` — update or re-sync |
| 3 | `modules/dev/instruction_core/data/skills/orch-routing/SKILL.md` | 1 | Template ownership reference |

**Note:** Synced skills may auto-update when `adhd refresh --full` runs. Verify after p02_01 recompilation. If stale, manually update or trigger `instruction_core` refresh.

### Blueprint Documentation

| # | File | Refs | Notes |
|---|------|------|-------|
| 4 | `.agent_plan/day_dream/blueprint/02_architecture.md` | 2 | Architecture doc references template location |
| 5 | `.agent_plan/day_dream/blueprint/81_module_structure.md` | 7 | Module structure references template paths |

### Files Explicitly NOT Updated

| File | Reason |
|------|--------|
| `_archive/dream_iterations/DREAM_v4.md` | Historical archive — never edit |
| `_archive/dream_iterations/DREAM_v4.01.md` | Historical archive — never edit |
| `_archive/dream_iterations/DREAM_v4.02.md` | Historical archive — never edit |
| `_archive/dream-upgrade/architecture.md` | Historical archive — never edit |
| `DREAM_v4.05.md` | Spec uses `_templates/` already (§15) — no update needed |

## How to Verify (Manual)

1. `grep -r "day_dream/templates/" . --include="*.md" | grep -v _archive | grep -v DREAM_v4` — should return 0
2. Synced skills match `.github/skills/` versions

## Acceptance Criteria

- [x] Zero stale `templates/` references outside `_archive/` and DREAM version history files
- [x] Synced skill copies in `instruction_core/data/skills/` are current
- [x] Blueprint docs reference `_templates/` correctly
