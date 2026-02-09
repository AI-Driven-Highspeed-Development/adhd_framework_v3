# 05 - Feature: Scope Decisions

> Part of [Agent .flow Migration Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                        │
├────────────────────────────────┼────────────────────────────────┤
│  30 data files, unclear which  │  30 files with explicit       │
│  benefit from .flow migration  │  YES/NO/CONDITIONAL + reason  │
│       ↓                        │       ↓                        │
│  💥 Risk of over-migrating     │  ✅ Focused 9-file scope       │
│  💥 Risk of under-migrating    │  ✅ Clear rationale per file   │
│  💥 Scope creep                │  ✅ Decision matrix on record  │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Document the YES/NO/CONDITIONAL migration decision for every data file so scope is explicit and reviewable.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| Scope clarity | ❌ Ambiguous | ✅ Per-file decision with rationale |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Provide a reviewable decision matrix for all 30 instruction_core data files, recording which files are migrated to `.flow` and why.

**Priority:** P0 (decision), P1-P2 (execution)  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Decision matrix for all 30 data files
- Rationale for each YES/NO/CONDITIONAL decision
- Migration benefit criteria definition

**Out of Scope:**
- Actually performing the migrations (see [04 - Agent Migration](./04_feature_agent_migration.md))
- Changing file content or behavior
- Evaluating files outside `instruction_core/data/`

---

## [Custom] 📋 Migration Benefit Criteria

A file benefits from `.flow` migration when it meets **any** of:

| Criterion | Weight | Example |
|-----------|--------|---------|
| **Shares content** with other files | High | Common rules shared across 8 agents |
| **Composes** from multiple logical sections | Medium | Agent = shared rules + unique behavior |
| **Frequently updated** shared portions | Medium | Stopping rules updated as team evolves |
| **Conditional content** based on target | Low | Mode presets varying by agent context |

A file does **NOT** benefit when:
- It's a standalone reference document (read-only, no composition)
- It's short and self-contained (no shared blocks)
- It's static prose with no structural patterns
- Loading it requires no assembly from parts

---

## [Custom] 📊 Full Decision Matrix

### Agents (8 files, 952 lines)

| File | Lines | Decision | Phase | Rationale |
|------|-------|----------|-------|-----------|
| `hyper_san_checker.adhd.agent.md` | 120 | ✅ YES | P1 | Shares 9 content blocks with other agents. Proof-of-concept. |
| `hyper_architect.adhd.agent.md` | 129 | ✅ YES | P2 | Shares 9 content blocks. Complex but high-value. |
| `hyper_orchestrator.adhd.agent.md` | 150 | ✅ YES | P2 | Shares 9 content blocks. Most complex (5 mode presets). Highest dedup value. |
| `hyper_red.adhd.agent.md` | 149 | ✅ YES | P2 | Shares 9 content blocks. |
| `hyper_iq_guard.adhd.agent.md` | 103 | ✅ YES | P2 | Shares 9 content blocks. |
| `hyper_day_dreamer.adhd.agent.md` | 117 | ✅ YES | P2 | Shares 9 content blocks. |
| `hyper_agent_smith.adhd.agent.md` | 96 | ✅ YES | P2 | Shares 9 content blocks. |
| `hyper_expedition.adhd.agent.md` | 88 | ✅ YES | P2 | Shares 9 content blocks. |

**Summary:** All 8 agents share 9 identified content blocks totaling ~170 duplicated lines. Migration eliminates all duplication.

### Instructions (10 files, 928 lines)

| File | Lines | Decision | Phase | Rationale |
|------|-------|----------|-------|-----------|
| `agent_common_rules.instructions.md` | 70 | ✅ YES | P2 | Agent-coupled metadata — defines the canonical rules that agents import. Migrating means `_lib/patterns/` becomes the single source for both this instruction AND agent imports. |
| `adhd_framework_context.instructions.md` | ~200 | ❌ NO | — | Standalone reference document. Read by agents but not composed from parts. No shared blocks with other files. |
| `agents_format.instructions.md` | ~80 | ❌ NO (Enforcement) | P2 eval ✅ | **Enforcement**: Defines required section order, YAML header fields, template as format spec. Auto-loaded on every `.agent.md` edit via `applyTo`. Converting to skill would lose auto-enforcement — regression. |
| `cli_manager.instructions.md` | ~60 | ❌ NO | — | Module-specific instruction. Self-contained, no sharing. |
| `config_manager.instructions.md` | ~80 | ❌ NO | — | Module-specific instruction. Self-contained, no sharing. |
| `exceptions.instructions.md` | ~60 | ❌ NO | — | Module-specific instruction. Self-contained, no sharing. |
| `instructions_format.instructions.md` | ~80 | ❌ NO (Enforcement) | P2 eval ✅ | **Enforcement**: Defines required structure, naming conventions, `applyTo` pattern rules. Auto-loaded on every `.instructions.md` edit. Format enforcement, not procedural SOP. |
| `logger_util.instructions.md` | ~60 | ❌ NO | — | Module-specific instruction. Self-contained, no sharing. |
| `module_development.instructions.md` | ~120 | ❌ NO (Enforcement) | P2 eval ✅ | **Enforcement**: Anti-hallucination rules (NEVER invent imports, NEVER print()), module file structure (MUST include), verification checklist. Auto-loaded on every `modules/**/*.py` edit. All enforcement content. |
| `prompts_format.instructions.md` | ~60 | ❌ NO (Enforcement) | P2 eval ✅ | **Enforcement**: Defines required structure, naming conventions, best practices. Auto-loaded on every `.prompt.md` edit. Format enforcement, not procedural SOP. |

**Summary:** `agent_common_rules` benefits from `.flow` migration (canonical source). Four instruction files (`module_development`, `prompts_format`, `instructions_format`, `agents_format`) evaluated P2 → **all Enforcement**. They stay as instructions with existing `applyTo` globs. Converting to skills would lose auto-enforcement (instructions auto-load on file edit; skills require explicit `read_file`). No conversions needed.

### Prompts (3 files, 213 lines)

| File | Lines | Decision | Phase | Rationale |
|------|-------|----------|-------|-----------|
| `create_agent.prompt.md` | ~80 | ❌ NO | — | Static, self-contained prompt. No sharing between prompts. |
| `hyper_san_output.prompt.md` | ~70 | ❌ NO | — | Static output template. No composition value. |
| `update_requirements.prompt.md` | ~63 | ❌ NO | — | Static prompt. No sharing. |

**Summary:** All 3 prompts are static, short, and share nothing. Zero migration value.

### Skills — Orchestrator Presets (5 files, ~1,200 lines)

| File | Lines | Decision | Phase | Rationale |
|------|-------|----------|-------|-----------|
| `orch-discussion` | ~200 | ❌ NO | P2 eval ✅ | Runtime-loaded by HyperOrch via `read_file`. Unique discussion protocol. Only ~4 lines shared (`autonomy_guidance` variant). No compile-time composition benefit. |
| `orch-implementation` | ~250 | ❌ NO | P2 eval ✅ | Runtime-loaded by HyperOrch. Unique implementation protocol with embedded `execution_guidance`. No shared blocks justify migration. |
| `orch-testing` | ~250 | ❌ NO | P2 eval ✅ | Runtime-loaded by HyperOrch. Unique testing protocol with embedded `testing_standards`. No shared blocks justify migration. |
| `orch-routing` | ~250 | ❌ NO | P2 eval ✅ | Runtime-loaded by HyperOrch. Unique routing protocol with agent selection table. No shared blocks justify migration. |
| `orch-expedition` | ~250 | ❌ NO | P2 eval ✅ | Runtime-loaded by HyperOrch. Most complex skill, entirely self-contained 8-phase pipeline. No shared blocks. |

**Summary:** ❌ All 5 NO. These skills are loaded at **runtime** by HyperOrch via `read_file` when a workflow preset triggers — NOT compiled into agent definitions. Each has unique protocol content. The only shared text is a ~4-line `autonomy_guidance` variant across 4 skills, with per-skill wording variations. .flow is designed for compile-time composition; runtime-loaded skills don't benefit.

### Skills — Standalone (4 files, ~881 lines)

| File | Lines | Decision | Phase | Rationale |
|------|-------|----------|-------|-----------|
| `day-dream` | ~450 | ❌ NO | — | Prose-heavy skill with template references. No composition value — already organized as a standalone skill. |
| `expedition` | ~200 | ❌ NO | — | Standalone skill. Self-contained export workflow. |
| `testing` | ~130 | ❌ NO | — | Standalone skill. Self-contained testing guide. |
| `writing-skills` | ~100 | ❌ NO | — | Meta-skill about writing skills. Self-contained. |

**Summary:** All 4 standalone skills are prose documentation. No shared blocks, no composition need.

---

## [Custom] 🏛️ Architectural Scope Decisions

> Decisions from structured multi-agent discussion (2026-02-09). Participants: HyperArch, HyperSan, HyperDream. See [discussion record](../../discussion/2026-02-09_flow_migration_scope_decisions_discussion_record.md).

### Decision 1: REJECT raw-text `+` import — Keep sidecar approach ❌

| Aspect | Detail |
|--------|--------|
| **Proposal** | Add `+./file.yaml \| @node = $_ \|.` syntax to flow_core for non-.flow file imports |
| **Verdict** | **REJECTED** — full consensus |
| **Rationale** | The sidecar approach in `instruction_controller.py` is the correct boundary. flow_core stays pure — no grammar changes for non-`.flow` file imports. |
| **Condition** | Re-evaluate only if a second non-flow format demands inclusion (first case: YAML sidecars, handled outside flow_core). |
| **Impact on blueprint** | No changes needed — [03_feature_p0_infrastructure.md](./03_feature_p0_infrastructure.md) already specifies sidecar `.yaml` as the solution. This decision ratifies that design. |

### Decision 2: ACCEPT pass-through at instruction_controller level (P2) ✅

| Aspect | Detail |
|--------|--------|
| **Proposal** | Unified pipeline where `instruction_controller` handles both `.flow` compilation and non-flow passthrough |
| **Verdict** | **ACCEPTED** as P2 quality-of-life — partial acceptance |
| **Rationale** | A thin dispatcher in `instruction_controller` (if `.flow` → compile, else → copy) provides a unified pipeline. This already largely exists in the current architecture. |
| **Key constraint** | Pass-through lives in `instruction_controller`, NOT in `flow_core`. flow_core's boundary is `.flow` files only. |
| **Manifest change** | Manifest schema adds `type: compiled` vs `type: passthrough` distinction per entry. |
| **Phase** | P2 — not blocking P0/P1. Slot alongside full fleet migration. |

### Decision 3: ACCEPT HYBRID approach for instructions → skills ✅

| Aspect | Detail |
|--------|--------|
| **Proposal** | Evaluate four instruction files for potential conversion to skills |
| **Verdict** | **ACCEPTED** as hybrid — per-file evaluation |
| **Rationale** | `applyTo` auto-enforcement has no skills equivalent; wholesale removal is a regression. Each file needs individual evaluation. |

**Per-file evaluation matrix (P2):**

| File | Evaluation Question | If SOP only | If Enforcement | Preliminary Assessment |
|------|-------------------|-------------|----------------|------------------------|
| `module_development.instructions.md` | SOP or enforcement? | → Convert to skill | → Keep instruction, tighten `applyTo` | ✅ **Enforcement** — Anti-hallucination rules + module file structure requirements. Auto-loaded on every `modules/**/*.py` edit. |
| `prompts_format.instructions.md` | SOP or enforcement? | → Convert to skill | → Keep instruction, tighten `applyTo` | ✅ **Enforcement** — Required structure + naming conventions. Auto-loaded on every `.prompt.md` edit. |
| `instructions_format.instructions.md` | SOP or enforcement? | → Convert to skill | → Keep instruction, tighten `applyTo` | ✅ **Enforcement** — Required structure + `applyTo` rules. Auto-loaded on every `.instructions.md` edit. |
| `agents_format.instructions.md` | SOP or enforcement? | → Convert to skill | → Keep instruction, tighten `applyTo` | ✅ **Enforcement** — Required section order + YAML header spec. Auto-loaded on every `.agent.md` edit. |

**Decision rules:**
- If file contains **SOP/workflow guidance** only needed during creation → convert to skill
- If file contains **format-enforcement rules** that must apply on every edit → keep as instruction with tightened `applyTo` glob
- If file has **both** → split into thin instruction (enforcement only) + skill (workflow/SOP)

**Long-term note:** flow_core composition may eventually subsume the instruction/skill distinction entirely. This evaluation is an interim step.

---

## [Custom] 📊 Decision Summary

| Category | Total Files | Total Lines | Migrate | Phase |
|----------|-------------|-------------|---------|-------|
| Agents | 8 | 952 | 8 (100%) | P1-P2 |
| Instructions | 10 | 928 | 1 (10%) | P2 |
| Prompts | 3 | 213 | 0 (0%) | — |
| Orch-Skills | 5 | ~1,200 | 0 (0%) | Evaluated P2 — NO |
| Standalone Skills | 4 | ~881 | 0 (0%) | — |
| **Total** | **30** | **~4,174** | **9** | |

> **Note:** 4 instruction files evaluated P2 → all Enforcement (stay as instructions). 5 orch-skills evaluated P2 → all NO (runtime-loaded, no compile-time composition benefit). Final migration scope: **9 files** (8 agents + 1 instruction).

### Migration Effort vs Value

```
Value (shared content deduplicated)
  ▲
  │  ★ Agents (8)           ← HIGH value, 8 files, ~170 lines deduped
  │         
  │     ◆ agent_common_rules ← MEDIUM value, 1 file, canonical source
  │
  │          ▲ Orch-skills (5) ← UNKNOWN value, evaluate P2
  │
  │                         ● Instructions (9) ← LOW value, standalone
  │                         ● Prompts (3)      ← ZERO value
  │                         ● Skills (4)       ← ZERO value
  └──────────────────────────────────────────────► Migration Effort
```

---

## ✅ Acceptance Criteria

- [x] Every data file (30 total) has an explicit YES/NO/CONDITIONAL decision
- [x] Each decision has a rationale citing the benefit criteria
- [x] Orch-skills have evaluation criteria for P2 decision — **Evaluated: all NO**
- [x] Total migration scope is bounded: **9 definite** (8 agents + 1 instruction)

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Content analysis of all 30 files | Internal | ✅ Done | From multi-agent discussion |
| Shared content inventory | Internal | ✅ Done | 9 blocks identified |

---

## ✅ Simple Feature Validation Checklist

### Narrative
- [x] **The Story** clearly states user problem and value
- [x] **Intent** is unambiguous to a non-technical reader

### Technical
- [x] **Scope** is explicitly bounded (In/Out of Scope filled)
- [x] **Acceptance Criteria** are testable (not vague)
- [x] **Dependencies** are listed with status

### Linkage
- [x] Feature linked from [00_index.md](./00_index.md) and [01_executive_summary.md](./01_executive_summary.md)

---

**Prev:** [Feature: Agent Migration](./04_feature_agent_migration.md) | **Next:** [Implementation](./80_implementation.md)

---

**← Back to:** [Index](./00_index.md)
