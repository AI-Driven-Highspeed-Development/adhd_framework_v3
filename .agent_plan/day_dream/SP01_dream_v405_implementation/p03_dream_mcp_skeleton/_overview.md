---
name: p03_dream_mcp_skeleton
type: system
magnitude: Trivial
status: DONE
origin: .agent_plan/day_dream/SP01_dream_v405_implementation/_overview.md
last_updated: 2026-02-13
---

# p03 — dream_mcp Module Skeleton

## Purpose

Create the `dream_mcp` module at `modules/dev/dream_mcp/` with proper ADHD module structure. Populate README and module files with the command specification from DREAM v4.05 §13. This phase creates the **skeleton and spec only** — actual P0 command implementation (`status`, `tree`, `stale`, `validate`) is a separate follow-up System Plan.

**Independent:** No dependency on other phases. Can execute at any time.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_create_module_skeleton.md | Task | ✅ [DONE] | Scaffold module via ADHD MCP tools, populate specs |

## Acceptance Criteria

- [x] `modules/dev/dream_mcp/` exists with standard ADHD module structure
- [x] `__init__.py`, `pyproject.toml`, `README.md` present and valid
- [x] `dream_mcp.py` MCP server stub exists with P0 command signatures
- [x] `refresh_full.py` exists (standard MCP module file)
- [x] README documents P0/P1/P2 command roadmap from §13
- [x] Module is importable (no syntax errors)

## Integration Map

Single task — output is the complete `dream_mcp` module scaffold.

## Reading Order

Single task — read `01_create_module_skeleton.md`.
