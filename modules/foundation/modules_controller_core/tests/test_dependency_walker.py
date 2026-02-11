"""Tests for DependencyWalker.get_reverse_deps — reverse dependency lookup.

MOCKS USED IN THIS FILE:
- controller (MagicMock) – stands in for ModulesController.
  list_all_modules() returns a pre-built ModulesReport.
  get_module_pyproject() returns per-module dependency dicts.
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock

from modules_controller_core.modules_controller import ModuleInfo, ModulesReport
from modules_controller_core.module_types import ModuleLayer
from modules_controller_core.dependency_walker import DependencyWalker


# ── helpers ─────────────────────────────────────────────────────────────────


def _make_module(
    name: str,
    *,
    layer: ModuleLayer = ModuleLayer.FOUNDATION,
    requirements: list[str] | None = None,
) -> ModuleInfo:
    """Create a minimal ModuleInfo for testing."""
    return ModuleInfo(
        name=name,
        version="1.0.0",
        layer=layer,
        path=Path(f"/fake/modules/{layer.value}/{name}"),
        requirements=requirements or [],
    )


def _build_controller(
    modules: list[ModuleInfo],
    dep_map: dict[str, list[str]],
) -> MagicMock:
    """Build a mock controller whose list_all_modules and get_module_pyproject
    return data consistent with *modules* and *dep_map*.

    MOCK JUSTIFICATION:
    - controller is a collaborator with heavy filesystem I/O (scans module
      directories).  Mocking avoids needing a real module tree on disk.
    - dep_map lets us precisely control which modules declare which deps so
      tests are deterministic.

    Args:
        modules: List of ModuleInfo objects returned by list_all_modules().
        dep_map: module_name -> list of dependency strings (kebab-case ok).
    """
    controller = MagicMock()
    report = ModulesReport(modules=modules, issued_modules=[], root_path=Path("/fake"))
    controller.list_all_modules.return_value = report

    def _pyproject_for(path: Path) -> dict:
        """Return a synthetic pyproject dict for the module at *path*."""
        mod_name = path.name
        deps = dep_map.get(mod_name, [])
        return {
            "project": {"dependencies": deps},
            "tool": {"adhd": {"layer": "foundation"}},
        }

    controller.get_module_pyproject.side_effect = _pyproject_for

    # get_module_by_name — look up by name in our module list
    name_lookup = {m.name: m for m in modules}
    controller.get_module_by_name.side_effect = lambda n: name_lookup.get(n)

    return controller


# ── tests ───────────────────────────────────────────────────────────────────


class TestGetReverseDeps:
    """Test DependencyWalker.get_reverse_deps()."""

    def test_no_dependants(self):
        """Module with zero consumers returns empty set.

        MOCKS: controller (MagicMock) — avoids filesystem scan.
        """
        a = _make_module("alpha")
        b = _make_module("bravo")
        controller = _build_controller([a, b], {"alpha": [], "bravo": []})

        walker = DependencyWalker(controller)
        result = walker.get_reverse_deps("alpha")

        assert result == set()

    def test_single_dependant(self):
        """One module depends on target → returned in set.

        MOCKS: controller (MagicMock)
        """
        a = _make_module("alpha")
        b = _make_module("bravo")
        controller = _build_controller(
            [a, b],
            {"alpha": [], "bravo": ["alpha"]},
        )

        walker = DependencyWalker(controller)
        result = walker.get_reverse_deps("alpha")

        assert result == {"bravo"}

    def test_multiple_dependants(self):
        """Several modules depend on target → all returned.

        MOCKS: controller (MagicMock)
        """
        core = _make_module("core_lib")
        a = _make_module("alpha")
        b = _make_module("bravo")
        c = _make_module("charlie")
        controller = _build_controller(
            [core, a, b, c],
            {
                "core_lib": [],
                "alpha": ["core-lib"],  # kebab-case in deps
                "bravo": ["core-lib"],
                "charlie": [],
            },
        )

        walker = DependencyWalker(controller)
        result = walker.get_reverse_deps("core_lib")

        assert result == {"alpha", "bravo"}

    def test_kebab_case_input_normalised(self):
        """Passing kebab-case module name still matches snake_case modules.

        MOCKS: controller (MagicMock)
        """
        target = _make_module("config_manager")
        consumer = _make_module("my_app", layer=ModuleLayer.RUNTIME)
        controller = _build_controller(
            [target, consumer],
            {"config_manager": [], "my_app": ["config-manager"]},
        )

        walker = DependencyWalker(controller)
        # Input uses kebab-case
        result = walker.get_reverse_deps("config-manager")

        assert result == {"my_app"}

    def test_self_not_included(self):
        """Module listing itself as a dependency should not appear in output.

        MOCKS: controller (MagicMock)
        """
        a = _make_module("alpha")
        controller = _build_controller(
            [a],
            {"alpha": ["alpha"]},  # pathological self-dep
        )

        walker = DependencyWalker(controller)
        result = walker.get_reverse_deps("alpha")

        assert result == set()

    def test_transitive_deps_not_included(self):
        """Only direct dependants are returned, not transitive consumers.

        A depends on B depends on C.  get_reverse_deps("C") should return
        only {"B"}, NOT {"A", "B"}.

        MOCKS: controller (MagicMock)
        """
        c = _make_module("charlie")
        b = _make_module("bravo")
        a = _make_module("alpha")
        controller = _build_controller(
            [a, b, c],
            {"charlie": [], "bravo": ["charlie"], "alpha": ["bravo"]},
        )

        walker = DependencyWalker(controller)
        result = walker.get_reverse_deps("charlie")

        assert result == {"bravo"}

    def test_nonexistent_module_returns_empty(self):
        """Querying a module that doesn't exist returns empty set (no crash).

        MOCKS: controller (MagicMock)
        """
        a = _make_module("alpha")
        controller = _build_controller([a], {"alpha": []})

        walker = DependencyWalker(controller)
        result = walker.get_reverse_deps("does_not_exist")

        assert result == set()
