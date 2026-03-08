# Day Dream — Plans Overview

> Root navigator for all ADHD Framework planning artifacts.

---

## Current Sprint

| Plan | Phase | Status | Next Action |
|------|-------|--------|-------------|
| SP01_dream_v405_implementation | p03_dream_mcp_skeleton | ⏳ [TODO] | Scaffold `dream_mcp` module at `modules/dev/dream_mcp/` |
| SP01_dream_v405_implementation | p04_parsing_and_simple_commands | ⏳ [TODO] | Build shared parsing infra + `dream tree` + `dream stale` |
| SP01_dream_v405_implementation | p05_status_and_validate | ⏳ [TODO] | Implement `dream status` + `dream validate` (completes P0) |
| PP02_context_injection_restructure | p00_usage_audit | ⏳ [TODO] | Audit 17 instruction files, classify STAY/MIGRATE |
| PP03_dream_sop_skills | p00_skill_inventory_design | ⏳ [TODO] | Review existing dream skills + archived iterations, design dispatch table |
| PP04_dream_skills_consolidation | p00_canonical_asset_audit | ⏳ [TODO] | Audit all 9 dream-* skills for inline duplicated content |

## Plans

| Name | Type | Status | Priority | Description |
|------|------|--------|----------|-------------|
| [SP01_dream_v405_implementation/](./SP01_dream_v405_implementation/_overview.md) | System | 🔄 [WIP] | normal | Align ecosystem with DREAM v4.05 — skills, templates, agents, dream_mcp skeleton |
| [module-lifecycle/](./module-lifecycle/_overview.md) | Plan | ⏳ [TODO] | normal | Module remove & update commands for the ADHD CLI |
| [PP02_context_injection_restructure/](./PP02_context_injection_restructure/_overview.md) | Procedure | ⏳ [TODO] | normal | Restructure context injection files using 3-axis taxonomy (agent/instruction/skill) |
| [PP03_dream_sop_skills/](./PP03_dream_sop_skills/_overview.md) | Procedure | ⏳ [TODO] | normal | Transform DREAM into active dispatch system with routing skill + leaf SOPs |
| [PP04_dream_skills_consolidation/](./PP04_dream_skills_consolidation/_overview.md) | Procedure | ⏳ [TODO] | normal | Consolidate 9 dream-* skills: extract shared refs + merge create-pp/sp → dream-create |

## Module Index

| Module | Origin Plan | Modified By | Spec File | Knowledge Gaps |
|--------|-------------|-------------|-----------|----------------|
| dream_mcp | SP01 | SP01 | `SP01_dream_v405_implementation/modules/dream_mcp.md` | — |
| instruction_core | (pre-existing) | SP01 | `SP01_dream_v405_implementation/modules/instruction_core.md` | Auto-sync behavior unverified |

## State Deltas

### 🔄 SP01_dream_v405_implementation — Feb 2026

- `_templates/`: renamed from `templates/`, PP summary template created, frontmatter schemas updated to v4.05
- dream-planning SKILL.md: rewritten with 8-slot magnitude, full frontmatter schema, SP/PP types
- day-dream SKILL.md: rewritten with `_templates/` paths, dependency/invalidation/knowledge-gap rules, Module Index gate
- writing-templates SKILL.md: all path references updated to `_templates/`
- instruction_core: flow sources updated (`templates/` → `_templates/`), agents recompiled, synced skills refreshed
- ⏳ dream_mcp: skeleton not yet created (p03 pending)

## Legacy References

| Name | Purpose |
|------|---------|
| [DREAM_v3.md](./DREAM_v3.md) | DREAM v3 specification reference |

## Reading Order

1. **SP01_dream_v405_implementation/** — Active. Aligning ecosystem with DREAM v4.05.
2. **PP02_context_injection_restructure/** — Ready. Context injection files restructuring with 3-axis taxonomy.
3. **PP03_dream_sop_skills/** — Blocked on PP02. Transform DREAM into active dispatch with routing + leaf SOPs.
4. **PP04_dream_skills_consolidation/** — Ready. Consolidate dream-* skills: extract shared refs, merge create skills.
5. **module-lifecycle/** — Next. Module remove & update commands.
