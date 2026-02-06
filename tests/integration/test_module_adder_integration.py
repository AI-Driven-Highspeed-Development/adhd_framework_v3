"""Integration tests for module_adder_core using real GitHub test repos.

These tests perform real git clone operations against private repos in
AI-Driven-Highspeed-Development org. They require network connectivity
and GitHub authentication (via `gh` CLI).

Test Repos
----------
1. testing_standalone_module   — has valid pyproject.toml (layer=runtime)
2. testing_standalone_no_pyproject — no pyproject.toml at all
3. testing_monorepo            — packages/alpha (has pyproject), packages/beta (no pyproject)

MOCK DOCUMENTATION (for later bug assessment)
=============================================
MOCK: None — these are real integration tests.
- Real git clone over network.
- Real filesystem operations in a temporary project_root.
- Real pyproject.toml reading/writing.
- Real `modules_controller_core.ModulesController.sync` is PATCHED OUT because
  calling `uv sync` on a temp directory without a full workspace would fail.
  This is the ONLY mock in these integration tests.
  RISK: If sync() is called incorrectly or the module isn't actually placed
  correctly in the workspace, this mock would hide it. However, we verify
  the target directory layout independently, so the risk is low.

MOCK: `ModulesController.sync` — patched to no-op.
  WHY: Integration test copies modules into a temp dir that has no real uv
  workspace. Running real uv sync would fail with missing lockfile/workspace.
  RISK: If add_from_repo changes the order of operations (e.g., sync before
  move), the mock could hide a sequencing bug. Mitigated by verifying the
  module dir was actually created.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Skip the entire module if GitHub is unreachable
_SKIP_REASON = "Requires network & GitHub auth"
_ORG = "AI-Driven-Highspeed-Development"
_STANDALONE_URL = f"https://github.com/{_ORG}/testing_standalone_module"
_NO_PYPROJECT_URL = f"https://github.com/{_ORG}/testing_standalone_no_pyproject"
_MONOREPO_URL = f"https://github.com/{_ORG}/testing_monorepo"


def _can_reach_github() -> bool:
    """Quick check that `gh` can auth and the org is reachable."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", f"{_ORG}/testing_standalone_module", "--json", "name"],
            capture_output=True, text=True, timeout=15,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


pytestmark = pytest.mark.skipif(
    not _can_reach_github(),
    reason=_SKIP_REASON,
)


@pytest.fixture
def fake_project_root(tmp_path):
    """Create a minimal fake ADHD project root for integration testing.

    This includes the modules/{foundation,runtime,dev}/ directories to
    mirror a real project layout, but does NOT include a real uv workspace
    or lockfile.
    """
    root = tmp_path / "project"
    root.mkdir()
    (root / "modules" / "foundation").mkdir(parents=True)
    (root / "modules" / "runtime").mkdir(parents=True)
    (root / "modules" / "dev").mkdir(parents=True)
    return root


@pytest.fixture
def patched_sync():
    """Patch out ModulesController.sync() so we don't need a real uv workspace.

    MOCK: ModulesController.sync -> no-op
    RISK: Hides any bug where sync() is called at the wrong time or with
    wrong arguments. Mitigated by checking target directory contents.
    """
    with patch("modules_controller_core.ModulesController") as MockCtrl:
        instance = MockCtrl.return_value
        instance.sync.return_value = None
        yield instance


class TestAddStandaloneWithPyproject:
    """Mode 1: standalone repo with valid pyproject.toml."""

    def test_add_standalone_success(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _STANDALONE_URL,
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success, f"Expected success but got: {result.message}"
        assert result.module_name == "testing_standalone_module"
        assert result.layer == "runtime"
        assert result.target_path is not None
        assert result.target_path.exists()
        # Verify key files present
        assert (result.target_path / "pyproject.toml").exists()
        assert (result.target_path / "__init__.py").exists()
        assert (result.target_path / "testing_standalone_module.py").exists()

    def test_add_standalone_strips_git(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _STANDALONE_URL,
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success
        # .git/ should be removed
        assert not (result.target_path / ".git").exists()
        # .gitignore should be preserved
        assert (result.target_path / ".gitignore").exists()

    def test_add_standalone_keep_git(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _STANDALONE_URL,
            keep_git=True,
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success
        # .git/ should be preserved when keep_git=True
        assert (result.target_path / ".git").exists()

    def test_add_standalone_collision(self, fake_project_root, patched_sync):
        """Adding the same module twice should fail on the second attempt."""
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)

        # First add
        r1 = adder.add_from_repo(
            _STANDALONE_URL, skip_prompt=True, add_to_root=False,
        )
        assert r1.success

        # Second add - should fail with collision
        r2 = adder.add_from_repo(
            _STANDALONE_URL, skip_prompt=True, add_to_root=False,
        )
        assert not r2.success
        assert "already exists" in r2.message


class TestAddStandaloneNoPyproject:
    """Mode 1: standalone repo WITHOUT pyproject.toml (scaffolding test)."""

    def test_auto_scaffold_with_skip_prompt(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _NO_PYPROJECT_URL,
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success, f"Expected success but got: {result.message}"
        # Scaffolded pyproject.toml should exist
        assert (result.target_path / "pyproject.toml").exists()
        # Default layer is runtime
        assert result.layer == "runtime"
        # Should be placed in modules/runtime/
        assert "runtime" in str(result.target_path)

    def test_scaffold_creates_valid_pyproject(self, fake_project_root, patched_sync):
        import tomllib
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _NO_PYPROJECT_URL,
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success
        pyproject_path = result.target_path / "pyproject.toml"
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)

        # Validate structure
        assert "project" in data
        assert "name" in data["project"]
        assert "tool" in data
        assert "adhd" in data["tool"]
        assert data["tool"]["adhd"]["layer"] == "runtime"


class TestAddMonorepoSubfolder:
    """Mode 2: extract a subfolder from a monorepo."""

    def test_add_alpha_subfolder_success(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _MONOREPO_URL,
            subfolder="packages/alpha",
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success, f"Expected success but got: {result.message}"
        assert result.module_name == "testing_alpha"
        assert result.layer == "foundation"
        # Verify alpha files are present (not the full repo)
        assert (result.target_path / "pyproject.toml").exists()
        assert (result.target_path / "__init__.py").exists()
        assert (result.target_path / "alpha_module.py").exists()
        # Verify repo root files are NOT present
        assert not (result.target_path / "README.md").exists()
        assert not (result.target_path / "packages").exists()

    def test_add_beta_subfolder_no_pyproject(self, fake_project_root, patched_sync):
        """Beta has no pyproject.toml, should auto-scaffold."""
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _MONOREPO_URL,
            subfolder="packages/beta",
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success, f"Expected success but got: {result.message}"
        # Scaffolded pyproject.toml should exist
        assert (result.target_path / "pyproject.toml").exists()
        # Original files should be present
        assert (result.target_path / "__init__.py").exists()
        assert (result.target_path / "beta_code.py").exists()

    def test_add_nonexistent_subfolder(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _MONOREPO_URL,
            subfolder="packages/nonexistent",
            skip_prompt=True,
            add_to_root=False,
        )

        assert not result.success
        assert "subfolder not found" in result.message.lower() or "Subfolder not found" in result.message

    def test_monorepo_alpha_preserves_gitignore(self, fake_project_root, patched_sync):
        """Alpha has its own .gitignore — should be preserved."""
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            _MONOREPO_URL,
            subfolder="packages/alpha",
            skip_prompt=True,
            add_to_root=False,
        )

        assert result.success
        assert (result.target_path / ".gitignore").exists()


class TestAddEdgeCases:
    """Edge cases and error handling with real repos."""

    def test_invalid_url_format(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo("not-a-url", skip_prompt=True)

        assert not result.success
        assert "Invalid URL" in result.message or "URL" in result.message

    def test_unreachable_repo(self, fake_project_root, patched_sync):
        from module_adder_core import ModuleAdder

        adder = ModuleAdder(project_root=fake_project_root)
        result = adder.add_from_repo(
            "https://github.com/AI-Driven-Highspeed-Development/nonexistent_repo_9999",
            skip_prompt=True,
        )

        assert not result.success
        assert "clone failed" in result.message.lower() or "error" in result.message.lower()
