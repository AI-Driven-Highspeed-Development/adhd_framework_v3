# CLI Commands Reference

> Part of [Module Lifecycle](./_overview.md) · ⏳ [TODO]

---

## 📖 The Story

### 🎯 One-Liner

> Flat CLI naming consistent with `adhd add`: `adhd remove`, `adhd update`, with dry-run and batch support.

---

## 🔧 The Spec

---

## 🎮 Command Reference

### `adhd remove <name>`

Remove an ADHD module from the workspace.

```
Usage: adhd remove <module-name> [options]

Arguments:
  module-name       Name of the module to remove (e.g., "session-manager")

Options:
  --dry-run         Show what would be removed without making changes
  --force           Remove even if other modules depend on this one
  --no-confirm      Skip confirmation prompt (for CI/scripting)
  --keep-dir        Unregister from pyproject.toml but don't delete the directory

Aliases: adhd rm
```

**Examples:**

```bash
# Preview what would happen
adhd remove session-manager --dry-run

# Remove with confirmation
adhd remove session-manager

# Force remove (has dependents)
adhd remove session-manager --force

# CI/scripting (no prompts)
adhd remove session-manager --no-confirm
```

---

### `adhd update <name>`

Update an ADHD module to the latest version from its git source.

```
Usage: adhd update <module-name> [options]

Arguments:
  module-name       Name of the module to update (e.g., "session-manager")

Options:
  --dry-run         Show what would change without making changes
  --no-confirm      Skip confirmation prompt
  --branch <name>   Use a specific git branch (default: default branch)
  --keep-backup     Don't delete .bak directory after successful update

Aliases: adhd up
```

**Examples:**

```bash
# Preview what would change
adhd update session-manager --dry-run

# Update to latest
adhd update session-manager

# Update from specific branch
adhd update session-manager --branch develop
```

---

### `adhd update --layer <layer>`

Batch update all modules in a specific layer.

```
Usage: adhd update --layer <layer> [options]

Arguments:
  --layer <layer>   Layer to update: "dev" or "foundation"
                    NOTE: "runtime" is NOT accepted (project-specific modules)

Options:
  --dry-run         Show what would change for each module
  --no-confirm      Skip confirmation prompt
  --continue-on-error  Don't stop batch on first failure

Aliases: adhd up --layer
```

**Examples:**

```bash
# Preview batch update of all dev modules
adhd update --layer dev --dry-run

# Update all foundation modules
adhd update --layer foundation

# CI: update all dev, don't stop on error
adhd update --layer dev --no-confirm --continue-on-error
```

---

## 📋 CLI Registration

Commands will be registered in `adhd_framework.py`:

```python
command_map = {
    # ... existing commands ...
    'add': self.add_module,
    'a': self.add_module,
    'remove': self.remove_module,     # NEW
    'rm': self.remove_module,         # NEW (alias)
    'update': self.update_module,     # NEW
    'up': self.update_module,         # NEW (alias)
}
```

---

## 🔒 Safety Behavior Summary

| Scenario | Default Behavior |
|----------|-----------------|
| Module has dependents | ❌ Refuse remove — show dependents list, suggest `--force` |
| Remove without `--no-confirm` | Prompt user for confirmation with preview |
| Update fails uv sync | Rollback to backup, report error |
| `--layer runtime` passed | ❌ Reject at controller level with error message |
| Module not found | Error with suggestion (did you mean `X`?) |
| Module has local changes (git) | ⚠️ Warn, require `--force` for update |

---

## [Custom] 📊 Command Comparison

| Aspect | `adhd add` (existing) | `adhd remove` (new) | `adhd update` (new) |
|--------|----------------------|---------------------|---------------------|
| Direction | External → workspace | Workspace → gone | External → workspace (replace) |
| pyproject.toml | Add dep + uv.source | Remove dep + uv.source | No change (swap in-place) |
| Module directory | Create | Delete | Atomic swap |
| Safety check | Duplicate detection | Reverse-dep check | Validate new before swap |
| Rollback | N/A (additive) | N/A (destructive, backup) | .bak directory |

---

**← Back to:** [Module Lifecycle Overview](./_overview.md)
