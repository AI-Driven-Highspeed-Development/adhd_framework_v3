---
project: "Agent .flow Migration"
current_phase: complete
phase_name: "Full Fleet Migration"
status: DONE
last_updated: "2026-02-09"
---

# 80 - Implementation Plan

> Part of [Agent .flow Migration Blueprint](./00_index.md)

---

## 📊 Status Legend

| Icon | Status | Meaning |
|------|--------|---------|
| ⏳ | `[TODO]` | Not started |
| 🔄 | `[WIP]` | In progress |
| ✅ | `[DONE]` | Complete |
| 🚧 | `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 | `[CUT]` | Removed from scope |

---

## 📋 Phasing Overview

| Phase | Name | Duration | Difficulty | Status |
|-------|------|----------|------------|--------|
| **P0** | Infrastructure Fixes | 3-5 days | `[KNOWN]` | ✅ [DONE] |
| **P1** | First Agent (Proof-of-Concept) | 3-5 days | `[KNOWN]` | ✅ [DONE] |
| **P2** | Full Fleet Migration | 1-2 weeks | `[KNOWN]` | ✅ [DONE] |

---

## 🦴 Phase 0: Infrastructure Fixes

**Goal:** *"Fix the two compilation blockers and bootstrap the shared fragment library so agent migration can begin"*

**Duration:** 3-5 days (HARD LIMIT)

### Exit Gate

- [x] Modifying `_lib/core_philosophy.flow` and recompiling triggers recompilation of a test `.flow` that imports it
- [x] A test `.flow` file that imports a `_lib/` fragment compiles and produces output with valid YAML frontmatter
- [x] `_apply_mcp_injection_to_agents()` succeeds on a compiled file with sidecar-prepended frontmatter

### Tasks

| Status | Task | Module | Difficulty | Ref |
|--------|------|--------|------------|-----|
| ✅ | P0-1: Expose `_graph_files` via public accessor on FlowController | `flow_core` | `[KNOWN]` | [03](./03_feature_p0_infrastructure.md) |
| ✅ | P0-2: Update `_compile_flows()` to compute transitive hash from `_graph_files` | `instruction_core` | `[KNOWN]` | [03](./03_feature_p0_infrastructure.md) |
| ✅ | P0-3: Implement `_prepend_frontmatter()` method + sidecar `.yaml` support | `instruction_core` | `[KNOWN]` | [03](./03_feature_p0_infrastructure.md) |
| ✅ | P0-4: Create `_lib/` shared fragments (6 files) extracted from current agents | `instruction_core/data` | `[KNOWN]` | [03](./03_feature_p0_infrastructure.md) |
| ✅ | P0-5: Verification — transitive hash + frontmatter integration test | Both | `[KNOWN]` | [03](./03_feature_p0_infrastructure.md) |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ✅ 5 tasks (at limit)
- ✅ All `[KNOWN]`

### P0-1: Expose `_graph_files` via FlowController

**What:** Add a public method to `FlowController` that returns the set of all `.flow` files involved in the last compilation (the resolver's `_graph_files`).

**Design options:**
- (A) `FlowController.get_last_resolved_files() → Set[Path]` — post-compile accessor
- (B) `FlowController.compile_file_with_deps(path) → tuple[str, Set[Path]]` — returns deps alongside markdown

**Recommendation:** Option (A) — simpler, non-breaking, keeps `compile_file()` unchanged.

**Chosen:** Option (A).

**Implementation notes:**
- `get_last_resolved_files() → Set[Path]` returns a defensive copy of `_graph_files`
- Stored as `self._graph_files` on FlowController after each `compile_file()` call

**How to Verify (Manual):**

| What to Try | Expected Result |
|-------------|-----------------|
| Create test `.flow` importing another `.flow`, compile via `FlowController`, call `get_last_resolved_files()` | Returns set containing both files |
| Compile a `.flow` with no imports, call `get_last_resolved_files()` | Returns set containing only the entry file |

### P0-2: Update `_compile_flows()` Transitive Hash

**What:** Replace the single-file `source_sha256` with a transitive hash covering the full import closure.

**Changes to `_compile_flows()` in `instruction_controller.py`:**
1. After `controller.compile_file(flow_file)`, call `controller.get_last_resolved_files()`
2. Compute `transitive_sha256 = sha256(sorted_concatenation_of_all_file_bytes)`
3. Compare `transitive_sha256` (not `source_sha256`) against manifest for skip decision
4. Store both `source_sha256` and `transitive_sha256` in manifest entries

**Implementation notes:**
- `_compute_transitive_hash()` is a standalone method on the controller
- `_lib/` files excluded from glob discovery (they are only pulled in transitively via imports)
- Manifest entries include `transitive_sha256` + `transitive_files` (list of resolved paths)
- Backward compatible: legacy manifest entries without `transitive_sha256` trigger recompilation gracefully

**How to Verify (Manual):**

| What to Try | Expected Result |
|-------------|-----------------|
| Compile a `.flow` with `_lib/` import, modify the `_lib/` fragment, recompile with `force=False` | Agent recompiles (not skipped) |
| Compile without changes, recompile with `force=False` | Agent skipped (transitive hash unchanged) |

### P0-3: Implement `_prepend_frontmatter()`

**What:** New method in `instruction_controller.py` that merges sidecar `.yaml` metadata with compiled markdown body.

**Logic:**
1. Given `stem` (e.g., `hyper_san_checker`) and `compiled_body` (markdown string)
2. Look for `data/flows/agents/{stem}.yaml`
3. If found: `yaml.safe_load()`, then `f"---\n{yaml.dump(data, default_flow_style=None)}---\n{compiled_body}"`
4. If not found: log warning, return `compiled_body` unchanged

**Integration:** Called from `_compile_flows()` after `compile_file()` for every `.flow` in `flows/agents/`.

**YAML format constraint:** `tools:` must render as inline list `[tool1, tool2]` for MCP injection regex compatibility. Use `yaml.dump(default_flow_style=None)` which auto-selects inline for short lists.

**Implementation notes:**
- `_load_sidecar(stem) → dict | None` loads the YAML sidecar, returns `None` on missing file (graceful)
- `_prepend_frontmatter(sidecar_data, compiled_body) → str` formats the YAML frontmatter block
- `tools:` rendered in flow-style YAML (inline `[...]`) for MCP injection compatibility
- Sidecar file is included in the transitive hash — sidecar changes trigger recompilation
- Pipeline: compile `.flow` → load sidecar → prepend frontmatter → write output

**How to Verify (Manual):**

| What to Try | Expected Result |
|-------------|-----------------|
| Create `test.yaml` with `name: test\ntools: [grep_search]`, compile matching `test.flow` | Output starts with `---\nname: test\ntools: [grep_search]\n---` |
| Compile `.flow` without matching `.yaml` sidecar | Warning logged, output has no frontmatter |

### P0-4: Create `_lib/` Shared Fragments

**What:** Extract shared content from current agent files into reusable `.flow` fragments.

**Files to create:**

| File | Content Source | Approx Lines |
|------|---------------|--------------|
| `_lib/adhd/framework_info.flow` | `<ADHD_framework_information>` section from agents | ~16 |
| `_lib/patterns/core_philosophy.flow` | Truthfulness principle, Read Before Write | ~12 |
| `_lib/patterns/stopping_rules_base.flow` | Agent file edit restriction + no-edit override + persistence meta-rule | ~20 |
| `_lib/patterns/critical_rules_base.flow` | Anti-hallucination, verification, stopping rules bind | ~30 |
| `_lib/patterns/specialist_awareness.flow` | 8-agent roster table | ~24 |
| `_lib/provider/chatagent_wrapper.flow` | modeInstructions XML wrapper + self-id step 0 | ~20 |

**Implementation notes:**
- 3 subdirectories created: `patterns/` (4 fragments), `adhd/` (1 fragment), `provider/` (1 fragment)
- All 6 files are valid FLOW syntax, no `@out` nodes (pure fragments for import)
- Fragments designed as composable building blocks — agents `@import` them and wire via `@out`

**Extraction process:**
1. Read `hyper_san_checker.adhd.agent.md` (reference agent)
2. Identify each shared block
3. Create `.flow` file with `@fragment_name |<<<block content>>>|.` node definition
4. Verify fragment compiles independently: `FlowController.compile_source(fragment_source)`

**How to Verify (Manual):**

| What to Try | Expected Result |
|-------------|-----------------|
| `ls data/flows/_lib/` | Shows `adhd/`, `patterns/`, `provider/` subdirectories |
| Compile each fragment with `FlowController.compile_source()` | No errors, outputs Markdown content |

### P0-5: Verification — Integration Test

**What:** End-to-end test proving all P0 deliverables work together.

**Test scenario:**
1. Create a test agent `.flow` that imports from `_lib/`
2. Create a matching `.yaml` sidecar
3. Run `adhd refresh --full`
4. Verify compiled output has YAML frontmatter + composited body
5. Modify a `_lib/` fragment
6. Run `adhd refresh --full` again
7. Verify the agent was recompiled (not skipped)

**How to Verify (Manual):**

| What to Try | Expected Result |
|-------------|-----------------|
| Run `adhd refresh --full`, check `data/compiled/` for test agent | Complete `.adhd.agent.md` with frontmatter |
| Modify `_lib/` fragment, re-run `adhd refresh --full` | Agent recompiled (log shows "Compiled flow:" not "Skipped") |

### P0 Completion Checklist

- [x] Exit gate: `_lib/` fragment change triggers recompilation
- [x] Exit gate: compiled output has valid YAML frontmatter
- [x] Exit gate: MCP injection works on compiled output
- [x] All 5 tasks marked ✅
- [x] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [x] ≤5 tasks total ✅
- [x] Manual verification steps pass

### P0 POST-CHECK Summary

**Verified by:** HyperSan POST-CHECK | **Result:** PASS (7/7 checkpoints, 0 issues)

**Non-blocking suggestions (deferred):**
- Sidecar path `.resolve()` — cosmetic, no functional impact
- `_transitive_data` temporal coupling — minor design note, no bug risk

**All code quality checks passed. Backward compatible with existing manifests.**

### Target Folder Structure (P0)

```
data/flows/
├── _lib/                          (NEW)
│   ├── adhd/
│   │   └── framework_info.flow
│   ├── patterns/
│   │   ├── core_philosophy.flow
│   │   ├── stopping_rules_base.flow
│   │   ├── critical_rules_base.flow
│   │   └── specialist_awareness.flow
│   └── provider/
│       └── chatagent_wrapper.flow
└── instruction_sync_overview.flow  (EXISTING)
```

---

## 🏗️ Phase 1: First Agent (Proof-of-Concept)

**Goal:** *"Migrate hyper_san_checker from hand-written markdown to compiled .flow source with zero behavioral regression"*  
**Duration:** 3-5 days

### Exit Gate

- [x] `adhd refresh --full` compiles `hyper_san_checker.flow` → `compiled/agents/hyper_san_checker.adhd.agent.md`
- [x] `diff` compiled output vs hand-written original shows zero functional differences
- [x] MCP injection works on the compiled agent file
- [x] Hand-written `data/agents/hyper_san_checker.adhd.agent.md` removed *(completed as part of P2-10)*

### Tasks

| Status | Task | Module | Difficulty | Ref |
|--------|------|--------|------------|-----|
| ✅ | P1-0: Extend `instruction_controller.py` for agent compilation pipeline | `instruction_core` | `[KNOWN]` | — |
| ✅ | P1-1: Author `hyper_san_checker.flow` with `@import` from `_lib/` | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P1-2: Create `hyper_san_checker.yaml` sidecar from existing frontmatter | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P1-3: Compile + diff against hand-written original, fix until clean | Both | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P1-4: End-to-end validation — sync to `.github/`, test MCP injection, spot-check behavior | Both | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P1-5: Remove hand-written `data/agents/hyper_san_checker.adhd.agent.md` — *completed as part of P2-10* | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |

### Target Folder Structure (P1)

```
data/flows/
├── _lib/                          (FROM P0)
├── agents/                        (NEW)
│   ├── hyper_san_checker.flow
│   └── hyper_san_checker.yaml
└── instruction_sync_overview.flow  (EXISTING)

data/compiled/agents/              (NEW)
└── hyper_san_checker.adhd.agent.md

data/agents/                       (MODIFIED)
├── hyper_san_checker.adhd.agent.md → REMOVED
├── hyper_architect.adhd.agent.md   (unchanged)
└── ... (7 remaining, unchanged)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd refresh --full` | Compiles `hyper_san_checker.flow`, writes to `compiled/agents/` |
| `diff data/compiled/agents/hyper_san_checker.adhd.agent.md <(cat old_backup)` | Zero functional differences (whitespace normalization allowed) |
| Check `.github/agents/hyper_san_checker.adhd.agent.md` exists after sync | File present with frontmatter + compiled body |

### P1-0: Extend `instruction_controller.py` for Agent Compilation

**What:** The existing `_compile_flows()` method only handled flat output to `compiled/`. Agent `.flow` files live in `flows/agents/` and must compile to `compiled/agents/` with `.adhd.agent.md` extension. This task extended the compilation pipeline to be subdirectory-aware.

**Undocumented during planning** — emerged as a prerequisite when P1-1 implementation began.

**Changes:**
- `_get_output_rel_path(flow_file)` — maps `flows/agents/*.flow` → `compiled/agents/*.adhd.agent.md` (currently handles `agents/` only; needs extension for future subdirectories like `instructions/`)
- `_compile_flows()` updated to discover `flows/agents/*.flow` alongside top-level flows
- Manifest entries include subdirectory-aware output paths
- Sync routing: `compiled/agents/*.adhd.agent.md` → `.github/agents/` (via existing sync logic)

**How to Verify (Manual):**

| What to Try | Expected Result |
|-------------|------------------|
| Place a `.flow` in `flows/agents/`, run `adhd refresh --full` | Output appears in `compiled/agents/` with `.adhd.agent.md` extension |
| Check manifest after compilation | Entry has correct `output_path` under `compiled/agents/` |

### P1 Implementation Notes

**`chatagent_wrapper.flow` rewrite:**
The P0 `chatagent_wrapper.flow` was rewritten to export real template nodes (`@mode_intro_template`, `@self_id_template`) using forward references (`^agent_display_name`, `^agent_role_description`). These templates produce correct output when compiled standalone. However, they are **NOT used** in `hyper_san_checker.flow` because the compiler joins content items with `"\n"`, which inserts unwanted newlines for mid-sentence substitution (e.g., "I am **{name}**, a specialized **{role}**." would break across lines). The templates will become usable once the compiler gains a join-mode option.

**Known compiler limitation:**
The FLOW compiler's `"\n".join()` for `@out` content items prevents true inline substitution of template nodes. This is a non-blocking limitation — agents inline the wrapper content directly for now. A future `join-mode: inline` or similar compiler feature would unlock template reuse.

**`_get_output_rel_path()` scope:**
Currently only handles the `agents/` subdirectory. Will need extension for `instructions/` (P2-8) and any future flow subdirectories. Designed for easy extension via elif chain or mapping dict.

### P1 Completion Checklist

- [x] Exit gate: compiled agent matches hand-written original
- [x] Exit gate: MCP injection works
- [x] Exit gate: hand-written original removed *(completed as part of P2-10)*
- [x] All `[KNOWN]` items completed (P1-0 through P1-5)
- [x] Manual verification steps pass
- [x] Linked to [04 - Agent Migration](./04_feature_agent_migration.md)

### P1 POST-CHECK Summary

**Verified by:** HyperSan POST-CHECK | **Result:** PASS (all syntax valid, all references resolve, backward compatibility preserved)

**Non-blocking suggestions (4, all deferred):**
- Extra blank lines in compiled output (cosmetic)
- Singular wording in shared fragment (style nit)
- Bullet format for point 5 in a shared section (style nit)
- `_get_output_rel_path()` only handles `agents/` subdirectory (needs extension in P2)

**All checks passed. Differences between compiled and hand-written output are cosmetic (whitespace) or intentional (shared fragment normalization).**

---

## 📡 Phase 2: Full Fleet Migration

**Goal:** *"Migrate all remaining 7 agents + agent_common_rules + evaluate orch-skills"*  
**Duration:** 1-2 weeks

### Exit Gate

- [x] All 8 agents compile from `.flow` sources via `adhd refresh --full`
- [x] All compiled agents match hand-written originals (functional equivalence)
- [x] `data/agents/` directory is empty (all superseded by `compiled/agents/`)
- [x] `agent_common_rules.flow` compiles to `compiled/instructions/agent_common_rules.instructions.md`
- [x] Orch-skills evaluation documented (YES/NO per skill) — ✅ All 5 NO
- [x] Pass-through dispatcher operational: non-`.flow` files copied with `type: passthrough` in manifest
- [x] 4 instruction files evaluated (SOP-vs-enforcement) with conversions executed — ✅ All 4 Enforcement, no conversions needed

### Tasks

| Status | Task | Module | Difficulty | Ref |
|--------|------|--------|------------|-----|
| ✅ | P2-1: Migrate `hyper_expedition` (88 lines) | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-2: Migrate `hyper_agent_smith` (96 lines) | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-3: Migrate `hyper_iq_guard` (103 lines) | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-4: Migrate `hyper_day_dreamer` (117 lines) | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-5: Migrate `hyper_architect` (129 lines) | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-6: Migrate `hyper_red` (149 lines) | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-7: Migrate `hyper_orchestrator` (150 lines, 5 mode presets) | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-8: Migrate `agent_common_rules.instructions.md` to `.flow` | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-9: Evaluate orch-skills for migration (5 files) — **NO for all 5** (runtime-loaded, no compile-time composition benefit) | `instruction_core/data` | `[KNOWN]` | [05](./05_feature_scope_decisions.md) |
| ✅ | P2-10: Remove hand-written `data/agents/` originals | `instruction_core/data` | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-11: Full fleet validation — all 8 agents compiled, synced, MCP injected | Both | `[KNOWN]` | [04](./04_feature_agent_migration.md) |
| ✅ | P2-12: Implement pass-through dispatcher in `instruction_controller` | `instruction_core` | `[KNOWN]` | [05 — Decision 2](./05_feature_scope_decisions.md#custom--architectural-scope-decisions) |
| ✅ | P2-13: Add `type: compiled` vs `type: passthrough` to manifest schema | `instruction_core` | `[KNOWN]` | [05 — Decision 2](./05_feature_scope_decisions.md#custom--architectural-scope-decisions) |
| ✅ | P2-14: Evaluate 4 instruction files SOP-vs-enforcement — **All 4 Enforcement** (keep as instructions, no conversions) | `instruction_core/data` | `[KNOWN]` | [05 — Decision 3](./05_feature_scope_decisions.md#custom--architectural-scope-decisions) |
| ✅ | P2-15: Execute instruction→skill conversions per evaluation results — **No conversions needed** (all 4 are enforcement) | `instruction_core/data` | `[KNOWN]` | [05 — Decision 3](./05_feature_scope_decisions.md#custom--architectural-scope-decisions) |

### Target Folder Structure (P2)

```
data/flows/
├── _lib/                          (FROM P0 — may grow)
├── agents/                        (8 agents, FROM P1+P2)
│   ├── hyper_san_checker.flow + .yaml
│   ├── hyper_expedition.flow + .yaml
│   ├── hyper_agent_smith.flow + .yaml
│   ├── hyper_iq_guard.flow + .yaml
│   ├── hyper_day_dreamer.flow + .yaml
│   ├── hyper_architect.flow + .yaml
│   ├── hyper_red.flow + .yaml
│   └── hyper_orchestrator.flow + .yaml
├── instructions/                  (NEW)
│   └── agent_common_rules.flow
└── instruction_sync_overview.flow  (EXISTING)

data/compiled/agents/              (8 compiled agents)
├── hyper_san_checker.adhd.agent.md
├── hyper_expedition.adhd.agent.md
├── hyper_agent_smith.adhd.agent.md
├── hyper_iq_guard.adhd.agent.md
├── hyper_day_dreamer.adhd.agent.md
├── hyper_architect.adhd.agent.md
├── hyper_red.adhd.agent.md
└── hyper_orchestrator.adhd.agent.md

data/compiled/instructions/        (NEW)
└── agent_common_rules.instructions.md

data/agents/                       (EMPTY — all removed)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd refresh --full` | 8 agents + 1 instruction compiled, 0 errors |
| `ls data/agents/` | Empty directory (all superseded) |
| `ls .github/agents/` | 8 compiled agents synced |
| Place a non-`.flow` file in the flows directory, run refresh | File is copied (passthrough), manifest entry has `type: passthrough` |
| Place a `.flow` file, run refresh | File is compiled, manifest entry has `type: compiled` |

### P2 Implementation Notes

**`_lib/` fragment reuse patterns:**
All 8 agents share fragments from `_lib/`. The most reused fragments are `core_philosophy.flow`, `stopping_rules_base.flow`, `critical_rules_base.flow`, and `framework_info.flow`. The `specialist_awareness.flow` fragment has two variants: `specialist_table_implementer` (used by most agents) and `specialist_table_full` (used by `hyper_orchestrator`). Each agent `.flow` file `@import`s its needed fragments and wires them into `@out`.

**`chatagent_wrapper.flow` still not usable:**
The P0/P1 known compiler limitation persists — `"\n".join()` for `@out` content items prevents inline substitution of template nodes. All agents continue to inline the wrapper content directly. A future `join-mode: inline` compiler feature would unlock template reuse.

**All evaluations resulted in "no migration":**
Final migration scope = 9 files (8 agents + 1 instruction `agent_common_rules`). All 5 orch-skills evaluated as NO (runtime-loaded, no compile-time composition benefit). All 4 instruction files evaluated as Enforcement (keep as `.instructions.md`, no skill conversion). The `.flow` system's value is compile-time composition; runtime-loaded files and enforcement-pattern files gain nothing from it.

**No code changes needed for sync pipeline:**
The existing sync pipeline already reads from `compiled/` output. Agent removal from `data/agents/` required zero sync logic changes — the pipeline transparently picks up compiled agents from `compiled/agents/`.

**Stale comments in `.flow` files:**
Some `.flow` files contain references to `data/agents/` in inline comments. These are cosmetic, non-blocking, and do not affect compilation or output. Can be cleaned up in a future housekeeping pass.

**Pass-through dispatcher:**
Non-`.flow` files in `flows/` are copied to `compiled/` preserving relative path. Excludes `_lib/` fragments and sidecar `.yaml` files. Manifest entries distinguish `"type": "compiled"` (`.flow` sources) from `"type": "passthrough"` (copied as-is).

**`_get_output_rel_path()` extension:**
Extended with `instructions/` branch (P2-8) to map `flows/instructions/*.flow` → `compiled/instructions/*.instructions.md`, completing the pattern started in P1-0 for `agents/`.

### P2 POST-CHECK Summary

**Verified by:** Full fleet validation (P2-11) | **Result:** PASS (29/29 checkpoints, 0 issues)

**Validation scope:**
- All 8 agents compile from `.flow` sources without errors
- All compiled agents functionally equivalent to hand-written originals
- `agent_common_rules.flow` compiles to `compiled/instructions/agent_common_rules.instructions.md`
- MCP injection works on all compiled agent files
- Sync pipeline correctly routes compiled output to `.github/agents/` and `.github/instructions/`
- Pass-through dispatcher copies non-`.flow` files with `type: passthrough` manifest entries
- `data/agents/` and `data/instructions/agents/` emptied of hand-written originals

**Non-blocking observations (all deferred):**
- Stale `data/agents/` references in `.flow` inline comments (cosmetic)
- `chatagent_wrapper.flow` templates remain unused pending compiler join-mode feature

**All P2 exit gates passed. Migration complete.**

### P2 Completion Checklist

- [x] All 8 agents compile from `.flow` sources
- [x] All compiled agents match originals (functional equivalence)
- [x] `agent_common_rules.flow` compiles correctly
- [x] Orch-skills evaluation documented
- [x] Pass-through dispatcher working (if `.flow` → compile, else → copy)
- [x] Manifest entries include `type: compiled` vs `type: passthrough`
- [x] 4 instruction files SOP-vs-enforcement evaluation complete
- [x] Instruction→skill conversions executed per evaluation
- [x] `data/agents/` emptied
- [x] Manual verification steps pass

---

## ⚠️ Error Handling Implementation

### Error Types

| Error Class | When Raised | Recovery |
|-------------|-------------|----------|
| `FlowError` (from flow_core) | Syntax/resolution error in `.flow` file | Log warning, skip that agent, continue |
| `yaml.YAMLError` | Malformed sidecar `.yaml` | Log error, compile without frontmatter |
| `FileNotFoundError` | Missing sidecar `.yaml` | Log warning, compile without frontmatter |
| `OSError` | File I/O failure | Log error, skip that file |

### Logging Requirements

| Level | When | Example |
|-------|------|---------|
| ERROR | Sidecar YAML parse failure | `"Failed to parse frontmatter YAML for hyper_san: {error}"` |
| WARNING | Missing sidecar, flow compile failure | `"No sidecar .yaml found for hyper_san, skipping frontmatter"` |
| INFO | Successful compilation, skip (unchanged) | `"Compiled flow: hyper_san_checker.flow"` |
| DEBUG | Hash comparison, file discovery | `"Transitive hash unchanged, skipping: hyper_san_checker.flow"` |

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-09 | Sidecar `.yaml` for frontmatter (not embedded in `.flow`) | Keeps flow_core as pure Markdown emitter. Separation of concerns. | Multi-agent discussion |
| 2026-02-09 | Accessor pattern for `_graph_files` (not return value) | Non-breaking change to `compile_file()` API. Simpler adoption. | Multi-agent discussion |
| 2026-02-09 | Migration order smallest→largest | Build experience on simpler agents. Reduce risk. | Multi-agent discussion |
| 2026-02-09 | 9 files migrate, 21 don't | Composition benefit criteria: only files with shared content blocks. | Multi-agent discussion |
| 2026-02-09 | Orch-skills deferred to P2 evaluation | Not enough data to decide now. P1 learnings will inform. | Multi-agent discussion |
| 2026-02-09 | REJECT raw-text `+` import syntax | Sidecar approach is the correct boundary. flow_core stays pure. Re-evaluate only if a second non-flow format demands inclusion. | Multi-agent discussion (Decision 1) |
| 2026-02-09 | ACCEPT pass-through dispatcher at instruction_controller level (P2) | Thin dispatcher (if `.flow` → compile, else → copy). Manifest adds `type: compiled` vs `type: passthrough`. Lives in instruction_controller, NOT flow_core. | Multi-agent discussion (Decision 2) |
| 2026-02-09 | ACCEPT hybrid instructions→skills evaluation (P2) | Per-file SOP-vs-enforcement evaluation of 4 instruction files. `applyTo` auto-enforcement has no skills equivalent; wholesale removal is a regression. | Multi-agent discussion (Decision 3) |
| 2026-02-09 | Sidecar included in transitive hash | Sidecar `.yaml` changes trigger recompilation. Prevents stale frontmatter in compiled output. | P0 implementation |
| 2026-02-09 | `chatagent_wrapper` templates not used in P1 agent | Compiler `"\n".join()` inserts unwanted newlines for mid-sentence substitution. Templates exist and work standalone but produce broken output when inlined. Revisit when compiler gains join-mode option. | P1 implementation |
| 2026-02-09 | P1-5 (remove hand-written original) deferred | User validation of compiled output required before deleting the hand-written source of truth. Risk mitigation — no data loss before sign-off. | P1 implementation |
| 2026-02-09 | P1-0 added retroactively (agent pipeline extension) | `instruction_controller.py` needed subdirectory-aware compilation (`agents/` → `compiled/agents/` with `.adhd.agent.md` extension). Not anticipated during planning; emerged as prerequisite. | P1 implementation |
| 2026-02-09 | All 5 orch-skills: NO migration | Runtime-loaded via skills system, no compile-time composition benefit. `.flow` = compile-time composition; skills = runtime loading at usage-time. | P2 implementation |
| 2026-02-09 | All 4 instruction files: Enforcement (no conversion) | All use `applyTo` for auto-enforcement. Converting to skills would lose auto-loading. No composition value. | P2 implementation |
| 2026-02-09 | P1-5 completed as part of P2-10 | All hand-written originals (8 agents + `agent_common_rules.instructions.md`) removed in a single batch after full fleet validation passed. | P2 implementation |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| `_lib/templates/adhd_agent.flow` master skeleton | 2026-02-09 | Agents compose fragments directly. Skeleton adds a layer of indirection without proven benefit. Reconsider if patterns emerge in P2. |
| Raw-text `+` import syntax for non-.flow files | 2026-02-09 | Decision 1: sidecar approach is the correct boundary. flow_core stays pure. |
| Standalone instruction migration (9 files) | 2026-02-09 | Zero composition value — standalone reference docs. (4 files now CONDITIONAL for SOP→skill conversion per Decision 3.) |
| Prompt migration (3 files) | 2026-02-09 | Static, short, no sharing. |
| Standalone skill migration (4 files) | 2026-02-09 | Prose documentation, no composition. |

---

## 🔬 Exploration Log

| Date | Topic | Status | Synthesized To |
|------|-------|--------|----------------|
| 2026-02-09 | Agent shared content analysis | SYNTHESIZED | [01](./01_executive_summary.md), [03](./03_feature_p0_infrastructure.md) |
| 2026-02-09 | `_lib/` topology design | SYNTHESIZED | [02](./02_architecture.md) |
| 2026-02-09 | Scope decision matrix | SYNTHESIZED | [05](./05_feature_scope_decisions.md) |

---

**← Back to:** [Index](./00_index.md)
