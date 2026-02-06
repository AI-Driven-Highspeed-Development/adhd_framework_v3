# 90 - Decision Log

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## Purpose

This document records all **locked decisions** for the folder structure revamp. Once a decision is locked, it should not be revisited without explicit user override.

All decisions below were made by the **user** on **2026-02-04**.

---

## 🔒 Decision 1: Remove `type` Entirely

### Status: ✅ LOCKED

### Decision
Remove the `type` field from everywhere — not just `[tool.adhd]`, but from all code, documentation, and tooling.

### Rationale

| Problem | Impact |
|---------|--------|
| `type` is subjective | "Is this a manager or a util?" — endless debates |
| `type` vs folder mismatch | Module in `managers/` could claim type="util" |
| 6 choices, no clear guidance | New contributors paralyzed by choice |
| Type was already dead code | `modules_controller.py` didn't even read it |

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Keep type as optional metadata | Still causes confusion, no clear use case |
| Rename type to "category" | Same problem with different name |
| Auto-infer type from name | Fragile heuristics, still subjective |

### Implications
- Remove `type` from all `pyproject.toml` files
- Remove type filtering from MCP/CLI
- Remove type-related issue codes
- Update all documentation

---

## 🔒 Decision 2: Symmetric Layer Folders (Option C)

### Status: ✅ LOCKED (Updated 2026-02-04)

### Decision
All three layers have **explicit subfolders**: `modules/foundation/`, `modules/runtime/`, and `modules/dev/`.

### The Structure

```
modules/
├── foundation/           # Foundation layer
│   ├── config_manager/
│   └── logger_util/
├── dev/                  # Dev layer
│   └── hyper_red_core/
└── runtime/              # Runtime layer (explicit subfolder)
    ├── my_plugin/
    ├── api_gateway/
    └── cli_manager/
```

### Rationale

| Benefit | Explanation |
|---------|-------------|
| **Scalability for 30+ modules** | This is an "empty" framework for generating actual projects. Real projects will have 30+ small modules. |
| **Reduced cognitive load at scale** | Symmetric structure means consistent mental model across all layers |
| **Simpler discovery algorithm** | No "exclude foundation/dev" logic — just scan 3 explicit folders |
| **Clearer layer identification** | Layer is always the first path component, no special cases |
| **AI-friendly** | Modules designed to be small (fit in AI context window), so many modules expected |

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Option A: Flat runtime at root | Asymmetric, requires exclusion logic, confusing at 30+ modules |
| Option B: Nested by type | Back to the same subjective debates we're solving |

### Implications
- Discovery scans 3 explicit layer folders: foundation/*, runtime/*, dev/*
- Layer inference: direct from first path component, no special cases
- All layers treated uniformly

---

## 🔒 Decision 3: `[tool.adhd].layer` Remains Required

### Status: ✅ LOCKED

### Decision
The `layer` field in `[tool.adhd]` is **required** for all modules.

### Rationale

**Problem:** External modules (installed from git, not in `modules/`) cannot derive layer from path.

**Solution:** `layer` provides **portability**.

```toml
# External module installed in some random location
[tool.adhd]
name = "external_plugin"
version = "1.0.0"
layer = "runtime"  # ← Tells framework: "I may depend on foundation"
```

### For Internal Modules

For modules inside `modules/`, the layer is **redundant** (path determines layer). However, requiring it:
1. Makes the metadata self-documenting
2. Enables validation (path vs declared layer mismatch = warning)
3. Prepares for future extraction to standalone package

### Implications
- Module creator wizard asks layer question
- Layer written to pyproject.toml
- Validation can warn if declared layer ≠ path-inferred layer

---

## 🔒 Decision 4: `[tool.adhd].mcp = true` Flag

### Status: ✅ LOCKED

### Decision
Add an explicit `mcp = true` flag to identify MCP servers.

### Rationale

| Problem | Solution |
|---------|----------|
| Previously, MCP servers lived in `mcps/` folder | With unified modules/, we lose that signal |
| MCP servers have special requirements | Need to identify them for tooling |
| Type="mcp" is gone | Need replacement mechanism |

### Schema

```toml
[tool.adhd]
name = "adhd_mcp"
version = "0.1.0"
layer = "runtime"
mcp = true           # ← NEW: Explicit MCP flag
```

### Implications
- Module creator wizard asks "Is this an MCP server?"
- `mcp = true` written for MCP servers
- Filtering can use `mcp` flag instead of type

---

## 🔒 Decision 5: No Backward Compatibility

### Status: ✅ LOCKED

### Decision
Provide **zero backward compatibility** for the old structure.

### Rationale

| Factor | Assessment |
|--------|------------|
| **Who uses this?** | Only ADHD framework developers (internal tooling) |
| **External dependencies?** | None — this is not a public API |
| **Migration cost?** | One-time, manageable |
| **Maintenance burden of compat shim?** | High — not worth it |

### What This Means
- Old folders (`cores/`, `managers/`, etc.) will be deleted
- No shim to redirect old imports
- No deprecation period
- Clean break, clean codebase

### Migration Path
1. Complete all code changes (P0-P4)
2. Physical migration (P5) in single commit
3. Update imports in one pass

---

## � Decision 6: Foundation Layer Dependency Rules

### Status: ✅ LOCKED

### Decision
Foundation modules **may depend on other foundation modules**, but must form a DAG (no circular dependencies). They NEVER import from runtime or dev layers.

### Rationale

| Old (Wrong) | New (Correct) |
|-------------|---------------|
| Foundation = "zero ADHD deps" | Foundation = "may depend on other foundation, never runtime or dev" |

**The key insight**: The layer system is about **dependency direction**, not about having zero dependencies.

```
Valid foundation dependency chain:

exceptions_core (true zero deps)
       ↓
logger_util (→ exceptions_core) 
       ↓
config_manager (→ logger_util, exceptions_core)
```

All three are foundation because:
1. None import from runtime or dev
2. They form a DAG (no cycles)
3. Removing any of them breaks modules above them in the chain

### Layer Dependency Model

| Layer | Can Import From | Production? | Removal Test |
|-------|-----------------|-------------|---------------|
| **foundation** | Foundation only | ✅ Ships | Remove → runtime and dev break |
| **runtime** | Foundation + runtime | ✅ Ships | Remove → dev breaks |
| **dev** | Anything | ❌ Stripped | Remove → nothing breaks |

### Implications
- Foundation modules are allowed to import from each other
- Circular dependencies within foundation are forbidden
- The "removal test" determines layer, not "zero deps"
- Documentation and wizard text updated accordingly

---

## 📊 Summary Table

| # | Decision | Choice | Locked |
|---|----------|--------|--------|
| 1 | Remove type | ✅ Yes, everywhere | 🔒 |
| 2 | Layer structure | ✅ Symmetric folders (Option C) | 🔒 |
| 3 | Layer required | ✅ Yes, for portability | 🔒 |
| 4 | MCP flag | ✅ `mcp = true` | 🔒 |
| 5 | Backward compat | ❌ None | 🔒 |
| 6 | Foundation deps | ✅ May depend on other foundation (DAG) | 🔒 |
| 7 | Framework vs generated projects | ✅ Foundation + dev only in framework repo | 🔒 |

---

## 🔒 Decision 7: Framework Repo = Foundation + Dev Only

### Status: ✅ LOCKED

### Decision
In the ADHD Framework repository itself, **all modules are foundation or dev**. The runtime layer is **empty** here and only populated in generated projects.

### Rationale

| Insight | Explanation |
|---------|-------------|
| **Framework = "Factory"** | ADHD Framework will never "ship" as a product. It creates projects. |
| **Infrastructure = Foundation** | cli_manager, modules_controller_core, etc. ARE the framework |
| **Dev-time tooling = Dev** | adhd_mcp (MCP for agents) and hyper_red_core (testing) are dev-only |
| **Runtime = App-specific** | Runtime modules contain business logic specific to each generated project |
| **Empty runtime is intentional** | Users add runtime modules in their projects, not in the framework source |

### The Mental Model

```
┌─────────────────────────────────────────────────────────────────┐
│  ADHD Framework Repo          │  Generated Project              │
│  (This repo)                  │  (User's project)               │
├───────────────────────────────┼─────────────────────────────────┤
│  modules/foundation/          │  modules/foundation/            │
│    ├── exceptions_core        │    ├── exceptions_core          │
│    ├── logger_util            │    ├── logger_util              │
│    ├── cli_manager            │    ├── cli_manager              │
│    └── ...                    │    └── ...                      │
│                               │                                 │
│  modules/runtime/             │  modules/runtime/               │
│    └── (empty)                │    ├── my_api_handler  ← NEW   │
│                               │    ├── data_processor  ← NEW   │
│  modules/dev/                 │    └── custom_plugin   ← NEW   │
│    ├── adhd_mcp               │                                 │
│    └── hyper_red_core         │  modules/dev/                   │
│                               │    ├── adhd_mcp                 │
│                               │    └── hyper_red_core           │
└───────────────────────────────┴─────────────────────────────────┘
```

### What This Means

| In Framework Repo | Classification | Rationale |
|-------------------|----------------|-----------|
| cli_manager | **Foundation** | Framework CLI infrastructure |
| modules_controller_core | **Foundation** | Framework's module discovery |
| project_creator_core | **Foundation** | Framework's project generation |
| instruction_core | **Foundation** | Framework's instruction management |
| adhd_mcp | **Dev** | MCP server for AI agents during development |
| hyper_red_core | **Dev** | Testing tooling |
| *(nothing)* | Runtime | Empty — users add in their projects |

### Implications
- Migration plan moves ALL framework modules to `modules/foundation/`
- `modules/runtime/` folder exists but is empty (with `.gitkeep`)
- Generated projects inherit foundation and add their own runtime modules
- Documentation clarifies the "factory" nature of this repo

---

## Future Decisions (Not Yet Locked)

These may need decisions during implementation:

| Topic | Options | Notes |
|-------|---------|-------|
| Layer dependency validation severity | Warn vs Error | Foundation importing runtime = error, runtime importing dev = warn? |
| External module discovery | Auto-scan vs Explicit registration | For modules outside `modules/` |
| Layer override | Allow `layer` to override path? | Edge case for testing |

---

**← Back to:** [Index](./00_index.md)
