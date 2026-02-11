# Feature: Remove Command

> Part of [P1: Core Commands](./_overview.md) · ⏳ [TODO]

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  To remove a module:           │  To remove a module:           │
│  1. Edit pyproject.toml deps   │  adhd remove my-module         │
│  2. Edit pyproject.toml sources│     → ✅ Done                  │
│  3. Delete directory           │                                │
│  4. uv sync                    │  With safety:                  │
│  5. adhd workspace             │  • Reverse-dep check           │
│  6. Hope nothing depends on it │  • Dry-run preview             │
│       ↓                        │  • Confirmation prompt         │
│  💥 6 manual steps, error-prone│  😊 One command, safe          │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> `adhd remove <name>` — the reverse of `adhd add`, with reverse-dep safety checks and complete cleanup.

---

## 🔧 The Spec

**Priority:** P1 · **Difficulty:** `[KNOWN]`

**In Scope:**
- `ModuleRemover` class in `module_lifecycle_core/module_remover.py`
- Full cleanup sequence: reverse-dep check → dry-run → confirm → unregister pyproject → remove uv.sources → delete dir → uv sync → workspace regen
- `--force` flag to override reverse-dep warnings
- `--dry-run` flag to preview changes
- `--no-confirm` for CI/scripting
- `--keep-dir` to unregister without deleting files
- CLI wiring in `adhd_framework.py`

**Out of Scope:**
- Removing module data (user-managed)
- `init.yaml` cleanup (legacy, excluded)
- Undo/rollback for remove (destructive by design, use git)

---

## ✅ Acceptance Criteria

- [ ] `adhd remove my-module` removes dep from pyproject.toml, uv.sources entry, module directory
- [ ] Runs `uv sync` after removal
- [ ] Runs `adhd workspace` to regenerate workspace file
- [ ] `--dry-run` shows preview without modifying anything
- [ ] Reverse-dep check warns if module has dependents, requires `--force`
- [ ] `--no-confirm` skips interactive prompt
- [ ] `--keep-dir` unregisters but preserves directory
- [ ] Informative error if module not found

---

## 🛠️ Technical Notes

### `ModuleRemover` Class Design

```python
@dataclass
class RemoveResult:
    success: bool
    module_name: str
    layer: Optional[str]
    reverse_deps: Set[str]  # Modules that depended on this
    message: str

class ModuleRemover:
    def __init__(self, project_root: Path):
        ...
    
    def remove(
        self,
        module_name: str,
        dry_run: bool = False,
        force: bool = False,
        keep_dir: bool = False,
    ) -> RemoveResult:
        """Remove a module from the workspace."""
```

### Removal Sequence

1. **Find module** — Use `ModulesController` to locate module path and metadata
2. **Check reverse deps** — Call `DependencyWalker.get_reverse_deps()`
3. **If dependents exist** — Refuse unless `--force` provided
4. **Dry-run preview** — Print what would be changed and return
5. **Unregister** — Call `remove_from_root_pyproject()`
6. **Delete directory** — `shutil.rmtree()` the module directory
7. **uv sync** — Subprocess call to regenerate lockfile
8. **Workspace regen** — Call workspace builder

### Edge Cases

| Scenario | Behavior |
|----------|----------|
| Module not found | Error with suggestion (fuzzy match) |
| Module has dependents | Refuse, list dependents, suggest `--force` |
| pyproject.toml entry missing but dir exists | Warn, delete dir anyway |
| Dir missing but pyproject.toml has entry | Clean up pyproject.toml entries |
| uv sync fails after removal | Warn but don't rollback (entry already removed) |

---

## 🔗 Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| `get_reverse_deps()` | ⏳ P0 | Must exist before remove can check safety |
| `remove_from_root_pyproject()` | ⏳ P0 | Must exist before remove can clean up |
| `ModulesController` | ✅ Done | Module discovery |
| `workspace_core` | ✅ Done | Workspace regeneration |

---

**← Back to:** [P1 Overview](./_overview.md) · [Module Lifecycle](../_overview.md)
