---
name: day-dream
description: "Vision and planning workflows — creating blueprint plans, architecture assets, and day-dream documents for the ADHD Framework. Covers tier selection (Simple vs Blueprint), plan types (SP/PP), document authoring rules, Story/Spec pattern, status syntax, dependency tracking, invalidation protocol, knowledge gaps, Module Index gate, State Deltas, phasing rules, natural verification, and validation checklists. Use this skill when creating visions, roadmaps, blueprints, or planning new features."
---

# Day Dream

Blueprint authoring and vision planning for the ADHD Framework.

## When to Use
- Creating a new blueprint (day-dream) plan
- Authoring feature specs, architecture docs, or implementation plans
- Building supporting assets (diagrams, data models, mockups)
- Adding dependency tracking, knowledge gaps, or invalidation metadata
- Understanding document line limits, phasing rules, and verification requirements

---

## Tier Selection

| Tier | Use When | Template |
|------|----------|----------|
| **Simple** | ≤2 features, single module, no external APIs | `simple.template.md` |
| **Blueprint** | ≥3 features OR ≥2 cross-module deps OR external APIs | `blueprint/` folder |

Human override can force tier in either direction.

### Magnitude Routing

After selecting a tier, assess **magnitude** (Trivial → Epic) to determine planning depth:

| Tier + Magnitude | Route |
|------------------|-------|
| Simple + Trivial/Light | Execute directly — no planning document needed |
| Simple + Standard | Single plan file, execute in-session |
| Blueprint + Light/Standard | Blueprint docs, execute sequentially |
| Blueprint + Heavy | Blueprint docs, decompose into plan/task tree |
| Blueprint + Epic | Blueprint docs, mandatory decomposition, parallel agents |

> **Full magnitude table and decomposition protocol:** See the `dream-planning` skill.

---

## Templates Location

All templates at: `.agent_plan/day_dream/_templates/`

### Simple Tier

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `simple.template.md` | Single-file vision + quick start | ≤200 lines |

### Blueprint Tier

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `blueprint/overview.template.md` | `_overview.md` scaffold with full frontmatter | ≤100 lines |
| `blueprint/task.template.md` | Leaf task scaffold | ≤100 lines |
| `blueprint/00_index.template.md` | Navigation hub with flowchart | ≤150 lines |
| `blueprint/01_executive_summary.template.md` | Vision, goals, non-goals (System Plan) | ≤150 lines |
| `blueprint/01_summary.template.md` | Merged summary + architecture (Procedure Plan) | ≤200 lines |
| `blueprint/02_architecture.template.md` | System diagrams, components | ≤200 lines |
| `blueprint/NN_feature.template.md` | Full feature spec (≥3 modules or ext API) | ≤150 lines |
| `blueprint/NN_feature_simple.template.md` | Lightweight feature (80% of cases) | ≤100 lines |
| `blueprint/80_implementation.template.md` | Phased roadmap with 8-slot verification | ≤200 lines/phase |
| `blueprint/81_module_structure.template.md` | Reusable vs project-specific modules | ≤150 lines |
| `blueprint/82_cli_commands.template.md` | CLI interface and command reference | ≤150 lines |
| `blueprint/99_references.template.md` | External links | No limit |
| `blueprint/modules/module_spec.template.md` | Module implementation spec | ≤200 lines |

### Assets

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `assets/asset.template.md` | Non-code artifacts | ≤100 lines (excl. diagrams) |

**Asset Types:** `mockup`, `diagram`, `storyboard`, `infrastructure`, `design`, `data-model`, `other`
**Naming:** `{feature_id}_{description}.asset.md`

---

## Status Syntax

| Marker | Meaning |
|--------|---------|
| ⏳ `[TODO]` | Not started |
| 🔄 `[WIP]` | In progress |
| ✅ `[DONE]` | Complete |
| ✅ `[DONE:invalidated-by:XXnn]` | Complete but assumptions compromised by plan `XXnn` |
| 🚧 `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 `[CUT]` | Removed from scope |

---

## Difficulty Labels

| Label | Meaning | P0 Allowed? |
|-------|---------|-------------|
| `[KNOWN]` | Standard patterns, proven libraries | ✅ Yes |
| `[EXPERIMENTAL]` | Needs validation in our context | ⚠️ Conditional |
| `[RESEARCH]` | Active problem, no proven solution | ❌ NEVER in P0 |

---

## The Story → Spec Pattern

Every blueprint document MUST follow this two-part structure:

```markdown
## 📖 The Story
{Visual, scannable narrative — NOT a text wall}

---

## 🔧 The Spec
{Technical specification}
```

### Story Section Required Subsections

| Subsection | Purpose | Format |
|------------|---------|--------|
| 😤 **The Pain** | What's broken, who hurts | ASCII box + pain table |
| ✨ **The Vision** | What success looks like | ASCII box showing flow |
| 🎯 **One-Liner** | Elevator pitch | Single blockquote |
| 📊 **Impact** | Before/After metrics | Comparison table |

**If you can't draw the pain and vision, you don't understand the feature.**

---

## Document Rules & Line Limits

| Document | Required When | Line Limit |
|----------|---------------|------------|
| `_overview.md` | Every plan directory | ≤100 lines |
| `01_executive_summary.md` | Blueprint, System Plan | ≤150 lines |
| `01_summary.md` | Blueprint, Procedure Plan | ≤200 lines |
| `02_architecture.md` | System Plan with ≥3 modules/cross-module/ext API | ≤200 lines |
| `80_implementation.md` | Blueprint tier | ≤200 lines per phase |
| `81_module_structure.md` | System Plan, ADHD projects | ≤150 lines |
| Feature (full) | ≥3 modules, external APIs, P0 | ≤300 lines |
| Feature (simple) | ≤2 modules, no ext APIs | ≤100 lines |
| Task file | Any leaf task | ≤100 lines |
| Asset file | Supporting artifact | ≤100 lines (excl. diagrams) |

### Children Table Schema

The Children table in `_overview.md` has exactly 4 columns:

| Column | Description |
|--------|-------------|
| Name | File or directory name |
| Type | `Plan` (directory with `_overview.md`) or `Task` (single `.md` file) |
| Status | Status marker (⏳ [TODO], 🔄 [WIP], ✅ [DONE], etc.) |
| Description | One-line summary |

⚠️ **Type column values: ONLY `Plan` or `Task` are valid.** Values like 'Doc', 'Feature', 'Module', etc. are INVALID per §1.2's two-primitive rule.

### Authoring Rules

| Rule | Detail |
|------|--------|
| **Mandatory Skeleton** | Sections are present; write "N/A — [reason]" for inapplicable. Do NOT mark optional |
| **Executive Summary** | TL;DR max 3 sentences. Prior Art required. Non-Goals min 3. Max 5 P0 features. Freeze with 🔒 FROZEN |
| **Acceptance Criteria** | Task files MUST include `## Acceptance Criteria` with checkbox lists |
| **Custom Sections** | Prefix: `## [Custom] 🎨 Title`. Max 5 per doc. Prohibited: P0 tasks, blocking deps, arch changes |
| **Deep Dive** | `## 🔬 Deep Dive` only for algorithms, API contracts, error handling. Delete for straightforward features |
| **Clean-Code-First** | Delete wrong code, refactor fully, one correct path. Never try/catch fallbacks |

---

## Phasing Rules

| Phase | Constraint |
|-------|-----------|
| **P0 (Walking Skeleton)** | Max 5 tasks, max 5 slots, `[KNOWN]` only. Working passthrough/stub. NO complex logic |
| **P1 (First Enhancement)** | Add ONE simple heuristic or feature. Validate before adding more |
| **P2+** | Gradually layer complexity. Each phase independently deployable |

**Anti-Premature-Optimization:** If you cannot describe each P0 component in one sentence without the word "and," it's too complex. Split or defer.

---

## Natural Verification

Every implementation phase MUST have a `### How to Verify (Manual)` section:

- Max 3 human-executable steps
- Expected outcome for each step
- Steps MUST complete in <30 seconds

---

## Dependency Tracking

Plan-level `depends_on:` and `blocks:` fields in `_overview.md` frontmatter track structural relationships between plans.

| Rule | Detail |
|------|--------|
| **Plan-level only** | Never on individual tasks or phases |
| **DAG required** | No cycles. `dream validate` rejects cycles |
| **Bidirectional** | If A `depends_on: B`, then B SHOULD have `blocks: A` |
| **RECOMMENDED** | Omission triggers `dream validate` warning for cross-plan modifications |
| **Structural ≠ temporal** | `depends_on:` = permanent design relationship. `🚧 [BLOCKED:]` = transient obstacle |

A plan can have `depends_on:` AND not be BLOCKED (dependency met). A plan can be BLOCKED without `depends_on:` (external delay).

---

## Invalidation Protocol

When a plan's completion retroactively compromises assumptions of a previously-completed plan:

| Rule | Detail |
|------|--------|
| Only ✅ DONE plans can be invalidated | Cannot invalidate unbuilt work |
| `invalidation_scope` required | State WHAT is compromised, not just "partially invalidated" |
| Causing plan reports at closure | Invalidations listed in closure gate |
| **Parent writes to victim** | Sibling firewall compliance — causing agent NEVER writes to victim plan |
| Status variant | `✅ [DONE:invalidated-by:XXnn]` for scannable tree-level visibility |

**Frontmatter fields (written in victim plan's `_overview.md`):**

```yaml
invalidated_by: PP08_polyglot_persistence
invalidation_scope: storage_implementation
invalidation_date: 2025-09-15
```

---

## Knowledge Gaps

Source of truth: `knowledge_gaps:` frontmatter array in plan `_overview.md` and module spec frontmatter. The inline prose marker `⚠️ [KNOWLEDGE GAP]` remains valid for readability but is NOT the source of truth.

```yaml
knowledge_gaps:
  - "X12 EDI format expertise departed with Carlos"
  - "DynamoDB partition key strategy for high-cardinality events"
```

| When to Add | Example |
|-------------|---------|
| Key person departs | Sole expert on subsystem leaves |
| Domain expertise missing | No one understands X12 EDI |
| Unvalidated assumption | "We assume 10K writes/sec" |
| External dependency unknown | API rate limits undocumented |

**Resolution:** Remove from array when expertise is acquired or validated. Add a State Delta entry noting the resolution.

---

## Module Index Gate

The Module Index (table in root `_overview.md`) maps every module to its origin plan. A phase introducing a new module CANNOT mark ✅ DONE until:

1. **Table row exists** — module has a row in root Module Index
2. **Spec file exists** — `.md` spec file on disk at the referenced path

Both conditions are hard gates. Missing either = plan cannot close.

### Module Spec Frontmatter

```yaml
---
module: checkout
last_updated: 2025-09-15
modified_by_plans:
  - PP02_checkout_redesign
knowledge_gaps:
  - "Payment retry logic under partial failure"
---
```

---

## State Deltas

Append-only entries in root `_overview.md` logging codebase changes when a plan closes. **Gate condition** — a plan CANNOT mark ✅ DONE without appending one.

```markdown
## State Deltas

### ✅ PP02_checkout_redesign — Sep 2025
- checkout: linear flow → reservation-based state machine
- inventory_sync: new module, pessimistic locking + TTL
```

| Rule | Detail |
|------|--------|
| Active cap | 20 most recent entries in root `_overview.md` |
| Overflow | Oldest moves to `_state_deltas_archive.md` (auto-generated, NEVER hand-maintained) |
| Format | `{module}: {what changed}` per line |

---

## Plan Closure Gates

When marking a plan ✅ DONE or 🚫 CUT:

| Gate | Detail |
|------|--------|
| All children resolved | Every child ✅ DONE or 🚫 CUT |
| State Delta appended | Entry in root `_overview.md` |
| Module Index updated | New modules: table row AND spec file |
| `last_updated` updated | In plan's frontmatter |
| Invalidations reported | List compromised plans |
| Plan archived | Moved to `_completed/YYYY-QN/` |
| `dream validate` passes | Auto-triggered before closure (protocol requirement) |

---

## Estimation Defaults

All durations use AI-agent time unless `human_only: true`:

| Magnitude | AI-Agent Time |
|-----------|---------------|
| Trivial | 5–15 minutes |
| Light | 15–60 minutes |
| Standard | 1–4 hours |
| Heavy | 4–8 hours |
| Epic | Must decompose |

Mark tasks with `human_only: true` when they require human action (UX judgment, stakeholder approval, manual testing of physical devices).

---

## Folder Structure

### Blueprint Tier

```
.agent_plan/day_dream/
├── _overview.md                    ← Root navigator
├── _tree.md                        ← Generated folder tree (NEVER hand-edit)
├── _state_deltas_archive.md        ← Overflow State Deltas (auto-generated)
│
├── SP01_{plan_name}/               ← System Plan
│   ├── _overview.md                ← REQUIRED navigator with frontmatter
│   ├── 01_executive_summary.md
│   ├── 02_architecture.md
│   ├── 0N_feat_{feature}.md        ← feat_ prefix RECOMMENDED
│   ├── 80_implementation.md
│   ├── 81_module_structure.md
│   ├── pNN_{phase}/
│   │   ├── _overview.md
│   │   └── NN_{task}.md
│   ├── modules/
│   └── assets/
│
├── PP02_{plan_name}/               ← Procedure Plan
│   ├── _overview.md
│   ├── 01_summary.md               ← Merged exec summary + architecture
│   ├── 0N_feat_{step_name}.md
│   ├── 80_implementation.md
│   └── pNN_{phase}/
│
├── _completed/                     ← Archive (YYYY-QN/ subdirs)
├── exploration/                    ← Research docs (max 3 active, 14-day expiry)
│   └── _archive/
└── _templates/                     ← Plan templates (read-only, infrastructure)
```

### Phase Naming
- `pNN_name/` — zero-padded two digits, underscore separator
- Phases are ALWAYS directories (even single-task)
- Task numbering: `NN_{name}.md` starting at `01_`
- No `feat_` prefix on task files — that prefix is for plan-root feature files only

---

## Walking Skeleton

Opt-in, not default.

| When Required | When to Skip |
|---------------|-------------|
| Cross-boundary integration risk | Single-module changes |
| External API dependency | Skill/template/doc edits |
| 3+ module data flow | Self-contained features |
| — | Magnitude ≤ Light |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| `[RESEARCH]` in P0 | Defer to P1+ or resolve in exploration |
| Exceed line limits | Split into separate files |
| Edit frozen documents | Create new version or update implementation |
| >3 active explorations | Synthesize or abandon oldest |
| Skip verification sections | Always include manual verification |
| Simple tier for complex projects | Upgrade to Blueprint when threshold met |
| Orphan assets | Always link to parent feature |
| Human-time for AI tasks | Default to AI-agent time |
| `try/catch` fallbacks for old code | Delete old code or folder-separate v1/v2 |
| Hand-edit `_tree.md` | Generated by `dream tree` only |
| Omit `origin:` in frontmatter | Every plan traces to its trigger doc |

---

## Cross-References

| Topic | Where |
|-------|-------|
| Magnitude routing & decomposition | `dream-planning` skill |
| Plan/task hierarchy & frontmatter schema | `dream-planning` skill |
| MANAGER/WORKER lifecycle & closure gates | `dream-planning` skill |
| Sibling firewall & context isolation | `dream-planning` skill |
| Template catalog & format | `writing-templates` skill |
| Orchestrator dispatch mechanics | `orch-routing` skill |
| Implementation quality gates | `orch-implementation` skill |
