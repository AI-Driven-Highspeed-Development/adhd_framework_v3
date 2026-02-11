---
project: "DREAM Upgrade"
current_phase: 2
phase_name: "DREAM Integration"
status: DONE
last_updated: "2026-02-11"
---

# Implementation Plan

> Part of [DREAM Upgrade](./_overview.md) · ✅ [DONE]

---

## ⚙️ Phase 0: Fix Current Blueprint System ✅

**Goal:** *"Fix the three biggest pain points: estimation, walking skeleton, backward compat"*

**Duration:** ■□□□ Light (1 slot)

**Walking Skeleton:** NOT NEEDED — Skill/template text edits, testable immediately.

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|---------|
| ✅ | Add AI-agent estimation defaults table | `day-dream/SKILL.md` | `[KNOWN]` | [fix-estimation](./p0-fix-blueprint-system/fix-estimation.md) |
| ✅ | Add `human_only: true` flag semantics | `day-dream/SKILL.md` | `[KNOWN]` | [fix-estimation](./p0-fix-blueprint-system/fix-estimation.md) |
| ✅ | Change walking skeleton to conditional with trigger criteria | `day-dream/SKILL.md` | `[KNOWN]` | [fix-walking-skeleton](./p0-fix-blueprint-system/fix-walking-skeleton.md) |
| ✅ | Add clean-code-first directive section | `day-dream/SKILL.md` | `[KNOWN]` | [fix-backward-compat](./p0-fix-blueprint-system/fix-backward-compat.md) |
| ✅ | Add folder-separation compat pattern | `day-dream/SKILL.md` | `[KNOWN]` | [fix-backward-compat](./p0-fix-blueprint-system/fix-backward-compat.md) |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Read `day-dream/SKILL.md` estimation section | Shows AI-agent time scale (minutes/hours) |
| Search SKILL.md for "walking skeleton" | Described as conditional, with trigger criteria table |
| Search SKILL.md for "clean-code" | Clean-code-first directive with folder-separation pattern |

---

## 🛡️ Phase 1: Non-Vibe Code Practice ✅

**Goal:** *"Embed the Non-Vibe Code engineering discipline into the implementation workflow"*

**Duration:** ■■□□ Standard (2 slots)

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|--------|
| ✅ | Add Non-Vibe Code section to Arch's implementation standards | `orch-implementation/SKILL.md` | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |
| ✅ | Add Non-Vibe Code POST-CHECK checklist for San | `orch-implementation/SKILL.md` | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |
| ✅ | Add universal Non-Vibe Code directive | `agent_common_rules.instructions.md` | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |
| ✅ | Cross-ref Clean-Code-First → orch-implementation | `day-dream/SKILL.md` | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |
| ✅ | Document git checkpoint convention | `orch-implementation/SKILL.md` | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |
| ✅ | Fix wrong agent path references | 8 `.flow` files, 2 `SKILL.md` files | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |
| ✅ | Create `non_vibe_code.instructions.md` | `instruction_core/data/instructions/framework/` | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |
| ✅ | Add Non-Vibe Code refs to agent flows | `@critical_rules` in 3 agent `.flow` files | `[KNOWN]` | [non-vibe-code](./p1-non-vibe-code.md) |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|----------------|
| Read orch-implementation Arch standards | Contains 3 pillars + Unify or Justify gate |
| Read orch-implementation POST-CHECK | Contains Non-Vibe Code checklist for San |
| Read agent_common_rules | Contains Non-Vibe Code universal directive |

---

## 🏗️ Phase 2: DREAM Integration ✅

**Goal:** *"Create the dream-planning skill, update day-dream skill, refresh templates"*

⚡ GIT CHECKPOINT — commit before this phase (new skill creation + template updates)

**Duration:** ■■■□ Heavy (3 slots)

### Tasks

| Status | Task | Target File | Difficulty | Feature |
|--------|------|-------------|------------|---------|
| ✅ | Create `dream-planning` SKILL.md | `.github/skills/dream-planning/SKILL.md` | `[EXPERIMENTAL]` | [dream-planning-skill](./p2-dream-integration/dream-planning-skill.md) |
| ✅ | Add magnitude routing cross-reference | `day-dream/SKILL.md` | `[KNOWN]` | [update-day-dream-skill](./p2-dream-integration/update-day-dream-skill.md) |
| ✅ | Update tier selection with magnitude | `day-dream/SKILL.md` | `[KNOWN]` | [update-day-dream-skill](./p2-dream-integration/update-day-dream-skill.md) |
| ✅ | Update `00_index.template.md` planning standards | Templates | `[KNOWN]` | [template-refresh](./p2-dream-integration/template-refresh.md) |
| ✅ | Update `80_implementation.template.md` durations + skeleton | Templates | `[KNOWN]` | [template-refresh](./p2-dream-integration/template-refresh.md) |
| ✅ | Create `overview.template.md` | Templates | `[KNOWN]` | [template-refresh](./p2-dream-integration/template-refresh.md) |
| ✅ | Create `task.template.md` | Templates | `[KNOWN]` | [template-refresh](./p2-dream-integration/template-refresh.md) |
| ✅ | Add scaffold headers + plan/task terminology | Feature templates | `[KNOWN]` | [template-refresh](./p2-dream-integration/template-refresh.md) |

---

## 📝 Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-10 | No walking skeleton for this project | Skill/template text edits — no cross-boundary risk |
| 2026-02-10 | P0 = fixes only, P1 = Non-Vibe Code, P2 = DREAM integration | Sequential dependencies |
| 2026-02-10 | L0-L4 numbering replaced with directory-based hierarchy | `_overview.md` convention provides context without rigid numbers |
| 2026-02-10 | node.yaml + contract.yaml merged | Single plan.yaml sufficient |
| 2026-02-11 | Slot-based estimation replaces time-based | 4 actions/day baseline |
| 2026-02-11 | P0, P1, P2 all completed | All tasks verified |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| State machine tracking (execution.json) | 2026-02-10 | Overengineered |
| L0-L4 level numbering | 2026-02-10 | Directory-based hierarchy replaces it |

---

**← Back to:** [DREAM Upgrade Overview](./_overview.md)
