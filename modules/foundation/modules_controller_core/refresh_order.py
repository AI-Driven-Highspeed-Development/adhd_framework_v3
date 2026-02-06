"""Refresh Order — Dependency-based topological sort for module refresh execution.

Provides sort_modules_for_refresh() which orders modules so that dependencies
are refreshed before their dependents. Uses graphlib.TopologicalSorter on
declared pyproject.toml dependencies.
"""

from __future__ import annotations

import graphlib
from typing import TYPE_CHECKING, Dict, List, Set

from logger_util import Logger
from exceptions_core import ADHDError

from .dependency_walker import _package_name_to_module_name

if TYPE_CHECKING:
    from .modules_controller import ModuleInfo

logger = Logger(__name__)


def sort_modules_for_refresh(modules: List[ModuleInfo]) -> List[ModuleInfo]:
    """Sort modules in dependency order for refresh execution.

    Uses graphlib.TopologicalSorter to produce a flat list where every module's
    dependencies appear before it. External (non-ADHD) dependencies in
    pyproject.toml are silently ignored.

    Args:
        modules: Unordered list of ModuleInfo from list_all_modules().

    Returns:
        List of ModuleInfo ordered so dependencies refresh first.

    Raises:
        ADHDError: If circular dependencies are detected (should not happen
            if deps were validated at module-add/sync time).
    """
    if not modules:
        return []

    name_to_module = {m.name: m for m in modules}
    graph = _build_dependency_graph(modules, known_modules=set(name_to_module.keys()))

    try:
        sorter = graphlib.TopologicalSorter(graph)
        ordered_names = list(sorter.static_order())
    except graphlib.CycleError as exc:
        raise ADHDError(
            f"Circular dependency detected in module graph: {exc}. "
            "Fix the cycle in pyproject.toml dependencies before refreshing."
        ) from exc

    # Filter to only modules in the input list (topo sort may include names
    # that aren't in our module set if the graph references them).
    ordered = [name_to_module[name] for name in ordered_names if name in name_to_module]

    return ordered


def _build_dependency_graph(
    modules: List[ModuleInfo],
    *,
    known_modules: Set[str],
) -> Dict[str, Set[str]]:
    """Build a dependency adjacency dict for TopologicalSorter.

    Only ADHD module dependencies are included — external PyPI packages are
    filtered out by checking against the known module name set.

    Args:
        modules: All discovered modules.
        known_modules: Set of known ADHD module names for filtering.

    Returns:
        Dict mapping module name -> set of ADHD module dep names.
    """
    graph: Dict[str, Set[str]] = {}

    for module in modules:
        adhd_deps: Set[str] = set()
        for raw_dep in module.requirements:
            dep_name = _package_name_to_module_name(raw_dep)
            if dep_name in known_modules:
                adhd_deps.add(dep_name)
        graph[module.name] = adhd_deps

    return graph
