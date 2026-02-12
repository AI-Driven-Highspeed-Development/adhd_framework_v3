"""Unit tests for ModuleRemover and ModuleUpdater.

MOCKS USED IN THIS FILE:
- ModulesController: Mocked to return fake ModuleInfo objects. RISK: If
  the real controller changes its return shapes, tests may pass but real
  usage may diverge.
- DependencyWalker.get_reverse_deps: Mocked to return controlled sets.
  RISK: If the walker logic changes, integration tests are needed.
- ModulesController.sync: Mocked to no-op. RISK: If sync side-effects
  affect module registration, integration tests are needed.
- ModulesController.generate_workspace_file: Mocked to no-op.
- subprocess.run: Mocked for git operations in ModuleUpdater tests.
- shutil.which: Mocked to return a fake uv path.
- remove_from_root_pyproject: Mocked in some tests to avoid touching real
  pyproject.toml files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from module_lifecycle_core.module_remover import ModuleRemover, RemoveResult
from module_lifecycle_core.module_updater import ModuleUpdater, UpdateResult, BatchUpdateResult
from modules_controller_core.module_types import ModuleLayer

# Patch targets — the local imports inside remove()/update() pull from these
_CTRL_PATCH = "modules_controller_core.ModulesController"
_WALKER_PATCH = "modules_controller_core.dependency_walker.DependencyWalker"
# Updater tests use the same controller patch target
_UPDATER_CTRL_PATCH = _CTRL_PATCH


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_module_info(
    name: str = "test_module",
    version: str = "1.0.0",
    layer_value: str = "runtime",
    path: Path | None = None,
    repo_url: str | None = None,
    requirements: list[str] | None = None,
) -> MagicMock:
    """Build a MagicMock that behaves like ``ModuleInfo``."""
    mi = MagicMock()
    mi.name = name
    mi.version = version
    mi.path = path or Path(f"/fake/modules/{layer_value}/{name}")
    mi.repo_url = repo_url
    mi.requirements = requirements or []

    # layer is a real ModuleLayer enum for correct equality comparisons
    mi.layer = ModuleLayer(layer_value)

    return mi


def _create_module_dir(base: Path, name: str = "test_module", *, layer: str = "runtime",
                       package_name: str | None = None, version: str = "1.0.0") -> Path:
    """Create a minimal module directory with a valid pyproject.toml."""
    pkg = package_name or name.replace("_", "-")
    module_dir = base / "modules" / layer / name
    module_dir.mkdir(parents=True, exist_ok=True)
    (module_dir / "__init__.py").write_text(f'"""Test module."""\n')
    (module_dir / "pyproject.toml").write_text(
        f'[project]\nname = "{pkg}"\nversion = "{version}"\n'
        f'dependencies = []\n\n[tool.adhd]\nlayer = "{layer}"\n\n'
        f'[build-system]\nrequires = ["hatchling"]\n'
        f'build-backend = "hatchling.build"\n'
    )
    return module_dir


def _create_root_pyproject(base: Path, *, package_name: str = "test-module") -> Path:
    """Create a minimal root pyproject.toml with the given package in deps."""
    root_pp = base / "pyproject.toml"
    root_pp.write_text(
        f'[project]\nname = "test-project"\nversion = "0.0.1"\n'
        f'dependencies = [\n    "{package_name}",\n]\n\n'
        f'[tool.uv.sources]\n{package_name} = {{ workspace = true }}\n'
    )
    return root_pp


def _fake_clone_side_effect(
    cmd: list[str],
    *,
    capture_output: bool,
    text: bool,
    timeout: int,
) -> MagicMock:
    """Simulate a successful ``git clone`` by creating a minimal module on disk.

    Used as ``side_effect`` for ``subprocess.run`` in updater tests.
    """
    dest = Path(cmd[-1])
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "__init__.py").write_text('"""cloned."""\n')
    (dest / "pyproject.toml").write_text(
        '[project]\nname = "my-widget"\nversion = "2.0.0"\n'
        'dependencies = []\n\n[tool.adhd]\nlayer = "runtime"\n'
    )
    (dest / ".git").mkdir()
    result = MagicMock()
    result.returncode = 0
    return result


# ===========================================================================
# ModuleRemover tests
# ===========================================================================


class TestModuleRemoverDryRun:
    """Dry-run should print preview and make no modifications."""

    def test_dry_run_returns_success(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "my_widget")
        module = _make_module_info("my_widget", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = set()

            remover = ModuleRemover(project_root=tmp_path)
            result = remover.remove("my_widget", dry_run=True)

        assert result.success is True
        assert "dry-run" in result.message.lower() or "Dry-run" in result.message

    def test_dry_run_does_not_delete_directory(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "my_widget")
        module = _make_module_info("my_widget", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = set()

            remover = ModuleRemover(project_root=tmp_path)
            remover.remove("my_widget", dry_run=True)

        assert module_dir.exists(), "Dry-run should not delete the directory"

    def test_dry_run_does_not_call_sync(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "my_widget")
        module = _make_module_info("my_widget", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = set()

            remover = ModuleRemover(project_root=tmp_path)
            remover.remove("my_widget", dry_run=True)

        ctrl_inst.sync.assert_not_called()
        ctrl_inst.generate_workspace_file.assert_not_called()


class TestModuleRemoverReverseDeps:
    """Reverse dependency checks should block removal unless --force."""

    def test_refuses_when_dependents_exist(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "shared_util")
        module = _make_module_info("shared_util", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = {"api_gateway", "auth_manager"}

            remover = ModuleRemover(project_root=tmp_path)
            result = remover.remove("shared_util", no_confirm=True)

        assert result.success is False
        assert "api_gateway" in result.message
        assert "auth_manager" in result.message
        assert result.reverse_deps == {"api_gateway", "auth_manager"}

    def test_force_overrides_reverse_deps(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "shared_util")
        _create_root_pyproject(tmp_path, package_name="shared-util")
        module = _make_module_info("shared_util", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = {"api_gateway"}

            remover = ModuleRemover(project_root=tmp_path)
            result = remover.remove("shared_util", force=True, no_confirm=True)

        assert result.success is True


class TestModuleRemoverExecution:
    """Full removal sequence tests."""

    def test_full_removal_deletes_directory(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "old_module")
        _create_root_pyproject(tmp_path, package_name="old-module")
        module = _make_module_info("old_module", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = set()

            remover = ModuleRemover(project_root=tmp_path)
            result = remover.remove("old_module", no_confirm=True)

        assert result.success is True
        assert not module_dir.exists(), "Directory should be deleted after removal"

    def test_keep_dir_preserves_directory(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "old_module")
        _create_root_pyproject(tmp_path, package_name="old-module")
        module = _make_module_info("old_module", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = set()

            remover = ModuleRemover(project_root=tmp_path)
            result = remover.remove("old_module", keep_dir=True, no_confirm=True)

        assert result.success is True
        assert module_dir.exists(), "--keep-dir should preserve the directory"

    def test_calls_sync_and_workspace_regen(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "old_module")
        _create_root_pyproject(tmp_path, package_name="old-module")
        module = _make_module_info("old_module", path=module_dir)

        with (
            patch(_CTRL_PATCH) as MockCtrl,
            patch(_WALKER_PATCH) as MockWalker,
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            walker_inst = MockWalker.return_value
            walker_inst.get_reverse_deps.return_value = set()

            remover = ModuleRemover(project_root=tmp_path)
            remover.remove("old_module", no_confirm=True)

        ctrl_inst.sync.assert_called_once()
        ctrl_inst.generate_workspace_file.assert_called_once()

    def test_module_not_found_returns_failure(self, tmp_path: Path) -> None:
        with patch(_CTRL_PATCH) as MockCtrl:
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = None

            from exceptions_core import ADHDError
            ctrl_inst.require_module.side_effect = ADHDError(
                "Module 'nonexistent' not found."
            )

            remover = ModuleRemover(project_root=tmp_path)
            result = remover.remove("nonexistent")

        assert result.success is False
        assert "not found" in result.message.lower()


# ===========================================================================
# ModuleUpdater tests
# ===========================================================================


class TestModuleUpdaterDryRun:
    """Dry-run should print preview and make no modifications."""

    def test_dry_run_returns_success(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "my_widget")
        module = _make_module_info(
            "my_widget", path=module_dir, repo_url="https://github.com/org/my-widget.git"
        )

        with patch(_UPDATER_CTRL_PATCH) as MockCtrl:
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", dry_run=True)

        assert result.success is True
        assert "dry-run" in result.message.lower() or "Dry-run" in result.message

    def test_dry_run_does_not_call_sync(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "my_widget")
        module = _make_module_info(
            "my_widget", path=module_dir, repo_url="https://github.com/org/my-widget.git"
        )

        with patch(_UPDATER_CTRL_PATCH) as MockCtrl:
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            updater.update("my_widget", dry_run=True)

        ctrl_inst.sync.assert_not_called()
        ctrl_inst.generate_workspace_file.assert_not_called()


class TestModuleUpdaterValidation:
    """Validation checks before update."""

    def test_no_repo_url_returns_failure(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "local_module")
        module = _make_module_info("local_module", path=module_dir, repo_url=None)

        with patch(_UPDATER_CTRL_PATCH) as MockCtrl:
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("local_module")

        assert result.success is False
        assert "no source URL" in result.message

    def test_local_changes_blocks_without_force(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "dirty_module")
        module = _make_module_info(
            "dirty_module", path=module_dir, repo_url="https://github.com/org/dirty.git"
        )

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch.object(ModuleUpdater, "_has_local_changes", return_value=True),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("dirty_module")

        assert result.success is False
        assert "local changes" in result.message.lower()

    def test_module_not_found_returns_failure(self, tmp_path: Path) -> None:
        from exceptions_core import ADHDError

        with patch(_UPDATER_CTRL_PATCH) as MockCtrl:
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = None
            ctrl_inst.require_module.side_effect = ADHDError(
                "Module 'ghost' not found."
            )

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("ghost")

        assert result.success is False
        assert "not found" in result.message.lower()


class TestModuleUpdaterRollback:
    """Rollback should restore old module when sync fails."""

    def test_rollback_restores_module_dir_on_sync_failure(self, tmp_path: Path) -> None:
        """Simulate: clone succeeds, validate succeeds, swap succeeds, sync fails.

        After rollback the original module directory and root pyproject.toml
        should be restored.
        """
        from exceptions_core import ADHDError

        # Setup: real module dir + root pyproject
        module_dir = _create_module_dir(tmp_path, "my_widget", version="1.0.0")
        original_pyproject = _create_root_pyproject(tmp_path, package_name="my-widget")
        original_content = original_pyproject.read_text()

        module = _make_module_info(
            "my_widget",
            path=module_dir,
            version="1.0.0",
            repo_url="https://github.com/org/my-widget.git",
        )

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch("module_lifecycle_core._git_utils.subprocess.run", side_effect=_fake_clone_side_effect),
            patch.object(ModuleUpdater, "_has_local_changes", return_value=False),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module
            ctrl_inst.sync.side_effect = ADHDError("uv sync failed: dependency conflict")

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", force=True)

        assert result.success is False
        assert result.rollback_performed is True
        assert module_dir.exists(), "Module dir should be restored after rollback"

        # pyproject.toml should be restored
        restored_content = original_pyproject.read_text()
        assert restored_content == original_content


class TestModuleUpdaterSuccess:
    """Successful update scenario."""

    def test_successful_update_swaps_module(self, tmp_path: Path) -> None:
        """Simulate a full successful update cycle."""
        module_dir = _create_module_dir(tmp_path, "my_widget", version="1.0.0")
        _create_root_pyproject(tmp_path, package_name="my-widget")

        module = _make_module_info(
            "my_widget",
            path=module_dir,
            version="1.0.0",
            repo_url="https://github.com/org/my-widget.git",
        )

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch("module_lifecycle_core._git_utils.subprocess.run", side_effect=_fake_clone_side_effect),
            patch.object(ModuleUpdater, "_has_local_changes", return_value=False),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", force=True)

        assert result.success is True
        assert result.new_version == "2.0.0"
        assert result.old_version == "1.0.0"
        assert module_dir.exists()

        # The old .bak should be cleaned up
        bak_dir = module_dir.parent / "my_widget.bak"
        assert not bak_dir.exists(), ".bak should be cleaned after success"

        # Verify controller calls
        ctrl_inst.sync.assert_called_once()
        ctrl_inst.generate_workspace_file.assert_called_once()

    def test_keep_backup_preserves_bak(self, tmp_path: Path) -> None:
        module_dir = _create_module_dir(tmp_path, "my_widget", version="1.0.0")
        _create_root_pyproject(tmp_path, package_name="my-widget")

        module = _make_module_info(
            "my_widget",
            path=module_dir,
            version="1.0.0",
            repo_url="https://github.com/org/my-widget.git",
        )

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch("module_lifecycle_core._git_utils.subprocess.run", side_effect=_fake_clone_side_effect),
            patch.object(ModuleUpdater, "_has_local_changes", return_value=False),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", keep_backup=True, force=True)

        assert result.success is True
        bak_dir = module_dir.parent / "my_widget.bak"
        assert bak_dir.exists(), "--keep-backup should preserve .bak directory"


class TestModuleUpdaterSubfolderUrl:
    """Update from monorepo subfolder URL should clone full repo and extract subfolder."""

    def test_subfolder_url_extracts_module(self, tmp_path: Path) -> None:
        """Simulate: module.repo_url is a /tree/main/... browser URL.

        MOCKS: subprocess.run creates a monorepo-style directory with the module
        nested inside a subfolder. parse_github_url decomposes the URL and the
        updater clones the full repo then extracts only the subfolder.
        """
        module_dir = _create_module_dir(tmp_path, "my_widget", version="1.0.0")
        _create_root_pyproject(tmp_path, package_name="my-widget")

        monorepo_url = (
            "https://github.com/org/monorepo/tree/main/packages/my_widget"
        )
        module = _make_module_info(
            "my_widget",
            path=module_dir,
            version="1.0.0",
            repo_url=monorepo_url,
        )

        def _monorepo_clone_side_effect(
            cmd: list[str],
            *,
            capture_output: bool,
            text: bool,
            timeout: int,
        ) -> MagicMock:
            """Simulate cloning a monorepo: create packages/my_widget/ inside dest.

            MOCK: Replaces ``git clone``. Creates monorepo layout with module
            in a subfolder. RISK: Real monorepo might have different structure.
            """
            dest = Path(cmd[-1])
            dest.mkdir(parents=True, exist_ok=True)
            widget_dir = dest / "packages" / "my_widget"
            widget_dir.mkdir(parents=True)
            (widget_dir / "__init__.py").write_text('"""cloned."""\n')
            (widget_dir / "pyproject.toml").write_text(
                '[project]\nname = "my-widget"\nversion = "2.0.0"\n'
                'dependencies = []\n\n[tool.adhd]\nlayer = "runtime"\n'
            )
            (dest / ".git").mkdir()
            result = MagicMock()
            result.returncode = 0
            return result

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch(
                "module_lifecycle_core._git_utils.subprocess.run",
                side_effect=_monorepo_clone_side_effect,
            ),
            patch.object(ModuleUpdater, "_has_local_changes", return_value=False),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", force=True)

        assert result.success is True
        assert result.new_version == "2.0.0"
        assert module_dir.exists()

    def test_subfolder_url_with_cli_branch_override(self, tmp_path: Path) -> None:
        """CLI --branch should override branch parsed from URL.

        MOCKS: subprocess.run — verifies that the branch passed to git clone
        is the CLI override, not the URL-parsed branch.
        """
        module_dir = _create_module_dir(tmp_path, "my_widget", version="1.0.0")
        _create_root_pyproject(tmp_path, package_name="my-widget")

        monorepo_url = (
            "https://github.com/org/monorepo/tree/main/packages/my_widget"
        )
        module = _make_module_info(
            "my_widget",
            path=module_dir,
            version="1.0.0",
            repo_url=monorepo_url,
        )

        clone_args_captured: list[list[str]] = []

        def _capture_clone(
            cmd: list[str],
            *,
            capture_output: bool,
            text: bool,
            timeout: int,
        ) -> MagicMock:
            """Capture git clone args and create monorepo layout.

            MOCK: Records the exact git clone command for branch assertion.
            """
            clone_args_captured.append(list(cmd))
            dest = Path(cmd[-1])
            dest.mkdir(parents=True, exist_ok=True)
            widget_dir = dest / "packages" / "my_widget"
            widget_dir.mkdir(parents=True)
            (widget_dir / "__init__.py").write_text('"""cloned."""\n')
            (widget_dir / "pyproject.toml").write_text(
                '[project]\nname = "my-widget"\nversion = "2.0.0"\n'
                'dependencies = []\n\n[tool.adhd]\nlayer = "runtime"\n'
            )
            (dest / ".git").mkdir()
            result = MagicMock()
            result.returncode = 0
            return result

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch(
                "module_lifecycle_core._git_utils.subprocess.run",
                side_effect=_capture_clone,
            ),
            patch.object(ModuleUpdater, "_has_local_changes", return_value=False),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", branch="dev", force=True)

        assert result.success is True
        # Verify git clone used "--branch dev" not "--branch main"
        assert "--branch" in clone_args_captured[0]
        branch_idx = clone_args_captured[0].index("--branch")
        assert clone_args_captured[0][branch_idx + 1] == "dev"

    def test_subfolder_not_found_returns_failure(self, tmp_path: Path) -> None:
        """If parsed subfolder doesn't exist in clone, update should fail.

        MOCKS: subprocess.run creates an empty repo (no subfolder).
        """
        module_dir = _create_module_dir(tmp_path, "my_widget", version="1.0.0")
        _create_root_pyproject(tmp_path, package_name="my-widget")

        monorepo_url = (
            "https://github.com/org/monorepo/tree/main/packages/my_widget"
        )
        module = _make_module_info(
            "my_widget",
            path=module_dir,
            version="1.0.0",
            repo_url=monorepo_url,
        )

        def _empty_clone(
            cmd: list[str],
            *,
            capture_output: bool,
            text: bool,
            timeout: int,
        ) -> MagicMock:
            """Clone creates an empty repo (no packages/ directory).

            MOCK: Simulates a repo that doesn't contain the expected subfolder.
            """
            dest = Path(cmd[-1])
            dest.mkdir(parents=True, exist_ok=True)
            (dest / ".git").mkdir()
            result = MagicMock()
            result.returncode = 0
            return result

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch(
                "module_lifecycle_core._git_utils.subprocess.run",
                side_effect=_empty_clone,
            ),
            patch.object(ModuleUpdater, "_has_local_changes", return_value=False),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", force=True)

        assert result.success is False
        assert "not found" in result.message.lower()

    def test_plain_git_url_still_works(self, tmp_path: Path) -> None:
        """Standard .git URL (no /tree/) should work exactly as before.

        MOCKS: subprocess.run creates a standalone module (no subfolder).
        """
        module_dir = _create_module_dir(tmp_path, "my_widget", version="1.0.0")
        _create_root_pyproject(tmp_path, package_name="my-widget")

        module = _make_module_info(
            "my_widget",
            path=module_dir,
            version="1.0.0",
            repo_url="https://github.com/org/my-widget.git",
        )

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch(
                "module_lifecycle_core._git_utils.subprocess.run",
                side_effect=_fake_clone_side_effect,
            ),
            patch.object(ModuleUpdater, "_has_local_changes", return_value=False),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.get_module_by_name.return_value = module

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.update("my_widget", force=True)

        assert result.success is True
        assert result.new_version == "2.0.0"


# ===========================================================================
# BatchUpdateResult / batch_update tests
# ===========================================================================


class TestBatchUpdateResult:
    """BatchUpdateResult dataclass sanity checks."""

    def test_defaults(self) -> None:
        result = BatchUpdateResult()
        assert result.succeeded == []
        assert result.failed == []
        assert result.skipped == []
        assert result.total == 0

    def test_fields_populated(self) -> None:
        ok = UpdateResult(success=True, module_name="a", message="ok")
        fail = UpdateResult(success=False, module_name="b", message="fail")
        skip = UpdateResult(success=False, module_name="c", message="skip")
        result = BatchUpdateResult(
            succeeded=[ok], failed=[fail], skipped=[skip], total=3
        )
        assert len(result.succeeded) == 1
        assert len(result.failed) == 1
        assert len(result.skipped) == 1
        assert result.total == 3


class TestBatchUpdateRuntimeRejection:
    """Runtime layer must be rejected at the controller level."""

    def test_runtime_raises_adhd_error(self, tmp_path: Path) -> None:
        from exceptions_core import ADHDError

        updater = ModuleUpdater(project_root=tmp_path)
        with pytest.raises(ADHDError, match="Runtime modules are project-specific"):
            updater.batch_update("runtime")


class TestBatchUpdateDryRun:
    """Batch dry-run should preview without changes."""

    def test_batch_dry_run_succeeds(self, tmp_path: Path) -> None:
        mod_a = _make_module_info(
            "mod_a", layer_value="foundation",
            path=tmp_path / "modules" / "foundation" / "mod_a",
            repo_url="https://github.com/org/mod-a.git",
        )
        mod_b = _make_module_info(
            "mod_b", layer_value="foundation",
            path=tmp_path / "modules" / "foundation" / "mod_b",
            repo_url="https://github.com/org/mod-b.git",
        )

        report = MagicMock()
        report.modules = [mod_a, mod_b]

        with patch(_UPDATER_CTRL_PATCH) as MockCtrl:
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.list_all_modules.return_value = report
            ctrl_inst.get_module_by_name.side_effect = lambda name: {
                "mod_a": mod_a, "mod_b": mod_b
            }.get(name)

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.batch_update("foundation", dry_run=True)

        assert result.total == 2
        assert len(result.succeeded) == 2
        assert len(result.failed) == 0
        # Sync and workspace should NOT be called in dry-run
        ctrl_inst.sync.assert_not_called()
        ctrl_inst.generate_workspace_file.assert_not_called()


class TestBatchUpdateSkipNoRepoUrl:
    """Modules without repo_url should be skipped, not failed."""

    def test_skips_modules_without_repo_url(self, tmp_path: Path) -> None:
        mod_with = _make_module_info(
            "mod_with", layer_value="dev",
            path=tmp_path / "modules" / "dev" / "mod_with",
            repo_url="https://github.com/org/mod-with.git",
        )
        mod_without = _make_module_info(
            "mod_without", layer_value="dev",
            path=tmp_path / "modules" / "dev" / "mod_without",
            repo_url=None,
        )

        report = MagicMock()
        report.modules = [mod_with, mod_without]

        with patch(_UPDATER_CTRL_PATCH) as MockCtrl:
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.list_all_modules.return_value = report
            ctrl_inst.get_module_by_name.side_effect = lambda name: {
                "mod_with": mod_with, "mod_without": mod_without
            }.get(name)

            updater = ModuleUpdater(project_root=tmp_path)
            result = updater.batch_update("dev", dry_run=True)

        assert len(result.skipped) == 1
        assert result.skipped[0].module_name == "mod_without"
        assert len(result.succeeded) == 1
        assert result.succeeded[0].module_name == "mod_with"


class TestBatchUpdateContinueOnError:
    """--continue-on-error should process remaining modules after a failure."""

    def test_stops_on_first_failure_by_default(self, tmp_path: Path) -> None:
        mod_a = _make_module_info(
            "mod_a", layer_value="foundation",
            path=tmp_path / "modules" / "foundation" / "mod_a",
            repo_url="https://github.com/org/mod-a.git",
        )
        mod_b = _make_module_info(
            "mod_b", layer_value="foundation",
            path=tmp_path / "modules" / "foundation" / "mod_b",
            repo_url="https://github.com/org/mod-b.git",
        )

        report = MagicMock()
        report.modules = [mod_a, mod_b]

        def side_get(name: str):
            return {"mod_a": mod_a, "mod_b": mod_b}.get(name)

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch.object(
                ModuleUpdater, "_has_local_changes", return_value=True
            ),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.list_all_modules.return_value = report
            ctrl_inst.get_module_by_name.side_effect = side_get

            updater = ModuleUpdater(project_root=tmp_path)
            # force=False: local changes will cause failure
            result = updater.batch_update("foundation", continue_on_error=False)

        # Should stop after first failure — mod_b never attempted
        assert len(result.failed) == 1
        assert result.failed[0].module_name == "mod_a"
        # mod_b was never tried (break on first error)
        assert len(result.succeeded) == 0

    def test_continues_on_error_when_flag_set(self, tmp_path: Path) -> None:
        mod_a = _make_module_info(
            "mod_a", layer_value="foundation",
            path=tmp_path / "modules" / "foundation" / "mod_a",
            repo_url="https://github.com/org/mod-a.git",
        )
        mod_b = _make_module_info(
            "mod_b", layer_value="foundation",
            path=tmp_path / "modules" / "foundation" / "mod_b",
            repo_url="https://github.com/org/mod-b.git",
        )

        report = MagicMock()
        report.modules = [mod_a, mod_b]

        def side_get(name: str):
            return {"mod_a": mod_a, "mod_b": mod_b}.get(name)

        with (
            patch(_UPDATER_CTRL_PATCH) as MockCtrl,
            patch.object(
                ModuleUpdater, "_has_local_changes", return_value=True
            ),
        ):
            ctrl_inst = MockCtrl.return_value
            ctrl_inst.list_all_modules.return_value = report
            ctrl_inst.get_module_by_name.side_effect = side_get

            updater = ModuleUpdater(project_root=tmp_path)
            # force=False → both fail due to local changes
            result = updater.batch_update(
                "foundation", continue_on_error=True
            )

        # Both modules attempted
        assert len(result.failed) == 2
        assert result.failed[0].module_name == "mod_a"
        assert result.failed[1].module_name == "mod_b"
