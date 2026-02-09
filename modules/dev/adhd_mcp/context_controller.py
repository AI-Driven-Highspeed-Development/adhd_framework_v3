"""
Context Controller - AI context file operations for ADHD MCP.

Handles scanning and listing of instructions, agents, and prompts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from logger_util import Logger
from modules_controller_core import ModulesController


class ContextController:
    """Controller for AI context file operations."""

    def __init__(
        self,
        root_path: Path,
        modules_controller: ModulesController,
    ):
        self.root_path = root_path
        self.modules_controller = modules_controller
        self.logger = Logger(name=self.__class__.__name__)

    def list_context_files(
        self,
        file_type: str | None = None,
        include_modules: bool = True,
    ) -> dict[str, Any]:
        """List AI context files (instructions, agents, prompts).

        Args:
            file_type: Filter by type: "instruction", "agent", "prompt", or None for all
            include_modules: Include module-specific files

        Returns:
            Dict with lists of files by type
        """
        valid_types = ["instruction", "agent", "prompt", None]
        if file_type not in valid_types:
            return {
                "success": False,
                "error": "invalid_type",
                "message": f"file_type must be one of: {valid_types}",
            }

        try:
            result: dict[str, Any] = {"success": True}

            # Core paths
            core_data_path = self.root_path / "cores" / "instruction_core" / "data"
            github_path = self.root_path / ".github"

            # Scan instructions
            if file_type is None or file_type == "instruction":
                instructions = []
                # Core instructions
                instructions.extend(self._scan_files(
                    "*.instructions.md",
                    "core",
                    core_data_path / "instructions",
                ))
                # GitHub synced instructions
                instructions.extend(self._scan_files(
                    "*.instructions.md",
                    "synced",
                    github_path / "instructions",
                ))
                # Module instructions (if requested)
                if include_modules:
                    report = self.modules_controller.list_all_modules()
                    for module in report.modules:
                        instructions.extend(self._scan_files(
                            f"{module.name}.instructions.md",
                            module.name,
                            module.path,
                        ))
                result["instructions"] = instructions

            # Scan agents
            if file_type is None or file_type == "agent":
                agents = []
                # Core agents
                agents.extend(self._scan_files(
                    "*.agent.md",
                    "core",
                    core_data_path / "agents",
                ))
                # GitHub synced agents
                agents.extend(self._scan_files(
                    "*.agent.md",
                    "synced",
                    github_path / "agents",
                ))
                # Module agents
                if include_modules:
                    report = self.modules_controller.list_all_modules()
                    for module in report.modules:
                        agents.extend(self._scan_files(
                            "*.agent.md",
                            module.name,
                            module.path,
                        ))
                result["agents"] = agents

            # Scan prompts
            if file_type is None or file_type == "prompt":
                prompts = []
                # Core prompts
                prompts.extend(self._scan_files(
                    "*.prompt.md",
                    "core",
                    core_data_path / "prompts",
                ))
                # GitHub synced prompts
                prompts.extend(self._scan_files(
                    "*.prompt.md",
                    "synced",
                    github_path / "prompts",
                ))
                # Module prompts
                if include_modules:
                    report = self.modules_controller.list_all_modules()
                    for module in report.modules:
                        prompts.extend(self._scan_files(
                            "*.prompt.md",
                            module.name,
                            module.path,
                        ))
                result["prompts"] = prompts

            return result
        except Exception as e:
            return {
                "success": False,
                "error": "scan_error",
                "message": str(e),
            }

    def _scan_files(
        self,
        pattern: str,
        source: str,
        search_path: Path,
    ) -> list[dict[str, str]]:
        """Scan for files matching pattern.

        Args:
            pattern: Glob pattern to match
            source: Source identifier (e.g., "core", "synced", module name)
            search_path: Path to search in

        Returns:
            List of dicts with name, path, and source for each matched file
        """
        files = []
        if search_path.exists():
            for f in search_path.glob(pattern):
                files.append({
                    "name": f.stem,
                    "path": str(f.relative_to(self.root_path)),
                    "source": source,
                })
        return files

    def get_compilation_manifest(self) -> dict[str, Any]:
        """Read the flow compilation manifest from instruction_core.

        Returns:
            Dict with manifest data or error if manifest doesn't exist.
        """
        try:
            module = self.modules_controller.get_module_by_name("instruction_core")
            if not module:
                return {
                    "success": False,
                    "error": "module_not_found",
                    "message": "instruction_core module not found",
                }

            manifest_path = module.path / "data" / "compiled" / "compiled_manifest.json"
            if not manifest_path.exists():
                return {
                    "success": False,
                    "error": "manifest_not_found",
                    "message": "No compilation manifest found. Run 'adhd compile' or 'adhd refresh --full' first.",
                }

            content = manifest_path.read_text(encoding="utf-8")
            manifest = json.loads(content)
            manifest["success"] = True
            return manifest
        except (json.JSONDecodeError, OSError) as e:
            return {
                "success": False,
                "error": "read_error",
                "message": f"Failed to read manifest: {e}",
            }

    def list_skills(self) -> dict[str, Any]:
        """List available skills with name and description from SKILL.md frontmatter.

        Scans the skills directory in instruction_core and parses each
        skill's SKILL.md YAML frontmatter for name and description.

        Returns:
            Dict with count and list of skill dicts (name, description, path).
        """
        try:
            module = self.modules_controller.get_module_by_name("instruction_core")
            if not module:
                return {
                    "success": False,
                    "error": "module_not_found",
                    "message": "instruction_core module not found",
                }

            skills_dir = module.path / "data" / "skills"
            if not skills_dir.exists():
                return {"success": True, "count": 0, "skills": []}

            skills: list[dict[str, str]] = []
            for skill_dir in sorted(skills_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue

                skill_md = skill_dir / "SKILL.md"
                name = skill_dir.name
                description = ""

                if skill_md.exists():
                    try:
                        content = skill_md.read_text(encoding="utf-8")
                        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                        if match:
                            frontmatter = yaml.safe_load(match.group(1))
                            if isinstance(frontmatter, dict):
                                name = frontmatter.get("name", name)
                                description = frontmatter.get("description", "")
                    except (yaml.YAMLError, OSError) as e:
                        self.logger.warning(f"Failed to parse SKILL.md in {skill_dir.name}: {e}")

                skills.append({
                    "name": name,
                    "description": description,
                    "path": str(skill_dir.relative_to(self.root_path)),
                })

            return {"success": True, "count": len(skills), "skills": skills}
        except Exception as e:
            return {
                "success": False,
                "error": "scan_error",
                "message": str(e),
            }
