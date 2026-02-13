---
module: instruction_core
last_updated: 2026-02-12
modified_by_plans:
  - SP01_dream_v405_implementation
knowledge_gaps:
  - "Confirm whether instruction_core refresh auto-syncs .github/skills/ → data/skills/"
---

# Module Spec — instruction_core

## Current State

Existing module at `modules/dev/instruction_core/`. Manages skill syncing, agent compilation, and instruction delivery.

**Files affected by SP01:**
- `data/flows/agents/hyper_agent_smith.flow` — 2 stale `templates/` refs
- `data/flows/agents/hyper_day_dreamer.flow` — 2 stale `templates/` refs
- `data/compiled/agents/hyper_agent_smith.adhd.agent.md` — 2 stale refs (derived)
- `data/compiled/agents/hyper_day_dreamer.adhd.agent.md` — 2 stale refs (derived)
- `data/skills/writing-templates/SKILL.md` — 5 stale refs (synced copy)
- `data/skills/day-dream/SKILL.md` — 1 stale ref (synced copy)
- `data/skills/orch-routing/SKILL.md` — 1 stale ref (synced copy)

**Total:** 15 stale path references across 7 data files.

## Target State

All `templates/` references updated to `_templates/` in flow source files. Compiled agents regenerated. Synced skills current (via refresh or manual update).

**No module code changes** — only data files within the module are modified.

## Modified By This Plan

- Phase: p02_agent_instruction_updates
  - Task: `01_feat_update_flow_sources_and_agents.md` (flows + recompile)
  - Task: `02_feat_update_remaining_path_references.md` (synced skills)
