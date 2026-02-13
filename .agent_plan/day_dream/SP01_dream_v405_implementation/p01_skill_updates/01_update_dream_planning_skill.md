---
task: p01_01
title: Update dream-planning Skill
status: DONE
difficulty: "[KNOWN]"
---

# Update dream-planning Skill

## Scope

Rewrite `.github/skills/dream-planning/SKILL.md` to match DREAM v4.05. Covers items #7-9 from §14.1.

## Specific Changes

| # | Change | v4.05 Reference |
|---|--------|-----------------|
| 1 | Update magnitude routing to 8-slot scale (`■□□□□□□□` Trivial through `■■■■■■■■` Epic) with slot MAXIMUMS (1/2/3/5/8) | §1.3 |
| 2 | Remove ALL `plan.yaml` references — metadata lives in `_overview.md` frontmatter ONLY | §2.1, item #8 |
| 3 | Update `_overview.md` convention with full frontmatter schema (name, type, magnitude, status, origin, last_updated, depends_on, blocks, knowledge_gaps, priority, etc.) | §2.1, item #9 |
| 4 | Update folder structure examples to show `SP01_`/`PP01_` prefixed plan directories | §10.1 |
| 5 | Add `_completed/YYYY-QN/` archive directory to folder examples | §10.5 |
| 6 | Add `_tree.md` generated file to folder examples | §10.3 |
| 7 | Add dependency graph fields documentation (`depends_on`, `blocks`) — plan-level only, no phase-level deps | §6 |
| 8 | Add invalidation protocol section (fields, rules, flow) | §7 |
| 9 | Add Module Index gate to plan closure rules (table row + spec file both required) | §3.2 |
| 10 | Add State Delta as closure gate condition | §4 |
| 11 | Add `dream validate` auto-trigger to closure protocol | §12.3 |
| 12 | Update plan closure gates to match v4.05 §12.3 full gate list | §12.3 |
| 13 | Add Plan Types section (System Plan vs Procedure Plan, SP/PP prefixes) | §1.5 |
| 14 | Update anti-patterns table with v4.05 additions | Various |

## How to Verify (Manual)

1. Search for `plan.yaml` in updated file — should return zero matches
2. Verify magnitude table shows 8-slot scale with slot maximums
3. Verify `_overview.md` frontmatter example includes `origin:`, `depends_on:`, `blocks:`

## Acceptance Criteria

- [x] No `plan.yaml` references remain
- [x] Magnitude table uses 8-slot scale with 1/2/3/5/8 maximums
- [x] Full frontmatter schema documented
- [x] Dependency graph, invalidation, Module Index gate, State Delta sections present
- [x] Folder examples show SP/PP prefixes and `_completed/` archive
- [x] Plan Types (SP/PP) documented with tiebreaker rule
