# 04 - Feature: Module Creation

> Part of [Framework Modernization Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Module Creation:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  adhd create-module "my_module" --type core                                │
│          │                                                                 │
│          ▼                                                                 │
│  ┌─────────────────────────────────────┐                                   │
│  │ module_creator_core                 │                                   │
│  │                                     │                                   │
│  │  1. Create directory structure      │                                   │
│  │  2. Write init.yaml with:           │  ← DEPRECATED FORMAT              │
│  │     - version: 0.0.1                │                                   │
│  │     - type: core                    │                                   │
│  │     - requirements: []              │  ← CUSTOM FORMAT                  │
│  │  3. Write __init__.py, README.md    │                                   │
│  │  4. Optionally create remote repo   │                                   │
│  └─────────────────────────────────────┘                                   │
│          │                                                                 │
│          ▼                                                                 │
│  OUTPUT: Module with init.yaml                                             │
│          💥 NOT A VALID UV WORKSPACE MEMBER                                │
│          💥 CANNOT USE `from my_module import X`                           │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Developer creating new modules | 🔥🔥🔥 High | Several times/week |
| Developer importing new modules | 🔥🔥🔥 High | Immediately after creation |

### ✨ The Vision

```
After Modernization:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  adhd create-module "my_module" --type core                                │
│          │                                                                 │
│          ▼                                                                 │
│  ┌─────────────────────────────────────┐                                   │
│  │ module_creator_core                 │                                   │
│  │                                     │                                   │
│  │  1. Create directory structure      │                                   │
│  │  2. Write pyproject.toml with:      │  ← STANDARD FORMAT                │
│  │     - [project] name, version       │                                   │
│  │     - [project.dependencies]        │  ← PIP FORMAT                     │
│  │  3. Write __init__.py, README.md    │                                   │
│  │  4. Optionally create remote repo   │                                   │
│  │  5. Run `uv sync` to link module    │  ← IMMEDIATELY IMPORTABLE         │
│  └─────────────────────────────────────┘                                   │
│          │                                                                 │
│          ▼                                                                 │
│  OUTPUT: Module with pyproject.toml                                        │
│          ✅ VALID UV WORKSPACE MEMBER                                      │
│          ✅ IMMEDIATELY IMPORTABLE                                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Module creation generates pyproject.toml making new modules immediately importable via UV workspace.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Config format | ❌ Custom init.yaml | ✅ Standard pyproject.toml |
| Importable after creation | ❌ Need manual setup | ✅ Immediately via `uv sync` |
| Dependencies format | ❌ GitHub URLs | ✅ pip packages |
| Standard Python compatible | ❌ No | ✅ Yes |

---

## 🔧 The Spec

---

## 🎯 Overview

Modify `module_creator_core` to generate UV-native module structure:

1. **Generate pyproject.toml** instead of init.yaml
2. **Include proper package metadata** (PEP 621 compliant)
3. **Configure as workspace member** (already in glob pattern)
4. **Run `uv sync`** to make module immediately importable

**Priority:** P0  
**Difficulty:** `[KNOWN]`

---

## 📚 Prior Art

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| UV workspace members | Standard | High | ✅ Adopt |
| PEP 621 format | Standard | High | ✅ Adopt |
| src/ layout | Pattern | Medium | ❌ Reject (flat is fine) |

### Usage Decision

**Using:** PEP 621 pyproject.toml + UV workspace membership  
**How:** Emit minimal pyproject.toml, leverage root workspace glob patterns  
**Why:** Standard format, minimal configuration needed

---

## 👥 User Stories

| As a... | I want to... | So that... |
|---------|--------------|------------|
| Developer | Create new module | I can add functionality to my project |
| Developer | Import new module immediately | I don't need extra setup steps |
| Developer | Add dependencies to module | Module gets what it needs |

---

## ✅ Acceptance Criteria

- [ ] `adhd create-module` creates pyproject.toml (not init.yaml)
- [ ] pyproject.toml is PEP 621 compliant
- [ ] Module is importable after creation + `uv sync`
- [ ] Module type still determines directory (cores/, managers/, etc.)
- [ ] Remote repo creation still works
- [ ] Dependencies use pip format

---

## 📊 Data Flow

### Current Output

```yaml
# init.yaml (CURRENT)
version: 0.0.1
folder_path: cores/my_module
type: core
requirements: []
repo_url: https://github.com/.../my_module.git
```

### Target Output

```toml
# pyproject.toml (TARGET)
[project]
name = "my-module"
version = "0.0.1"
description = "A core module for ADHD Framework"
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["my_module"]
```

---

## 🛠️ Technical Notes

### Key Changes to module_creator_core

| File | Change |
|------|--------|
| `module_creator.py` | Replace `_write_init_yaml()` with `_write_pyproject_toml()` |
| `module_creator.py` | Add `_run_uv_sync()` call after creation |
| `module_creator.py` | Remove `_add_module_to_project_init()` (no more init.yaml) |
| `module_creator.py` | **ADD** embedded template constants (MODULE_PYPROJECT_TEMPLATE, etc.) |
| `module_creation_wizard.py` | Update prompts for pip-format dependencies |
| `module_types.py` | Keep (still useful for directory organization) |
| `templates.py` | **DELETE** if exists - templates now embedded in creator |

### Embedded Template Approach (YAGNI-Compliant)

> **Key Insight:** Module templates are embedded directly in `module_creator_core` code. No external template repos, no `project/data/templates/` folder. This is simpler and has proven sufficient.

```python
# module_creator.py - Templates embedded directly in code

MODULE_PYPROJECT_TEMPLATE = '''[project]
name = "{package_name}"
version = "0.0.1"
description = "A {module_type} module"
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{module_name}"]
'''

MODULE_INIT_TEMPLATE = '''"""{{module_name}} module."""
'''

MODULE_README_TEMPLATE = '''# {module_name}

A {module_type} module for ADHD Framework.
'''

def _write_pyproject_toml(self, target: Path, params: ModuleCreationParams) -> None:
    # Convert snake_case module name to kebab-case package name
    package_name = params.module_name.replace("_", "-")
    
    content = MODULE_PYPROJECT_TEMPLATE.format(
        package_name=package_name,
        module_type=params.module_type,
        module_name=params.module_name
    )
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{params.module_name}"]
'''
    (target / "pyproject.toml").write_text(content)
```

### Module Name Conventions

| Internal Name | Package Name | Import Name |
|---------------|--------------|-------------|
| `config_manager` | `config-manager` | `config_manager` |
| `logger_util` | `logger-util` | `logger_util` |

---

## ⚠️ Edge Cases

| Scenario | Handling |
|----------|----------|
| Module name with hyphens | Convert to underscores for directory/import |
| Module already exists | Error with clear message |
| No UV installed | Error with install instructions |
| Module type not in workspace glob | Add explicit member to root pyproject.toml |

---

## 🔗 Relationship to Workspace Patterns

Root pyproject.toml should have:

```toml
[tool.uv.workspace]
members = [
    "cores/*",
    "managers/*",
    "utils/*",
    "plugins/*",
    "mcps/*",
]
```

New modules created in these directories are **automatically** workspace members. No explicit registration needed!

---

## ❌ Out of Scope

| Item | Rationale |
|------|-----------|
| Migrating existing init.yaml modules | Covered in 09_feature_init_yaml_sunset.md |
| Custom build backends | Hatch is sufficient and simple |
| src/ layout | Flat layout matches existing convention |

---

## 🔗 Dependencies

| Depends On | For |
|------------|-----|
| UV installed | Running `uv sync` |
| Root workspace configured | Glob patterns for auto-membership |

---

**← Back to:** [03 - Feature: Project Creation](./03_feature_project_creation.md)  
**Next:** [05 - Feature: Module Inclusion](./05_feature_module_inclusion.md)
