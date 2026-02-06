# 03 - Research: UV Workspaces Deep Dive

> Part of [Workspace Monorepo Migration Blueprint](./00_index.md)
>
> **Status:** ⏳ [TODO] | **Difficulty:** `[KNOWN]`

---

## 📖 The Story

### 😤 The Pain

```
┌─────────────────────────────────────────────────────────────────┐
│  "What exactly IS a uv workspace?"                              │
│  "How does workspace = true differ from regular deps?"          │
│  "What commands do I need to know?"                             │
│                                                                 │
│  Without understanding uv workspaces, the migration is          │
│  a black box of copy-pasted commands.                           │
└─────────────────────────────────────────────────────────────────┘
```

### ✨ The Vision

> Deep understanding of uv workspace mechanics enables confident migration decisions.

---

## 🔧 The Spec

---

## 🎯 What is a UV Workspace?

A **uv workspace** is a way to manage multiple related Python packages in a single repository with:

- **One lockfile** (`uv.lock`) for all packages
- **One virtual environment** (`.venv/`) shared by all
- **Cross-package dependencies** resolved locally (no publishing needed)
- **Atomic operations** — `uv sync` handles everything

### Mental Model

```
Traditional (per-package):           UV Workspace:
┌─────────────────────────┐         ┌─────────────────────────────────┐
│ package-a/              │         │ workspace/                      │
│   pyproject.toml        │         │   pyproject.toml  (root)        │
│   uv.lock               │         │   uv.lock         (ONE!)        │
│   .venv/                │         │   .venv/          (ONE!)        │
├─────────────────────────┤         │                                 │
│ package-b/              │         │   packages/                     │
│   pyproject.toml        │         │     package-a/                  │
│   uv.lock               │         │       pyproject.toml            │
│   .venv/                │         │     package-b/                  │
├─────────────────────────┤         │       pyproject.toml            │
│ package-c/              │         │     package-c/                  │
│   pyproject.toml        │         │       pyproject.toml            │
│   uv.lock               │         │                                 │
│   .venv/                │         │                                 │
└─────────────────────────┘         └─────────────────────────────────┘
     3 lockfiles                           1 lockfile
     3 environments                        1 environment
     Manual coordination                   Automatic coordination
```

### Analogy to Other Tools

| Tool | Workspace Equivalent |
|------|----------------------|
| **npm/pnpm** | npm workspaces / pnpm workspaces |
| **Rust/Cargo** | Cargo workspaces |
| **Go** | Go modules with replace directives |
| **Java/Gradle** | Multi-project builds |

---

## ⚙️ How Workspaces Work

### Configuration

The root `pyproject.toml` declares workspace members:

```toml
# workspace_root/pyproject.toml

[tool.uv.workspace]
members = [
    "packages/*",        # Glob pattern: all subdirs of packages/
    "libs/my-lib",       # Specific path
]

# Optional: exclude patterns
exclude = [
    "packages/legacy-*", # Exclude legacy packages
]
```

### Member Detection

When you run `uv sync`:

1. UV reads root `pyproject.toml`
2. Expands `members` globs to find all `pyproject.toml` files
3. Each found `pyproject.toml` = one workspace member
4. Collects ALL dependencies from ALL members
5. Resolves them together into ONE `uv.lock`
6. Installs everything into ONE `.venv/`

### Workspace Members as Dependencies

Within a workspace, members can depend on each other **by package name**:

```toml
# packages/package-b/pyproject.toml
[project]
name = "package-b"
dependencies = [
    "package-a",  # Just the name! Not a path, not a git URL
]
```

UV knows `package-a` is a workspace member and installs it as an **editable install**.

---

## 🛠️ Essential UV Commands

### Setup & Installation

| Command | Purpose |
|---------|---------|
| `uv sync` | Install all dependencies (creates .venv if needed) |
| `uv sync --extra dev` | Install with dev dependencies |
| `uv sync --frozen` | Install from lockfile, don't update it |
| `uv lock` | Update lockfile without installing |

### Dependency Management

| Command | Purpose |
|---------|---------|
| `uv add <package>` | Add dependency (to CWD's pyproject.toml) |
| `uv add --dev <package>` | Add as dev dependency |
| `uv add <package> --package <member>` | Add to specific workspace member |
| `uv remove <package>` | Remove dependency |

### Running Code

| Command | Purpose |
|---------|---------|
| `uv run python script.py` | Run with correct environment |
| `uv run pytest` | Run pytest with correct environment |
| `uv run -m module` | Run a module |

### Workspace Info

| Command | Purpose |
|---------|---------|
| `uv tree` | Show dependency tree |
| `uv pip list` | List installed packages |
| `uv pip show <package>` | Show package info |

---

## 🔍 Key Concepts Deep Dive

### 1. `workspace = true` in Sources

When a package is a workspace member, UV automatically resolves it from the workspace. You can make this explicit:

```toml
# In a member's pyproject.toml
[project]
dependencies = ["logger-util"]

[tool.uv.sources]
logger-util = { workspace = true }  # Explicit: find in workspace
```

**But this is usually implicit!** UV figures it out automatically when the package name matches a workspace member.

### 2. Editable Installs

Workspace members are automatically installed in **editable mode**:

```
.venv/lib/python3.11/site-packages/
├── requests/              ← Regular package (copied)
├── pydantic/              ← Regular package (copied)
└── logger_util.egg-link   ← Editable! Points to source
```

This means:
- Changes to `logger_util` source files are **immediately visible**
- No need to reinstall after code changes
- `uv sync` is only needed after dependency changes

### 3. Resolution Strategy

UV resolves ALL workspace dependencies together:

```
Workspace has:
  - package-a requires: requests>=2.28
  - package-b requires: requests>=2.30
  - package-c requires: requests<2.32

UV Resolution:
  → requests==2.31.0 (satisfies ALL constraints)
  → One version in .venv for ALL packages
```

This prevents version conflicts within the workspace.

### 4. Root Package vs Workspace

The root `pyproject.toml` can be:

**Option A: Workspace-only (no package)**
```toml
# Just workspace config, no [project]
[tool.uv.workspace]
members = ["packages/*"]
```

**Option B: Workspace + Root Package**
```toml
[project]
name = "my-framework"
version = "1.0.0"

[tool.uv.workspace]
members = ["packages/*"]
```

ADHD uses Option B — the root is also a package (`adhd-framework`).

---

## 📋 Workspace Patterns

### Pattern 1: Flat Members

```
workspace/
├── pyproject.toml
├── package-a/
│   └── pyproject.toml
├── package-b/
│   └── pyproject.toml
└── package-c/
    └── pyproject.toml
```

Config:
```toml
[tool.uv.workspace]
members = ["package-*"]
```

### Pattern 2: Categorized Members (ADHD Style)

```
workspace/
├── pyproject.toml
├── cores/
│   ├── core-a/
│   └── core-b/
├── utils/
│   └── util-a/
└── plugins/
    └── plugin-a/
```

Config:
```toml
[tool.uv.workspace]
members = [
    "cores/*",
    "utils/*",
    "plugins/*",
]
```

### Pattern 3: Nested Packages

```
workspace/
├── pyproject.toml
└── packages/
    └── nested/
        └── deep/
            └── package/
                └── pyproject.toml
```

Config:
```toml
[tool.uv.workspace]
members = ["packages/**"]  # Double star for recursive
```

---

## ⚠️ Common Gotchas

### 1. Package Name vs Folder Name

```
Folder: cores/logger_util/    (underscores)
Package: logger-util          (hyphens in pyproject.toml)
Import: from logger_util      (underscores in Python)
```

**Rule:** Dependencies use the **package name** from `[project].name`.

### 2. Circular Dependencies

Workspace doesn't prevent cycles:
```
package-a depends on package-b
package-b depends on package-a
→ 💥 Import error at runtime
```

**Solution:** Design dependency graph as a DAG.

### 3. Missing Member

If a folder matches the glob but has no `pyproject.toml`:
```
cores/
├── logger_util/pyproject.toml  ← Member
└── empty_folder/               ← Ignored (no pyproject.toml)
```

UV silently ignores folders without `pyproject.toml`.

### 4. Running from Subdirectory

```bash
cd cores/logger_util/
uv sync  # ❌ Error: not a workspace
```

**Always run from workspace root:**
```bash
cd workspace/
uv sync  # ✅ Works
```

---

## 🔗 Official Documentation

- **UV Workspaces Guide:** https://docs.astral.sh/uv/concepts/workspaces/
- **UV Configuration Reference:** https://docs.astral.sh/uv/reference/settings/
- **UV CLI Reference:** https://docs.astral.sh/uv/reference/cli/

---

## 📊 ADHD Framework Application

### Current State

The ADHD Framework **already has** a uv workspace configured:

```toml
# adhd_framework_v3/pyproject.toml (current)
[tool.uv.workspace]
members = [
    "cores/*",
    "managers/*",
    "utils/*",
    "plugins/*",
    "mcps/*",
]
```

### What's Missing

1. **Module dependencies** may still reference git URLs instead of workspace names
2. **CI** may not be consolidated
3. **Documentation** of workspace workflows

### Migration Focus

The migration is less about "setting up" a workspace (already done) and more about:
- Ensuring all inter-module dependencies use workspace resolution
- Consolidating tooling to be workspace-aware
- Documentation for contributors

---

**← Back to:** [Blueprint Index](./00_index.md) | **Next:** [Research: PyPI Distribution](./04_research_pypi_distribution.md)
