"""
Output Formatter — Standardized output formatting for DREAM commands.

Formats tree, stale report, status dashboard, validation report, and
other DREAM command outputs into human-readable annotated markdown.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .tree_scanner import PlanNode

# Emoji prefix mapping for plan statuses (DREAM v4.05 §1.8)
_STATUS_EMOJI: dict[str, str] = {
    "TODO": "\u23f3",      # ⏳
    "WIP": "\U0001f504",   # 🔄
    "DONE": "\u2705",      # ✅
    "CUT": "\U0001f6ab",   # 🚫
    "BLOCKED": "\U0001f6a7",  # 🚧
}


def format_tree_markdown(
    root_node: PlanNode,
    day_dream_rel_path: str,
) -> str:
    """Format a PlanNode tree as annotated markdown for ``_tree.md``.

    Args:
        root_node: Root PlanNode from the tree scanner.
        day_dream_rel_path: Relative path to the day-dream directory
            from the workspace root (e.g. ``".agent_plan/day_dream"``).

    Returns:
        Complete ``_tree.md`` content as a string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = [
        "<!-- GENERATED — run 'dream tree' to refresh -->",
        f"<!-- Generated: {now} -->",
        "",
        "# Day Dream — Plan Tree",
        "",
        "```",
        f"{day_dream_rel_path}/",
    ]

    _render_tree_lines(root_node.children, lines, prefix="")

    lines.append("```")
    lines.append("")  # trailing newline

    return "\n".join(lines)


def format_stale_report(
    stale_modules: list[dict[str, Any]],
    weeks: int,
    total_scanned: int,
) -> str:
    """Format the ``dream stale`` report.

    Args:
        stale_modules: List of stale module dicts from the controller.
        weeks: The staleness threshold in weeks.
        total_scanned: Total number of module specs scanned.

    Returns:
        Formatted stale report as a markdown string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = [
        "# Dream Stale Report",
        "",
        (
            f"**Threshold:** {weeks} week(s) | "
            f"**Scanned:** {total_scanned} module spec(s) | "
            f"**Stale:** {len(stale_modules)}"
        ),
        f"**Generated:** {now}",
        "",
    ]

    if not stale_modules:
        lines.append("No stale module specs found.")
    else:
        lines.append("| Module | Last Updated | Plan | Days Stale |")
        lines.append("|--------|-------------|------|------------|")
        for mod in stale_modules:
            lines.append(
                f"| {mod['module']} | {mod['last_updated']} "
                f"| {mod['plan']} | {mod['days_stale']} |"
            )

    lines.append("")
    return "\n".join(lines)


def format_status_dashboard(
    categorized: dict[str, list[dict[str, Any]]],
    summary: dict[str, int],
    knowledge_gaps: list[dict[str, Any]],
    *,
    gaps: bool = False,
) -> str:
    """Format the ``dream status`` dashboard.

    Renders a box-drawing status dashboard following the DREAM v4.05 §13.2
    expected output format: emergencies first, then active, blocked, and
    remaining categories with summary counts.

    Args:
        categorized: Plans categorized by status bucket.
        summary: Summary counts dict.
        knowledge_gaps: List of knowledge gap dicts (plan + gap).
        gaps: Whether to include full knowledge gap details.

    Returns:
        Formatted status dashboard as a string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line_width = 66
    lines: list[str] = []

    lines.append(f"\u250c\u2500 DREAM Status \u2500{'─' * (line_width - 17)}\u2510")
    lines.append(f"\u2502{'':>{line_width}}\u2502")
    lines.append(f"\u2502  Generated: {now:<{line_width - 14}}\u2502")
    lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Emergency section
    emergency = categorized.get("emergency", [])
    if emergency:
        lines.append(f"\u2502  \U0001f6a8 EMERGENCY{'':>{line_width - 14}}\u2502")
        for p in emergency:
            status_display = _format_status_annotation(p["status"])
            name_status = f"  {p['name']:<30}{status_display}"
            lines.append(f"\u2502{name_status:<{line_width}}\u2502")
            declared = p.get("emergency_declared_at", "unknown")
            lines.append(
                f"\u2502    declared: {str(declared):<{line_width - 16}}\u2502"
            )
        lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Active section
    active = categorized.get("active", [])
    if active:
        lines.append(f"\u2502  \U0001f4cb ACTIVE{'':>{line_width - 11}}\u2502")
        for p in active:
            status_display = _format_status_annotation(p["status"])
            deps = p.get("depends_on", [])
            dep_str = f"  depends_on: {', '.join(deps)}" if deps else ""
            name_status = f"  {p['name']:<30}{status_display}{dep_str}"
            lines.append(f"\u2502{name_status:<{line_width}}\u2502")
        lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Blocked section
    blocked = categorized.get("blocked", [])
    if blocked:
        lines.append(f"\u2502  \U0001f6a7 BLOCKED{'':>{line_width - 12}}\u2502")
        for p in blocked:
            status_display = _format_status_annotation(p["status"])
            name_status = f"  {p['name']:<30}{status_display}"
            lines.append(f"\u2502{name_status:<{line_width}}\u2502")
        lines.append(f"\u2502{'':>{line_width}}\u2502")

    # TODO section
    todo = categorized.get("todo", [])
    if todo:
        lines.append(f"\u2502  \u23f3 TODO{'':>{line_width - 9}}\u2502")
        for p in todo:
            status_display = _format_status_annotation(p["status"])
            name_status = f"  {p['name']:<30}{status_display}"
            lines.append(f"\u2502{name_status:<{line_width}}\u2502")
        lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Done section (compact)
    done = categorized.get("done", [])
    if done:
        lines.append(f"\u2502  \u2705 DONE{'':>{line_width - 9}}\u2502")
        for p in done:
            name_line = f"  {p['name']}"
            lines.append(f"\u2502{name_line:<{line_width}}\u2502")
        lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Summary footer
    lines.append(f"\u2502{'':>{line_width}}\u2502")
    gap_count = len(knowledge_gaps)
    gap_line = f"  \U0001f4ca Knowledge Gaps: {gap_count}"
    if not gaps and gap_count > 0:
        gap_line += " (use --gaps for details)"
    lines.append(f"\u2502{gap_line:<{line_width}}\u2502")

    summary_line = (
        f"  \U0001f4ca Total: {summary['total']} | "
        f"Emergency: {summary['emergency']} | "
        f"Active: {summary['active']} | "
        f"Blocked: {summary['blocked']}"
    )
    lines.append(f"\u2502{summary_line:<{line_width}}\u2502")
    lines.append(f"\u2514{'─' * line_width}\u2518")

    # Knowledge gap details (if requested)
    if gaps and knowledge_gaps:
        lines.append("")
        lines.append("### Knowledge Gaps")
        lines.append("")
        for g in knowledge_gaps:
            lines.append(f"- **{g['plan']}**: {g['gap']}")

    lines.append("")
    return "\n".join(lines)


def format_validation_report(
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]],
) -> str:
    """Format the ``dream validate`` report.

    Renders a structured validation report with ERROR and WARNING
    categories, each issue showing plan name, check type, and message.

    Args:
        errors: List of ERROR-level issue dicts.
        warnings: List of WARNING-level issue dicts.

    Returns:
        Formatted validation report as a markdown string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    error_count = len(errors)
    warning_count = len(warnings)
    status = "PASS" if error_count == 0 else "FAIL"

    lines: list[str] = [
        "# Dream Validate Report",
        "",
        (
            f"**Status:** {status} | "
            f"**Errors:** {error_count} | "
            f"**Warnings:** {warning_count}"
        ),
        f"**Generated:** {now}",
        "",
    ]

    if error_count == 0 and warning_count == 0:
        lines.append("All checks passed. No issues found.")
        lines.append("")
        return "\n".join(lines)

    if errors:
        lines.append("## ❌ ERRORS (block closure)")
        lines.append("")
        for i, err in enumerate(errors, 1):
            lines.append(
                f"{i}. **[{err['check']}]** {err['plan']}: {err['message']}"
            )
        lines.append("")

    if warnings:
        lines.append("## ⚠️ WARNINGS (should fix)")
        lines.append("")
        for i, warn in enumerate(warnings, 1):
            lines.append(
                f"{i}. **[{warn['check']}]** {warn['plan']}: {warn['message']}"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _format_status_annotation(status: str) -> str:
    """Build the inline status annotation for a tree entry.

    Args:
        status: Raw status string from frontmatter
            (e.g. ``"WIP"``, ``"BLOCKED:waiting-on-api"``).

    Returns:
        Formatted annotation like ``"  🔄 [WIP]"`` or ``"  🚧 [BLOCKED:reason]"``.
    """
    base = status.split(":")[0]
    emoji = _STATUS_EMOJI.get(base, "")

    if emoji:
        return f"  {emoji} [{status}]"
    return f"  [{status}]"


def _render_tree_lines(
    nodes: list[PlanNode],
    lines: list[str],
    prefix: str,
) -> None:
    """Recursively render tree lines with box-drawing characters.

    Args:
        nodes: Child nodes to render.
        lines: Accumulator for output lines.
        prefix: Current indentation prefix for this depth level.
    """
    for i, node in enumerate(nodes):
        is_last = i == len(nodes) - 1
        connector = "\u2514\u2500\u2500 " if is_last else "\u251c\u2500\u2500 "

        display = node.name
        if node.is_dir:
            display += "/"

        annotation = _format_status_annotation(node.status) if node.status else ""

        lines.append(f"{prefix}{connector}{display}{annotation}")

        if node.is_dir and node.children:
            extension = "    " if is_last else "\u2502   "
            _render_tree_lines(node.children, lines, prefix + extension)


# ---------------------------------------------------------------------------
# Impact report formatter
# ---------------------------------------------------------------------------


def format_impact_report(
    *,
    plan_id: str,
    direct_dependents: list[dict[str, Any]],
    transitive_dependents: list[dict[str, Any]],
    affected_modules: list[dict[str, Any]],
    all_affected: list[str],
    show_modules: bool = False,
) -> str:
    """Format the ``dream impact`` report.

    Renders a box-drawing impact analysis report following the
    DREAM v4.05 §13.3 expected output format.

    Args:
        plan_id: The plan being analyzed.
        direct_dependents: List of plan summary dicts for direct dependents.
        transitive_dependents: List of plan summary dicts for transitive dependents.
        affected_modules: List of affected module dicts (if ``show_modules``).
        all_affected: Flat list of all affected plan names.
        show_modules: Whether to include module section.

    Returns:
        Formatted impact report as a string.
    """
    line_width = 66
    lines: list[str] = []

    lines.append(
        f"\u250c\u2500 Impact Analysis: {plan_id} "
        f"\u2500{'─' * max(1, line_width - 22 - len(plan_id))}\u2510"
    )
    lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Direct dependents section
    lines.append(f"\u2502  DIRECT DEPENDENTS (blocks:){'':>{line_width - 30}}\u2502")
    if direct_dependents:
        for p in direct_dependents:
            status_annotation = _format_status_annotation(p.get("status", ""))
            dep_info = f"  depends_on: {plan_id}"
            entry = f"  \u2514\u2500\u2500 {p['name']:<24}{status_annotation}{dep_info}"
            lines.append(f"\u2502{entry:<{line_width}}\u2502")
    else:
        lines.append(f"\u2502  (none){'':>{line_width - 9}}\u2502")
    lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Transitive dependents section
    lines.append(f"\u2502  TRANSITIVE DEPENDENTS{'':>{line_width - 24}}\u2502")
    if transitive_dependents:
        for p in transitive_dependents:
            status_annotation = _format_status_annotation(p.get("status", ""))
            deps = p.get("depends_on", [])
            dep_str = f"  depends_on: {', '.join(deps)}" if deps else ""
            entry = f"  \u2514\u2500\u2500 {p['name']:<24}{status_annotation}{dep_str}"
            lines.append(f"\u2502{entry:<{line_width}}\u2502")
    else:
        lines.append(f"\u2502  (none){'':>{line_width - 9}}\u2502")
    lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Affected modules section (optional)
    if show_modules:
        lines.append(f"\u2502  MODULES AFFECTED{'':>{line_width - 19}}\u2502")
        if affected_modules:
            for m in affected_modules:
                entry = f"  \u2514\u2500\u2500 {m['module']:<24}Origin: {m['origin']}"
                lines.append(f"\u2502{entry:<{line_width}}\u2502")
                modified = m.get("modified_by", [])
                if modified:
                    mod_str = f"      Modified by: {', '.join(str(x) for x in modified)}"
                    lines.append(f"\u2502{mod_str:<{line_width}}\u2502")
        else:
            lines.append(f"\u2502  (none){'':>{line_width - 9}}\u2502")
        lines.append(f"\u2502{'':>{line_width}}\u2502")

    # Invalidation warning
    if all_affected:
        warn_line = f"  \u26a0\ufe0f  Changing {plan_id} may invalidate: {', '.join(all_affected)}"
        lines.append(f"\u2502{warn_line:<{line_width}}\u2502")

    lines.append(f"\u2514{'─' * line_width}\u2518")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# History report formatter
# ---------------------------------------------------------------------------


def format_history_report(
    module_name: str,
    entries: list[dict[str, str]],
) -> str:
    """Format the ``dream history`` report.

    Renders a module-indexed change history table per DREAM v4.05 §5.

    Args:
        module_name: The module name being queried.
        entries: List of dicts with ``date``, ``plan``, ``change`` keys.

    Returns:
        Formatted history report as a markdown string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = [
        f"## Module History — {module_name} (auto-generated)",
        "",
        f"**Generated:** {now}",
        "",
    ]

    if not entries:
        lines.append(f"No State Delta entries found for module '{module_name}'.")
        lines.append("")
        return "\n".join(lines)

    lines.append("| Date | Plan | Change |")
    lines.append("|------|------|--------|")
    for entry in entries:
        lines.append(
            f"| {entry['date']} | {entry['plan']} | {entry['change']} |"
        )

    lines.append("")
    return "\n".join(lines)