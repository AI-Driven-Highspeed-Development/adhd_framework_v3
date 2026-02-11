# Executive Summary

> Part of [Module Lifecycle](./_overview.md) · ⏳ [TODO]

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌──────────────────────────────────────────────────────────────────┐
│  Developer adds a module  ──►  ✅ adhd add works great!          │
│                                                                  │
│  Developer wants to REMOVE it  ──►  💥 MANUAL HELL               │
│    1. Edit pyproject.toml (remove dependency)                    │
│    2. Edit pyproject.toml (remove uv.sources entry)              │
│    3. Delete module directory                                    │
│    4. Run uv sync                                                │
│    5. Regenerate workspace (adhd workspace)                      │
│    6. Hope you didn't break anything that depends on it          │
│                                                                  │
│  Developer wants to UPDATE it  ──►  💥 EVEN WORSE                │
│    1. Remove the old version (all steps above)                   │
│    2. Add the new version (adhd add again)                       │
│    3. Pray nothing broke in between                              │
│    4. If remove failed halfway, workspace is corrupted           │
└──────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Developers managing modules | 🔥🔥🔥 High | Every module change |
| CI/CD pipelines | 🔥🔥 Medium | Module version bumps |
| New contributors | 🔥🔥🔥 High | Afraid to touch modules |

### ✨ The Vision

```
After Module Lifecycle:
┌──────────────────────────────────────────────────────────────────┐
│  adhd remove my-module                                           │
│    → checks reverse deps → dry-run preview → confirmation        │
│    → unregisters pyproject.toml → removes uv.sources             │
│    → deletes directory → uv sync → workspace regen               │
│    → ✅ Done in one command                                      │
│                                                                  │
│  adhd update my-module                                           │
│    → clones new version to temp → validates it                   │
│    → backs up pyproject.toml → atomic swap → uv sync             │
│    → ✅ Done, with rollback on failure                           │
│                                                                  │
│  adhd update --layer dev                                         │
│    → updates ALL dev modules in one batch                        │
│    → ✅ Batch operations for power users                         │
└──────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Complete the module lifecycle with safe `remove` and atomic-swap `update` commands, including reverse-dep safety checks and batch operations.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Remove a module | ❌ 6+ manual steps, error-prone | ✅ Single command with safety checks |
| Update a module | ❌ Remove + re-add with failure window | ✅ Atomic swap, rollback on failure |
| Reverse dep check | ❌ None — can break dependents silently | ✅ Warns before removing depended-on modules |
| Batch operations | ❌ Update modules one-by-one | ✅ `adhd update --layer dev` |

---

## 🔧 The Spec

---

## 🌟 TL;DR

Add `adhd remove` and `adhd update` commands that safely undo what `adhd add` does. Remove uses reverse-dep checking and cleanup automation. Update uses an atomic swap pattern (clone → validate → swap) instead of naive remove+re-add. Batch update supports `--layer` flag for bulk operations.

---

## 🎯 Problem Statement

The ADHD Framework's `adhd add` command brings external modules into a workspace, but there is no inverse operation. Removing a module requires 6+ manual steps across multiple files, and updating requires a risky remove-then-add sequence with a failure window where the workspace is broken. This plan adds the missing lifecycle operations with safety features (reverse-dep checking, dry-run preview, lightweight backup, atomic swap for updates).

---

## 🔍 Prior Art & Existing Solutions

| Tool | What It Does | Decision | Rationale |
|------|--------------|----------|-----------|
| `adhd add` (internal) | Adds modules from git repos | WRAP | Extend `module_lifecycle_core` with reverse operations |
| `pyproject_patcher` (internal) | String-manipulation pyproject.toml patching | BUILD | Add `remove_from_root_pyproject()` — reverse of existing `add_to_root_pyproject()` |
| `DependencyWalker` (internal) | Forward dependency traversal | BUILD | Add `get_reverse_deps()` for safety checks |
| `uv remove` (uv CLI) | Removes packages from uv workspace | REJECT | Doesn't understand ADHD module structure |
| `pip uninstall` | Package uninstall | REJECT | Wrong abstraction level |

**Summary:** Build on existing internals (`module_lifecycle_core`, `pyproject_patcher`, `DependencyWalker`) by adding reverse operations. No external dependencies needed.

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Rename `module_adder_core` → `module_lifecycle_core` | Completed — rename applied across entire project |
| `adhd update --all` (update everything at once) | Too dangerous without per-module validation |
| `--layer runtime` for batch update | Runtime modules are project-specific, batch update of generic infra only |
| Git submodule management | Modules are copied, not submoduled |
| Version pinning / lockfile | Future feature — this plan handles current HEAD |
| `init.yaml` operations | init.yaml is legacy — excluded from all operations |
| Automatic migration of module data | Module data directories are user-managed |

---

## ✅ Features Overview

| Priority | Feature | Difficulty | Status | Description |
|----------|---------|------------|--------|-------------|
| P0 | [Reverse Dep Lookup](./p00_prerequisites/02_reverse_dep_lookup.md) | `[KNOWN]` | ⏳ [TODO] | Add `get_reverse_deps()` to `DependencyWalker` |
| P0 | [Pyproject Patcher Remove](./p00_prerequisites/01_pyproject_patcher_remove.md) | `[KNOWN]` | ⏳ [TODO] | Add `remove_from_root_pyproject()` to `pyproject_patcher` |
| P1 | [Remove Command](./p01_core_commands/01_remove_command.md) | `[KNOWN]` | ⏳ [TODO] | `adhd remove <name>` with full cleanup |
| P1 | [Update Command](./p01_core_commands/03_update_command.md) | `[KNOWN]` | ⏳ [TODO] | `adhd update <name>` with atomic swap pattern |
| P1 | [Safety Features](./p01_core_commands/02_safety_features.md) | `[KNOWN]` | ⏳ [TODO] | Dry-run preview, lightweight backup, confirmation |
| P2 | [Batch Update](./p02_batch_operations/01_batch_update_command.md) | `[KNOWN]` | ⏳ [TODO] | `adhd update --layer dev\|foundation` |

---

## [Custom] 🎯 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Swap pattern for update** (not remove+re-add) | Avoids failure window where workspace is broken between remove and add |
| **Reverse-dep check as P0 prerequisite** | Must exist before remove can be safe — foundational capability |
| **Flat CLI naming** (`adhd remove`, not `adhd module remove`) | Consistent with `adhd add`, minimal typing |
| **`--layer` for batch, not `--all`** | Explicit is safer; runtime modules are project-specific |
| **Extend `module_lifecycle_core`, don't rename** | Functional value now > cosmetic rename risk |
| **`init.yaml` excluded** | Legacy mechanism — not part of any new operations |
| **Controller-level `--layer runtime` guard** | Reject at controller, not just CLI — defense in depth |

---

**← Back to:** [Module Lifecycle Overview](./_overview.md)
