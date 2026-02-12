"""Module Adder - Core logic for adding external modules to the ADHD workspace.

Supports:
- Mode 1: Standalone repository (whole repo is one module)
- Mode 2: Monorepo subfolder (extract a subfolder from a larger repo)
- Mode 3: PyPI package (future, not yet implemented)
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from exceptions_core import ADHDError
from logger_util import Logger

from .pyproject_patcher import add_to_root_pyproject
from .pyproject_scaffolder import scaffold_pyproject
from ._git_utils import clone_repo, parse_github_url


@dataclass
class AddModuleResult:
    """Result of an add-module operation."""
    success: bool
    module_name: str
    target_path: Optional[Path] = None
    layer: Optional[str] = None
    message: str = ""


# Git-related items to remove by default (unless --keep-git)
# Note: .gitignore and .gitattributes are always preserved (not in this list).
_GIT_ITEMS_TO_REMOVE = [".git", ".github", ".gitmodules"]


class ModuleAdder:
    """Adds external modules to the ADHD workspace."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = (project_root or Path.cwd()).resolve()
        self.logger = Logger(name=__class__.__name__)

    def add_from_repo(
        self,
        repo_url: str,
        subfolder: Optional[str] = None,
        *,
        keep_git: bool = False,
        add_to_root: Optional[bool] = None,
        skip_prompt: bool = False,
    ) -> AddModuleResult:
        """Clone a repo (or subfolder) and install as workspace module.

        Args:
            repo_url: Git repository URL.
            subfolder: If provided, extract only this subfolder (Mode 2).
            keep_git: If True, preserve .git/ directory.
            add_to_root: If True, add to root pyproject.toml. None = ask user.
            skip_prompt: If True, skip all prompts and use defaults.

        Returns:
            AddModuleResult with success/failure info.
        """
        # Parse URL to handle GitHub browser URLs with embedded subfolder
        parsed = parse_github_url(repo_url)

        # Conflict: URL contains subfolder AND explicit --path also provided
        if parsed.subfolder and subfolder:
            return AddModuleResult(
                success=False,
                module_name="",
                message=(
                    f"Conflicting subfolder: URL contains path '{parsed.subfolder}' "
                    f"but --path '{subfolder}' was also provided. Use one or the other."
                ),
            )

        effective_subfolder = subfolder or parsed.subfolder
        effective_url = parsed.clone_url

        # Validate URL format
        if not (effective_url.startswith("http://") or effective_url.startswith("https://")):
            return AddModuleResult(
                success=False,
                module_name="",
                message="Invalid URL format. Must start with http:// or https://",
            )

        # Infer module name from subfolder (last component) or clone URL
        if effective_subfolder:
            inferred_name = effective_subfolder.rstrip("/").split("/")[-1]
        else:
            inferred_name = effective_url.rstrip("/").removesuffix(".git").split("/")[-1]
        inferred_name = inferred_name.lower().replace("-", "_")

        self.logger.info(f"\U0001f4e5 Adding module from: {repo_url}")

        temp_dir = Path(tempfile.mkdtemp(prefix=f"adhd_{inferred_name}_"))
        try:
            # Clone the repository
            self.logger.info("🔄 Cloning repository...")
            clone_path = clone_repo(effective_url, temp_dir / inferred_name, branch=parsed.branch)

            # Determine the source directory (whole clone or subfolder)
            if effective_subfolder:
                source_dir = clone_path / effective_subfolder
                if not source_dir.exists() or not source_dir.is_dir():
                    return AddModuleResult(
                        success=False,
                        module_name=inferred_name,
                        message=f"Subfolder not found in repository: {effective_subfolder}",
                    )
            else:
                source_dir = clone_path

            # Ensure pyproject.toml exists (or scaffold one)
            pyproject_path = source_dir / "pyproject.toml"
            if not pyproject_path.exists():
                scaffold_pyproject(source_dir, skip_prompt=skip_prompt)

            # Read and validate pyproject.toml
            result = self._read_and_validate_pyproject(source_dir)
            if not result["valid"]:
                return AddModuleResult(
                    success=False,
                    module_name=inferred_name,
                    message=result["error"],
                )

            package_name = result["package_name"]
            module_name = result["module_name"]
            layer = result["layer"]

            # Check collision
            target_dir = self.project_root / "modules" / layer / module_name
            if target_dir.exists():
                return AddModuleResult(
                    success=False,
                    module_name=module_name,
                    message=f"Module already exists at: {target_dir}",
                )

            # Strip git info (unless --keep-git)
            if not keep_git:
                self._strip_git_info(source_dir)

            # Move to target
            self.logger.info(f"\U0001f4c2 Moving to: {target_dir}")
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_dir), str(target_dir))

            # Run uv sync to register workspace member
            self.logger.info("\U0001f504 Running uv sync to register workspace member...")
            from modules_controller_core import ModulesController
            controller = ModulesController(self.project_root)
            controller.sync()
            self.logger.info("\u2705 Module registered in workspace")

            # Optionally add to root pyproject.toml
            should_add = add_to_root
            if should_add is None and not skip_prompt:
                from creator_common_core import QuestionaryCore
                prompter = QuestionaryCore()
                should_add = prompter.confirm(
                    f"Add '{package_name}' to root dependencies (needed if adhd CLI imports it)?",
                    default=False,
                )

            if should_add:
                self.logger.info(f"\U0001f4dd Adding '{package_name}' to root pyproject.toml...")
                add_to_root_pyproject(package_name, self.project_root)
                self.logger.info("\U0001f504 Running uv sync to update dependencies...")
                controller.sync()

            return AddModuleResult(
                success=True,
                module_name=module_name,
                target_path=target_dir,
                layer=layer,
                message=f"Module '{module_name}' added successfully at {target_dir}",
            )

        except ADHDError as e:
            return AddModuleResult(
                success=False,
                module_name=inferred_name,
                message=str(e),
            )
        except subprocess.TimeoutExpired:
            return AddModuleResult(
                success=False,
                module_name=inferred_name,
                message="git clone timed out",
            )
        except Exception as e:
            # FALLBACK: catch-all for unexpected errors (permissions, network, etc.) — permanent — CLI must not crash
            return AddModuleResult(
                success=False,
                module_name=inferred_name,
                message=f"Unexpected error: {e}",
            )
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def add_from_pypi(self, package_name: str) -> AddModuleResult:
        """Install from PyPI. Currently not implemented."""
        raise NotImplementedError(
            "PyPI mode is not yet available. No ADHD-compatible packages exist on PyPI."
        )

    def _read_and_validate_pyproject(self, source_dir: Path) -> Dict[str, Any]:
        """Read pyproject.toml from source_dir and validate it.

        Returns a dict with 'valid', 'package_name', 'module_name', 'layer', 'error'.
        """
        pyproject_path = source_dir / "pyproject.toml"
        try:
            with pyproject_path.open("rb") as f:
                data = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            return {"valid": False, "error": f"Invalid pyproject.toml: {e}"}

        package_name = data.get("project", {}).get("name")
        if not package_name:
            return {"valid": False, "error": "pyproject.toml missing [project] name field"}

        layer = data.get("tool", {}).get("adhd", {}).get("layer", "runtime")
        valid_layers = ["foundation", "runtime", "dev"]
        if layer not in valid_layers:
            return {
                "valid": False,
                "error": f"Unknown layer '{layer}' in pyproject.toml. Expected one of: {valid_layers}",
            }

        module_name = package_name.lower().replace("-", "_")
        self.logger.info(f"\U0001f4ca Layer: {layer}")
        self.logger.info(f"\U0001f3f7\ufe0f  Package name: {package_name}")

        return {
            "valid": True,
            "package_name": package_name,
            "module_name": module_name,
            "layer": layer,
            "error": None,
        }

    def _strip_git_info(self, directory: Path) -> None:
        """Remove git-related directories/files, preserving .gitignore and .gitattributes."""
        for item_name in _GIT_ITEMS_TO_REMOVE:
            item_path = directory / item_name
            if item_path.exists():
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                else:
                    item_path.unlink()
                self.logger.debug(f"Removed {item_name} from {directory}")
