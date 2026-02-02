# ADHD Framework v3

AI-Driven Highspeed Development Framework - A modular Python framework for rapid development.

## Getting Started

```bash
# Clone the repository
git clone <repo-url>
cd adhd_framework_v3

# Install dependencies and sync workspace
uv sync

# Run the ADHD CLI
uv run adhd
```

## CLI Commands

The framework provides an `adhd` CLI entry point:

```bash
# Initialize a new project
uv run adhd init

# Refresh module registrations
uv run adhd refresh

# List available modules
uv run adhd list

# Get help
uv run adhd --help
```

## Project Structure

```
adhd_framework_v3/
├── cores/       # Core modules (workspace members)
├── managers/    # Manager modules (workspace members)
├── utils/       # Utility modules (workspace members)
├── mcps/        # MCP modules (workspace members)
├── plugins/     # Plugin modules (workspace members)
└── pyproject.toml  # Root workspace configuration
```

## Module Inclusion

The framework uses UV workspace with glob patterns for module auto-discovery. There are three patterns for including modules:

### Pattern 1: Workspace Member (ADHD Module)

Clone a module into a workspace directory and UV auto-detects it:

```bash
# Clone module to workspace directory
git clone https://github.com/org/my_module.git cores/my_module

# Sync workspace (auto-detects new member via glob pattern)
uv sync

# Module is now importable
python -c "from my_module import something"
```

**Why this works:** The root `pyproject.toml` defines workspace members with glob patterns:

```toml
[tool.uv.workspace]
members = ["cores/*", "managers/*", "utils/*", "plugins/*", "mcps/*"]
```

New directories matching these patterns are automatically included in the workspace.

### Pattern 2: External Dependency (PyPI Package)

Add third-party packages from PyPI:

```bash
# Add a PyPI package
uv add requests

# Add with version constraint
uv add "requests>=2.28"
```

### Pattern 3: Path Dependency (Local Development)

For local modules outside the workspace (e.g., cross-project development):

```bash
# Add local module as editable dependency
uv add --path ../shared-utils
```

This adds to your `pyproject.toml`:

```toml
[tool.uv.sources]
shared-utils = { path = "../shared-utils" }
```

## Development

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```
