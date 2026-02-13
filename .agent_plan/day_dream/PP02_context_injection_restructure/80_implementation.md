---
project: "PP02 — Context Injection Files Restructuring"
current_phase: 2
phase_name: "Migration Execution"
status: DONE
start_date: "2026-02-13"
last_updated: "2026-02-13"
p2_duration: "Heavy (max 5 slots)"
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

**Goal:** *"Create 9 new skill folders using progressive disclosure pattern, restructure 1 existing skill (writing-flows), and deprecate old instruction files with thin stubs that preserve applyTo auto-injection."*
**Phase Status:** ✅ `[DONE]`

**Duration:** ■■■■■□□□ Heavy (max 5 slots)

### Scope

Create 10 skills total (9 new + 1 restructure) organized by owning agent. All skills follow the progressive disclosure pattern:

```
skill-name/
├── SKILL.md            ← Principles + SOP + workflow (< 500 lines)
├── references/         ← Syntax specs, format tables, detailed docs
└── assets/             ← Templates, examples, pyproject format
```

**Arch-owned (implementation):**
1. `module-dev` — from `module_development.instructions.md`. Chain-loads `mcp-module-dev` for MCP work.
2. `mcp-module-dev` — from `mcp_development.instructions.md`. FastMCP patterns + MCP pyproject template.
3. `cli-dev` — from module-local `cli_manager.instructions.md`. CLI architecture + decorator patterns.

**Smith-owned (authoring):**
4. `writing-agents` — from `agents_format.instructions.md`. Format spec in references/, agent template in assets/.
5. `writing-instructions` — from `instructions_format.instructions.md`. Same pattern.
6. `writing-prompts` — from `prompts_format.instructions.md`. Same pattern.
7. `module-instructions` — from `module_instructions.instructions.md`. Same pattern.
8. `writing-flows` (RESTRUCTURE) — SKILL.md < 500 lines, syntax/format detail to references/, agent flow template to assets/.

**San-owned:**
9. `hyper-san-output` — from `hyper_san_output.instructions.md`. Output contract + procedure.

**Multi-agent (companion skill):**
10. `modules-readme` — from `modules_readme.instructions.md`. Serves HyperSmith+HyperDream so instruction STAYS, but SOP/procedure portion extracted into companion skill.

### Deprecation Strategy

Old instruction source files become thin stubs:
- Add `deprecated: true` + `superseded_by: skill-name` in YAML frontmatter
- Retain `applyTo` glob so auto-injection still fires
- Body replaced with one-line directive: `Load skill \`{name}\` for full content`
- `adhd r -f` still syncs stubs (valid instructions, just minimal)
- **No dual-content** — full content lives ONLY in the skill

### Exit Gate

- [x] All 10 skill folders exist with SKILL.md + appropriate `references/` and `assets/`
- [x] `module-dev` SKILL.md references `mcp-module-dev` for MCP work
- [x] `writing-flows` restructured (SKILL.md < 500 lines, syntax moved to `references/`)
- [x] All deprecated instruction files have thin stubs with `applyTo` preserved
- [x] `adhd r -f` compiles successfully — skills synced, no dual-content

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ✅ | Create `module-dev` skill with progressive disclosure structure | `instruction_core` | `[KNOWN]` |
| ✅ | Create `mcp-module-dev` skill, chain-loaded by `module-dev` | `instruction_core` | `[KNOWN]` |
| ✅ | Create `cli-dev` skill from module-local `cli_manager` instruction | `instruction_core` | `[KNOWN]` |
| ✅ | Create 4 Smith-owned skills (`writing-agents`, `writing-instructions`, `writing-prompts`, `module-instructions`) | `instruction_core` | `[KNOWN]` |
| ✅ | Restructure `writing-flows` with `references/` and `assets/` subdirs | `instruction_core` | `[KNOWN]` |
| ✅ | Create `hyper-san-output` skill | `instruction_core` | `[KNOWN]` |
| ✅ | Create `modules-readme` skill (companion to multi-agent instruction) | `instruction_core` | `[KNOWN]` |
| ✅ | Deprecate old instruction files with thin stubs (`applyTo` preserved) | `instruction_core` | `[KNOWN]` |
| ✅ | Run `adhd r -f` and verify: skills synced, stubs compiled, no dual-content | verification | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `ls modules/dev/instruction_core/data/skills/module-dev/` | SKILL.md, assets/, references/ |
| `wc -l modules/dev/instruction_core/data/skills/writing-flows/SKILL.md` | < 500 lines |
| `grep "deprecated: true" modules/dev/instruction_core/data/instructions/modules/module_development.instructions.md` | Match found |
| `adhd r -f` | Clean compile, exit 0 |

### P2 Completion Checklist

- [x] Exit gate met — all skills created, `writing-flows` restructured
- [x] All deprecated files have thin stubs with `applyTo`
- [x] No dual-content (content in skill only, not instruction)
- [x] `module-dev` → `mcp-module-dev` chain working
- [x] Manual verification steps pass
- [x] Refresh verification note (2026-02-13): `adhd r -f` succeeded — 21 skills synced, 9 deprecated stubs compiled, `writing-flows/SKILL.md` = 165 lines

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
