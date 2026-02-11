# Feature: Template Refresh

> Part of [P2: DREAM Integration](./_overview.md) · ✅ [DONE]

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

> Update all blueprint templates to align with fixed skill rules: AI-agent time, conditional skeleton, plan/task terminology, scaffold-not-authority comment.

---

## 🔧 The Spec

**Priority:** P2 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Create `overview.template.md` — template for mandatory `_overview.md` files
- Create `task.template.md` — template for leaf task files
- Update `00_index.template.md` — planning standards
- Update `80_implementation.template.md` — AI-agent durations, conditional skeleton
- Update feature templates — terminology alignment, scaffold headers

**Out of Scope:**
- New template types beyond `overview.template.md` and `task.template.md`
- Changing Story/Spec pattern
- Updating `simple.template.md`

---

## ✅ Acceptance Criteria

- [x] `overview.template.md` exists with Purpose, Children table, Integration Map, Reading Order
- [x] `task.template.md` exists as scaffold for leaf task files
- [x] `00_index.template.md` planning standards updated
- [x] `80_implementation.template.md` uses AI-agent durations, conditional skeleton
- [x] All templates include scaffold-not-authority comment
- [x] No template uses "node" terminology — replaced with plan/task

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Create `overview.template.md` | `[KNOWN]` | ✅ [DONE] |
| Create `task.template.md` | `[KNOWN]` | ✅ [DONE] |
| Update `00_index.template.md` planning standards | `[KNOWN]` | ✅ [DONE] |
| Update `80_implementation.template.md` | `[KNOWN]` | ✅ [DONE] |
| Update feature templates with terminology + headers | `[KNOWN]` | ✅ [DONE] |

---

## [Custom] 📋 Templates Touched

| Template | Change | Priority |
|----------|---------|----------|
| `overview.template.md` | **NEW** — `_overview.md` scaffold | High |
| `task.template.md` | **NEW** — leaf task scaffold | Medium |
| `00_index.template.md` | Planning standards table | Medium |
| `80_implementation.template.md` | Durations, skeleton conditionality | High |
| `NN_feature*.template.md` | Terminology, scaffold header | Medium |

---

**← Back to:** [P2 Overview](./_overview.md) · [DREAM Upgrade](../../dream-upgrade/_overview.md)
