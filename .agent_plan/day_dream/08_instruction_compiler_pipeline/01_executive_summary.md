# 01 - Executive Summary

> Part of [Instruction Compiler Pipeline Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌──────────────────────────────────────────────────────────────────────┐
│                   THE SILENTLY BROKEN PIPELINE                       │
│                                                                      │
│  instruction_controller.py line 47:                                  │
│    self.official_source_path = root / "cores" / "instruction_core"   │
│                                       ^^^^^^                         │
│    💥 "cores/" DOES NOT EXIST — renamed to modules/dev/ long ago     │
│    💥 Official sync SILENTLY NO-OPS (path doesn't exist → skips)     │
│    💥 .github/ files are STALE — synced before migration, never      │
│       updated since                                                  │
│                                                                      │
│  CONTAMINATION IN 37 DATA FILES:                                     │
│  Layer 1: 20+ "cores/instruction_core/" path references (dead)       │
│  Layer 2: Files mandate init.yaml, pip install, sys.path.insert      │
│           (all dead v2 tooling — v3 uses pyproject.toml, uv,         │
│            package imports)                                          │
│  Layer 3: adhd_framework_context.instructions.md teaches agents      │
│           that "cores/" is a valid directory — agents build a        │
│           mental model of a project that doesn't exist               │
│                                                                      │
│  Net effect: EVERY AI AGENT operating in this project is being       │
│  taught wrong facts by its own instruction files.                    │
└──────────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Every AI agent (wrong mental model) | 🔥🔥🔥 Critical | Every single prompt — agents read stale instructions |
| Agent authors (HyperAgentSmith) | 🔥🔥🔥 High | Every agent update — shared content duplicated |
| Developers reading .github/ | 🔥🔥 Medium | Daily — trusting stale paths and dead patterns |
| Framework maintainers | 🔥🔥 Medium | Every new module or agent |

### ✨ The Vision

```
After This Blueprint:
┌──────────────────────────────────────────────────────────────────────┐
│  P0 — CONTAMINATION FIXED:                                           │
│  ✅ instruction_controller.py: Path(__file__).parent / "data"        │
│  ✅ Zero "cores/" references remain in any data file                 │
│  ✅ Zero init.yaml/pip/sys.path.insert references remain             │
│  ✅ All files reference v3 patterns: pyproject.toml, uv, package     │
│     imports, [project].dependencies                                  │
│  ✅ Agent format spec updated (argument-hint, handoffs, send)        │
│  ✅ adhd refresh --full actually syncs current content to .github/   │
│                                                                      │
│  P1 — COMPILATION PIPELINE:                                          │
│  instruction_core/data/                                              │
│    flows/{agents,instructions,prompts,_lib}/ ← SOURCE OF TRUTH       │
│    skills/{expedition,day-dream,testing,                             │
│           orch-discussion,orch-implementation,orch-testing,           │
│           orch-routing,orch-expedition}/                              │
│    compiled/{agents,instructions,prompts,skills}/                    │
│    compiled/compiled_manifest.json  ← provenance + hashes            │
│         │                                                            │
│         ▼  (flow_core.compile_file → manifest → sync)                │
│  .github/                                                            │
│    instructions/  ← always-on coding standards                       │
│    agents/        ← compiled agent files                             │
│    prompts/       ← compiled prompt files                            │
│    skills/        ← on-demand capability bundles (Agent Skills fmt)  │
└──────────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> We're fixing a silently broken instruction sync pipeline — repairing the dead path, purging v2 poison from 37 files, then building a compiled instruction pipeline so agent authors can compose agents from reusable .flow fragments with full provenance.

---

## 🔧 The Spec

---

## 🌟 TL;DR

instruction_core's official sync path points to `cores/instruction_core/data` which doesn't exist (renamed to `modules/dev/instruction_core/data` in the v3 migration). The sync silently no-ops, leaving .github/ files stale. Worse, the data files themselves are contaminated with v2 patterns — dead paths, dead tooling references, wrong vocabulary. We will (1) fix the broken path, (2) purge all v2 contamination from 37 files, (3) adopt Agent Skills for workflow-specific bundles, and (4) build a flow_core-powered compilation pipeline.

---

## 🎯 Problem Statement

ADHD's instruction system has a **3-layer contamination problem**:

1. **Layer 1 — Path References**: 20+ files contain `cores/instruction_core/` paths in `applyTo` frontmatter, body text, and examples. The `cores/` directory was renamed to `modules/dev/` during the v3 folder restructure (blueprint 04). These paths are dead.

2. **Layer 2 — Tooling Mental Model**: Files mandate `init.yaml` creation, `pip install` workflows, `sys.path.insert` import patterns, and `requirements.txt` dependency declarations. v3 uses `pyproject.toml` with `[tool.adhd]`, `uv` for package management, standard package imports via editable installs, and `[project].dependencies` for dependency declarations.

3. **Layer 3 — Structural Vocabulary**: `adhd_framework_context.instructions.md` (the most-read instruction file) lists `cores/` as a valid directory and tells agents to use it. Every agent builds a mental model of a project that doesn't exist.

The root cause that enables perpetual staleness: `instruction_controller.py` line 47 hardcodes `self.official_source_path = self.root_path / "cores" / "instruction_core" / "data"`. Since `cores/` doesn't exist, the sync silently skips, and .github/ never gets updated.

Beyond contamination, the sync is also architecturally limited — `shutil.copy2` with no composition, no provenance, and workflow files mixed with coding standards.

---

## 🔍 Prior Art & Existing Solutions

| Library/Tool | What It Does | Decision | License | Rationale |
|--------------|--------------|----------|---------|-----------|
| flow_core (internal) | `.flow` → Markdown compiler with tokenizer, parser, resolver, compiler stages | **BUILD ON** | Internal | Already mature, tested, in-repo. `FlowController.compile_file()` |
| VS Code / Agent Skills | On-demand capability bundles with `SKILL.md` + resources; [open standard](https://agentskills.io/) | **ADOPT** | Open standard | Native progressive disclosure, portable across VS Code, Copilot CLI, Copilot coding agent, Claude, Cursor, and others |
| Jinja2 templates | Template engine for markdown generation | **REJECT** | BSD-3 | flow_core already handles composition with `@import`, `$ref`, and styles |
| mdx-bundler | MDX compilation and bundling | **REJECT** | MIT | JavaScript ecosystem, wrong language, overkill |

**Summary:** We build on our own `flow_core` compiler (already proven) and adopt VS Code's native Skills format. No new external dependencies for P0. P1 adds `flow-core` as a workspace dependency via `pyproject.toml`.

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Creating `init.yaml` files | `init.yaml` is a dead v2 pattern. v3 uses `pyproject.toml` with `[tool.adhd]`. instruction_core already has one and IS discovered by ModulesController. |
| Rewriting flow_core | The compiler is mature and tested. We consume it as-is. |
| Converting per-module `.instructions.md` to `.flow` | These live in module directories, are sync'd separately by `_sync_module_files_to_target()`, and are owned by module authors. |
| Auto-generating agent logic | We compile structure/composition, not generate AI behavior. |
| Runtime compilation / hot-reload | Compilation is a dev-time build step via `adhd refresh --full`. |
| Changing flow_core's architecture | flow_core stays a pure compiler library with zero knowledge of instruction_core. |

---

## ✅ Features Overview

| Priority | Feature | Difficulty | Description |
|----------|---------|------------|-------------|
| P0 | v3 Contamination Fix | `[KNOWN]` | Fix broken sync path, purge v2 references from all 37 data files, update agent format spec |
| P0 | Skills Identification & Adoption | `[KNOWN]` | Reclassify workflow-specific files as Agent Skills (one skill per folder, SKILL.md format) |
| P1 | Flow Compilation Pipeline | `[EXPERIMENTAL]` | Build discover → compile → manifest → write pipeline in instruction_core |
| P1 | instruction_core Refactor | `[KNOWN]` | Transform instruction_core from dumb copier to compile+sync orchestrator |
| P2 | Cleanup | `[KNOWN]` | Remove hand-written files replaced by .flow sources |

→ See individual Feature Docs for details:
- [03 - v3 Contamination Fix](./03_feature_v3_format_fix.md)
- [04 - Skills Adoption](./04_feature_skills_adoption.md)
- [05 - Flow Compilation Pipeline](./05_feature_flow_compilation_pipeline.md)
- [06 - instruction_core Refactor](./06_feature_instruction_core_refactor.md)

---

## [Custom] 📜 Key Design Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | **Fix path via `Path(__file__).parent / "data"`** | Derive from module location, not hardcoded project-relative path. Survives future renames. |
| 2 | **Compiled output is committed** | Git blame, PR diffs, debuggability. `.github/` is what VS Code reads — it must be in git. |
| 3 | **Skills support dual-mode: static + .flow** | Skills can be pure static `.md` (copied as-is) or `.flow` sources (compiled by flow_core). Mixed mode per-skill. This avoids blocking future .flow-compiled skills while keeping simple skills trivial to author. |
| 4 | **Not all files need .flow** | Simple static markdown (e.g., `adhd_framework_context.instructions.md`) stays as-is. Only complex composed documents become .flow. |
| 5 | **Merge priority: compiled > static > per-module** | When sync encounters filename conflicts, compiled wins. Prevents stale overrides. |
| 6 | **Manifest-driven** | `compiled_manifest.json` provides provenance — source path, timestamp, content hash. |
| 7 | **Dependencies via pyproject.toml only** | `[project].dependencies = ["flow-core"]` + `[tool.uv.sources] flow-core = { workspace = true }`. No init.yaml, no GitHub URLs, no requirements.txt. |

---

## [Custom] 📊 v3 Module Discovery (Reference)

For clarity throughout this blueprint, here is how v3 module discovery works:

| Aspect | v3 (Current) | v2 (Dead) |
|--------|-------------|-----------|
| Discovery mechanism | `pyproject.toml` with `[tool.adhd]` section | `init.yaml` in module root |
| Dependency declaration | `[project].dependencies = ["flow-core"]` (package names, hyphens) | `requirements:` list with GitHub URLs |
| Workspace resolution | `[tool.uv.sources] flow-core = { workspace = true }` | `pip install -e` or `sys.path.insert` |
| Layer declaration | `[tool.adhd].layer = "dev"` | `init.yaml` `type:` field |
| Import pattern | `from flow_core import FlowController` (package import) | `sys.path.insert(0, root); from cores.flow_core import ...` |
| Package manager | `uv` | `pip` |
| Discovery scan path | `modules/{foundation,runtime,dev}/` for dirs with `pyproject.toml` | `cores/`, `managers/`, `utils/`, etc. |

---

## 📊 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| `instruction_controller.py` broken path | Fixed | `official_source_path` resolves to existing directory |
| `cores/` references in data files | Zero | `grep -r "cores/" modules/dev/instruction_core/data/` returns nothing |
| Dead v2 tooling references | Zero | No `init.yaml`, `pip install`, `sys.path.insert`, `requirements.txt` references in instruction content |
| Files with v3 format compliance | 100% (37/37) | Audit checklist in P0 |
| Workflow files reclassified as Skills | 8 skill bundles | Count `skills/` folders |
| Agent files compilable from .flow | 8/8 (after P1b) | `compiled_manifest.json` lists all 8 |
| Provenance coverage | 100% of compiled files | Every `.github/` file traceable to source |

---

## 📅 Scope Budget

| Phase | Duration | Hard Limit |
|-------|----------|------------|
| P0 (v3 Contamination Fix + Skills) | 3-5 days | Max 5 tasks, `[KNOWN]` only |
| P1 (Flow Compilation Pipeline) | 1-2 weeks | May include `[EXPERIMENTAL]` |
| P1b (Remaining Agent Migrations) | 1-2 weeks | `[KNOWN]` + `[EXPERIMENTAL]` |
| P2 (Cleanup) | 2-3 days | `[KNOWN]` only |

---

## 🛠️ Tech Preferences

| Category | Preference | Rationale |
|----------|------------|-----------|
| Language | Python 3.11+ | Framework standard |
| Package manager | uv | v3 standard — NOT pip |
| Dependency declaration | `pyproject.toml` `[project].dependencies` | v3 standard — NOT init.yaml, NOT requirements.txt |
| Compiler | flow_core (internal) | Already mature, `FlowController.compile_file()` |
| Skills format | VS Code `.github/skills/` | Native platform support, progressive disclosure |
| Manifest format | JSON | Simple, stdlib `json` module, git-diffable |
| Hashing | SHA-256 via `hashlib` | Stdlib, no deps. Solution sizing: stdlib > lightweight lib |
| Import pattern | Package imports via uv editable install | `from flow_core import FlowController` — NOT `sys.path.insert` |

---

## ❓ Open Questions

- Should `compiled_manifest.json` track per-module `.instructions.md` files too, or only compiled outputs?
- What's the exact threshold for "needs .flow" vs "stays static markdown"? Proposed: if a file uses shared fragments or conditional composition → .flow. Otherwise → static.
- ~~Should the `adhd refresh` command auto-compile, or should compilation be a separate `adhd compile` step?~~ **Resolved:** Compilation happens in `refresh_full.py` (via `adhd refresh --full`). No separate compile command needed.

---

## ✅ Executive Summary Validation Checklist

### Narrative (The Story)
- [x] **Problem** is specific (names who hurts and how)
- [x] **Value** is quantifiable or emotionally resonant
- [x] **Consequence** of not solving is clear
- [x] **3-layer contamination model** is the framing

### Scope Boundaries
- [x] **Non-Goals** has ≥3 explicit exclusions
- [x] **Non-Goals** explicitly excludes creating init.yaml files
- [x] **Features Overview** has ≤5 P0 features
- [x] **Tech Preferences** uses v3 patterns only (uv, pyproject.toml, package imports)

### v3 Accuracy
- [x] Zero references to init.yaml as something to create
- [x] Zero references to pip or sys.path.insert
- [x] Zero references to `cores/` as a valid directory
- [x] All dependency patterns use `pyproject.toml` format

---

**Next:** [Architecture](./02_architecture.md)

---

**← Back to:** [Index](./00_index.md)

