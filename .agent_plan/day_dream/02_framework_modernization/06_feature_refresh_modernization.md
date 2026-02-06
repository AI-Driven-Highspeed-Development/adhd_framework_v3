# 06 - Feature: Refresh Modernization

> Part of [Framework Modernization Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Refresh - What Does It Do?
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  adhd refresh                                                              │
│          │                                                                 │
│          ▼                                                                 │
│  ┌─────────────────────────────────────┐                                   │
│  │ modules_controller_core             │                                   │
│  │                                     │                                   │
│  │  For each module with refresh.py:   │                                   │
│  │    - Run refresh.py script          │  ← STILL NEEDED                   │
│  │                                     │                                   │
│  │  What refresh.py typically does:    │                                   │
│  │    - instruction_core: sync files   │  ← STILL NEEDED                   │
│  │    - adhd_mcp: generate schemas     │  ← STILL NEEDED                   │
│  │                                     │                                   │
│  └─────────────────────────────────────┘                                   │
│                                                                            │
│  PROBLEM: Refresh logic is mixed with init.yaml scanning                   │
│           Need to extract the good parts (refresh.py execution)            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Developer needing to sync instructions | 🔥🔥 Medium | After instruction changes |
| Developer needing to regenerate schemas | 🔥🔥 Medium | After MCP changes |

### ✨ The Vision

```
After Modernization:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  adhd refresh                                                              │
│          │                                                                 │
│          ▼                                                                 │
│  ┌─────────────────────────────────────┐                                   │
│  │ modules_controller_core (simplified)│                                   │
│  │                                     │                                   │
│  │  1. Read workspace members from     │                                   │
│  │     pyproject.toml                  │  ← NEW: READ STANDARD FORMAT      │
│  │                                     │                                   │
│  │  2. For each module:                │                                   │
│  │     - Check for refresh.py          │                                   │
│  │     - Run if exists                 │  ← UNCHANGED                      │
│  │                                     │                                   │
│  │  3. Optionally run `uv sync`        │  ← NEW: ENSURE DEPS SYNCED        │
│  │                                     │                                   │
│  └─────────────────────────────────────┘                                   │
│                                                                            │
│  ✅ SAME FUNCTIONALITY, CLEANER IMPLEMENTATION                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Refresh continues to run module refresh.py scripts, but discovers modules from pyproject.toml instead of init.yaml.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Module discovery | ❌ Scan for init.yaml | ✅ Read pyproject.toml workspace |
| Refresh script execution | ✅ Works | ✅ Works (unchanged) |
| Dependency sync | ❌ Separate command | ✅ Optional `--sync` flag |

---

## 🔧 The Spec

---

## 🎯 Overview

Refresh functionality stays, but the **module discovery** changes:

1. **Module discovery** reads from `pyproject.toml` workspace members
2. **refresh.py execution** stays exactly the same
3. **Optional `uv sync`** can be triggered with flag

**Priority:** P1  
**Difficulty:** `[KNOWN]`

---

## 📚 Prior Art

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| Current refresh.py pattern | Internal | High | ✅ Keep |
| UV workspace members | Standard | High | ✅ Adopt for discovery |

### Build-vs-Adopt

**Keep:** refresh.py execution pattern works well  
**Adopt:** UV workspace for module discovery

---

## 👥 User Stories

| As a... | I want to... | So that... |
|---------|--------------|------------|
| Developer | Refresh instruction files | .github/ folder stays in sync |
| Developer | Refresh MCP schemas | OpenAPI specs are regenerated |
| Developer | Refresh all modules at once | One command does everything |
| Developer | Refresh specific module | Faster for focused work |

---

## ✅ Acceptance Criteria

- [ ] `adhd refresh` discovers modules from pyproject.toml
- [ ] `adhd refresh` runs refresh.py for modules that have it
- [ ] `adhd refresh --module <name>` still works
- [ ] `adhd refresh --sync` runs `uv sync` first
- [ ] No dependency on init.yaml

---

## 📊 Module Discovery Change

### Before: init.yaml Scanning

```python
# modules_controller_core (current)
def scan_all_modules(self) -> ModulesReport:
    for module_type in self.module_types.get_all_types():
        for path in module_type.path.iterdir():
            init_yaml = path / "init.yaml"
            if init_yaml.exists():
                # Parse init.yaml, create ModuleInfo
                ...
```

### After: pyproject.toml Reading

```python
# modules_controller_core (modernized)
def scan_all_modules(self) -> ModulesReport:
    # Read workspace members from root pyproject.toml
    root_config = self._read_root_pyproject()
    members_patterns = root_config.get("tool", {}).get("uv", {}).get("workspace", {}).get("members", [])
    
    for pattern in members_patterns:
        for path in self.root_path.glob(pattern):
            if (path / "pyproject.toml").exists():
                # Parse pyproject.toml, create ModuleInfo
                ...
```

---

## 🛠️ Technical Notes

### ModuleInfo Changes

| Field | Before (init.yaml) | After (pyproject.toml) |
|-------|-------------------|------------------------|
| name | `name:` field | `[project]name` |
| version | `version:` field | `[project]version` |
| module_type | `type:` field | Inferred from path |
| requirements | `requirements:` list | `[project.dependencies]` |
| repo_url | `repo_url:` field | Not needed (git remote) |

### refresh.py Interface (UNCHANGED)

```python
# cores/instruction_core/refresh.py
def main() -> None:
    """Refresh script - interface stays exactly the same."""
    controller = InstructionController(root_path=Path.cwd())
    controller.run()

if __name__ == "__main__":
    main()
```

### CLI Changes

```python
def refresh_project(self, args) -> None:
    """Refresh project modules."""
    if getattr(args, 'sync', False):
        subprocess.run(["uv", "sync"])
    
    controller = ModulesController()  # Now reads pyproject.toml
    
    if args.module:
        module = controller.get_module_by_name(args.module)
        if module and module.has_refresh_script():
            controller.run_module_refresh_script(module)
    else:
        for module in controller.list_all_modules().modules:
            if module.has_refresh_script():
                controller.run_module_refresh_script(module)
```

---

## ⚠️ Edge Cases

| Scenario | Handling |
|----------|----------|
| Module without pyproject.toml | Skip with warning |
| Glob pattern matches non-module directory | Check for pyproject.toml before including |
| refresh.py fails | Log error, continue with other modules |
| No refresh.py in module | Skip silently (normal case) |

---

## ❌ Out of Scope

| Item | Rationale |
|------|-----------|
| Watching for file changes | Overkill, manual refresh is fine |
| Parallel refresh execution | Single-threaded is simple and predictable |
| Dependency-ordered refresh | Current execution order is fine |

---

## 🔗 Dependencies

| Depends On | For |
|------------|-----|
| Modules have pyproject.toml | Module discovery |
| refresh.py convention | Script execution |

---

**← Back to:** [05 - Feature: Module Inclusion](./05_feature_module_inclusion.md)  
**Next:** [07 - Feature: CLI Entry Points](./07_feature_cli_entry_points.md)
