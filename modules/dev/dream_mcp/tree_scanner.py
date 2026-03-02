"""
Tree Scanner — Directory tree scanner for DREAM planning artifacts.

Scans the day-dream directory structure, reads plan metadata from
``_overview.md`` frontmatter, and builds an annotated tree representation.
Also provides module spec scanning for staleness detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from logger_util import Logger

from .frontmatter_parser import parse_frontmatter_file

_logger = Logger(name="dream_mcp.tree_scanner")

# Directories excluded when active_only=True (per DREAM v4.05 §10.6)
_INACTIVE_DIRS: frozenset[str] = frozenset({"_completed", "_archive"})

# Items always skipped in tree scans (internal/generated artifacts)
_SKIP_ITEMS: frozenset[str] = frozenset({"__pycache__", ".DS_Store"})


@dataclass
class PlanNode:
    """A node in the plan directory tree.

    Attributes:
        name: File or directory name.
        path: Absolute path to this node.
        is_dir: Whether this node is a directory.
        frontmatter: Parsed frontmatter from _overview.md (directories only).
        children: Child nodes (directories only).
        status: Plan status extracted from frontmatter, if present.
    """

    name: str
    path: Path
    is_dir: bool
    frontmatter: dict[str, Any] | None = None
    children: list[PlanNode] = field(default_factory=list)
    status: str | None = None


def scan_plan_tree(
    day_dream_root: Path,
    *,
    active_only: bool = False,
) -> PlanNode:
    """Scan the day-dream directory tree and build a PlanNode tree.

    Args:
        day_dream_root: Absolute path to the day-dream directory.
        active_only: If True, exclude ``_completed/`` and
            ``_archive/`` directories.

    Returns:
        Root PlanNode representing the day-dream directory.
    """
    return _scan_dir(day_dream_root, active_only=active_only)


def scan_module_specs(day_dream_root: Path) -> list[dict[str, Any]]:
    """Scan all module spec files across plan directories.

    Finds ``modules/*.md`` files in plan directories (directories containing
    ``_overview.md``) and parses their frontmatter for staleness detection.

    Args:
        day_dream_root: Absolute path to the day-dream directory.

    Returns:
        List of dicts with module spec info::

            {"module": str, "path": Path, "last_updated": Any,
             "plan": str, "modified_by_plans": list, "knowledge_gaps": list}
    """
    results: list[dict[str, Any]] = []

    for modules_dir in sorted(day_dream_root.rglob("modules")):
        if not modules_dir.is_dir():
            continue

        # Only consider modules/ subdirectories of actual plan directories
        parent = modules_dir.parent
        if not (parent / "_overview.md").exists():
            continue

        for spec_file in sorted(modules_dir.glob("*.md")):
            frontmatter = parse_frontmatter_file(spec_file)
            if frontmatter is None:
                _logger.debug(f"No frontmatter in module spec: {spec_file}")
                continue

            results.append({
                "module": frontmatter.get("module", spec_file.stem),
                "path": spec_file,
                "last_updated": frontmatter.get("last_updated"),
                "plan": parent.name,
                "modified_by_plans": frontmatter.get("modified_by_plans", []),
                "knowledge_gaps": frontmatter.get("knowledge_gaps", []),
            })

    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _scan_dir(dir_path: Path, *, active_only: bool) -> PlanNode:
    """Recursively scan a directory and build a PlanNode.

    Args:
        dir_path: Directory to scan.
        active_only: If True, skip inactive directories.

    Returns:
        PlanNode for this directory with children populated.
    """
    overview_path = dir_path / "_overview.md"
    frontmatter = parse_frontmatter_file(overview_path)
    status = _extract_status(frontmatter) if frontmatter else None

    node = PlanNode(
        name=dir_path.name,
        path=dir_path,
        is_dir=True,
        frontmatter=frontmatter,
        status=status,
    )

    try:
        entries = sorted(dir_path.iterdir(), key=_sort_key)
    except PermissionError:
        _logger.debug(f"Permission denied scanning: {dir_path}")
        return node

    for entry in entries:
        if entry.name in _SKIP_ITEMS:
            continue
        if entry.name.startswith("."):
            continue

        if entry.is_dir():
            if active_only and entry.name in _INACTIVE_DIRS:
                continue
            child = _scan_dir(entry, active_only=active_only)
            node.children.append(child)
        else:
            node.children.append(
                PlanNode(name=entry.name, path=entry, is_dir=False)
            )

    return node


def _extract_status(frontmatter: dict[str, Any]) -> str | None:
    """Extract the status value from frontmatter.

    Args:
        frontmatter: Parsed YAML frontmatter dict.

    Returns:
        Status string (e.g., ``"WIP"``, ``"TODO"``, ``"DONE"``)
        or None if absent.
    """
    value = frontmatter.get("status")
    if isinstance(value, str):
        return value
    return None


def _sort_key(entry: Path) -> tuple[int, str]:
    """Sort key for directory entries: files first, then directories.

    Within each group entries are sorted alphabetically (case-insensitive).
    This matches the DREAM convention of listing documentation files
    before phase subdirectories.

    Args:
        entry: Path entry to sort.

    Returns:
        Sort tuple (0 for files, 1 for dirs, lowercase name).
    """
    return (0 if entry.is_file() else 1, entry.name.lower())
