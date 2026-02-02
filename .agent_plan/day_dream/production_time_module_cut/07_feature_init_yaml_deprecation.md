# 07 - Feature: init.yaml Deprecation ✅ COMPLETE

> Part of [Layer Taxonomy & Production Readiness Blueprint](./00_index.md)
>
> **Status:** ✅ **IMPLEMENTED** — All init.yaml files deleted, `[tool.adhd]` is source of truth
>
> See [Framework Modernization](../framework_modernization/09_feature_init_yaml_sunset.md) for full implementation details.

---

## 📖 The Story

### 😤 The Pain

```
Current Reality: Two Sources of Truth
┌───────────────────────────────────────────────────────────────────┐
│  init.yaml                        pyproject.toml (after P1)       │
│  ──────────                       ─────────────────────────       │
│  version: 0.0.1                   version = "0.1.0"  ◀── DUPE!   │
│  type: manager                                                    │
│  layer: runtime                                                   │
│  requirements:                    dependencies = [...]  ◀── DUPE! │
│    - https://github.com/...                                       │
│  repo_url: https://...                                            │
│                                                                   │
│  💥 Which one is authoritative?                                  │
│  💥 Version drift between files                                  │
│  💥 Two files to maintain per module                             │
└───────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Module maintainers | 🔥🔥 Medium | Every version bump |
| Framework developers | 🔥🔥 Medium | Adding new metadata |
| AI agents | 🔥 Low | Confusion about which file to read |

### ✨ The Vision

```
After This Feature:
┌───────────────────────────────────────────────────────────────────┐
│  pyproject.toml (SINGLE SOURCE OF TRUTH)                          │
│  ───────────────────────────────────────                          │
│  [project]                                                        │
│  name = "session-manager"                                         │
│  version = "0.1.0"                                                │
│  dependencies = ["config-manager", "pydantic>=2.0"]               │
│                                                                   │
│  [project.urls]                                                   │
│  Repository = "https://github.com/org/session_manager.git"        │
│                                                                   │
│  [tool.adhd]                                                      │
│  type = "manager"                                                 │
│  layer = "runtime"                                                │
│  shows_in_workspace = true                                        │
│                                                                   │
│  [tool.adhd.testing]                                              │
│  has_tests = true                                                 │
│  threat_model = "external"                                        │
│                                                                   │
│  ✅ ONE file per module                                           │
│  ✅ Standard Python tooling understands it                        │
│  ✅ ADHD-specific metadata in [tool.adhd]                         │
└───────────────────────────────────────────────────────────────────┘

init.yaml: DELETED ❌
```

### 🎯 One-Liner

> Replace init.yaml with `[tool.adhd]` section in pyproject.toml, achieving single-file-per-module metadata.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Metadata files per module | ❌ 2 (init.yaml + pyproject.toml) | ✅ 1 (pyproject.toml) |
| Version source of truth | ❌ Ambiguous | ✅ pyproject.toml only |
| Standard tooling compatibility | ⚠️ Partial | ✅ Full |
| ADHD-specific metadata | ❌ Custom format | ✅ Standard `[tool.X]` pattern |

---

## 🔧 The Spec

---

## 🎯 Overview

After P1 creates pyproject.toml for all modules, P3 migrates all remaining init.yaml fields to `[tool.adhd]` and deletes init.yaml files entirely.

**Priority:** P3  
**Difficulty:** `[KNOWN]`

---

## 📚 Prior Art

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| `[tool.pytest]` | pytest config in pyproject.toml | High | ✅ Same pattern |
| `[tool.black]` | Black formatter config | High | ✅ Same pattern |
| `[tool.ruff]` | Ruff linter config | High | ✅ Same pattern |
| `[tool.poetry]` | Poetry-specific metadata | High | ✅ Same pattern |

### The `[tool.X]` Pattern

This is the **standard Python pattern** for tool-specific metadata in pyproject.toml. ADHD uses `[tool.adhd]`.

---

## 🗺️ Field Migration Map

| init.yaml Field | pyproject.toml Location | Notes |
|-----------------|------------------------|-------|
| `version` | `[project].version` | Standard field |
| `type` | `[tool.adhd].type` | ADHD-specific |
| `layer` | `[tool.adhd].layer` | ADHD-specific |
| `repo_url` | `[project.urls].Repository` | Standard field |
| `requirements` | `[project].dependencies` | Standard field (package names, not URLs) |
| `folder_path` | **DELETED** | Legacy, not needed |
| `shows_in_workspace` | `[tool.adhd].shows_in_workspace` | ADHD-specific |
| `testing` | `[tool.adhd.testing]` | ADHD-specific nested table |
| `tags` | `[project].keywords` | Standard field |

---

## 👥 User Stories

| As a... | I want to... | So that... |
|---------|--------------|------------|
| Module maintainer | Edit one file for metadata | I don't have version drift |
| Framework developer | Use standard pyproject.toml | I don't maintain custom parsers |
| AI agent | Read `[tool.adhd]` | I understand module semantics |
| New contributor | See one metadata file | Less cognitive load |

---

## ✅ Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | All init.yaml content migrated to pyproject.toml | Diff check: no data loss |
| 2 | All init.yaml files deleted | `find . -name "init.yaml"` returns 0 |
| 3 | `[tool.adhd]` section present in all modules | grep check |
| 4 | ADHD framework reads from pyproject.toml | modules_controller test |
| 5 | yaml_reading_core deprecated or removed | Code audit |

---

## 🛠️ Technical Notes

### Complete pyproject.toml Example (Post-Migration)

```toml
# managers/session_manager/pyproject.toml
[project]
name = "session-manager"
version = "0.1.0"
requires-python = ">=3.10"
keywords = ["session", "auth", "database"]

dependencies = [
    "config-manager",
    "logger-util",
    "auth-manager",
    "pydantic>=2.0",
    "sqlalchemy>=2.0",
]

[project.urls]
Repository = "https://github.com/AI-Driven-Highspeed-Development/session_manager.git"

[tool.adhd]
type = "manager"
layer = "runtime"
shows_in_workspace = true

[tool.adhd.testing]
has_tests = true
scope.platforms = ["linux", "macos"]
scope.python_versions = ["3.10", "3.11"]
scope.threat_model = "external"
scope.input_assumptions = ["Inputs from authenticated users"]
scope.out_of_scope = ["DoS attacks"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### modules_controller_core Changes

```python
# BEFORE: Read from init.yaml
def load_module_metadata(path: Path) -> ModuleInfo:
    init_yaml = load_yaml(path / "init.yaml")
    return ModuleInfo(
        version=init_yaml["version"],
        type=init_yaml["type"],
        ...
    )

# AFTER: Read from pyproject.toml
def load_module_metadata(path: Path) -> ModuleInfo:
    pyproject = load_toml(path / "pyproject.toml")
    project = pyproject["project"]
    adhd = pyproject.get("tool", {}).get("adhd", {})
    
    return ModuleInfo(
        version=project["version"],
        type=adhd.get("type", "unknown"),
        layer=adhd.get("layer", "runtime"),
        repo_url=project.get("urls", {}).get("Repository"),
        ...
    )
```

### Migration Script

```python
def migrate_init_yaml_to_pyproject(module_path: Path) -> None:
    """Move all init.yaml data to pyproject.toml, then delete init.yaml"""
    init_yaml = load_yaml(module_path / "init.yaml")
    pyproject = load_toml(module_path / "pyproject.toml")
    
    # Ensure [tool.adhd] section exists
    if "tool" not in pyproject:
        pyproject["tool"] = {}
    if "adhd" not in pyproject["tool"]:
        pyproject["tool"]["adhd"] = {}
    
    adhd = pyproject["tool"]["adhd"]
    
    # Migrate fields
    adhd["type"] = init_yaml.get("type", "unknown")
    adhd["layer"] = init_yaml.get("layer", "runtime")
    if "shows_in_workspace" in init_yaml:
        adhd["shows_in_workspace"] = init_yaml["shows_in_workspace"]
    if "testing" in init_yaml:
        adhd["testing"] = init_yaml["testing"]
    
    # repo_url goes to [project.urls]
    if "repo_url" in init_yaml:
        if "urls" not in pyproject["project"]:
            pyproject["project"]["urls"] = {}
        pyproject["project"]["urls"]["Repository"] = init_yaml["repo_url"]
    
    # Write back
    write_toml(module_path / "pyproject.toml", pyproject)
    
    # DELETE init.yaml
    (module_path / "init.yaml").unlink()
```

---

## ⚠️ Edge Cases

| Scenario | Handling |
|----------|----------|
| Module has init.yaml but no pyproject.toml | Error: P1 must complete first |
| init.yaml has fields not in pyproject.toml | Migrate to `[tool.adhd]` |
| Module uses yaml_reading_core for other YAML | Only init.yaml deprecated, not the core |
| External tools depend on init.yaml | Update tools in same PR |

---

## ❌ Out of Scope

| Excluded | Rationale |
|----------|-----------|
| Deprecating YAML usage entirely | Only init.yaml, not config files |
| Removing yaml_reading_core | Still needed for .config files |
| Backward compatibility shim | P3 is clean break, no dual-read |

---

## 🔗 Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| P1 complete (pyproject.toml exists) | Internal | Prerequisite |
| P2 complete (new CLI works) | Internal | Prerequisite |
| modules_controller_core updated | Internal | Part of this feature |

---

## ❓ Open Questions

| Question | Status | Tentative Answer |
|----------|--------|------------------|
| What about projects using ADHD modules externally? | ⏳ Open | They should pin versions, not rely on init.yaml |
| Should we keep init.yaml reader for backward compat? | ✅ Resolved | No. Clean break in P3. |
| What about `.config_template` files? | ✅ Resolved | Keep, unrelated to metadata |

---

## ✅ Feature Validation Checklist

### Narrative Completeness
- [x] The Story section clearly states user problem and value
- [x] Intent is unambiguous to a non-technical reader
- [x] Scope is explicitly bounded

### Technical Completeness
- [x] Field migration map complete
- [x] Complete pyproject.toml example provided
- [x] Migration script illustrative
- [x] Edge cases enumerated

### Traceability
- [x] Dependencies on P1/P2 documented
- [x] Links to architecture doc

---

**← Back to:** [Feature: CLI Migration](./06_feature_cli_migration.md) | **Next:** [Implementation](./80_implementation.md)
