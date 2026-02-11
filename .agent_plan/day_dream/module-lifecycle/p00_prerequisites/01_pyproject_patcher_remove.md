# Feature: Pyproject Patcher Remove

> Part of [P0: Prerequisites](./_overview.md) · ⏳ [TODO]

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  pyproject_patcher can:        │  pyproject_patcher can:        │
│  ✅ add_to_root_pyproject()    │  ✅ add_to_root_pyproject()    │
│  ❌ (no remove)                │  ✅ remove_from_root_pyproject()│
│       ↓                        │       ↓                        │
│  💥 Manual editing of          │  ✅ Clean removal of both      │
│     pyproject.toml required    │     deps and uv.sources        │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Add `remove_from_root_pyproject()` — the exact reverse of `add_to_root_pyproject()` — removing a package from both `[project.dependencies]` and `[tool.uv.sources]`.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Pyproject dep removal | ❌ Manual text editing | ✅ Single function call |
| uv.sources removal | ❌ Manual text editing | ✅ Handled automatically |
| Format preservation | N/A | ✅ String manipulation preserves formatting |

---

## 🔧 The Spec

**Priority:** P0 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Add `remove_from_root_pyproject(package_name: str, project_root: Path) -> None`
- Remove from `[project.dependencies]` list
- Remove from `[tool.uv.sources]` section
- Preserve file formatting (string manipulation, same pattern as add)
- Handle edge cases: not found, already removed
- Unit tests

**Out of Scope:**
- Removing from `[tool.uv.workspace.members]` (workspace members auto-discovered)
- Modifying module's own pyproject.toml
- Handle cascading pyproject changes across multiple files

---

## ✅ Acceptance Criteria

- [ ] `remove_from_root_pyproject("my-package", root)` removes from both deps and uv.sources
- [ ] Gracefully handles "not found" (warning, no error)
- [ ] Preserves formatting of remaining entries (no rewrite/reformat)
- [ ] Round-trip test: add → remove → file identical to original
- [ ] Unit test with real pyproject.toml fixture

---

## 🛠️ Technical Notes

### Approach

Mirror the existing `add_to_root_pyproject()` pattern:

1. Read pyproject.toml as string
2. Parse with `tomllib` to validate structure
3. Use string manipulation to find and remove the dependency line
4. Use string manipulation to find and remove the uv.sources line
5. Write back

### Key Implementation Details

**Removing from dependencies (list format):**
```toml
# Find and remove this line (including trailing comma/newline):
    "my-package",
```

**Removing from uv.sources (key-value format):**
```toml
# Find and remove this line:
my-package = { workspace = true }
```

**Edge cases:**
- Last item in dependencies list (no trailing comma after it)
- Whitespace variations in uv.sources entries
- Package not in one section but present in the other

### API Design

```python
def remove_from_root_pyproject(package_name: str, project_root: Path) -> None:
    """Remove a package from root pyproject.toml dependencies and [tool.uv.sources].
    
    Mirror of add_to_root_pyproject(). Uses string manipulation to preserve formatting.
    
    Args:
        package_name: The package name (kebab-case, e.g. 'my-module')
        project_root: Path to the project root directory
        
    Raises:
        ADHDError: If the file is missing or malformed.
    """
```

---

## 🔗 Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| `pyproject_patcher` module | ✅ Done | Exists — extend with new function |
| `add_to_root_pyproject()` | ✅ Done | Reference implementation to mirror |

---

**← Back to:** [P0 Overview](./_overview.md) · [Module Lifecycle](../_overview.md)
