# 07 - Feature: Update Day-Dream Skill

> Part of [DREAM Upgrade Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  day-dream skill has:          │  day-dream skill has:          │
│  • Human-time estimates        │  • AI-agent time defaults      │
│  • Mandatory walking skeleton  │  • Conditional skeleton        │
│  • No compat directive         │  • Clean-code-first directive  │
│  • No magnitude awareness      │  • References dream-planning   │
│       ↓                        │       ↓                        │
│  💥 Agents follow wrong rules  │  ✅ Agents get correct rules   │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Apply all P0 fixes to the existing `day-dream` skill and add cross-references to the new `dream-planning` skill for magnitude-gated tier selection.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Estimation defaults | ❌ Human days/weeks | ✅ AI-agent hours/minutes |
| Walking skeleton | ❌ Always mandatory | ✅ Conditional with trigger criteria |
| Backward compat | ❌ Not addressed | ✅ Clean-code-first directive |
| Tier selection | ❌ Feature count only | ✅ Magnitude-aware + feature count |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Update the existing `day-dream` SKILL.md with all P0 fixes and P1 cross-references to create a unified, correct authoring guide.

**Priority:** P1  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Update estimation tables with AI-agent time scale (from feature 03)
- Update walking skeleton policy to conditional (from feature 04)
- Add clean-code-first and folder-separation compat directive (from feature 05)
- Add `dream-planning` skill cross-reference for magnitude routing
- Update tier selection to include magnitude-gated criteria
- Ensure all existing valid rules remain unchanged

**Out of Scope:**
- Rewriting the skill from scratch
- Moving authoring rules to `dream-planning` (they stay here)
- Template changes (that's feature 08)

---

## ✅ Acceptance Criteria

- [ ] All estimation references use AI-agent time scale
- [ ] Walking skeleton section documents conditionality with trigger table
- [ ] Clean-code-first directive added as a named section
- [ ] Tier selection table includes magnitude routing (references `dream-planning`)
- [ ] `human_only: true` flag documented
- [ ] Existing valid rules (Story/Spec pattern, status syntax, line limits) unchanged

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Feature 03 (estimation) | internal | Pending | Provides time scale changes |
| Feature 04 (walking skeleton) | internal | Pending | Provides conditionality rules |
| Feature 05 (backward compat) | internal | Pending | Provides directive text |
| Feature 06 (dream-planning skill) | internal | Pending | Must exist before cross-referencing |

---

## 🚀 Phase 1 Tasks

| Task | Difficulty | Owner | Status |
|------|------------|-------|--------|
| Update tier selection with magnitude awareness | `[KNOWN]` | TBD | ⏳ [TODO] |
| Apply estimation fixes from feature 03 | `[KNOWN]` | TBD | ⏳ [TODO] |
| Apply walking skeleton fixes from feature 04 | `[KNOWN]` | TBD | ⏳ [TODO] |
| Add clean-code-first directive from feature 05 | `[KNOWN]` | TBD | ⏳ [TODO] |
| Add `dream-planning` skill cross-reference | `[KNOWN]` | TBD | ⏳ [TODO] |

---

## [Custom] 📝 Sections to Modify in SKILL.md

| Existing Section | Change | Source |
|-----------------|--------|--------|
| Tier Selection | Add magnitude-gated routing reference | Feature 06 |
| Templates Location | Update duration defaults in template descriptions | Feature 03 |
| Anti-Patterns | Add "inline compat" and "forced skeleton" entries | Features 04, 05 |
| (new) Estimation Defaults | Add AI-agent time scale table | Feature 03 |
| (new) Walking Skeleton Policy | Add conditional trigger criteria | Feature 04 |
| (new) Clean-Code-First | Add directive + folder-separation pattern | Feature 05 |
| (new) Related Skills | Add `dream-planning` cross-reference | Feature 06 |

---

## ✅ Simple Feature Validation Checklist

### Narrative
- [ ] **The Story** clearly states user problem and value
- [ ] **Intent** is unambiguous to a non-technical reader

### Technical
- [ ] **Scope** is explicitly bounded (In/Out of Scope filled)
- [ ] **Acceptance Criteria** are testable (not vague)
- [ ] **Dependencies** are listed with status

### Linkage
- [ ] Feature linked from `01_executive_summary.md`

---

**Prev:** [DREAM Planning Skill](./06_feature_dream_planning_skill.md) | **Next:** [Template Refresh](./08_feature_template_refresh.md)

---

**← Back to:** [Index](./00_index.md)
