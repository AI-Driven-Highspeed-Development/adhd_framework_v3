# Discussion Record: Module Management Architecture

**Date:** 2026-02-03
**Participants:** HyperSan, HyperArch, HyperDream
**Orchestrator:** HyperOrch
**Status:** Consensus Reached ✅

## Topic

How to manage modules with objectives:
1. Make every module reusable
2. Reduce magic (hidden functionality)

Pain points addressed:
- GitHub org flooding (one-repo-per-module)
- Too many modules in project, hard to focus
- Historical naming (logger_util, config_manager should be cores)
- Core exposure adds noise

## Final Consensus

### 1. Repository Strategy: Tiered Consolidation
- Monorepo for cores/foundation modules (internal infrastructure)
- Keep external-facing modules (MCPs, plugins) separate IF real consumers exist
- Consumer audit BEFORE consolidation (P3)

### 2. Naming: Gradual Migration via Aliases
- Canonical aliases in `__init__.py` + deprecation warnings
- No hard breaking changes
- New code uses clean names, old imports stay valid

### 3. Taxonomy: Layer > Type
- PRIMARY axis: `layer` (foundation/runtime/dev)
- SECONDARY axis: `type` (core/manager/util/plugin/mcp)
- Layer is the user-facing filter

### 4. Visibility: Workspace Focus Profiles
- Enhance `workspace_core` to filter by layer
- `adhd workspace --layer runtime` shows only runtime+foundation
- Workspace is a lens, not a container

### 5. Migration Order
- P1: Add `layer` field to all modules (IN PROGRESS)
- P2: Implement workspace filtering by layer
- P3: Evaluate consolidation after consumer audit

## Layer Definitions

| Layer | Definition |
|-------|------------|
| foundation | Zero ADHD dependencies, could be standalone PyPI package |
| runtime | Required for framework operation, depends on foundation |
| dev | Tooling/scaffolding only, not needed in production |

## Consumer Audit Gate (P3)

> A module has real external consumers if it's imported by ≥1 external project OR documented in public API surface.

## Key Insights from Discussion

1. **"Repo sprawl is a symptom, not the disease"** (San) — The real issue is unclear module boundaries and ad-hoc categorization
2. **"Virtual extraction is vapor until proven"** (Arch) — Must prove external consumption path before consolidation
3. **"All modules treated equally visible when they shouldn't be"** (Dream) — Visibility layers solve cognitive load without restructuring

## Related Documents

- `.agent_plan/day_dream/production_time_module_cut/04_feature_layer_taxonomy.md`
- `.agent_plan/day_dream/production_time_module_cut/06_feature_cli_migration.md`
- `.agent_plan/day_dream/uv_migration/90_federation_architecture_vision.md`

---

## Discussion Part 2: Module Type Removal (Round 1-2)

**Topic:** Should we remove the module type concept (core/manager/util/plugin/mcp) entirely?

### Positions

| Agent | Initial Position |
|-------|-----------------|
| **HyperSan** | MODIFY — Demote type to organizational hint, make layer explicit. "Manager vs util is documentation theater, not architecture." |
| **HyperArch** | Keep folders for import stability, type becomes pure metadata string. Only checked in 2 places (core layer validation, MCP scaffolding). |
| **HyperDream** | Replace with layer-first folders: foundation/, runtime/, internal/, mcps/. "Manager/util distinction is arbitrary." |

### Key Findings

1. **Manager vs Util distinction is NOT enforced** — `logger_util` has module-level state, violating "stateless pure functions"
2. **Only 3 things branch on type**: MCP file generation, workspace visibility, layer defaults
3. **~150 import rewrites** if we flatten folders (one-time cost)

### Emergent Proposal: Flat `modules/` Folder

All agents converged on: Single `modules/` folder with metadata in pyproject.toml

```
modules/
├── config_manager/
├── logger_util/
├── adhd_mcp/
└── ... (all modules flat)
```

### Final Vote (Revised Consensus)

**Proposal:**
1. Single `modules/` folder — flat structure
2. `layer` = REQUIRED — enforced for dependency ordering
3. `type` = OPTIONAL — no enforcement, used for filtering/scaffolding hints
4. `mcp` = OPTIONAL boolean — triggers MCP scaffolding
5. Clean imports via uv workspace
6. Keep naming suffixes as convention

| Agent | Vote | Concern |
|-------|------|---------|
| HyperSan | ❌ REJECT | "Flat + optional type = no reliable way to determine module type. Need REQUIRED type OR keep folders." |
| HyperArch | ✅ ACCEPT | "Layer is the right enforcement axis, not type." |
| HyperDream | ✅ ACCEPT | "Filesystem structure is rigid. Move semantics to metadata." |

### Status: Partial Consensus ⚠️

Agreed: layer REQUIRED, type not enforced, MCPs special
Disagreed: Whether `type` should be REQUIRED or OPTIONAL with flat structure

---

## Discussion Part 3: Does Tooling Really Need Type? (Round 3)

**User's Challenge:**
1. "Only cores and MCPs have actual meaning — MCPs export settings for IDE/servers"
2. "config_manager and logger_util ARE core functionality — historical naming problem"
3. "Plugin/Manager/Util have vague differences — boundaries are arbitrary"
4. "Module nature changes during agile dev — type becomes stale or redundant to update"

### Revised Positions

| Agent | Previous | Revised |
|-------|----------|---------|
| **HyperSan** | Type should be REQUIRED if flat | "I concede. `layer` + `mcp` flag is enough. Type creates debt, not prevents it." |
| **HyperArch** | Type as optional metadata | "`layer` is the meaningful axis. Type is presentation only. ~200-300 lines can be deleted." |
| **HyperDream** | Deprecate type gradually | "Minimum taxonomy: `layer` + `mcp` is sufficient. 'Is this util or manager?' debates die forever." |

### Consensus: UNANIMOUS ✅

**Remove `type` entirely. Keep only `layer` (required) and `mcp` (optional flag).**

### Final Schema

```toml
[tool.adhd]
layer = "foundation"     # REQUIRED — foundation/runtime/dev
mcp = true               # OPTIONAL, default false — triggers MCP scaffolding
# type = REMOVED
```

### Key Arguments That Changed Minds

1. **Historical debt proof**: `logger_util` and `config_manager` being misclassified proves the type system creates debt rather than preventing it

2. **Actual tooling needs**:
   - Folder placement → GONE with flat `modules/`
   - MCP scaffolding → Replaced by `mcp = true`
   - Dependency ordering → Handled by `layer`
   - Filtering → Can use layer, name patterns, or custom tags

3. **Agile reality**: Module nature changes during development. A required `type` field becomes stale or requires redundant updates.

4. **The question that killed type**: "What does tooling ACTUALLY do with `type` that can't be done with `layer` + `mcp`?" — Answer: Nothing.

### What's Lost vs Gained

| Lost | Gained |
|------|--------|
| `ls cores/` folder browsing | No more "util or manager?" debates |
| `adhd list -r manager` type filtering | Modules never need reclassification |
| Automatic folder routing | Historical naming debt becomes fixable |
| | ~200-300 lines of code deleted |
| | Simpler mental model |

### Migration Impact

- Module name suffixes (`_manager`, `_util`, `_core`, `_mcp`) stay as **human convention** — descriptive but not enforced
- All modules move to flat `modules/` folder
- `[tool.adhd].type` field removed from all pyproject.toml files
- `layer` field becomes REQUIRED
- `mcp = true` added only to MCP modules

---

## Type Removal Audit Summary (HyperSan Scan)

**Date:** 2026-02-03  
**Auditor:** HyperSan  
**Total Impact:** ~92 code locations

### Findings by Priority

#### CRITICAL (must change first)

| Component | Findings | Key Changes |
|-----------|----------|-------------|
| **modules_controller_core** | 26 | `ModuleTypeEnum` (DELETE), `ModuleTypes` class (DELETE), `ModuleFilter` TYPE dimension, `ModuleInfo.module_type`, type-layer validation, `REQUIRED_INIT_KEYS` |
| **module_creator_core** | 15 | `ModuleCreationParams.module_type` → layer+mcp, wizard "what type?" question, MCP conditional, template placeholders |
| **project_creator_core** | 15 | `MODULE_TYPE_TO_DIR` dict (DELETE), `PROJECT_DIRECTORIES`, `_extract_module_metadata()`, pyproject.toml.template |

#### HIGH (significant changes)

| Component | Findings | Key Changes |
|-----------|----------|-------------|
| **adhd_mcp + adhd_framework** | 19 | `list_modules(types=[])` param, CLI `--types` arg, `create_module(type=)`, display code |

#### MEDIUM (documentation)

| Component | Findings | Key Changes |
|-----------|----------|-------------|
| **Instruction files** | 17 | DELETE Module Types table, remove type decision tree, update naming conventions, update pyproject.toml examples |

#### SAFE (no changes needed)

- `workspace_core` — type-agnostic
- `dependency_walker.py` — uses layer only
- `exceptions_core`, `yaml_reading_core`, `github_api_core` — no type references

### Key Migration Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Folder structure | Keep existing as cosmetic | No import rewrites, gradual migration |
| ModuleTypeEnum | DELETE entirely | No semantic meaning = no enum |
| ModuleInfo.module_type | Rename to `folder` | Preserves display backward compat |
| Type-layer validation | Remove entirely | Layer is the enforcement axis |
| Filtering | Layer + MCP only | Remove `adhd list -r manager` |

### Dependency Order for Migration

```
modules_controller_core FIRST
         ↓
  ┌──────┴──────┐
  ↓             ↓
module_creator  project_creator
  ↓             ↓
  └──────┬──────┘
         ↓
    adhd_mcp
         ↓
  adhd_framework
         ↓
  Instruction files
```

### Estimated Effort

| Phase | Component | Hours |
|-------|-----------|-------|
| P2.5.1 | modules_controller_core | 4-6 |
| P2.5.2 | module_creator_core | 3-4 |
| P2.5.2 | project_creator_core | 3-4 |
| P2.5.3 | adhd_mcp + adhd_framework | 2-3 |
| P2.5.4 | Instruction files | 1-2 |
| **Total** | — | **14-20 hours** (~3 days) |

### Breaking Changes for External Consumers

| Change | Migration Path |
|--------|----------------|
| `ModuleTypeEnum` deleted | Use string literals or remove type checks |
| `ModuleInfo.module_type` removed | Use `module.layer` or `module.folder` |
| `list_modules(types=[])` removed | Use `list_modules(layers=[])` |
| CLI `--types` removed | Use `--layer` or `--mcp` |

### Implementation Blueprint

Full file-by-file migration plan: `.agent_plan/day_dream/workspace_monorepo_migration/08_type_removal_migration.md`
