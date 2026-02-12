# Workspace Core

Programmatic builder for VS Code `.code-workspace` files with layered configuration support.

## Overview
- Creates or updates `.code-workspace` files using a step-based builder pattern
- Composes workspace settings from multiple sources via `WorkspaceBuildingStep`
- Provides `generate_workspace_file` for one-call workspace creation from module data
- Validates file extensions, handles IO errors, and auto-creates missing files

## Features
- **Step-based construction** – add steps targeting specific parts of the workspace JSON
- **Deep key chaining** – `TargetLayer` ensures nested keys exist before applying updates
- **Safe persistence** – validates JSON serializability and handles file system errors
- **Auto-creation** – creates the workspace file and parent directories if they don't exist
- **One-call generation** – `generate_workspace_file` builds a complete workspace from module paths

## Quickstart

Build a workspace manually with steps:

```python
from workspace_core import WorkspaceBuilder, WorkspaceBuildingStep, TargetLayer

builder = WorkspaceBuilder("my-project.code-workspace")

# Add folders at root level
builder.add_step(
    WorkspaceBuildingStep(
        target=[],
        content={"folders": [{"path": "."}, {"path": "./libs"}]},
    )
)

# Add settings nested under "settings" key
builder.add_step(
    WorkspaceBuildingStep(
        target=[TargetLayer("settings", {})],
        content={"python.analysis.typeCheckingMode": "basic"},
    )
)

data = builder.build_workspace()
builder.write_workspace(data)
```

Generate a workspace from module data in one call:

```python
from pathlib import Path
from workspace_core import generate_workspace_file

modules = [{"path": "modules/runtime/my_module"}, {"path": "modules/dev/tools"}]
ws_path = generate_workspace_file(modules, root_path=Path("."))
```

## API

```python
@dataclass
class TargetLayer:
    target: str
    default: Dict | List

@dataclass
class WorkspaceBuildingStep:
    target: List[TargetLayer]
    content: Dict

class WorkspaceBuilder:
    def __init__(self, workspace_path: Optional[Union[str, Path]] = None) -> None: ...
    def add_step(self, step: WorkspaceBuildingStep) -> None: ...
    def clear_steps(self) -> None: ...
    def build_workspace(self) -> Dict: ...
    def write_workspace(self, workspace_data: Dict) -> None: ...

def generate_workspace_file(
    modules_data: List[Dict[str, Any]],
    root_path: Path,
    workspace_path: Optional[Path] = None,
) -> Path: ...
```

## Notes
- `TargetLayer` chains allow drilling into nested JSON (e.g., `settings` → `python`).
- `WorkspaceBuilder` defaults to `<cwd_name>.code-workspace` when no path is given.
- `generate_workspace_file` deduplicates folder entries and always includes the root folder.

## Requirements & prerequisites
- logger-util
- exceptions-core

## Troubleshooting
- **`ValueError: Invalid workspace file extension`** – ensure the path ends with `.code-workspace`.
- **`ADHDError: Unable to write workspace file`** – check file permissions and disk space.
- **`ADHDError: Unable to prepare workspace directory`** – parent directory cannot be created; check path validity.
- **Settings not appearing** – verify the `TargetLayer` chain points to the correct nesting level.
- **Duplicate folder entries** – `generate_workspace_file` deduplicates by path; manual steps do not.

## Module structure

```
workspace_core/
├─ __init__.py             # exports WorkspaceBuilder, WorkspaceBuildingStep, TargetLayer, generate_workspace_file
├─ workspace_builder.py    # builder logic and generate_workspace_file
├─ pyproject.toml          # package metadata and dependencies
└─ README.md               # this file
```

## See also
- Project Creator Core – uses this module to generate workspaces during project setup
- Config Manager – manages configuration that may be injected into workspace settings
- Logger Utility – logging used throughout the builder
