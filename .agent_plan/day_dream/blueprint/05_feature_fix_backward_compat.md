# 05 - Feature: Fix Backward Compatibility Directive

> Part of [DREAM Upgrade Blueprint](./00_index.md)

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
│                                │  😊 Clean code always          │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Prioritize clean, correct code over minimizing edits; when backward compat IS needed, separate old/new paths in distinct files/folders.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Default stance | ❌ Minimize changes, preserve old behavior | ✅ Write correct code, clean implementation |
| Compat pattern | ❌ try/catch side-by-side in same file | ✅ Separate files/folders, deletable old path |
| Agent behavior | ❌ Afraid to break anything | ✅ Confident to write correct code |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Establish a "clean-code-over-backward-compat" directive for all agent work. When backward compatibility IS needed, enforce folder-separated old/new paths instead of inline try/catch.

**Priority:** P0  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Add clean-code-first directive to `day-dream` skill
- Document the folder-separation pattern for compat when genuinely needed
- Add to HyperDream and HyperArch agent instructions/skill references
- Define criteria for when backward compat IS justified

**Out of Scope:**
- Automated compat detection tooling
- Rewriting existing code that has inline compat patterns
- External library API backward compatibility (that's a different concern)

---

## ✅ Acceptance Criteria

- [ ] `day-dream` skill includes clean-code-first directive with clear language
- [ ] Folder-separation pattern documented with example structure
- [ ] Criteria for "when compat IS needed" are explicit (e.g., published API, external consumers)
- [ ] Agent instructions reference the directive

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| `day-dream` skill | internal | Done | File to be edited |

---

## 🚀 Phase 0 Tasks

| Task | Difficulty | Owner | Status |
|------|------------|-------|--------|
| Write clean-code-first directive section in skill | `[KNOWN]` | TBD | ⏳ [TODO] |
| Document folder-separation compat pattern | `[KNOWN]` | TBD | ⏳ [TODO] |
| Define "when compat IS justified" criteria | `[KNOWN]` | TBD | ⏳ [TODO] |

---

## [Custom] 🎯 The Directive

### Clean-Code-First Rule

```
DEFAULT: Write correct code. Do not preserve wrong behavior.
         Do not minimize edit count. Do not add fallbacks to old patterns.

EXCEPTION: Backward compat is justified ONLY when:
  1. Published API consumed by external projects
  2. Data format with existing persisted data that cannot be migrated
  3. Explicit human instruction to maintain compatibility

WHEN COMPAT IS NEEDED: Folder separation, not inline branching.
```

### Folder Separation Pattern

```
module/
├── v2/                    # NEW correct implementation
│   ├── __init__.py
│   └── processor.py
├── v1_compat/             # OLD path (delete when migration done)
│   ├── __init__.py
│   └── processor.py
└── __init__.py            # Entry point selects path
```

### Anti-Pattern (NEVER DO THIS)

```python
# ❌ WRONG: Inline compat spaghetti
def process(data):
    try:
        return new_correct_process(data)
    except (OldFormatError, KeyError):
        return old_wrong_fallback(data)  # This never gets deleted
```

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

**Prev:** [Fix Walking Skeleton](./04_feature_fix_walking_skeleton.md) | **Next:** [DREAM Planning Skill](./06_feature_dream_planning_skill.md)

---

**← Back to:** [Index](./00_index.md)
