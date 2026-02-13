---
task: p03_01
title: Create dream_mcp Module Skeleton
status: DONE
difficulty: "[KNOWN]"
---

# Create dream_mcp Module Skeleton

## Scope

Create the `dream_mcp` module at `modules/dev/dream_mcp/` with proper ADHD module structure. Populate with P0/P1/P2 command specifications from DREAM v4.05 §13. This task creates the **skeleton and spec only** — actual command implementation is a separate follow-up System Plan.

## Specific Changes

| # | Action | Detail |
|---|--------|--------|
| 1 | Create module via `adhd_mcp create_module` | name: `dream_mcp`, layer: `dev`, is_mcp: `true` |
| 2 | Populate `README.md` | Module purpose, command reference (P0/P1/P2), design properties |
| 3 | Populate `dream_mcp.py` | MCP server stub with P0 tool signatures (no implementation) |
| 4 | Verify `__init__.py` | Standard ADHD module init |
| 5 | Verify `pyproject.toml` | Dependencies: `pyyaml` (for frontmatter parsing) |
| 6 | Verify `refresh.py` | Standard MCP refresh script |

### P0 Command Stubs (from §13.2)

```python
# dream_mcp.py — tool signatures only, implementation TBD
@mcp_tool
def dream_status(gaps: bool = False) -> str:
    """Display current sprint, active/blocked/emergency plans, aggregate warnings."""
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")

@mcp_tool
def dream_tree(active_only: bool = False) -> str:
    """Generate _tree.md — annotated folder tree of day-dream directory."""
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")

@mcp_tool
def dream_stale(weeks: int = 4, module: str | None = None) -> str:
    """Flag module specs where last_updated exceeds staleness threshold."""
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")

@mcp_tool
def dream_validate(plan: str | None = None) -> str:
    """Comprehensive gate validation — check all convention enforcement rules."""
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")
```

### README Command Reference Outline

| Priority | Commands | Status |
|----------|----------|--------|
| P0 | `status`, `tree`, `stale`, `validate` | Stub signatures |
| P1 | `impact`, `history`, `emergency`, `archive` | Spec only in README |
| P2 | `--hypothetical impact`, `gaps --proactive`, watch mode | Aspirational in README |

## How to Verify (Manual)

1. `ls modules/dev/dream_mcp/` — should show `__init__.py`, `dream_mcp.py`, `refresh.py`, `pyproject.toml`, `README.md`
2. `python -c "import modules.dev.dream_mcp"` — should not error (importable skeleton)
3. Open `README.md` — should document all P0/P1/P2 commands

## Acceptance Criteria

- [x] Module directory exists at `modules/dev/dream_mcp/`
- [x] All standard ADHD MCP module files present
- [x] `dream_mcp.py` has P0 tool signatures with `NotImplementedError` stubs
- [x] `README.md` documents full command roadmap (P0/P1/P2)
- [x] Module is importable without errors
- [x] `pyproject.toml` has correct metadata and dependencies
