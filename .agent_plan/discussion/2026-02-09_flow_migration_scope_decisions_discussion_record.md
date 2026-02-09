# 📋 Discussion Report: Flow Migration Scope Decisions

> **Date**: 2026-02-09  
> **Participants**: HyperArch, HyperSan, HyperDream  
> **Status**: ✅ CONSENSUS REACHED  
> **Blueprint**: [09 - Agent .flow Migration](../day_dream/09_flow_migration/00_index.md)

---

## 🎯 Problem Statement

Three open design questions in the Agent .flow Migration blueprint required multi-agent discussion:

1. Should flow_core support raw-text `+` import syntax for non-`.flow` files (e.g., YAML)?
2. Should `instruction_controller` provide a unified pass-through pipeline for non-flow files?
3. Should four instruction files be converted to skills, kept as instructions, or handled with a hybrid approach?

---

## 📊 Discussion Rounds

### Round 1: Raw-text `+` import syntax

| Participant | Position | Key Argument |
|-------------|----------|-------------|
| **User** | Propose `+./file.yaml \| @node = $_ \|.` syntax | Single-language solution, everything through flow_core |
| **HyperArch** | REJECT | flow_core is a pure Markdown emitter. Adding YAML awareness violates its design boundary. Sidecar is simpler and already designed in the blueprint. |
| **HyperSan** | REJECT | Grammar expansion adds parser complexity with no clear second use case. One-off need doesn't justify language-level changes. |
| **HyperDream** | REJECT | Sidecar approach in `instruction_controller.py` is the correct boundary. Re-evaluate only if a second non-flow format demands inclusion. |

**Outcome:** ❌ **REJECTED** — unanimous

---

### Round 2: Pass-through dispatcher in instruction_controller

| Participant | Position | Key Argument |
|-------------|----------|-------------|
| **User** | Single workflow for all files through flow_core | Simplicity of one pipeline |
| **HyperArch** | ACCEPT (modified) | Yes to unified pipeline, but dispatcher belongs in `instruction_controller`, not `flow_core`. Thin if/else: `.flow` → compile, else → copy. Already largely exists. |
| **HyperSan** | ACCEPT | Manifest should distinguish `type: compiled` vs `type: passthrough` for auditability. Slot as P2 quality-of-life, not a P0 blocker. |
| **HyperDream** | ACCEPT | Adds clarity to the pipeline without expanding flow_core's scope. P2 is the right phase — doesn't block agent migration. |

**Outcome:** ✅ **ACCEPTED** as P2, with `instruction_controller` as the home (not flow_core)

---

### Round 3: Instructions → skills hybrid approach

| Participant | Position | Key Argument |
|-------------|----------|-------------|
| **User** | Convert `module_development`, `prompts_format`, `instructions_format`, `agents_format` to skills | Skills are loaded on-demand vs instructions always-on |
| **HyperArch** | ACCEPT HYBRID | Per-file evaluation needed. Cannot wholesale convert — `applyTo` auto-enforcement has no skills equivalent. Split candidates into thin instruction + skill if mixed. |
| **HyperSan** | ACCEPT HYBRID | Removing `applyTo` enforcement is a regression. Each file must be evaluated: SOP-only → skill, enforcement → keep instruction, mixed → split. |
| **HyperDream** | ACCEPT HYBRID | Long-term, flow_core composition may subsume the instruction/skill distinction. This evaluation is interim. Document the SOP-vs-enforcement criterion for each file. |

**Outcome:** ✅ **ACCEPTED** as hybrid per-file evaluation at P2

---

## ✅ Final Consensus Summary

| # | Decision | Verdict | Phase | Impact |
|---|----------|---------|-------|--------|
| 1 | Raw-text `+` import syntax | ❌ REJECTED | — | flow_core grammar unchanged. Sidecar approach ratified. |
| 2 | Pass-through dispatcher | ✅ ACCEPTED | P2 | `instruction_controller` gets thin dispatcher. Manifest adds `type` field. |
| 3 | Instructions → skills | ✅ ACCEPTED (hybrid) | P2 | 4 files evaluated per SOP-vs-enforcement criterion. No wholesale conversion. |

---

## 📝 Amendments to Blueprint

| Document | Change | Reference |
|----------|--------|-----------|
| [05_feature_scope_decisions.md](../day_dream/09_flow_migration/05_feature_scope_decisions.md) | Added `## [Custom] 🏛️ Architectural Scope Decisions` section with all 3 decisions. Updated 4 instruction file rows from ❌ NO to ⚠️ CONDITIONAL. Updated summary counts. | Decisions 1–3 |
| [03_feature_p0_infrastructure.md](../day_dream/09_flow_migration/03_feature_p0_infrastructure.md) | Added ratification note to sidecar `.yaml` section confirming Decision 1. | Decision 1 |
| [80_implementation.md](../day_dream/09_flow_migration/80_implementation.md) | Added P2 tasks 12–15 (pass-through dispatcher, manifest type, instruction evaluation, conversions). Updated decisions log, cut list, exit gate, and completion checklist. | Decisions 1–3 |

---

## 📌 Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | No action — Decision 1 ratifies existing sidecar design | — | ✅ Done (blueprint updated) |
| 2 | Implement pass-through dispatcher at P2 | HyperArch | ⏳ [TODO] — P2-12 |
| 3 | Add `type` field to manifest schema at P2 | HyperArch | ⏳ [TODO] — P2-13 |
| 4 | Evaluate 4 instruction files SOP-vs-enforcement at P2 | HyperSan + HyperDream | ⏳ [TODO] — P2-14 |
| 5 | Execute instruction→skill conversions per evaluation | HyperArch | ⏳ [TODO] — P2-15 |
