---
name: p04_parsing_and_simple_commands
type: system
magnitude: Standard
status: TODO
origin: .agent_plan/day_dream/DREAM_v4.05.md
last_updated: 2026-02-13
depends_on:
  - p03_dream_mcp_skeleton
---

# p04 — P0: Parsing Infrastructure & Simple Commands

## Purpose

Build the shared parsing layer that all `dream_mcp` commands depend on, then implement the two simplest P0 commands (`dream tree`, `dream stale`). This phase delivers working filesystem reads before tackling the heavier `status` and `validate` commands.

## Children

| Name | Type | Magnitude | Status | Description |
|------|------|-----------|--------|-------------|
| 01_shared_parsing_infrastructure.md | Task | Light | ⏳ [TODO] | YAML frontmatter parser, plan tree scanner, output formatter |
| 02_dream_tree_command.md | Task | Light | ⏳ [TODO] | Implement `dream tree` — annotated folder tree generator |
| 03_dream_stale_command.md | Task | Trivial | ⏳ [TODO] | Implement `dream stale` — module staleness detection |

## Integration Map

```
01_shared_parsing ──► 02_dream_tree (uses scanner + formatter)
                  └─► 03_dream_stale (uses frontmatter parser)
```

Task 01 produces the shared library; tasks 02 and 03 consume it (parallel-safe with each other).

## Reading Order

1. 01_shared_parsing_infrastructure.md — prerequisite for both commands
2. 02_dream_tree_command.md — parallel-safe with 03
3. 03_dream_stale_command.md — parallel-safe with 02
