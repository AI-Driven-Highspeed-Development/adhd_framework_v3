"""Tests for pyproject_patcher - root pyproject.toml patching.

MOCKS USED IN THIS FILE:
- None. These tests use real filesystem operations on tmp_path.
  No mocks needed because the patcher does pure file I/O.
"""

import tomllib
from pathlib import Path

import pytest


@pytest.fixture
def root_pyproject(tmp_path: Path) -> Path:
    """Create a minimal root pyproject.toml for testing."""
    root = tmp_path / "project"
    root.mkdir()
    pyproject = root / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-project"
version = "1.0.0"
dependencies = [
    "existing-dep",
]

[tool.uv.sources]
existing-dep = { workspace = true }

[tool.uv.workspace]
members = ["modules/*"]
""")
    return root


class TestAddToRootPyproject:
    """Test adding package to root pyproject.toml."""

    def test_add_new_dep(self, root_pyproject):
        """Should add new package to dependencies and sources.

        MOCKS: None (real file I/O)
        """
        from module_adder_core.pyproject_patcher import add_to_root_pyproject

        add_to_root_pyproject("new-package", root_pyproject)

        content = (root_pyproject / "pyproject.toml").read_text()
        assert '"new-package"' in content
        assert "new-package = { workspace = true }" in content

        # Verify TOML is still valid
        with (root_pyproject / "pyproject.toml").open("rb") as f:
            data = tomllib.load(f)
        assert "new-package" in data["project"]["dependencies"]

    def test_add_duplicate_dep_no_change(self, root_pyproject):
        """Should not add duplicate if package already in deps.

        MOCKS: None
        """
        from module_adder_core.pyproject_patcher import add_to_root_pyproject

        original = (root_pyproject / "pyproject.toml").read_text()
        add_to_root_pyproject("existing-dep", root_pyproject)
        modified = (root_pyproject / "pyproject.toml").read_text()

        assert original == modified

    def test_preserves_existing_content(self, root_pyproject):
        """Existing deps and sources should remain unchanged.

        MOCKS: None
        """
        from module_adder_core.pyproject_patcher import add_to_root_pyproject

        add_to_root_pyproject("new-package", root_pyproject)

        content = (root_pyproject / "pyproject.toml").read_text()
        assert '"existing-dep"' in content
        assert 'existing-dep = { workspace = true }' in content

    def test_missing_pyproject_raises(self, tmp_path):
        """Should raise ADHDError if pyproject.toml doesn't exist.

        MOCKS: None
        """
        from module_adder_core.pyproject_patcher import add_to_root_pyproject
        from exceptions_core import ADHDError

        with pytest.raises(ADHDError, match="not found"):
            add_to_root_pyproject("pkg", tmp_path)

    def test_missing_deps_section_raises(self, tmp_path):
        """Should raise ADHDError if dependencies section is missing.

        MOCKS: None
        """
        from module_adder_core.pyproject_patcher import add_to_root_pyproject
        from exceptions_core import ADHDError

        root = tmp_path / "project"
        root.mkdir()
        (root / "pyproject.toml").write_text("""[project]
name = "test"

[tool.uv.sources]
dep = { workspace = true }
""")

        with pytest.raises(ADHDError, match="dependencies"):
            add_to_root_pyproject("new-pkg", root)

    def test_missing_sources_section_raises(self, tmp_path):
        """Should raise ADHDError if [tool.uv.sources] section is missing.

        MOCKS: None
        """
        from module_adder_core.pyproject_patcher import add_to_root_pyproject
        from exceptions_core import ADHDError

        root = tmp_path / "project"
        root.mkdir()
        (root / "pyproject.toml").write_text("""[project]
name = "test"
dependencies = ["dep"]
""")

        with pytest.raises(ADHDError, match="sources"):
            add_to_root_pyproject("new-pkg", root)
