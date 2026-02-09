# 01 - Executive Summary

> Part of [Agent .flow Migration Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌──────────────────────────────────────────────────────────────────────┐
│  8 ADHD agents share ~170 lines of IDENTICAL content:                │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   │
│  │ san_checker │  │  architect  │  │ orchestrator│  ... (×8)         │
│  │             │  │             │  │             │                   │
│  │ common_rules│  │ common_rules│  │ common_rules│  ← COPY-PASTE     │
│  │ stopping    │  │ stopping    │  │ stopping    │  ← COPY-PASTE     │
│  │ self-id     │  │ self-id     │  │ self-id     │  ← COPY-PASTE     │
│  │ framework   │  │ framework   │  │ framework   │  ← COPY-PASTE     │
│  │ truthful    │  │ truthful    │  │ truthful    │  ← COPY-PASTE     │
│  └─────────────┘  └─────────────┘  └─────────────┘                   │
│                                                                      │
│  💥 Update shared content = manually edit 8 files                    │
│  💥 Drift between agents = silent consistency bugs                   │
│  💥 No tooling to verify cross-agent consistency                     │
└──────────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| HyperAgentSmith (agent author) | 🔥🔥🔥 High | Every shared-content update — 8-file manual edit |
| All agents (consistency) | 🔥🔥🔥 High | Silent drift risk on every update |
| Framework maintainers | 🔥🔥 Medium | PR reviews can't verify 8-way consistency |

### ✨ The Vision

```
After This Blueprint:
┌──────────────────────────────────────────────────────────────────────┐
│  _lib/ fragments = SINGLE SOURCE OF TRUTH                            │
│                                                                      │
│  ┌──────────────────┐     ┌─────────────────────────────────┐        │
│  │ _lib/patterns/   │     │  agents/hyper_san_checker.flow  │        │
│  │  core_philosophy │────►│    @import "../_lib/patterns/..."        │
│  │  stopping_rules  │     │    + agent-specific content     │        │
│  │  critical_rules  │     └───────────┬─────────────────────┘        │
│  │  specialist_aware│                 │                              │
│  ├──────────────────┤     compile_file()                             │
│  │ _lib/adhd/       │                 │                              │
│  │  framework_info  │                 ▼                              │
│  ├──────────────────┤     ┌─────────────────────────────────┐        │
│  │ _lib/provider/   │     │  compiled/agents/               │        │
│  │  chatagent_wrapper     │  hyper_san_checker.adhd.agent.md│        │
│  └──────────────────┘     │  (frontmatter prepended)        │        │
│                           └─────────────────────────────────┘        │
│                                                                      │
│  ✅ Edit core_philosophy.flow → recompile → ALL 8 agents updated     │
│  ✅ Git diff shows exactly what changed                              │
│  ✅ Compilation guarantees zero drift                                │
└──────────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Migrate 8 ADHD agent files from hand-maintained markdown to composable `.flow` sources with a shared fragment library, eliminating copy-paste drift forever.

---

## 🔧 The Spec

---

## 🌟 TL;DR

Eight ADHD agent files share ~170 lines of duplicated content across 9 common blocks. This blueprint migrates them to composable `.flow` sources with a `_lib/` shared fragment library, using the compilation pipeline built in Blueprint 08. Two infrastructure blockers (transitive hashing, YAML frontmatter) must be fixed first.

---

## 🎯 Problem Statement

ADHD agent files (`*.adhd.agent.md`) contain both agent-specific logic and shared framework content (common rules, stopping rules, self-identification, framework context). Today, shared content is copy-pasted across all 8 agents. Any update to shared content requires manually editing 8 files, with no tooling to detect drift. Blueprint 08 built the compilation infrastructure; this blueprint puts it to work.

---

## 🔍 Prior Art & Existing Solutions

| Library/Tool | What It Does | Decision | License | Rationale |
|--------------|--------------|----------|---------|-----------|
| Blueprint 08 compilation pipeline | `_compile_flows()` + manifest + merge-priority sync | BUILD (done) | Internal | Already built and tested. P0-P2 complete. |
| Blueprint 08 Feature 05 | Original migration strategy vision, shared fragment plan | BUILD (this blueprint) | Internal | We're executing the vision documented there. |
| flow_core `@import` directive | Enables shared fragments via file composition | ADOPT | Internal | Core language feature, proven in tests + playground. |
| flow_core playground v4 | Aspirational `lib/` structure prototype | ADAPT | Internal | Informed `_lib/` structure design. |
| Jinja2 / template engines | General-purpose template composition | REJECT | BSD | Overkill — flow_core already solves this with `@import` + `@out`. Solution sizing: we have a purpose-built tool. |

**Summary:** All infrastructure exists from Blueprint 08. This blueprint fixes two blockers and executes the migration.

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Migrate standalone instruction files (9 files) | Zero composition value — they're static reference docs with no shared content |
| Migrate prompt files (3 files) | Static, short, no sharing between prompts |
| Migrate standalone skill files (4 non-orch skills) | Prose documentation with no composition need |
| Modify flow_core's language or compiler | Flow_core is stable; changes are limited to exposing existing internal state |
| Auto-watch / live-recompile on file change | <20 files total — manual `adhd refresh --full` is sufficient |
| Parallel compilation | Sub-second compile time for <20 files makes this pointless |
| Create new agents or change agent behavior | Migration preserves exact current behavior, byte-for-byte where possible |

---

## ✅ Features Overview

| Priority | Feature | Difficulty | Description |
|----------|---------|------------|-------------|
| P0 | [Transitive Hash Fix](./03_feature_p0_infrastructure.md) | `[KNOWN]` | Expose `_graph_files` from resolver so compilation hashes the full import closure |
| P0 | [YAML Frontmatter Post-Processing](./03_feature_p0_infrastructure.md) | `[KNOWN]` | Sidecar `.yaml` files prepended to compiled output for agent frontmatter |
| P0 | [`_lib/` Fragment Library](./03_feature_p0_infrastructure.md) | `[KNOWN]` | Create shared fragments extracted from current agent content |
| P1 | [First Agent Migration](./04_feature_agent_migration.md) | `[KNOWN]` | hyper_san_checker proof-of-concept: `.flow` source → compiled agent |
| P2 | [Remaining Agent Migrations](./04_feature_agent_migration.md) | `[KNOWN]` | 7 remaining agents + `agent_common_rules.flow` + orch-skills evaluation |

→ See individual feature docs for details.

---

## [Custom] 📊 Migration Scope Summary

| Category | Files | Lines | Migration? | Phase |
|----------|-------|-------|------------|-------|
| Agents | 8 | 952 | ✅ YES | P1-P2 |
| `agent_common_rules` instruction | 1 | 70 | ✅ YES (agent-coupled) | P2 |
| Other instructions | 9 | 858 | ❌ NO | — |
| Prompts | 3 | 213 | ❌ NO | — |
| Orch-skills | 5 | ~1,200 | ⚠️ CONDITIONAL | P2 eval |
| Standalone skills | 4 | ~881 | ❌ NO | — |
| **Total target** | **9** | **~1,022** | | |
| **Grand total files** | **30** | **~4,174** | | |

→ See [05 - Scope Decisions](./05_feature_scope_decisions.md) for per-file reasoning.

---

## 📊 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Shared content duplication | 0 instances | `grep` for shared blocks in compiled output — all trace to `_lib/` sources |
| Agent compilation success | 8/8 agents compile | `adhd refresh --full` with zero flow errors |
| Behavioral fidelity | Byte-identical output | `diff` compiled output vs pre-migration hand-written files |
| Change propagation | 1 edit → 8 updates | Modify `_lib/` fragment, recompile, verify all affected agents updated |
| MCP injection compatibility | Injection works post-compile | `_apply_mcp_injection_to_agents()` succeeds on compiled agent files |

---

## 📅 Scope Budget

| Phase | Duration | Hard Limit |
|-------|----------|------------|
| P0 (Infrastructure) | 3-5 days | Max 5 tasks, `[KNOWN]` only |
| P1 (First Agent) | 3-5 days | `[KNOWN]` only |
| P2 (Full Fleet) | 1-2 weeks | `[KNOWN]`, may include `[EXPERIMENTAL]` for orch-skills |

---

## 🛠️ Tech Preferences

| Category | Preference | Rationale |
|----------|------------|-----------|
| Language | Python 3.11+ | Framework standard |
| Composition tool | flow_core `@import` + `@out` | Purpose-built, already a dependency |
| Frontmatter | Sidecar `.yaml` files | Keeps flow_core as pure Markdown emitter |
| Hashing | stdlib `hashlib.sha256` | Solution sizing: stdlib handles this trivially |
| File I/O | stdlib `pathlib` + `shutil` | No new dependencies needed |

---

## ❓ Open Questions

- Should orch-skill `.instructions.md` files be migrated to `.flow`? (Evaluate during P2 based on P1 learnings)
- Should `_lib/templates/adhd_agent.flow` define a master skeleton, or should each agent compose fragments directly? (Decide during P0 `_lib/` design)

---

## 📋 Handoff Checklist

- [x] TL;DR exists and is ≤3 sentences
- [x] Prior Art section documents existing solutions considered
- [x] Non-Goals has ≥3 explicit exclusions
- [x] All P0 features have difficulty labels
- [x] No `[RESEARCH]` items in P0
- [x] Scope Budget is defined
- [x] Success Metrics are quantifiable

**HANDOFF STATUS:** ⬜ Pending

---

## ✅ Executive Summary Validation Checklist

### Narrative (The Story)
- [x] **Problem** is specific (names who hurts and how)
- [x] **Value** is quantifiable or emotionally resonant
- [x] **Consequence** of not solving is clear

### Scope Boundaries
- [x] **Non-Goals** has ≥3 explicit exclusions
- [x] **Features Overview** has ≤5 P0 features
- [x] No `[RESEARCH]` items in P0

### Technical Grounding
- [x] **Prior Art** section documents ≥2 alternatives considered
- [x] **Tech Preferences** are stated
- [x] **Scope Budget** has time estimates per phase

---

**Next:** [Architecture](./02_architecture.md)

---

**← Back to:** [Index](./00_index.md)
