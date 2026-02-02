# 08 - ~~Feature: Template Updates~~ DEPRECATED: Template Elimination

> Part of [Framework Modernization Blueprint](./00_index.md)

---

## 🚫 DEPRECATION NOTICE

**Status:** `[CUT]` - This feature has been **ELIMINATED** as of 2026-02-01.

**Reason:** External template system was **over-engineered** (YAGNI). User feedback confirms:
1. There has **NEVER** been a need for non-default templates
2. Cloning template repos adds unnecessary latency and complexity
3. `project/data/templates/` folder was unnecessary overhead

**Resolution:** Templates are now **embedded directly in creator modules** as Python string constants.

---

## 📖 The Story (Historical)

### 😤 The Original Pain (NOW RESOLVED DIFFERENTLY)

```
Current Templates:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  Project Templates (in repos):                                             │
│  ├── init.yaml                    ← DEPRECATED                             │
│  ├── requirements.txt             ← DEPRECATED                             │
│  ├── .gitignore                   ← OK                                     │
│  └── README.md                    ← OK                                     │
│                                                                            │
│  Module Templates (in code):                                               │
│  ├── _write_init_yaml()           ← GENERATES DEPRECATED FORMAT            │
│  ├── _write_placeholder_files()   ← OK but incomplete                      │
│  └── No pyproject.toml!           ← 💥 MISSING KEY FILE                    │
│                                                                            │
│  PROBLEM: Templates emit old-world artifacts that don't work with UV       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Project creator | 🔥🔥🔥 High | Every new project |
| Module creator | 🔥🔥🔥 High | Every new module |
| Template maintainer | 🔥🔥 Medium | Each update |

### ✨ The Vision (SUPERSEDED)

> **This vision has been SUPERSEDED by the embedded template approach.**

```
ACTUAL Implementation (Simpler):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  project_creator_core/project_creator.py:                                  │
│  ├── PYPROJECT_TEMPLATE = '''...'''    ← EMBEDDED AS CONSTANTS             │
│  ├── GITIGNORE_TEMPLATE = '''...'''    ← NO EXTERNAL FILES                 │
│  ├── README_TEMPLATE = '''...'''       ← NO CLONING                        │
│  └── def create_project():             ← GENERATES FROM CONSTANTS          │
│                                                                            │
│  module_creator_core/module_creator.py:                                    │
│  ├── MODULE_PYPROJECT_TEMPLATE = '''...'''                                 │
│  ├── MODULE_INIT_TEMPLATE = '''...'''                                      │
│  └── def create_module():              ← GENERATES FROM CONSTANTS          │
│                                                                            │
│  ✅ NO EXTERNAL REPOS                                                      │
│  ✅ NO project/data/templates/ FOLDER                                      │
│  ✅ NO TEMPLATE CLONING                                                    │
│  ✅ INSTANT PROJECT/MODULE CREATION                                        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner (Updated)

> ~~All templates (project and module) emit UV-native artifacts, no legacy formats.~~

> **NEW:** Templates are **embedded in creator modules** as Python constants. No external template repos, no template folder, no cloning.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Project template files | ❌ init.yaml, requirements.txt | ✅ pyproject.toml |
| Module template files | ❌ init.yaml | ✅ pyproject.toml |
| sys.path hacks in templates | ❌ Yes | ✅ No |
| UV-compatible out of the box | ❌ No | ✅ Yes |

---

## 🔧 The Spec (DEPRECATED)

> **⚠️ This entire section is DEPRECATED. The spec below documents what was originally planned but is NO LONGER being implemented.**

---

## 🎯 Overview (DEPRECATED)

~~Update all templates across the framework:~~

1. ~~**Project templates** in external repos~~ → **ELIMINATED**
2. ~~**Module templates** in code (module_creator_core)~~ → **EMBEDDED as constants**
3. ~~**Documentation templates** (README patterns)~~ → **EMBEDDED in creators**
4. ~~**Configuration templates** (.config_template)~~ → **EMBEDDED if needed**

**Priority:** ~~P2~~ `[CUT]`  
**Difficulty:** `[CUT]`

---

## 📚 Prior Art (Historical)

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| PEP 621 | Standard | High | ✅ Adopt |
| Hatchling build system | Tool | High | ✅ Adopt |
| Copier templates | Tool | Medium | 🤔 Consider later |

### Usage Decision (SUPERSEDED)

~~**Using:** PEP 621 pyproject.toml + Hatchling~~  
~~**How:** Standardize all templates on these~~  
~~**Why:** Modern Python standards, UV compatible~~

**ACTUAL Decision:** Embed templates directly in creator modules. Copier/external repos are **YAGNI**.

---

## 👥 User Stories (DEPRECATED)

| As a... | I want to... | So that... | Status |
|---------|--------------|------------|--------|
| ~~Developer~~ | ~~Create project with modern structure~~ | ~~It works with UV immediately~~ | ✅ Achieved via embedded templates |
| ~~Developer~~ | ~~Create module with pyproject.toml~~ | ~~Module is properly packaged~~ | ✅ Achieved via embedded templates |
| ~~Template maintainer~~ | ~~Have one template format~~ | ~~Less maintenance burden~~ | ✅ Achieved via code constants |

---

## ✅ Acceptance Criteria (ALL CUT)

- [x] ~~All project templates emit pyproject.toml~~ → **Achieved via embedded PYPROJECT_TEMPLATE constant**
- [x] ~~All module templates emit pyproject.toml~~ → **Achieved via embedded MODULE_PYPROJECT_TEMPLATE constant**
- [x] ~~No templates emit init.yaml~~ → **N/A - no external templates exist**
- [x] ~~No templates emit requirements.txt~~ → **N/A - no external templates exist**
- [x] ~~Templates include appropriate .gitignore~~ → **Achieved via embedded GITIGNORE_TEMPLATE constant**
- [x] ~~READMEs reference UV commands~~ → **Achieved via embedded README_TEMPLATE constant**

---

## 📊 Template Specifications (NOW EMBEDDED CONSTANTS)

### Project Template: pyproject.toml

```toml
[project]
name = "{{project_name}}"
version = "0.1.0"
description = "{{description}}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.workspace]
members = [
    "cores/*",
    "managers/*",
    "utils/*",
    "plugins/*",
    "mcps/*",
]

[project.scripts]
adhd = "adhd_framework:main"
```

### Project Template: .gitignore

```gitignore
# UV
.venv/
uv.lock    # Or include if you want reproducible builds

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project
*.egg-info/
dist/
build/
.eggs/

# Environment
.env
.env.local

# ADHD Framework
project/data/
```

### Project Template: README.md (snippet)

```markdown
## Getting Started

### Prerequisites
- Python 3.10+
- [UV](https://github.com/astral-sh/uv)

### Setup
```bash
# Clone and enter project
git clone <repo>
cd {{project_name}}

# Install dependencies and sync workspace
uv sync

# Run a command
uv run adhd --help
```
```

### Module Template: pyproject.toml

```toml
[project]
name = "{{module_name_kebab}}"
version = "0.0.1"
description = "A {{module_type}} module for ADHD Framework"
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{{module_name_snake}}"]
```

### Module Template: __init__.py

```python
"""{{module_name}} {{module_type}} module."""

# Clean exports - no sys.path manipulation!
from .{{module_name}}_main import *  # Or specific exports

__all__ = [
    # Explicit exports
]
```

### Module Template: .config_template

```json
{
    "module_name": "{{module_name}}",
    "path": {
        "data": "./project/data/{{module_name}}"
    }
}
```

---

## 🛠️ Technical Notes (UPDATED)

### Template Variable Convention (Still Valid)

| Variable | Example | Used In |
|----------|---------|---------|
| `{project_name}` | `my-project` | Project name |
| `{module_name}` | `config_manager` | Python import (snake_case) |
| `{package_name}` | `config-manager` | Package name (kebab-case) |
| `{module_type}` | `core` | Module type |
| `{description}` | User input | Descriptions |

### Template Locations (CHANGED)

| Template | ~~Old Location~~ | **New Location** |
|----------|------------------|------------------|
| Project templates | ~~External repos (GitHub)~~ | **Embedded in `project_creator_core/project_creator.py`** |
| Module templates | ~~`module_creator_core/*.py` (external files)~~ | **Embedded in `module_creator_core/module_creator.py`** |
| Config templates | `*/.config_template` | Unchanged (JSON, per-module) |

### Migration Strategy (SIMPLIFIED)

~~1. **Phase 1:** Update in-code templates (module_creator_core)~~  
~~2. **Phase 2:** Update external project template repos~~  
~~3. **Phase 3:** Document new template variables~~

**NEW Strategy (Single Step):**
1. Embed all templates as Python string constants in creator modules
2. Delete any external template repo references
3. Delete `project/data/templates/` folder if it exists

---

## ⚠️ Edge Cases (NOW SIMPLER)

| Scenario | ~~Old Handling~~ | **New Handling** |
|----------|------------------|------------------|
| ~~Old template repo cloned~~ | ~~Overwrite with new pyproject.toml~~ | **N/A - no template repos** |
| ~~Template variables not substituted~~ | ~~Error with clear message~~ | **Python .format() handles this** |
| ~~Custom module type~~ | ~~Use default template with type substituted~~ | **Same - embedded templates support this** |

---

## ❌ Out of Scope (CONFIRMED AS CUT)

| Item | Rationale | Status |
|------|-----------|--------|
| Copier/Cookiecutter integration | ~~Simple templates sufficient~~ | **CUT - embedded templates are simpler** |
| Template versioning | ~~Git versioning is sufficient~~ | **CUT - code versioning handles this** |
| Template marketplace | ~~Overkill for current needs~~ | **CUT - YAGNI confirmed** |
| **External template repos** | N/A | **CUT - never needed** |
| **`project/data/templates/` folder** | N/A | **CUT - never needed** |

---

## 🔗 Dependencies (ELIMINATED)

| ~~Depends On~~ | ~~For~~ | Status |
|----------------|---------|--------|
| ~~Project creation updates (03)~~ | ~~Templates used by creator~~ | **N/A - templates IN creator** |
| ~~Module creation updates (04)~~ | ~~Templates used by creator~~ | **N/A - templates IN creator** |

---

## [Custom] 📁 Files to Create/Update (REVISED)

### ~~New Files Needed~~ → Now Embedded Constants

| ~~File~~ | ~~Purpose~~ | **Replacement** |
|----------|-------------|-----------------|
| ~~Project template pyproject.toml~~ | ~~Root UV workspace config~~ | `PYPROJECT_TEMPLATE` constant in `project_creator.py` |
| ~~Module template pyproject.toml~~ | ~~Per-module config~~ | `MODULE_PYPROJECT_TEMPLATE` constant in `module_creator.py` |
| ~~Updated .gitignore~~ | ~~UV-aware ignores~~ | `GITIGNORE_TEMPLATE` constant in `project_creator.py` |
| ~~Updated README.md~~ | ~~UV-based instructions~~ | `README_TEMPLATE` constant in `project_creator.py` |

### Files to REMOVE/DELETE

| File/Folder | Reason | Action |
|-------------|--------|--------|
| `project/data/templates/` | No longer needed | **DELETE if exists** |
| External template repo URLs in config | No longer needed | **REMOVE from any config** |
| Template cloning code | No longer needed | **DELETE from creators** |
| ~~init.yaml in templates~~ | ~~Replaced by pyproject.toml~~ | **N/A - no template files** |
| ~~requirements.txt in templates~~ | ~~Replaced by pyproject.toml~~ | **N/A - no template files** |

---

## 📝 Summary: What Changed

| Aspect | Original Plan | Final Decision |
|--------|---------------|----------------|
| Template storage | External GitHub repos | **Embedded in code as constants** |
| Template folder | `project/data/templates/` | **ELIMINATED** |
| Template cloning | At project creation time | **ELIMINATED** |
| Custom templates | Supported | **YAGNI - never needed** |
| Feature status | P2 Feature | **CUT - absorbed into 03 and 04** |

---

**← Back to:** [07 - Feature: CLI Entry Points](./07_feature_cli_entry_points.md)  
**Next:** [09 - Feature: init.yaml Sunset](./09_feature_init_yaml_sunset.md)
