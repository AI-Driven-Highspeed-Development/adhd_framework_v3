"""Tests for remove_from_root_pyproject — root pyproject.toml un-patching.

MOCKS USED IN THIS FILE:
- None.  These tests use real filesystem operations on tmp_path.
  No mocks needed because the patcher does pure file I/O.
"""

import tomllib
from pathlib import Path

import pytest


# ── fixtures ────────────────────────────────────────────────────────────────

MINIMAL_PYPROJECT = """\
[project]
name = "test-project"
version = "1.0.0"
dependencies = [
    "existing-dep",
    "another-dep",
]

[tool.uv.sources]
existing-dep = { workspace = true }
another-dep = { workspace = true }

[tool.uv.workspace]
members = ["modules/*"]
"""


@pytest.fixture
def root_pyproject(tmp_path: Path) -> Path:
    """Create a project root with a minimal pyproject.toml."""
    root = tmp_path / "project"
    root.mkdir()
    (root / "pyproject.toml").write_text(MINIMAL_PYPROJECT)
    return root


# ── helpers ─────────────────────────────────────────────────────────────────


def _parsed(root: Path) -> dict:
    """Parse pyproject.toml and return the dict."""
    with (root / "pyproject.toml").open("rb") as f:
        return tomllib.load(f)


# ── tests ───────────────────────────────────────────────────────────────────


class TestRemoveFromRootPyproject:
    """Test removing packages from root pyproject.toml."""

    def test_remove_existing_dep(self, root_pyproject: Path):
        """Should remove package from both deps and sources.

        MOCKS: None (real file I/O)
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject

        remove_from_root_pyproject("existing-dep", root_pyproject)

        data = _parsed(root_pyproject)
        assert "existing-dep" not in data["project"]["dependencies"]
        assert "existing-dep" not in data["tool"]["uv"]["sources"]
        # Other dep should remain
        assert "another-dep" in data["project"]["dependencies"]
        assert "another-dep" in data["tool"]["uv"]["sources"]

    def test_remove_not_found_no_error(self, root_pyproject: Path):
        """Removing a nonexistent package logs warning but does not raise.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject

        original = (root_pyproject / "pyproject.toml").read_text()
        # Should NOT raise
        remove_from_root_pyproject("ghost-package", root_pyproject)
        after = (root_pyproject / "pyproject.toml").read_text()

        assert original == after

    def test_file_missing_raises(self, tmp_path: Path):
        """Should raise ADHDError when pyproject.toml does not exist.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject
        from exceptions_core import ADHDError

        with pytest.raises(ADHDError, match="not found"):
            remove_from_root_pyproject("pkg", tmp_path)

    def test_toml_still_valid_after_removal(self, root_pyproject: Path):
        """File must remain valid TOML after removal.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject

        remove_from_root_pyproject("existing-dep", root_pyproject)

        # Should parse without error
        data = _parsed(root_pyproject)
        assert data["project"]["name"] == "test-project"

    def test_preserves_other_sections(self, root_pyproject: Path):
        """[tool.uv.workspace] and [project] metadata must survive removal.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject

        remove_from_root_pyproject("existing-dep", root_pyproject)

        data = _parsed(root_pyproject)
        assert data["tool"]["uv"]["workspace"]["members"] == ["modules/*"]
        assert data["project"]["version"] == "1.0.0"

    def test_remove_last_dep(self, tmp_path: Path):
        """Removing the only dependency should leave an empty list.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject

        root = tmp_path / "project"
        root.mkdir()
        (root / "pyproject.toml").write_text("""\
[project]
name = "test-project"
version = "1.0.0"
dependencies = [
    "only-dep",
]

[tool.uv.sources]
only-dep = { workspace = true }

[tool.uv.workspace]
members = ["modules/*"]
""")

        remove_from_root_pyproject("only-dep", root)

        data = _parsed(root)
        assert data["project"]["dependencies"] == []
        assert "only-dep" not in data["tool"]["uv"]["sources"]

    def test_idempotent_double_remove(self, root_pyproject: Path):
        """Calling remove twice should succeed without error.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject

        remove_from_root_pyproject("existing-dep", root_pyproject)
        # Second call — package already gone
        remove_from_root_pyproject("existing-dep", root_pyproject)

        data = _parsed(root_pyproject)
        assert "existing-dep" not in data["project"]["dependencies"]

    def test_round_trip_add_then_remove(self, root_pyproject: Path):
        """add → remove should yield a file identical to the original.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import (
            add_to_root_pyproject,
            remove_from_root_pyproject,
        )

        original = (root_pyproject / "pyproject.toml").read_text()

        add_to_root_pyproject("new-package", root_pyproject)
        # Verify it was added
        data = _parsed(root_pyproject)
        assert "new-package" in data["project"]["dependencies"]

        remove_from_root_pyproject("new-package", root_pyproject)
        after = (root_pyproject / "pyproject.toml").read_text()

        assert original == after

    def test_missing_deps_section_raises(self, tmp_path: Path):
        """Should raise ADHDError when dependencies section is absent.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject
        from exceptions_core import ADHDError

        root = tmp_path / "project"
        root.mkdir()
        # Package in sources only (no dependencies key at all — pathological)
        (root / "pyproject.toml").write_text("""\
[project]
name = "test"

[tool.uv.sources]
dep = { workspace = true }
""")

        with pytest.raises(ADHDError, match="dependencies"):
            remove_from_root_pyproject("dep", root)

    def test_missing_sources_section_raises(self, tmp_path: Path):
        """Should raise ADHDError when [tool.uv.sources] section is absent.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_patcher import remove_from_root_pyproject
        from exceptions_core import ADHDError

        root = tmp_path / "project"
        root.mkdir()
        (root / "pyproject.toml").write_text("""\
[project]
name = "test"
dependencies = ["dep"]
""")

        with pytest.raises(ADHDError, match="sources"):
            remove_from_root_pyproject("dep", root)
