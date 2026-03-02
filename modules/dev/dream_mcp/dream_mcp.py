"""
dream_mcp - Day-Dream Planning MCP Server

MCP server for ADHD day-dream planning artifact management.
Provides tools for status monitoring, validation, staleness detection,
planning artifact tree generation, impact analysis, module history,
emergency declaration, and plan archival.

Run with: python -m dream_mcp.dream_mcp
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .dream_controller import DreamController

# Create MCP server instance
mcp = FastMCP(
    name="dream_mcp",
    instructions=(
        "Day-dream planning MCP server. "
        "Provides status monitoring, validation, staleness detection, "
        "tree generation, impact analysis, module history, emergency "
        "declaration, and plan archival for ADHD planning artifacts."
    ),
)

# Module-level controller instance (lazy init)
_controller: DreamController | None = None


def _get_controller() -> DreamController:
    """Get or create the DreamController instance."""
    global _controller  # noqa: PLW0603
    if _controller is None:
        _controller = DreamController()
    return _controller


# =============================================================================
# P0 Tools — Implemented
# =============================================================================


@mcp.tool()
def dream_tree(active_only: bool = False) -> dict:
    """Generate _tree.md — annotated folder tree of day-dream directory.

    Creates a visual tree representation of the day-dream directory structure
    with annotations showing plan status from _overview.md frontmatter.
    Writes the result to .agent_plan/day_dream/_tree.md.

    Args:
        active_only: If True, exclude _completed/ and _archive/

    Returns:
        dict with success, tree_path, content, and active_only flag
    """
    return _get_controller().dream_tree(active_only=active_only)


@mcp.tool()
def dream_stale(weeks: int = 4, module: str | None = None) -> dict:
    """Flag module specs where last_updated exceeds staleness threshold.

    Scans modules/*.md spec files across all plan directories and identifies
    those whose last_updated date exceeds the staleness threshold.

    Args:
        weeks: Number of weeks threshold for staleness (default: 4).
            Use weeks=0 to flag all modules as stale.
        module: Optional module name to filter staleness check

    Returns:
        dict with success, stale list, total_scanned, threshold_weeks, report
    """
    return _get_controller().dream_stale(weeks=weeks, module=module)


@mcp.tool()
def dream_status(gaps: bool = False) -> dict:
    """Display current sprint, active/blocked/emergency plans, aggregate warnings.

    Provides a high-level overview of the current planning state including:
    - Active sprint information
    - Emergency plans (ordered by emergency_declared_at)
    - Plans in progress, blocked, or TODO status
    - Aggregate warnings about potential issues
    - Knowledge gap summary (with --gaps for details)

    Args:
        gaps: If True, include knowledge gap analysis in the status report

    Returns:
        dict with success, plans (categorized), summary (counts), report
    """
    return _get_controller().dream_status(gaps=gaps)


@mcp.tool()
def dream_validate(plan: str | None = None) -> dict:
    """Comprehensive gate validation — check all convention enforcement rules.

    Validates planning artifacts against DREAM v4.05 conventions including:
    - Frontmatter schema compliance (required fields, valid types)
    - Status syntax correctness
    - Line limit enforcement
    - Dependency graph integrity (cycles, bidirectional consistency)
    - Conditional field requirements (emergency, invalidation)

    Args:
        plan: Optional specific plan directory name to validate, or None for all

    Returns:
        dict with success, errors, warnings, error_count, warning_count,
        valid (bool), and report (formatted string)
    """
    return _get_controller().dream_validate(plan=plan)


# =============================================================================
# P1 Tools — Advanced Workflows
# =============================================================================


@mcp.tool()
def dream_impact(plan_id: str, modules: bool = False) -> dict:
    """DAG walk showing all plans affected by changes to a given plan.

    Traverses depends_on/blocks relationships to find all direct and
    transitive dependents. Optionally includes affected modules from
    State Delta and Module Index.

    Args:
        plan_id: Plan directory name (e.g. "SP01_dream_v405_implementation")
        modules: If True, also show affected modules

    Returns:
        dict with success, plan_id, direct_dependents, transitive_dependents,
        all_affected, report, and optionally affected_modules
    """
    return _get_controller().dream_impact(plan_id=plan_id, modules=modules)


@mcp.tool()
def dream_history(module_name: str) -> dict:
    """Generate module-indexed change history from State Delta entries.

    Scans State Deltas from root _overview.md and _state_deltas_archive.md
    for entries referencing the given module name, returning a chronological
    change history table.

    Args:
        module_name: Module name to search for (e.g. "dream_mcp")

    Returns:
        dict with success, module, entries list, entry_count, and report
    """
    return _get_controller().dream_history(module_name=module_name)


@mcp.tool()
def dream_emergency(plan_id: str, reason: str) -> dict:
    """Declare emergency priority on a plan.

    Sets priority to emergency, records emergency_declared_at timestamp,
    and updates last_updated in the plan's _overview.md frontmatter.
    Uses atomic write-then-rename pattern for safety.

    Args:
        plan_id: Plan directory name
        reason: Human-readable reason for the emergency declaration

    Returns:
        dict with success, plan_id, emergency_declared_at, reason, message
    """
    return _get_controller().dream_emergency(plan_id=plan_id, reason=reason)


@mcp.tool()
def dream_archive(plan_id: str) -> dict:
    """Move a completed or cut plan to _completed/YYYY-QN/ archive.

    Only works on plans with status DONE or CUT. Creates the _completed/
    and quarter directories as needed.

    Args:
        plan_id: Plan directory name

    Returns:
        dict with success, plan_id, archived_to, message
    """
    return _get_controller().dream_archive(plan_id=plan_id)


def main() -> None:
    """Run the MCP server with stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
