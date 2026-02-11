"""Module Updater - Update modules via atomic swap.

Clone the latest version to a temp directory, validate, swap the old module
directory with the new one, and run ``uv sync``.  On failure the old directory
is restored from a ``.bak`` backup.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from exceptions_core import ADHDError
from logger_util import Logger

from ._git_utils import clone_repo

if TYPE_CHECKING:
    from modules_controller_core.modules_controller import ModulesController, ModuleInfo


@dataclass
class UpdateResult:
    """Result of an update-module operation."""

    success: bool
    module_name: str
    old_version: Optional[str] = None
    new_version: Optional[str] = None
    message: str = ""
    rollback_performed: bool = False


@dataclass
class BatchUpdateResult:
    """Result of a batch update operation across multiple modules."""

    succeeded: List[UpdateResult] = field(default_factory=list)
    failed: List[UpdateResult] = field(default_factory=list)
    skipped: List[UpdateResult] = field(default_factory=list)
    total: int = 0


class ModuleUpdater:
    """Updates modules via an atomic directory swap.

    Sequence:
        1. Find module, get ``ModuleInfo.repo_url``
        2. Error if no ``repo_url``
        3. Check for local modifications (unless ``--force``)
        4. Dry-run preview → return without changes
        5. Clone new version to temp dir
        6. Validate new module (valid pyproject.toml, matching package name)
        7. Backup: ``pyproject.toml`` → ``pyproject.toml.bak``
        8. Swap: old dir → ``{name}.bak``, new dir → target
        9. ``uv sync``
       10. On SUCCESS: delete ``.bak`` (unless ``--keep-backup``)
       11. On FAILURE: rollback from ``.bak``, report error
       12. Regenerate workspace file
    """

    def __init__(self, project_root: Optional[Path] = None) -> None:
        self.project_root = (project_root or Path.cwd()).resolve()
        self.logger = Logger(name=__class__.__name__)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update(
        self,
        module_name: str,
        *,
        dry_run: bool = False,
        branch: Optional[str] = None,
        keep_backup: bool = False,
        force: bool = False,
        skip_post_steps: bool = False,
    ) -> UpdateResult:
        """Update a module to the latest version via atomic swap.

        Args:
            module_name: Module name (snake_case or kebab-case).
            dry_run: If True, print preview and return without changes.
            branch: Optional git branch to clone from.
            keep_backup: If True, keep the ``.bak`` directory after success.
            force: If True, allow update even with uncommitted local changes.
            skip_post_steps: If True, skip ``controller.sync()`` and
                ``controller.generate_workspace_file()`` after the swap.
                Used by ``batch_update()`` to defer these to a single
                post-loop invocation.

        Returns:
            UpdateResult with outcome details.
        """
        from modules_controller_core import ModulesController

        controller = ModulesController(self.project_root)

        # 1. Find module
        module = controller.get_module_by_name(module_name)
        if module is None:
            try:
                module = controller.require_module(module_name)
            except ADHDError as e:
                return UpdateResult(success=False, module_name=module_name, message=str(e))

        old_version = module.version

        # 2. Check for repo_url
        if not module.repo_url:
            return UpdateResult(
                success=False,
                module_name=module.name,
                old_version=old_version,
                message=(
                    f"Cannot update '{module.name}' — no source URL recorded. "
                    "Add a [project.urls] Repository entry to its pyproject.toml, "
                    "or remove and re-add with `adhd add <url>`."
                ),
            )

        # 3. Check for local modifications
        if not force and self._has_local_changes(module.path):
            return UpdateResult(
                success=False,
                module_name=module.name,
                old_version=old_version,
                message=(
                    f"Module '{module.name}' has uncommitted local changes. "
                    "Use --force to overwrite."
                ),
            )

        # 4. Dry-run preview
        if dry_run:
            self._print_dry_run(module, branch)
            return UpdateResult(
                success=True,
                module_name=module.name,
                old_version=old_version,
                message="Dry-run complete — no changes made.",
            )

        # 5–12. Clone, validate, swap, sync (with rollback on failure)
        return self._execute_update(controller, module, branch, keep_backup, skip_post_steps)

    def batch_update(
        self,
        layer: str,
        *,
        dry_run: bool = False,
        branch: Optional[str] = None,
        keep_backup: bool = False,
        force: bool = False,
        continue_on_error: bool = False,
    ) -> BatchUpdateResult:
        """Update all modules in a layer via batch operation.

        Calls ``update()`` for each module with ``skip_post_steps=True``,
        then runs ``controller.sync()`` and
        ``controller.generate_workspace_file()`` once at the end.

        Per-module semantics: if module 3 fails, modules 1–2 stay updated.
        Modules without ``repo_url`` are skipped (not failed).

        Args:
            layer: Layer to update (``"foundation"``, ``"runtime"``, ``"dev"``).
            dry_run: Preview without making changes.
            branch: Optional git branch override for all modules.
            keep_backup: Keep ``.bak`` directories after success.
            force: Update even if modules have local changes.
            continue_on_error: If False, stop on the first failure.

        Returns:
            BatchUpdateResult with per-module outcomes.

        Raises:
            ADHDError: If *layer* is ``"runtime"`` (runtime modules are
                project-specific and must be updated individually).
        """
        from modules_controller_core import ModulesController
        from modules_controller_core import ModuleLayer as LayerEnum

        if layer == "runtime":
            raise ADHDError(
                "Runtime modules are project-specific. "
                "Update them individually with 'adhd update <name>'."
            )

        controller = ModulesController(self.project_root)
        report = controller.list_all_modules()

        target_layer = LayerEnum(layer)
        layer_modules = [m for m in report.modules if m.layer == target_layer]

        if not layer_modules:
            self.logger.warning(f"No modules found in layer '{layer}'.")
            return BatchUpdateResult(total=0)

        self.logger.info(
            f"🔄 Batch update: {len(layer_modules)} module(s) in '{layer}' layer"
        )

        result = BatchUpdateResult(total=len(layer_modules))

        for module in layer_modules:
            # Modules without repo_url → skipped (not failed)
            if not module.repo_url:
                skip_result = UpdateResult(
                    success=False,
                    module_name=module.name,
                    old_version=module.version,
                    message=(
                        f"Skipped '{module.name}' — no source URL recorded."
                    ),
                )
                result.skipped.append(skip_result)
                self.logger.info(f"  ⏭️  Skipping {module.name} (no repo_url)")
                continue

            self.logger.info(f"  📥 Updating {module.name}...")
            update_result = self.update(
                module.name,
                dry_run=dry_run,
                branch=branch,
                keep_backup=keep_backup,
                force=force,
                skip_post_steps=True,
            )

            if update_result.success:
                result.succeeded.append(update_result)
                self.logger.info(f"  ✅ {module.name}: {update_result.message}")
            else:
                result.failed.append(update_result)
                self.logger.error(f"  ❌ {module.name}: {update_result.message}")
                if not continue_on_error:
                    self.logger.error(
                        "Stopping batch update (use --continue-on-error to skip failures)."
                    )
                    break

        # Post-loop: run sync + workspace regen ONCE (unless dry-run)
        if not dry_run and (result.succeeded or result.failed):
            self.logger.info("🔄 Running uv sync...")
            try:
                controller.sync()
            except ADHDError as e:
                self.logger.warning(
                    f"⚠️  uv sync failed after batch update: {e}. "
                    "Run 'adhd sync' manually to finish cleanup."
                )
            self.logger.info("🔄 Regenerating workspace file...")
            controller.generate_workspace_file()

        # Summary
        self.logger.info(
            f"\n📊 Batch update summary: "
            f"{len(result.succeeded)} succeeded, "
            f"{len(result.failed)} failed, "
            f"{len(result.skipped)} skipped "
            f"(out of {result.total})"
        )

        return result

    # ------------------------------------------------------------------
    # Private: execute the atomic swap
    # ------------------------------------------------------------------

    def _execute_update(
        self,
        controller: "ModulesController",
        module: "ModuleInfo",
        branch: Optional[str],
        keep_backup: bool,
        skip_post_steps: bool = False,
    ) -> UpdateResult:
        """Perform the clone → validate → swap → sync sequence.

        Uses ``tempfile.mkdtemp`` + ``shutil.rmtree`` in ``finally``.

        When *skip_post_steps* is True, ``controller.sync()`` and
        ``controller.generate_workspace_file()`` are skipped.  The caller
        (typically ``batch_update``) is responsible for running them once
        after the loop.
        """
        old_version = module.version
        target_dir = module.path
        backup_dir = target_dir.parent / f"{module.name}.bak"
        root_pyproject_bak = self.project_root / "pyproject.toml.bak"
        temp_dir = Path(tempfile.mkdtemp(prefix=f"adhd_update_{module.name}_"))

        try:
            # 5. Clone new version to temp dir
            self.logger.info(f"📥 Cloning latest from: {module.repo_url}")
            clone_dest = temp_dir / module.name
            clone_repo(module.repo_url, clone_dest, branch=branch)

            # 6. Validate new module
            new_pyproject = self._read_and_validate_pyproject(clone_dest, module.name)
            new_version = new_pyproject.get("version", "0.0.0")

            # Strip .git from clone (we don't keep it in workspace)
            git_dir = clone_dest / ".git"
            if git_dir.exists():
                shutil.rmtree(git_dir)

            # 7. Backup root pyproject.toml
            root_pyproject = self.project_root / "pyproject.toml"
            self.logger.info("💾 Backing up pyproject.toml...")
            shutil.copy2(root_pyproject, root_pyproject_bak)

            # 8. Swap: old → .bak, new → target
            self.logger.info(f"🔄 Swapping {module.name}...")
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.move(str(target_dir), str(backup_dir))
            shutil.move(str(clone_dest), str(target_dir))

            # 9. uv sync (skipped in batch mode)
            if not skip_post_steps:
                self.logger.info("🔄 Running uv sync...")
                try:
                    controller.sync()
                except ADHDError as sync_err:
                    # 11. FAILURE → rollback
                    self.logger.error(f"❌ uv sync failed: {sync_err}")
                    return self._rollback(
                        module.name,
                        old_version,
                        target_dir,
                        backup_dir,
                        root_pyproject,
                        root_pyproject_bak,
                        reason=str(sync_err),
                    )

            # 10. SUCCESS — cleanup .bak
            if keep_backup:
                self.logger.info(f"📂 Keeping backup: {backup_dir}")
            else:
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)
                if root_pyproject_bak.exists():
                    root_pyproject_bak.unlink()

            # 12. Regenerate workspace (skipped in batch mode)
            if not skip_post_steps:
                self.logger.info("🔄 Regenerating workspace file...")
                controller.generate_workspace_file()

            self.logger.info(
                f"✅ Module '{module.name}' updated: {old_version} → {new_version}"
            )
            return UpdateResult(
                success=True,
                module_name=module.name,
                old_version=old_version,
                new_version=new_version,
                message=f"Module '{module.name}' updated: {old_version} → {new_version}",
            )

        except ADHDError as e:
            # Something failed before swap completed — try rollback if swap started
            if backup_dir.exists() and not target_dir.exists():
                return self._rollback(
                    module.name,
                    old_version,
                    target_dir,
                    backup_dir,
                    self.project_root / "pyproject.toml",
                    root_pyproject_bak,
                    reason=str(e),
                )
            return UpdateResult(
                success=False,
                module_name=module.name,
                old_version=old_version,
                message=str(e),
            )
        except subprocess.TimeoutExpired:
            if backup_dir.exists() and not target_dir.exists():
                return self._rollback(
                    module.name,
                    old_version,
                    target_dir,
                    backup_dir,
                    self.project_root / "pyproject.toml",
                    root_pyproject_bak,
                    reason="git clone timed out",
                )
            return UpdateResult(
                success=False,
                module_name=module.name,
                old_version=old_version,
                message="git clone timed out",
            )
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

    # ------------------------------------------------------------------
    # Private: rollback
    # ------------------------------------------------------------------

    def _rollback(
        self,
        module_name: str,
        old_version: Optional[str],
        target_dir: Path,
        backup_dir: Path,
        root_pyproject: Path,
        root_pyproject_bak: Path,
        *,
        reason: str,
    ) -> UpdateResult:
        """Restore from .bak directories after a failed swap/sync."""
        self.logger.warning(f"⏪ Rolling back '{module_name}'...")

        # Restore module directory
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        if backup_dir.exists():
            shutil.move(str(backup_dir), str(target_dir))
            self.logger.info("  ✅ Module directory restored from backup.")

        # Restore pyproject.toml
        if root_pyproject_bak.exists():
            shutil.copy2(root_pyproject_bak, root_pyproject)
            root_pyproject_bak.unlink()
            self.logger.info("  ✅ pyproject.toml restored from backup.")

        return UpdateResult(
            success=False,
            module_name=module_name,
            old_version=old_version,
            message=f"Update failed ({reason}). Rolled back to previous version.",
            rollback_performed=True,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _has_local_changes(self, module_path: Path) -> bool:
        """Check if the module directory has uncommitted git changes.

        Returns False if git is not available or the directory is not a repo.
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain", "--", "."],
                cwd=module_path,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                # FALLBACK: returns False when git unavailable — permanent — module may not be a git repo
                return False
            return bool(result.stdout.strip())
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # FALLBACK: git binary missing or timed out — permanent — graceful degradation
            return False

    # JUSTIFY: different return shape — updater needs version only, adder needs full validation result
    def _read_and_validate_pyproject(
        self,
        source_dir: Path,
        expected_module_name: str,
    ) -> dict:
        """Read and validate the new module's pyproject.toml.

        Checks:
        - pyproject.toml exists and is valid TOML
        - ``[project] name`` field exists
        - Package name matches expected module name (kebab ↔ snake)

        Returns:
            Parsed project data (version, etc.).

        Raises:
            ADHDError: If validation fails.
        """
        pyproject_path = source_dir / "pyproject.toml"
        if not pyproject_path.exists():
            raise ADHDError(f"New module is missing pyproject.toml in {source_dir}")

        try:
            with pyproject_path.open("rb") as f:
                data = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise ADHDError(f"Invalid pyproject.toml in new module: {e}") from e

        project_data = data.get("project", {})
        package_name = project_data.get("name")
        if not package_name:
            raise ADHDError("New module's pyproject.toml is missing [project] name field")

        # Normalise both names: kebab → snake
        new_module_name = package_name.lower().replace("-", "_")
        if new_module_name != expected_module_name.lower().replace("-", "_"):
            raise ADHDError(
                f"Package name mismatch — expected '{expected_module_name}', "
                f"got '{package_name}'"
            )

        return {
            "version": project_data.get("version", "0.0.0"),
            "package_name": package_name,
        }

    def _print_dry_run(
        self,
        module: "ModuleInfo",
        branch: Optional[str],
    ) -> None:
        """Print a dry-run preview of the update."""
        layer_str = module.layer.value if module.layer else "unknown"
        branch_info = f" (branch: {branch})" if branch else " (HEAD)"

        lines = [
            "",
            f"🔍 Dry-run: adhd update {module.name}",
            "",
            f"  Module:    {module.name}",
            f"  Layer:     {layer_str}",
            f"  Path:      {module.path}",
            f"  Source:    {module.repo_url}{branch_info}",
            f"  Current:   v{module.version}",
            "",
            "  Steps:",
            f"    📥 Clone latest from {module.repo_url}",
            "    ✅ Validate new module (pyproject.toml, package name)",
            "    💾 Backup current module directory → .bak",
            "    🔄 Swap: old → .bak, new → target",
            "    🔄 Run uv sync",
            "    🧹 Clean up .bak on success (or rollback on failure)",
            "    🔄 Regenerate .code-workspace",
            "",
            "  No changes made (dry-run mode).",
        ]
        self.logger.info("\n".join(lines))
