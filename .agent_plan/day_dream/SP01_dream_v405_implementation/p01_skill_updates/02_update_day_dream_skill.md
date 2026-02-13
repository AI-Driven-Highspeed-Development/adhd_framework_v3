---
task: p01_02
title: Update day-dream Skill
status: DONE
difficulty: "[KNOWN]"
---

# Update day-dream Skill

## Scope

Rewrite `.github/skills/day-dream/SKILL.md` to match DREAM v4.05. Covers items #1-5 from §14.1.

## Specific Changes

| # | Change | v4.05 Reference |
|---|--------|-----------------|
| 1 | Update ALL template path references from `templates/` to `_templates/` | §10.2, §15, item #1 |
| 2 | Add dependency graph fields (`depends_on`, `blocks`) to authoring rules and frontmatter documentation | §6, item #2 |
| 3 | Add invalidation protocol to authoring rules (fields, status variant `[DONE:invalidated-by:XXnn]`) | §7, item #2 |
| 4 | Add knowledge gap frontmatter (`knowledge_gaps:` string array) to authoring rules | §8, item #2 |
| 5 | Update folder structure examples: `SP01_`/`PP01_` prefixed dirs, `_completed/YYYY-QN/`, `_tree.md`, `_state_deltas_archive.md` | §10.2, item #3 |
| 6 | Add `dream validate` auto-trigger to plan closure rules | §12.3, item #4 |
| 7 | Add Module Index gate (table row + spec file) to closure checklist | §3.2, item #5 |
| 8 | Add Plan Types section (System Plan vs Procedure Plan) with file presence matrix (§2.4) | §1.5, §2.4 |
| 9 | Add `01_summary.template.md` to template listing (PP merged summary) | §15 |
| 10 | Update template location section header to reference `_templates/` | §15 |
| 11 | Remove `plan.yaml` from folder structure examples (metadata in frontmatter only) | §2.1 |
| 12 | Add State Delta section explaining format and cap (20 entries) | §4 |
| 13 | Add root `_overview.md` extended sections documentation (Current Sprint, Plans, Module Index, State Deltas) | §2.3 |
| 14 | Update estimation table to 8-slot scale if not already aligned | §1.3 |

## How to Verify (Manual)

1. Search for `templates/` (without underscore) in updated file — should return zero matches except in prose explaining the rename
2. Verify "Plan Types" section exists with SP/PP distinction
3. Verify Module Index gate documented in closure checklist

## Acceptance Criteria

- [x] All path references use `_templates/` (not `templates/`)
- [x] Dependency graph, invalidation, knowledge gap sections present
- [x] Plan Types (SP/PP) with file presence matrix documented
- [x] Module Index gate + State Delta + `dream validate` in closure rules
- [x] Folder structure example matches v4.05 §10.2
- [x] PP `01_summary.template.md` listed in template inventory
