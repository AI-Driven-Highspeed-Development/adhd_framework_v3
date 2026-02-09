from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

from exceptions_core import ADHDError
from modules_controller_core import ModulesController
from config_manager import ConfigManager
from logger_util import Logger
from flow_core import FlowController, FlowError


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

    def _load_existing_manifest(self) -> dict:
        """Load existing compiled manifest for incremental compilation.

        Returns:
            Manifest dict if found and valid, empty dict otherwise.
        """
        manifest_path = self.official_source_path / "compiled" / "compiled_manifest.json"
        if not manifest_path.exists():
            return {}
        try:
            content = manifest_path.read_text(encoding="utf-8")
            return json.loads(content)
        except (json.JSONDecodeError, OSError) as e:
            self.logger.warning(f"Failed to load existing manifest: {e}")
            return {}

    def _compute_transitive_hash(self, resolved_files: set[Path]) -> str:
        """Compute SHA-256 over all resolved files' contents, sorted by path.

        Produces a deterministic hash representing the combined state of all
        files that participated in a flow compilation (entry + transitive imports).

        Args:
            resolved_files: Set of absolute file paths to hash.

        Returns:
            Hex digest of the combined SHA-256 hash, or empty string if no files.
        """
        if not resolved_files:
            return ""
        hasher = hashlib.sha256()
        for file_path in sorted(resolved_files):
            try:
                hasher.update(file_path.read_bytes())
            except OSError:
                # Include path as bytes to force cache miss if file disappears
                hasher.update(str(file_path).encode("utf-8"))
        return hasher.hexdigest()

    def _load_sidecar(self, sidecar_path: Path) -> Optional[dict]:
        """Load and validate a sidecar `.yaml` file for a `.flow` file.

        Sidecar files contain YAML frontmatter metadata (name, tools, handoffs,
        etc.) that gets prepended to compiled Markdown output.

        Args:
            sidecar_path: Path to the sidecar `.yaml` file.

        Returns:
            Parsed YAML dict if valid, or ``None`` if the file doesn't exist
            or contains invalid YAML.
        """
        if not sidecar_path.exists():
            return None

        try:
            content = sidecar_path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                self.logger.warning(
                    f"Sidecar {sidecar_path.name} must be a YAML mapping, got {type(data).__name__}. Skipping frontmatter."
                )
                return None
            self.logger.debug(f"Loaded sidecar: {sidecar_path.name}")
            return data
        except yaml.YAMLError as e:
            self.logger.warning(f"Failed to parse sidecar {sidecar_path.name}: {e}")
            return None
        except OSError as e:
            self.logger.error(f"Failed to read sidecar {sidecar_path.name}: {e}")
            return None

    def _prepend_frontmatter(self, body: str, sidecar: dict) -> str:
        """Prepend YAML frontmatter from sidecar metadata to compiled Markdown body.

        Keys are serialized in the order they appear in the sidecar dict.
        The ``tools`` key receives special handling: it is always serialized in
        YAML flow style (``tools: ['tool1', 'tool2']``) so that the MCP
        injection regex in ``_build_modified_content()`` can match it.

        Args:
            body: Compiled Markdown content from flow_core.
            sidecar: Metadata dict loaded from sidecar ``.yaml`` file.

        Returns:
            Complete agent file content with ``---`` frontmatter prepended.
        """
        if not sidecar:
            return body

        lines: list[str] = []
        for key, value in sidecar.items():
            if key == "tools" and isinstance(value, list):
                # Force flow-style list with single-quoted items for MCP injection compatibility
                tools_items = ", ".join(f"'{t}'" for t in value)
                lines.append(f"tools: [{tools_items}]")
            else:
                # Use yaml.dump for all other keys (block style, preserves order)
                chunk = yaml.dump(
                    {key: value},
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    width=float('inf'),
                )
                lines.append(chunk.rstrip("\n"))

        frontmatter = "\n".join(lines)
        return f"---\n{frontmatter}\n---\n{body}"

    def _get_output_rel_path(self, flow_file: Path, flows_dir: Path) -> str:
        """Determine compiled output relative path for a flow source file.

        Subdirectory determines output type:
        - ``flows/agents/foo.flow`` → ``agents/foo.adhd.agent.md``
        - ``flows/instructions/foo.flow`` → ``instructions/foo.instructions.md``
        - ``flows/foo.flow`` (flat) → ``foo.md``

        Args:
            flow_file: Absolute path to the ``.flow`` source file.
            flows_dir: Absolute path to the ``data/flows/`` directory.

        Returns:
            Relative output path suitable as key in compiled dict and manifest.
        """
        rel = flow_file.relative_to(flows_dir)
        parts = rel.parts
        stem = flow_file.stem

        if len(parts) > 1 and parts[0] == "agents":
            return str(Path("agents") / f"{stem}.adhd.agent.md")
        elif len(parts) > 1 and parts[0] == "instructions":
            return str(Path("instructions") / f"{stem}.instructions.md")
        return f"{stem}.md"

    def _compile_flows(self, force: bool = False) -> dict[str, str]:
        """
        Compile all .flow files from data/flows/ using FlowController.

        Supports incremental compilation: if force=False, skips files whose
        source SHA-256 matches the existing manifest entry.

        Handles subdirectory-based output types:
        - ``flows/agents/foo.flow`` → key ``agents/foo.adhd.agent.md``
        - ``flows/foo.flow`` → key ``foo.md``

        Args:
            force: If True, recompile everything ignoring cache.

        Returns:
            Dict mapping output relative path to compiled Markdown content.
            Empty dict if data/flows/ doesn't exist or no files found.
        """
        flows_dir = self.official_source_path / "flows"
        if not flows_dir.exists():
            self.logger.debug("No data/flows/ directory found, skipping flow compilation.")
            return {}

        all_flow_files = list(flows_dir.rglob("*.flow"))
        # Filter out _lib/ fragments — shared imports, not standalone compilable files
        flow_files = [
            f for f in all_flow_files
            if "_lib" not in f.relative_to(flows_dir).parts
        ]
        if not flow_files:
            self.logger.debug("No compilable .flow files found in data/flows/.")
            return {}

        lib_count = len(all_flow_files) - len(flow_files)
        if lib_count:
            self.logger.debug(f"Filtered {lib_count} _lib/ fragment(s) from compilation.")
        self.logger.info(f"Compiling {len(flow_files)} .flow file(s) from {flows_dir}")

        # Load existing manifest for incremental compilation
        existing_manifest: dict = {}
        if not force:
            existing_manifest = self._load_existing_manifest()

        controller = FlowController(logger=self.logger)
        compiled: dict[str, str] = {}
        skipped = 0

        # Transitive hash tracking — read by _generate_manifest()
        self._transitive_data: dict[str, dict] = {}
        # Source file mapping — maps output_rel_path to source .flow Path
        self._source_map: dict[str, Path] = {}

        for flow_file in flow_files:
            stem = flow_file.stem
            compiled_name = self._get_output_rel_path(flow_file, flows_dir)

            # Incremental: check if source AND transitive deps haven't changed
            if not force and existing_manifest:
                try:
                    source_hash = hashlib.sha256(flow_file.read_bytes()).hexdigest()
                    entry = existing_manifest.get("entries", {}).get(compiled_name, {})
                    if entry.get("source_sha256") == source_hash:
                        # Entry file unchanged — also verify transitive deps
                        stored_transitive_sha = entry.get("transitive_sha256")
                        stored_transitive_files = entry.get("transitive_files", [])

                        transitive_ok = False
                        if stored_transitive_sha and stored_transitive_files:
                            stored_paths = {Path(p) for p in stored_transitive_files}
                            current_transitive = self._compute_transitive_hash(stored_paths)
                            transitive_ok = current_transitive == stored_transitive_sha
                        elif not stored_transitive_sha:
                            # Legacy manifest without transitive hash — source check suffices
                            transitive_ok = True

                        # Detect new sidecar .yaml that wasn't in previous transitive set
                        if transitive_ok:
                            sidecar_path = flow_file.with_suffix(".yaml")
                            if sidecar_path.exists() and str(sidecar_path) not in (stored_transitive_files or []):
                                transitive_ok = False
                                self.logger.info(
                                    f"New sidecar detected: {sidecar_path.name}, recompiling {flow_file.name}."
                                )

                        if transitive_ok:
                            compiled_path = self.official_source_path / "compiled" / compiled_name
                            if compiled_path.exists():
                                compiled[compiled_name] = compiled_path.read_text(encoding="utf-8")
                                self._source_map[compiled_name] = flow_file
                                # Preserve transitive data for skipped files
                                if stored_transitive_sha:
                                    self._transitive_data[compiled_name] = {
                                        "transitive_sha256": stored_transitive_sha,
                                        "transitive_files": stored_transitive_files,
                                    }
                                self.logger.info(f"Skipped (unchanged): {flow_file.name}")
                                skipped += 1
                                continue
                except OSError as e:
                    self.logger.warning(f"Failed incremental check for {flow_file.name}: {e}")

            try:
                markdown = controller.compile_file(flow_file)

                # Load sidecar .yaml and prepend frontmatter if available
                sidecar_path = flow_file.with_suffix(".yaml")
                sidecar = self._load_sidecar(sidecar_path)
                if sidecar:
                    markdown = self._prepend_frontmatter(markdown, sidecar)

                compiled[compiled_name] = markdown
                self._source_map[compiled_name] = flow_file

                # Compute transitive hash from all files that participated
                resolved_files = controller.get_last_resolved_files()
                # Include sidecar in transitive set so changes trigger recompilation
                if sidecar_path.exists():
                    resolved_files = resolved_files | {sidecar_path}
                if resolved_files:
                    transitive_sha = self._compute_transitive_hash(resolved_files)
                    self._transitive_data[compiled_name] = {
                        "transitive_sha256": transitive_sha,
                        "transitive_files": [str(p) for p in sorted(resolved_files)],
                    }

                self.logger.info(f"Compiled flow: {flow_file.name}")
            except FlowError as e:
                self.logger.warning(f"Failed to compile {flow_file.name}, skipping: {e}")

        # Pass-through: copy non-.flow files to compiled output (excluding _lib/ and sidecar .yaml)
        self._passthrough_keys: set[str] = set()
        all_files_in_flows = [f for f in flows_dir.rglob("*") if f.is_file()]
        passthrough_candidates = [
            f for f in all_files_in_flows
            if f.suffix != ".flow"
            and "_lib" not in f.relative_to(flows_dir).parts
            and not (f.suffix == ".yaml" and f.with_suffix(".flow").exists())
        ]
        for pt_file in passthrough_candidates:
            rel = str(pt_file.relative_to(flows_dir))
            try:
                content = pt_file.read_text(encoding="utf-8")
                compiled[rel] = content
                self._passthrough_keys.add(rel)
                self._source_map[rel] = pt_file
                self.logger.info(f"Pass-through: {pt_file.name}")
            except OSError as e:
                self.logger.warning(f"Failed to read pass-through file {pt_file.name}: {e}")

        passthrough = len(self._passthrough_keys)
        compiled_total = len(compiled) - passthrough  # .flow entries (fresh + cached)
        fresh = compiled_total - skipped
        failed = len(flow_files) - compiled_total
        self.logger.info(
            f"Flow compilation complete: {fresh} compiled, {skipped} skipped (unchanged), "
            f"{passthrough} pass-through, {failed} failed."
        )
        return compiled

    def _write_compiled_output(self, compiled: dict[str, str]) -> list[Path]:
        """
        Write compiled Markdown files to data/compiled/.

        Handles subdirectories (e.g., ``compiled/agents/``) automatically.

        Args:
            compiled: Dict mapping output relative path to compiled Markdown content.

        Returns:
            List of written file paths.
        """
        compiled_dir = self.official_source_path / "compiled"
        compiled_dir.mkdir(parents=True, exist_ok=True)

        written: list[Path] = []
        for output_rel, content in compiled.items():
            out_path = compiled_dir / output_rel
            out_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                out_path.write_text(content, encoding="utf-8")
                written.append(out_path)
                self.logger.info(f"Wrote compiled output: {output_rel}")
            except OSError as e:
                self.logger.error(f"Failed to write compiled file {output_rel}: {e}")

        return written

    def _generate_manifest(self, compiled: dict[str, str]) -> dict:
        """
        Generate compiled_manifest.json in data/compiled/ with SHA-256 hashes.

        Includes both source file hash (for incremental compilation) and
        compiled output hash (for integrity verification).

        Args:
            compiled: Dict mapping output relative path to compiled Markdown content.

        Returns:
            The manifest dict that was written to disk.
        """
        compiled_dir = self.official_source_path / "compiled"
        compiled_dir.mkdir(parents=True, exist_ok=True)
        flows_dir = self.official_source_path / "flows"

        source_map: dict[str, Path] = getattr(self, "_source_map", {})
        passthrough_keys: set[str] = getattr(self, "_passthrough_keys", set())

        entries: dict[str, dict] = {}
        for output_rel, content in compiled.items():
            content_bytes = content.encode("utf-8")

            # Determine source .flow file
            source_file = source_map.get(output_rel)
            if source_file is None:
                # Fallback for legacy: derive from output_rel stem
                source_file = flows_dir / f"{Path(output_rel).stem}.flow"

            # Compute relative source path and hash
            source_sha256 = ""
            try:
                source_rel = str(source_file.relative_to(flows_dir))
            except ValueError:
                source_rel = source_file.name
            if source_file.exists():
                try:
                    source_sha256 = hashlib.sha256(source_file.read_bytes()).hexdigest()
                except OSError:
                    pass

            entry_data: dict = {
                "source": source_rel,
                "type": "passthrough" if output_rel in passthrough_keys else "compiled",
                "sha256": hashlib.sha256(content_bytes).hexdigest(),
                "source_sha256": source_sha256,
                "size": len(content_bytes),
            }

            # Include transitive hash data if available
            transitive_info = getattr(self, "_transitive_data", {}).get(output_rel, {})
            if transitive_info:
                entry_data["transitive_sha256"] = transitive_info.get("transitive_sha256", "")
                entry_data["transitive_files"] = transitive_info.get("transitive_files", [])

            entries[output_rel] = entry_data

        manifest: dict = {
            "version": "1.1",
            "compiled_at": datetime.now(timezone.utc).isoformat(),
            "entries": entries,
        }

        manifest_path = compiled_dir / "compiled_manifest.json"
        try:
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )
            self.logger.info(f"Generated manifest: {manifest_path.name} ({len(entries)} entries)")
        except OSError as e:
            self.logger.error(f"Failed to write manifest: {e}")

        return manifest

    def _sync_skills(self) -> None:
        """
        Sync skill directories from data/skills/ to each official target's sibling skills/ directory.

        Skills go to {target}/../skills/ (e.g., .github/skills/, not .github/instructions/skills/).
        Uses shutil.copytree with dirs_exist_ok=True for each skill subdirectory.
        """
        skills_source = self.official_source_path / "skills"
        if not skills_source.exists():
            self.logger.debug("No data/skills/ directory found, skipping skills sync.")
            return

        skill_dirs = [d for d in skills_source.iterdir() if d.is_dir()]
        if not skill_dirs:
            self.logger.debug("No skill subdirectories found in data/skills/.")
            return

        for target_path in self.official_target_paths:
            skills_target = target_path / "skills"
            skills_target.mkdir(parents=True, exist_ok=True)

            for skill_dir in skill_dirs:
                dst = skills_target / skill_dir.name
                try:
                    shutil.copytree(skill_dir, dst, dirs_exist_ok=True)
                    self.logger.info(f"Synced skill: {skill_dir.name} -> {dst}")
                except OSError as e:
                    self.logger.error(f"Failed to sync skill {skill_dir.name}: {e}")

    def _sync_files_by_pattern(self, source_dir: Path, target_dir: Path, pattern: str, subdir: str, label: str, compiled_files: set[str] | None = None) -> None:
        """
        Sync files matching a pattern from source subdirectory to target subdirectory.
        Supports nested subdirectories in source - all files are flattened to target.
        
        Args:
            source_dir: Source directory containing the subdir
            target_dir: Target directory containing the subdir
            pattern: Glob pattern for files (e.g., "*.instructions.md")
            subdir: Subdirectory name (e.g., "instructions", "agents", "prompts")
            label: Label for logging
            compiled_files: Optional set of compiled filenames to skip (compiled takes priority)
        """
        src = source_dir / subdir
        if src.exists():
            # Use rglob to find files in nested subdirectories, flatten to target
            for file_path in src.rglob(pattern):
                # Skip files that were already placed by compiled output
                if compiled_files and file_path.name in compiled_files:
                    self.logger.debug(f"Skipping static {file_path.name} (compiled version takes priority)")
                    continue
                try:
                    # Flatten: all files go to target_dir/subdir/ regardless of source nesting
                    dest_path = target_dir / subdir / file_path.name
                    shutil.copy2(file_path, dest_path)
                    self.logger.info(f"Synced {subdir[:-1]} ({label}): {file_path.name}")
                except OSError as e:
                    self.logger.error(f"Failed to sync {file_path.name} to {subdir}: {e}")

    def _sync_data_to_target(self, source_path: Path, target_path: Path, label: str, compiled_files: set[str] | None = None) -> None:
        """
        Sync instruction, agent, and prompt files from source to target.
        Supports nested subdirectories in source - files are flattened to target.

        Compiled files take priority: if compiled_files is provided, any compiled
        output files are copied first from data/compiled/, routed by subdirectory
        (agents/ → target/agents/, flat → target/instructions/), and static files
        with the same name are skipped.

        Args:
            source_path: Source directory containing instructions/, agents/, prompts/ subdirs
            target_path: Target directory (e.g., .github)
            label: Label for logging (e.g., "official", "custom")
            compiled_files: Optional set of compiled output relative paths
                (e.g., {"foo.md", "agents/bar.adhd.agent.md"}) that take priority
        """
        if not source_path.exists():
            self.logger.info(f"{label} source path not found: {source_path}. Skipping.")
            return

        self.logger.info(f"Syncing {label} data from {source_path} to {target_path}")

        # Copy compiled files first (highest priority) — route by subdirectory
        if compiled_files:
            compiled_dir = self.official_source_path / "compiled"
            if compiled_dir.exists():
                for compiled_rel in compiled_files:
                    compiled_path = compiled_dir / compiled_rel
                    if compiled_path.exists():
                        # Route: agents/ subdir → target/agents/, else → target/instructions/
                        rel_parts = Path(compiled_rel).parts
                        if len(rel_parts) > 1 and rel_parts[0] == "agents":
                            sync_subdir = target_path / "agents"
                        else:
                            sync_subdir = target_path / "instructions"
                        sync_subdir.mkdir(parents=True, exist_ok=True)
                        try:
                            dest = sync_subdir / Path(compiled_rel).name
                            shutil.copy2(compiled_path, dest)
                            self.logger.info(f"Synced compiled file: {compiled_rel}")
                        except OSError as e:
                            self.logger.error(f"Failed to sync compiled file {compiled_rel}: {e}")

        # Build basenames set for skip-check in _sync_files_by_pattern
        compiled_basenames = {Path(cf).name for cf in compiled_files} if compiled_files else None

        for pattern, subdir, _ in FILE_TYPE_CONFIGS:
            self._sync_files_by_pattern(source_path, target_path, pattern, subdir, label, compiled_files=compiled_basenames)

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

    def compile_only(self, force: bool = False) -> dict:
        """Compile .flow files and generate manifest without syncing.

        Intended for CI validation — compiles all flows, writes compiled output,
        generates manifest, but does NOT sync to .github/ or any targets.

        Args:
            force: If True, recompile everything ignoring cache. Defaults to False.

        Returns:
            dict with compilation results (manifest data).
        """
        compiled = self._compile_flows(force=force)
        if compiled:
            self._write_compiled_output(compiled)
            return self._generate_manifest(compiled)
        return {
            "version": "1.1",
            "compiled_at": datetime.now(timezone.utc).isoformat(),
            "entries": {},
        }

    def run(self) -> None:
        """Execute the full synchronization process based on config."""
        self.logger.info("Starting instruction synchronization...")
        
        # Compile .flow files with incremental compilation
        compiled = self._compile_flows(force=False)
        compiled_files: set[str] | None = None
        if compiled:
            self._write_compiled_output(compiled)
            self._generate_manifest(compiled)
            compiled_files = set(compiled.keys())

        # Sync .agent_plan from official source to project root
        self._sync_agent_plan(self.official_source_path)
        
        # Sync official source to all official targets
        if self.official_target_paths:
            for target_path in self.official_target_paths:
                self.logger.info(f"Official sync: {self.official_source_path} -> {target_path}")
                self._ensure_target_structure(target_path)
                self._sync_data_to_target(self.official_source_path, target_path, "official", compiled_files=compiled_files)
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
        
        # Sync skills to official targets
        self._sync_skills()
        
        self.logger.info("Instruction synchronization completed.")
