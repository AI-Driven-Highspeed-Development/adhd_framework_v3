# 03 - Feature: Fix Estimation Defaults

> Part of [DREAM Upgrade Blueprint](./00_index.md)

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

---

## 🎯 Intent & Scope

**Intent:** Replace fragile time-based estimation defaults with fixed slot-based capacity units across all planning documents and skills.

**Priority:** P0  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Update `day-dream` skill's estimation tables to use slot magnitudes
- Update `80_implementation.template.md` P0 duration defaults to slot budgets
- Define `human_only: true` flag semantics for exception cases
- Update HyperDream agent instructions to reference slot-based estimation

**Out of Scope:**
- Automated time tracking or estimation tooling
- Changing already-written blueprints retroactively

---

## ✅ Acceptance Criteria

- [x] `day-dream` SKILL.md uses slot-based capacity scale in all estimation references
- [x] `80_implementation.template.md` shows slot budgets (fixed counts, not time ranges)
- [x] `human_only: true` flag is documented with clear usage criteria
- [x] Magnitude-to-slot mapping table uses fixed values with visual bars

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| `day-dream` skill | internal | Done | File to be edited |
| `80_implementation.template.md` | internal | Done | Template to be updated |

---

## 🚀 Phase 0 Tasks

| Task | Difficulty | Owner | Status |
|------|------------|-------|--------|
| Update estimation tables in `day-dream` SKILL.md to slots | `[KNOWN]` | HyperDream | ✅ [DONE] |
| Update `80_implementation.template.md` to slot budgets | `[KNOWN]` | HyperDream | ✅ [DONE] |
| Document `human_only: true` flag semantics in skill | `[KNOWN]` | HyperDream | ✅ [DONE] |

---

## [Custom] 📏 Slot-Based Estimation Scale

**Baseline:** 4 action slots per day

| Magnitude | Slot Cost | Cognitive Signal |
|-----------|-----------|------------------|
| Trivial | <<1 slot | Negligible overhead, batches with other work |
| Light | 1 slot | Single focused work unit |
| Standard | 2 slots | Half a day's capacity |
| Heavy | 3 slots | Nearly full day |
| Epic | 4+ slots | **MUST DECOMPOSE** — too large for single task |

**Phase Duration Defaults:**
| Phase | Slot Budget | Visual | Notes |
|-------|-------------|--------|-------|
| P0 | 2 slots | ■■□□ Standard | Walking skeleton — must be small |
| P1 | 4 slots | ■■■■ Epic boundary | First real enhancement |
| P2+ | Per-task | Sum of ■ bars | Sum of individual task slots |

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

**Prev:** [Architecture](./02_architecture.md) | **Next:** [Fix Walking Skeleton](./04_feature_fix_walking_skeleton.md)

---

**← Back to:** [Index](./00_index.md)
