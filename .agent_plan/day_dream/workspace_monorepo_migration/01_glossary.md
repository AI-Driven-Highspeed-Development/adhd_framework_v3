# 01 - Glossary: Python Packaging Fundamentals

> Part of [Workspace Monorepo Migration Blueprint](./00_index.md)
>
> **Audience:** Developers unfamiliar with modern Python packaging, uv, or PyPI

---

## 📖 The Story

### 😤 The Pain

```
┌─────────────────────────────────────────────────────────────────┐
│  "What's the difference between pip and uv?"                    │
│  "What does PyPI even stand for?"                               │
│  "Editable install? Workspace? Distribution? 😵"                │
│                                                                 │
│  Modern Python packaging has dozens of overlapping concepts     │
│  and tools. Without clear definitions, discussions get muddy.   │
└─────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| New Python developers | 🔥🔥🔥 High | Every project |
| Experienced devs from other languages | 🔥🔥 Medium | Learning curve |

### ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  📚 GLOSSARY                                                    │
│  ────────────                                                   │
│  • Clear definitions for every term                             │
│  • Analogies to familiar concepts                               │
│  • Quick reference during discussions                           │
│                                                                 │
│  "Ah, so PyPI is like npm for Python!" ✅                       │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> A comprehensive glossary of Python packaging terms so everyone speaks the same language.

---

## 🔧 The Spec

---

## 🐍 Package Managers

### pip

**What:** The original Python package installer, bundled with Python since 3.4.

**Analogy:** Like `npm install` for Python (but slower and simpler).

**Key Facts:**
- Reads `requirements.txt` or `pyproject.toml`
- Downloads from PyPI by default
- No lockfile (non-deterministic installs)
- No workspace support

**Common Commands:**
```bash
pip install requests            # Install a package
pip install -r requirements.txt # Install from file
pip install -e .                # Editable install (development)
pip freeze > requirements.txt   # Export installed versions
```

---

### uv (⭐ RECOMMENDED)

**What:** A blazing-fast Python package manager written in Rust, by [Astral](https://astral.sh/).

**Analogy:** Like `pnpm` or `bun` for Python — same job as pip, 10-100x faster.

**Key Facts:**
- 10-100x faster than pip (parallel downloads, cached resolution)
- Native **workspace support** (monorepo-friendly)
- Generates `uv.lock` lockfile (deterministic)
- Can manage Python versions itself
- Drop-in compatible with pip commands (`uv pip install`)

**Common Commands:**
```bash
uv sync                  # Install all deps (creates .venv if needed)
uv add requests          # Add a dependency
uv add --dev pytest      # Add dev dependency
uv lock                  # Update lockfile
uv run python script.py  # Run with correct environment
```

**Official Docs:** https://docs.astral.sh/uv/

---

### poetry

**What:** A dependency management and packaging tool with its own lockfile format.

**Analogy:** Like npm (before pnpm) — full featured but slower than modern alternatives.

**Key Facts:**
- Uses `pyproject.toml` + `poetry.lock`
- Good dependency resolution
- Slower than uv
- No native workspace support (plugins exist)

**Why Not poetry for ADHD?:** uv is faster, has native workspaces, and is actively developed by Astral (ruff team).

---

### pdm

**What:** A modern Python package manager with PEP 582 support.

**Similar to:** poetry but with better standards compliance.

**Why Not pdm for ADHD?:** uv has better workspace support and is faster.

---

## 📦 Package Concepts

### Package

**What:** A directory containing Python code with an `__init__.py` file.

**Structure:**
```
my_package/
├── __init__.py     # Makes it a package
├── module1.py
└── module2.py
```

**Usage:**
```python
from my_package import something
from my_package.module1 import function
```

---

### Module

**What:** A single `.py` file OR a package (directory with `__init__.py`).

**Confusingly:** Python uses "module" for both files and packages. In ADHD, we use "module" to mean a self-contained package like `logger_util`.

---

### Distribution (dist)

**What:** A packaged format of your code ready for installation.

**Types:**
| Format | Extension | Description |
|--------|-----------|-------------|
| **Wheel** | `.whl` | Pre-built, fast to install (preferred) |
| **Source** | `.tar.gz` | Raw source, needs build step |

**Building Distributions:**
```bash
uv build              # Creates dist/ folder with .whl and .tar.gz
python -m build       # Alternative using build tool
```

---

### Editable Install

**What:** Installing a package so changes to source code take effect immediately, without reinstalling.

**Analogy:** Like `npm link` — symlinks instead of copies.

**How:**
```bash
pip install -e .           # Old way
uv sync                    # uv does this automatically for workspace members
```

**Why It Matters:** During development, you want code changes to reflect immediately. Editable installs make this happen.

---

### Virtual Environment (.venv)

**What:** An isolated Python installation for your project.

**Analogy:** Like `node_modules` but for Python — each project has its own dependencies.

**Why:**
```
Without venv:                    With venv:
┌─────────────────────────┐      ┌─────────────────────────┐
│ System Python           │      │ Project A (.venv)       │
│ requests 2.28           │      │ requests 2.31           │
│ numpy 1.24              │      └─────────────────────────┘
│                         │      ┌─────────────────────────┐
│ 💥 Version conflicts!   │      │ Project B (.venv)       │
└─────────────────────────┘      │ requests 2.28           │
                                 └─────────────────────────┘
                                 ✅ Isolated, no conflicts
```

**With uv:** Auto-managed. `uv sync` creates `.venv/` if missing.

---

### Lockfile (uv.lock)

**What:** A file listing the EXACT versions of every dependency (including transitive ones).

**Analogy:** Like `package-lock.json` or `pnpm-lock.yaml`.

**Without Lockfile:**
```
pyproject.toml says: requests>=2.28
Machine A installs: requests 2.28.0
Machine B installs: requests 2.31.0
→ "Works on my machine" bugs 😭
```

**With Lockfile:**
```
uv.lock says: requests==2.31.0 (exact hash)
Machine A installs: requests 2.31.0
Machine B installs: requests 2.31.0
→ Reproducible builds ✅
```

---

## 🌐 PyPI (Python Package Index)

### What is PyPI?

**Full Name:** Python Package Index

**URL:** https://pypi.org/

**Analogy:** Like npmjs.com for Python — THE central repository of Python packages.

**Key Facts:**
- 500,000+ packages
- Free to use and publish
- **PUBLIC ONLY** — no private packages on pypi.org
- Owned by Python Software Foundation

---

### TestPyPI

**What:** A separate PyPI instance for testing package uploads.

**URL:** https://test.pypi.org/

**Use Case:** Test your package publishing workflow before pushing to real PyPI.

```bash
uv publish --repository testpypi  # Upload to test
pip install --index-url https://test.pypi.org/simple/ my-package  # Install from test
```

---

### Package Index

**What:** A server that hosts Python packages for installation.

**Examples:**
| Index | URL | Type |
|-------|-----|------|
| PyPI | pypi.org | Public, default |
| TestPyPI | test.pypi.org | Public, testing |
| Private PyPI | your-server.com | Self-hosted |
| GitHub Packages | pkg.github.com | Private, GitHub-hosted |

---

## 🏗️ Workspace Concepts

### Workspace (uv)

**What:** A collection of related packages in one repository sharing a single lockfile and virtual environment.

**Analogy:** Like npm workspaces, Cargo workspaces (Rust), or Lerna monorepos.

**Configuration:**
```toml
# Root pyproject.toml
[tool.uv.workspace]
members = [
    "modules/*",     # ADHD: Flat structure, all modules here
]
```

> **Note:** Generic uv workspaces can use any folder structure. ADHD uses a flat `modules/` folder.

**Benefits:**
| Aspect | Without Workspace | With Workspace |
|--------|-------------------|----------------|
| Lockfiles | N lockfiles (one per package) | 1 lockfile (root) |
| Virtual envs | N .venv folders | 1 .venv (root) |
| Cross-package imports | Publish & install | Just import |
| Atomic commits | Split across repos | Single commit |

---

### Monorepo

**What:** A single repository containing multiple packages/projects.

**Opposite:** Polyrepo — one repository per package.

**ADHD Context:**
```
BEFORE (Polyrepo):                    AFTER (Monorepo):
┌─────────────────────┐               ┌─────────────────────────────┐
│ github.com/org/     │               │ adhd_framework_v3/          │
│   logger_util       │               │   modules/                  │
│   config_manager    │               │     logger_util/            │
│   exceptions_core   │               │     config_manager/         │
│   ... (20+ repos)   │               │     exceptions_core/        │
│                     │               │     adhd_mcp/               │
│ 💥 Repo sprawl!     │               │     ... (flat structure)    │
└─────────────────────┘               │                             │
                                      │ ✅ All in one place         │
                                      └─────────────────────────────┘
```

---

### Workspace Member

**What:** A package that is part of a workspace.

**In pyproject.toml:**
```toml
[tool.uv.workspace]
members = ["modules/*"]  # Everything in modules/ is a member (ADHD)
```

**Key Behavior:** Workspace members can depend on each other by package name without publishing.

---

## 📤 Publishing Concepts

### Publishing / Uploading

**What:** Making your package available for others to install via a package index.

**Process:**
```
Source Code → Build → Distribution (.whl) → Upload → Package Index
```

**Commands:**
```bash
uv build      # Create dist/
uv publish    # Upload to PyPI (needs API token)
```

---

### Version (Semantic)

**What:** A number indicating the package release, following semver convention.

**Format:** `MAJOR.MINOR.PATCH` (e.g., `2.31.0`)

| Part | When to Increment |
|------|-------------------|
| MAJOR | Breaking changes |
| MINOR | New features (backwards compatible) |
| PATCH | Bug fixes |

**In pyproject.toml:**
```toml
[project]
version = "0.1.0"
```

---

### Release

**What:** A specific published version of a package.

**PyPI Shows:**
- Package: `requests`
- Releases: 2.28.0, 2.29.0, 2.30.0, 2.31.0, ...

---

## 🔗 Dependency Concepts

### Dependency

**What:** A package your code needs to run.

**In pyproject.toml:**
```toml
[project]
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0,<3.0",
]
```

---

### Transitive Dependency

**What:** A dependency of your dependency.

**Example:**
```
Your package → requests → urllib3 → ...
                 ↑             ↑
           direct dep    transitive dep
```

**Lockfiles track:** Both direct AND transitive dependencies.

---

### Version Specifier

**What:** Rules for which versions of a dependency are acceptable.

| Specifier | Meaning | Example |
|-----------|---------|---------|
| `>=2.0` | Minimum version | Any 2.x or higher |
| `<3.0` | Maximum version | Anything below 3.0 |
| `>=2.0,<3.0` | Range | 2.x only |
| `==2.31.0` | Exact | Only this version |
| `~=2.31` | Compatible | 2.31.x (patch updates OK) |

---

### Optional Dependencies / Extras

**What:** Dependencies only installed when explicitly requested.

**In pyproject.toml:**
```toml
[project.optional-dependencies]
dev = ["pytest", "ruff"]
docs = ["sphinx", "myst-parser"]
```

**Installation:**
```bash
uv sync --extra dev   # Install with dev extras
pip install .[dev]    # pip syntax
```

---

## 📚 Quick Reference Card

| Term | One-Line Definition |
|------|---------------------|
| **pip** | Original Python installer, bundled with Python |
| **uv** | Fast, modern pip replacement with workspaces |
| **PyPI** | Python Package Index (npmjs.com for Python) |
| **Package** | Directory with `__init__.py` |
| **Distribution** | Built package ready for install (.whl) |
| **Wheel** | Pre-built distribution format (.whl) |
| **Editable Install** | Install that reflects source changes immediately |
| **Virtual Environment** | Isolated Python for one project |
| **Lockfile** | Exact versions of all dependencies |
| **Workspace** | Multiple packages, one lockfile |
| **Monorepo** | One repo, multiple packages |

---

**← Back to:** [Blueprint Index](./00_index.md) | **Next:** [Architecture](./02_architecture.md)
