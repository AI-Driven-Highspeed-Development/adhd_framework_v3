---
task: p01_03
title: Update writing-templates Skill
status: DONE
difficulty: "[KNOWN]"
---

# Update writing-templates Skill

## Scope

Update `.github/skills/writing-templates/SKILL.md` to replace all `templates/` path references with `_templates/`. Covers item #6 from §14.1.

## Specific Changes

| # | Change | Location in File |
|---|--------|-----------------|
| 1 | YAML description: update `placement rules (.agent_plan/day_dream/templates/)` → `(.agent_plan/day_dream/_templates/)` | Frontmatter line 3 |
| 2 | Placement section: update `Templates live in .agent_plan/day_dream/templates/:` → `_templates/` | Line ~38 |
| 3 | Placement section: update directory tree example root from `templates/` → `_templates/` | Line ~41 |
| 4 | Critical Rules table: update `ONLY in .agent_plan/day_dream/templates/` → `_templates/` | Line ~211 |
| 5 | Reference section: update `templates/simple.template.md` → `_templates/simple.template.md` | Bottom of file |
| 6 | Reference section: update `templates/blueprint/*.template.md` → `_templates/blueprint/*.template.md` | Bottom of file |

**Total:** ~6 path references to update.

## How to Verify (Manual)

1. `grep -c "day_dream/templates/" .github/skills/writing-templates/SKILL.md` — should return 0
2. `grep -c "day_dream/_templates/" .github/skills/writing-templates/SKILL.md` — should return ≥4

## Acceptance Criteria

- [x] Zero occurrences of `day_dream/templates/` in the file
- [x] All path references use `_templates/`
- [x] File still reads correctly and examples are coherent
