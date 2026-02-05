# 01 - Feature: New modules/ Structure

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌──────────────────────────────────────────────────────────────────┐
│  Developer creates new module  ──────►  💥 DECISION PARALYSIS    │
│                                                                  │
│  "Is this a manager or a util?"                                  │
│  "Is this a plugin or a core?"                                   │
│  "Where does an MCP server go?"                                  │
│                                                                  │
│  6 folders, subjective type debates, inconsistent conventions    │
└──────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| New contributors | 🔥🔥🔥 High | Every new module |
| Existing devs | 🔥🔥 Medium | Refactoring, reviewing |
| AI agents | 🔥🔥🔥 High | Module discovery, routing |

**Root Cause:** `type` is subjective. Two developers can disagree whether something is a "util" or "manager."

### ✨ The Vision

```
After This Change:
┌──────────────────────────────────────────────────────────────────┐
│  Developer creates new module  ──────►  ✅ ONE QUESTION          │
│                                                                  │
│  "What layer? (foundation / runtime / dev)"                      │
│                                                                  │
│  Layer = dependency order. Objective. No debates.                │
│  modules/foundation/ → modules/runtime/ → modules/dev/           │
└──────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> We're replacing 6 subjective type folders with a single `modules/` structure where objective dependency layers determine placement.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Folders to choose from | ❌ 6 (subjective) | ✅ 3 (objective layers) |
| "Where does X go?" debates | ❌ Common | ✅ Never |
| Discovery code paths | ❌ 6 separate scans | ✅ 1 unified scan |
| Cognitive load | ❌ High | ✅ Low |

---

## 🔧 The Spec

---

## 🎯 Overview

The new structure replaces legacy folders (`cores/`, `managers/`, `plugins/`, `utils/`, `mcps/`, `project/`) with a unified `modules/` directory organized by **layer** (dependency order):

```
modules/
├── foundation/           # Foundation layer: only depends on other foundation
│   ├── exceptions_core/  # (true zero deps)
│   ├── logger_util/      # (→ exceptions_core)
│   ├── config_manager/   # (→ logger_util, exceptions_core)
│   ├── cli_manager/      # Framework infrastructure
│   └── ...               # All framework modules
├── dev/                  # Dev layer: development-time only
│   ├── hyper_red_core/   # Testing tooling
│   └── adhd_mcp/         # MCP server for AI agents during development
└── runtime/              # Runtime layer: app-specific modules
    ├── (empty in framework repo)
    └── ...               # In generated projects: user's modules

```

> **Critical Context: Framework vs Generated Projects**
>
> | Context | Foundation | Runtime | Dev |
> |---------|------------|---------|-----|
> | **ADHD Framework repo** | All framework modules | **Empty** | Testing tools |
> | **Generated projects** | Inherited from framework | User's app modules | Testing tools |
>
> **Why?** The ADHD Framework is a "factory" for creating projects — it will never "ship" as a product itself. Framework infrastructure (cli_manager, modules_controller_core, etc.) is **foundation**. Dev-time tooling (adhd_mcp, hyper_red_core) goes in **dev**. Runtime modules only appear in **generated projects** where users add their own business logic.

> **Rationale for symmetric folders:** Real projects using ADHD Framework will have 30+ modules since modules are designed to be small (fit in AI context window). At that scale, symmetric layer folders reduce cognitive load.

**Priority:** P0  
**Difficulty:** `[KNOWN]`

---

## 📚 Prior Art

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| Go's `internal/` convention | Pattern | Medium | 🔧 Adapt |
| Rust's crate workspaces | Pattern | Medium | 🔧 Adapt |
| monorepo tools (Nx, Turborepo) | Tool | Low | ❌ Reject |
| Our current 6-folder structure | Pattern | High | ❌ Reject |

### Build-vs-Adopt Justification

| Rejected Solution | Reason |
|-------------------|--------|
| Keep 6 folders | Subjective type debates, discovery complexity |
| Nx/Turborepo | Overkill for module organization only |
| Flat modules/ with no layers | Loses dependency clarity |

---

## 🗺️ The New Structure

### Layer Definitions

| Layer | Path | Can Import From | Production? | Removal Test |
|-------|------|-----------------|-------------|---------------|
| **foundation** | `modules/foundation/` | Foundation only | ✅ Ships | Remove → runtime and dev break |
| **runtime** | `modules/runtime/` | Foundation + runtime | ✅ Ships | Remove → dev breaks |
| **dev** | `modules/dev/` | Anything | ❌ Stripped | Remove → nothing breaks |

> **Foundation DAG Rule**: Foundation modules must form a directed acyclic graph (no circular dependencies).
>
> **Valid foundation example**:
> ```
> exceptions_core (true zero deps)
>        ↓
> logger_util (→ exceptions_core) 
>        ↓
> config_manager (→ logger_util, exceptions_core)
> ```
> All three are foundation because none import from runtime or dev.

| Layer | Examples |
|-------|----------|
| **foundation** | logger_util, config_manager, exceptions_core, cli_manager, modules_controller_core (framework infrastructure) |
| **runtime** | *(empty in framework repo)* — in generated projects: user's api_gateway, data_processor, etc. |
| **dev** | hyper_red_core, adhd_mcp (MCP for development), test utilities |

### Layer from Path Algorithm

```python
def layer_from_path(module_path: Path) -> str:
    """Determine layer from physical location."""
    relative = module_path.relative_to(modules_root)
    first_part = relative.parts[0]
    
    if first_part == "foundation":
        return "foundation"
    elif first_part == "dev":
        return "dev"
    elif first_part == "runtime":
        return "runtime"
    else:
        raise ValueError(f"Unknown layer folder: {first_part}")
```

### Discovery Algorithm

```python
def discover_modules(root: Path) -> list[Module]:
    modules_dir = root / "modules"
    results = []
    
    # All 3 layers have explicit subfolders - simple and symmetric
    for layer in ("foundation", "runtime", "dev"):
        layer_dir = modules_dir / layer
        if not layer_dir.exists():
            continue
        for path in layer_dir.iterdir():
            if _is_module(path):
                results.append(Module(path, layer=layer))
    
    return results
```

---

## 📋 Metadata Schema

### `[tool.adhd]` in pyproject.toml

```toml
[tool.adhd]
name = "my_module"
version = "0.1.0"
layer = "runtime"    # REQUIRED: foundation | runtime | dev
mcp = true           # OPTIONAL: true if MCP server
```

**What Changed:**
- ❌ `type` — REMOVED (was never used consistently anyway)
- ✅ `layer` — REQUIRED (determines dependency order)
- ✅ `mcp` — NEW (explicit flag for MCP servers)

### Why `layer` is Still Required

External modules (installed from git, not in `modules/`) cannot derive layer from path. The `layer` field provides **portability**.

```toml
# External module installed elsewhere
[tool.adhd]
layer = "runtime"  # Tells framework: "I may depend on foundation"
```

---

## ✅ Acceptance Criteria

- [ ] All existing modules migrated to `modules/` structure
- [ ] `modules_controller_core` discovers modules from new paths
- [ ] No references to `type` anywhere in codebase
- [ ] `layer` correctly inferred from path for internal modules
- [ ] `[tool.adhd].layer` read for external modules
- [ ] MCP servers identifiable via `[tool.adhd].mcp = true`
- [ ] Module creator wizard uses new questions
- [ ] All 14 instruction files updated

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| modules_controller_core | internal | Must update first | Discovery logic |
| module_creator_core | internal | P1 | Wizard + templates |
| project_creator_core | internal | P2 | New project scaffolding |

---

## ⚠️ Edge Cases

| Scenario | Handling |
|----------|----------|
| External module without `layer` | Validation error with clear message |
| Module in wrong layer folder | Warning + guidance to move |
| Legacy folder exists after migration | Ignore (not scanned) |
| Nested folders in runtime | Only scan direct children |

---

## ❌ Out of Scope

- **Backward compatibility** — Internal tooling, not public API
- **Automatic migration** — Manual file moves with git assistance
- **Dependency validation** — Foundation modules importing runtime (future)

---

## ✅ Feature Validation Checklist

### Narrative Completeness
- [x] The Story section clearly states user problem and value
- [x] Intent is unambiguous to a non-technical reader
- [x] Scope is explicitly bounded

### Technical Completeness
- [x] Layer definitions are clear and testable
- [x] Discovery algorithm is specified
- [x] Edge cases are documented
- [x] Acceptance criteria are testable

### Linkage
- [x] Linked from `00_index.md`

---

**← Back to:** [Index](./00_index.md)
