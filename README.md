# ADHD Framework v3

**AI-Driven Highspeed Development Framework** - A modular Python framework designed for AI agents to navigate and modify codebases effectively.

## Core Philosophy

The **ADHD Framework** is built on a single premise: **AI agents are the new developers, and they need a workspace designed for them.**

### The "Vibe Coding" Trap

Modern "vibe coding" with LLMs is deceptively fast. You can generate a prototype in minutes. But as complexity grows, you hit the **Context Wall**:
- **Objective Misalignment**: Agents misunderstand project goals without clear guidance.
- **Forced Solutions**: Agents hack around limitations instead of addressing root causes.
- **Hallucinations**: Agents lose track of large file structures.
- **Regression**: Fixing one bug breaks three other features.
- **Scalability**: "One giant script" architectures collapse under their own weight.

### The ADHD Solution

We treat the codebase as a **Structured Knowledge Graph** rather than just text files:

1. **Fractal Modularity** — Everything is a module with its own `pyproject.toml` (metadata), `refresh.py` (state management), and `*.instructions.md` (agent context). Agents only load what they need.

2. **Layer Hierarchy** — Modules are organized into `foundation`, `runtime`, and `dev` layers with enforced dependency rules. Lower layers cannot depend on higher layers.

3. **AI-Native Context** — Preset agents with specific roles (e.g., `HyperArch`, `HyperSan`, `HyperOrch`). Instruction files (`.instructions.md`) teach agents *how* to use the code.

4. **UV Workspace** — Modern Python tooling with `uv` for dependency management. No more path hacks or import gymnastics.

---

## Quick Start

### Prerequisites

- **Python 3.11+**
- **[UV](https://docs.astral.sh/uv/)** — Modern Python package manager
- **Git** (configured with SSH or HTTPS)
- **GitHub CLI (`gh`)** — Run `gh auth login` to authenticate
- **Visual Studio Code** — Required for agent integrations

### Installation

```bash
# Clone the repository
git clone https://github.com/AI-Driven-Highspeed-Development/adhd_framework_v3.git
cd adhd_framework_v3

# Install dependencies and sync workspace
uv sync

# Run the ADHD CLI
uv run adhd

# Verify installation
uv run adhd list
```

---

## CLI Reference

The framework provides an `adhd` CLI entry point:

```bash
uv run adhd <command> [options]
```

| Command | Alias | Description |
|---------|-------|-------------|
| `create-project` | `cp` | Interactive wizard to create a new ADHD project |
| `create-module` | `cm` | Interactive wizard to create a new module from templates |
| `sync` | `s` | Synchronize dependencies with `uv sync` |
| `init` | `i` | Alias for `sync` (backward compatibility) |
| `refresh` | `r` | Run module refresh scripts and sync instructions |
| `list` | `ls` | List all discovered modules with filters |
| `info` | `in` | Show detailed info about a specific module |
| `workspace` | `ws` | Update VS Code `.code-workspace` file |
| `migrate` | `mg` | Migrate legacy `init.yaml` to `pyproject.toml` |
| `doctor` | `doc` | Health check for modules (missing deps, layer violations) |
| `deps` | `dp` | Dependency analysis and layer violation detection |

### Examples

```bash
# List all modules
uv run adhd ls

# List only foundation layer modules
uv run adhd ls --layer foundation

# Show info about a specific module
uv run adhd info -m config-manager

# Refresh a specific module
uv run adhd refresh -m logger-util

# Run health check
uv run adhd doctor

# Check for dependency issues
uv run adhd deps
```

---

## Project Structure

```
📦 adhd_framework_v3/
├── 📄 adhd_framework.py          # Main CLI entry point
├── 📄 pyproject.toml             # Root workspace configuration
├── 📄 README.md                  # This file
├── 📁 modules/                   # All ADHD modules
│   ├── 📁 foundation/            # Core utilities (no ADHD cross-deps)
│   │   ├── 📁 logger_util/
│   │   ├── 📁 config_manager/
│   │   ├── 📁 exceptions_core/
│   │   └── ...
│   ├── 📁 runtime/               # Normal operational modules
│   │   └── ...
│   └── 📁 dev/                   # Development-only tools
│       └── 📁 adhd_mcp/          # MCP server for AI introspection
├── 📁 project/                   # Project-specific files
│   └── 📁 data/                  # Project data (conventional location)
├── 📁 .github/                   # Synced agent/instruction files
│   ├── 📁 agents/                # Agent definitions (*.adhd.agent.md)
│   ├── 📁 instructions/          # Instruction files (*.instructions.md)
│   └── 📁 prompts/               # Reusable prompts (*.prompt.md)
├── 📁 .agent_plan/               # Agent-generated plans and visions
│   └── 📁 day_dream/             # Long-term planning documents
└── 📁 tests/                     # Test files
```

---

## Module Architecture

### Layer Hierarchy

Modules are organized into three layers with strict dependency rules:

| Layer | Directory | Purpose | Can Depend On |
|-------|-----------|---------|---------------|
| **foundation** | `modules/foundation/` | Core infra, bootstrap-time utilities | External packages only |
| **runtime** | `modules/runtime/` | Normal operational modules | foundation + external |
| **dev** | `modules/dev/` | Development-only tools (MCPs, testers) | All layers + external |

> **Layer Rule**: Modules can only depend on modules in the same or lower layers. `foundation < runtime < dev`

### Module Structure

Each module is a self-contained Python package:

```
📁 modules/<layer>/<module_name>/
├── 📄 __init__.py                    # Package exports
├── 📄 pyproject.toml                 # Module metadata (see below)
├── 📄 <module_name>.py               # Main implementation
├── 📄 refresh.py                     # Idempotent refresh script (optional)
├── 📄 <module_name>.instructions.md  # Agent context (optional)
├── 📄 .config_template               # Default config values (optional)
├── 📁 data/                          # Module-specific data (optional)
└── 📄 README.md                      # Module documentation
```

### Module `pyproject.toml`

Modules use standard `pyproject.toml` with an `[tool.adhd]` section:

```toml
[project]
name = "my-module"
version = "1.0.0"
description = "ADHD Framework module: my_module"
requires-python = ">=3.11"
dependencies = [
    "logger-util",        # ADHD module dependency
    "requests>=2.28",     # External dependency
]

[project.urls]
Repository = "https://github.com/org/my-module.git"

[tool.adhd]
layer = "runtime"         # foundation | runtime | dev
mcp = false               # true if this is an MCP server

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Adding Modules

The framework uses UV workspace with glob patterns for auto-discovery:

```toml
# Root pyproject.toml
[tool.uv.workspace]
members = [
    "modules/foundation/*",
    "modules/runtime/*",
    "modules/dev/*",
]
```

**To add a new module:**

```bash
# Clone into the appropriate layer directory
git clone https://github.com/org/my-module.git modules/runtime/my_module

# Sync workspace (auto-detects new member)
uv sync

# Module is now importable
python -c "from my_module import something"
```

### Module Distribution

There are **3 ways to include external modules** in your ADHD project:

#### Method 1: Monorepo Subdirectory Import

Use when pulling a specific module from another ADHD project's monorepo.

```toml
[tool.uv.sources]
some-module = { git = "https://github.com/org/adhd-project.git", subdirectory = "modules/foundation/some_module" }
```

**Best for**: Cherry-picking individual modules from other ADHD monorepos without cloning the entire project.

#### Method 2: Standalone Git Repository

Use when the module has its own dedicated repository.

```toml
[tool.uv.sources]
some-module = { git = "https://github.com/org/some-module.git", tag = "v1.0.0" }
```

**Best for**: Shared modules maintained as separate repos. Supports `tag`, `branch`, or `rev` (commit hash).

#### Method 3: PyPI Package

Use for formally released modules on PyPI.

```toml
[project]
dependencies = [
    "some-module>=1.0.0",
]
# No [tool.uv.sources] entry needed - UV fetches from PyPI by default
```

**Best for**: Stable, versioned public releases with semantic versioning.

#### Comparison Table

| Method | Use Case | `pyproject.toml` Syntax | Version Control |
|--------|----------|-------------------------|-----------------|
| Monorepo Subdirectory | Pull from ADHD monorepo | `{ git = "...", subdirectory = "..." }` | tag / branch / commit |
| Standalone Git Repo | Module has own repo | `{ git = "...", tag = "v1.0.0" }` | tag / branch / commit |
| PyPI Package | Public release | `"package>=1.0"` (no source entry) | Semantic version |

### Publishing Modules

To share your modules with others, publish them using one of these methods:

#### Publish to Monorepo (Internal Sharing)

Keep modules in the ADHD monorepo structure. Consumers use subdirectory imports:

```bash
# Your monorepo layout
modules/foundation/my_module/
# Consumers reference via:
{ git = "https://github.com/you/your-adhd-project.git", subdirectory = "modules/foundation/my_module" }
```

#### Publish to Standalone Repository

Extract a module to its own git repository:

```bash
# Create standalone repo from module
cd modules/foundation/my_module
git init
git remote add origin https://github.com/org/my-module.git
git push -u origin main
git tag v1.0.0 && git push --tags
```

#### Publish to PyPI

For formal releases with semantic versioning:

```bash
# Build and publish (from module directory)
uv build
uv publish
```

Requires PyPI credentials configured. See [UV documentation](https://docs.astral.sh/uv/guides/publish/) for details.

---

## Agents

The framework includes specialized AI agents, each with a distinct role:

| Agent | Alias | Role | Description |
|-------|-------|------|-------------|
| **HyperOrchestrator** | `HyperOrch` | Orchestrator | Coordinates multi-agent workflows. Routes tasks to specialists. |
| **HyperArchitect** | `HyperArch` | Lead Developer | Implements features with strict adherence to ADHD architecture. |
| **HyperSanityChecker** | `HyperSan` | QA & Auditor | Reviews plans and code for logic flaws and security risks. |
| **HyperIQGuard** | — | Code Quality | Identifies anti-patterns, redundancy, and inefficiencies. |
| **HyperDayDreamer** | `HyperDream` | Visionary | Long-term planning and conceptualization. Documents future visions. |
| **HyperAgentSmith** | — | Agent Creator | Creates and maintains agent/instruction/prompt files. |
| **HyperExpedition** | `HyperExped` | Export Specialist | Exports ADHD agents to external projects (Vue3, React, Unity, etc.). |
| **HyperRed** | — | Adversarial Tester | Finds edge cases and breaks assumptions through stress testing. |

### How Agents Work

1. **Source Location**: Agent definitions live in `modules/foundation/instruction_core/data/`
2. **Sync**: Running `uv run adhd refresh` copies files to `.github/agents/`, `.github/instructions/`, and `.github/prompts/`
3. **VS Code Integration**: VS Code Copilot automatically picks up files from `.github/` for custom instructions

**To use an agent**: In VS Code Copilot Chat, type `@` followed by the agent name (e.g., `@HyperArch`).

### Typical Workflow

```
HyperDream (vision) → HyperSan (validate) → HyperOrch (coordinate) 
    → HyperArch (implement) → HyperSan (review) → HyperIQGuard (quality)
```

---

## Configuration Management

The `config_manager` module handles project and module configuration:

1. Each module can have a `.config_template` file with default values
2. On refresh, templates are merged into the project's root `.config` file
3. Access configuration via:

```python
from config_manager import ConfigManager

cm = ConfigManager()
config = cm.config.my_module_name
data_path = config.paths.data
value = config.dict_get('some_key')
```

See `modules/foundation/config_manager/README.md` for detailed usage.

---

## Development

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run a specific module's refresh script
uv run adhd refresh -m instruction-core
```

### Tab Completion (Linux/Mac)

The CLI supports tab completion via `argcomplete`:

```bash
# Add to your shell config (~/.bashrc or ~/.zshrc)
eval "$(register-python-argcomplete adhd)"

# Usage
uv run adhd <TAB>           # Shows available commands
uv run adhd info -m <TAB>   # Shows available module names
```

---

## Troubleshooting

### UV Not Found

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Module Import Errors

Ensure you're running commands from the project root and have synced:

```bash
uv sync
uv run adhd doctor  # Check for issues
```

### GitHub CLI Not Authenticated

```bash
gh auth login
```

### Module Not Found

```bash
uv run adhd list  # See available modules and their exact names
```

---

## License

See LICENSE file for details.
