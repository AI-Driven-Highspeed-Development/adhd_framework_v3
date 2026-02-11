# P1: Core Commands

> ⏳ **[TODO]** — Implement `adhd remove` and `adhd update` commands with safety features.

---

## Purpose

Build the main remove and update commands that users interact with. Remove is the reverse of add — unregister, delete, sync. Update uses an atomic swap pattern to avoid the failure window of naive remove+re-add. Safety features (dry-run, backup, confirmation) are integrated from the start.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| [remove-command.md](./remove-command.md) | Task | ⏳ [TODO] | `adhd remove <name>` — full cleanup with safety checks |
| [update-command.md](./update-command.md) | Task | ⏳ [TODO] | `adhd update <name>` — atomic swap pattern |
| [safety-features.md](./safety-features.md) | Task | ⏳ [TODO] | Dry-run preview, lightweight backup, confirmation |

## Integration Map

```mermaid
flowchart LR
    SAFETY[safety-features.md] --> RM[remove-command.md]
    SAFETY --> UP[update-command.md]
    RM --> UP
```

Safety features are consumed by both commands. Remove is a dependency of update (update uses remove's unregister logic internally for the old version swap-out).

## Reading Order

1. [safety-features.md](./safety-features.md) — Cross-cutting safety patterns
2. [remove-command.md](./remove-command.md) — Remove command
3. [update-command.md](./update-command.md) — Update command (builds on remove)
