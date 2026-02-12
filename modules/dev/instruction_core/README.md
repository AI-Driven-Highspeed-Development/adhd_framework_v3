# Instruction Core

Compiles Flow files and synchronizes instructions, agents, and prompts across configured targets.

## Overview

- Orchestrates the full instruction lifecycle: compile `.flow` sources, sync outputs to target directories.
- Supports official and custom sync targets, each configurable as a list of paths via `ConfigManager`.
- Incrementally compiles `.flow` files using SHA-256 manifest caching to skip unchanged sources.
- Injects MCP tool permissions into agent YAML headers during sync.
- Generates a skills index from discovered skill directories.

## Features

- Incremental `.flow` compilation with transitive-hash cache invalidation.
- Sidecar `.yaml` frontmatter prepended to compiled agent files.
- Multi-target sync for official and custom source directories.
- MCP permission injection into `.agent.md` files from a JSON config.
- Skills index generation from `SKILL.md` frontmatter.
- Module-level instruction/agent/prompt file collection across all workspace modules.

## Quickstart

```python
from instruction_core import InstructionController
from logger_util import Logger
from pathlib import Path

logger = Logger(name="InstructionSync")
controller = InstructionController(root_path=Path.cwd(), logger=logger)

# Full sync: compile flows, sync to all targets, generate skills index
controller.run()

# Compile only (no sync) — useful for CI validation
manifest = controller.compile_only(force=True)
```

## API

```python
class InstructionController:
    def __init__(self, root_path: Optional[Path] = None, logger: Optional[Logger] = None): ...
    def run(self) -> None: ...
    def compile_only(self, force: bool = False) -> dict: ...
```

- `__init__`: Loads config via `ConfigManager`, resolves official/custom source and target paths.
- `run()`: Full pipeline — compile `.flow` files, sync to all configured targets, inject MCP permissions, generate skills index.
- `compile_only(force)`: Compile `.flow` files and write manifest without syncing. Returns manifest dict. Pass `force=True` to ignore cache.

## Notes

- Config is read from the `instruction_core` section via `ConfigManager`. Key paths: `path.data`, `path.official_target_dir`, `path.custom_target_dir`, `path.mcp_permission_injection_json`.
- Flow files under `data/flows/_lib/` are treated as shared fragments and excluded from standalone compilation.
- Output filenames are derived from subdirectory: `flows/agents/foo.flow` → `agents/foo.adhd.agent.md`, `flows/instructions/bar.flow` → `instructions/bar.instructions.md`.

## Requirements & prerequisites

- `exceptions-core` — ADHD exception hierarchy
- `modules-controller-core` — module discovery and enumeration
- `logger-util` — structured logging
- `config-manager` — configuration loading
- `flow-core` — Flow DSL compiler
- `pyyaml>=6.0` — YAML parsing

## Troubleshooting

- **"No official targets configured"**: Set `instruction_core.path.official_target_dir` in your project config to a list of target paths.
- **Compilation skipped for unchanged files**: Pass `force=True` to `compile_only()` or delete `data/compiled/compiled_manifest.json` to force full recompilation.
- **MCP injection not applying**: Verify the JSON file at `path.mcp_permission_injection_json` exists, contains a valid dict mapping agent keys to tool lists, and that agent files have a `tools: [...]` line in their YAML header.
- **Import errors**: Ensure all dependencies are installed in the workspace. Run `uv sync` from the project root.
- **Skills index empty**: Check that skill directories contain a `SKILL.md` with valid YAML frontmatter (`name`, `description` fields).

## Module structure

```
instruction_core/
├─ __init__.py              # exports InstructionController
├─ instruction_controller.py # main implementation
├─ refresh_full.py          # CLI refresh entry point
├─ .config_template         # default config keys
├─ pyproject.toml           # package metadata and dependencies
├─ data/                    # official source data
│  ├─ compiled/             # compiled flow output and manifest
│  ├─ flows/                # .flow source files
│  ├─ instructions/         # instruction files
│  ├─ prompts/              # prompt files
│  └─ skills/               # skill directories
└─ playground/              # exploration scripts
```

## See also

- Flow Core — Flow DSL compiler used for `.flow` compilation
- Config Manager — configuration loading for sync paths
- Modules Controller Core — module discovery for collecting per-module files
- Logger Util — structured logging
