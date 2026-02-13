# Feature: Fix Estimation Defaults

> Part of [P0: Fix Blueprint System](./_overview.md) · ✅ [DONE]

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  "P0: 3-5 days"                │  "P0: ■■□□ Standard (2 slots)" │
│       ↓                        │       ↓                        │
│  💥 Time-based = always wrong  │  ✅ Slots = cognitive capacity │
│       ↓                        │       ↓                        │
│  😤 Fragile, meaningless       │  😊 Stable, composable         │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Replace fragile time-based estimates with fixed slot-based capacity units (4 slots/day); add `human_only: true` flag for tasks that genuinely require human involvement.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| P0 duration default | ❌ "3-5 days" | ✅ ■■□□ Standard (2 slots) |
| Task estimate unit | ❌ Human days/weeks | ✅ Fixed slots (1-4 capacity units) |
| Human tasks | ❌ Same scale as agent tasks | ✅ Flagged with `human_only: true` |

---

## 🔧 The Spec

**Priority:** P0 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Update `day-dream` skill's estimation tables to use slot magnitudes
- Update `80_implementation.template.md` P0 duration defaults to slot budgets
- Define `human_only: true` flag semantics

**Out of Scope:**
- Automated time tracking or estimation tooling
- Changing already-written blueprints retroactively

---

## ✅ Acceptance Criteria

- [x] `day-dream` SKILL.md uses slot-based capacity scale in all estimation references
- [x] `80_implementation.template.md` shows slot budgets
- [x] `human_only: true` flag is documented with clear usage criteria
- [x] Magnitude-to-slot mapping table uses fixed values with visual bars

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Update estimation tables in `day-dream` SKILL.md to slots | `[KNOWN]` | ✅ [DONE] |
| Update `80_implementation.template.md` to slot budgets | `[KNOWN]` | ✅ [DONE] |
| Document `human_only: true` flag semantics in skill | `[KNOWN]` | ✅ [DONE] |

---

## [Custom] 📏 Slot-Based Estimation Scale

**Baseline:** 4 action slots per day

| Magnitude | Slot Cost | Cognitive Signal |
|-----------|-----------|------------------|
| Trivial | <<1 slot | Negligible overhead, batches with other work |
| Light | 1 slot | Single focused work unit |
| Standard | 2 slots | Half a day's capacity |
| Heavy | 3 slots | Nearly full day |
| Epic | 4+ slots | **MUST DECOMPOSE** |

---

**← Back to:** [P0 Overview](./_overview.md) · [DREAM Upgrade](../_overview.md)
