# Feature: Safety Features

> Part of [P1: Core Commands](./_overview.md) · ⏳ [TODO]

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  Manual module removal:        │  Every lifecycle command has:  │
│  • No preview of consequences  │  • --dry-run preview           │
│  • No backup before changes    │  • Lightweight backup          │
│  • No confirmation prompt      │  • Confirmation prompt         │
│  • No rollback on failure      │  • Rollback on failure         │
│       ↓                        │       ↓                        │
│  💥 Mistakes are permanent     │  ✅ Mistakes are recoverable   │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Cross-cutting safety patterns shared by remove and update: dry-run preview, lightweight backup, confirmation prompt, and rollback on failure.

---

## 🔧 The Spec

**Priority:** P1 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Dry-run mode for both remove and update
- Lightweight backup for update (pyproject.toml + module dir → .bak)
- Confirmation prompt with preview (skippable via `--no-confirm`)
- Rollback logic for update failures

**Out of Scope:**
- Full workspace backup (use git for that)
- Undo command (use git)
- Backup rotation / history

---

## ✅ Acceptance Criteria

- [ ] `--dry-run` for remove shows: files to delete, pyproject changes, reverse deps
- [ ] `--dry-run` for update shows: files to replace, version diff
- [ ] Confirmation prompt shows action summary before proceeding
- [ ] `--no-confirm` skips prompt
- [ ] Update creates .bak before swap, restores on failure
- [ ] .bak is cleaned up on success (unless `--keep-backup`)

---

## 🛠️ Technical Notes

### Dry-Run Output Format

```
$ adhd remove session-manager --dry-run

🔍 Dry-run: adhd remove session-manager

  Module:    session-manager
  Layer:     runtime
  Path:      modules/runtime/session_manager/
  
  Changes:
    ✂️  Remove "session-manager" from pyproject.toml dependencies
    ✂️  Remove session-manager = { workspace = true } from [tool.uv.sources]
    🗑️  Delete modules/runtime/session_manager/ (14 files)
    🔄  Run uv sync
    🔄  Regenerate .code-workspace
  
  ⚠️  Reverse dependencies: auth-manager, api-gateway
      Use --force to remove anyway.
  
  No changes made (dry-run mode).
```

### Backup Strategy (Lightweight)

| What | How | When Restored |
|------|-----|---------------|
| `pyproject.toml` | Copy → `pyproject.toml.bak` | If uv sync fails after update |
| Module directory | Move → `{name}.bak/` | If uv sync fails after swap |
| `.code-workspace` | Not backed up | Regenerated via `adhd workspace` |

**Why lightweight:** Full backups are git's job. We only need enough to rollback a failed atomic swap.

### Confirmation Prompt

```
$ adhd remove session-manager

  About to remove: session-manager (runtime)
  This will delete 14 files in modules/runtime/session_manager/
  
  Continue? [y/N]: 
```

For update:
```
$ adhd update session-manager

  About to update: session-manager (runtime)
  Source: https://github.com/org/session-manager.git
  Current: abc1234 → Latest: def5678
  
  Continue? [y/N]: 
```

---

## 🔗 Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| `get_reverse_deps()` | ⏳ P0 | Needed for dry-run reverse dep display |
| `ModulesController` | ✅ Done | Module info for preview |

---

**← Back to:** [P1 Overview](./_overview.md) · [Module Lifecycle](../_overview.md)
