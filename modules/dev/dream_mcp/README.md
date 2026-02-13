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

### P1 — Extended Tools (Spec Only)

| Command | Description |
|---------|-------------|
| `dream_impact` | Analyze impact of changes on dependent plans |
| `dream_history` | Show history of plan state changes |
| `dream_emergency` | List/manage emergency escalation plans |
| `dream_archive` | Archive completed or abandoned plans |

### P2 — Aspirational Features

| Feature | Description |
|---------|-------------|
| `--hypothetical impact` | Simulate impact without making changes |
| `gaps --proactive` | Proactive gap detection with suggestions |
| Watch mode | Real-time monitoring of day-dream changes |

## Command Roadmap

| Priority | Commands | Status |
|----------|----------|--------|
| **P0** | `status`, `tree`, `stale`, `validate` | Stub signatures |
| **P1** | `impact`, `history`, `emergency`, `archive` | Spec only |
| **P2** | `--hypothetical impact`, `gaps --proactive`, watch mode | Aspirational |

## Notes
- The server uses `FastMCP` from the `mcp` package with stdio transport.
- P0 tools have stub implementations that raise `NotImplementedError`.
- Implementation of actual functionality is tracked as a separate plan.

## Requirements & Prerequisites
- `logger-util` — Logging framework
- `pyyaml` — YAML parsing for frontmatter
- `mcp>=1.1.0` — Model Context Protocol server
