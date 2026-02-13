---
name: dream_v405_implementation
type: system
magnitude: Epic
status: WIP
origin: .agent_plan/day_dream/DREAM_v4.05.md
last_updated: 2026-02-13
start_at: 2026-02-12
knowledge_gaps: []
---

# SP01 — DREAM v4.05 Implementation

## Purpose

Bring the ADHD Framework ecosystem — skills, templates, agents, instructions, and tooling — into full alignment with DREAM v4.05. This is the first plan authored under v4.05's own format: a meta-implementation where the planning system deploys itself.

**Scope:** Update existing documentation artifacts, create the `dream_mcp` module skeleton, and implement all P0/P1/P2 commands. Phases p00–p02 align existing docs; p03 scaffolds the module; p04–p07 implement commands incrementally.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_executive_summary.md | Task | ✅ [DONE] | Vision, goals, non-goals, prior art, TL;DR |
| 02_architecture.md | Task | ✅ [DONE] | System diagrams, component relationships |
| 80_implementation.md | Task | ✅ [DONE] | Phased roadmap with verification |
| 81_module_structure.md | Task | ✅ [DONE] | Reusable vs project-specific module classification |
| p00_foundation/ | Plan | ✅ [DONE] | Rename `templates/` → `_templates/`, create PP summary template, update template schema |
| p01_skill_updates/ | Plan | ✅ [DONE] | Rewrite dream-planning, day-dream, writing-templates skills to v4.05 |
| p02_agent_instruction_updates/ | Plan | ✅ [DONE] | Fix 27+ stale path references across agents, flows, synced skills, docs |
| p03_dream_mcp_skeleton/ | Plan | ✅ [DONE] | Create `dream_mcp` module skeleton with command specs |
| p04_parsing_and_simple_commands/ | Plan | ⏳ [TODO] | Shared parsing infra + `dream tree` + `dream stale` |
| p05_status_and_validate/ | Plan | ⏳ [TODO] | `dream status` dashboard + `dream validate` engine |
| p06_advanced_workflows/ | Plan | ⏳ [TODO] | `dream impact`, `history`, `emergency`, `archive` |
| p07_intelligence_layer/ | Plan | ⏳ [TODO] | Hypothetical impact + proactive gap detection |
| modules/ | — | — | ADHD module specs (dream_mcp, instruction_core) |

<!-- Plan-scoped tracking, canonical index is at root -->
## Module Index

| Module | Origin Plan | Modified By | Spec File | Knowledge Gaps |
|--------|-------------|-------------|-----------|----------------|
| dream_mcp | SP01 | SP01 | `modules/dream_mcp.md` | — |
| instruction_core | (pre-existing) | SP01 | `modules/instruction_core.md` | Auto-sync behavior unverified |

## Integration Map

1. **p00** produces the `_templates/` directory and updated template files — these are referenced by skill content (p01) and path updates (p02).
2. **p01** produces updated skill files aligned with v4.05 conventions and `_templates/` paths.
3. **p02** produces corrected path references across compiled agents, flow sources, synced skills, and blueprint docs.
4. **p03** produces the `dream_mcp` module skeleton — stub signatures, no implementation.
5. **p04** produces shared parsing infrastructure + working `dream tree` and `dream stale` commands.
6. **p05** produces `dream status` dashboard + `dream validate` engine — completes P0.
7. **p06** produces P1 commands: `dream impact`, `dream history`, `dream emergency`, `dream archive`.
8. **p07** produces P2 intelligence layer: hypothetical impact analysis + proactive gap detection.

Phases p00–p02 = docs aligned. p03 = skeleton. p04–p05 = P0 complete. p06 = P1. p07 = P2.

## Reading Order

1. `01_executive_summary.md` — vision, goals, scope
2. `02_architecture.md` — system diagrams, component relationships
3. `80_implementation.md` — phased roadmap with verification
4. `81_module_structure.md` — module classification
5. `p00_foundation/` — prerequisite (blocks p01, p02)
6. `p03_dream_mcp_skeleton/` — independent, read anytime
7. `p01_skill_updates/` — after p00
8. `p02_agent_instruction_updates/` — after p00, parallel-safe with p01
9. `p04_parsing_and_simple_commands/` — after p03
10. `p05_status_and_validate/` — after p04
11. `p06_advanced_workflows/` — after p05
12. `p07_intelligence_layer/` — after p06


