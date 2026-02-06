# 03 - Migration: module_creator_core

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  Wizard: "What type?"          │  Wizard: "What layer?"         │
│       ↓                        │       ↓                        │
│  💥 6 subjective choices       │  ✅ 3 objective choices        │
│       ↓                        │       ↓                        │
│  Routes to managers/           │  Routes to modules/            │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Update the module creation wizard to ask layer + mcp questions, route to `modules/` paths, and fix the `{module_type}` template bug.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Type question | ❌ 6 options | ✅ Gone |
| Layer question | ❌ Doesn't exist | ✅ 3 options |
| MCP question | ❌ Implicit | ✅ Explicit |
| Output paths | ❌ managers/, utils/, etc. | ✅ modules/foundation/, modules/runtime/, modules/dev/ |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Update module creator wizard and templates for the new structure

**Priority:** P1  
**Difficulty:** `[KNOWN]`

**Estimated Lines Changed:** ~150 lines across 3-4 files + templates

**In Scope:**
- Remove type question from wizard
- Add layer question (foundation, runtime, dev)
- Add MCP question (yes/no)
- Update routing logic to new paths
- Fix template bug: `{module_type}` placeholder not provided
- Remove `SINGULAR_TO_FOLDER` mapping

**Out of Scope:**
- New templates for specific module types
- Validation of layer dependencies

---

## 📁 Files to Modify

| File | Changes | Lines |
|------|---------|-------|
| `module_creation_wizard.py` | New wizard flow | ~80 |
| `module_creator.py` | Remove `SINGULAR_TO_FOLDER`, update routing | ~50 |
| Templates (4 files) | Remove `{module_type}` placeholder | ~20 |

---

## 🔧 Implementation Details

### 1. New Wizard Flow

**Current Flow:**
```
1. "Module name"
2. "What type?" → [core, manager, plugin, util, mcp, project]
3. "Create instructions file?"
4. "Create GitHub repo?"
```

**New Flow:**
```
1. "Module name"
2. "What layer?" → [foundation, runtime, dev]
3. "Is this an MCP server?" → [yes, no]
4. "Create instructions file?"
5. "Create GitHub repo?"
```

### 2. module_creation_wizard.py

**New Questions:**
```python
LAYER_QUESTION = {
    "type": "list",
    "name": "layer",
    "message": "What layer does this module belong to?",
    "choices": [
        {"name": "runtime — Most modules, may depend on foundation + runtime", "value": "runtime"},
        {"name": "foundation — Only depends on other foundation (logger, config, exceptions)", "value": "foundation"},
        {"name": "dev — Development-time only, may depend on anything (test utils, red team)", "value": "dev"},
    ],
    "default": "runtime",
}

MCP_QUESTION = {
    "type": "confirm",
    "name": "is_mcp",
    "message": "Is this an MCP server?",
    "default": False,
}
```

### 3. module_creator.py — Routing Logic

**Current:**
```python
SINGULAR_TO_FOLDER = {
    "core": "cores",
    "manager": "managers",
    "plugin": "plugins",
    "util": "utils",
    "mcp": "mcps",
    "project": "project",
}

def _get_target_folder(module_type: str) -> Path:
    return project_root / SINGULAR_TO_FOLDER[module_type]
```

**New:**
```python
# Symmetric layer mapping
LAYER_TO_FOLDER = {
    "foundation": "foundation",
    "runtime": "runtime",
    "dev": "dev",
}

def _get_target_folder(layer: str) -> Path:
    """Get target folder based on layer."""
    modules_dir = project_root / "modules"
    return modules_dir / LAYER_TO_FOLDER[layer]
```

### 4. Template Fix

**Bug Found:** Templates use `{module_type}` but `_get_template_vars()` doesn't provide it.

**Fix Options:**
1. ❌ Add `module_type` back — Wrong direction
2. ✅ Remove `{module_type}` from templates — Correct
3. ✅ Replace with `{layer}` if needed — Optional

**Templates to Update:**
- `pyproject.toml.template`
- `README.md.template`
- `__init__.py.template`
- `{module_name}.py.template`

### 5. pyproject.toml Template Update

**Current:**
```toml
[tool.adhd]
name = "{module_name}"
version = "0.1.0"
```

**New:**
```toml
[tool.adhd]
name = "{module_name}"
version = "0.1.0"
layer = "{layer}"
{%- if is_mcp %}
mcp = true
{%- endif %}
```

---

## ✅ Acceptance Criteria

- [ ] Wizard asks layer question instead of type
- [ ] Wizard asks MCP question
- [ ] New modules created in correct `modules/` paths
- [ ] `[tool.adhd].layer` set in generated pyproject.toml
- [ ] `[tool.adhd].mcp = true` set for MCP servers
- [ ] No `{module_type}` placeholder errors
- [ ] `SINGULAR_TO_FOLDER` constant removed

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| modules_controller_core | internal | Must complete P0 first | Layer constants |

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Update wizard questions | `[KNOWN]` | ⏳ [TODO] |
| Update routing logic | `[KNOWN]` | ⏳ [TODO] |
| Remove `SINGULAR_TO_FOLDER` | `[KNOWN]` | ⏳ [TODO] |
| Fix template `{module_type}` bug | `[KNOWN]` | ⏳ [TODO] |
| Update pyproject.toml template | `[KNOWN]` | ⏳ [TODO] |
| Update tests | `[KNOWN]` | ⏳ [TODO] |

---

## 🧪 Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Run `adhd create module test_mod` | Asks layer, then MCP questions |
| Select "foundation" layer | Creates in `modules/foundation/test_mod/` |
| Select "runtime" + MCP=yes | Creates in `modules/runtime/test_mod/` with `mcp = true` |
| Select "dev" layer | Creates in `modules/dev/test_mod/` |

---

## ✅ Migration Validation Checklist

### Completeness
- [ ] Wizard flow updated
- [ ] Routing logic updated
- [ ] Templates fixed
- [ ] Tests updated

### Traceability
- [ ] Implements [01_feature_new_structure.md](./01_feature_new_structure.md)
- [ ] Depends on [02_migration_modules_controller.md](./02_migration_modules_controller.md)

---

**← Back to:** [Index](./00_index.md) | **Prev:** [02 - modules_controller_core](./02_migration_modules_controller.md) | **Next:** [04 - project_creator_core](./04_migration_project_creator.md)
