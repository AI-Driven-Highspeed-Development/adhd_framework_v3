"""Module Remover - Remove modules from the ADHD workspace.

Provides the reverse of ``adhd add``: unregisters a module from pyproject.toml,
optionally deletes its directory, runs ``uv sync``, and regenerates the
workspace file.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Set

from exceptions_core import ADHDError
from logger_util import Logger

from .pyproject_patcher import remove_from_root_pyproject

if TYPE_CHECKING:
    from modules_controller_core.modules_controller import ModuleInfo


@dataclass
class RemoveResult:
    """Result of a remove-module operation."""

    success: bool
    module_name: str
    layer: Optional[str] = None
    reverse_deps: Set[str] = field(default_factory=set)
    message: str = ""


class ModuleRemover:
    """Removes modules from the ADHD workspace."""

    def __init__(self, project_root: Optional[Path] = None) -> None:
        self.project_root = (project_root or Path.cwd()).resolve()
        self.logger = Logger(name=__class__.__name__)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def remove(
        self,
        module_name: str,
        *,
        dry_run: bool = False,
        force: bool = False,
        keep_dir: bool = False,
        no_confirm: bool = False,
    ) -> RemoveResult:
        """Remove a module from the workspace.

        Sequence:
            1. Find module via ModulesController
            2. Check reverse deps via DependencyWalker
            3. Refuse if dependents exist (unless *force*)
            4. Dry-run preview → return without changes
            5. Confirmation prompt (unless *no_confirm*)
            6. Unregister from pyproject.toml
            7. Delete module directory (unless *keep_dir*)
            8. ``uv sync``
            9. Regenerate workspace file

        Args:
            module_name: Module name (snake_case or kebab-case).
            dry_run: If True, print preview and return without changes.
            force: If True, allow removal even when other modules depend on it.
            keep_dir: If True, unregister but do **not** delete the directory.
            no_confirm: If True, skip interactive confirmation prompt.

        Returns:
            RemoveResult with outcome details.
        """
        from modules_controller_core import ModulesController
        from modules_controller_core.dependency_walker import DependencyWalker

        controller = ModulesController(self.project_root)

        # 1. Find module
        module = controller.get_module_by_name(module_name)
        if module is None:
            # Use require_module for fuzzy-match error message
            try:
                module = controller.require_module(module_name)
            except ADHDError as e:
                return RemoveResult(success=False, module_name=module_name, message=str(e))

        package_name = module.name.replace("_", "-")
        layer_str = module.layer.value if module.layer else "unknown"

        # 2. Check reverse dependencies
        walker = DependencyWalker(controller)
        reverse_deps = walker.get_reverse_deps(module.name)

        # 3. Refuse if dependents exist (unless --force)
        if reverse_deps and not force:
            dep_list = ", ".join(sorted(reverse_deps))
            return RemoveResult(
                success=False,
                module_name=module.name,
                layer=layer_str,
                reverse_deps=reverse_deps,
                message=(
                    f"Cannot remove '{module.name}' — the following modules depend on it: "
                    f"{dep_list}. Use --force to remove anyway."
                ),
            )

        # 4. Dry-run preview
        if dry_run:
            self._print_dry_run(module, reverse_deps, keep_dir)
            return RemoveResult(
                success=True,
                module_name=module.name,
                layer=layer_str,
                reverse_deps=reverse_deps,
                message="Dry-run complete — no changes made.",
            )

        # 5. Confirmation prompt (unless --no-confirm)
        if not no_confirm:
            if not self._confirm_removal(module, reverse_deps, keep_dir):
                return RemoveResult(
                    success=False,
                    module_name=module.name,
                    layer=layer_str,
                    reverse_deps=reverse_deps,
                    message="Removal cancelled by user.",
                )

        # 6. Unregister from pyproject.toml (idempotent)
        self.logger.info(f"📝 Unregistering '{package_name}' from root pyproject.toml...")
        try:
            remove_from_root_pyproject(package_name, self.project_root)
        except ADHDError as e:
            return RemoveResult(
                success=False,
                module_name=module.name,
                layer=layer_str,
                reverse_deps=reverse_deps,
                message=f"Failed to unregister from pyproject.toml: {e}",
            )

        # 7. Delete module directory (unless --keep-dir)
        if not keep_dir:
            self.logger.info(f"🗑️  Deleting {module.path}...")
            try:
                shutil.rmtree(module.path)
            except OSError as e:
                return RemoveResult(
                    success=False,
                    module_name=module.name,
                    layer=layer_str,
                    reverse_deps=reverse_deps,
                    message=f"Failed to delete module directory: {e}",
                )
        else:
            self.logger.info(f"📂 Keeping directory: {module.path} (--keep-dir)")

        # 8. uv sync
        self.logger.info("🔄 Running uv sync...")
        sync_warning = ""
        try:
            controller.sync()
        except ADHDError as e:
            self.logger.warning(
                f"⚠️  uv sync failed after removing '{module.name}': {e}. "
                "Run 'adhd sync' manually to finish cleanup."
            )
            sync_warning = " (warning: uv sync failed — run 'adhd sync' manually)"

        # 9. Regenerate workspace
        self.logger.info("🔄 Regenerating workspace file...")
        controller.generate_workspace_file()

        action = "unregistered (directory kept)" if keep_dir else "removed"
        self.logger.info(f"✅ Module '{module.name}' {action} successfully.")
        return RemoveResult(
            success=True,
            module_name=module.name,
            layer=layer_str,
            reverse_deps=reverse_deps,
            message=f"Module '{module.name}' {action} successfully.{sync_warning}",
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _print_dry_run(
        self,
        module: "ModuleInfo",
        reverse_deps: Set[str],
        keep_dir: bool,
    ) -> None:
        """Print a dry-run preview of the removal."""
        package_name = module.name.replace("_", "-")
        layer_str = module.layer.value if module.layer else "unknown"

        file_count = sum(1 for _ in module.path.rglob("*") if _.is_file()) if module.path.exists() else 0

        lines = [
            "",
            f"🔍 Dry-run: adhd remove {module.name}",
            "",
            f"  Module:    {module.name}",
            f"  Layer:     {layer_str}",
            f"  Path:      {module.path}",
            "",
            "  Changes:",
            f'    ✂️  Remove "{package_name}" from pyproject.toml dependencies',
            f"    ✂️  Remove {package_name} = {{ workspace = true }} from [tool.uv.sources]",
        ]
        if keep_dir:
            lines.append(f"    📂 Keep directory {module.path} (--keep-dir)")
        else:
            lines.append(f"    🗑️  Delete {module.path} ({file_count} files)")
        lines.append("    🔄 Run uv sync")
        lines.append("    🔄 Regenerate .code-workspace")

        if reverse_deps:
            dep_list = ", ".join(sorted(reverse_deps))
            lines.append("")
            lines.append(f"  ⚠️  Reverse dependencies: {dep_list}")
            lines.append("      Use --force to remove anyway.")

        lines.append("")
        lines.append("  No changes made (dry-run mode).")
        self.logger.info("\n".join(lines))

    def _confirm_removal(
        self,
        module: "ModuleInfo",
        reverse_deps: Set[str],
        keep_dir: bool,
    ) -> bool:
        """Show summary and ask for confirmation. Returns True to proceed."""
        layer_str = module.layer.value if module.layer else "unknown"
        file_count = sum(1 for _ in module.path.rglob("*") if _.is_file()) if module.path.exists() else 0

        action = "unregister (keep files)" if keep_dir else f"delete {file_count} files in {module.path}"
        self.logger.info(f"\n  About to remove: {module.name} ({layer_str})")
        self.logger.info(f"  This will {action}")

        if reverse_deps:
            dep_list = ", ".join(sorted(reverse_deps))
            self.logger.warning(f"  ⚠️  These modules depend on it: {dep_list}")

        try:
            answer = input("\n  Continue? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        return answer in ("y", "yes")
