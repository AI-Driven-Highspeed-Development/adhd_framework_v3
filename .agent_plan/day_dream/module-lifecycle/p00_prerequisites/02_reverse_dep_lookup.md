# Feature: Reverse Dependency Lookup

> Part of [P0: Prerequisites](./_overview.md) · ⏳ [TODO]

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  DependencyWalker answers:     │  DependencyWalker answers:     │
│  "What does X depend on?"      │  "What does X depend on?"      │
│                                │  "What depends on X?" ← NEW    │
│       ↓                        │       ↓                        │
│  💥 Can't check if removing X  │  ✅ "3 modules depend on X,    │
│     will break other modules   │      are you sure?"            │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Add `get_reverse_deps(module_name)` to `DependencyWalker` so the remove command can warn before breaking dependents.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Dependency direction | ❌ Forward only | ✅ Forward + reverse |
| Safety before remove | ❌ None | ✅ "These modules depend on X" |

---

## 🔧 The Spec

**Priority:** P0 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Add `get_reverse_deps(module_name: str) -> Set[str]` to `DependencyWalker`
- Iterate all known modules, check if `module_name` appears in their dependency closure
- Return set of module names that depend on the given module
- Unit tests

**Out of Scope:**
- Transitive reverse deps (direct dependents are sufficient for safety warning)
- Caching or performance optimization (module count is small)
- CLI integration (that's P1)

---

## ✅ Acceptance Criteria

- [ ] `get_reverse_deps("logger-util")` returns modules that list logger-util as a dependency
- [ ] Returns empty set for modules with no dependents
- [ ] Works for both foundation and dev layer modules
- [ ] Unit test with known dependency graph

---

## 🛠️ Technical Notes

### Approach

The `DependencyWalker` already has `walk()` which builds a forward closure. For reverse lookup:

1. Use `ModulesController.get_all_modules()` to enumerate all modules
2. For each module, read its `pyproject.toml` dependencies
3. Check if `module_name` (or its package name equivalent) appears in the dependency list
4. Collect all matching modules as the reverse dependency set

This is an O(N) scan where N = number of modules. Acceptable for ADHD projects (typically <50 modules).

### API Design

```python
def get_reverse_deps(self, module_name: str, controller: "ModulesController") -> Set[str]:
    """Get modules that depend on the given module.
    
    Args:
        module_name: Name of the module to check (e.g., "logger-util")
        controller: ModulesController for module discovery
        
    Returns:
        Set of module names that have module_name in their dependencies
    """
```

---

## 🔗 Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| `ModulesController.get_all_modules()` | ✅ Done | Exists — module enumeration |
| `DependencyWalker` | ✅ Done | Exists — extend with new method |

---

**← Back to:** [P0 Overview](./_overview.md) · [Module Lifecycle](../_overview.md)
