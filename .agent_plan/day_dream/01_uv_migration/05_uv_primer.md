# 📘 UV Primer: Beginner's Guide

> *A gentle introduction to `uv` for developers new to modern Python packaging.*

**Document Type:** Educational Reference  
**Audience:** Developers new to `uv` or transitioning from pip/poetry  
**Prerequisites:** Basic Python knowledge, familiarity with virtual environments concept

---

## 🎯 What is UV?

**UV** is a blazing-fast Python package manager written in Rust, created by [Astral](https://astral.sh/) (the same team behind [Ruff](https://docs.astral.sh/ruff/), the fast Python linter).

### The Elevator Pitch

> *"UV is pip, pip-tools, virtualenv, poetry, and pyenv—combined into one tool that's 10-100x faster."*

### What UV Replaces

| Old Tool(s) | What It Did | UV Equivalent |
|-------------|-------------|---------------|
| `pip` | Install packages | `uv add`, `uv pip install` |
| `pip-tools` | Lock dependencies | `uv lock` |
| `virtualenv` / `venv` | Create environments | Auto-managed by `uv sync` |
| `poetry` | Project management | `uv init`, `pyproject.toml` |
| `pyenv` | Python version management | `uv python install` |

### Key Benefits

| Benefit | Description |
|---------|-------------|
| ⚡ **Speed** | 10-100x faster than pip (Rust-based resolver) |
| 📦 **Workspaces** | Native monorepo support (multiple packages, one lockfile) |
| 🔒 **Lockfiles** | Deterministic `uv.lock` for reproducible builds |
| 🐍 **Python Management** | Can install/manage Python versions itself |
| 🔄 **Drop-in Compatible** | Works with existing `pyproject.toml` and `requirements.txt` |

### Official Resources

- 📖 Documentation: https://docs.astral.sh/uv/
- 🐙 GitHub: https://github.com/astral-sh/uv
- 📝 Changelog: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md

---

## 🧠 Core Concepts for Beginners

### 1. `pyproject.toml` — The Project Manifest

This is **the** configuration file for modern Python projects. It replaces `setup.py`, `setup.cfg`, `requirements.txt`, and more.

```toml
# pyproject.toml - Minimal example
[project]
name = "my-package"
version = "0.1.0"
description = "A sample Python package"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Key Sections:**

| Section | Purpose |
|---------|---------|
| `[project]` | Package metadata (name, version, dependencies) |
| `[project.optional-dependencies]` | Extra deps for dev/test/docs |
| `[build-system]` | How to build the package |
| `[tool.uv]` | UV-specific configuration |

### 2. `uv.lock` — The Lockfile

A **lockfile** captures the exact versions of every dependency (including transitive ones) that were resolved at a specific time.

```
# uv.lock (auto-generated, don't edit manually)
version = 1
requires-python = ">=3.10"

[[package]]
name = "requests"
version = "2.31.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "certifi" },
    { name = "charset-normalizer" },
    ...
]
```

**Why Lockfiles Matter:**

| Without Lockfile | With Lockfile |
|-----------------|---------------|
| `requests>=2.28` could install 2.28, 2.29, 2.31... | Always installs exactly 2.31.0 |
| Different machines get different versions | Every machine gets identical deps |
| "Works on my machine" bugs | Reproducible environments |

### 3. Workspaces — Monorepo Support

A **workspace** lets you manage multiple related packages in a single repository with a shared lockfile and virtual environment.

```toml
# Root pyproject.toml
[tool.uv.workspace]
members = [
    "cores/*",      # All packages in cores/ folder
    "utils/*",      # All packages in utils/ folder
]
```

**Workspace Benefits:**

- 🔒 **Single lockfile** — All packages share `uv.lock` at the root
- 📁 **Single venv** — One `.venv/` for the whole workspace
- 🔗 **Cross-references** — Packages can depend on each other
- ⚡ **Fast syncing** — Only changed packages are rebuilt

### 4. Virtual Environments (Auto-Managed)

UV automatically creates and manages a `.venv/` folder. You rarely need to think about it.

```bash
# Old way (manual)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# UV way (automatic)
uv sync  # Creates .venv if missing, installs everything
```

---

## 🛠️ Key Commands Reference

### Project Initialization

```bash
# Create a new Python project
uv init my-project

# Creates:
# my-project/
# ├── pyproject.toml
# ├── README.md
# └── src/
#     └── my_project/
#         └── __init__.py
```

### Dependency Management

```bash
# Add a runtime dependency
uv add requests
uv add "pydantic>=2.0"

# Add a dev dependency
uv add --dev pytest ruff

# Remove a dependency
uv remove requests

# Add a local/workspace package dependency
uv add --editable ./cores/logger_util
```

### Installing & Syncing

```bash
# Install all dependencies (creates .venv if needed)
uv sync

# Install including dev dependencies
uv sync --extra dev

# Install only production dependencies
uv sync --no-dev

# Update lockfile without installing
uv lock
```

### Running Code

```bash
# Run a Python script with correct environment
uv run python my_script.py

# Run a module
uv run python -m pytest

# Run a package entry point (if defined)
uv run my-cli-command
```

### Python Version Management

```bash
# List available Python versions
uv python list

# Install a specific Python version
uv python install 3.12

# Pin Python version for project
uv python pin 3.11
```

### Command Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `uv init` | Create new project | `uv init my-app` |
| `uv add` | Add dependency | `uv add requests` |
| `uv remove` | Remove dependency | `uv remove requests` |
| `uv sync` | Install all deps | `uv sync --extra dev` |
| `uv lock` | Update lockfile | `uv lock` |
| `uv run` | Run with env | `uv run pytest` |
| `uv pip` | pip compatibility | `uv pip install -r req.txt` |

---

## � Package Sources

UV can install packages from multiple sources. Understanding these is key for monorepo setups.

### PyPI (Default)

Standard packages from the Python Package Index:

```toml
[project]
dependencies = [
    "requests>=2.28",     # Latest compatible
    "pydantic==2.5.0",    # Exact version
    "numpy>=1.24,<2.0",   # Version range
]
```

### Workspace Members (Local Packages)

Sibling packages within the same monorepo are automatically available:

```toml
# Root pyproject.toml - define workspace members
[tool.uv.workspace]
members = ["cores/*", "utils/*", "managers/*"]

# In a module's pyproject.toml - depend on sibling
[project]
name = "config-core"
dependencies = [
    "logger-util",  # Another workspace member (by package name)
]
```

> 💡 **Key insight**: Workspace members use their **package name** (from `[project].name`), not folder name.

### Git Repository Packages

Install directly from Git repositories:

```toml
[project]
dependencies = [
    # GitHub (HTTPS) - latest default branch
    "package-name @ git+https://github.com/owner/repo.git",
    
    # Specific tag/branch/commit
    "package-name @ git+https://github.com/owner/repo.git@v1.0.0",
    "package-name @ git+https://github.com/owner/repo.git@main",
    "package-name @ git+https://github.com/owner/repo.git@abc123def",
    
    # Subdirectory within repository
    "package-name @ git+https://github.com/owner/repo.git#subdirectory=packages/pkg",
]
```

**Cleaner syntax with UV sources:**

```toml
[tool.uv.sources]
my-package = { git = "https://github.com/owner/repo.git", tag = "v1.0.0" }
dev-tool = { git = "https://github.com/owner/tool.git", branch = "main" }
```

### Local Path Dependencies

Packages outside the workspace (useful for development):

```toml
[project]
dependencies = [
    "local-pkg @ file:///absolute/path/to/package",
]

# Recommended: Use sources for cleaner syntax + editable mode
[tool.uv.sources]
local-pkg = { path = "../external-package", editable = true }
```

### Package Sources Summary

| Source | Syntax Example | Use Case |
|--------|---------------|----------|
| PyPI | `"requests>=2.28"` | Public packages |
| Workspace | `"logger-util"` | Sibling packages in monorepo |
| Git (HTTPS) | `"pkg @ git+https://..."` | Private repos, forks |
| Git (tag) | `"pkg @ git+...@v1.0.0"` | Pinned releases |
| Git (branch) | `{ git = "...", branch = "main" }` | Tracking development |
| Local path | `{ path = "...", editable = true }` | External local development |

---

## �📂 File Structure Explanation

UV supports two package layouts: **flat** (recommended for ADHD Framework) and **src** layout.

### Flat Layout (Primary — ADHD Framework Style)

Code lives directly in the package folder, no `src/` intermediary:

```
logger_util/
├── pyproject.toml      # Project manifest
├── __init__.py         # Package entry point (code here directly)
├── logger.py           # Module files at root level
├── handlers.py
├── init.yaml           # ADHD module config
└── README.md
```

**Required `pyproject.toml` for flat layout:**

```toml
[project]
name = "logger-util"    # Package name (use hyphens)
version = "0.1.0"
requires-python = ">=3.10"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# IMPORTANT: Tell hatch where to find the package
[tool.hatch.build.targets.wheel]
packages = ["."]   # Current directory IS the package
```

> 💡 **Why flat?** Matches current ADHD structure, simpler navigation, less nesting.

### Src Layout (Alternative)

Code lives in a `src/<package_name>/` subdirectory:

```
my-package/
├── pyproject.toml
├── README.md
└── src/
    └── my_package/     # Note: underscores for Python module name
        ├── __init__.py
        └── main.py
```

**When to use src layout:**
- Publishing to PyPI (isolates installed vs development code)
- Large packages with many submodules
- Strict testing requirements (ensures tests import the *installed* package)

### Workspace (Monorepo) — Flat Layout

```
project_root/
├── pyproject.toml      # Root workspace config
├── uv.lock             # Single lockfile for ALL packages
├── .venv/              # Shared virtual environment
├── README.md
│
├── cores/
│   ├── logger_util/
│   │   ├── pyproject.toml   # name = "logger-util"
│   │   ├── __init__.py      # Code here directly (flat)
│   │   ├── logger.py
│   │   └── README.md
│   │
│   └── config_core/
│       ├── pyproject.toml   # name = "config-core"
│       ├── __init__.py
│       └── config.py
│
└── utils/
    └── string_utils/
        ├── pyproject.toml
        ├── __init__.py
        └── helpers.py
```

### Key Files Explained

| File | Location | Purpose |
|------|----------|---------|
| `pyproject.toml` | Root | Defines workspace members, shared config |
| `pyproject.toml` | Each module | Module's name, version, dependencies |
| `uv.lock` | Root only | Exact versions for entire workspace |
| `.venv/` | Root only | Shared virtual environment |
| `__init__.py` | Each module root | Package entry (flat layout) |

---

## 🔗 How This Applies to ADHD Framework

The ADHD Framework is migrating from a custom path-hack system to proper `uv` workspaces.

### Before UV (Current Pain)

```python
# Every file needs this ugly hack to import modules
import sys
sys.path.insert(0, "/path/to/adhd_framework/cores")
sys.path.insert(0, "/path/to/adhd_framework/utils")

from logger_util import Logger  # Only works after path hacks
```

### After UV (The Goal)

```python
# Clean imports, no hacks needed
from logger_util import Logger  # Just works™
from config_core import ConfigManager
```

### ADHD Workspace Structure (Target)

```
adhd_framework_v3/
├── pyproject.toml           # Workspace root
├── uv.lock                  # All deps locked
├── .venv/                   # One environment
│
├── cores/
│   ├── logger_util/
│   │   ├── pyproject.toml   # name = "logger-util"
│   │   ├── __init__.py      # Flat layout - code here directly
│   │   ├── logger.py
│   │   ├── init.yaml        # ADHD module config
│   │   └── README.md
│   │
│   ├── config_core/
│   │   ├── pyproject.toml   # name = "config-core"
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── init.yaml
│   │
│   └── ... (20+ cores)
│
├── utils/
│   └── ...
│
├── managers/
│   └── ...
│
└── plugins/
    └── ...
```

### What Changes for Developers

| Task | Before | After |
|------|--------|-------|
| Install deps | `pip install -r requirements.txt` | `uv sync` |
| Add new dep | Edit requirements.txt, pip install | `uv add package` |
| Run script | Ensure path hacks are in place | `uv run python script.py` |
| Import module | Add sys.path hack first | Just import it |

---

## 📚 Further Reading

- [UV Documentation](https://docs.astral.sh/uv/) — Official docs
- [UV Workspaces Guide](https://docs.astral.sh/uv/concepts/workspaces/) — Monorepo deep dive
- [Migrating from pip](https://docs.astral.sh/uv/pip/compatibility/) — Compatibility guide
- [pyproject.toml Specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/) — Official spec

---

## ✅ Quick Start Checklist

For developers joining an existing UV workspace:

- [ ] Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Clone the repository
- [ ] Run `uv sync` in the project root
- [ ] Use `uv run python <script>` to run code
- [ ] Use `uv add <package>` to add dependencies

---

*This primer is part of the [UV Migration Blueprint](./00_index.md). See [03_feature_core_migration.md](./03_feature_core_migration.md) for the ADHD-specific migration plan.*
