# 05 - Migration: adhd_mcp + CLI

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  list_modules --types manager  │  list_modules --layers runtime │
│       ↓                        │       ↓                        │
│  💥 Type filtering (broken)    │  ✅ Layer filtering (works)    │
│       ↓                        │       ↓                        │
│  Inconsistent results          │  Predictable results           │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Update MCP tools and CLI to filter by layer instead of type.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Filter parameter | ❌ `--types` | ✅ `--layers` |
| MCP tool param | ❌ `types: list[str]` | ✅ `layers: list[str]` |
| Help text | ❌ Mentions type | ✅ Mentions layer |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Update all external interfaces (MCP, CLI) to use layer instead of type

**Priority:** P3  
**Difficulty:** `[KNOWN]`

**Estimated Lines Changed:** ~100 lines across 4 files

**In Scope:**
- Remove `types` parameter from `list_modules` MCP tool
- Add `layers` parameter
- Update `adhd_controller.py` filtering
- Update CLI `--types` → `--layers`
- Update help text everywhere

**Out of Scope:**
- New MCP tools
- CLI command restructuring

---

## 📁 Files to Modify

| File | Changes | Lines |
|------|---------|-------|
| `adhd_mcp.py` | Update tool parameters | ~30 |
| `adhd_controller.py` | Replace type filtering with layer | ~40 |
| `adhd_cli.py` | Update CLI arguments | ~20 |
| `adhd_framework.py` | Update help text | ~10 |

---

## 🔧 Implementation Details

### 1. adhd_mcp.py — Tool Definition

**Current:**
```python
@mcp.tool()
async def list_modules(
    include_cores: bool = False,
    types: list[str] | None = None,
    with_imports: bool = False,
) -> dict:
    """List discovered modules with optional filtering.
    
    Args:
        types: Filter by module types (e.g., ["manager", "util", "mcp"])
    """
```

**New:**
```python
@mcp.tool()
async def list_modules(
    include_cores: bool = False,  # Deprecated, kept for compat
    layers: list[str] | None = None,
    with_imports: bool = False,
) -> dict:
    """List discovered modules with optional filtering.
    
    Args:
        layers: Filter by layers (e.g., ["runtime", "foundation", "dev"])
    """
```

### 2. adhd_controller.py — Filtering

**Current:**
```python
def list_modules(
    include_cores: bool = False,
    types: list[str] | None = None,
) -> list[ModuleInfo]:
    modules = discover_modules(root)
    
    if types:
        modules = [m for m in modules if m.type in types]
    
    if not include_cores:
        modules = [m for m in modules if m.type != "core"]
    
    return modules
```

**New:**
```python
def list_modules(
    layers: list[str] | None = None,
) -> list[ModuleInfo]:
    modules = discover_modules(root)
    
    if layers:
        modules = [m for m in modules if m.layer in layers]
    
    return modules
```

**Note:** `include_cores` is now unnecessary since "core" was a type, not a layer. Foundation modules are just modules with `layer="foundation"`.

### 3. adhd_cli.py — Arguments

**Current:**
```python
@click.option("--types", "-t", multiple=True, help="Filter by module types")
def list_modules(types: tuple[str, ...]):
    ...
```

**New:**
```python
@click.option("--layers", "-l", multiple=True, 
              type=click.Choice(["foundation", "runtime", "dev"]),
              help="Filter by layers")
def list_modules(layers: tuple[str, ...]):
    ...
```

### 4. adhd_framework.py — Help Text

**Update any references:**
```python
# OLD
"Filter modules by type (core, manager, plugin, util, mcp)"

# NEW
"Filter modules by layer (foundation, runtime, dev)"
```

---

## ✅ Acceptance Criteria

- [ ] `list_modules` MCP tool accepts `layers` parameter
- [ ] `list_modules` MCP tool no longer accepts `types` parameter
- [ ] CLI `--layers` works with choices validation
- [ ] CLI `--types` removed
- [ ] All help text updated
- [ ] Filtering by layer works correctly

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| modules_controller_core | internal | Must complete P0 first | Layer inference |

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Update `adhd_mcp.py` tool definition | `[KNOWN]` | ⏳ [TODO] |
| Update `adhd_controller.py` filtering | `[KNOWN]` | ⏳ [TODO] |
| Update `adhd_cli.py` arguments | `[KNOWN]` | ⏳ [TODO] |
| Update `adhd_framework.py` help text | `[KNOWN]` | ⏳ [TODO] |
| Update tests | `[KNOWN]` | ⏳ [TODO] |

---

## 🧪 Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| MCP: `list_modules(layers=["foundation"])` | Returns only foundation modules |
| CLI: `adhd modules --layers runtime` | Lists runtime modules only |
| CLI: `adhd modules --types manager` | Error: unrecognized option |
| CLI: `adhd modules --help` | Shows `--layers` option |

---

## ✅ Migration Validation Checklist

### Completeness
- [ ] MCP tool updated
- [ ] Controller updated
- [ ] CLI updated
- [ ] Help text updated
- [ ] Tests updated

### Traceability
- [ ] Implements [01_feature_new_structure.md](./01_feature_new_structure.md)
- [ ] Depends on [02_migration_modules_controller.md](./02_migration_modules_controller.md)

---

**← Back to:** [Index](./00_index.md) | **Prev:** [04 - project_creator_core](./04_migration_project_creator.md) | **Next:** [06 - Instructions](./06_migration_instructions.md)
