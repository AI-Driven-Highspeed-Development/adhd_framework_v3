# ADHD Framework v3

**AI-Driven Highspeed Development Framework** - A modular Python framework designed for AI agents to navigate and modify codebases effectively.

## Core Philosophy

The **ADHD Framework** is built on a single premise: **Create an expected, modular, and predictable environment for AI agents to operate effectively.**

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

3. **AI-Native Context** — Preset agents with specific roles (e.g., `HyperArch`, `HyperSan`, `HyperOrch`). Instruction files (`.instructions.md`) teach agents *how* to use the code. Skills provide domain-specific workflows.

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

## Typical Workflow

This is **not** vibe coding. You are the quality controller — the agents are your team. How well you can understand and organize your own thoughts determines project quality.

### 1. Create a New Project

From the framework repository, run the project creation wizard:

```bash
uv run adhd cp
```

Follow the interactive wizard to set up your project name, description, and initial modules. After creation, the framework automatically runs:
- **Sync** (`adhd s`) — installs dependencies and syncs the workspace
- **Full Refresh** (`adhd r -f`) — runs all refresh scripts, compiles Flow DSL, syncs instructions
- **Workspace Setup** (`adhd ws -r runtime`) — generates a `.code-workspace` file filtered to runtime modules

No manual initialization needed.

### 2. Open Your Project

Open the generated `.code-workspace` file in VS Code. The workspace shows only your runtime modules (where you'll develop) — foundation and dev modules are hidden to reduce noise.

### 3. Plan with HyperDream

Ask **HyperDream** to create a blueprint for your project vision. It creates structured plans in `.agent_plan/day_dream/` using the Story/Spec pattern:

- **Simple tier** (≤2 features): Single document with inline specs
- **Blueprint tier** (≥3 features): Full directory with index, executive summary, architecture, feature specs, and implementation plan

Example: *"@HyperDream Create a blueprint for a media management application with library scanning, metadata enrichment, and notification support."*

### 4. Validate with HyperSan

Have **HyperSan** review your blueprint before implementation. HyperSan checks for:
- Feasibility and technical constraints
- Logic gaps and missing edge cases
- Alignment with ADHD architecture patterns
- Module boundary correctness

### 5. Implement with HyperOrch

**HyperOrch** is your primary interface for complex tasks. It coordinates the full agent team automatically:

```
PRE-CHECK (HyperSan) → IMPLEMENT (HyperArch) → POST-CHECK (HyperSan + HyperIQGuard)
```

Just tell HyperOrch what you want to build — it handles delegation, quality gates, and workflow management.

HyperOrch supports multiple presets:
- **Implementation** — Build features with automated quality checks
- **Testing** — Plan → spec-test → adversarial attack → verify
- **Discussion** — Multi-agent collaborative analysis
- **Routing** — Automatic task-to-agent routing

Example: *"@HyperOrch Implement the library scanner module from the blueprint."*

### 6. Create Modules

Break your project into small, single-responsibility modules:

```bash
# Create a new module interactively
uv run adhd cm

# Add an existing module from a git repository
uv run adhd add https://github.com/org/some-module.git
```

Each module gets its own `pyproject.toml`, `refresh.py`, and optional `.instructions.md` for teaching agents how to use it.

### 7. Iterate

Use the full agent team as your development cycle matures:
- **HyperIQGuard** — Code quality audits and anti-pattern detection
- **HyperRed** — Adversarial testing to break assumptions and find edge cases
- **HyperAgentSmith** — Create new agents, instructions, and prompts as your project grows

### 8. Stuck? Tech Debt?

Modularity means you can always start a module fresh:

```bash
# Remove a problematic module
uv run adhd rm my_broken_module

# Recreate it from scratch
uv run adhd cm
```

Nuke it and rebuild with agents. Small modules make this cheap — you never lose more than one unit of work.

---

## CLI Reference

The framework provides two CLI entry points:

### Main CLI (`adhd`)

```bash
uv run adhd <command> [options]
```

| Command | Alias | Description |
|---------|-------|-------------|
| `create-project` | `cp` | Interactive wizard to create a new ADHD project |
| `create-module` | `cm` | Interactive wizard to create a new module from templates |
| `add` | `a` | Add an existing module to the workspace from a git repository |
| `remove` | `rm` | Remove a module from the workspace |
| `update` | `up` | Update a module (or all modules in a layer) to the latest version |
| `sync` | `s` | Synchronize dependencies with `uv sync` |
| `init` | `i` | Alias for `sync` (backward compatibility) |
| `refresh` | `r` | Run module refresh scripts and sync instructions |
| `list` | `ls` | List all discovered modules with filters |
| `info` | `in` | Show detailed info about a specific module |
| `workspace` | `ws` | Update VS Code `.code-workspace` file |
| `migrate` | `mg` | Migrate legacy `init.yaml` to `pyproject.toml` |
| `doctor` | `doc` | Health check for modules (missing deps, layer violations) |
| `deps` | `dp` | Dependency analysis and layer violation detection |

### Admin CLI (`admin_cli.py`)

A secondary CLI for module-registered commands. Modules register their own subcommands via `cli_manager`:

```bash
uv run python admin_cli.py <module> <command> [args...]
```

Modules like `flow_core` and `uv_migrator_core` register commands here (e.g., `flow compile`, `uv-migrator migrate`).

### Examples

```bash
# List all modules
uv run adhd ls

# List only foundation layer modules
uv run adhd ls --include foundation

# List with filter info
uv run adhd ls --show-filters

# Add an existing module from a git repository
uv run adhd add https://github.com/org/my-module.git

# Add a module from a monorepo subfolder
uv run adhd add https://github.com/org/monorepo.git --path modules/runtime/some_module

# Add without confirmation prompt
uv run adhd add https://github.com/org/my-module.git --skip-prompt

# Remove a module
uv run adhd rm my_module

# Remove with dry run preview
uv run adhd rm my_module --dry-run

# Update a single module
uv run adhd up my_module

# Update all modules in a layer
uv run adhd up --layer foundation

# Update with dry run
uv run adhd up my_module --dry-run

# Show info about a specific module
uv run adhd info -m config-manager

# Refresh all modules and sync instructions
uv run adhd refresh

# Refresh a specific module
uv run adhd refresh -m logger-util

# Full refresh (includes heavy refresh_full.py scripts)
uv run adhd refresh --full

# Run health check
uv run adhd doctor

# Check dependency tree for a module
uv run adhd deps --closure config-manager

# Check layer violations across all modules
uv run adhd deps --closure-all

# Update workspace file
uv run adhd ws

# Toggle a module's workspace visibility
uv run adhd ws -m some_module
```

### Adding External Modules

The `adhd add` command lets you add external ADHD modules to your workspace:

```bash
uv run adhd add <git_repository_url>
```

**What it does:**
1. Clones the module repository to a temporary location
2. Reads `pyproject.toml` to determine the module's layer and package name
3. Moves the module to the correct workspace directory (`modules/<layer>/<module_name>`)
4. Runs `uv sync` to register the module as a workspace member
5. Optionally adds the module to root `dependencies` if needed by the framework CLI

**Example:**

```bash
# Add a module from GitHub
uv run adhd add https://github.com/AI-Driven-Highspeed-Development/session_manager.git

# Output:
# 📥 Adding module from: https://github.com/.../session_manager.git
# 📦 Module name: session_manager
# 🔄 Cloning repository...
# 📊 Layer: runtime
# 🏷️  Package name: session-manager
# 📂 Moving to: modules/runtime/session_manager
# 🔄 Running uv sync to register workspace member...
# ✅ Module registered in workspace
# Add 'session-manager' to root dependencies (needed if adhd CLI imports it)? [y/N]: n
# ✅ Module 'session_manager' added successfully!
```

**Notes:**
- The module MUST have a valid `pyproject.toml` with `[project] name` and `[tool.adhd] layer`
- Auto-discovery works via UV workspace patterns - no manual configuration needed
- Only add to root dependencies if the framework CLI script imports the module at startup
- Most modules don't need to be in root dependencies (workspace auto-discovery handles them)

### Removing Modules

```bash
uv run adhd rm <module_name> [options]
```

| Flag | Description |
|------|-------------|
| `--force`, `-f` | Remove even if other modules depend on it |
| `--dry-run`, `-n` | Preview changes without modifying anything |
| `--no-confirm`, `-y` | Skip confirmation prompt |
| `--keep-dir` | Unregister from pyproject.toml but keep the directory |

### Updating Modules

```bash
# Single module
uv run adhd up <module_name> [options]

# All modules in a layer
uv run adhd up --layer <foundation|runtime|dev> [options]
```

| Flag | Description |
|------|-------------|
| `--dry-run`, `-n` | Preview changes without modifying anything |
| `--branch`, `-b` | Clone from a specific branch |
| `--keep-backup` | Keep the `.bak` directory after successful update |
| `--force`, `-f` | Update even if module has uncommitted local changes |
| `--continue-on-error` | Continue batch update even if a module fails (batch mode) |

---

## Project Structure

```
📦 adhd_framework_v3/
├── 📄 adhd_framework.py          # Main CLI entry point (`uv run adhd`)
├── 📄 admin_cli.py               # Admin CLI for module-registered commands
├── 📄 pyproject.toml             # Root workspace configuration
├── 📄 README.md                  # This file
├── 📁 modules/                   # All ADHD modules
│   ├── 📁 foundation/            # Core utilities (no ADHD cross-deps)
│   │   ├── 📁 cli_manager/
│   │   ├── 📁 config_manager/
│   │   ├── 📁 exceptions_core/
│   │   ├── 📁 logger_util/
│   │   ├── 📁 modules_controller_core/
│   │   └── 📁 temp_files_manager/
│   ├── 📁 runtime/               # Normal operational modules
│   │   └── (empty — project-specific modules go here)
│   └── 📁 dev/                   # Development-only tools
│       ├── 📁 adhd_mcp/          # MCP server for AI introspection
│       ├── 📁 creator_common_core/
│       ├── 📁 flow_core/         # Flow DSL compiler and LSP
│       ├── 📁 github_api_core/
│       ├── 📁 instruction_core/  # Agent/instruction/prompt sync
│       ├── 📁 module_creator_core/
│       ├── 📁 module_lifecycle_core/
│       ├── 📁 project_creator_core/
│       ├── 📁 uv_migrator_core/
│       └── 📁 workspace_core/
├── 📁 project/                   # Project-specific application code
│   └── 📁 data/                  # Project data (conventional location)
├── 📁 .github/                   # Synced agent/instruction/skill files
│   ├── 📁 agents/                # Agent definitions (*.adhd.agent.md)
│   ├── 📁 instructions/          # Instruction files (*.instructions.md)
│   ├── 📁 prompts/               # Reusable prompts (*.prompt.md)
│   └── 📁 skills/                # Agent skills (domain-specific workflows)
├── 📁 .agent_plan/               # Agent-generated plans and visions
│   ├── 📁 day_dream/             # Long-term planning documents
│   └── 📁 discussion/            # Multi-agent discussion artifacts
├── 📁 tests/                     # Project-level test files
└── 📁 playground/                # Exploration, demos, prototypes
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

### Current Modules

#### Foundation Layer (`modules/foundation/`)

| Module | Package Name | Description |
|--------|-------------|-------------|
| `exceptions_core` | `exceptions-core` | Base exception classes (`ADHDError` and subclasses) for the framework |
| `logger_util` | `logger-util` | Structured logging utility with Rich output and compact styles |
| `config_manager` | `config-manager` | Project and module configuration management (`.config` files, templates) |
| `cli_manager` | `cli-manager` | CLI command registration system for `admin_cli.py` |
| `modules_controller_core` | `modules-controller-core` | Module discovery, listing, doctor checks, dependency walking, migration, workspace generation |
| `temp_files_manager` | `temp-files-manager` | Temporary file and directory management with automatic cleanup |

#### Runtime Layer (`modules/runtime/`)

No runtime modules are included in the framework itself. This is where **project-specific** operational modules live when you build an application on top of the framework.

#### Dev Layer (`modules/dev/`)

| Module | Package Name | Description |
|--------|-------------|-------------|
| `adhd_mcp` | `adhd-mcp` | MCP server providing AI agents with project introspection, module management, and git operations |
| `instruction_core` | `instruction-core` | Syncs agents, instructions, prompts, and skills from module `data/` directories to `.github/` |
| `flow_core` | `flow-core` | Flow DSL compiler, parser, tokenizer, and Language Server Protocol (LSP) implementation |
| `module_creator_core` | `module-creator-core` | Interactive wizard for creating new modules from templates |
| `project_creator_core` | `project-creator-core` | Interactive wizard for creating new ADHD projects |
| `creator_common_core` | `creator-common-core` | Shared utilities and interactive prompter for project/module creators |
| `github_api_core` | `github-api-core` | GitHub API integration (repo creation, cloning, URL utilities) |
| `workspace_core` | `workspace-core` | VS Code `.code-workspace` file generation and management |
| `module_lifecycle_core` | `module-lifecycle-core` | Module lifecycle management — add from git, remove, and update modules |
| `uv_migrator_core` | `uv-migrator-core` | Migration tool for converting legacy `init.yaml` to `pyproject.toml` |

### Module Structure

Each module is a self-contained Python package:

```
📁 modules/<layer>/<module_name>/
├── 📄 __init__.py                    # Package exports
├── 📄 pyproject.toml                 # Module metadata (see below)
├── 📄 <module_name>.py               # Main implementation
├── 📄 refresh.py                     # Idempotent refresh script (optional)
├── 📄 refresh_full.py                # Heavy refresh operations (optional, run with --full)
├── 📄 <module_name>.instructions.md  # Agent context (optional)
├── 📄 .config_template               # Default config values (optional)
├── 📁 data/                          # Module-specific data (optional)
├── 📁 tests/                         # Module-level tests (optional)
├── 📁 playground/                    # Module-level exploration (optional)
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

## AI Context System

The framework provides a layered AI context system that teaches agents how to work with the codebase.

### Agents

Specialized AI agents, each with a distinct role:

| Agent | Alias | Role | Description |
|-------|-------|------|-------------|
| **HyperOrchestrator** | `HyperOrch` | Orchestrator | Universal orchestrator for multi-agent workflows. Routes tasks to specialists. |
| **HyperArchitect** | `HyperArch` | Lead Developer | Expert developer. Implements features with strict adherence to ADHD architecture. |
| **HyperSanityChecker** | `HyperSan` | QA & Auditor | Validates plans and code for logic flaws, feasibility, and alignment. |
| **HyperIQGuard** | — | Code Quality | Code quality guardian focusing on pragmatic fixes and anti-patterns. |
| **HyperDayDreamer** | `HyperDream` | Visionary | Visionary architect for long-term planning and conceptualization. |
| **HyperAgentSmith** | — | Instruction Architect | Creates and maintains agent, prompt, and instruction files. |
| **HyperExpedition** | `HyperExped` | Export Specialist | Exports ADHD agents and instructions to external projects (Vue3, React, Unity, etc.). |
| **HyperRed** | — | Adversarial Tester | Finds edge cases and breaks assumptions through stress testing. |

### Instructions

Instruction files (`.instructions.md`) provide contextual guidance to agents for specific domains:

| Instruction | Applies To | Purpose |
|-------------|-----------|---------|
| `adhd_framework_context` | All agents | Core framework philosophy and structure |
| `agent_common_rules` | Agent files | Shared rules for all ADHD agents |
| `agents_format` | `*.agent.md` | Agent file format specification |
| `cli_manager` | `*_cli.py` | CLI registration patterns |
| `config_manager` | `*.py` | Configuration access patterns |
| `exceptions` | `*.py` | Exception hierarchy and usage |
| `flow_format` | `*.flow` | Flow DSL syntax rules |
| `hyper_san_output` | HyperSan agent | Output format for sanity checks |
| `instructions_format` | `*.instructions.md` | How to write instruction files |
| `logger_util` | `*.py` | Logging patterns and usage |
| `mcp_development` | `*_mcp.py` | MCP server development patterns |
| `module_development` | `modules/**/*.py` | Module coding standards |
| `module_instructions` | Module instructions | How to write module-level instructions |
| `modules_readme` | Module READMEs | README format for modules |
| `non_vibe_code` | `*.py` | Anti-hallucination and quality rules |
| `prompts_format` | `*.prompt.md` | Prompt file format specification |

### Skills

Skills provide tested, domain-specific workflows that agents can load on demand:

| Skill | Purpose |
|-------|---------|
| `day-dream` | Vision and planning — blueprints, roadmaps, feature templates |
| `dream-planning` | DREAM decomposition — magnitude-gated routing, plan/task hierarchy |
| `expedition` | Framework export — 8-phase pipeline for exporting agents to external projects |
| `orch-discussion` | Structured multi-agent discussion protocol |
| `orch-expedition` | Orchestrating the expedition export pipeline |
| `orch-implementation` | Coordinating implementation with quality gates |
| `orch-routing` | Routing requests to the correct specialist agent |
| `orch-testing` | Coordinating testing workflows (plan → spec → attack → verify) |
| `testing` | Test conventions, folder locations, pytest patterns |
| `writing-flows` | Flow DSL syntax and agent authoring patterns |
| `writing-skills` | How to write proper SKILL.md files |
| `writing-templates` | Template file creation for day-dream artifacts |

### Prompts

Reusable prompt files (`.prompt.md`) for common operations:

| Prompt | Purpose |
|--------|---------|
| `pull_modules` | Pull latest changes across modules |
| `push_modules` | Commit and push module changes |
| `update_requirements` | Update module requirements |

### How the Context System Works

1. **Source Location**: Agent definitions, instructions, and skills live in `modules/dev/instruction_core/data/`
2. **Module-Level Context**: Each module can have its own `<name>.instructions.md` file
3. **Sync**: Running `uv run adhd refresh` compiles Flow DSL files and copies everything to `.github/agents/`, `.github/instructions/`, `.github/prompts/`, and `.github/skills/`
4. **VS Code Integration**: VS Code Copilot automatically picks up files from `.github/` for custom instructions and agents

**To use an agent**: In VS Code Copilot Chat, type `@` followed by the agent name (e.g., `@HyperArch`).

### Agent Pipeline (Quick Reference)

```
HyperDream (vision) → HyperSan (validate) → HyperOrch (coordinate) 
    → HyperArch (implement) → HyperSan (review) → HyperIQGuard (quality)
```

See the [Typical Workflow](#typical-workflow) section for detailed step-by-step guidance.

### Flow DSL

The framework includes a custom **Flow DSL** for authoring agent definitions declaratively. Flow files (`.flow`) are compiled into markdown agent files by `flow_core`:

- **Parser & Tokenizer**: Parses `.flow` syntax with nodes, pipes, and content blocks
- **Compiler**: Compiles `.flow` + `.yaml` sidecar files into `.agent.md` output
- **LSP**: Language Server Protocol implementation for Flow DSL editor support
- **Dependency Graph**: Resolves imports and shared fragments (`_lib/`)

Run `uv run adhd refresh --full` to recompile all Flow files.

---

## DREAM System

**DREAM** (Decomposition Rules for Engineering Atomic Modules) is the framework's structured planning and decomposition protocol. It breaks complex work into parallelizable, isolated units that agents can execute independently.

### Day-Dream: Vision & Blueprint Planning

HyperDream creates structured plans in `.agent_plan/day_dream/` using a tiered approach:

#### Simple Tier (≤2 features)
A single document with inline feature specifications. Suitable for small enhancements or focused changes.

#### Blueprint Tier (≥3 features)
A full directory structure for complex projects:

```
📁 .agent_plan/day_dream/<vision_name>/
├── 📄 index.md                    # Blueprint index and navigation
├── 📄 executive_summary.md        # High-level goals and constraints
├── 📄 architecture.md             # System architecture and module boundaries
├── 📁 features/                   # Individual feature specifications
│   ├── 📄 feature_1.md            # Story/Spec pattern: user story + technical spec
│   ├── 📄 feature_2.md
│   └── 📄 feature_3.md
└── 📄 implementation_plan.md      # Phased execution order
```

Feature documents follow the **Story/Spec pattern**: each feature has a user-facing story (what and why) paired with a technical specification (how and where).

### DREAM Planning: Task Decomposition

When implementing blueprints, the DREAM system uses magnitude-based routing to decide how to decompose work:

| Magnitude | Scope | Routing |
|-----------|-------|---------|
| **Trivial** | Single function or config change | Execute inline, no decomposition |
| **Light** | Single file, small feature | Single agent task |
| **Standard** | Multi-file, one module | Plan with 2-4 subtasks |
| **Heavy** | Multi-module feature | Plan with subtasks, parallel execution |
| **Epic** | Cross-cutting, architectural | Nested plans, phased rollout |

Decomposition uses two primitives:
- **Plans** — Directories containing `_overview.md` and child tasks. Represent compound work.
- **Tasks** — Leaf files representing atomic, executable units of work.

#### Isolation Rules

- **Sibling Firewall**: Sibling tasks never read each other's content. Each task gets only the context it needs from its parent plan.
- **MANAGER/WORKER Pattern**: The orchestrator (MANAGER) creates plans and dispatches tasks. Workers execute tasks in isolation and report results back.

This isolation ensures agents don't create cross-dependencies between parallel work streams, keeping each unit independently executable.

### Using DREAM in Practice

1. **Ask HyperDream** to create a blueprint for your vision
2. **Have HyperSan** validate the blueprint for completeness and feasibility
3. **Use HyperOrch** to implement the blueprint phase by phase — it automatically decomposes work using DREAM magnitude routing
4. **Iterate**: Each phase produces working, tested code before the next phase begins

The DREAM system ensures complex projects are broken down systematically rather than attempted all at once. You always know where you are in the plan, what's done, and what's next.

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

## MCP Server

The `adhd_mcp` module provides a **Model Context Protocol (MCP)** server that gives AI agents introspection capabilities:

- **Project info** — Query project metadata and structure
- **Module listing** — Discover and filter modules by layer
- **Module details** — Deep-dive into a module's dependencies, imports, and git status
- **Context files** — List available agents, instructions, prompts, and skills
- **Git operations** — Status, diff, pull, and push across modules
- **Module creation** — Scaffold new modules via MCP tools

The MCP server is configured automatically for VS Code Copilot when the framework is set up.

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

# Full refresh (compile flows + heavy operations)
uv run adhd refresh --full

# Run module health check
uv run adhd doctor

# Check for layer violations across all modules
uv run adhd deps --closure-all
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
