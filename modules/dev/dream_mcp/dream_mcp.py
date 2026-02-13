"""
dream_mcp - Day-Dream Planning MCP Server

MCP server for ADHD day-dream planning artifact management.
Provides tools for status monitoring, validation, staleness detection,
and planning artifact tree generation.

Run with: python -m dream_mcp.dream_mcp
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP(
    name="dream_mcp",
    instructions=(
        "Day-dream planning MCP server. "
        "Provides status monitoring, validation, staleness detection, "
        "and tree generation for ADHD planning artifacts."
    ),
)


# =============================================================================
# P0 Tools — Core functionality (stubs)
# =============================================================================


@mcp.tool()
def dream_status(gaps: bool = False) -> str:
    """Display current sprint, active/blocked/emergency plans, aggregate warnings.

    Provides a high-level overview of the current planning state including:
    - Active sprint information
    - Plans in progress, blocked, or emergency status
    - Aggregate warnings about potential issues

    Args:
        gaps: If True, include knowledge gap analysis in the status report

    Returns:
        Formatted status report as string
    """
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")


@mcp.tool()
def dream_tree(active_only: bool = False) -> str:
    """Generate _tree.md — annotated folder tree of day-dream directory.

    Creates a visual tree representation of the day-dream directory structure
    with annotations showing plan status, priorities, and relationships.

    Args:
        active_only: If True, only include active (non-archived) plans in the tree

    Returns:
        Annotated tree structure as markdown string
    """
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")


@mcp.tool()
def dream_stale(weeks: int = 4, module: str | None = None) -> str:
    """Flag module specs where last_updated exceeds staleness threshold.

    Scans planning artifacts to identify stale specifications that may need
    review or updates based on their last modification date.

    Args:
        weeks: Number of weeks threshold for staleness (default: 4)
        module: Optional module name to filter staleness check

    Returns:
        Report of stale artifacts as formatted string
    """
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")


@mcp.tool()
def dream_validate(plan: str | None = None) -> str:
    """Comprehensive gate validation — check all convention enforcement rules.

    Validates planning artifacts against ADHD framework conventions including:
    - Frontmatter schema compliance
    - Status syntax correctness
    - Dependency graph integrity
    - Naming conventions

    Args:
        plan: Optional specific plan path to validate, or None for all plans

    Returns:
        Validation report with pass/fail status and details
    """
    raise NotImplementedError("SP01 skeleton — implementation is separate plan")


# =============================================================================
# Entry point
# =============================================================================


def main() -> None:
    """Run the MCP server with stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
