# P2: Batch Operations

> ⏳ **[TODO]** — Add `--layer` flag to `adhd update` for batch module updates.

---

## Purpose

After single-module remove and update commands are working (P1), add batch update capability so users can update all modules in a layer with one command. Includes controller-level runtime layer exclusion and per-module error handling.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| [batch-update-command.md](./batch-update-command.md) | Task | ⏳ [TODO] | `adhd update --layer dev\|foundation` with safety guards |

## Integration Map

Single child — no internal dependencies. Depends on P1's `ModuleUpdater.update()` for per-module execution.

## Reading Order

1. [batch-update-command.md](./batch-update-command.md) — Batch update with `--layer` flag
