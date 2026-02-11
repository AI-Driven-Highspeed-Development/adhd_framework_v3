---
project: "DREAM Upgrade"
current_phase: 2
phase_name: "DREAM Integration"
status: IN_PROGRESS
last_updated: "2026-02-11"
---

# 80 - Implementation Plan

> Part of [DREAM Upgrade Blueprint](./00_index.md)

<!--
⚠️  CODE EXAMPLES & FOLDER STRUCTURES WARNING ⚠️
════════════════════════════════════════════════════════════════════════════════
Examples in this document are ILLUSTRATIVE, not PRESCRIPTIVE.

• Folder structures show INTENT, actual paths may differ
• Task descriptions are GOALS, not step-by-step instructions

The implementation agent (HyperArch) will determine actual file locations
and implementation details based on current codebase state.
════════════════════════════════════════════════════════════════════════════════
-->

---

## 📊 Status Legend

| Icon | Status | Meaning |
|------|--------|---------|
| ⏳ | `[TODO]` | Not started |
| 🔄 | `[WIP]` | In progress |
| ✅ | `[DONE]` | Complete |
| 🚧 | `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 | `[CUT]` | Removed from scope |

---

## ⚙️ Phase 0: Fix Current Blueprint System

**Goal:** *"Fix the three biggest pain points in the current planning system: estimation, walking skeleton, and backward compat"*

**Duration:** ■□□□ Light (1 slot)

**Walking Skeleton:** NOT NEEDED — These are skill/template text edits, testable immediately by reading the output. No cross-boundary integration risk.

### Exit Gate

- [x] `day-dream` SKILL.md contains AI-agent time scale, conditional skeleton, and clean-code-first directive
- [x] Templates reference updated rules

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|---------|
| ✅ | Add AI-agent estimation defaults table | `day-dream/SKILL.md` | `[KNOWN]` | [03](./03_feature_fix_estimation.md) |
| ✅ | Add `human_only: true` flag semantics | `day-dream/SKILL.md` | `[KNOWN]` | [03](./03_feature_fix_estimation.md) |
| ✅ | Change walking skeleton to conditional with trigger criteria | `day-dream/SKILL.md` | `[KNOWN]` | [04](./04_feature_fix_walking_skeleton.md) |
| ✅ | Add clean-code-first directive section | `day-dream/SKILL.md` | `[KNOWN]` | [05](./05_feature_fix_backward_compat.md) |
| ✅ | Add folder-separation compat pattern | `day-dream/SKILL.md` | `[KNOWN]` | [05](./05_feature_fix_backward_compat.md) |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ✅ 5 tasks (at limit)
- ✅ All `[KNOWN]` difficulty

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Read `day-dream/SKILL.md` estimation section | Shows AI-agent time scale (minutes/hours), not human (days/weeks) |
| Search SKILL.md for "walking skeleton" | Described as conditional, with trigger criteria table |
| Search SKILL.md for "clean-code" or "backward compat" | Clean-code-first directive section exists with folder-separation pattern |

### P0 Completion Checklist

- [x] Exit gate checks pass
- [x] All tasks marked ✅
- [x] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [x] ≤5 tasks total
- [x] Manual verification steps pass

---

## 🛡️ Phase 1: Non-Vibe Code Practice

**Goal:** *"Embed the Non-Vibe Code engineering discipline into the implementation workflow and agent instructions"*

**Duration:** ■■□□ Standard (2 slots)

**Walking Skeleton:** NOT NEEDED — instruction/skill text edits, no cross-boundary risk.

### Exit Gate

- [x] `orch-implementation` skill contains Non-Vibe Code standards + POST-CHECK checklist
- [x] `agent_common_rules.instructions.md` contains universal directive
- [x] `day-dream` skill cross-references `orch-implementation` for full practice

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|--------|
| ✅ | Add Non-Vibe Code section to Arch's implementation standards | `orch-implementation/SKILL.md` | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |
| ✅ | Add Non-Vibe Code POST-CHECK checklist for San | `orch-implementation/SKILL.md` | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |
| ✅ | Add universal Non-Vibe Code directive | `agent_common_rules.instructions.md` | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |
| ✅ | Cross-ref Clean-Code-First → orch-implementation | `day-dream/SKILL.md` | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |
| ✅ | Document git checkpoint convention in implementation plans | `orch-implementation/SKILL.md` | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |
| ✅ | Fix wrong agent path references (`data/agents/` → `.github/agents/` / `data/flows/agents/`) | 8 `.flow` files, 2 `SKILL.md` files | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |
| ✅ | Create `non_vibe_code.instructions.md` (3 pillars, Unify or Justify, Batched Escalation) | `instruction_core/data/instructions/framework/` | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |
| ✅ | Add Non-Vibe Code references to agent flows (HyperArch Follow, HyperSan Validate, HyperIQGuard Enforce) | `@critical_rules` in 3 agent `.flow` files | `[KNOWN]` | [09](./09_feature_non_vibe_code.md) |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|----------------|
| Read orch-implementation Arch standards | Contains 3 pillars + Unify or Justify gate |
| Read orch-implementation POST-CHECK | Contains Non-Vibe Code checklist for San |
| Read agent_common_rules | Contains Non-Vibe Code universal directive |

### P1 Completion Checklist

- [x] Exit gate checks pass
- [x] All tasks marked ✅
- [x] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [x] 8 tasks total (exceeded 5-task soft limit — 3 ad-hoc follow-up tasks added post-completion for path fixes, instructions file, and agent flow references)
- [x] Manual verification steps pass
- [x] POST-CHECK: all 3 exit gates validated

---

## 🏗️ Phase 2: DREAM Integration

**Goal:** *"Create the dream-planning skill, update day-dream skill with cross-references, and refresh templates"*

⚡ GIT CHECKPOINT — commit before this phase (new skill creation + template updates)

**Duration:** ■■■□ Heavy (3 slots)

### Exit Gate

- [ ] `dream-planning` SKILL.md exists and passes Agent Skills format validation
- [ ] `day-dream` SKILL.md cross-references `dream-planning` for magnitude routing
- [ ] Templates align with updated skill rules

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|---------|
| ⏳ | Create `dream-planning` SKILL.md with full decomposition protocol | `.github/skills/dream-planning/SKILL.md` | `[EXPERIMENTAL]` | [06](./06_feature_dream_planning_skill.md) |
| ⏳ | Add magnitude routing cross-reference to day-dream skill | `day-dream/SKILL.md` | `[KNOWN]` | [07](./07_feature_update_day_dream_skill.md) |
| ⏳ | Update tier selection in day-dream to include magnitude | `day-dream/SKILL.md` | `[KNOWN]` | [07](./07_feature_update_day_dream_skill.md) |
| ⏳ | Update `00_index.template.md` planning standards | `templates/blueprint/00_index.template.md` | `[KNOWN]` | [08](./08_feature_template_refresh.md) |
| ⏳ | Update `80_implementation.template.md` durations + skeleton | `templates/blueprint/80_implementation.template.md` | `[KNOWN]` | [08](./08_feature_template_refresh.md) |
| ⏳ | Create `overview.template.md` for `_overview.md` convention | `templates/blueprint/overview.template.md` | `[KNOWN]` | [08](./08_feature_template_refresh.md) |
| ⏳ | Create `task.template.md` for leaf task files | `templates/blueprint/task.template.md` | `[KNOWN]` | [08](./08_feature_template_refresh.md) |
| ⏳ | Add scaffold headers + plan/task terminology to feature templates | `templates/blueprint/NN_feature*.template.md` | `[KNOWN]` | [08](./08_feature_template_refresh.md) |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Read `dream-planning/SKILL.md` | Contains magnitude table, decomposition protocol, sibling firewall rules |
| Read `day-dream/SKILL.md` tier selection | References `dream-planning` for magnitude routing |
| Read `80_implementation.template.md` P0 section | Shows AI-agent durations, walking skeleton as conditional |

### P2 Completion Checklist

- [ ] Exit gate checks pass
- [ ] All `[EXPERIMENTAL]` items validated or cut
- [ ] Manual verification steps pass
- [ ] `dream-planning` and `day-dream` skills don't duplicate rules

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-10 | No walking skeleton for this project | Skill/template text edits — no cross-boundary integration risk | HyperDream |
| 2026-02-10 | P0 = fixes only, P1 = DREAM integration | Fixes are simpler, immediately valuable, and P1 depends on them | HyperDream |
| 2026-02-10 | AI-agent time estimates used in this blueprint | Applying our own principle — this IS the standard we're establishing | HyperDream |
| 2026-02-10 | P0 completed — all 5 tasks done | All changes in source SKILL.md (406 lines, under 500 budget) | HyperArch |
| 2026-02-10 | L0-L4 **numbering** replaced with directory-based hierarchy | `_overview.md` convention at every plan directory provides hierarchical context without rigid level numbers | Discussion consensus |
| 2026-02-10 | node.yaml + contract.yaml merged | Single plan.yaml or inline frontmatter is sufficient | Discussion consensus |
| 2026-02-10 | Non-Vibe Code practice added as new P1 | Correctness-over-completion discipline with 3 pillars, current P1 becomes P2 | Discussion consensus |
| 2026-02-11 | Slot-based estimation replaces time-based | 4 actions/day baseline; Trivial=<<1, Light=1, Standard=2, Heavy=3, Epic=4+ must decompose. Complexity flag deferred to post-P0. | Discussion consensus |
| 2026-02-11 | P1 completed — all 5 tasks done | Non-Vibe Code embedded in orch-implementation, agent_common_rules, and day-dream | HyperAgentSmith |
| 2026-02-11 | Non-Vibe Code expanded: dedicated instructions.md + agent flow references + path fixes | 3 ad-hoc follow-up tasks: fixed stale `data/agents/` paths across 8 flows + 2 skills, created `non_vibe_code.instructions.md` with full practice spec, added `@critical_rules` references in HyperArch/HyperSan/HyperIQGuard flows | HyperAgentSmith |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| State machine tracking (execution.json) | 2026-02-10 | Overengineered; agents report via status markers |
| L0-L4 level **numbering** | 2026-02-10 | Directory-based hierarchy with `_overview.md` replaces rigid numbers; hierarchy preserved, numbering removed |
| DREAM_AGENT_CARD.md | 2026-02-10 | Skill file serves the same purpose |
| Migration tooling for existing blueprints | 2026-02-10 | Too few existing blueprints to justify tooling |

---

**← Back to:** [Index](./00_index.md)
