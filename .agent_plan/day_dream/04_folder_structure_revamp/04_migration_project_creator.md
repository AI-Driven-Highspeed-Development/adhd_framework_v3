# 04 - Migration: project_creator_core

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  New project gets 6 folders    │  New project gets modules/     │
│       ↓                        │       ↓                        │
│  💥 cores/, managers/, etc.    │  ✅ modules/foundation/        │
│       ↓                        │       ↓                        │
│  Workspace members = 6 globs   │  Workspace members = 1 glob    │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Update new project scaffolding to create `modules/` structure instead of 6 legacy folders.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Created folders | ❌ 6 legacy folders | ✅ modules/, modules/foundation/, modules/dev/ |
| pyproject.toml workspace | ❌ 6 member patterns | ✅ `modules/**` |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Update project scaffolding for new structure

**Priority:** P2  
**Difficulty:** `[KNOWN]`

**Estimated Lines Changed:** ~76 lines across 2-3 files

**In Scope:**
- Update `PROJECT_DIRECTORIES` constant
- Delete `_infer_folder_from_name()` helper (no longer needed)
- Update `pyproject.toml.template` workspace members
- Update `.gitignore.template` if needed

**Out of Scope:**
- Migrating existing projects (that's P5)
- New project templates beyond structure

---

## 📁 Files to Modify

| File | Changes | Lines |
|------|---------|-------|
| `project_creator.py` | Update directories, remove helper | ~50 |
| `pyproject.toml.template` | Update workspace members | ~15 |
| `.gitignore.template` | Update ignored paths (if needed) | ~11 |

---

## 🔧 Implementation Details

### 1. project_creator.py — PROJECT_DIRECTORIES

**Current:**
```python
PROJECT_DIRECTORIES = [
    "cores",
    "managers", 
    "plugins",
    "utils",
    "mcps",
    "project",
    "tests",
    "playground",
    ".agent_plan",
]
```

**New:**
```python
PROJECT_DIRECTORIES = [
    "modules",
    "modules/foundation",
    "modules/runtime",
    "modules/dev",
    "tests",
    "playground",
    ".agent_plan",
]
```

### 2. project_creator.py — Remove _infer_folder_from_name()

**Delete this function entirely:**
```python
def _infer_folder_from_name(module_name: str) -> str:
    """Infer target folder from module name suffix."""
    # This logic is obsolete - we use explicit layer now
    ...
```

### 3. pyproject.toml.template — Workspace Members

**Current:**
```toml
[tool.uv.workspace]
members = [
    "cores/*",
    "managers/*", 
    "plugins/*",
    "utils/*",
    "mcps/*",
    "project/*",
]
```

**New:**
```toml
[tool.uv.workspace]
members = [
    "modules/**",
]
```

**Note:** The `**` glob handles all nesting depths (foundation/*, dev/*, and root modules).

### 4. .gitignore.template — Update Paths

**Add/Update:**
```gitignore
# Module artifacts
modules/**/build/
modules/**/__pycache__/
modules/**/*.egg-info/
```

**Remove (if present):**
```gitignore
# Legacy folders
cores/
managers/
plugins/
utils/
mcps/
```

---

## ✅ Acceptance Criteria

- [ ] `adhd init new_project` creates `modules/`, `modules/foundation/`, `modules/runtime/`, `modules/dev/`
- [ ] New projects have correct workspace members in pyproject.toml
- [ ] `_infer_folder_from_name()` removed
- [ ] No legacy folder references in templates

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| modules_controller_core | internal | Must complete P0 first | Constants |
| module_creator_core | internal | Must complete P1 first | Uses same paths |

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Update `PROJECT_DIRECTORIES` | `[KNOWN]` | ⏳ [TODO] |
| Remove `_infer_folder_from_name()` | `[KNOWN]` | ⏳ [TODO] |
| Update `pyproject.toml.template` | `[KNOWN]` | ⏳ [TODO] |
| Update `.gitignore.template` | `[KNOWN]` | ⏳ [TODO] |
| Update tests | `[KNOWN]` | ⏳ [TODO] |

---

## 🧪 Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd init test_project` | Creates `modules/`, `modules/foundation/`, `modules/runtime/`, `modules/dev/` |
| Check `test_project/pyproject.toml` | Has `members = ["modules/**"]` |
| Check folder structure | No `cores/`, `managers/`, etc. |

---

## ✅ Migration Validation Checklist

### Completeness
- [ ] All templates updated
- [ ] Helper function removed
- [ ] Tests updated

### Traceability
- [ ] Implements [01_feature_new_structure.md](./01_feature_new_structure.md)
- [ ] Depends on [02_migration_modules_controller.md](./02_migration_modules_controller.md)
- [ ] Depends on [03_migration_module_creator.md](./03_migration_module_creator.md)

---

**← Back to:** [Index](./00_index.md) | **Prev:** [03 - module_creator_core](./03_migration_module_creator.md) | **Next:** [05 - adhd_mcp + CLI](./05_migration_adhd_mcp_cli.md)
