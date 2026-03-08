---
project: "PP04 — Dream Skills Consolidation"
current_phase: 0
phase_name: "Canonical Asset Audit & Assignment"
status: TODO
start_date: "2026-03-02"
last_updated: "2026-03-02"
---

# 80 — Implementation Plan

> Part of [PP04 — Dream Skills Consolidation](./_overview.md)

<!--
This plan implements the MODERATE scale option (consensus recommendation).
- Conservative differs: skip P2 (no merge), end after P1 with 9 skills.
- Aggressive differs: add P2b (merge fix+validate → dream-check) and
  P2c (merge update+close → dream-lifecycle), resulting in 6 skills.
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

## ⚙️ Phase 0: Canonical Asset Audit & Assignment

**Goal:** *"Audit all 9 dream-* skills for inline duplicated content and map each block to its canonical owner asset file."*

**Duration:** ■□□□□□□□ Trivial (1 slot)

### Exit Gate

- [ ] Duplication audit matrix exists: skill × data-block → inline/pointer/absent
- [ ] Each duplicated block assigned to a canonical owner with asset file path
- [ ] Any missing canonical asset files identified (expected: ≤1 new file)

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Grep all 9 dream-* SKILL.md files for inline status syntax, frontmatter schema, line limits, difficulty labels, and phase rules | `instruction_core/data/skills/dream-*/` | `[KNOWN]` |
| ⏳ | Build duplication matrix: rows = data blocks, columns = skills, cells = inline/pointer/absent | `PP04` | `[KNOWN]` |
| ⏳ | Verify canonical assets exist in `dream-planning/assets/` (status-syntax.md, overview-frontmatter-schema.md) and `dream-vision/assets/` (document-line-limits.md, story-spec-pattern.md) | `dream-planning/`, `dream-vision/` | `[KNOWN]` |
| ⏳ | Identify missing canonical assets (e.g., difficulty-labels.md) — create if needed | `dream-planning/assets/` | `[KNOWN]` |
| ⏳ | Produce canonical owner assignment table for P1 consumption | `PP04` | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Read duplication matrix | Every shared data block has exactly 1 canonical owner assigned |
| `ls dream-planning/assets/` | status-syntax.md, overview-frontmatter-schema.md present |
| `ls dream-vision/assets/` | document-line-limits.md, story-spec-pattern.md present |

### P0 Completion Checklist

- [ ] Exit gate met — duplication matrix and owner assignment complete
- [ ] All canonical assets verified or created
- [ ] No skill SKILL.md files modified (audit only)
- [ ] Manual verification steps pass

---

## 🏗️ Phase 1: Extract & Replace

**Goal:** *"Replace inline duplicated content in all SOP skills with `→ See` pointers to canonical asset files."*

**Duration:** ■■□□□□□□ Light (2 slots)

### Exit Gate

- [ ] All 6 SOP skills (create-pp, create-sp, update, close, fix, validate) use `→ See` pointers for shared data
- [ ] Zero inline copies of status syntax, frontmatter schema, line limits, or difficulty labels remain
- [ ] `adhd r -f` compiles clean
- [ ] Each modified skill still reads as a complete, coherent SOP

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Replace inline status syntax blocks with `→ See dream-planning/assets/status-syntax.md` in all SOP skills | `dream-*/SKILL.md` | `[KNOWN]` |
| ⏳ | Replace inline frontmatter schema with `→ See dream-planning/assets/overview-frontmatter-schema.md` in all SOP skills | `dream-*/SKILL.md` | `[KNOWN]` |
| ⏳ | Replace inline line limits with `→ See dream-vision/assets/document-line-limits.md` in all SOP skills | `dream-*/SKILL.md` | `[KNOWN]` |
| ⏳ | Replace inline difficulty labels and phase rules with appropriate `→ See` pointers | `dream-*/SKILL.md` | `[KNOWN]` |
| ✅ | Broaden `module-dev/SKILL.md` print() warning from MCP-only to all-modules | `module-dev/SKILL.md` | `[KNOWN]` |
| ⏳ | Run `adhd r -f` and verify all skills sync correctly to `.github/skills/` | all skills | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `grep -r "⏳.*TODO.*WIP.*DONE" dream-*/SKILL.md` | Zero matches (inline syntax blocks removed) |
| Read any SOP skill end-to-end | `→ See` pointers are clear; skill reads as complete SOP |
| `adhd r -f` | Clean compilation, no errors |

### P1 Completion Checklist

- [ ] Exit gate met — all inline copies replaced with pointers
- [ ] Each skill still self-contained as an SOP (pointers supplement, not fragment)
- [ ] `adhd r -f` compiles clean
- [ ] Manual verification steps pass

---

## 🔧 Phase 2: Merge create-pp + create-sp → dream-create

**Goal:** *"Combine the two near-identical create skills into a single `dream-create` skill with SP/PP conditional branching."*

**Duration:** ■■□□□□□□ Light (2 slots)

### Exit Gate

- [ ] `dream-create/SKILL.md` exists with SP/PP conditional branching
- [ ] `dream-create-pp/` and `dream-create-sp/` folders deleted
- [ ] `dream-routing/SKILL.md` dispatch table updated to route to `dream-create`
- [ ] `adhd r -f` compiles clean

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Create `dream-create/SKILL.md` — merge shared structure from create-pp and create-sp, add `### If PP:` / `### If SP:` conditional sections for divergent steps | `instruction_core/data/skills/dream-create/` | `[KNOWN]` |
| ⏳ | Delete `dream-create-pp/` and `dream-create-sp/` skill folders | `instruction_core/data/skills/` | `[KNOWN]` |
| ⏳ | Update `dream-routing/SKILL.md` dispatch table: replace `dream-create-pp` and `dream-create-sp` entries with single `dream-create` entry | `dream-routing/SKILL.md` | `[KNOWN]` |
| ⏳ | Run `adhd r -f` — verify dream-create syncs, old skills removed from `.github/skills/` | all skills | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `ls instruction_core/data/skills/dream-create*/` | Only `dream-create/` exists |
| Read `dream-create/SKILL.md` — follow PP path | Produces valid PP blueprint |
| Read `dream-create/SKILL.md` — follow SP path | Produces valid SP blueprint |
| `grep "dream-create-pp\|dream-create-sp" dream-routing/SKILL.md` | Zero matches |

### P2 Completion Checklist

- [ ] Exit gate met — dream-create exists, old skills removed
- [ ] Dispatch table updated
- [ ] `adhd r -f` compiles clean
- [ ] Manual verification steps pass

---

## 📡 Phase 3: Verification & Cleanup

**Goal:** *"End-to-end verification of the consolidated skill system and cleanup of stale references."*

**Duration:** ■□□□□□□□ Trivial (1 slot)

### Exit Gate

- [ ] End-to-end test: dream-routing → dream-create → valid artifact for both PP and SP
- [ ] Zero broken `→ See` links across all dream-* skills
- [ ] No stale references to `dream-create-pp` or `dream-create-sp` anywhere in the repository

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | End-to-end routing test: simulate PP creation request through dream-routing → dream-create | `dream-routing/`, `dream-create/` | `[KNOWN]` |
| ⏳ | Grep entire repo for stale references to `dream-create-pp`, `dream-create-sp` — fix any hits | repo-wide | `[KNOWN]` |
| ⏳ | Verify all `→ See` pointers resolve to existing asset files | `dream-*/SKILL.md` | `[KNOWN]` |
| ⏳ | Update PP03 state deltas if needed (PP03 created the skills being modified) | `.agent_plan/day_dream/` | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `grep -r "dream-create-pp\|dream-create-sp" .github/ modules/ .agent_plan/` | Zero matches (except archives) |
| Follow `→ See` link from any skill | Asset file exists and contains expected content |
| `adhd r -f` | Clean compilation |

### P3 Completion Checklist

- [ ] Exit gate met — end-to-end verified, zero stale refs
- [ ] All `→ See` links valid
- [ ] PP04 State Deltas documented
- [ ] Manual verification steps pass

---

**← Back to:** [_overview.md](./_overview.md)
