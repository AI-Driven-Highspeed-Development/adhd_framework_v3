# Project Creator Core

Creates new ADHD Framework projects from embedded templates with module preloading and workspace configuration.

## Overview
- Scaffolds a complete ADHD Framework project directory with standard layout.
- Installs preloaded modules by cloning them from git into workspace folders.
- Generates `pyproject.toml` with workspace members and `uv` source mappings.
- Provides an interactive wizard for guided project creation.

## Features
- **Embedded templates** — project files generated from bundled templates, no external cloning required.
- **Module preload sets** — YAML-defined bundles of core and optional modules auto-installed during creation.
- **Monorepo and standalone sources** — supports module sources from monorepo subdirectories or standalone repos.
- **Remote repo creation** — optionally creates a GitHub repository and pushes the initial project.
- **Interactive wizard** — guided prompts for project name, directory, description, and module selection.
- **Preload set parsing** — v1 and v2 YAML formats with repo aliases and multiple source types.

## Quickstart
```python
from project_creator_core import ProjectCreator, ProjectParams, ModuleSource

params = ProjectParams(
    repo_path="~/projects/my_new_project",
    module_sources=[
        ModuleSource(url="https://github.com/org/repo.git", subdirectory="modules/foundation/config_manager"),
    ],
    project_name="my_new_project",
    description="My ADHD project",
)

creator = ProjectCreator(params)
project_path = creator.create()
```

## API
```python
class ProjectCreator:
    def __init__(self, params: ProjectParams): ...
    def create(self) -> Path: ...

@dataclass
class ProjectParams:
    repo_path: str
    module_sources: List[ModuleSource]
    project_name: str
    description: str = ""
    repo_options: Optional[RepoCreationOptions] = None

@dataclass
class ModuleInfo:
    package_name: str       # from [project] name in pyproject.toml
    layer: str              # from [tool.adhd] layer
    folder_name: str        # directory name (e.g., "config_manager")
    git_url: str            # original git URL
    subdirectory: Optional[str] = None

@dataclass
class ModuleSource:
    url: str
    subdirectory: Optional[str] = None

@dataclass
class PreloadSet:
    name: str
    description: str
    modules: List[ModuleSource]

def parse_preload_sets(yf: YamlFile) -> Tuple[List[ModuleSource], List[PreloadSet]]: ...

def run_project_creation_wizard(
    *,
    prompter: QuestionaryCore,
    logger: Logger,
    prefilled: Optional[ProjectWizardArgs] = None,
) -> None: ...
```

## Notes
- `ensure_templates()` copies bundled YAML templates to `project/data/project_creator_core/` on first use; called lazily, not on import.
- The wizard validates that the destination path does not already exist, re-prompting if it does.
- `ModuleInfo` is extracted from cloned module `pyproject.toml` files during installation — it is not user-supplied.
- `parse_preload_sets` supports both v1 (legacy `framework_repo` + `subdirectories`) and v2 (`repos` aliases + `modules`) YAML formats.

## Requirements & prerequisites
- logger-util
- creator-common-core
- exceptions-core
- github-api-core
- modules-controller-core
- pyyaml>=6.0

## Troubleshooting
- **"Framework file not found"**: `ProjectCreator` expects to run from the ADHD Framework root where `adhd_framework.py` exists. Ensure the correct working directory.
- **"Template not found"**: Embedded templates in `data/templates/` are missing. Reinstall or re-clone the module.
- **"Path already exists"**: The wizard refuses to overwrite existing directories. Choose a different project name or parent directory.
- **"Unknown repo alias"**: A module source references a repo alias not defined in the `repos` section of `module_preload_sets.yaml`. Add the alias or use an explicit `url`.
- **uv sync fails after creation**: The generated `pyproject.toml` may reference modules that failed to clone. Check network connectivity and retry.

## Module structure
```
project_creator_core/
├─ __init__.py                  # exports: ProjectCreator, ProjectParams, ModuleInfo, PreloadSet, ModuleSource, parse_preload_sets
├─ project_creator.py           # main project creation logic
├─ project_creation_wizard.py   # interactive wizard for guided creation
├─ preload_sets.py              # preload set parsing and ModuleSource/PreloadSet types
├─ yaml_utils.py                # inlined YAML reading utilities (YamlFile, YamlReader)
├─ pyproject.toml               # package metadata and dependencies
├─ requirements.txt             # PyPI dependencies (pyyaml)
├─ README.md                    # this file
├─ data/
│  ├─ module_preload_sets.yaml  # default module preload set definitions
│  └─ templates/                # embedded project templates
└─ tests/                       # unit tests
```

## See also
- Creator Common Core — shared prompting, repo creation, and naming utilities
- Module Lifecycle Core — add, remove, and update modules in existing projects
- Modules Controller Core — module discovery and workspace sync
- GitHub API Core — GitHub repository operations
