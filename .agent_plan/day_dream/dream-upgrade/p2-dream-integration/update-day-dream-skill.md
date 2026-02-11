# Feature: Update Day-Dream Skill

> Part of [P2: DREAM Integration](./_overview.md) · ✅ [DONE]

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
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Apply all P0 fixes to the existing `day-dream` skill and add cross-references to the new `dream-planning` skill for magnitude-gated tier selection.

---

## 🔧 The Spec

**Priority:** P2 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Update estimation tables with AI-agent time scale (from P0 fix-estimation)
- Update walking skeleton policy to conditional (from P0 fix-walking-skeleton)
- Add clean-code-first directive (from P0 fix-backward-compat)
- Add `dream-planning` skill cross-reference for magnitude routing
- Update tier selection to include magnitude-gated criteria

**Out of Scope:**
- Rewriting skill from scratch
- Moving authoring rules to `dream-planning`
- Template changes (that's template-refresh)

---

## ✅ Acceptance Criteria

- [x] All estimation references use AI-agent time scale
- [x] Walking skeleton section documents conditionality with trigger table
- [x] Clean-code-first directive added
- [x] Tier selection includes magnitude routing
- [x] `human_only: true` flag documented

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Update tier selection with magnitude awareness | `[KNOWN]` | ✅ [DONE] |
| Apply estimation fixes | `[KNOWN]` | ✅ [DONE] |
| Apply walking skeleton fixes | `[KNOWN]` | ✅ [DONE] |
| Add clean-code-first directive | `[KNOWN]` | ✅ [DONE] |
| Add `dream-planning` skill cross-reference | `[KNOWN]` | ✅ [DONE] |

---

**← Back to:** [P2 Overview](./_overview.md) · [DREAM Upgrade](../../dream-upgrade/_overview.md)
