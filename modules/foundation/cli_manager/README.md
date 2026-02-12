# CLI Manager

Centralized CLI command registration and admin CLI generation for ADHD projects.

## Overview

- Modules register their CLI commands via `CLIManager.register_module()`
- Commands are persisted to a JSON registry and used to build an `argparse`-based admin CLI
- Singleton pattern ensures consistent state across the project
- Supports module short names (aliases) with conflict detection

## Features

- Dataclass-based command and argument definitions (`Command`, `CommandArg`, `ModuleRegistration`)
- Thread-safe singleton with file-level locking for concurrent access
- Dynamic handler resolution via `module.path:function_name` strings
- Argparse integration with nested module → command subparsers
- Configurable admin CLI filename and output directory via Config Manager

## Quickstart

```python
from cli_manager import CLIManager, ModuleRegistration, Command, CommandArg

cli = CLIManager()
cli.register_module(ModuleRegistration(
    module_name="my_module",
    short_name="mm",
    description="My module commands",
    commands=[
        Command(
            name="run",
            help="Run the main task",
            handler="my_module.cli:run_handler",
            args=[
                CommandArg(name="--verbose", short="-v", action="store_true", help="Verbose output"),
            ],
        ),
    ],
))

# Build parser and dispatch
parser = cli.build_parser()
args = parser.parse_args()
cli.dispatch(args)
```

## API

```python
class CLIManager:                                   # singleton
    def register_module(self, registration: ModuleRegistration) -> bool: ...
    def unregister_module(self, module_name: str) -> bool: ...
    def get_registry(self) -> dict[str, dict]: ...
    def list_modules(self) -> list[str]: ...
    def build_parser(self, prog: str = "admin_cli", description: str = "Project Admin CLI") -> argparse.ArgumentParser: ...
    def dispatch(self, args: argparse.Namespace) -> int: ...
    def resolve_handler(self, handler_path: str) -> Callable | None: ...
    def get_admin_cli_path(self) -> Path: ...

@dataclass
class ModuleRegistration:
    module_name: str
    short_name: str | None = None
    description: str = ""
    commands: list[Command] = field(default_factory=list)

@dataclass
class Command:
    name: str
    help: str
    handler: str                                     # "module.path:function_name"
    args: list[CommandArg] = field(default_factory=list)

@dataclass
class CommandArg:
    name: str
    help: str = ""
    short: str | None = None
    type: str = "str"                                # str, int, float, bool
    required: bool = False
    default: Any = None
    nargs: str | None = None                         # ?, *, +
    choices: list | None = None
    action: str | None = None                        # store_true, store_false, count
```

## Notes

- Handler functions receive the parsed `argparse.Namespace` and return `int | None` (0 or None = success).
- The registry file is locked with `fcntl` for process-safe reads and writes.
- Short name conflicts are logged as warnings; the conflicting alias is silently dropped.

## Requirements & prerequisites

- `logger-util`
- `config-manager`

## Troubleshooting

- **Import error**: Ensure you import from the package — `from cli_manager import CLIManager`.
- **Handler not found**: Verify the `handler` string uses the format `package.module:function_name` and the target is importable.
- **Short name ignored**: Another module already claimed that alias; check the warning log.
- **Registry file missing**: `CLIManager` creates `commands.json` automatically on first use.
- **Permission errors**: The data directory must be writable; check path in `.config`.

## Module structure

```
cli_manager/
├─ __init__.py                  # exports CLIManager, Command, CommandArg, ModuleRegistration
├─ cli_manager.py               # singleton manager and parser builder
├─ cli_manager.instructions.md  # agent instructions
├─ refresh_full.py              # refresh hook
├─ .config_template             # default config schema
├─ pyproject.toml               # package metadata and dependencies
├─ data/                        # runtime registry storage
├─ tests/                       # unit tests
└─ README.md                    # this file
```

## See also

- Config Manager — configuration access used by CLIManager
- Logger Utility — logging used internally
- Modules Controller Core — module discovery and metadata
