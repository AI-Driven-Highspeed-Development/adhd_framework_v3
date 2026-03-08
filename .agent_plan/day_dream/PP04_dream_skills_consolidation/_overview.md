---
name: dream_skills_consolidation
type: procedure
magnitude: Standard
status: TODO
origin: discussion/dream_skills_consolidation_2026-03-02
last_updated: "2026-03-02"
depends_on:
  - PP03_dream_sop_skills
blocks: []
knowledge_gaps:
  - "Exact line counts of duplicated content across 9 skills not yet audited"
---

# PP04 — Dream Skills Consolidation

## Purpose

Eliminate ~350-450 lines of duplicated reference data across 9 dream-* skills by extracting shared definitions (status syntax, frontmatter schema, line limits) into canonical asset files with `→ See` pointers, and merging `dream-create-pp` + `dream-create-sp` into a single `dream-create` skill with SP/PP conditional branching. Result: 8 skills, zero inline duplication of reference data.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_summary.md | Task | ⏳ [TODO] | Merged summary: pain, 3 scale options, approach, success metrics |
| 80_implementation.md | Task | ⏳ [TODO] | Phased roadmap: audit → extract → merge → verify (Moderate scale) |

## Integration Map

```
01_summary.md ──► defines scope, 3 scale options, canonical owner map
                       │
80_implementation.md ◄─┘ implements Moderate scale in 4 phases
```

## Reading Order

1. **01_summary.md** — Understand pain, review 3 scale options, see chosen approach.
2. **80_implementation.md** — Phased roadmap for Moderate (consensus) scale option.
