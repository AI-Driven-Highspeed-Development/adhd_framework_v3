# UV Migrator Core

Migration tool that converts ADHD framework modules from legacy `init.yaml` format to `pyproject.toml`.

## Overview
- Converts module metadata from `init.yaml` to uv-compatible `pyproject.toml` format
- Supports single-module and batch migration with dry-run preview
- Automatically infers layer classification and converts GitHub URLs to package dependencies

## Features
- **Single module migration** – `migrate_module` converts one module with optional dry-run
- **Batch migration** – `migrate_all` processes all discovered modules
- **Preview mode** – `preview_migration` returns generated content without writing
- **Safe mode** – `no_overwrite` flag skips modules with existing `pyproject.toml`
- **Layer inference** – determines `foundation`, `runtime`, or `dev` from module path
- **GitHub URL conversion** – converts GitHub URLs to `[tool.uv.sources]` workspace entries
- **Template-based generation** – uses composable template parts for consistent output

## Quickstart

```python
from uv_migrator_core import UVMigratorCore

migrator = UVMigratorCore()

# Migrate a single module
result = migrator.migrate_module("session_manager")
print(result.success, result.message)

# Preview without writing
content = migrator.preview_migration("session_manager")
print(content)

# Migrate all modules
report = migrator.migrate_all(dry_run=False)
report.print_summary(migrator.logger)
```

## API

```python
@dataclass
class MigrationResult:
    module_name: str
    success: bool
    message: str
    output_path: Path | None = None
    content: str | None = None

@dataclass
class MigrationReport:
    results: list[MigrationResult]
    @property
    def successful(self) -> list[MigrationResult]: ...
    @property
    def failed(self) -> list[MigrationResult]: ...
    def print_summary(self, logger: Logger) -> None: ...

class UVMigratorCore:
    def __init__(self, root_path: Path | None = None): ...
    def migrate_module(self, module_name: str, dry_run=False, no_overwrite=False) -> MigrationResult: ...
    def migrate_all(self, dry_run=False, no_overwrite=False, include_cores=True) -> MigrationReport: ...
    def preview_migration(self, module_name: str) -> str | None: ...

# Low-level conversion functions (migrator.py)
def parse_init_yaml(module_path: Path) -> dict: ...
def parse_requirements_txt(module_path: Path) -> list[str]: ...
def github_url_to_package_name(url: str) -> str: ...
def convert_requirements(requirements: list) -> tuple[list[str], dict]: ...
def infer_layer(module_path: Path) -> str: ...
def generate_pyproject_toml(module_path: Path, dry_run=False) -> str: ...
```

## Notes
- This is a dev-only migration tool used during the `init.yaml` → `pyproject.toml` transition.
- Layer inference defaults: `cores/utils → foundation`, `managers/plugins → runtime`, `mcps → dev`.
- Some known dev-only cores (e.g., `module_creator_core`, `project_creator_core`) override the foundation default.

## Requirements & prerequisites
- `logger-util`
- `modules-controller-core`
- `pyyaml>=6.0`

## Troubleshooting
- **`FileNotFoundError: No init.yaml`** – the target module has no legacy `init.yaml` to migrate.
- **Layer inferred incorrectly** – check the module's folder location; override via `[tool.adhd].layer` in the generated `pyproject.toml`.
- **GitHub URLs not converted** – ensure URLs follow `https://github.com/<org>/<repo>.git` format.
- **`no_overwrite` skips everything** – modules that already have `pyproject.toml` are intentionally skipped.

## Module structure

```
uv_migrator_core/
├─ __init__.py              # exports UVMigratorCore, MigrationResult, MigrationReport, helpers
├─ uv_migrator_core.py      # UVMigratorCore controller
├─ migrator.py              # conversion logic (parse, convert, generate)
├─ templates.py             # pyproject.toml template strings
├─ uv_migrator_cli.py       # CLI command registration
├─ refresh.py               # framework refresh hook
├─ pyproject.toml           # module metadata
├─ requirements.txt         # PyPI dependencies
├─ README.md                # this file
├─ tests/                   # unit tests
└─ playground/              # interactive exploration
```

## See also
- Modules Controller Core – module discovery used to find migration targets
- Logger Util – logging throughout migration operations
- Config Manager – project root path resolution