---
module: dream_mcp
last_updated: 2026-02-13
modified_by_plans:
  - SP01_dream_v405_implementation
knowledge_gaps: []
---

# Module Spec — dream_mcp

## Current State

**Created.** Module skeleton exists at `modules/dev/dream_mcp/` with P0 tool stubs. Commands raise `NotImplementedError` — implementation is p04/p05.

## Target State (This Plan — Skeleton Only)

Module skeleton at `modules/dev/dream_mcp/` with:
- Standard ADHD MCP module structure (`__init__.py`, `pyproject.toml`, `README.md`, `dream_mcp.py`, `refresh.py`)
- P0 tool signatures as `NotImplementedError` stubs (`status`, `tree`, `stale`, `validate`)
- README documenting full P0/P1/P2 command roadmap
- Importable but non-functional

## Target State (Follow-up Plan — P0 Implementation)

Separate System Plan will implement P0 commands:
- `dream status` — display sprint, active/blocked/emergency plans
- `dream tree` — generate `_tree.md` annotated folder tree
- `dream stale` — flag modules with stale `last_updated`
- `dream validate` — comprehensive gate validation

P1/P2 commands (`impact`, `history`, `emergency`, `archive`, `--hypothetical`, `gaps --proactive`) are further follow-up work.

## Design Properties (from §13.1)

| Property | Detail |
|----------|--------|
| Read-only | Validates but NEVER mutates (exceptions: `tree`, `archive`, `emergency`) |
| Deterministic | Same input → same output |
| MCP server | Exposes tools for agent consumption via MCP protocol |
| Layer | `dev` |

## Modified By This Plan

Phase: p03_dream_mcp_skeleton, Task: 01_create_module_skeleton.md
