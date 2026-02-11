"""Unit tests for module_adder_core.

MOCKS USED IN THIS FILE:
- subprocess.run: Mocked to simulate git clone behavior. Creates files in tmp_path
  instead of actually cloning. RISK: If the real git clone returns different directory
  structures or exit codes, tests may pass but real usage may fail.
- shutil.which: Mocked to return a fake uv path. RISK: None (just avoids uv-not-found).
- ModulesController.sync: Mocked to no-op. RISK: If sync has side effects that affect
  module registration, integration tests may reveal issues.
- QuestionaryCore: Mocked to return predetermined answers. RISK: If prompt structure
  changes, scaffolder tests may not reflect real interactive flow.
"""

import shutil
import subprocess
import tomllib
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


# ---------------------
# Helper to create a mock clone directory
# ---------------------

def _create_mock_clone_dir(dest: Path, *, has_pyproject: bool = True, layer: str = "runtime",
                           has_git: bool = True, has_github: bool = True, has_gitignore: bool = True,
                           package_name: str = "testing-standalone-module"):
    """Create a directory structure simulating a cloned repo.

    MOCK: This replaces git clone. It creates a local directory with typical repo files.
    """
    dest.mkdir(parents=True, exist_ok=True)
    if has_pyproject:
        (dest / "pyproject.toml").write_text(f"""[project]
name = "{package_name}"
version = "0.0.1"
description = "Test module"
requires-python = ">=3.11"
dependencies = []

[tool.adhd]
layer = "{layer}"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
""")
    if has_git:
        (dest / ".git").mkdir()
        (dest / ".git" / "config").write_text("")
    if has_github:
        (dest / ".github").mkdir()
        (dest / ".github" / "workflows").mkdir()
    if has_gitignore:
        (dest / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    (dest / "__init__.py").write_text('"""Test module."""\n')


def _mock_subprocess_run_success(clone_dest: Path, **clone_kwargs):
    """Return a mock subprocess.run that populates clone_dest with files.

    MOCK: Replaces `git clone --depth 1 <url> <dest>`.
    """
    def mock_run(args, **kwargs):
        if args[0] == "git" and args[1] == "clone":
            dest = Path(args[-1])
            _create_mock_clone_dir(dest, **clone_kwargs)
            return MagicMock(returncode=0, stderr="", stdout="")
        return MagicMock(returncode=0)
    return mock_run


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """Create a minimal project root with modules/ directories and root pyproject.toml."""
    root = tmp_path / "project"
    (root / "modules" / "foundation").mkdir(parents=True)
    (root / "modules" / "runtime").mkdir(parents=True)
    (root / "modules" / "dev").mkdir(parents=True)
    (root / "pyproject.toml").write_text("""[project]
name = "test-project"
version = "1.0.0"
dependencies = [
    "some-dep",
]

[tool.uv.sources]
some-dep = { workspace = true }

[tool.uv.workspace]
members = ["modules/foundation/*", "modules/runtime/*", "modules/dev/*"]
""")
    return root


class TestAddFromRepoSuccess:
    """Test successful module addition from a standalone repo."""

    def test_add_from_repo_success(self, project_root):
        """Full success path: clone, validate, strip git, move, sync.

        MOCKS: subprocess.run (git clone), shutil.which, ModulesController.sync
        """
        from module_adder_core import ModuleAdder

        mock_run = _mock_subprocess_run_success(project_root, layer="runtime")

        with patch("subprocess.run", side_effect=mock_run):
            with patch("shutil.which", return_value="/usr/bin/uv"):
                with patch("modules_controller_core.ModulesController.sync"):
                    adder = ModuleAdder(project_root=project_root)
                    result = adder.add_from_repo(
                        "https://github.com/org/testing-standalone-module",
                        skip_prompt=True,
                    )

        assert result.success is True
        assert result.module_name == "testing_standalone_module"
        target = project_root / "modules" / "runtime" / "testing_standalone_module"
        assert target.exists()
        # .git should be removed
        assert not (target / ".git").exists()
        # .gitignore should be preserved
        assert (target / ".gitignore").exists()
        # .github should be removed
        assert not (target / ".github").exists()

    def test_add_from_repo_keep_git_flag(self, project_root):
        """--keep-git should preserve .git/ directory.

        MOCKS: subprocess.run, shutil.which, ModulesController.sync
        """
        from module_adder_core import ModuleAdder

        mock_run = _mock_subprocess_run_success(project_root, layer="runtime")

        with patch("subprocess.run", side_effect=mock_run):
            with patch("shutil.which", return_value="/usr/bin/uv"):
                with patch("modules_controller_core.ModulesController.sync"):
                    adder = ModuleAdder(project_root=project_root)
                    result = adder.add_from_repo(
                        "https://github.com/org/testing-standalone-module",
                        keep_git=True,
                        skip_prompt=True,
                    )

        assert result.success is True
        target = project_root / "modules" / "runtime" / "testing_standalone_module"
        # .git should be preserved
        assert (target / ".git").exists()
        # .github should also be preserved
        assert (target / ".github").exists()


class TestAddFromRepoNoProject:
    """Test adding module without pyproject.toml (scaffolding)."""

    def test_add_from_repo_no_pyproject_skip_prompt(self, project_root):
        """When pyproject.toml is missing and skip_prompt=True, scaffold with defaults.

        MOCKS: subprocess.run (creates dir without pyproject.toml), shutil.which, ModulesController.sync
        """
        from module_adder_core import ModuleAdder

        mock_run = _mock_subprocess_run_success(project_root, has_pyproject=False)

        with patch("subprocess.run", side_effect=mock_run):
            with patch("shutil.which", return_value="/usr/bin/uv"):
                with patch("modules_controller_core.ModulesController.sync"):
                    adder = ModuleAdder(project_root=project_root)
                    result = adder.add_from_repo(
                        "https://github.com/org/testing-standalone-module",
                        skip_prompt=True,
                    )

        assert result.success is True
        # Default layer is runtime
        assert result.layer == "runtime"
        target = project_root / "modules" / "runtime" / result.module_name
        assert target.exists()
        # pyproject.toml should have been scaffolded
        assert (target / "pyproject.toml").exists()
        # Verify the scaffolded pyproject is valid TOML
        with (target / "pyproject.toml").open("rb") as f:
            data = tomllib.load(f)
        assert data["project"]["name"] is not None
        assert data["tool"]["adhd"]["layer"] == "runtime"


class TestAddFromRepoFailures:
    """Test failure paths."""

    def test_add_from_repo_invalid_url(self, project_root):
        """Non-URL input should fail immediately.

        MOCKS: None
        """
        from module_adder_core import ModuleAdder
        adder = ModuleAdder(project_root=project_root)
        result = adder.add_from_repo("not-a-url")
        assert result.success is False
        assert "URL" in result.message or "url" in result.message

    def test_add_from_repo_collision_detection(self, project_root):
        """Should fail if module already exists at target path.

        MOCKS: subprocess.run, shutil.which, ModulesController.sync
        """
        from module_adder_core import ModuleAdder

        # Pre-create the target directory
        existing = project_root / "modules" / "runtime" / "testing_standalone_module"
        existing.mkdir(parents=True)

        mock_run = _mock_subprocess_run_success(project_root, layer="runtime")

        with patch("subprocess.run", side_effect=mock_run):
            with patch("shutil.which", return_value="/usr/bin/uv"):
                with patch("modules_controller_core.ModulesController.sync"):
                    adder = ModuleAdder(project_root=project_root)
                    result = adder.add_from_repo(
                        "https://github.com/org/testing-standalone-module",
                        skip_prompt=True,
                    )

        assert result.success is False
        assert "already exists" in result.message

    def test_add_from_repo_clone_failure(self, project_root):
        """Failed git clone should return failure result.

        MOCKS: subprocess.run (returns non-zero exit code)
        """
        from module_adder_core import ModuleAdder

        def mock_run(args, **kwargs):
            if args[0] == "git":
                return MagicMock(returncode=1, stderr="fatal: repository not found", stdout="")
            return MagicMock(returncode=0)

        with patch("subprocess.run", side_effect=mock_run):
            adder = ModuleAdder(project_root=project_root)
            result = adder.add_from_repo(
                "https://github.com/org/nonexistent",
                skip_prompt=True,
            )

        assert result.success is False
        # URL should be redacted in error message
        assert "<URL>" in result.message or "clone failed" in result.message

    def test_add_from_repo_clone_timeout(self, project_root):
        """Clone timeout should return failure result.

        MOCKS: subprocess.run (raises TimeoutExpired)
        """
        from module_adder_core import ModuleAdder

        def mock_run(args, **kwargs):
            if args[0] == "git":
                raise subprocess.TimeoutExpired(cmd="git clone", timeout=120)
            return MagicMock(returncode=0)

        with patch("subprocess.run", side_effect=mock_run):
            adder = ModuleAdder(project_root=project_root)
            result = adder.add_from_repo(
                "https://github.com/org/slow-repo",
                skip_prompt=True,
            )

        assert result.success is False
        assert "timed out" in result.message

    def test_add_from_repo_invalid_layer(self, project_root):
        """Invalid layer in pyproject.toml should fail.

        MOCKS: subprocess.run (creates dir with invalid layer)
        """
        from module_adder_core import ModuleAdder

        mock_run = _mock_subprocess_run_success(project_root, layer="invalid")

        with patch("subprocess.run", side_effect=mock_run):
            adder = ModuleAdder(project_root=project_root)
            result = adder.add_from_repo(
                "https://github.com/org/bad-layer",
                skip_prompt=True,
            )

        assert result.success is False
        assert "layer" in result.message.lower() or "Unknown" in result.message


class TestAddFromMonorepo:
    """Test Mode 2: adding from monorepo subfolder."""

    def test_add_from_monorepo_success(self, project_root):
        """Extract subfolder from cloned monorepo.

        MOCKS: subprocess.run (creates monorepo with packages/alpha/)
        """
        from module_adder_core import ModuleAdder

        def mock_run(args, **kwargs):
            if args[0] == "git" and args[1] == "clone":
                dest = Path(args[-1])
                dest.mkdir(parents=True, exist_ok=True)
                # Create monorepo structure
                alpha_dir = dest / "packages" / "alpha"
                alpha_dir.mkdir(parents=True)
                (alpha_dir / "pyproject.toml").write_text("""[project]
name = "testing-alpha"
version = "0.1.0"
dependencies = []

[tool.adhd]
layer = "foundation"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
""")
                (alpha_dir / "__init__.py").write_text('"""Alpha."""\n')
                (alpha_dir / ".gitignore").write_text("__pycache__/\n")
                (dest / ".git").mkdir()
                return MagicMock(returncode=0, stderr="", stdout="")
            return MagicMock(returncode=0)

        with patch("subprocess.run", side_effect=mock_run):
            with patch("shutil.which", return_value="/usr/bin/uv"):
                with patch("modules_controller_core.ModulesController.sync"):
                    adder = ModuleAdder(project_root=project_root)
                    result = adder.add_from_repo(
                        "https://github.com/org/testing-monorepo",
                        subfolder="packages/alpha",
                        skip_prompt=True,
                    )

        assert result.success is True
        assert result.module_name == "testing_alpha"
        assert result.layer == "foundation"
        target = project_root / "modules" / "foundation" / "testing_alpha"
        assert target.exists()
        assert (target / "__init__.py").exists()
        # .gitignore from subfolder should be preserved
        assert (target / ".gitignore").exists()

    def test_add_from_monorepo_subfolder_not_found(self, project_root):
        """Should fail when subfolder doesn't exist in cloned repo.

        MOCKS: subprocess.run (creates repo without the requested subfolder)
        """
        from module_adder_core import ModuleAdder

        def mock_run(args, **kwargs):
            if args[0] == "git" and args[1] == "clone":
                dest = Path(args[-1])
                dest.mkdir(parents=True, exist_ok=True)
                (dest / ".git").mkdir()
                return MagicMock(returncode=0, stderr="", stdout="")
            return MagicMock(returncode=0)

        with patch("subprocess.run", side_effect=mock_run):
            adder = ModuleAdder(project_root=project_root)
            result = adder.add_from_repo(
                "https://github.com/org/testing-monorepo",
                subfolder="packages/nonexistent",
                skip_prompt=True,
            )

        assert result.success is False
        assert "not found" in result.message.lower()


class TestAddFromPyPI:
    """Test Mode 3: PyPI (stub)."""

    def test_add_from_pypi_raises_not_implemented(self):
        """PyPI mode should raise NotImplementedError."""
        from module_adder_core import ModuleAdder
        adder = ModuleAdder()
        with pytest.raises(NotImplementedError, match="not yet available"):
            adder.add_from_pypi("some-package")


class TestGitStripping:
    """Test git info stripping behavior."""

    def test_strips_git_and_github_preserves_gitignore(self, project_root):
        """Default mode should strip .git/ and .github/ but preserve .gitignore.

        MOCKS: subprocess.run
        """
        from module_adder_core import ModuleAdder

        mock_run = _mock_subprocess_run_success(
            project_root, has_git=True, has_github=True, has_gitignore=True
        )

        with patch("subprocess.run", side_effect=mock_run):
            with patch("shutil.which", return_value="/usr/bin/uv"):
                with patch("modules_controller_core.ModulesController.sync"):
                    adder = ModuleAdder(project_root=project_root)
                    result = adder.add_from_repo(
                        "https://github.com/org/testing-standalone-module",
                        skip_prompt=True,
                    )

        assert result.success is True
        target = project_root / "modules" / "runtime" / "testing_standalone_module"
        assert not (target / ".git").exists(), ".git/ should be removed"
        assert not (target / ".github").exists(), ".github/ should be removed"
        assert (target / ".gitignore").exists(), ".gitignore should be preserved"
