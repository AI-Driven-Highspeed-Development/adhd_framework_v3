---
task: p00_01
title: Rename templates/ → _templates/
status: DONE
difficulty: "[KNOWN]"
---

# Rename templates/ → _templates/

## Scope

Physically rename the template directory from `templates/` to `_templates/` to follow v4.05's infrastructure underscore convention (§10.3). This is the single blocking prerequisite for all path reference updates.

## Specific Changes

| # | Action | Target |
|---|--------|--------|
| 1 | `git mv .agent_plan/day_dream/templates/ .agent_plan/day_dream/_templates/` | Directory rename |
| 2 | Verify all subdirectories moved cleanly | `_templates/blueprint/`, `_templates/assets/`, `_templates/examples/` |
| 3 | Verify no broken symlinks or references within `_templates/` | Internal relative links |

## How to Verify (Manual)

1. Run `ls .agent_plan/day_dream/_templates/` — should list `simple.template.md`, `blueprint/`, `assets/`, `examples/`
2. Run `ls .agent_plan/day_dream/templates/` — should return "No such file or directory"
3. Run `git status` — should show rename, not delete+create

## Acceptance Criteria

- [x] `_templates/` exists with all contents from former `templates/`
- [x] `templates/` no longer exists
- [x] Git tracks as rename (not delete + add)
