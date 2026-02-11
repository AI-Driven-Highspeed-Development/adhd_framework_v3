# 08 - Feature: Template Refresh

> Part of [DREAM Upgrade Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  Templates say:                │  Templates say:                │
│  "P0: 3-5 days (HARD LIMIT)"   │  "P0: 2-4 hours (AI-agent)"    │
│  "Walking Skeleton First"      │  "Walking Skeleton (optional)" │
│  No plan/task terminology      │  plan/task terminology used    │
│       ↓                        │       ↓                        │
│  💥 Templates contradict skill │  ✅ Templates match skill      │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Update all blueprint templates to align with the fixed skill rules: AI-agent time, conditional skeleton, plan/task terminology, and a comment reminding that templates are scaffolds, not protocol.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Duration defaults | ❌ Human-scale in templates | ✅ AI-agent-scale |
| Walking skeleton | ❌ Presented as mandatory | ✅ Presented as conditional |
| Terminology | ❌ Mixed/absent | ✅ plan/task used consistently |
| Authority | ❌ Templates contain rules | ✅ Templates reference skills |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Refresh all blueprint templates so they align with the updated `day-dream` skill and reference the `dream-planning` skill. Templates are passive scaffolds — they render structure, they don't define protocol.

**Priority:** P1  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Create `overview.template.md` — template for mandatory `_overview.md` files in plan directories
- Create `task.template.md` — template for leaf task files
- Update `00_index.template.md` — planning standards table, duration references
- Update `80_implementation.template.md` — P0 duration, walking skeleton conditionality
- Update `NN_feature.template.md` and `NN_feature_simple.template.md` — terminology alignment
- Add comment header to all templates: "This template is a scaffold. Protocol rules live in skills."
- Ensure plan/task terminology is used where "node" was implied

**Out of Scope:**
- Creating new template types beyond `overview.template.md` and `task.template.md`
- Changing template section structure (Story/Spec pattern stays)
- Updating the simple.template.md (Single-file tier, separate concern)
- Moving templates to a different location

---

## ✅ Acceptance Criteria

- [ ] `00_index.template.md` planning standards table says "Conditional Walking Skeleton"
- [ ] `80_implementation.template.md` uses AI-agent durations in phase defaults
- [ ] `80_implementation.template.md` walking skeleton section marked as conditional
- [ ] All templates include scaffold-not-authority comment
- [ ] `overview.template.md` exists with Purpose, Children table, Integration Map, Reading Order sections
- [ ] `task.template.md` exists as scaffold for leaf task files
- [ ] No template uses "node" terminology — replaced with plan/task where applicable
- [ ] Templates still compile correctly when used by HyperDream

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Feature 07 (day-dream skill update) | internal | Pending | Skill must be updated before templates match |
| Feature 06 (dream-planning skill) | internal | Pending | Templates reference this skill |

---

## 🚀 Phase 1 Tasks

| Task | Difficulty | Owner | Status |
|------|------------|-------|--------|
| Update `00_index.template.md` planning standards | `[KNOWN]` | TBD | ⏳ [TODO] |
| Update `80_implementation.template.md` durations + skeleton | `[KNOWN]` | TBD | ⏳ [TODO] |
| Update feature templates with plan/task terminology | `[KNOWN]` | TBD | ⏳ [TODO] |
| Create `overview.template.md` for `_overview.md` files | `[KNOWN]` | TBD | ⏳ [TODO] |
| Create `task.template.md` for leaf task files | `[KNOWN]` | TBD | ⏳ [TODO] |
| Add scaffold comment headers to all templates | `[KNOWN]` | TBD | ⏳ [TODO] |

---

## [Custom] 📋 Templates to Touch

| Template | Changes | Priority |
|----------|---------|----------|
| `00_index.template.md` | Planning standards table, duration references | Medium |
| `01_executive_summary.template.md` | Minimal — terminology only | Low |
| `02_architecture.template.md` | Minimal — no protocol content | Low |
| `80_implementation.template.md` | Durations, skeleton conditionality, scaffold header | High |
| `81_module_structure.template.md` | Scaffold header only | Low |
| `NN_feature.template.md` | Terminology, scaffold header | Medium |
| `NN_feature_simple.template.md` | Terminology, scaffold header | Medium |
| `overview.template.md` | **NEW** — template for mandatory `_overview.md` at plan directories | High |
| `task.template.md` | **NEW** — template for leaf task files | Medium |

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

**Prev:** [Update Day-Dream Skill](./07_feature_update_day_dream_skill.md) | **Next:** [Implementation](./80_implementation.md)

---

**← Back to:** [Index](./00_index.md)
