# 07 - Feature: CLI Entry Points

> Part of [Framework Modernization Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current CLI Setup:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  HOW USERS RUN THE CLI TODAY:                                              │
│                                                                            │
│  ./adhd_framework.py new-project      ← DIRECT SCRIPT EXECUTION            │
│  python adhd_framework.py new-project ← PYTHON INVOCATION                  │
│                                                                            │
│  PROBLEMS:                                                                 │
│  ┌────────────────────────────────────────┐                                │
│  │ 1. Requires being in project root      │                                │
│  │ 2. Requires correct Python in PATH     │                                │
│  │ 3. No standard installation path       │                                │
│  │ 4. Tab completion requires venv hack   │                                │
│  │ 5. Not pip-installable                 │                                │
│  └────────────────────────────────────────┘                                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Developer | 🔥🔥 Medium | Every CLI invocation |
| New user | 🔥🔥🔥 High | First-time setup confusion |

### ✨ The Vision

```
After Modernization:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  HOW USERS RUN THE CLI:                                                    │
│                                                                            │
│  adhd new-project                     ← CLEAN COMMAND NAME                 │
│  uv run adhd new-project              ← UV-AWARE INVOCATION                │
│                                                                            │
│  HOW IT WORKS:                                                             │
│  ┌────────────────────────────────────────┐                                │
│  │ pyproject.toml:                        │                                │
│  │   [project.scripts]                    │                                │
│  │   adhd = "adhd_framework:main"         │  ← STANDARD ENTRY POINT        │
│  └────────────────────────────────────────┘                                │
│                                                                            │
│  BENEFITS:                                                                 │
│  ┌────────────────────────────────────────┐                                │
│  │ 1. Works from any directory            │                                │
│  │ 2. UV handles Python selection         │                                │
│  │ 3. Standard pip-installable            │                                │
│  │ 4. Tab completion via standard tools   │                                │
│  │ 5. Discoverable in PATH                │                                │
│  └────────────────────────────────────────┘                                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> CLI exposed via pyproject.toml entry points, making `adhd` a proper installable command.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Invocation | ❌ `./adhd_framework.py` | ✅ `adhd` or `uv run adhd` |
| Installation | ❌ Manual file copy | ✅ `uv sync` installs command |
| Directory constraint | ❌ Must be in project root | ✅ Works anywhere |
| Tab completion | ❌ Venv hack required | ✅ Standard shell integration |

---

## 🔧 The Spec

---

## 🎯 Overview

Configure CLI as proper Python entry point:

1. **Add `[project.scripts]`** to root pyproject.toml
2. **Refactor adhd_framework.py** to be importable module
3. **Remove bootstrap code** that's no longer needed
4. **Document invocation patterns** for UV workflow

**Priority:** P1  
**Difficulty:** `[KNOWN]`

---

## 📚 Prior Art

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| PEP 621 entry points | Standard | High | ✅ Adopt |
| UV `uv run` | Tool | High | ✅ Adopt |
| Click/Typer | Library | Medium | 🤔 Consider for future |

### Usage Decision

**Using:** PEP 621 `[project.scripts]` entry point  
**How:** Configure in pyproject.toml, refactor script to module  
**Why:** Standard Python packaging, works with UV

---

## 👥 User Stories

| As a... | I want to... | So that... |
|---------|--------------|------------|
| Developer | Run `adhd` from anywhere | I don't need to navigate to project root |
| Developer | Use `uv run adhd` | UV manages the environment |
| Developer | Have tab completion | CLI is discoverable |

---

## ✅ Acceptance Criteria

- [ ] `uv sync` installs `adhd` command
- [ ] `adhd --help` works after sync
- [ ] `uv run adhd` works
- [ ] Works from any directory within project
- [ ] Tab completion works with standard tools

---

## 📊 Configuration

### pyproject.toml Entry Point

```toml
[project]
name = "adhd-framework"
version = "3.0.0"
# ...

[project.scripts]
adhd = "adhd_framework:main"
```

### Module Structure

```
adhd_framework_v3/
├── pyproject.toml           # Defines entry point
├── adhd_framework.py        # Becomes adhd_framework/__init__.py OR stays as-is
│                            # with main() function exposed
└── ...
```

---

## 🛠️ Technical Notes

### Option A: Keep as Single File

```python
# adhd_framework.py
def main():
    """Entry point for CLI."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
    else:
        framework = ADHDFramework()
        framework.run(args)

if __name__ == "__main__":
    main()
```

```toml
# pyproject.toml
[project.scripts]
adhd = "adhd_framework:main"
```

### Option B: Convert to Package

```
adhd_framework/
├── __init__.py              # Exports main
├── cli.py                   # CLI logic
├── framework.py             # ADHDFramework class
└── ...
```

**Recommendation:** Option A (single file) is simpler and sufficient.

### Removing Bootstrap Code

**Current adhd_framework.py (~474 LOC):**
- Lines 1-120: Bootstrap logic (REMOVE)
- Lines 121-200: Tab completion hack (REMOVE)
- Lines 200-474: CLI logic (KEEP)

**Result:** ~200 LOC pure CLI code

### Invocation Patterns

```bash
# After `uv sync` installs the command:
adhd new-project            # Direct command
adhd create-module --type core

# With UV environment awareness:
uv run adhd new-project     # Ensures correct environment

# From any directory:
cd ~/somewhere
adhd --help                 # Still works (if in PATH)
```

---

## ⚠️ Edge Cases

| Scenario | Handling |
|----------|----------|
| Command run outside any project | Error with helpful message |
| Multiple ADHD projects installed | Use project-local `uv run adhd` |
| Global vs local installation | Document both patterns |

---

## ❌ Out of Scope

| Item | Rationale |
|------|-----------|
| Global CLI installation | Per-project is safer |
| Click/Typer migration | Argparse works fine |
| Shell plugin for tab completion | Standard tools sufficient |

---

## 🔗 Dependencies

| Depends On | For |
|------------|-----|
| Bootstrap removal | Clean entry point |
| pyproject.toml setup | Entry point configuration |

---

## 📋 Command Reference

### Complete Command Listing (Before/After Modernization)

| Command | Shorthand | Before (Current) | After (Modernized) | Status | Notes |
|---------|-----------|------------------|-------------------|--------|-------|
| `create-project` | `cp` | Interactive wizard, creates project structure with init.yaml | Interactive wizard, creates project with pyproject.toml | **KEEP** | Output format changes only |
| `create-module` | `cm` | Interactive wizard, creates module with init.yaml | Interactive wizard, creates module with pyproject.toml | **KEEP** | Output format changes only |
| `init` | `i` | Git clone missing modules + `pip install -r requirements.txt` | `uv sync` (handles deps + editable installs) | **MODIFY** | Simplified - UV handles everything |
| `refresh` | `r` | Run module refresh.py scripts (data/template sync) | Run module refresh.py scripts | **KEEP** | No change needed |
| `list` | `ls` | Read modules via init.yaml files | Read modules via pyproject.toml files | **MODIFY** | Source changes, output same |
| `info` | `in` | Read module details from init.yaml | Read module details from pyproject.toml | **MODIFY** | Source changes, output same |
| `req` | `rq` | `pip install -r requirements.txt` for all modules | N/A | **REMOVE** | `uv sync` replaces entirely |
| `workspace` | `ws` | Generate/update .code-workspace from module list | TBD - may simplify or remove | **SIMPLIFY** | Static file or optional |
| `update-framework` | `uf` | Fetch latest adhd_framework.py from repo | TBD - may integrate with `uv sync` | **MODIFY** | Consider removal if published |

### Command Details by Status

#### ✅ KEEP (No Significant Changes)

| Command | Current Behavior | Notes |
|---------|------------------|-------|
| `create-project` / `cp` | Interactive wizard prompts for project name, modules to include, creates directory structure | Template output changes (pyproject.toml instead of init.yaml) but user experience unchanged |
| `create-module` / `cm` | Interactive wizard prompts for module type, name, creates module scaffold | Template output changes (pyproject.toml instead of init.yaml) but user experience unchanged |
| `refresh` / `r` | Executes `refresh.py` in each module to sync data/templates | Completely independent of dependency management - keeps working |

#### 🔄 MODIFY (Behavior Changes)

| Command | Before | After | Why |
|---------|--------|-------|-----|
| `init` / `i` | 1. Git clone missing modules from BOOTSTRAP_MODULES<br>2. Run `pip install -r requirements.txt` per module<br>3. Configure venv tab completion | 1. Run `uv sync`<br>(handles deps, editable installs, lockfile) | UV's `uv sync` replaces clone+install pattern; modules come via git submodules or workspace deps |
| `list` / `ls` | Scan for `init.yaml` files, parse module metadata | Scan for `pyproject.toml` files, read `[project]` and `[tool.adhd]` | Data source changes; output format stays the same |
| `info` / `in` | Read `init.yaml` for version, repo_url, requirements | Read `pyproject.toml` for same data | Data source changes; output format stays the same |
| `update-framework` / `uf` | Fetch `adhd_framework.py` from GitHub raw URL | Option A: Keep as-is (useful during development)<br>Option B: Remove if framework is pip-installable | If framework is a proper package, `uv sync --upgrade` handles updates |

#### ❌ REMOVE (Replaced by UV)

| Command | Current Behavior | Replacement | Migration Path |
|---------|------------------|-------------|----------------|
| `req` / `rq` | Walks all modules, runs `pip install -r requirements.txt` | `uv sync` | Users run `uv sync` directly; single command does everything |

**Why `req` is Removed:**
1. `uv sync` installs ALL dependencies from `uv.lock` in one atomic operation
2. No need to visit each module - workspace dependencies handle this
3. Faster and more reliable than sequential pip installs
4. Lockfile ensures reproducibility across machines

#### ⚡ SIMPLIFY (Reduced Scope)

| Command | Current Behavior | After | Rationale |
|---------|------------------|-------|-----------|
| `workspace` / `ws` | Dynamically generates `.code-workspace` from discovered modules with visibility toggles | Option A: Static `.code-workspace` committed to repo<br>Option B: Simplified generator without overrides | Dynamic generation adds complexity; most users don't change workspace structure often |

### New Commands (Potential Additions)

| Command | Shorthand | Purpose | Status | Priority |
|---------|-----------|---------|--------|----------|
| `migrate` | `mig` | Run uv_migrator_core to convert init.yaml → pyproject.toml | **Add in P1** | Required for transition |
| `sync` | `s` | Wrapper for `uv sync` with ADHD-specific pre/post hooks | **Consider** | P2 - only if hooks needed |
| `doctor` | `doc` | Validate project health (deps, structure, versions) | **Consider** | P2 - nice to have |

#### `migrate` Command Specification

```bash
# Migrate current project
adhd migrate

# Migrate specific module only  
adhd migrate --module config_manager

# Dry run (show what would change)
adhd migrate --dry-run
```

**Implementation:** Wraps existing `uv_migrator_core.UVMigrator` class.

### Command Invocation Changes

```bash
# === BEFORE (Current) ===
./adhd_framework.py init           # Script in project root
python adhd_framework.py list      # Explicit python invocation

# === AFTER (Modernized) ===
adhd init                          # Proper CLI command
uv run adhd list                   # UV-managed execution
```

### Argument Changes Summary

| Command | Removed Args | Modified Args | New Args |
|---------|--------------|---------------|----------|
| `init` | (none) | Behavior change only | `--skip-sync` (optional - just setup, no uv sync) |
| `list` | (none) | (none) | (none) |
| `info` | (none) | (none) | (none) |
| `refresh` | (none) | (none) | (none) |
| `workspace` | `--all`, `--ignore-overrides`, `--module` | Simplify to just regenerate | (none) |
| `update-framework` | `--dry-run` may become default | TBD | (none) |

### Migration Guide for Users

```bash
# === OLD WORKFLOW ===
./adhd_framework.py init          # Clone modules + install deps
./adhd_framework.py req           # Re-install all requirements
./adhd_framework.py workspace     # Regenerate workspace file

# === NEW WORKFLOW ===
uv sync                           # One command does everything
# OR
adhd init                         # Alias for uv sync (after entry point installed)

# workspace file is now static - edit manually or use:
adhd workspace                    # Optional: regenerate if needed
```

---

## [Custom] 🤔 Global vs Project-Local

**Question:** Should `adhd` be globally installable?

| Option | Pros | Cons |
|--------|------|------|
| Project-local only | Safer, version-matched | Need `uv run` or activate |
| Global install | Convenient | Version mismatches possible |

**Recommendation:** Project-local primary, with documentation for global if desired.

```bash
# Project-local (recommended)
cd my-project
uv run adhd new-module

# Global (optional, documented)
uv tool install adhd-framework
adhd new-module
```

---

**← Back to:** [06 - Feature: Refresh Modernization](./06_feature_refresh_modernization.md)  
**Next:** [08 - Feature: Template Updates](./08_feature_template_updates.md)
