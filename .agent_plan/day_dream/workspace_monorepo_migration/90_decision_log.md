# 90 - Decision Log

> Part of [Workspace Monorepo Migration Blueprint](./00_index.md)
>
> **Purpose:** Record key decisions and their rationale for future reference.

---

## 📋 Decision Record Format

Each decision follows this format:

```
### DEC-XXX: [Title]
**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded | Deprecated
**Context:** Why this decision was needed
**Decision:** What was decided
**Consequences:** What happens as a result
**Alternatives Considered:** What else was evaluated
```

---

## 🗳️ Decisions

### DEC-001: Repository Strategy — Workspace Monorepo

**Date:** 2026-02-03  
**Status:** ✅ Accepted

**Context:**
The ADHD Framework consists of 15+ modules historically designed for potential polyrepo deployment. Managing these as separate repos (or with git URL dependencies) created:
- GitHub org flooding
- Complex cross-repo dependency management  
- Inconsistent CI configurations
- Difficult atomic changes

**Decision:**
Consolidate all modules into a single **UV workspace monorepo**. Each module retains its own `pyproject.toml` for identity, but shares:
- One `uv.lock` lockfile
- One `.venv/` virtual environment
- One CI pipeline

**Consequences:**
- ✅ Simplified dependency management
- ✅ Atomic commits across modules
- ✅ Single CI configuration
- ✅ Easier onboarding (clone one repo)
- ⚠️ Lose ability to release modules independently (acceptable trade-off)
- ⚠️ Larger repo size (acceptable)

**Alternatives Considered:**

| Alternative | Why Rejected |
|-------------|--------------|
| Keep polyrepo | Too much overhead, doesn't scale |
| Federated with git URLs | UV's workspace=true vs git mutually exclusive |
| Monorepo with manual linking | UV workspace handles this better |

**References:**
- [Discussion Record](../../discussion/2026-02-03_module_management_architecture.md)
- [Federation Architecture Vision](../uv_migration/90_federation_architecture_vision.md)

---

### DEC-002: Distribution Strategy — Git-Based (Not PyPI)

**Date:** 2026-02-03  
**Status:** ✅ Accepted

**Context:**
User asked: "Can we upload PRIVATE packages to PyPI for selected users to pull?"

**Decision:**
Use **git-based dependencies** instead of PyPI for distribution.

For internal use (within monorepo):
- UV workspace handles everything

For external consumers (if needed):
- Git-based install: `git+https://github.com/org/repo.git@tag`
- No PyPI publishing required

**Consequences:**
- ✅ Zero infrastructure to maintain
- ✅ Private by default (GitHub repo permissions)
- ✅ Rapid updates (push to branch)
- ✅ Version control via git tags
- ❌ Consumers must have GitHub access
- ❌ Slightly more complex install URL

**Alternatives Considered:**

| Alternative | Why Rejected |
|-------------|--------------|
| PyPI (public) | ADHD is not a public library |
| Private PyPI (self-hosted) | Unnecessary complexity |
| AWS CodeArtifact/GCP | Cost + complexity for internal tool |
| GitHub Packages | Python support is limited |

**References:**
- [04_research_pypi_distribution.md](./04_research_pypi_distribution.md)

---

### DEC-003: Rapid Updates Strategy — Branch Tracking + Editable Installs

**Date:** 2026-02-03  
**Status:** ✅ Accepted

**Context:**
User asked: "Can we rapidly update packages like a git repo (not slow release cycles)?"

**Decision:**
Two strategies depending on context:

1. **Internal development:** Editable installs via UV workspace
   - Changes reflect immediately
   - No reinstall needed

2. **External consumers:** Git branch tracking
   - `{ git = "...", branch = "main" }` in pyproject.toml
   - Update with `uv lock --upgrade-package`

**Consequences:**
- ✅ Development changes are instant
- ✅ External consumers can track main branch
- ✅ No version bump required for updates
- ⚠️ Breaking changes can affect consumers (mitigated by good CI)

**Alternatives Considered:**

| Alternative | Why Rejected |
|-------------|--------------|
| Traditional semver releases | Too slow for internal tooling |
| Auto-versioning CI | Complexity for internal tool |
| CalVer | Same overhead as semver |

---

### DEC-004: Layer Taxonomy Preservation

**Date:** 2026-02-03  
**Status:** ✅ Accepted

**Context:**
The production_time_module_cut blueprint established a layer taxonomy (foundation/runtime/dev). Does monorepo migration affect this?

**Decision:**
**Preserve the layer taxonomy.** Monorepo structure (folders) is orthogonal to semantic layers.

- `[tool.adhd].layer` remains the source of truth
- Layer validation continues via `adhd deps --closure`
- Folder organization (cores/, managers/, etc.) is physical grouping
- Layer is semantic classification

**Consequences:**
- ✅ Existing layer work is preserved
- ✅ Can filter by layer regardless of folder
- ✅ Clear separation: physical structure vs semantic meaning

---

### DEC-005: CI Approach — Simple First

**Date:** 2026-02-03  
**Status:** ✅ Accepted

**Context:**
Two CI approaches were considered:
1. Path-filtered: Only test changed modules
2. Simple: Test everything on every change

**Decision:**
Start with **simple "run-all" approach**. Optimize to path-filtering only if CI times become a problem.

**Consequences:**
- ✅ Simpler to maintain
- ✅ Catches cross-module regressions
- ❌ Slower for small changes
- 🔄 Can optimize later if needed

**Alternatives Considered:**

| Alternative | Why Deferred |
|-------------|--------------|
| Path-filtered CI | More complex, optimize later |
| Per-module CI files | Defeats monorepo benefits |

---

### DEC-006: Package Manager — UV (Not pip/poetry/pdm)

**Date:** 2026-02-03  
**Status:** ✅ Accepted (Inherited from UV Migration)

**Context:**
Multiple Python package managers exist. Which to use for workspace monorepo?

**Decision:**
Use **UV** (already decided in UV migration). Reinforced for workspace monorepo because:
- Native workspace support
- Single lockfile
- 10-100x faster than pip
- Active development by Astral

**References:**
- [../uv_migration/05_uv_primer.md](../uv_migration/05_uv_primer.md)

---

### DEC-007: Type Removal — Replace with Layer + MCP Flag

**Date:** 2026-02-03  
**Status:** ✅ Accepted (Unanimous Consensus)

**Context:**
The module "type" system (core/manager/util/plugin/mcp) created confusion and technical debt:
- `logger_util` and `config_manager` are misclassified (both are core functionality)
- Manager vs Util distinction was never enforced anywhere
- Type creates stale metadata during agile development
- "What type is this module?" debates slow development

HyperSan audit found ~92 code locations that reference type.

**Decision:**
**Remove `type` field entirely.** Keep only:
- `layer` (REQUIRED) — foundation/runtime/dev — for dependency ordering
- `mcp` (OPTIONAL boolean) — triggers MCP scaffolding

**New Schema:**
```toml
[tool.adhd]
layer = "foundation"     # REQUIRED
mcp = true               # OPTIONAL, default false
# type = REMOVED
```

**Consequences:**
- ✅ No more "util or manager?" debates
- ✅ Historical naming debt becomes fixable
- ✅ ~200-300 lines of type-handling code deleted
- ✅ Simpler mental model
- ❌ Lose `adhd list -r manager` filtering (use layer instead)
- ❌ ~92 code locations to update

**Migration Decisions:**
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Folder structure | Keep existing as cosmetic | No import rewrites needed |
| ModuleTypeEnum | DELETE entirely | No semantic meaning = no enum |
| ModuleInfo.module_type | Rename to `folder` | Preserves display compat |
| Type-layer validation | Remove entirely | Layer is enforcement axis |

**Audit Summary:**

| Component | Findings | Priority |
|-----------|----------|----------|
| modules_controller_core | 26 | CRITICAL |
| module_creator_core | 15 | CRITICAL |
| project_creator_core | 15 | CRITICAL |
| adhd_mcp + adhd_framework | 19 | HIGH |
| Instruction files | 17 | MEDIUM |

**References:**
- [Discussion Record](../../discussion/2026-02-03_module_management_architecture.md) — Full consensus discussion
- [08_type_removal_migration.md](./08_type_removal_migration.md) — File-by-file migration plan

---

## 📝 Pending Decisions

### DEC-P01: External Consumer Support

**Status:** 🕐 Pending (P4 decision)

**Question:** Do we need to support external consumers using ADHD as a dependency?

**Options:**
1. Internal only — no external support needed
2. Git-based — document how to depend via git URL
3. PyPI — publish for easy `pip install`

**When to Decide:** P4 (if external consumers emerge)

---

### DEC-P02: Python Version Support

**Status:** 🕐 Pending

**Question:** Which Python versions should CI test?

**Options:**
1. 3.11 only (simplest)
2. 3.10, 3.11, 3.12 (matrix)
3. Latest two minor versions

**Current:** 3.11 primary, decision deferred

---

## 🔍 Decision Traceability

| Decision | Related Document | Implementation Phase |
|----------|------------------|----------------------|
| DEC-001 | [02_architecture.md](./02_architecture.md) | P1 |
| DEC-002 | [04_research_pypi_distribution.md](./04_research_pypi_distribution.md) | P4 |
| DEC-003 | [04_research_pypi_distribution.md](./04_research_pypi_distribution.md) | P4 |
| DEC-004 | [05_feature_monorepo_structure.md](./05_feature_monorepo_structure.md) | P1 |
| DEC-005 | [07_feature_ci_consolidation.md](./07_feature_ci_consolidation.md) | P3 |
| DEC-006 | [03_research_uv_workspaces.md](./03_research_uv_workspaces.md) | P0 |
| DEC-007 | [08_type_removal_migration.md](./08_type_removal_migration.md) | P2.5 |

---

**← Back to:** [Blueprint Index](./00_index.md)
