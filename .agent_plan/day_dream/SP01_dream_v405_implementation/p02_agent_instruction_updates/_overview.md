---
name: p02_agent_instruction_updates
type: system
magnitude: Light
status: DONE
origin: .agent_plan/day_dream/SP01_dream_v405_implementation/_overview.md
last_updated: 2026-02-13
---

# p02 — Agent & Instruction Updates

## Purpose

Fix all stale `templates/` → `_templates/` path references across compiled agents, flow source files, synced skill copies, and blueprint docs. Also update any DREAM convention references that changed in v4.05 (folder naming, plan type prefixes, etc.).

**Depends on:** p00_foundation (rename must be complete before references are valid).

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_update_flow_sources_and_agents.md | Task | ✅ [DONE] | Update .flow source files, recompile agents |
| 02_update_remaining_path_references.md | Task | ✅ [DONE] | Fix synced skills, blueprint docs, other stale refs |

## Acceptance Criteria

- [x] `grep -r "day_dream/templates/" .` returns zero matches outside `_archive/` and `DREAM_v4*.md`
- [x] Compiled agent files reflect updated paths
- [x] Flow source files compile cleanly after edits
- [x] Synced skill copies in `instruction_core/data/skills/` are updated

## Integration Map

Task 01 updates flow sources and recompiles agents (source of truth). Task 02 sweeps remaining stale references. Combined output: zero `templates/` references across the ecosystem.

## Reading Order

1. `01_update_flow_sources_and_agents.md` — update sources first, then recompile
2. `02_update_remaining_path_references.md` — sweep remaining references
