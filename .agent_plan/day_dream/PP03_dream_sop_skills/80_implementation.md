---
project: "PP03 — Dream SOP Skills"
current_phase: 0
phase_name: "Skill Inventory & Design"
status: TODO
start_date: "2026-02-13"
last_updated: "2026-02-13"
---

# 80 — Implementation Plan

> Part of [PP03 — Dream SOP Skills](./_overview.md)

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

## ⚙️ Phase 0: Skill Inventory & Design

**Goal:** *"Review existing dream skills, mine archived iterations for pain patterns, and produce the dream-routing dispatch table with finalized leaf skill list."*

**Duration:** ■■■□□□□□ Standard (max 3 slots)

### Exit Gate

- [ ] Dispatch table document exists mapping user intents → leaf skill names
- [ ] Leaf skill list finalized with scope descriptions for each
- [ ] Archived iteration review summary produced (pain patterns + lessons learned)

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Inventory existing dream skills: `day-dream`, `dream-planning`, `writing-templates` — extract what each covers and what's missing | `.github/skills/` | `[KNOWN]` |
| ⏳ | Review archived iterations at `_archive/dream_iterations/` (12 files, v3→v4.04) — extract recurring pain points and failed patterns | `_archive/` | `[KNOWN]` |
| ⏳ | Design intent classification table: map user requests → DREAM operations (create-PP, create-SP, update, close, fix, validate, etc.) | `PP03` | `[KNOWN]` |
| ⏳ | Finalize leaf skill list with scope boundary for each skill — what it covers, what it doesn't | `PP03` | `[KNOWN]` |
| ⏳ | Document template relocation plan: current `_templates/` structure → `dream-routing/references/` mapping | `_templates/` | `[KNOWN]` |

### Preliminary Dispatch Table (Hypothesis — P0 validates)

| User Intent | Route To | Example Trigger |
|-------------|----------|-----------------|
| Create a new PP blueprint | `dream-create-PP` | "Create a PP for X" |
| Create a new SP blueprint | `dream-create-SP` | "Create an SP for X" |
| Update/resurrect an existing plan | `dream-update` | "Update PP02", "Resurrect plan X" |
| Close/complete a plan | `dream-close` | "Close SP01", "Mark plan done" |
| Fix a plan (validation errors) | `dream-fix` | "Fix the frontmatter in PP02" |
| Validate plan structure | `dream-validate` | "Validate all plans", "Check PP03" |
| Discuss/explore (no artifact) | `day-dream` (existing) | "Let's discuss feature X" |
| Decompose work into plan tree | `dream-planning` (existing) | "Break this into subtasks" |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ❌ Max 5 tasks (currently 5)
- ❌ Must fit within slot budget (≤2 slots)
- ❌ **No skills are created in P0** — design only

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Read dispatch table document | Every common DREAM operation has a named target skill |
| Cross-check leaf list against archived iteration pain points | Pain points are addressed by at least one leaf skill |
| Verify no leaf skill scope overlaps another | Each skill has clear, non-overlapping boundary |

### P0 Completion Checklist

- [ ] Exit gate met — dispatch table + leaf list finalized
- [ ] Archived iteration review complete (12 files scanned)
- [ ] No skill files created (design only)
- [ ] Template relocation plan documented
- [ ] Manual verification steps pass

---

## 🏗️ Phase 1: dream-routing Skill

**Goal:** *"Create the dream-routing skill with references/ subfolder containing all templates, and implement intent classification dispatch logic."*

**Duration:** ■■■□□□□□ Standard (max 3 slots)

### Exit Gate

- [ ] `dream-routing/SKILL.md` exists with complete intent→skill dispatch table
- [ ] `dream-routing/references/` contains all templates (moved from `_templates/`)
- [ ] `_templates/` replaced with redirect notice pointing to new location
- [ ] `adhd r -f` syncs dream-routing skill to `.github/skills/` without errors

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Create `instruction_core/data/skills/dream-routing/SKILL.md` with intent classification table and dispatch rules from P0 output | `instruction_core` | `[KNOWN]` |
| ⏳ | Create `instruction_core/data/skills/dream-routing/references/` and copy all template files from `_templates/` (preserving directory structure) | `instruction_core` | `[KNOWN]` |
| ⏳ | Replace `_templates/` contents with a single `README.md` redirect: "Templates have moved to `dream-routing/references/`" | `_templates/` | `[KNOWN]` |
| ⏳ | Run `adhd r -f` — verify dream-routing skill syncs to `.github/skills/dream-routing/` with `references/` intact | `instruction_core` | `[KNOWN]` |
| ⏳ | Update `writing-templates` SKILL.md — change template path references from `_templates/` to `dream-routing/references/` | `instruction_core` | `[KNOWN]` |

### Target Folder Structure (P1)

```
instruction_core/data/skills/
├── dream-routing/                      (NEW)
│   ├── SKILL.md                        (dispatch table + intent rules)
│   └── references/                     (templates relocated from _templates/)
│       ├── simple.template.md
│       ├── blueprint/
│       │   ├── overview.template.md
│       │   ├── 01_summary.template.md
│       │   ├── 80_implementation.template.md
│       │   └── ...
│       ├── assets/
│       └── examples/

.agent_plan/day_dream/
├── _templates/                         (GUTTED — redirect notice only)
│   └── README.md                       ("Templates moved to dream-routing/references/")
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `cat .github/skills/dream-routing/SKILL.md` | Dispatch table with intent→skill mapping |
| `ls .github/skills/dream-routing/references/blueprint/` | Template files present |
| `cat .agent_plan/day_dream/_templates/README.md` | Redirect notice to new location |
| `adhd r -f` | Clean compilation, no errors |

### P1 Completion Checklist

- [ ] Exit gate met — routing skill exists with references/
- [ ] All templates relocated (no orphaned templates in old location)
- [ ] Redirect notice in `_templates/`
- [ ] `writing-templates` updated with new paths
- [ ] Manual verification steps pass

---

## 🔧 Phase 2: Core Leaf Skills

**Goal:** *"Create the four most critical leaf skills — each a self-contained SOP that works without reading any sibling skill."*

**Duration:** ■■■■■□□□ Heavy (max 5 slots)

### Exit Gate

- [ ] `dream-create-PP/SKILL.md` exists — complete SOP for PP blueprint creation
- [ ] `dream-create-SP/SKILL.md` exists — complete SOP for SP blueprint creation
- [ ] `dream-update/SKILL.md` exists — complete SOP for plan updates/resurrection
- [ ] `dream-close/SKILL.md` exists — complete SOP for plan closure
- [ ] Each skill is self-contained — an agent reading ONLY that skill can complete the operation

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Author `dream-create-PP/SKILL.md`: step-by-step SOP for creating a PP blueprint — frontmatter, 01_summary, 80_implementation, _overview, root _overview update | `instruction_core` | `[KNOWN]` |
| ⏳ | Author `dream-create-SP/SKILL.md`: step-by-step SOP for creating an SP blueprint — separate exec summary + architecture, feature files, _overview | `instruction_core` | `[KNOWN]` |
| ⏳ | Author `dream-update/SKILL.md`: SOP for updating plans (status changes, resurrecting CUT/archived plans, adding phases, modifying scope) | `instruction_core` | `[KNOWN]` |
| ⏳ | Author `dream-close/SKILL.md`: SOP for plan closure gates — exit criteria verification, status rollup, State Deltas update, root _overview cleanup | `instruction_core` | `[KNOWN]` |
| ⏳ | Self-containment test: for each skill, verify an agent with ONLY that skill loaded can complete the operation without referencing siblings | verification | `[KNOWN]` |

### Leaf Skill Content Requirements

Each leaf skill MUST include (self-contained):

```
1. When to Use           — exact trigger conditions
2. Prerequisites         — what must exist before starting
3. Step-by-Step SOP      — numbered steps with file paths, templates, field values
4. Frontmatter Schema    — exact YAML fields required (copied, not referenced)
5. Validation Checklist  — exit criteria for the operation
6. Common Mistakes       — top 3 errors and how to avoid them
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Read `dream-create-PP/SKILL.md` alone — follow steps to create a dummy PP | Complete, valid PP blueprint produced |
| Read `dream-close/SKILL.md` alone — follow steps on an existing plan | Plan correctly closed with status rollup |
| Grep any leaf skill for "see dream-routing" or "see dream-create-SP" | Zero cross-references to sibling skills |

### P2 Completion Checklist

- [ ] Exit gate met — all 4 leaf skills exist
- [ ] Each skill is self-contained (no sibling references)
- [ ] Each skill follows Leaf Skill Content Requirements
- [ ] `adhd r -f` syncs all skills without errors
- [ ] Manual verification steps pass

---

## 📡 Phase 3: Extended Leaf Skills & Integration

**Goal:** *"Create remaining leaf skills, update existing skills to reference the routing system, and verify the full dispatch chain works end-to-end."*

**Duration:** ■■■□□□□□ Standard (max 3 slots)

### Exit Gate

- [ ] Extended leaf skills created: `dream-fix`, `dream-validate` (+ any others from P0 list)
- [ ] `day-dream` SKILL.md updated — references dream-routing for operations, retains format spec role
- [ ] `dream-planning` SKILL.md updated — references dream-routing for dispatch
- [ ] End-to-end test: user intent → dream-routing → leaf skill → correct artifact produced

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Author `dream-fix/SKILL.md`: SOP for fixing validation errors (frontmatter, status syntax, missing sections, line limit violations) | `instruction_core` | `[KNOWN]` |
| ⏳ | Author `dream-validate/SKILL.md`: SOP for validating plan structure (can delegate to `dream validate` MCP command when available) | `instruction_core` | `[EXPERIMENTAL]` |
| ⏳ | Update `day-dream/SKILL.md`: add "For step-by-step operations, see dream-routing" section, clarify its role as format reference only | `instruction_core` | `[KNOWN]` |
| ⏳ | Update `dream-planning/SKILL.md`: add routing reference, clarify its role as decomposition protocol only | `instruction_core` | `[KNOWN]` |
| ⏳ | End-to-end verification: test 3 user intents through dream-routing → leaf skill → artifact | verification | `[KNOWN]` |

### Integration Changes to Existing Skills

```
day-dream SKILL.md:
  ADD section: "## Operations Dispatch"
  CONTENT: "For step-by-step DREAM operations, use the dream-routing skill.
            This skill (day-dream) is the format reference only."

dream-planning SKILL.md:
  ADD section: "## Operations Dispatch"  
  CONTENT: "For creating/updating/closing plans, use dream-routing.
            This skill covers decomposition protocol only."

writing-templates SKILL.md:
  UPDATE: All _templates/ paths → dream-routing/references/
  (Already started in P1; P3 verifies completeness)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| "Create a PP for feature X" → check dream-routing dispatches to dream-create-PP | Correct leaf skill selected |
| "Fix the frontmatter in PP02" → check dream-routing dispatches to dream-fix | Correct leaf skill selected |
| Read updated day-dream SKILL.md | Clear that operations go through dream-routing |
| `adhd r -f` | Clean compilation, all skills synced |

### P3 Completion Checklist

- [ ] Exit gate met — extended skills created, existing skills updated
- [ ] All `[EXPERIMENTAL]` items validated or cut
- [ ] Full dispatch chain verified (3 intents tested)
- [ ] `adhd r -f` compiles cleanly
- [ ] Manual verification steps pass

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-13 | Templates relocate to `dream-routing/references/` not duplicated | Single source of truth; skills can have subfolders | Discussion consensus |
| 2026-02-13 | Leaf skills must be fully self-contained | Reduces context window; prevents agents needing to read 3+ skills | Discussion consensus |
| 2026-02-13 | Follow orch-routing → orch-implementation pattern | Proven layered dispatch already working in framework | Discussion consensus |
| 2026-02-13 | Review archived iterations in P0 only | Learn from past pain; don't carry forward structure | Discussion consensus |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| — | — | (none yet) |

---

**← Back to:** [_overview.md](./_overview.md)
