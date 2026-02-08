from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Optional

import yaml

from exceptions_core import ADHDError
from modules_controller_core import ModulesController
from config_manager import ConfigManager
from logger_util import Logger


# File type configurations: (pattern, subdirectory, label)
# Used by multiple sync methods to avoid repetition
FILE_TYPE_CONFIGS = (
    ("*.instructions.md", "instructions", "instruction"),
    ("*.agent.md", "agents", "agent"),
    ("*.prompt.md", "prompts", "prompt"),
)


class InstructionController:
    """
    Controller for managing instruction and agent files.
    
    Supports two sync modes via config (both accept lists of target directories):
    - official_target_dir: List of paths. Syncs from instruction_core's data directory to each target
    - custom_target_dir: List of paths. Syncs from ./project/data/instruction_core (or config path) to each target
    
    Empty lists or empty strings within lists are skipped.
    """

    def __init__(self, root_path: Optional[Path] = None, logger: Optional[Logger] = None):
        self.root_path = (root_path or Path.cwd()).resolve()
        self.logger = logger or Logger(name=__class__.__name__)
        self.modules_controller = ModulesController(root_path=self.root_path)
        
        # Load config
        cm = ConfigManager()
        self.config = cm.config.instruction_core
        
        # Official source: instruction_core/data (relative to this module)
        self.official_source_path = Path(__file__).resolve().parent / "data"
        
        # Custom source: from config path.data or default
        custom_data_path = self.config.path.data
        self.custom_source_path = (self.root_path / custom_data_path).resolve()
        
        # Target directories from config (now lists)
        official_targets = self.config.path.official_target_dir
        custom_targets = self.config.path.custom_target_dir
        
        # Convert to lists of resolved paths, filtering out empty strings
        self.official_target_paths = [
            (self.root_path / target).resolve() 
            for target in (official_targets if isinstance(official_targets, list) else [official_targets])
            if target
        ]
        self.custom_target_paths = [
            (self.root_path / target).resolve()
            for target in (custom_targets if isinstance(custom_targets, list) else [custom_targets])
            if target
        ]
        
        # MCP permission injection JSON path
        mcp_injection_path = self.config.path.dict_get("mcp_permission_injection_json")
        self.mcp_permission_injection_path = (
            (self.root_path / mcp_injection_path).resolve() if mcp_injection_path else None
        )

    def _ensure_target_structure(self, target_path: Path) -> None:
        """Ensure instructions, agents, and prompts directories exist under target path."""
        try:
            (target_path / "instructions").mkdir(parents=True, exist_ok=True)
            (target_path / "agents").mkdir(parents=True, exist_ok=True)
            (target_path / "prompts").mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Ensured target structure exists at {target_path}")
        except OSError as e:
            raise ADHDError(f"Failed to create target structure at {target_path}: {e}") from e

    def _load_mcp_permissions(self) -> dict[str, list[str]]:
        """Load MCP permission injection configuration from JSON file."""
        if not self.mcp_permission_injection_path:
            self.logger.debug("No MCP permission injection path configured.")
            return {}
        
        if not self.mcp_permission_injection_path.exists():
            self.logger.debug(f"MCP permission injection file not found: {self.mcp_permission_injection_path}")
            return {}
        
        try:
            content = self.mcp_permission_injection_path.read_text(encoding="utf-8").strip()
            if not content:
                self.logger.debug("MCP permission injection file is empty.")
                return {}
            
            permissions = json.loads(content)
            if not isinstance(permissions, dict):
                self.logger.warning("MCP permission injection file must contain a JSON object.")
                return {}
            
            self.logger.info(f"Loaded MCP permissions for {len(permissions)} agent(s).")
            return permissions
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse MCP permission injection JSON: {e}")
            return {}
        except OSError as e:
            self.logger.error(f"Failed to read MCP permission injection file: {e}")
            return {}

    def _read_agent_file(self, agent_file: Path) -> Optional[str]:
        """Read agent file content, returning None on error."""
        try:
            return agent_file.read_text(encoding="utf-8")
        except OSError as e:
            self.logger.error(f"Failed to read agent file {agent_file.name}: {e}")
            return None

    def _extract_yaml_header(self, content: str, filename: str) -> Optional[tuple[re.Match, dict]]:
        """Extract and parse YAML header from agent file content.
        
        Returns tuple of (header_match, parsed_header) or None on failure.
        """
        header_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not header_match:
            self.logger.warning(f"No YAML header found in {filename}, skipping injection.")
            return None
        
        try:
            header = yaml.safe_load(header_match.group(1))
            if not isinstance(header, dict):
                self.logger.warning(f"Invalid YAML header in {filename}, skipping injection.")
                return None
            return header_match, header
        except yaml.YAMLError as e:
            self.logger.error(f"Failed to parse YAML header in {filename}: {e}")
            return None

    def _get_new_tools_to_inject(self, header: dict, additional_tools: list[str], filename: str) -> list[str]:
        """Filter additional_tools to only those not already in header."""
        existing_tools = header.get("tools", [])
        if not isinstance(existing_tools, list):
            existing_tools = [existing_tools] if existing_tools else []
        existing_set = set(existing_tools)
        
        new_tools = [t for t in additional_tools if t not in existing_set]
        if not new_tools:
            self.logger.debug(f"No new tools to inject into {filename}, all already present.")
        return new_tools

    def _inject_mcp_permissions_to_agent(self, agent_file: Path, additional_tools: list[str]) -> None:
        """Inject additional MCP tools into an agent file's YAML header."""
        if not additional_tools:
            return
        
        content = self._read_agent_file(agent_file)
        if content is None:
            return
        
        result = self._extract_yaml_header(content, agent_file.name)
        if result is None:
            return
        header_match, header = result
        
        new_tools = self._get_new_tools_to_inject(header, additional_tools, agent_file.name)
        if not new_tools:
            return
        
        new_tools_str = ", ".join(f"'{t}'" for t in new_tools)
        new_content = self._build_modified_content(content, header_match, new_tools_str, agent_file.name)
        if new_content is None:
            return
        
        try:
            agent_file.write_text(new_content, encoding="utf-8")
            self.logger.info(f"Injected {len(new_tools)} MCP permission(s) into {agent_file.name}")
        except OSError as e:
            self.logger.error(f"Failed to write agent file {agent_file.name}: {e}")

    def _build_modified_content(self, content: str, header_match: re.Match, new_tools_str: str, filename: str) -> Optional[str]:
        """Build modified file content with injected tools."""
        header_text = header_match.group(1)
        tools_pattern = r"(tools:\s*\[)([^\]]*?)(\])"
        
        def replace_tools(match: re.Match) -> str:
            prefix, existing, suffix = match.group(1), match.group(2).rstrip(), match.group(3)
            return f"{prefix}{existing}, {new_tools_str}{suffix}" if existing else f"{prefix}{new_tools_str}{suffix}"
        
        new_header_text, count = re.subn(tools_pattern, replace_tools, header_text, count=1)
        if count == 0:
            self.logger.warning(f"Could not find tools line in {filename}, skipping injection.")
            return None
        
        rest_of_file = content[header_match.end():]
        return f"---\n{new_header_text}\n---{rest_of_file}"

    def _apply_mcp_injection_to_agents(self, target_path: Path) -> None:
        """Apply MCP permission injection to all agent files in target directory."""
        permissions = self._load_mcp_permissions()
        if not permissions:
            return
        
        agents_dir = target_path / "agents"
        if not agents_dir.exists():
            self.logger.debug(f"Agents directory not found: {agents_dir}")
            return
        
        for agent_file in agents_dir.glob("*.agent.md"):
            # Extract agent key from filename: hyper_architect.adhd.agent.md -> hyper_architect
            agent_key = agent_file.stem.replace(".adhd.agent", "").replace(".agent", "")
            
            if agent_key in permissions:
                additional_tools = permissions[agent_key]
                if isinstance(additional_tools, list):
                    self._inject_mcp_permissions_to_agent(agent_file, additional_tools)
                else:
                    self.logger.warning(f"Invalid tools format for agent '{agent_key}', expected list.")

    def _sync_files_by_pattern(self, source_dir: Path, target_dir: Path, pattern: str, subdir: str, label: str) -> None:
        """
        Sync files matching a pattern from source subdirectory to target subdirectory.
        Supports nested subdirectories in source - all files are flattened to target.
        
        Args:
            source_dir: Source directory containing the subdir
            target_dir: Target directory containing the subdir
            pattern: Glob pattern for files (e.g., "*.instructions.md")
            subdir: Subdirectory name (e.g., "instructions", "agents", "prompts")
            label: Label for logging
        """
        src = source_dir / subdir
        if src.exists():
            # Use rglob to find files in nested subdirectories, flatten to target
            for file_path in src.rglob(pattern):
                try:
                    # Flatten: all files go to target_dir/subdir/ regardless of source nesting
                    dest_path = target_dir / subdir / file_path.name
                    shutil.copy2(file_path, dest_path)
                    self.logger.info(f"Synced {subdir[:-1]} ({label}): {file_path.name}")
                except OSError as e:
                    self.logger.error(f"Failed to sync {file_path.name} to {subdir}: {e}")

    def _sync_data_to_target(self, source_path: Path, target_path: Path, label: str) -> None:
        """
        Sync instruction, agent, and prompt files from source to target.
        Supports nested subdirectories in source - files are flattened to target.
        
        Args:
            source_path: Source directory containing instructions/, agents/, prompts/ subdirs
            target_path: Target directory (e.g., .github)
            label: Label for logging (e.g., "official", "custom")
        """
        if not source_path.exists():
            self.logger.info(f"{label} source path not found: {source_path}. Skipping.")
            return

        self.logger.info(f"Syncing {label} data from {source_path} to {target_path}")

        for pattern, subdir, _ in FILE_TYPE_CONFIGS:
            self._sync_files_by_pattern(source_path, target_path, pattern, subdir, label)

    def _sync_agent_plan(self, source_path: Path) -> None:
        """
        Sync .agent_plan directory from source to project root.
        Overlays files without removing existing files that don't collide.
        
        Args:
            source_path: Source directory containing .agent_plan subdirectory
        """
        agent_plan_source = source_path / ".agent_plan"
        if not agent_plan_source.exists():
            self.logger.debug(f"No .agent_plan found in {source_path}. Skipping.")
            return
        
        agent_plan_target = self.root_path / ".agent_plan"
        
        self.logger.info(f"Syncing .agent_plan from {agent_plan_source} to {agent_plan_target}")
        
        # Walk through source and copy files, preserving directory structure
        for source_file in agent_plan_source.rglob("*"):
            if source_file.is_file():
                # Calculate relative path from .agent_plan source
                relative_path = source_file.relative_to(agent_plan_source)
                target_file = agent_plan_target / relative_path
                
                try:
                    # Ensure parent directory exists
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)
                    self.logger.info(f"Synced .agent_plan: {relative_path}")
                except OSError as e:
                    self.logger.error(f"Failed to sync .agent_plan file {relative_path}: {e}")

    def _sync_module_files_to_target(self, target_path: Path, pattern: str, subdir: str, file_type: str) -> None:
        """
        Scan all modules and copy files matching pattern to target subdirectory.
        
        Args:
            target_path: Target base directory
            pattern: Glob pattern (e.g., "*.instructions.md")
            subdir: Target subdirectory (e.g., "instructions")
            file_type: Human-readable file type for logging (e.g., "instruction")
        """
        self.logger.info(f"Syncing module {file_type}s to {target_path}...")
        
        report = self.modules_controller.list_all_modules()
        
        for module in report.modules:
            files = list(module.path.glob(pattern))
            if files:
                for file_path in files:
                    try:
                        dest_path = target_path / subdir / file_path.name
                        shutil.copy2(file_path, dest_path)
                        self.logger.info(f"Synced module {file_type}: {module.name} -> {dest_path.name}")
                    except OSError as e:
                        self.logger.error(f"Failed to sync {file_type} {file_path.name} for module {module.name}: {e}")
            else:
                self.logger.debug(f"No {file_type}s found for module {module.name}")

    def run(self) -> None:
        """Execute the full synchronization process based on config."""
        self.logger.info("Starting instruction synchronization...")
        
        # Sync .agent_plan from official source to project root
        self._sync_agent_plan(self.official_source_path)
        
        # Sync official source to all official targets
        if self.official_target_paths:
            for target_path in self.official_target_paths:
                self.logger.info(f"Official sync: {self.official_source_path} -> {target_path}")
                self._ensure_target_structure(target_path)
                self._sync_data_to_target(self.official_source_path, target_path, "official")
                for pattern, subdir, file_type in FILE_TYPE_CONFIGS:
                    self._sync_module_files_to_target(target_path, pattern, subdir, file_type)
                # Apply MCP permission injection to copied agents
                self._apply_mcp_injection_to_agents(target_path)
        else:
            self.logger.info("No official targets configured, skipping official sync.")
        
        # Sync custom source to all custom targets (also sync its .agent_plan if present)
        if self.custom_target_paths:
            self._sync_agent_plan(self.custom_source_path)
            for target_path in self.custom_target_paths:
                self.logger.info(f"Custom sync: {self.custom_source_path} -> {target_path}")
                self._ensure_target_structure(target_path)
                self._sync_data_to_target(self.custom_source_path, target_path, "custom")
                # Apply MCP permission injection to copied agents (custom targets may have agents too)
                self._apply_mcp_injection_to_agents(target_path)
        else:
            self.logger.info("No custom targets configured, skipping custom sync.")
        
        self.logger.info("Instruction synchronization completed.")
