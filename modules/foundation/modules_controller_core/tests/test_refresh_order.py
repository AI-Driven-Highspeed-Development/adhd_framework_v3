"""Tests for refresh_order — dependency-based module ordering for refresh.

Tests sort_modules_for_refresh() for happy path, no-deps modules,
cross-layer deps, and external dep filtering.
"""

import pytest
from pathlib import Path

from modules_controller_core.modules_controller import ModuleInfo
from modules_controller_core.module_types import ModuleLayer
from modules_controller_core.refresh_order import sort_modules_for_refresh


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


class TestSortModulesForRefresh:
    """Test dependency-based topological ordering."""

    def test_empty_input(self):
        """Empty module list returns empty list."""
        assert sort_modules_for_refresh([]) == []

    def test_single_module_no_deps(self):
        """Single module with no deps returns itself."""
        m = _make_module("alpha")
        result = sort_modules_for_refresh([m])
        assert result == [m]

    def test_linear_chain(self):
        """A -> B -> C should produce C before B before A."""
        c = _make_module("mod_c")
        b = _make_module("mod_b", requirements=["mod-c"])
        a = _make_module("mod_a", requirements=["mod-b"])

        result = sort_modules_for_refresh([a, b, c])
        names = [m.name for m in result]

        assert names.index("mod_c") < names.index("mod_b")
        assert names.index("mod_b") < names.index("mod_a")

    def test_diamond_dependency(self):
        """Diamond: A depends on B and C, both depend on D."""
        d = _make_module("mod_d")
        b = _make_module("mod_b", requirements=["mod-d"])
        c = _make_module("mod_c", requirements=["mod-d"])
        a = _make_module("mod_a", requirements=["mod-b", "mod-c"])

        result = sort_modules_for_refresh([a, b, c, d])
        names = [m.name for m in result]

        assert names.index("mod_d") < names.index("mod_b")
        assert names.index("mod_d") < names.index("mod_c")
        assert names.index("mod_b") < names.index("mod_a")
        assert names.index("mod_c") < names.index("mod_a")

    def test_modules_with_no_deps_all_appear(self):
        """Modules with no inter-deps all appear in output."""
        a = _make_module("alpha")
        b = _make_module("beta")
        c = _make_module("gamma")

        result = sort_modules_for_refresh([a, b, c])
        assert set(m.name for m in result) == {"alpha", "beta", "gamma"}

    def test_external_deps_filtered_out(self):
        """External (non-ADHD) deps in requirements are ignored."""
        inner = _make_module("inner_mod")
        outer = _make_module(
            "outer_mod",
            requirements=["inner-mod", "rich>=13.0", "pydantic"],
        )

        result = sort_modules_for_refresh([inner, outer])
        names = [m.name for m in result]

        assert names.index("inner_mod") < names.index("outer_mod")
        assert len(result) == 2  # No fake modules created for external deps

    def test_cross_layer_deps_sorted_correctly(self):
        """Dev module depending on foundation module: foundation comes first."""
        foundation_mod = _make_module("logger_util", layer=ModuleLayer.FOUNDATION)
        dev_mod = _make_module(
            "adhd_mcp",
            layer=ModuleLayer.DEV,
            requirements=["logger-util"],
        )

        result = sort_modules_for_refresh([dev_mod, foundation_mod])
        names = [m.name for m in result]

        assert names.index("logger_util") < names.index("adhd_mcp")

    def test_realistic_foundation_chain(self):
        """Realistic foundation chain: exceptions -> logger -> config -> cli."""
        exceptions = _make_module("exceptions_core")
        logger = _make_module("logger_util", requirements=["exceptions-core"])
        config = _make_module(
            "config_manager",
            requirements=["logger-util", "exceptions-core"],
        )
        cli = _make_module(
            "cli_manager",
            requirements=["config-manager", "logger-util"],
        )

        result = sort_modules_for_refresh([cli, config, logger, exceptions])
        names = [m.name for m in result]

        assert names.index("exceptions_core") < names.index("logger_util")
        assert names.index("logger_util") < names.index("config_manager")
        assert names.index("config_manager") < names.index("cli_manager")

    def test_version_specifiers_stripped(self):
        """Version specifiers like >=1.0 are stripped when matching."""
        base = _make_module("base_mod")
        child = _make_module("child_mod", requirements=["base-mod>=2.0.0"])

        result = sort_modules_for_refresh([child, base])
        names = [m.name for m in result]

        assert names.index("base_mod") < names.index("child_mod")

    def test_preserves_all_modules(self):
        """All input modules appear in output, regardless of deps."""
        modules = [
            _make_module("a"),
            _make_module("b", requirements=["a"]),
            _make_module("c"),
        ]
        result = sort_modules_for_refresh(modules)
        assert len(result) == 3
        assert set(m.name for m in result) == {"a", "b", "c"}

    def test_partial_dep_not_in_input(self):
        """Dep that resolves to a known module name but isn't in input is ignored."""
        # Only 'child' is passed in, 'parent' is not — the edge is simply dropped
        child = _make_module("child_mod", requirements=["parent-mod"])

        result = sort_modules_for_refresh([child])
        assert len(result) == 1
        assert result[0].name == "child_mod"

    def test_modules_without_refresh_scripts_still_sorted(self):
        """Modules without refresh.py are still present in sorted output."""
        # refresh.py existence is irrelevant to ordering — it's about dep order
        base = _make_module("base_mod")
        dependent = _make_module("dependent_mod", requirements=["base-mod"])

        result = sort_modules_for_refresh([dependent, base])
        names = [m.name for m in result]

        assert names == ["base_mod", "dependent_mod"]
