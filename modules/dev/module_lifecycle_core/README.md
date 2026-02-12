# Module Lifecycle Core

Manages the full lifecycle of ADHD workspace modules — add from git, remove with dependency checks, and update via atomic swap with rollback.

## Overview
- Add external modules from standalone repos or monorepo subfolders via git clone.
- Remove modules with reverse-dependency checking, dry-run preview, and optional directory retention.
- Update modules atomically — clone new version, swap directories, rollback on failure.
- Batch-update all modules in a layer with a single command.

## Features
- **Git URL parsing** — handles GitHub browser URLs, clone URLs, SSH URLs, and embedded subfolder/branch paths.
- **Pyproject scaffolding** — interactively generates `pyproject.toml` for modules that lack one.
- **Reverse-dependency safety** — refuses removal when other modules depend on the target (unless forced).
- **Atomic swap with rollback** — backup → swap → sync; restores `.bak` on failure.
- **Dry-run mode** — preview add/remove/update operations without making changes.
- **Root pyproject patching** — adds or removes workspace members from root `pyproject.toml` while preserving formatting.

## Quickstart
```python
from module_lifecycle_core import ModuleAdder, ModuleRemover, ModuleUpdater

# Add a module from a GitHub repo
adder = ModuleAdder()
result = adder.add_from_repo("https://github.com/org/my_module.git")
print(result.message)

# Remove a module (with dry-run preview)
remover = ModuleRemover()
result = remover.remove("my_module", dry_run=True)
print(result.message)

# Update a module to latest version
updater = ModuleUpdater()
result = updater.update("my_module")
print(result.old_version, "->", result.new_version)
```

## API
```python
class ModuleAdder:
    def __init__(self, project_root: Optional[Path] = None): ...
    def add_from_repo(
        self,
        repo_url: str,
        subfolder: Optional[str] = None,
        *,
        keep_git: bool = False,
        add_to_root: Optional[bool] = None,
        skip_prompt: bool = False,
    ) -> AddModuleResult: ...

@dataclass
class AddModuleResult:
    success: bool
    module_name: str
    target_path: Optional[Path] = None
    layer: Optional[str] = None
    message: str = ""

class ModuleRemover:
    def __init__(self, project_root: Optional[Path] = None): ...
    def remove(
        self,
        module_name: str,
        *,
        dry_run: bool = False,
        force: bool = False,
        keep_dir: bool = False,
        no_confirm: bool = False,
    ) -> RemoveResult: ...

@dataclass
class RemoveResult:
    success: bool
    module_name: str
    layer: Optional[str] = None
    reverse_deps: Set[str] = field(default_factory=set)
    message: str = ""

class ModuleUpdater:
    def __init__(self, project_root: Optional[Path] = None): ...
    def update(
        self,
        module_name: str,
        *,
        dry_run: bool = False,
        branch: Optional[str] = None,
        keep_backup: bool = False,
        force: bool = False,
        skip_post_steps: bool = False,
    ) -> UpdateResult: ...
    def batch_update(
        self,
        layer: str,
        *,
        dry_run: bool = False,
        branch: Optional[str] = None,
        keep_backup: bool = False,
        force: bool = False,
        continue_on_error: bool = False,
    ) -> BatchUpdateResult: ...

@dataclass
class UpdateResult:
    success: bool
    module_name: str
    old_version: Optional[str] = None
    new_version: Optional[str] = None
    message: str = ""
    rollback_performed: bool = False

@dataclass
class BatchUpdateResult:
    succeeded: List[UpdateResult] = field(default_factory=list)
    failed: List[UpdateResult] = field(default_factory=list)
    skipped: List[UpdateResult] = field(default_factory=list)
    total: int = 0
```

## Notes
- `batch_update` raises `ADHDError` if the target layer is `"runtime"` — runtime modules are project-specific and must be updated individually.
- The updater checks for local modifications before updating; use `force=True` to overwrite uncommitted changes.
- `ModuleAdder` runs `uv sync` automatically after cloning to register the new workspace member.

## Requirements & prerequisites
- exceptions-core
- logger-util
- modules-controller-core
- creator-common-core

## Troubleshooting
- **"Module already exists"**: The target directory already contains a module with the same name. Remove it first or use a different name.
- **"no source URL recorded"**: The module's `pyproject.toml` has no `[project.urls] Repository` entry. Add one manually, or remove and re-add with `adhd add <url>`.
- **"has uncommitted local changes"**: The updater refuses to overwrite local edits by default. Use `--force` to proceed.
- **"Cannot remove — modules depend on it"**: Other modules list this one as a dependency. Use `--force` to remove anyway, then fix dependents.
- **"git clone timed out"**: Network issue or slow connection. Check connectivity and retry.

## Module structure
```
module_lifecycle_core/
├─ __init__.py              # exports: ModuleAdder, ModuleRemover, ModuleUpdater, result types
├─ module_adder.py          # add modules from git repos
├─ module_remover.py        # remove modules with dependency checks
├─ module_updater.py        # update modules via atomic swap
├─ pyproject_patcher.py     # add/remove entries in root pyproject.toml
├─ pyproject_scaffolder.py  # scaffold pyproject.toml for modules that lack one
├─ _git_utils.py            # shared git clone and URL parsing utilities
├─ pyproject.toml           # package metadata and dependencies
├─ README.md                # this file
└─ tests/                   # unit tests
```

## See also
- Modules Controller Core — module discovery, dependency walking, workspace sync
- Creator Common Core — shared prompting and repo creation utilities
- Module Creator Core — scaffolding new modules from scratch
- GitHub API Core — GitHub repository operations
