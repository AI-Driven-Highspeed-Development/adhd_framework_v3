# 80 - Implementation Plan

> Part of [Instruction Compiler Pipeline Blueprint](./00_index.md)

---

## 📋 Phasing Overview

| Phase | Name | Duration | Difficulty | Status |
|-------|------|----------|------------|--------|
| **P0** | Walking Skeleton — Fix & Cleanse | 3–5 days | `[KNOWN]` | ✅ [DONE] 2026-02-08 |
| **P1** | First Enhancement — Compilation Pipeline | 1–2 weeks | `[KNOWN]` | ⏳ [TODO] |
| **P2** | Polish — Manifest, Skills Sync, CI | 1–2 weeks | `[EXPERIMENTAL]` | ⏳ [TODO] |

---

## P0 — Walking Skeleton: Fix & Cleanse

> **Goal:** Every instruction file is v3-compliant. The broken path is fixed. `adhd refresh --full` actually works. Zero `cores/` references remain.
>
> **Status: ✅ COMPLETED 2026-02-08** — 18 files modified, 9 files created (`refresh_full.py` + 8 `SKILL.md`), 2 files deleted (`refresh.py` + orphan instruction).

### P0 Task List

| # | Task | Feature | Difficulty | Status |
|---|------|---------|------------|--------|
| P0-1 | Fix `instruction_controller.py` broken path | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ✅ [DONE] |
| P0-2 | Git tag `pre-instruction-pipeline-v0` | [03](./03_feature_v3_format_fix.md) | `[KNOWN]` | ✅ [DONE] |
| P0-3 | Batch-fix v2 contamination (17 data files) | [03](./03_feature_v3_format_fix.md) | `[KNOWN]` | ✅ [DONE] |
| P0-4 | Update agent format spec (`argument-hint`, `handoffs`, `send`) | [03](./03_feature_v3_format_fix.md) | `[KNOWN]` | ✅ [DONE] |
| P0-5 | Verification pass — grep audit, refresh test | [03](./03_feature_v3_format_fix.md) | `[KNOWN]` | ✅ [DONE] |
| P0-6 | `refresh.py` → `refresh_full.py` (full-only sync) | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ✅ [DONE] |
| P0-7 | Delete orphan `.github/instructions/modules.init.yaml.instructions.md` | [03](./03_feature_v3_format_fix.md) | `[KNOWN]` | ✅ [DONE] |
| P0-8 | Create 8 SKILL.md files in `data/skills/` | [04](./04_feature_skills_adoption.md) | `[KNOWN]` | ✅ [DONE] |

### P0-1: Fix `instruction_controller.py` Broken Path

**What:** Change line 47 from dead `cores/` path to `__file__`-relative:

| Line | Before | After |
|------|--------|-------|
| 47 | `self.official_source_path = self.root_path / "cores" / "instruction_core" / "data"` | `self.official_source_path = Path(__file__).resolve().parent / "data"` |

**Why:** This is THE critical bug. The entire official sync silently no-ops because `_sync_data_to_target()` checks `if not source_path.exists(): return`. With `cores/` gone, the condition is always true.

**How to Verify (Manual):**

1. Run: `python -c "from pathlib import Path; p = Path('/home/stellar/PublicRepo/ADHD-Framework/adhd_framework_v3/modules/dev/instruction_core/instruction_controller.py'); lines = p.read_text().splitlines(); print(lines[46])"`
2. Confirm output contains `Path(__file__)` not `cores/`
3. Run `adhd refresh --full` and confirm `.github/instructions/` gets updated files

### P0-2: Write v3 Compliance Reference Doc

**What:** Create a reference document (in `.agent_plan/day_dream/` or similar) listing the correct v3 patterns that all data files must follow:

| Topic | Correct v3 Pattern |
|-------|--------------------|
| Module discovery | `pyproject.toml` with `[tool.adhd]` section |
| Dependencies | `[project].dependencies = ["flow-core"]` (hyphens, package name) |
| Workspace resolution | `[tool.uv.sources] flow-core = { workspace = true }` |
| Imports | `from flow_core import FlowController` (package import) |
| Path references | Module-relative: `Path(__file__).parent / "data"` |
| Project structure | `modules/{foundation,runtime,dev}/module_name/` |
| Instruction frontmatter | `applyTo: "modules/**/*.py"` |
| Agent frontmatter | `name`, `description`, `argument-hint`, `tools`, `handoffs` |
| Skill format | `.github/skills/{name}/SKILL.md` with YAML frontmatter |

| Dead v2 Pattern | Note |
|-----------------|------|
| `init.yaml` | Never existed in v3. Discovery is pyproject.toml only. |
| `cores/` directory | Renamed to `modules/dev/` during v3 migration. |
| `sys.path.insert(0, project_root)` | Dead. uv editable installs handle resolution. |
| `pip install` | Dead. `uv sync` only. |
| `requirements.txt` | Dead for framework modules (pyproject.toml dependencies only). |
| `modules.init.yaml.instructions.md` | File doesn't exist. Dead reference. |

**How to Verify (Manual):**

1. Confirm file exists and contains all patterns above
2. Cross-reference with `instruction_core/pyproject.toml` (real v3 example)

### P0-3: Batch-Fix All ~37 Contaminated Data Files

**What:** Fix all three contamination layers across all data files.

**Scope (from [03 audit matrix](./03_feature_v3_format_fix.md)):**

| Layer | Count | Example Fix |
|-------|-------|-------------|
| L1: Dead `cores/` path refs | ~20 | `cores/instruction_core/data/` → `modules/dev/instruction_core/data/` |
| L2: Dead tooling refs | ~10 | References to `init.yaml`, `requirements.txt`, `pip install` |
| L3: Structural vocabulary | ~7 | `adhd_framework_context.instructions.md` folder taxonomy teaches `cores/` |

**Confirmed files requiring edits (from grep):**

| File | Layer | Line(s) | Fix Required |
|------|-------|---------|-------------|
| `expedition_schemas.instructions.md` | L1 | 2, 136 | `applyTo:` path + body reference |
| `hyper_exped_reference.instructions.md` | L1 | 2, 82 | `applyTo:` path + body reference |
| `adhd_framework_context.instructions.md` | L1+L3 | 100+ | `Source:` line + folder taxonomy section |
| `instructions_format.instructions.md` | L1 | 57 | Body reference |
| `prompts_format.instructions.md` | L1 | 51 | Body reference |
| `orch_routing_preset.instructions.md` | L1 | 69 | Body reference |
| `update_requirements.prompt.md` | L2 | 53 | Dead ref to `modules.init.yaml.instructions.md` |
| *All agent files (8)* | L2 (if any) | Varies | Check for init.yaml, cores/ refs |
| *All instruction files (21)* | L1-L3 | Varies | Full audit needed per file |
| *All prompt files (3)* | L1-L2 | Varies | Full audit needed per file |

**How to Verify (Manual):**

1. Run: `grep -rn "cores/" modules/dev/instruction_core/data/`
2. Expected output: **zero matches**
3. Run: `grep -rn "init\.yaml" modules/dev/instruction_core/data/`
4. Expected output: **zero matches** (unless in a template documenting what NOT to do)
5. Run: `grep -rn "requirements\.txt" modules/dev/instruction_core/data/`
6. Expected output: **zero matches** in instruction/agent files (may appear in migration docs)

### P0-4: Update Agent Format Spec

**What:** Ensure all 8 agent files in `data/agents/` use the correct v3 YAML frontmatter format:

```yaml
---
name: hyper_san_checker
description: "Sanity checker agent"
argument-hint: "task description"
tools:
  - grep_search
  - read_file
  - semantic_search
handoffs:
  - label: "Escalate to Architect"
    agent: hyper_architect
    prompt: "Review this finding"
    send: auto
---
```

**Key corrections:**
- `handoffs` is an array of objects with `label`, `agent`, `prompt`, `send` (not a simple list)
- `tools` is an array of tool identifiers (not wrapped objects)
- `argument-hint` uses hyphen (not underscore)
- No `model:` field (handled externally)

**How to Verify (Manual):**

1. Run: `head -20 modules/dev/instruction_core/data/agents/hyper_san_checker.adhd.agent.md`
2. Confirm frontmatter matches format above
3. Repeat for all 8 agent files

### P0-5: Verification Pass — Grep Audit, Refresh Test

**What:** Final verification sweep confirming zero contamination remains.

**Audit commands:**

```bash
# Layer 1: No cores/ references in data files
grep -rn "cores/" modules/dev/instruction_core/data/
# Expected: 0 matches

# Layer 1: No cores/ references in controller
grep -n "cores/" modules/dev/instruction_core/instruction_controller.py
# Expected: 0 matches

# Layer 2: No init.yaml references
grep -rn "init\.yaml" modules/dev/instruction_core/
# Expected: 0 matches (only in pyproject.toml if any)

# Layer 2: No sys.path.insert
grep -rn "sys\.path\.insert" modules/dev/instruction_core/
# Expected: 0 matches

# Layer 2: No dead module refs
grep -rn "modules\.init\.yaml\.instructions\.md" modules/dev/instruction_core/data/
# Expected: 0 matches

# Functional test: refresh works
adhd refresh --full
# Expected: .github/ updated with current files, no errors
```

**How to Verify (Manual):**

1. Run all grep commands above from project root
2. Confirm each returns 0 matches
3. Run `adhd refresh --full` and confirm no errors
4. Spot-check 3 random files in `.github/instructions/` — confirm contents match `data/instructions/` source

---

## P1 — First Enhancement: Compilation Pipeline

> **Goal:** `adhd refresh --full` compiles `.flow` files via flow_core, generates a manifest, and syncs with merge priority. Skills sync to `.github/skills/`.

### P1 Task List

| # | Task | Feature | Difficulty | Status |
|---|------|---------|------------|--------|
| P1-1 | Add flow-core dependency to instruction_core's pyproject.toml | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-2 | Implement `_compile_flows()` method | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-3 | Implement `_generate_manifest()` method | [05](./05_feature_flow_compilation_pipeline.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-4 | Implement `_write_compiled_output()` method | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-5 | Update `run()` to integrate compile→manifest→write→sync | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-6 | Implement merge priority in `_sync_data_to_target()` | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-7 | Implement `_sync_skills()` method | [04](./04_feature_skills_adoption.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-8 | Create first `.flow` source file (proof of concept) | [05](./05_feature_flow_compilation_pipeline.md) | `[KNOWN]` | ⏳ [TODO] |
| P1-9 | End-to-end test: `.flow` → `compiled/` → `.github/` | All | `[KNOWN]` | ⏳ [TODO] |

### P1-1: Add flow-core Dependency

**What:** Update `modules/dev/instruction_core/pyproject.toml`:

**Current `[project].dependencies`:**
```toml
dependencies = [
    "exceptions-core",
    "modules-controller-core",
    "logger-util",
    "config-manager",
    "pyyaml",
]
```

**Updated:**
```toml
dependencies = [
    "exceptions-core",
    "modules-controller-core",
    "logger-util",
    "config-manager",
    "pyyaml",
    "flow-core",
]

[tool.uv.sources]
exceptions-core = { workspace = true }
modules-controller-core = { workspace = true }
logger-util = { workspace = true }
config-manager = { workspace = true }
flow-core = { workspace = true }
```

**NOT required:** init.yaml, requirements.txt, GitHub URLs, pip install commands.

**How to Verify (Manual):**

1. Run: `grep "flow-core" modules/dev/instruction_core/pyproject.toml`
2. Expected: matches in both `[project].dependencies` and `[tool.uv.sources]`
3. Run: `uv sync` from project root — confirm no resolution errors

### P1-5: Update `run()` Pipeline

**What:** Modify `InstructionController.run()` to:

```
1. (existing) _sync_agent_plan()
2. (NEW)     _compile_flows()         — only if data/flows/ or skills/**/*.flow exists
3. (NEW)     _generate_manifest()     — from compiled entries
4. (NEW)     _write_compiled_output() — to data/compiled/
5. (existing) _sync_data_to_target()  — ENHANCED with merge priority
6. (NEW)     _sync_skills()           — only if data/skills/ exists (static copy + compiled)
7. (existing) _sync_module_files()
8. (existing) _apply_mcp_injection()
```

**Trigger:** Runs via `refresh_full.py` on `adhd refresh --full` only. Instruction sync does not happen on plain `adhd refresh`.

**Backward compatibility:** If `data/flows/` doesn't exist (i.e., no `.flow` files authored yet), steps 2-4 are skipped entirely. The controller degrades to its current (path-fixed) behavior.

**How to Verify (Manual):**

1. With no `data/flows/` dir: run `adhd refresh --full` — works exactly like P0
2. Create `data/flows/test.flow` with minimal content
3. Run `adhd refresh --full` — confirms `data/compiled/test.md` is created
4. Confirm `compiled_manifest.json` exists in `data/compiled/`
5. Confirm `.github/` has the compiled file (merged with static files)

---

## P2 — Polish: Manifest UI, CI Integration, Skills Workflow

> **Goal:** Production polish. CI gates on compilation success. Manifest accessible via MCP. Skills discoverable by VS Code.

### P2 Task List

| # | Task | Feature | Difficulty | Status |
|---|------|---------|------------|--------|
| P2-1 | Expose `compile_only()` method for CI | [06](./06_feature_instruction_core_refactor.md) | `[KNOWN]` | ⏳ [TODO] |
| P2-2 | CLI `adhd compile` subcommand | — | `[KNOWN]` | ⏳ [TODO] |
| P2-3 | MCP tool to query manifest | — | `[EXPERIMENTAL]` | ⏳ [TODO] |
| P2-4 | Skills discovery for Agent Skills panel | [04](./04_feature_skills_adoption.md) | `[EXPERIMENTAL]` | ⏳ [TODO] |
| P2-5 | Incremental compilation (hash comparison) | — | `[EXPERIMENTAL]` | ⏳ [TODO] |

---

## 📊 Decisions Log

| Decision | Rationale | Date | Alternatives Considered |
|----------|-----------|------|------------------------|
| Path fix uses `Path(__file__).resolve().parent / "data"` | Survives directory renames and relocations. Module-relative is idiomatic Python. `__file__` is always available for installed packages. | 2025-01 | `importlib.resources` (too heavy for simple path), config key (another moving part) || Instruction sync via `refresh_full.py` only (`adhd refresh --full`) | Instruction files don't change often. Bundling compile + sync in `refresh_full.py` ensures no stale compiled files get synced. Module has NO `refresh.py`. | 2026-02-08 | `refresh.py` (runs on every `adhd refresh` — wasteful), separate compile + sync commands (extra complexity) |
| Creator templates not updated | `.github/` structure (instructions, agents, prompts, skills) is managed by `instruction_core`'s sync pipeline, not by project/module scaffolding. `project_creator_core`, `module_creator_core`, and `creator_common_core` are out of scope. | 2026-02-08 | Update creator templates (wrong — would create coupling) || Dependencies via `pyproject.toml` only | v3 architecture uses `[project].dependencies` + `[tool.uv.sources]`. No `init.yaml` in v3. No `requirements.txt` for framework modules. | 2025-01 | init.yaml (dead in v3), requirements.txt (dead for framework modules) |
| Compilation opt-in via `flows/` directory existence | Zero-config. No feature flags to forget. If `data/flows/` doesn't exist, skip compilation. Simplest possible backward compatibility. | 2025-01 | Config flag (another knob), always-compile (breaks when no flows) |
| Merge priority: compiled > static > per-module | Compiled output is the authoritative version. Static files are handwritten fallbacks. Per-module files are locally scoped. | 2025-01 | Timestamp-based (non-deterministic), error-on-collision (too strict) |
| P0 is cleansing only (no new features) | The path is broken. Nothing else matters until official sync works and contamination is gone. Adding features on a broken foundation wastes effort. | 2025-01 | Combined fix+feature (too much risk for P0) |
| Verification via grep commands (not unit tests) | P0 changes are ~37 find-and-replace edits in markdown files + 1 line change in Python. Grep is the correct verification tool. Unit tests for markdown content are over-engineering. | 2025-01 | Unit tests (wrong abstraction level), CI linter (build it later in P2) |
| P0-2 became git tag, not doc | Original plan was a v3 compliance reference doc. Replaced with `pre-instruction-pipeline-v0` git tag — captures the known-good state before changes. The compliance patterns are already documented in `adhd_framework_context.instructions.md`. | 2026-02-08 | Write separate doc (redundant with existing instructions) |
| 17 files fixed, not ~37 | Actual contamination count was 17 (4 agents, 10 instructions, 3 prompts). Original estimate of ~37 was conservative upper bound. | 2026-02-08 | — |
| Skills folders created in P0 | Originally P1 scope, but creating static `SKILL.md` stubs is trivial and establishes the `data/skills/` directory structure needed for P1 compilation. 8 skills: expedition, day-dream, testing, orch-discussion, orch-implementation, orch-testing, orch-routing, orch-expedition. | 2026-02-08 | Defer to P1 (delays skills adoption for no benefit) |
| Orphan `.github/instructions/modules.init.yaml.instructions.md` deleted | File was synced from a source that no longer exists. Dead reference to v2 `init.yaml` concept. Confirmed not re-created by `adhd refresh --full`. | 2026-02-08 | Leave orphan (confuses agents), add to `.gitignore` (wrong layer) |
| `refresh.py` removed, `refresh_full.py` only | Module has no `refresh.py` — instruction sync runs exclusively on `adhd refresh --full`. Prevents wasteful re-sync on every `adhd refresh`. Docstring + L46 comment also fixed. | 2026-02-08 | Keep `refresh.py` (too frequent), add config flag (over-engineering) |

---

## 📊 Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Flow compilation introduces breaking changes to agent behavior | 🔥 High | Medium | P1-8 starts with ONE proof-of-concept `.flow` file. Diff compiled output against existing manual file before replacing. |
| Merge priority causes silent overwrites | 🔥 Medium | Low | `compiled_manifest.json` tracks every override. Review manifest after each refresh. |
| `Path(__file__)` doesn't work in some edge case (frozen binary, zip import) | 🔥 High | Very Low | We don't support frozen/zip deployment. uv always installs as editable. Non-issue for our use case. |
| batch-fix (P0-3) introduces typos in 37 files | 🔥 Medium | Medium | Grep verification pass (P0-5) catches misses. `git diff` review before commit. |
| `flow_core` API changes between P0 and P1 | 🔥 Low | Low | `FlowController.compile_file()` is already stable. Pin to current interface. |

---

## 🚪 Exit Gate

### P0 Exit Gate

**All must pass before P0 is complete:**

- [x] `grep -rn "cores/" modules/dev/instruction_core/` returns **0 matches** ✅
- [x] `grep -rn "init\.yaml" modules/dev/instruction_core/` returns **0 matches** ✅
- [x] `grep -rn "sys\.path\.insert" modules/dev/instruction_core/` returns **0 matches** ✅
- [x] `grep -rn "modules\.init\.yaml" modules/dev/instruction_core/data/` returns **0 matches** ✅
- [x] `instruction_controller.py` line 47 uses `Path(__file__).resolve().parent / "data"` ✅
- [x] `adhd refresh --full` runs without error ✅
- [x] `.github/instructions/` contains fresher-than-before copies of data files ✅
- [x] `git diff --stat` shows all contaminated files changed, nothing unexpected ✅

**P0 completed: 2026-02-08** — Verified by HyperSan (all 7 checks green)

### P1 Exit Gate

**All must pass before P1 is complete:**

- [ ] `pyproject.toml` lists `flow-core` in `[project].dependencies` and `[tool.uv.sources]`
- [ ] `uv sync` resolves without errors
- [ ] A proof-of-concept `.flow` file compiles via `adhd refresh --full`
- [ ] `data/compiled/` contains compiled output files
- [ ] `compiled_manifest.json` is valid JSON with SHA-256 hashes
- [ ] `.github/` contains compiled files (merged with static)
- [ ] `adhd refresh --full` with no `data/flows/` still works (backward compat)
- [ ] `.github/skills/` populated with 8 skill folders (if skills exist)

### P2 Exit Gate

- [ ] `adhd compile` CLI subcommand works standalone
- [ ] CI passes compilation gate
- [ ] Incremental compilation skips unchanged files

---

## 🖼️ Related Assets

| Asset | Description |
|-------|-------------|
| (None yet) | Assets will be created as P1 design solidifies |

---

**← Back to:** [Index](./00_index.md)

