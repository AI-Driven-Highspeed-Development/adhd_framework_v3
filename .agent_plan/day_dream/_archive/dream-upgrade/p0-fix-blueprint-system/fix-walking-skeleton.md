# Feature: Fix Walking Skeleton Policy

> Part of [P0: Fix Blueprint System](./_overview.md) · ✅ [DONE]

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

---

## 🔧 The Spec

**Priority:** P0 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Update `day-dream` skill to make walking skeleton conditional
- Define clear criteria for when walking skeleton IS required
- Update index and implementation templates

**Out of Scope:**
- Removing phasing entirely (phases remain; skeleton is one P0 pattern)
- Automated detection of integration risk

---

## ✅ Acceptance Criteria

- [x] `day-dream` SKILL.md documents walking skeleton as conditional
- [x] Clear trigger criteria listed
- [x] `80_implementation.template.md` shows walking skeleton as one option, not the only P0 pattern
- [x] Planning standards table reflects conditionality

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Define walking skeleton trigger criteria | `[KNOWN]` | ✅ [DONE] |
| Update `day-dream` SKILL.md skeleton policy | `[KNOWN]` | ✅ [DONE] |
| Update index + implementation templates | `[KNOWN]` | ✅ [DONE] |

---

## [Custom] 🎯 Walking Skeleton Trigger Criteria

Walking skeleton is **REQUIRED** when:

| Trigger | Example |
|---------|---------|
| ≥2 modules with shared data flow | Frontend + Backend API |
| External API integration | Third-party service calls |
| New infrastructure setup | Database, message queue |

Walking skeleton is **NOT NEEDED** when:

| Scenario | Example |
|----------|---------|
| Single skill/instruction update | Editing SKILL.md |
| Template-only changes | Updating .template.md files |
| Documentation/planning only | Writing blueprints |
| Single-module internal changes | Adding a function to a module |

---

**← Back to:** [P0 Overview](./_overview.md) · [DREAM Upgrade](../_overview.md)
