---
project: "Instruction System Optimization"
current_phase: 0
phase_name: "Walking Skeleton"
status: TODO
last_updated: "2026-02-09"
---

# 80 - Implementation Plan

> Part of [Instruction System Optimization Blueprint](./00_index.md)

<!-- 
⚠️  CODE EXAMPLES & FOLDER STRUCTURES WARNING ⚠️
Examples in this document are ILLUSTRATIVE, not PRESCRIPTIVE.
The implementation agent (HyperArch) will determine actual paths and syntax.
-->

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

## 🦴 Phase 0: Walking Skeleton

**Goal:** *"Prove validation pipeline works with simplest possible implementation"*

**Duration:** 5 days (HARD LIMIT)

### Exit Gate

- [ ] `adhd instruction sync` validates line limits and emits SKILLS_INDEX.md

### Tasks

| Status | Task | Module | Difficulty | Feature |
|--------|------|--------|------------|---------|
| ⏳ | Add `line_validator.py` with simple line count check | `instruction_core/` | `[KNOWN]` | F03 |
| ⏳ | Hook line validation into `instruction_controller.compile()` | `instruction_core/` | `[KNOWN]` | F03 |
| ⏳ | Add token annotation regex parser (no aggregation yet) | `instruction_core/` | `[KNOWN]` | F04 |
| ⏳ | Create `skills_indexer.py` to scan SKILL.md files | `instruction_core/` | `[KNOWN]` | F06 |
| ⏳ | Generate SKILLS_INDEX.md during `instruction sync` | `instruction_core/` | `[KNOWN]` | F06 |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ❌ Max 5 tasks
- ✅ All tasks are `[KNOWN]`

### Target Folder Structure (P0)

```
instruction_core/
├── instruction_controller.py     (MODIFIED)
├── validators/
│   └── line_validator.py         (NEW)
├── budget/
│   └── token_parser.py           (NEW)
├── indexers/
│   └── skills_indexer.py         (NEW)
└── data/
    └── compiled/
        └── SKILLS_INDEX.md       (GENERATED)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Create test agent > 100 lines, run `instruction sync` | Compilation fails with clear error |
| Add `<!-- tokens: ~150 -->` to fragment, run sync | Token annotation logged (no error) |
| Run `instruction sync` with skills present | SKILLS_INDEX.md generated in `data/compiled/` |

### P0 Completion Checklist

- [ ] Exit gate command runs successfully
- [ ] All tasks marked ✅
- [ ] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [ ] ≤5 tasks total
- [ ] Manual verification steps pass

---

## 🏗️ Phase 1: Core Features Complete

**Goal:** *"All P0 features functional with full validation and audit capability"*

**Duration:** 1 week

### Exit Gate

- [ ] `adhd audit instructions <file>` shows co-activations, conflicts, and budget
- [ ] VS Code profile can be toggled on/off

### Tasks

| Status | Task | Module | Difficulty | Feature |
|--------|------|--------|------------|---------|
| ⏳ | Implement token budget aggregator | `instruction_core/` | `[KNOWN]` | F04 |
| ⏳ | Add warning/error thresholds (70%/90%) | `instruction_core/` | `[KNOWN]` | F04 |
| ⏳ | Split schema into `core.schema.json` + `vscode.profile.json` | `instruction_core/` | `[KNOWN]` | F05 |
| ⏳ | Implement profile loader and merger | `instruction_core/` | `[KNOWN]` | F05 |
| ⏳ | Create `conflict_detector.py` for instruction conflicts | `instruction_core/` | `[KNOWN]` | F07 |
| ⏳ | Implement `audit_instructions` MCP tool | `adhd_mcp/` | `[KNOWN]` | F07 |
| ⏳ | Add `adhd audit instructions` CLI command | `cli_manager/` | `[KNOWN]` | F07 |
| ⏳ | Add "When NOT to Use" extraction to skills indexer | `instruction_core/` | `[KNOWN]` | F06 |

### Target Folder Structure (P1)

```
instruction_core/
├── validators/
│   └── line_validator.py         (EXISTS)
├── budget/
│   ├── token_parser.py           (EXISTS)
│   └── token_aggregator.py       (NEW)
├── indexers/
│   └── skills_indexer.py         (MODIFIED)
├── audit/
│   └── conflict_detector.py      (NEW)
├── profiles/
│   └── profile_loader.py         (NEW)
└── data/
    └── schemas/
        ├── core.schema.json      (NEW)
        └── profiles/
            └── vscode.profile.json (NEW)

adhd_mcp/
└── adhd_mcp.py                   (MODIFIED - add audit tool)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Run `adhd audit instructions modules/dev/adhd_mcp/adhd_mcp.py` | Lists active instructions + conflicts + budget |
| Compile with total tokens > 70% of limit | Warning emitted |
| Run sync with `--profile generic` (no vscode) | VS Code fields not required |

### P1 Completion Checklist

- [ ] Exit gate command runs successfully
- [ ] All `[EXPERIMENTAL]` items validated or cut
- [ ] Manual verification steps pass
- [ ] Linked module specs updated

---

## 📡 Phase 2+: Deferred Features

**Goal:** *"Platform maturity and advanced observability"*

**Duration:** TBD (after P0/P1 validated)

### Deferred - P1: Flow Fragment Versioning

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ⏳ | Design versioning schema for flow fragments | `flow_core/` | `[EXPERIMENTAL]` |
| ⏳ | Implement version tracking when flow count >20 | `flow_core/` | `[EXPERIMENTAL]` |

**Trigger:** Activate when flow file count exceeds 20

### Deferred - P2: Behavioral Compliance Testing

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ⏳ | Design compliance test framework | `instruction_core/` | `[RESEARCH]` |
| ⏳ | Implement behavioral assertion runner | `instruction_core/` | `[RESEARCH]` |

**Trigger:** Activate after observability infrastructure (audit tool) is mature

### Deferred - Future: Runtime Content Deduplication

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| 🚫 | Design deduplication algorithm | `instruction_core/` | `[RESEARCH]` |

**Status:** Cut until orchestration layer matures

---

## ⚠️ Error Handling Implementation

### Error Types

| Error Class | When Raised | Recovery |
|-------------|-------------|----------|
| `LineLimitExceeded` | Compiled agent > 100 lines | fail compilation |
| `TokenBudgetWarning` | Budget > 70% | warn, continue |
| `TokenBudgetExceeded` | Budget > 90% | fail (configurable) |
| `SkillMissingMetadata` | SKILL.md lacks frontmatter | fail sync |
| `ConflictDetected` | Contradictory instructions | warn |
| `ProfileNotFound` | Unknown profile specified | fail |

### Logging Requirements

| Level | When | Example |
|-------|------|---------|
| ERROR | Line limit exceeded | `"Agent 'hyper_arch' exceeds line limit: 127/100"` |
| WARNING | Budget threshold crossed | `"Token budget at 72% (144000/200000)"` |
| WARNING | Missing token annotation | `"Fragment 'core_rules.md' missing token annotation"` |
| INFO | Validation passed | `"All agents within line limits"` |
| INFO | Index generated | `"SKILLS_INDEX.md generated with 9 skills"` |

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-09 | Line limit = 100 | Balances context usage with detail | HyperDream |
| 2026-02-09 | Tilde required in token annotation | Signals approximation, prevents false precision | HyperDream |
| 2026-02-09 | Warning at 70%, error at 90% | Leave buffer for response generation | HyperDream |
| 2026-02-09 | Defer runtime deduplication | Orchestration layer not mature | Multi-agent discussion |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| Runtime content deduplication | 2026-02-09 | Wait for orchestration maturity |
| Multi-model token optimization | 2026-02-09 | Start with single model (Claude) |
| Auto-fix line violations | 2026-02-09 | Human/agent judgment required |

---

## 🔬 Exploration Log

| Date | Topic | Status | Synthesized To |
|------|-------|--------|----------------|
| - | - | - | - |

---

**← Back to:** [Index](./00_index.md)

<!--
NOTES:
1. Update YAML frontmatter when changing phases
2. Status flow: ⏳ → 🔄 → ✅
3. P0 tasks must be completed before starting P1
4. Deferred features have explicit triggers
-->
