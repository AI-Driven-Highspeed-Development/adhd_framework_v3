# 02 - Migration: modules_controller_core

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  Discovery scans 6 folders     │  Discovery scans 3 layer dirs  │
│       ↓                        │       ↓                        │
│  💥 Complex path logic         │  ✅ Simple layer_from_path()   │
│       ↓                        │       ↓                        │
│  😤 "type" everywhere          │  😊 "layer" only               │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Rewrite module discovery to scan `modules/foundation/`, `modules/runtime/`, and `modules/dev/` instead of 6 legacy folders.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Discovery paths | ❌ 6 folders | ✅ 3 explicit layer folders |
| Type field | ❌ Used for filtering | ✅ Gone |
| Layer inference | ❌ None | ✅ From path (symmetric folders) |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Replace all module discovery logic to use the new `modules/` structure

**Priority:** P0 (Critical Path — all other migrations depend on this)  
**Difficulty:** `[KNOWN]`

**Estimated Lines Changed:** ~455 lines across 4-5 files

**In Scope:**
- Rewrite `MODULE_FOLDERS` constant
- New discovery algorithm in `modules_controller.py`
- New `layer_from_path()` function
- Remove/repurpose filter logic in `module_filter.py`
- Remove `MISSING_TYPE`, `INVALID_TYPE_LAYER_COMBO` issue codes
- Update all discovery tests

**Out of Scope:**
- Physical file migration (P5)
- CLI changes (P3)

---

## 📁 Files to Modify

| File | Changes | Lines |
|------|---------|-------|
| `module_constants.py` | Replace `MODULE_FOLDERS` constant | ~20 |
| `modules_controller.py` | Rewrite discovery logic, add `layer_from_path()` | ~200 |
| `module_filter.py` | Remove type filtering, update layer validation | ~80 |
| `module_issues.py` | Remove dead issue codes | ~30 |
| `tests/` | Rewrite discovery tests | ~125 |

---

## 🔧 Implementation Details

### 1. module_constants.py

**Current:**
```python
MODULE_FOLDERS = ["cores", "managers", "plugins", "utils", "mcps", "project"]
```

**New:**
```python
# Layer subfolder names
LAYER_FOUNDATION = "foundation"
LAYER_RUNTIME = "runtime"
LAYER_DEV = "dev"

# The unified modules directory
MODULES_DIR = "modules"

# All layer subfolders (symmetric structure)
LAYER_SUBFOLDERS = (LAYER_FOUNDATION, LAYER_RUNTIME, LAYER_DEV)
```

### 2. modules_controller.py — Discovery

**New Discovery Algorithm:**
```python
def discover_modules(root: Path) -> list[ModuleInfo]:
    """Discover all modules in the new structure.
    
    Scans 3 explicit layer folders - no exclusion logic needed.
    """
    modules_dir = root / MODULES_DIR
    if not modules_dir.exists():
        return []
    
    results = []
    
    # Symmetric scan: all 3 layers have explicit subfolders
    for layer in LAYER_SUBFOLDERS:
        layer_dir = modules_dir / layer
        if not layer_dir.exists():
            continue
        for path in layer_dir.iterdir():
            if _is_valid_module(path):
                results.append(_load_module(path, layer=layer))
    
    return results
```

### 3. modules_controller.py — layer_from_path()

**New Function:**
```python
def layer_from_path(module_path: Path, modules_root: Path) -> str | None:
    """Infer layer from physical location.
    
    Args:
        module_path: Path to the module directory
        modules_root: Path to the modules/ directory
        
    Returns:
        Layer name: "foundation", "runtime", or "dev"
        None if external module (cannot infer from path)
    """
    try:
        relative = module_path.relative_to(modules_root)
        first_part = relative.parts[0] if relative.parts else ""
        
        if first_part in LAYER_SUBFOLDERS:
            return first_part
        else:
            # Not in a recognized layer folder
            return None
    except ValueError:
        # External module — cannot infer from path
        return None
```

### 4. module_filter.py

**Changes:**
- Remove `filter_by_type()` or repurpose as `filter_by_layer()`
- Remove any `type` dimension from filter logic
- Keep `filter_by_layer()` for MCP/CLI filtering needs

### 5. module_issues.py

**Remove:**
```python
# Dead code — these are never raised
MISSING_TYPE = "missing_type"
INVALID_TYPE_LAYER_COMBO = "invalid_type_layer_combo"
```

---

## ✅ Acceptance Criteria

- [ ] `discover_modules()` returns all modules from `modules/foundation/`, `modules/runtime/`, `modules/dev/`
- [ ] `layer_from_path()` correctly returns "foundation", "runtime", or "dev"
- [ ] No references to `type` in modules_controller_core
- [ ] `MODULE_FOLDERS` constant replaced with `LAYER_SUBFOLDERS`
- [ ] Issue codes `MISSING_TYPE`, `INVALID_TYPE_LAYER_COMBO` removed
- [ ] All existing tests updated and passing
- [ ] New tests for layer inference

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| None | — | — | This is the foundation |

**Depended on by:**
- module_creator_core (imports discovery)
- adhd_mcp (imports module listing)
- cli_manager (imports module listing)

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Update `module_constants.py` | `[KNOWN]` | ⏳ [TODO] |
| Rewrite discovery in `modules_controller.py` | `[KNOWN]` | ⏳ [TODO] |
| Add `layer_from_path()` function | `[KNOWN]` | ⏳ [TODO] |
| Update `module_filter.py` | `[KNOWN]` | ⏳ [TODO] |
| Remove dead issue codes | `[KNOWN]` | ⏳ [TODO] |
| Rewrite discovery tests | `[KNOWN]` | ⏳ [TODO] |

---

## 🧪 Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Create test `modules/foundation/test_mod/` with pyproject.toml | Discovered with layer="foundation" |
| Create test `modules/runtime/my_plugin/` | Discovered with layer="runtime" |
| Create test `modules/dev/test_util/` | Discovered with layer="dev" |
| Run existing discovery command | Lists modules from all 3 layer folders |

---

## ✅ Migration Validation Checklist

### Completeness
- [ ] All files listed are modified
- [ ] No type references remain
- [ ] Tests cover layer inference

### Traceability
- [ ] Implements [01_feature_new_structure.md](./01_feature_new_structure.md)

---

**← Back to:** [Index](./00_index.md) | **Next:** [03 - module_creator_core](./03_migration_module_creator.md)
