# Instruction Core

## Overview
Manages synchronization of AI context files (instructions, agents, prompts) from source directories to target directories (e.g., `.github/`). This enables VS Code Copilot to access project-specific agent configurations and instructions.

Supports two sync modes:
- **Official sync**: From `cores/instruction_core/data/` to configured target directories
- **Custom sync**: From project-specific data path to configured target directories

## Features
- Syncs `.instructions.md`, `.agent.md`, and `.prompt.md` files
- Scans all modules for their instruction/agent/prompt files
- **MCP Permission Injection**: Injects project-specific tool permissions into copied agent files

## Configuration
Located in `.config` (generated from `.config_template`):

```json
{
    "module_name": "instruction_core",
    "path": {
        "data": "./project/data/instruction_core",
        "official_target_dir": ["./.github"],
        "custom_target_dir": [],
        "mcp_permission_injection_json": "./project/data/instruction_core/mcp_permission_injection.json"
    }
}
```

## MCP Permission Injection
Allows projects to add project-specific MCP tools to agents without modifying the source agent files.

### JSON Format
Create a JSON file at the configured `mcp_permission_injection_json` path:

```json
{
    "hyper_architect": ["unity_adhd_mcp/*", "custom_tool"],
    "hyper_san_checker": ["unity_adhd_mcp/some_tool"]
}
```

- **Keys**: Agent filename stem (e.g., `hyper_architect` from `hyper_architect.adhd.agent.md`)
- **Values**: List of tool strings to inject into the agent's `tools:` YAML field

### Behavior
- Injection happens **after** copying to target directory (source files remain unchanged)
- Tools are deduplicated while preserving order
- Missing/empty JSON file is gracefully handled (no injection occurs)

## Usage
Typically invoked via the refresh command:

```bash
python adhd_framework.py refresh --module instruction_core
```

Or programmatically:

```python
from cores.instruction_core.instruction_controller import InstructionController

controller = InstructionController()
controller.run()
```

## Module Structure
```
instruction_core/
├── __init__.py
├── init.yaml
├── instruction_controller.py    # Main controller class
├── refresh.py                   # Refresh entry point
├── README.md
└── data/
    ├── agents/                  # Official agent definitions
    ├── instructions/            # Official instruction files
    └── prompts/                 # Official prompt files
```