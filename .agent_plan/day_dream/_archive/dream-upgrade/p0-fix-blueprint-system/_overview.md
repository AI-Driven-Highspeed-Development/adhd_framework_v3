# P0: Fix Current Blueprint System

> ✅ **[DONE]** — Fixed the three biggest pain points: estimation, walking skeleton, backward compat.

---

## Purpose

Fix critical friction in the existing blueprint system before adding DREAM integration. These are skill/template text edits — no cross-boundary integration risk, no walking skeleton needed.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| [fix-estimation.md](./fix-estimation.md) | Task | ✅ [DONE] | AI-agent time defaults with `human_only: true` flag |
| [fix-walking-skeleton.md](./fix-walking-skeleton.md) | Task | ✅ [DONE] | Conditional/opt-in — only for cross-boundary integration risk |
| [fix-backward-compat.md](./fix-backward-compat.md) | Task | ✅ [DONE] | Clean-code-first directive, folder-separated compat |

## Integration Map

All three features are independent edits to the `day-dream` SKILL.md. No cross-dependencies between them.

## Reading Order

1. [fix-estimation.md](./fix-estimation.md) — Slot-based estimation scale
2. [fix-walking-skeleton.md](./fix-walking-skeleton.md) — Conditional trigger criteria
3. [fix-backward-compat.md](./fix-backward-compat.md) — Clean-code-first directive
