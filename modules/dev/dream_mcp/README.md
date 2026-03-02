# Dream MCP

Day-dream planning artifact management MCP server for ADHD Framework.

## Overview
- Provides tools for status monitoring, validation, and maintenance of day-dream planning artifacts
- Designed to support ADHD planning workflows with status, tree, staleness, and validation tools
- Integrates with `.agent_plan/day_dream/` directory structure

## Features
- **Status monitoring** – `dream_status` shows current sprint, active/blocked plans, warnings
- **Tree generation** – `dream_tree` creates annotated folder tree of day-dream directory
- **Staleness detection** – `dream_stale` flags module specs exceeding staleness threshold
- **Validation** – `dream_validate` checks convention enforcement rules

## Quickstart

```bash
# Run the MCP server
python -m dream_mcp.dream_mcp
```

```python
# Tool usage examples (called via MCP protocol)
dream_status()
dream_status(gaps=True)
dream_tree()
dream_tree(active_only=True)
dream_stale(weeks=4)
dream_stale(weeks=2, module="config_manager")
dream_validate()
dream_validate(plan=".agent_plan/day_dream/vision_001/")
```

## API

### P0 — Core Tools (Implemented)

```python
@mcp.tool()
def dream_status(gaps: bool = False) -> str:
    """Display current sprint, active/blocked/emergency plans, aggregate warnings."""
    ...

@mcp.tool()
def dream_tree(active_only: bool = False) -> str:
    """Generate _tree.md — annotated folder tree of day-dream directory."""
    ...

@mcp.tool()
def dream_stale(weeks: int = 4, module: str | None = None) -> str:
    """Flag module specs where last_updated exceeds staleness threshold."""
    ...

@mcp.tool()
def dream_validate(plan: str | None = None) -> str:
    """Comprehensive gate validation — check all convention enforcement rules."""
    ...
```

### P1 — Extended Tools (Implemented)

| Command | Description |
|---------|-------------|
| `dream_impact` | BFS-based DAG walk showing transitive dependents + affected modules |
| `dream_history` | Module-indexed change history from State Delta entries |
| `dream_emergency` | Declare emergency priority on a plan (atomic write-then-rename) |
| `dream_archive` | Move DONE/CUT plans to `_completed/YYYY-QN/` |

### P2 — Aspirational Features

| Feature | Description |
|---------|-------------|
| `--hypothetical impact` | Simulate impact without making changes |
| `gaps --proactive` | Proactive gap detection with suggestions |
| Watch mode | Real-time monitoring of day-dream changes |

## Command Roadmap

| Priority | Commands | Status |
|----------|----------|--------|
| **P0** | `status`, `tree`, `stale`, `validate` | Implemented |
| **P1** | `impact`, `history`, `emergency`, `archive` | Implemented |
| **P2** | `--hypothetical impact`, `gaps --proactive`, watch mode | Aspirational |

## Notes
- The server uses `FastMCP` from the `mcp` package with stdio transport.
- P0 and P1 tools are fully implemented via `dream_controller.py` (business logic) with `dream_mcp.py` as thin MCP wrapper.
- Supporting modules: `frontmatter_parser.py`, `tree_scanner.py`, `output_formatter.py`.
- P2 intelligence layer is aspirational and not yet implemented.

## Requirements & Prerequisites
- `logger-util` — Logging framework
- `pyyaml` — YAML parsing for frontmatter
- `mcp>=1.1.0` — Model Context Protocol server
