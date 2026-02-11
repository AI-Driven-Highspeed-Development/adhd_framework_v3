# Feature: Update Command

> Part of [P1: Core Commands](./_overview.md) · ⏳ [TODO]

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  To update a module:           │  To update a module:           │
│  1. adhd remove old-version    │  adhd update my-module         │
│     (6 manual steps)           │     → ✅ Done (atomic swap)    │
│  2. adhd add new-version       │                                │
│     (if step 1 failed halfway, │  Swap pattern:                 │
│      workspace is broken)      │  clone temp → validate →       │
│       ↓                        │  backup → swap → sync          │
│  💥 Failure window between     │       ↓                        │
│     remove and re-add          │  😊 No failure window,         │
│                                │     rollback on error          │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> `adhd update <name>` — atomic swap pattern: clone new to temp, validate, swap directories, clean up old. Never leaves workspace in a broken state.

---

## 🔧 The Spec

**Priority:** P1 · **Difficulty:** `[KNOWN]`

**In Scope:**
- `ModuleUpdater` class in `module_adder_core/module_updater.py`
- Atomic swap sequence: clone → validate → backup → swap → patch pyproject → uv sync → cleanup
- Rollback on failure (restore from backup)
- `--dry-run` flag
- `--branch <name>` flag
- `--keep-backup` flag
- Reuse `ModuleAdder` git clone patterns
- CLI wiring in `adhd_framework.py`

**Out of Scope:**
- Version comparison (always updates to latest HEAD)
- Changelog generation
- Auto-merging local modifications
- Batch update (that's P2)

---

## ✅ Acceptance Criteria

- [ ] `adhd update my-module` clones latest, validates, swaps atomically
- [ ] If uv sync fails after swap, rolls back to backup
- [ ] `--dry-run` shows diff preview without modifying anything
- [ ] `--branch develop` clones from specific branch
- [ ] `--keep-backup` preserves the .bak directory
- [ ] Module with local changes triggers warning (require `--force`)
- [ ] pyproject.toml is not modified (module replaces in-place, same package name)

---

## 🛠️ Technical Notes

### Atomic Swap Sequence

```
1. CLONE    — Clone new version to temp directory (via temp_files_manager)
2. VALIDATE — Check new module has valid pyproject.toml, correct package name
3. BACKUP   — Copy current pyproject.toml to pyproject.toml.bak
4. SWAP     — Move old module dir → {name}.bak, move new → target location
5. SYNC     — Run uv sync
6a. SUCCESS — Delete .bak directories
6b. FAILURE — Restore from .bak, report error
7. REGEN    — Run adhd workspace
```

### Key Insight: Why Swap, Not Remove+Re-Add

```
Remove + Re-Add:
  remove() → workspace is BROKEN → add() → workspace fixed (if add succeeds)
             ╰─ FAILURE WINDOW ─╯

Atomic Swap:
  clone_temp() → validate() → swap_dirs() → workspace is UPDATED
                               ╰─ if fails, restore .bak → workspace STILL WORKS
```

The swap pattern ensures the workspace is never in a broken intermediate state.

### `ModuleUpdater` Class Design

```python
@dataclass
class UpdateResult:
    success: bool
    module_name: str
    old_version: Optional[str]
    new_version: Optional[str]
    message: str
    rollback_performed: bool = False

class ModuleUpdater:
    def __init__(self, project_root: Path):
        ...
    
    def update(
        self,
        module_name: str,
        dry_run: bool = False,
        branch: Optional[str] = None,
        keep_backup: bool = False,
    ) -> UpdateResult:
        """Update a module to the latest version via atomic swap."""
```

### Where Does the Git URL Come From?

The module's existing `pyproject.toml` should contain the source URL in `[tool.adhd]` metadata:

```toml
[tool.adhd]
layer = "dev"
source_url = "https://github.com/org/module-name.git"
```

If no `source_url` is recorded, the command should error with a helpful message.

### Edge Cases

| Scenario | Behavior |
|----------|----------|
| No `source_url` in module's pyproject.toml | Error: "Cannot update — no source URL recorded. Re-add with `adhd add <url>`" |
| New version has different package name | Error: "Package name mismatch — expected X, got Y" |
| New version has incompatible layer change | Error: "Layer changed from X to Y — remove and re-add manually" |
| Git clone fails | Error before any modifications (safe) |
| Validation fails | Error before any modifications (safe) |
| uv sync fails after swap | Rollback: restore .bak directory, restore pyproject.toml.bak |
| Module has uncommitted local changes | Warn: "Module has local changes — use --force to overwrite" |

---

## 🔗 Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| `ModuleAdder` (git clone patterns) | ✅ Done | Reuse clone + validation logic |
| `remove_from_root_pyproject()` | ⏳ P0 | Needed for cleanup if pyproject needs patching |
| `ModulesController` | ✅ Done | Module discovery, path resolution |
| `temp_files_manager` | ✅ Done | Temp directory for cloning |
| `workspace_core` | ✅ Done | Workspace regeneration |

---

**← Back to:** [P1 Overview](./_overview.md) · [Module Lifecycle](../_overview.md)
