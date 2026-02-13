# Feature: Fix Backward Compatibility Directive

> Part of [P0: Fix Blueprint System](./_overview.md) · ✅ [DONE]

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  Agent writes:                 │  Agent writes:                 │
│  try:                          │  # Clean, correct code         │
│    new_correct_code()          │  new_correct_code()            │
│  except:                       │                                │
│    old_wrong_fallback()        │  # If compat needed:           │
│       ↓                        │  compat/old_path/module.py     │
│  💥 Spaghetti grows forever    │  compat/new_path/module.py     │
│       ↓                        │       ↓                        │
│  😤 Code gets worse over time  │  ✅ Delete old/ when done      │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Prioritize clean, correct code over minimizing edits; when backward compat IS needed, separate old/new paths in distinct files/folders.

---

## 🔧 The Spec

**Priority:** P0 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Add clean-code-first directive to `day-dream` skill
- Document the folder-separation pattern for compat
- Define criteria for when backward compat IS justified

**Out of Scope:**
- Automated compat detection tooling
- Rewriting existing code that has inline compat patterns

---

## ✅ Acceptance Criteria

- [x] `day-dream` skill includes clean-code-first directive
- [x] Folder-separation pattern documented with example
- [x] Criteria for "when compat IS needed" are explicit

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Write clean-code-first directive section in skill | `[KNOWN]` | ✅ [DONE] |
| Document folder-separation compat pattern | `[KNOWN]` | ✅ [DONE] |
| Define "when compat IS justified" criteria | `[KNOWN]` | ✅ [DONE] |

---

## [Custom] 🎯 The Directive

```
DEFAULT: Write correct code. Do not preserve wrong behavior.

EXCEPTION: Backward compat is justified ONLY when:
  1. Published API consumed by external projects
  2. Data format with existing persisted data that cannot be migrated
  3. Explicit human instruction to maintain compatibility

WHEN COMPAT IS NEEDED: Folder separation, not inline branching.
```

### Anti-Pattern (NEVER)

```python
# ❌ WRONG: Inline compat spaghetti
try:
    result = new_correct_handler(data)
except:
    result = old_broken_handler(data)  # This never gets deleted
```

---

**← Back to:** [P0 Overview](./_overview.md) · [DREAM Upgrade](../_overview.md)
