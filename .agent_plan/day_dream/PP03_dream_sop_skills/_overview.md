---
name: dream_sop_skills
type: procedure
magnitude: Heavy
status: TODO
origin: discussion/dream_routing_sop_skills
last_updated: 2026-02-13
depends_on: [PP02_context_injection_restructure]
blocks: []
knowledge_gaps:
  - "Full leaf skill list not finalized — P0 reviews archived iterations to inform"
  - "Template relocation UX impact — moving from _templates/ to dream-routing/references/"
---

# PP03 — Dream SOP Skills

## Purpose

Transform DREAM from a static format spec into an active dispatch system by creating a `dream-routing` skill with `references/` subfolder (absorbing current `_templates/`), plus self-contained leaf skills (`dream-create-PP`, `dream-create-SP`, `dream-update`, `dream-close`, etc.) — each a complete SOP for a specific DREAM operation. Follows the same layered calling pattern as `orch-routing → orch-implementation`.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_summary.md | Task | ⏳ [TODO] | Merged exec summary + architecture: pain, vision, taxonomy, approach |
| 80_implementation.md | Task | ⏳ [TODO] | Phased roadmap: inventory → routing skill → core leaf skills → extended skills |
| p00_skill_inventory_design/ | Plan | ⏳ [TODO] | Review existing skills + archived iterations, design dispatch table + leaf list |
| p01_dream_routing/ | Plan | ⏳ [TODO] | Create dream-routing skill, move templates to references/, implement dispatch |
| p02_core_leaf_skills/ | Plan | ⏳ [TODO] | Create dream-create-PP, dream-create-SP, dream-update, dream-close |
| p03_extended_skills_integration/ | Plan | ⏳ [TODO] | Create remaining leaf skills, update existing skills, verify integration |

## Integration Map

```
p00_skill_inventory_design/ ──► dispatch table + leaf skill list
                                    │
p01_dream_routing/ ◄────────────────┘ (uses dispatch table)
        │
        ├──► dream-routing skill with references/
        │
p02_core_leaf_skills/ ◄────────────┘ (routing dispatches to these)
        │
        ├──► dream-create-PP, dream-create-SP, dream-update, dream-close
        │
p03_extended_skills_integration/ ◄─┘ (completes the skill set)
        │
        └──► full DREAM dispatch system, existing skills updated
```

## Reading Order

1. **01_summary.md** — Start here. Understand pain, vision, and approach.
2. **80_implementation.md** — Phased roadmap with tasks and verification.
3. **p00_skill_inventory_design/** — First phase: audit + design (strict prereq).
4. **p01_dream_routing/** — Depends on P0 dispatch table output.
5. **p02_core_leaf_skills/** — Depends on P1 routing skill existing.
6. **p03_extended_skills_integration/** — Depends on P2 completion.
