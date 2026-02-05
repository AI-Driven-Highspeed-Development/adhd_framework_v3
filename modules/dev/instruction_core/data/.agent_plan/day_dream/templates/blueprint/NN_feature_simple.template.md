````markdown
<!--
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    SIMPLE FEATURE TEMPLATE                                    ║
║                                                                               ║
║  Use this template for SIMPLE features:                                       ║
║    • ≤2 modules involved                                                      ║
║    • No external API integration                                              ║
║    • Not P0 priority (not critical path)                                      ║
║    • No deep technical decisions (algorithm design, state machines)           ║
║                                                                               ║
║  Upgrade to NN_feature.template.md when complexity increases.                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
-->

# NN - Feature: {Feature Name}

> Part of [{Project Name} Blueprint](./00_index.md)

---

## 📖 The Story

<!--
REQUIRED: Visual, scannable narrative — NOT a text wall.
Use ASCII boxes, tables, and emoji anchors. A PM should grasp the problem/solution in 10 seconds.
Simple template = simpler diagrams, but STILL visual.
-->

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                        │
├────────────────────────────────┼────────────────────────────────┤
│  User wants {X}                │  User wants {X}                │
│       ↓                        │       ↓                        │
│  💥 {blocker/pain}             │  ✅ {solution works}           │
│       ↓                        │       ↓                        │
│  😤 Frustrated                 │  😊 Happy                      │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> {The elevator pitch in ONE sentence — what we're building and why it matters}

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| {thing} | ❌ {bad} | ✅ {good} |

---

## 🔧 The Spec

<!-- Everything below this line is technical specification. -->

---

## 🎯 Intent & Scope

**Intent:** {What this feature achieves in one sentence}

**Priority:** P0 | P1 | P2  
**Difficulty:** `[KNOWN]` | `[EXPERIMENTAL]`

**In Scope:**
- {What this feature includes}
- {Another included item}

**Out of Scope:**
- {What this feature explicitly does NOT include}
- {Deferred to later}

---

## ✅ Acceptance Criteria

<!-- Specific, testable criteria. Each should be verifiable. -->

- [ ] {Criterion 1 — specific and testable}
- [ ] {Criterion 2 — specific and testable}
- [ ] {Criterion 3 — specific and testable}

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| {Module/API} | internal / external | Done / Pending | {Notes} |

---

## 🚀 Phase 0 Tasks

| Task | Difficulty | Owner | Status |
|------|------------|-------|--------|
| {Task 1} | `[KNOWN]` | TBD | ⏳ [TODO] |
| {Task 2} | `[KNOWN]` | TBD | ⏳ [TODO] |

---

## ⬆️ Upgrade Trigger

Expand to full `NN_feature.template.md` when:
- ≥3 modules involved
- External API integration required
- P0 priority (critical path)
- Deep technical decisions needed (algorithm design, state machines)
- Need for Deep Dive section (complexity analysis, API contracts)

---

## ✅ Simple Feature Validation Checklist

<!-- MANDATORY: Complete before handoff. -->

### Narrative
- [ ] **The Story** clearly states user problem and value
- [ ] **Intent** is unambiguous to a non-technical reader

### Technical
- [ ] **Scope** is explicitly bounded (In/Out of Scope filled)
- [ ] **Acceptance Criteria** are testable (not vague)
- [ ] **Dependencies** are listed with status

### Linkage
- [ ] Feature linked from `00_index.md` or `01_executive_summary.md`

---

**← Back to:** [Index](./00_index.md)

````
