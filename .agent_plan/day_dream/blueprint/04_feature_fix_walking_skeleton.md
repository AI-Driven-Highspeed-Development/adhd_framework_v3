# 04 - Feature: Fix Walking Skeleton Policy

> Part of [DREAM Upgrade Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  Every blueprint MUST have     │  Walking skeleton only when    │
│  a walking skeleton phase      │  cross-boundary risk is high   │
│       ↓                        │       ↓                        │
│  💥 Trivial task gets P0       │  ✅ Trivial tasks skip it      │
│     with hardcoded stubs       │     and test at any phase      │
│       ↓                        │       ↓                        │
│  😤 More complex than the      │  😊 Right tool for right job   │
│     actual implementation      │                                │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Make walking skeleton conditional/opt-in — required only when cross-boundary integration risk is high, not for every plan.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Walking skeleton | ❌ Always mandatory | ✅ Conditional on integration risk |
| Simple tasks | ❌ Forced into P0 stubs | ✅ Can test directly at any phase |
| Phasing | ❌ Always starts with skeleton | ✅ Phases still used; skeleton is opt-in |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Change walking skeleton from mandatory to conditional. The skeleton is triggered by cross-boundary integration risk, not by project existence.

**Priority:** P0  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Update `day-dream` skill to make walking skeleton conditional
- Define clear criteria for when walking skeleton IS required
- Update `00_index.template.md` planning standards table
- Update `80_implementation.template.md` to show skeleton as optional P0 pattern

**Out of Scope:**
- Removing phasing entirely (phases remain; skeleton is just one P0 pattern)
- Automated detection of integration risk

---

## ✅ Acceptance Criteria

- [ ] `day-dream` SKILL.md documents walking skeleton as conditional, not mandatory
- [ ] Clear trigger criteria listed (e.g., "≥2 modules with shared data flow", "external API integration")
- [ ] `80_implementation.template.md` shows walking skeleton as one option, not the only P0 pattern
- [ ] Index template's planning standards table reflects conditionality

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| `day-dream` skill | internal | Done | File to be edited |
| `00_index.template.md` | internal | Done | Planning standards table |
| `80_implementation.template.md` | internal | Done | P0 section |

---

## 🚀 Phase 0 Tasks

| Task | Difficulty | Owner | Status |
|------|------------|-------|--------|
| Define walking skeleton trigger criteria | `[KNOWN]` | TBD | ⏳ [TODO] |
| Update `day-dream` SKILL.md skeleton policy | `[KNOWN]` | TBD | ⏳ [TODO] |
| Update index + implementation templates | `[KNOWN]` | TBD | ⏳ [TODO] |

---

## [Custom] 🎯 Walking Skeleton Trigger Criteria

Walking skeleton is **REQUIRED** when:

| Trigger | Example | Why |
|---------|---------|-----|
| ≥2 modules with shared data flow | Frontend + Backend API | Need to prove plumbing works before building features |
| External API integration | Third-party service calls | Need to validate connectivity before building logic |
| New infrastructure setup | Database, message queue | Need to prove environment works before coding |

Walking skeleton is **NOT NEEDED** when:

| Scenario | Example | Why |
|----------|---------|-----|
| Single skill/instruction update | Editing SKILL.md | Testable immediately, no integration boundary |
| Template-only changes | Updating .template.md files | No runtime integration to validate |
| Documentation/planning only | Writing blueprints | No code execution involved |
| Single-module internal changes | Adding a function to a module | Module tests validate directly |

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

**Prev:** [Fix Estimation](./03_feature_fix_estimation.md) | **Next:** [Fix Backward Compat](./05_feature_fix_backward_compat.md)

---

**← Back to:** [Index](./00_index.md)
