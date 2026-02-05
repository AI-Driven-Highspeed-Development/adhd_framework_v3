"""Module preload sets - defines modules to auto-install in new projects.

Provides parsing logic for module_preload_sets.yaml which defines:
- `repos`: Reusable repo aliases (e.g., adhd -> https://github.com/...)
- `always`: Core modules every project needs (config_manager, logger_util, etc.)
- `options`: Optional module bundles users can select during project creation

Supports multiple source types:
- Monorepo subdirectories: `repo: <alias>` + `subdirectory: <path>`
- Explicit monorepo URL: `url: <git_url>` + `subdirectory: <path>`
- Standalone repos: `url: <git_url>` (no subdirectory)
- Plain string URLs: `- https://github.com/org/module.git` (backward compat)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional

from .yaml_utils import YamlFile


@dataclass
class ModuleSource:
	"""A module source that can be from a monorepo subdirectory or standalone repo.
	
	Attributes:
		url: The git repository URL
		subdirectory: Optional subdirectory path within the repo (for monorepos)
	"""
	url: str
	subdirectory: Optional[str] = None
	
	@property
	def is_monorepo(self) -> bool:
		"""Check if this source is from a monorepo subdirectory."""
		return self.subdirectory is not None
	
	@property
	def display_name(self) -> str:
		"""Get a display-friendly name for the module.
		
		For monorepo modules, uses the subdirectory's final component.
		For standalone repos, uses the repo name from the URL.
		"""
		if self.subdirectory:
			return self.subdirectory.rstrip('/').split('/')[-1].lower().replace('-', '_')
		return self.url.rstrip('/').removesuffix('.git').split('/')[-1].lower().replace('-', '_')


@dataclass
class PreloadSet:
	"""An optional module bundle that users can select during project creation.
	
	Attributes:
		name: Display name for the set (e.g., "HyperPM", "Default")
		description: User-facing description of what the set provides
		modules: List of ModuleSource objects for modules in this set
	"""
	name: str
	description: str
	modules: List[ModuleSource]


def _parse_module_item(
	item: Any,
	repo_aliases: Dict[str, str],
) -> ModuleSource:
	"""Parse a single module item into a ModuleSource.
	
	Handles multiple formats:
	- Plain string URL: "https://github.com/org/module.git"
	- Dict with repo alias: {"repo": "adhd", "subdirectory": "modules/foundation/config_manager"}
	- Dict with explicit URL: {"url": "https://github.com/org/repo.git", "subdirectory": "path/to/module"}
	- Dict with URL only: {"url": "https://github.com/org/standalone.git"}
	- Legacy dict with subdirectory only: {"subdirectory": "path"} (requires framework_repo fallback)
	
	Args:
		item: The module item from YAML (string or dict)
		repo_aliases: Dict mapping repo alias names to URLs
		
	Returns:
		ModuleSource with resolved URL and optional subdirectory
		
	Raises:
		ValueError: If the item format is invalid or references unknown alias
	"""
	# Plain string URL (backward compat)
	if isinstance(item, str):
		return ModuleSource(url=item, subdirectory=None)
	
	if not isinstance(item, dict):
		raise ValueError(f"Module item must be a string or dict, got: {type(item)}")
	
	subdirectory = item.get("subdirectory")
	
	# Dict with repo alias: {"repo": "adhd", "subdirectory": "..."}
	if "repo" in item:
		alias = item["repo"]
		if alias not in repo_aliases:
			available = ", ".join(repo_aliases.keys()) if repo_aliases else "(none defined)"
			raise ValueError(f"Unknown repo alias '{alias}'. Available: {available}")
		return ModuleSource(url=repo_aliases[alias], subdirectory=subdirectory)
	
	# Dict with explicit URL: {"url": "...", "subdirectory": "..."}
	if "url" in item:
		return ModuleSource(url=item["url"], subdirectory=subdirectory)
	
	# Legacy format: {"subdirectory": "..."} without repo or url
	# This requires a fallback repo (framework_repo from v1 format or first repo alias)
	if subdirectory is not None:
		# Try to use 'adhd' alias as default, or first available alias
		fallback_url = repo_aliases.get("adhd") or (
			next(iter(repo_aliases.values())) if repo_aliases else None
		)
		if fallback_url:
			return ModuleSource(url=fallback_url, subdirectory=subdirectory)
		raise ValueError(
			f"Module has subdirectory '{subdirectory}' but no 'repo' or 'url' specified, "
			"and no repo aliases are defined to use as fallback."
		)
	
	raise ValueError(f"Invalid module item format: {item}")


def _parse_module_list(
	items: List[Any],
	repo_aliases: Dict[str, str],
) -> List[ModuleSource]:
	"""Parse a list of module items into ModuleSource objects.
	
	Args:
		items: List of module items (strings or dicts)
		repo_aliases: Dict mapping repo alias names to URLs
		
	Returns:
		List of ModuleSource objects
	"""
	return [_parse_module_item(item, repo_aliases) for item in items]


def parse_preload_sets(yf: YamlFile) -> Tuple[List[ModuleSource], List[PreloadSet]]:
	"""Parse the module preload sets YAML into always modules and optional sets.
	
	Supports v2 format with:
	- `repos`: Reusable repo aliases
	- `always`: Core modules (can be strings, dicts with repo/url + subdirectory)
	- `options`: Optional bundles with `modules` (preferred) or `urls` (legacy)
	
	Also supports v1 format with:
	- `framework_repo`: Single monorepo URL (used as fallback)
	- `always`: List of dicts with `subdirectory` only
	- `options`: Sets with `subdirectories` or `urls`
	
	Args:
		yf: YamlFile object with parsed YAML content
		
	Returns:
		Tuple of (always_modules, optional_sets) where:
		- always_modules: List of ModuleSource for core modules
		- optional_sets: List of PreloadSet for user-selectable bundles
	"""
	# Build repo aliases dict
	repo_aliases: Dict[str, str] = {}
	
	# Check for v2 repos section
	repos_raw = yf.get("repos", {})
	if isinstance(repos_raw, dict):
		repo_aliases = {k: str(v) for k, v in repos_raw.items()}
	
	# Check for v1 framework_repo (backward compat)
	framework_repo = yf.get("framework_repo")
	if framework_repo and "adhd" not in repo_aliases:
		repo_aliases["adhd"] = str(framework_repo)
	
	# Parse always modules
	always_raw = yf.get("always", [])
	always_modules: List[ModuleSource] = []
	
	if isinstance(always_raw, list):
		always_modules = _parse_module_list(always_raw, repo_aliases)
	
	# Parse options
	options = yf.get("options", {})
	options_out: List[PreloadSet] = []
	
	if not isinstance(options, dict):
		raise ValueError("module_preload_sets.options must be a mapping of set name -> {description, modules/urls}")
	
	for name, value in options.items():
		desc = ""
		modules: List[ModuleSource] = []
		
		if isinstance(value, dict):
			desc = str(value.get("description", ""))
			
			# v2 format: modules (list of module sources)
			if "modules" in value and isinstance(value["modules"], list):
				modules = _parse_module_list(value["modules"], repo_aliases)
			
			# v1 format: subdirectories (list of strings, need fallback repo)
			elif "subdirectories" in value and isinstance(value["subdirectories"], list):
				for subdir in value["subdirectories"]:
					modules.append(_parse_module_item({"subdirectory": subdir}, repo_aliases))
			
			# Legacy format: urls (list of plain strings)
			elif "urls" in value and isinstance(value["urls"], list):
				modules = [ModuleSource(url=str(u)) for u in value["urls"]]
		
		options_out.append(PreloadSet(name=name, description=desc, modules=modules))

	return always_modules, options_out


__all__ = ["ModuleSource", "PreloadSet", "parse_preload_sets"]

