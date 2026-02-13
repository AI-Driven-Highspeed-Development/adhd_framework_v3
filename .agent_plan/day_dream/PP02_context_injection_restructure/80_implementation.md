---
project: "PP02 — Context Injection Files Restructuring"
current_phase: 2
phase_name: "Migration Execution"
status: WIP
start_date: "2026-02-13"
last_updated: "2026-02-13"
---

# 80 — Implementation Plan

> Part of [PP02 — Context Injection Files Restructuring](./_overview.md)

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

## ⚙️ Phase 0: Usage Audit

**Goal:** *"Produce a two-scope usage audit: (A) centralized source inventory (11) and (B) runtime-visible inventory (17 acceptance scope), then classify each runtime-visible file as STAY or MIGRATE."*
**Phase Status:** ✅ `[DONE]`

**Duration:** ■■□□□□□□ Light (max 2 slots)

### Exit Gate

- [x] Classification matrix exists with explicit two-scope inventory and 17-file runtime acceptance scope
- [x] Each runtime-visible file marked STAY or MIGRATE with consumer list and rationale

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ✅ | Inventory centralized source `.instructions.md` files in `instruction_core/data/instructions/` (baseline = 11) | `instruction_core` | `[KNOWN]` |
| ✅ | Inventory runtime-visible `.github/instructions/*.instructions.md` and resolve acceptance scope (17) | `instruction_core` | `[KNOWN]` |
| ✅ | Build classification matrix: file → consumers → STAY/MIGRATE → rationale | `PP02` | `[KNOWN]` |
| ✅ | Identify module-local instruction boundary (excluded from migration per consensus) | all modules | `[KNOWN]` |

### Final Classification (P0 Output)

See: `p00_usage_audit/01_usage_audit_matrix.md`

| Instruction File | Consumers | Final Decision |
|------------------|-----------|----------------|
| `adhd_framework_context` | All agents | STAY (framework philosophy) |
| `agent_common_rules` | All agents | STAY (universal rules) |
| `agents_format` | HyperSmith | MIGRATE → skill |
| `cli_manager` | HyperArch | MIGRATE → skill |
| `config_manager` | HyperArch, HyperSan | STAY |
| `exceptions` | HyperArch, HyperSan | STAY |
| `flow_format` | HyperSmith | MIGRATE → skill |
| `hyper_san_output` | HyperSan | MIGRATE → skill |
| `instructions_format` | HyperSmith | MIGRATE → skill |
| `logger_util` | HyperArch, HyperSan | STAY |
| `mcp_development` | HyperArch | MIGRATE → skill |
| `module_development` | HyperArch | MIGRATE → skill |
| `module_instructions` | HyperSmith | MIGRATE → skill |
| `modules_readme` | HyperSmith, HyperDream | STAY |
| `non_vibe_code` | HyperArch, HyperSan | STAY |
| `prompts_format` | HyperSmith | MIGRATE → skill |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ❌ Max 5 tasks (currently 4)
- ❌ Must fit within slot budget (≤1 slot)
- ❌ **No files are moved or edited in P0** — audit only

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Open classification matrix | Two inventories documented (11 centralized baseline, 17 runtime acceptance) with STAY/MIGRATE + rationale |
| Cross-check 3 random MIGRATE entries against scope rule | Each maps to single-agent workflow rationale |

### P0 Completion Checklist

- [x] Exit gate met — classification matrix complete
- [x] Two-scope audit complete (11 centralized baseline; 17 runtime acceptance scope)
- [x] P0 outputs are documentation-only artifacts
- [x] Manual verification steps pass

---

## 🏗️ Phase 1: Taxonomy Documentation

**Goal:** *"Document the 3-axis taxonomy, the 'context injection files' umbrella term, and the decision rule as a framework-level instruction."*
**Phase Status:** ✅ `[DONE]`

**Duration:** ■■□□□□□□ Light (max 2 slots)

### Exit Gate

- [x] Taxonomy instruction file exists at `instruction_core/data/instructions/framework/`
- [x] `adhd r -f` syncs it to `.github/instructions/` without errors

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ✅ | Author `context_injection_taxonomy.instructions.md` with 3-axis definitions, decision rule, and examples | `instruction_core` | `[KNOWN]` |
| ✅ | Add `applyTo` glob targeting all file types (`**/*.md`, `**/*.py`) for universal visibility | `instruction_core` | `[KNOWN]` |
| ✅ | Run `adhd r -f` and verify file syncs to `.github/instructions/` | `instruction_core` | `[KNOWN]` |

### Key Content for Taxonomy File

```
Context Injection Files (umbrella term):
├── .agent.md    → PERSPECTIVE axis  (personality, tone, stopping rules)
├── .instructions.md → TRUTH axis    (framework specs, formats, principles)
└── SKILL.md     → PROCEDURE axis    (SOPs, workflows, step-by-step guides)

Decision Rule:
  Instruction → Skill  IFF  exclusively consumed by one agent's workflow.
  Multi-agent applyTo  →  stays instruction.
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `cat .github/instructions/context_injection_taxonomy.instructions.md` | File exists with 3-axis definitions |
| `adhd r -f` | Clean compilation, no errors |

### P1 Completion Checklist

- [x] Exit gate met — taxonomy file exists and syncs
- [x] Decision rule is clear, unambiguous, and includes examples
- [x] Manual verification steps pass
- [x] Refresh verification note (2026-02-13): `adhd r -f` succeeded and `.github/instructions/context_injection_taxonomy.instructions.md` is synced

---

## 🔧 Phase 2: Migration Execution

**Goal:** *"For each MIGRATE-classified file: create skill folder, move content, add deprecated marker to old instruction, update agent flow files to reference the new skill."*
**Phase Status:** ⏳ `[TODO]` *(not started)*

**Duration:** ■■■□□□□□ Standard (max 3 slots)

### Exit Gate

- [ ] All MIGRATE files have corresponding skill folders in `instruction_core/data/skills/`
- [ ] All old instruction files have `deprecated: true` + `superseded_by:` in YAML frontmatter
- [ ] `adhd r -f` excludes deprecated files and compiles new skills correctly

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | For each MIGRATE file: create `instruction_core/data/skills/{name}/SKILL.md` with migrated content | `instruction_core` | `[KNOWN]` |
| ⏳ | Add YAML frontmatter `deprecated: true` + `superseded_by: {skill-name}` to each old instruction source | `instruction_core` | `[KNOWN]` |
| ⏳ | Update agent `.flow` files: replace `+./instructions/{file}` with skill imports | `instruction_core` | `[KNOWN]` |
| ⏳ | Verify `adhd r -f` compiles — deprecated files excluded, new skills synced | `instruction_core` | `[KNOWN]` |
| ⏳ | Spot-check 2 agents: confirm they receive the new skill content, not the old instruction | verification | `[KNOWN]` |

### Transition Safety Protocol

```
For each MIGRATE file:
1. CREATE  .../skills/{name}/SKILL.md  (new home)
2. ADD     deprecated: true + superseded_by: {name}  (old file frontmatter)
3. UPDATE  agent .flow files  (reference new skill)
4. RUN     adhd r -f  (verify no dual-visibility)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `adhd r -f` | Clean compile, no warnings about deprecated files |
| `grep -r "deprecated: true" instruction_core/data/instructions/` | Lists only MIGRATE files |
| Open compiled agent `.md` — check for skill reference | New skill content present, old instruction absent |

### P2 Completion Checklist

- [ ] Exit gate met — all skills created, all old files deprecated
- [ ] No dual-visibility (deprecated files excluded from sync)
- [ ] Agent flow files updated
- [ ] Manual verification steps pass

---

## 🧹 Phase 3: Deprecation Cleanup & Verification

**Goal:** *"Remove deprecated instruction files, verify `adhd r -f` compiles cleanly, verify no agent lost context coverage."*
**Phase Status:** ⏳ `[TODO]` *(not started)*

**Duration:** ■■□□□□□□ Light (max 2 slots)

### Exit Gate

- [ ] Zero deprecated instruction files remain in `instruction_core/data/instructions/`
- [ ] `adhd r -f` compiles with zero errors and zero warnings
- [ ] Every agent's compiled output has equivalent or better context coverage

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | Delete all `deprecated: true` instruction source files | `instruction_core` | `[KNOWN]` |
| ⏳ | Run `adhd r -f` — verify clean compilation | `instruction_core` | `[KNOWN]` |
| ⏳ | Diff each agent's compiled `.agent.md` before/after — confirm no lost sections | verification | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `grep -r "deprecated" instruction_core/data/instructions/` | No matches |
| `adhd r -f` | Clean compile, exit 0, no warnings |
| Compare agent `.md` file sizes before vs after | Sizes comparable (±10%) — no large drops |

### P3 Completion Checklist

- [ ] Exit gate met — zero deprecated files, clean compilation
- [ ] Coverage audit confirms no agent lost context
- [ ] Manual verification steps pass

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-13 | 3-axis taxonomy (agent/instruction/skill) | Clear separation of concerns; each axis has distinct purpose | 4-agent consensus |
| 2026-02-13 | Instruction → skill IFF single-agent consumer | Multi-agent instructions must remain universally available | 4-agent consensus |
| 2026-02-13 | `deprecated: true` YAML marker for transition | Compile-time exclusion prevents dual-visibility confusion | 4-agent consensus |
| 2026-02-13 | No dual-visibility period | Ambiguity about source of truth causes more harm than brief transition risk | 4-agent consensus |
| 2026-02-13 | Module-local instructions stay in module dirs | Edit-location rule preserved; these aren't centralized files | 4-agent consensus |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| — | — | No cuts yet |

---

**← Back to:** [_overview.md](./_overview.md)
