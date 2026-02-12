# Module Creator Core

Scaffolder for new ADHD Framework modules with embedded templates and optional GitHub repository provisioning.

## Overview
- Generates module directories with `pyproject.toml`, `__init__.py`, main source file, README, and config template
- Uses embedded templates from `data/templates/` instead of cloning external repositories
- Supports MCP module scaffolding with additional server, CLI, and refresh files
- Integrates with GitHub API Core to create remote repos and push the initial commit

## Features
- **Embedded templates** – all scaffolding content is generated from bundled template files
- **MCP support** – `is_mcp` flag generates MCP server, CLI, refresh, and init files via `McpModCreator`
- **Name validation** – `validate_module_name` enforces snake_case conventions before any file operations
- **Interactive wizard** – `run_module_creation_wizard` guides users through naming, layer, MCP flag, and repo setup
- **Repo automation** – creates the remote repository and pushes the initial commit when `RepoCreationOptions` is provided
- **Instructions file** – optionally generates a `.instructions.md` file for AI agent context

## Quickstart

Programmatic creation:

```python
from module_creator_core import ModuleCreator, ModuleCreationParams
from creator_common_core import RepoCreationOptions

params = ModuleCreationParams(
    module_name="github_sync",
    layer="runtime",
    is_mcp=False,
    description="Syncs GitHub data",
    repo_options=RepoCreationOptions(owner="my-org", visibility="private"),
)

creator = ModuleCreator()
module_path = creator.create(params)
```

Interactive wizard:

```python
from module_creator_core.module_creation_wizard import run_module_creation_wizard, ModuleWizardArgs
from creator_common_core import QuestionaryCore
from logger_util import Logger

run_module_creation_wizard(
    prompter=QuestionaryCore(),
    logger=Logger("ModuleWizard"),
    prefilled=ModuleWizardArgs(name="my_tool", layer="dev"),
)
```

## API

```python
@dataclass
class ModuleCreationParams:
    module_name: str
    layer: str = "runtime"                          # foundation | runtime | dev
    is_mcp: bool = False
    description: str = ""
    repo_options: Optional[RepoCreationOptions] = None
    shows_in_workspace: Optional[bool] = None
    create_instructions: bool = False

class ModuleCreator:
    def __init__(self) -> None: ...
    def create(self, params: ModuleCreationParams) -> Path: ...

def validate_module_name(name: str) -> None: ...

# In module_creation_wizard.py:
@dataclass
class ModuleWizardArgs:
    name: Optional[str] = None
    layer: Optional[str] = None
    is_mcp: Optional[bool] = None
    description: Optional[str] = None
    create_instructions: Optional[bool] = None
    create_repo: Optional[bool] = None
    owner: Optional[str] = None
    visibility: Optional[str] = None

def run_module_creation_wizard(
    *,
    prompter: QuestionaryCore,
    logger: Logger,
    prefilled: Optional[ModuleWizardArgs] = None,
) -> None: ...
```

## Notes
- `ModuleCreator` writes `pyproject.toml` with `[tool.adhd]` containing `layer` and optional `mcp = true`.
- `validate_module_name` rejects Python keywords, names over 50 chars, and non-snake_case formats.
- The wizard normalizes names via `to_snake_case` and prompts for layer, MCP flag, instructions, and repo options.

## Requirements & prerequisites
- config-manager
- logger-util
- creator-common-core
- exceptions-core
- github-api-core
- modules-controller-core

## Troubleshooting
- **`ADHDError: Invalid module name`** – name must be snake_case, start with a letter, and not end with an underscore.
- **`ADHDError: Invalid layer`** – layer must be one of `foundation`, `runtime`, or `dev`.
- **Remote repo creation failed** – confirm GitHub CLI authentication and push rights for the selected owner.
- **`FileNotFoundError: Bundled template not found`** – the `data/templates/` directory is missing or incomplete.
- **MCP files not generated** – ensure `is_mcp=True` in `ModuleCreationParams`.

## Module structure

```
module_creator_core/
├─ __init__.py                    # exports ModuleCreator, ModuleCreationParams, validate_module_name
├─ module_creator.py              # ModuleCreator class and ModuleCreationParams dataclass
├─ module_creation_wizard.py      # interactive wizard and ModuleWizardArgs
├─ mcps_mod.py                    # MCP-specific file generation
├─ requirements.txt               # pip requirements
├─ pyproject.toml                 # package metadata and dependencies
├─ data/
│  ├─ templates/                  # embedded module scaffolding templates
│  └─ mcps_mod/                   # MCP-specific templates
└─ README.md                      # this file
```

## See also
- Creator Common Core – shared clone/repo helpers and QuestionaryCore
- GitHub API Core – low-level gh CLI wrapper for cloning and pushing
- Modules Controller Core – provides layer constants and module directory paths
- Project Creator Core – complementary scaffolder for full projects