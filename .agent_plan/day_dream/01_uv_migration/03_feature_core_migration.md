# 03 - Feature: Core Migration (P0)

> Part of [UV Migration Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
THE PATH HACK (copy-pasted 100+ times):
┌───────────────────────────────────────────────────────────────────┐
│  # Every. Single. Python. File.                                   │
│  import os, sys                                                   │
│  current_dir = os.path.dirname(os.path.abspath(__file__))         │
│  project_root = os.getcwd()  # 💥 BROKEN if run from other dir    │
│  sys.path.insert(0, project_root)                                 │
│                                                                   │
│  # Then we can finally import                                     │
│  from managers.config_manager import ConfigManager                │
└───────────────────────────────────────────────────────────────────┘

Why this exists:
┌───────────────────────────────────────────────────────────────────┐
│  $ cd managers/session_manager                                    │
│  $ python session_manager.py                                      │
│  ❌ ModuleNotFoundError: No module named 'managers'               │
│                                                                   │
│  Because: Python doesn't know "managers" is a package             │
│  Because: We're not using real Python packaging                   │
│  Because: Modules are just folders, not installed packages        │
└───────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Module developers | 🔥🔥🔥 High | Every new file |
| Anyone debugging | 🔥🔥🔥 High | "Why doesn't it work from this dir?" |
| New contributors | 🔥🔥🔥 High | Onboarding confusion |
| CI/CD pipelines | 🔥🔥 Medium | Non-standard setup |

### ✨ The Vision

```
After This Feature:
┌───────────────────────────────────────────────────────────────────┐
│  # managers/session_manager/session_manager.py                    │
│                                                                   │
│  # NO MORE PATH HACKS! Just normal imports:                       │
│  from config_manager import ConfigManager                         │
│  from logger_util import Logger                                   │
│  from exceptions_core import ADHDError                            │
│                                                                   │
│  # Why it works:                                                  │
│  # uv workspace + editable install = real Python packages         │
└───────────────────────────────────────────────────────────────────┘

Running modules standalone:
┌───────────────────────────────────────────────────────────────────┐
│  $ cd managers/session_manager                                    │
│  $ python -m session_manager                                      │
│  ✅ Works! Because session_manager is an installed package        │
│                                                                   │
│  $ cd /anywhere                                                   │
│  $ python -c "from session_manager import SessionManager"         │
│  ✅ Works! Package is in site-packages via editable install       │
└───────────────────────────────────────────────────────────────────┘

Standard onboarding:
┌───────────────────────────────────────────────────────────────────┐
│  $ git clone <repo>                                               │
│  $ cd repo                                                        │
│  $ uv sync                    ◀── All modules installed          │
│  ✅ Ready to develop                                              │
└───────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Eliminate all 100+ path hacks via uv workspaces and editable installs that make modules real packages.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| `sys.path.insert()` occurrences | ❌ 100+ files | ✅ 0 |
| Run module from any dir | ❌ Fails | ✅ Works (`python -m module`) |
| Import style | ❌ `from managers.x import` | ✅ `from x import` |
| Onboarding steps | ❌ Clone, bootstrap, wait | ✅ Clone, `uv sync` |

---

## 🔧 The Spec

---

## 🎯 Overview

**Two major transformations in one phase:**

1. **Create pyproject.toml for all modules**: Standard Python packaging
2. **Eliminate path hacks**: Editable installs make modules real packages

**Priority:** P0 (Foundation — do this first!)  
**Difficulty:** `[KNOWN]`  
**Duration:** 1-2 weeks

---

## 👥 User Stories

| As a... | I want to... | So that... |
|---------|--------------|------------|
| New contributor | Run `git clone && uv sync` | I'm ready to develop in 2 commands |
| Module developer | Run `python -m my_module` from anywhere | I can test without cd'ing to project root |
| Maintainer | Delete all `sys.path.insert()` hacks | Code is cleaner, no copy-paste boilerplate |
| Developer | Add a PyPI dependency | I edit pyproject.toml like any Python project |

---

## ✅ Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Every module has pyproject.toml | `find cores managers utils -name "pyproject.toml" \| wc -l` matches module count |
| 2 | Root pyproject.toml exists with workspace config | File exists at root, contains `[tool.uv.workspace]` |
| 3 | `uv sync` succeeds from clean clone | `rm -rf .venv && uv sync` exits 0 |
| 4 | **No `sys.path.insert()` in any module** | `grep -r "sys.path.insert" cores/ managers/ utils/` returns 0 |
| 5 | **Imports use package names, not folder paths** | No `from managers.x import`, only `from x import` |
| 6 | Module runs standalone | `cd managers/session_manager && python -m session_manager` works |
| 7 | Imports work from any directory | `cd /tmp && python -c "from config_manager import ConfigManager"` |

---

## 🛠️ Technical Notes

### Root pyproject.toml

```toml
[project]
name = "adhd-framework"
version = "3.0.0"
requires-python = ">=3.10"

[project.optional-dependencies]
dev = [
    "instruction-core",
    "module-creator-core",
    "project-creator-core",
    "questionary-core",
]

[tool.uv.workspace]
members = [
    "cores/*",
    "managers/*",
    "plugins/*",
    "mcps/*",
    "utils/*",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Per-Module pyproject.toml Template

```toml
[project]
name = "{package-name}"
version = "{version}"
requires-python = ">=3.10"

dependencies = [
    # ADHD modules (workspace deps)
    # PyPI packages
]

[project.urls]
Repository = "{repo_url}"

[tool.adhd]
type = "{core|manager|util|plugin|mcp}"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Import Path Migration Script (Illustrative)

```python
def migrate_file(file_path: Path) -> None:
    """Remove path hacks and update import paths"""
    content = file_path.read_text()
    
    # Remove the path hack block
    content = re.sub(
        r'import os.*?sys\.path\.insert\(0, project_root\)\n',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Update import paths
    # from managers.config_manager import X → from config_manager import X
    content = re.sub(
        r'from (managers|cores|utils|plugins|mcps)\.(\w+)',
        r'from \2',
        content
    )
    
    file_path.write_text(content)
```

---

## 📁 Target Folder Structure

```
pyproject.toml              (NEW - root workspace config)

cores/exceptions_core/
├── init.yaml               (UNCHANGED - will be deprecated later)
├── pyproject.toml          (NEW - package metadata)
├── __init__.py             (MODIFIED - remove sys.path.insert!)
└── adhd_exceptions.py

managers/session_manager/
├── init.yaml               (UNCHANGED)
├── pyproject.toml          (NEW)
├── __init__.py             (MODIFIED - remove sys.path.insert!)
└── session_manager.py      (MODIFIED - imports become: from config_manager import...)

utils/logger_util/
├── init.yaml               (UNCHANGED)
├── pyproject.toml          (NEW)
├── __init__.py             (MODIFIED)
└── logger_util.py

# ... same pattern for all modules
```

---

## ⚠️ Edge Cases

| Scenario | Handling |
|----------|----------|
| Module with no dependencies | Empty `dependencies = []` |
| Circular dependency between modules | uv detects and errors — must resolve |
| Module not in any folder pattern | Add explicit path to `members` |
| PyPI package name conflicts with local | Use explicit path dep syntax |
| `__init__.py` with path hack | Remove hack, keep re-exports |

---

## ❌ Out of Scope

| Excluded | Rationale |
|----------|-----------|
| Layer taxonomy field | Separate blueprint |
| init.yaml deprecation | Separate blueprint |
| CLI migration | Separate blueprint |
| Publishing to PyPI | Local path deps only |

---

## 🔗 Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| uv installed globally | External | User responsibility |
| Python ≥3.10 | External | Required by uv |
| init.yaml exists for each module | Internal | ✅ Current state |

---

## How to Verify (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `rm -rf .venv && uv sync` | All deps installed, no errors |
| `grep -r "sys.path.insert" cores/ managers/ utils/` | **0 matches** |
| `python -c "from session_manager import SessionManager"` | Import succeeds |
| `cd managers/session_manager && python -m session_manager` | Works (standalone execution) |
| `cd /tmp && python -c "from config_manager import ConfigManager"` | Import succeeds |

---

## ✅ Feature Validation Checklist

### Narrative Completeness
- [x] The Story section clearly states user problem and value
- [x] Intent is unambiguous to a non-technical reader
- [x] Scope is explicitly bounded

### Technical Completeness
- [x] Root pyproject.toml structure defined
- [x] Per-module pyproject.toml structure defined
- [x] Edge cases enumerated
- [x] Acceptance criteria are testable

### Traceability
- [x] Links to architecture doc
- [x] Dependencies listed

---

**← Back to:** [Architecture](./02_architecture.md) | **Next:** [Feature: UV Migrator Tool](./04_feature_uv_migrator_tool.md)
