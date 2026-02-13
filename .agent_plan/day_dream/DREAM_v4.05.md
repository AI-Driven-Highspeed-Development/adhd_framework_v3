# DREAM v4.05 — Unified Planning System Specification

**Version:** 4.05  
**Date:** 2026-02-12  
**Status:** ✅ Authoritative

DREAM (Decomposition Rules for Engineering Atomic Modules) is a protocol for breaking complex work into atomic, parallelizable units that AI agents execute independently. It defines how to assess complexity (8-slot magnitude routing), how to structure plans (filesystem hierarchy with `_overview.md` convention), how agents coordinate (sibling firewall + MANAGER/WORKER lifecycle), and how tooling enforces conventions (`dream_mcp`).

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Plan Anatomy](#2-plan-anatomy)
3. [Module Index](#3-module-index)
4. [State Deltas](#4-state-deltas)
5. [Module History](#5-module-history)
6. [Dependency Graph](#6-dependency-graph)
7. [Invalidation Protocol](#7-invalidation-protocol)
8. [Knowledge Gaps](#8-knowledge-gaps)
9. [Priority & Emergency](#9-priority--emergency)
10. [Folder Conventions](#10-folder-conventions)
11. [Context Isolation & Sibling Firewall](#11-context-isolation--sibling-firewall)
12. [MANAGER/WORKER Lifecycle](#12-managerworker-lifecycle)
13. [`dream_mcp` Target Specification](#13-dream_mcp-target-specification)
14. [Implementation Notes](#14-implementation-notes)
15. [Appendix: Templates](#15-appendix-templates)

---

## Quick Reference Card

| Concept | Rule |
|---------|------|
| **Plan** | Directory with `_overview.md` — decomposable, has children |
| **Task** | Single `.md` file — leaf, directly executable |
| **Bridge** | Plan = dir, Task = file. The only two primitives |
| **Metadata** | YAML frontmatter in `_overview.md` |
| **Status markers** | ⏳`[TODO]` · 🔄`[WIP]` · ✅`[DONE]` · ✅`[DONE:invalidated-by:XXnn]` · 🚧`[BLOCKED:reason]` · 🚫`[CUT]` |
| **Difficulty labels** | `[KNOWN]` · `[EXPERIMENTAL]` · `[RESEARCH]` (never in P0) |
| **Magnitudes** | Trivial(1) · Light(2) · Standard(3) · Heavy(5) · Epic(8) — slot MAXIMUMS |
| **Tiers** | Simple (≤2 features, no APIs) · Blueprint (≥3 features OR cross-module OR external APIs) |
| **Plan types** | System Plan (architecture + features) · Procedure Plan (workflow + steps) |
| **Plan folder prefix** | `SP01_` (System Plan) · `PP01_` (Procedure Plan) — creation-order number, IMMUTABLE |
| **Sibling firewall** | Siblings NEVER read/write each other's content. Coordinate through parent only |
| **Max parallel agents** | 5 |
| **P0 hard limits** | Max 5 tasks, `[KNOWN]` only, ≤5 slots |
| **Plan closure gate** | State Delta + Module Index (table row AND spec file) + invalidation report |
| **Dependencies** | `depends_on:` / `blocks:` plan-level frontmatter. RECOMMENDED for any plan with cross-plan relationships |
| **Priority** | `normal` (default, omit) · `emergency` (supersedes in-progress plans, requires `emergency_declared_at:`) |
| **Knowledge gaps** | `knowledge_gaps:` frontmatter string array (source of truth) |
| **Invalidation** | `invalidated_by:` in victim plan frontmatter. Written by parent/orchestrator, never by sibling |
| **State Delta cap** | 20 entries in root `_overview.md`. Overflow → `_state_deltas_archive.md` |
| **`dream_mcp`** | P0: `status`, `tree`, `stale`, `validate`. P1: `impact`, `history`, `emergency`, `archive`. P2: `hypothetical impact`, proactive gap detection |
| **Timestamp precision** | Human: `YYYY-MM-DD`. Machine (`dream_mcp`): ISO 8601 `YYYY-MM-DDTHH:MM:SS` |
| **Human authority** | Human decides WHETHER to plan. DREAM decides the FORMAT |

---

## 1. Core Concepts

### 1.1 What DREAM Is

DREAM governs **decomposition and coordination** — how work breaks into units and how agents operate on those units without corrupting each other. It does not govern coding style, testing strategy, or deployment.

### 1.2 The Two Primitives

| Primitive | Representation | Has Children? | Required File |
|-----------|---------------|---------------|---------------|
| **Plan** | Directory | Yes | `_overview.md` |
| **Task** | Single `.md` file | No | — |

Every DREAM artifact is one of these. A plan decomposes into children (plans or tasks). A task is a leaf — directly executable by a single agent in a single session.

### 1.3 Magnitude Routing

Magnitude is assessed FIRST. It determines whether decomposition is needed and constrains plan structure.

```
■□□□□□□□  Trivial   max 1 slot   ≤1 hour    Execute immediately
■■□□□□□□  Light     max 2 slots  ≤2 hours   Execute directly
■■■□□□□□  Standard  max 3 slots  ≤3 hours   Decompose if ≥3 subtasks
■■■■■□□□  Heavy     max 5 slots  ≤5 hours   SHOULD decompose
■■■■■■■■  Epic      max 8 slots  ≤8 hours   MUST decompose
```

Each slot ≈ 1 hour AI-agent time. Values are MAXIMUMS.

**Routing rules:**

| Magnitude | Action | Agent Role |
|-----------|--------|------------|
| Trivial / Light | Execute directly | WORKER |
| Standard (≥3 subtasks or cross-module) | Decompose | MANAGER |
| Standard (<3 subtasks, single module) | Execute directly | WORKER |
| Heavy | SHOULD decompose | MANAGER |
| Epic | MUST decompose. Epic at task level → REFUSE and escalate | MANAGER |

**Assessment signals (agent judgment, not rigid checklist):**

| Signal | Points Toward |
|--------|--------------|
| Single file change | Trivial/Light |
| Multiple files, one module | Light/Standard |
| Cross-module changes | Standard/Heavy |
| New module or external API | Heavy/Epic |
| Ambiguity in requirements | Standard+ (needs decomposition) |

### 1.4 Tier Selection

| Tier | Use When | Template |
|------|----------|----------|
| **Simple** | ≤2 features, single module, no external APIs | `simple.template.md` |
| **Blueprint** | ≥3 features OR ≥2 cross-module deps OR external APIs | `blueprint/` folder |

Human override can force tier in either direction.

### 1.5 Plan Types

| Plan Type | Use When | Prefix | Key Difference |
|-----------|----------|--------|----------------|
| **System Plan** | Building/extending software architecture | `SP` | Separate `01_executive_summary.md` + `02_architecture.md` |
| **Procedure Plan** | Workflow, migration, operational process | `PP` | Merged `01_summary.md` (exec summary + architecture co-evolve) |

**Tiebreaker:** Triggered by existing plan AND primary deliverable modifies existing code → Procedure Plan.

### 1.6 Plan Lifecycle

```
ASSESS     → Classify magnitude
SELECT     → Pick tier (Simple/Blueprint) and type (SP/PP)
AUTHOR     → Create plan artifacts per tier rules
EXECUTE    → MANAGER decomposes, WORKER implements
CLOSE      → Satisfy gate conditions (§4, §3), archive to _completed/
```

### 1.7 Planning Authority

Human decides WHETHER to plan. DREAM decides HOW to plan (tier, type, structure). Agents do NOT decide whether planning happens. Human override suppresses auto-format-detection.

### 1.8 Status Syntax

| Marker | Meaning |
|--------|---------|
| ⏳ `[TODO]` | Not started |
| 🔄 `[WIP]` | In progress |
| ✅ `[DONE]` | Complete |
| ✅ `[DONE:invalidated-by:XXnn]` | Complete but assumptions retroactively compromised by plan `XXnn` |
| 🚧 `[BLOCKED:reason]` | Stuck (kebab-case reason, e.g., `[BLOCKED:waiting-on-api]`) |
| 🚫 `[CUT]` | Removed from scope |

### 1.9 Difficulty Labels

| Label | Meaning | P0 Allowed? |
|-------|---------|-------------|
| `[KNOWN]` | Standard patterns, proven libraries | ✅ Yes |
| `[EXPERIMENTAL]` | Needs validation in our context | ⚠️ Conditional |
| `[RESEARCH]` | Active problem, no proven solution | ❌ NEVER in P0 |

---

## 2. Plan Anatomy

### 2.1 Frontmatter Schema

Every plan `_overview.md` has YAML frontmatter. Fields are classified as REQUIRED, RECOMMENDED, or OPTIONAL.

**REQUIRED** = plan is invalid without it. `dream validate` errors on omission.  
**RECOMMENDED** = should be present for any plan with cross-plan relationships. `dream validate` warns on omission when applicable.  
**OPTIONAL** = present only when relevant. Omit entirely when not applicable (omit, don't N/A).

| Field | Type | Classification | Description | Example |
|-------|------|---------------|-------------|---------|
| `name` | string | REQUIRED | Plan identifier (snake_case) | `core_shop` |
| `type` | enum | REQUIRED | `system` or `procedure` | `system` |
| `magnitude` | enum | REQUIRED | `Trivial` / `Light` / `Standard` / `Heavy` / `Epic` | `Heavy` |
| `status` | enum | REQUIRED | See §1.8 Status Syntax | `WIP` |
| `origin` | string | REQUIRED | Path to exploration/meeting doc that triggered this plan | `exploration/meeting_2026_02_01.md` |
| `last_updated` | date | REQUIRED | Last modification date. Human: `YYYY-MM-DD`. Machine: ISO 8601 | `2026-02-12` |
| `start_at` | date | OPTIONAL | When work began. Omit for exploratory plans not yet started | `2026-02-10` |
| `depends_on` | string[] | RECOMMENDED | Plans this plan requires to complete first. Required for any plan with structural dependencies | `[SP05_billing_engine]` |
| `blocks` | string[] | RECOMMENDED | Plans that cannot proceed until this plan completes | `[PP19_perf_optimization]` |
| `knowledge_gaps` | string[] | RECOMMENDED | Missing expertise or unvalidated assumptions. See §8 | `["X12 EDI format expertise"]` |
| `priority` | enum | OPTIONAL | `normal` (default — omit) or `emergency`. See §9 | `emergency` |
| `emergency_declared_at` | datetime | CONDITIONAL | ISO 8601 timestamp. REQUIRED when `priority: emergency`. Used for concurrent emergency ordering | `2026-02-12T10:30:00` |
| `invalidated_by` | string | CONDITIONAL | Plan that caused invalidation. Only in victim plans, written by parent/orchestrator. See §7 | `PP08_polyglot_persistence` |
| `invalidation_scope` | string | CONDITIONAL | What parts are compromised. REQUIRED when `invalidated_by` is set | `storage_implementation` |
| `invalidation_date` | date | CONDITIONAL | When invalidation was recorded. REQUIRED when `invalidated_by` is set | `2025-09-15` |

**Full frontmatter example:**

```yaml
---
name: marketplace
type: system
magnitude: Heavy
status: WIP
origin: exploration/meeting_2026_02_01_marketplace.md
start_at: 2026-02-03
last_updated: 2026-02-12
depends_on:
  - SP01_core_shop
blocks:
  - PP19_perf_optimization
knowledge_gaps:
  - "Multi-currency settlement edge cases"
---
```

### 2.2 Required `_overview.md` Content

After frontmatter, every plan `_overview.md` MUST contain:

```markdown
# {Plan Name}

## Purpose
Why this plan exists and what it delivers.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_login_flow.md | Task | ⏳ [TODO] | Login endpoint |
| auth_tokens/ | Plan | 🔄 [WIP] | Token lifecycle |

## Integration Map
How children's outputs combine into the plan's deliverable.

## Reading Order
1. 01_login_flow.md (independent)
2. auth_tokens/ (depends on login)
```

### 2.3 Root `_overview.md` — Extended Sections

The root `_overview.md` (at `.agent_plan/day_dream/_overview.md`) has additional required sections.

**Write access restriction:** Only the root MANAGER or `dream_mcp` writes to this file. Individual agents update their own plan's `status:` frontmatter only.

| Section | Position | Purpose |
|---------|----------|---------|
| `## Current Sprint` | FIRST content section | 3–5 bullets of actively worked items |
| `## Plans` | After Current Sprint | All plans with type, status, priority, dependencies |
| `## Module Index` | After Plans | See §3 |
| `## State Deltas` | LAST section | Append-only changelog, capped at 20. See §4 |

**Plans table schema:**

| Column | Content |
|--------|---------|
| Name | Plan ID with prefix (e.g., `SP01_core_shop`) |
| Type | System / Procedure |
| Status | Status marker |
| Priority | `emergency` or `—` |
| Depends On | Plan IDs or `—` |
| Description | One-line summary |

### 2.4 Plan Type — File Presence Matrix

One folder structure, two template profiles. Only which files appear on disk differs.

| File | System Plan | Procedure Plan | Purpose |
|------|:-----------:|:--------------:|---------|
| `_overview.md` | ✅ | ✅ | Plan navigator (always required) |
| `01_executive_summary.md` | ✅ | — | Vision, goals, non-goals, prior art |
| `01_summary.md` | — | ✅ | Merged exec summary + architecture |
| `02_architecture.md` | ✅ | — | System diagrams, components |
| `0N_feat_{feature}.md` | ✅ | ✅ | Feature/step specs. `feat_` prefix RECOMMENDED — distinguishes from structural docs (`01_executive_summary`, `80_implementation`, etc.) |
| `80_implementation.md` | ✅ | ✅ | Phased roadmap with verification |
| `81_module_structure.md` | ✅ | — | Reusable vs project-specific modules |
| `82_cli_commands.md` | Optional | — | CLI interface (only if CLI exists) |
| `99_references.md` | Optional | Optional | External links |
| `modules/` | Optional | — | Module specs |
| `assets/` | Optional | Optional | Supporting artifacts |
| `pNN_{phase}/` | As needed | As needed | Phase directories |

Omitted files do NOT exist on disk. Never create a file to write "N/A."

### 2.5 Module Spec Frontmatter

Module spec files in `modules/` directories track staleness and provenance:

| Field | Type | Classification | Description |
|-------|------|---------------|-------------|
| `module` | string | REQUIRED | Module name |
| `last_updated` | date | REQUIRED | Updated when any plan modifies this module |
| `modified_by_plans` | string[] | REQUIRED | Audit trail of plans that touched this module |
| `knowledge_gaps` | string[] | RECOMMENDED | Missing expertise for this module |

```yaml
---
module: checkout
last_updated: 2025-09-15
modified_by_plans:
  - PP02_checkout_redesign
  - PP05_payment_migration
knowledge_gaps:
  - "Payment retry logic under partial failure"
---
```

### 2.6 The Story → Spec Pattern

Every blueprint document MUST follow this two-part structure:

```markdown
## 📖 The Story
{Visual, scannable narrative — NOT a text wall}

---

## 🔧 The Spec
{Technical specification}
```

**Story section required subsections:**

| Subsection | Purpose | Format |
|------------|---------|--------|
| 😤 **The Pain** | What's broken, who hurts | ASCII box + pain table |
| ✨ **The Vision** | What success looks like | ASCII box showing flow |
| 🎯 **One-Liner** | Elevator pitch | Single blockquote |
| 📊 **Impact** | Before/After metrics | Comparison table |

If you can't draw the pain and vision, you don't understand the feature.

### 2.7 Document Rules & Line Limits

| Document | Required When | Line Limit |
|----------|---------------|------------|
| `_overview.md` | Every plan directory | ≤100 lines |
| `01_executive_summary.md` | Blueprint, System Plan | ≤150 lines |
| `01_summary.md` | Blueprint, Procedure Plan | ≤200 lines |
| `02_architecture.md` | System Plan with ≥3 modules/cross-module/ext API | ≤200 lines |
| `80_implementation.md` | Blueprint tier | ≤200 lines per phase |
| `81_module_structure.md` | System Plan, ADHD projects | ≤150 lines |
| `82_cli_commands.md` | Plan has CLI commands | ≤150 lines |
| Feature (full) | ≥3 modules, external APIs, P0 | ≤300 lines |
| Feature (simple) | ≤2 modules, no external APIs | ≤100 lines |
| Task file | Any leaf task | ≤100 lines |
| Asset file | Supporting artifact | ≤100 lines (excl. diagrams) |

### 2.8 Phasing Rules

| Phase | Constraint |
|-------|-----------|
| **P0 (Walking Skeleton)** | Max 5 tasks, max 5 slots, `[KNOWN]` only. Working passthrough/stub. NO complex logic |
| **P1 (First Enhancement)** | Add ONE simple heuristic or feature. Validate before adding more |
| **P2+** | Gradually layer complexity. Each phase independently deployable |

**Anti-Premature-Optimization:** If you cannot describe each P0 component in one sentence without the word "and," it's too complex. Split or defer.

### 2.9 Natural Verification

Every implementation phase MUST have a `### How to Verify (Manual)` section:

- Max 3 human-executable steps
- Expected outcome for each step
- Steps MUST complete in <30 seconds

### 2.10 Additional Authoring Rules

| Rule | Detail |
|------|--------|
| **Executive Summary** | TL;DR max 3 sentences. `## 🔍 Prior Art & Existing Solutions` with BUY/BUILD/WRAP decisions required. Non-Goals min 3. Features max 5 P0. Freeze with 🔒 FROZEN after approval |
| **Acceptance Criteria** | Task files MUST include `## Acceptance Criteria` with checkbox lists |
| **Mandatory Skeleton** | Sections are present; write "N/A — [reason]" for inapplicable sections. Do not mark sections optional |
| **Custom Sections** | Prefix: `## [Custom] 🎨 Title`. Max 5 per document. Prohibited: P0 tasks, blocking dependencies, architecture changes |
| **Deep Dive** | Add `## 🔬 Deep Dive` only for algorithms, API contracts, error handling. Delete for straightforward features |
| **Exploration Docs** | Max 3 active. Each expires after 14 days. Archive to `exploration/_archive/` |
| **Decision Recording** | Create/modify/cut decisions MUST be recorded in exploration docs with links to affected plans |
| **Clean-Code-First** | Plans specify clean, correct code — delete wrong code, refactor fully, one correct path. Never try/catch fallbacks |
| **Asset Authoring** | Naming: `{feature_id}_{description}.asset.md`. Types: mockup, diagram, storyboard, infrastructure, design, data-model, other |
| **Estimation** | All durations use AI-agent time unless `human_only: true`. Mark human-routed tasks explicitly |
| **Walking Skeleton** | Opt-in, not default. Required: cross-boundary integration, external API, 3+ module data flow. Skip for single-module, docs, Light magnitude |

---

## 3. Module Index

The Module Index is a table in the root `_overview.md` that maps every module to its origin plan, modifying plans, and knowledge gaps.

### 3.1 Schema

| Column | Content |
|--------|---------|
| Module | Module name |
| Origin Plan | Plan that created it |
| Modified By | Plans that subsequently modified it |
| Spec File | Location of the module's `.md` spec file |
| Knowledge Gaps | Module-level gaps (from spec frontmatter) or `—` |

### 3.2 Enforcement Gate

A phase that introduces a new module CANNOT mark ✅ DONE until BOTH conditions are met:

1. **Table row exists** — module has a row in the root Module Index
2. **Spec file exists** — a `.md` spec file for the module exists on disk at the path referenced in the table

`dream validate` checks both conditions. A missing spec file with a present table row is a validation error, not a warning.

### 3.3 Registration Flow

```
Plan creates new module
  │
  ├─► Plan's MANAGER requests registration via parent
  │
  ├─► Root MANAGER / dream_mcp writes table row + verifies spec file path
  │
  └─► `dream validate` checks:
        ✓ Table row exists in Module Index
        ✓ Spec file exists on disk at referenced path
        ✗ Either missing → GATE VIOLATION (plan cannot close)
```

### 3.4 `modified_by_plans` Enforcement

`dream validate` cross-references the `modified_by_plans` field in module specs against State Delta entries. Drift between the two is reported as a warning.

---

## 4. State Deltas

State Deltas are append-only entries in the root `_overview.md` that log what changed in the codebase when a plan closes. They are a GATE CONDITION — a plan CANNOT mark ✅ DONE without appending one.

### 4.1 Format

```markdown
## State Deltas

### ✅ PP02_checkout_redesign — Sep 2025
- checkout: linear flow → reservation-based state machine
- inventory_sync: new module, pessimistic locking + TTL

### ✅ PP05_payment_migration — Nov 2025
- checkout: direct Stripe calls → PaymentProvider abstraction
- payment: new module with Stripe/PayPal/Mollie adapters
```

Each entry lists module-level changes using `{module}: {what changed}` format.

### 4.2 Cap & Archive

| Rule | Detail |
|------|--------|
| **Active cap** | Root `_overview.md` holds the 20 MOST RECENT State Delta entries |
| **Overflow** | When a 21st entry is added, the oldest is moved to `_state_deltas_archive.md` |
| **Archive file** | Auto-generated by `dream_mcp`. NEVER hand-maintained. Header: `<!-- GENERATED — managed by dream_mcp -->` |
| **Until `dream_mcp`** | Author moves oldest entry manually when adding new ones (best effort) |
| **Default cap** | 20 entries ≈ 60–100 lines. At 1 entry/week cadence: covers ~5 months. Future: configurable per project (P2) |

### 4.3 Reading State Deltas

Scan top-to-bottom for any module name. The full history of any module is visible in 30 seconds across root `_overview.md` + archive.

---

## 5. Module History

Module History is a module-indexed view alongside the chronological State Deltas. It answers "what happened to module X over time?" in a single table.

| Rule | Detail |
|------|--------|
| **Source of truth** | State Deltas remain the source of truth. Module History is a derived view |
| **Maintenance** | Auto-generated by `dream history {module}`. NEVER hand-maintained |
| **Output** | Printed to stdout or written to plan-local file (not root) |
| **Until `dream_mcp`** | Module History does not exist — use grep on State Deltas |

**Output format:**

```markdown
## Module History — audit_trail (auto-generated)

| Date | Plan | Change |
|------|------|--------|
| Feb 2025 | SP02 | Created — auth event logging to PostgreSQL |
| Sep 2025 | PP08 | PostgreSQL JSONB → DynamoDB event store |
| Nov 2025 | PP13 | DynamoDB encryption enabled (critical gap) |
```

---

## 6. Dependency Graph

### 6.1 Fields

| Field | Type | Classification | Scope | Description |
|-------|------|---------------|-------|-------------|
| `depends_on` | string[] | RECOMMENDED | Plan-level ONLY | Plans this plan structurally requires |
| `blocks` | string[] | RECOMMENDED | Plan-level ONLY | Plans that cannot proceed until this plan completes |

**RECOMMENDED** means: omission triggers a `dream validate` warning for any plan that modifies modules touched by other active plans. For plans with no cross-plan relationships, omission is acceptable.

### 6.2 Structural vs Temporal

```
┌──────────────────────────────────────────────────────────────────────────┐
│  depends_on: SP05_billing_engine                                        │
│    ← "This plan's design ASSUMES SP05 is complete"                      │
│    ← Structural relationship. Permanent. Part of the causal model.      │
│    ← Used by `dream impact` for DAG traversal.                          │
│                                                                          │
│  🚧 [BLOCKED:waiting-on-api]                                            │
│    ← "Work is paused RIGHT NOW because of a temporary obstacle"         │
│    ← Temporal status. Transient. Clears when obstacle resolves.         │
│                                                                          │
│  A plan can have depends_on: AND not be BLOCKED (dependency met).       │
│  A plan can be BLOCKED without depends_on: (external delay).            │
└──────────────────────────────────────────────────────────────────────────┘
```

### 6.3 DAG Rules

| Rule | Detail |
|------|--------|
| **No cycles** | `depends_on:` / `blocks:` must form a Directed Acyclic Graph. `dream validate` rejects cycles |
| **Plan-level only** | Never on individual tasks or phases. Phase-level dependencies are explicitly out of scope — they add O(n²) validation cost for marginal benefit; use reading order and prose in `_overview.md` to express intra-plan sequencing |
| **Bidirectional consistency** | If A `depends_on: B`, then B SHOULD have `blocks: A`. `dream validate` warns on asymmetry |
| **Write-time validation** | `dream validate` auto-triggers before any plan closure that modifies dependency fields. Pre-commit hook validates DAG integrity |

### 6.4 Impact Analysis

`dream impact {plan_id}` traverses the DAG to show:
- Direct dependents (plans with `depends_on: {plan_id}`)
- Transitive dependents (the full downstream chain)
- Modules affected (from State Delta + Module Index)

---

## 7. Invalidation Protocol

When a plan's completion retroactively compromises assumptions made by a previously-completed plan, the invalidation protocol captures this causal relationship.

### 7.1 Fields

| Field | Type | Classification | Description |
|-------|------|---------------|-------------|
| `invalidated_by` | string | CONDITIONAL | Plan ID that caused invalidation. REQUIRED when invalidation has occurred |
| `invalidation_scope` | string | CONDITIONAL | What parts are compromised. REQUIRED when `invalidated_by` is set |
| `invalidation_date` | date | CONDITIONAL | When invalidation was recorded. REQUIRED when `invalidated_by` is set |

### 7.2 Rules

| Rule | Detail |
|------|--------|
| Only ✅ DONE plans/phases can be invalidated | Cannot invalidate something not yet built |
| `invalidation_scope` is required | Must state WHAT is compromised, not just "partially invalidated" |
| Causing plan must report | Invalidations listed in causing plan's closure gate |
| Parent writes to victim | Sibling firewall compliance — causing agent NEVER writes to victim plan |
| `dream validate` is safety net | Detects unwritten invalidations by cross-referencing module modifications against completed plans |
| Status variant | Use `✅ [DONE:invalidated-by:XXnn]` for scannable tree-level visibility |

### 7.3 Invalidation Flow

```
Causing plan reaches ✅ DONE
  │
  ├─► Author identifies compromised assumptions in completed plans
  │
  ├─► Closure gate: REPORT invalidations list
  │
  ├─► Parent/orchestrator writes `invalidated_by:` to victim plan's _overview.md
  │
  └─► `dream validate` independently checks:
        • Does causing plan's dependency DAG connect to victim?
        • Are there unwritten invalidations? (module-level cross-referencing)
        • Surfaces warning if parent forgot to write
```

### 7.4 `invalidation_scope` Vocabulary

Currently free-text. `dream validate` does not enforce vocabulary. A controlled vocabulary will be defined in a future version (P2) when plan count exceeds ~50 and searchability becomes critical.

---

## 8. Knowledge Gaps

### 8.1 Format

The source of truth is the `knowledge_gaps:` frontmatter field — a string array in plan `_overview.md` and module spec frontmatter.

```yaml
knowledge_gaps:
  - "X12 EDI format expertise departed with Carlos"
  - "DynamoDB partition key strategy for high-cardinality audit events"
```

The inline prose marker `⚠️ [KNOWLEDGE GAP]` remains valid for readability but is NOT the source of truth.

### 8.2 When to Add

| Trigger | Example |
|---------|---------|
| Key person departs | Sole expert on telemedicine video leaves |
| Domain expertise missing | No one understands X12 EDI format |
| Unvalidated assumption | "We assume DynamoDB handles 10K writes/sec" |
| External dependency unknown | Third-party API rate limits undocumented |

### 8.3 Resolution

Remove from `knowledge_gaps:` array when expertise is acquired, validated, or documented. Add a State Delta entry noting the resolution.

### 8.4 Aggregation

`dream status --gaps` scans all plans and module specs, aggregating gaps into a single report. The root Module Index table surfaces module-level gaps for at-a-glance visibility.

### 8.5 Future: Structured Objects (P2)

Current format (string array) is a validated MVP. Future versions may add structured objects with `severity:`, `owner:`, and `escalation_date:` fields to support triage at scale. This is deferred — do not implement until plan count exceeds ~30 concurrent.

---

## 9. Priority & Emergency

### 9.1 Model

Binary: `normal` (default — omit from frontmatter) and `emergency`.

### 9.2 Emergency Declaration

When `priority: emergency` is set, the plan MUST also include:

| Field | Purpose |
|-------|---------|
| `emergency_declared_at` | ISO 8601 timestamp. Used for ordering concurrent emergencies |
| `blocks` | SHOULD list resource-sharing plans that this emergency supersedes |

### 9.3 The `dream emergency` Command

`dream emergency {plan_id}` automates emergency declaration (P1):

1. Sets `priority: emergency` in plan's `_overview.md` frontmatter
2. Sets `emergency_declared_at:` to current ISO 8601 timestamp
3. Prompts for `blocks:` — which plans should be superseded
4. Updates `blocks:` in the emergency plan and `depends_on:` in affected plans
5. Surfaces the emergency in `dream status` output (top of list)

Until `dream emergency` is built, emergency declaration requires manual edits to the plan's frontmatter and to any plans that should be blocked.

### 9.4 Concurrent Emergency Triage

When multiple plans have `priority: emergency` simultaneously:

1. **Order by `emergency_declared_at:`** — earliest timestamp has priority
2. **If timestamps are identical** — human decides order
3. **`dream status`** displays emergencies sorted by `emergency_declared_at:` ascending (oldest first = highest priority)
4. **Resolution:** When emergency resolves, set `priority: normal` (or omit) and remove `emergency_declared_at:`. The `blocks:` relationships are evaluated — if no longer needed, clean up

### 9.5 Graduated Response (Out of Scope)

Graduated severity levels (critical/high/medium/low) are explicitly not part of DREAM. Binary is sufficient for projects under ~15 concurrent plans. If projects consistently have 3+ concurrent emergencies, the planning process has a scoping problem, not a priority-model problem.

---

## 10. Folder Conventions

### 10.1 Plan Directory Naming

```
{TYPE}{NN}_{plan_name}/

TYPE:  SP = System Plan    PP = Procedure Plan
NN:    Two-digit creation order (01, 02, 03...)

RULES:
• Numbers are IMMUTABLE — never reassigned after creation
• Gaps are allowed (SP01, SP03 — SP02 was cut)
• Numbers reflect creation order across ALL plan types
```

### 10.2 Full Directory Structure

```
.agent_plan/day_dream/
├── _overview.md                         ← Root navigator (Current Sprint, Plans, Module Index, State Deltas)
├── _tree.md                             ← Generated folder tree (`dream tree`). NEVER hand-maintained
├── _state_deltas_archive.md             ← Overflow State Deltas (auto-generated, never hand-maintained)
│
├── SP01_{plan_name}/                    ← System Plan
│   ├── _overview.md                     ← REQUIRED — plan navigator with full frontmatter
│   ├── 01_executive_summary.md
│   ├── 02_architecture.md
│   ├── 0N_feat_{feature_name}.md         ← feat_ prefix RECOMMENDED (distinguishes from structural docs)
│   ├── 80_implementation.md
│   ├── 81_module_structure.md
│   ├── 82_cli_commands.md               ← Only if CLI exists
│   ├── 99_references.md
│   ├── pNN_{phase}/                     ← Phase directories
│   │   ├── _overview.md
│   │   └── NN_{task}.md
│   ├── modules/
│   │   └── {module_name}.md
│   └── assets/
│       └── {id}_{desc}.asset.md
│
├── PP02_{plan_name}/                    ← Procedure Plan
│   ├── _overview.md
│   ├── 01_summary.md                    ← Merged exec summary + architecture
│   ├── 0N_feat_{step_name}.md            ← feat_ prefix RECOMMENDED
│   ├── 80_implementation.md
│   ├── 99_references.md
│   ├── pNN_{phase}/
│   │   ├── _overview.md
│   │   └── NN_{task}.md
│   └── assets/
│
├── _completed/                          ← Archive of ✅ DONE and 🚫 CUT plans
│   ├── 2025-Q1/
│   ├── 2025-Q3/
│   └── 2026-Q1/
│
├── exploration/                         ← Research docs, meeting notes, decision records
│   └── _archive/
│
└── _templates/                          ← Plan templates (read-only, underscore = infrastructure)
```

### 10.3 Infrastructure File Conventions

All infrastructure files use underscore prefix: `_overview.md`, `_tree.md`, `_state_deltas_archive.md`, `_completed/`, `_templates/`.

| File | Purpose | Who Maintains |
|------|---------|---------------|
| `_overview.md` | Root navigator | Root MANAGER / `dream_mcp` ONLY |
| `_tree.md` | Folder tree with inline status. Header: `<!-- GENERATED — run 'dream tree' to refresh -->` | `dream tree` (generated, NEVER hand-maintained) |
| `_state_deltas_archive.md` | Overflow State Deltas >20. Header: `<!-- GENERATED — managed by dream_mcp -->` | `dream_mcp` (generated, NEVER hand-maintained) |
| `_completed/` | Archive directory, organized by `YYYY-QN/` quarters | Authors / `dream archive` |
| `_templates/` | Template scaffolds | HyperDream (template ownership) |
| `exploration/` | Research docs, meeting notes, decision records | Authors |

### 10.4 Phase Directories

| Rule | Detail |
|------|--------|
| Naming | `pNN_name/` — zero-padded two digits, underscore separator |
| Always directories | Even single-task phases. Never flatten phases |
| Task numbering | `NN_{task_name}.md` starting at `01_` (`00_` is implicitly `_overview.md`) |
| No type prefix | Task files use plain `NN_{name}.md`. The `feat_` prefix is for **plan-root feature files only** (see §2.4) |
| Capacity | Up to `p99_` |

### 10.5 Archival

When a plan reaches ✅ DONE or 🚫 CUT:

1. Move plan directory to `_completed/YYYY-QN/` (quarter of closure)
2. Plan retains original prefix (e.g., `SP01_core_shop/` stays `SP01_core_shop/`)
3. Root `_overview.md` retains a summary row with status and completion date
4. `dream archive {plan_id}` automates this (creates quarter directory if needed)

CUT plans are archived alongside DONE plans. The status marker distinguishes them. A separate `_cut/` directory adds folder overhead without meaningful benefit.

### 10.6 `_tree.md` Filters

`dream tree` generates the full tree by default. The `--active-only` flag filters out `_completed/` and `_templates/`:

```
$ dream tree --active-only
```

This flag addresses scalability — full trees exceed 200 lines at ~16+ plans.

---

## 11. Context Isolation & Sibling Firewall

### 11.1 Visibility Rules

| Scope | What Agent Can See |
|-------|-------------------|
| **Read** | Own task/plan + all ancestors up to root + skill files |
| **Write** | Own task/plan ONLY |
| **Sibling status** | Yes — via parent's `_overview.md` |
| **Sibling content** | **NO — NEVER** |

### 11.2 Parallel Execution Safety

| Scenario | Parallel Safe? | Reason |
|----------|---------------|--------|
| Siblings with no shared writes | ✅ Yes | No race conditions |
| Siblings needing parent state | ❌ No | Sequential — parent integrates |
| Workers on independent branches | ✅ Yes | No shared ancestors modified |

### 11.3 Coordination

Siblings do NOT coordinate directly. The parent MANAGER:

1. Delegates tasks to children
2. Waits for children to report completion
3. Integrates results in INTEGRATE phase
4. Resolves conflicts between sibling outputs

### 11.4 Shared File Updates

When an agent needs to update a file owned by a higher layer, it MUST report this to the parent. The parent decides how to proceed.

---

## 12. MANAGER/WORKER Lifecycle

### 12.1 MANAGER (Processes a Plan)

```
DECOMPOSE  → Verify/create children with _overview.md
DELEGATE   → Assign each child to subagent (max 5 parallel). Apply sibling firewall
INTEGRATE  → Collect results, merge outputs, resolve sibling conflicts
REPORT     → Mark plan ✅ [DONE], satisfy closure gates (§3, §4, §7), notify parent
```

**MANAGER rules:**

| Rule | Detail |
|------|--------|
| MUST create `_overview.md` | If it does not exist |
| MUST NOT fulfill children's tasks | Always delegate |
| MUST integrate | No child output is final until parent accepts |
| MUST report invalidations | List compromised plans at closure gate |
| MUST satisfy Module Index gate | New modules registered before closure |
| Max parallel subagents | 5 |

### 12.2 WORKER (Fulfills a Task)

```
VALIDATE   → Check magnitude ≠ Epic (refuse + escalate). Check dependencies resolved
IMPLEMENT  → Read task spec, create/modify artifacts
VERIFY     → Check acceptance criteria
REPORT     → Mark task ✅ [DONE], notify parent
```

**WORKER rules:**

| Rule | Detail |
|------|--------|
| MUST refuse Epic tasks | Escalate to parent for decomposition |
| MUST NOT modify sibling tasks | Or parent plan content |
| MUST report completion | Status marker update to parent |

### 12.3 Plan Closure Gates

When marking a plan ✅ DONE or 🚫 CUT:

| Gate | Type | Detail |
|------|------|--------|
| All children resolved | REQUIRED | Every child is ✅ DONE or 🚫 CUT |
| State Delta appended | REQUIRED (gate) | Entry in root `_overview.md`. See §4 |
| Module Index updated | REQUIRED (gate) | New modules have BOTH table row AND spec file. See §3 |
| `last_updated` updated | REQUIRED | In plan's `_overview.md` frontmatter |
| Invalidations reported | REQUIRED | List plans/phases this work compromises. See §7 |
| Plan archived | REQUIRED | Moved to `_completed/YYYY-QN/` |
| `dream validate` passes | REQUIRED | Auto-triggered before closure. See §13 |
| Reconciliation checklist | PROCEDURE PLANS ONLY | Verify all touched module specs are updated |

### 12.4 Decomposition Termination

| Becomes a Task when... | Becomes a Plan when... |
|------------------------|----------------------|
| Single agent, single session | Contains ambiguity needing breakdown |
| No ambiguity about output | ≥2 independent children |
| Magnitude ≤ Standard | Magnitude Heavy or Epic |

**Flatten rule:** A plan with only 1 child is suspect — probably a task. SHOULD flatten. Exception: phases (`pNN_name/`) are always directories to preserve sequential ordering.

---

## 13. `dream_mcp` Target Specification

`dream_mcp` is an MCP server module (dev layer) that enforces DREAM conventions through tooling. Convention-only enforcement has a proven ~6 month half-life for cross-referential metadata. `dream_mcp` is the enforcement layer that makes conventions durable.

### 13.1 Design Properties

| Property | Detail |
|----------|--------|
| **Read-only** | Validates but NEVER mutates plan files (exceptions: `dream tree` writes `_tree.md`, `dream archive` moves directories, `dream emergency` writes frontmatter) |
| **Deterministic** | Same input always produces same output |
| **Reports** | Surfaces staleness, gate violations, status via structured output |
| **MCP server** | Exposes tools for agent consumption via MCP protocol |

### 13.2 Command Reference — P0

P0 commands form the walking skeleton. These are the minimum viable enforcement layer.

#### `dream status`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Display current sprint, active/blocked/emergency plans, aggregate warnings |
| **Arguments** | `--gaps` (include knowledge gap aggregation) |
| **Input** | Reads all `_overview.md` frontmatter across plan tree |
| **Output** | Structured status report: emergencies first (ordered by `emergency_declared_at:`), then active, then blocked. Appends summary counts for knowledge gaps, stale modules, gate violations |
| **Mutates** | No |
| **When to call** | Start of any planning session. Before making cross-plan decisions. After emergency declaration |

**Expected output format:**

```
┌─ DREAM Status ──────────────────────────────────────────────────┐
│                                                                  │
│  🚨 EMERGENCY                                                    │
│  PP13_compliance_fix        🔄 [WIP]   p01 in progress          │
│    declared: 2026-02-12T10:30:00                                │
│                                                                  │
│  📋 ACTIVE                                                       │
│  SP03_marketplace           🔄 [WIP]   p01 — order splitting    │
│  SP09_analytics             ⏳ [TODO]  depends_on: SP05         │
│                                                                  │
│  🚧 BLOCKED                                                      │
│  PP06_audit_expansion       🚧 [BLOCKED:pp08-storage-change]    │
│                                                                  │
│  📊 Knowledge Gaps: 3 (use --gaps for details)                   │
│  ⚠️  Stale modules: 2 (use `dream stale` for details)           │
│  ❌ Gate violations: 1 (use `dream validate` for details)        │
└──────────────────────────────────────────────────────────────────┘
```

#### `dream tree`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Generate `_tree.md` — annotated folder tree of the day-dream directory |
| **Arguments** | `--active-only` (exclude `_completed/` and `_templates/`) |
| **Input** | Scans `.agent_plan/day_dream/` directory recursively. Reads status from `_overview.md` frontmatter |
| **Output** | Writes `_tree.md` with status annotations inline. Header: `<!-- GENERATED — run 'dream tree' to refresh -->`. Includes generation timestamp |
| **Mutates** | Yes — writes `_tree.md` |
| **When to call** | After plan creation, closure, or structural changes. On-demand when navigating |

#### `dream stale`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Flag module specs where `last_updated` exceeds staleness threshold |
| **Arguments** | `--weeks N` (default: 4). Module name (optional — filter to single module) |
| **Input** | Reads `last_updated` from all module spec frontmatter |
| **Output** | List of stale modules with last update date and owning plan |
| **Mutates** | No |
| **When to call** | Weekly sweep. Before modifying a module to check spec currency |

#### `dream validate`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Comprehensive gate validation — check all convention enforcement rules |
| **Arguments** | `--plan {plan_id}` (scope to single plan, optional). `--fix` (future: auto-fix where possible, P2) |
| **Input** | Reads all `_overview.md` frontmatter, Module Index, dependency graph, module specs, plan directories |
| **Output** | List of violations categorized as ERROR (blocks closure) or WARNING (should fix) |
| **Mutates** | No |
| **When to call** | **Auto-triggered** before any plan marks ✅ DONE. Also available on-demand. Intended for CI/pre-commit integration |
| **Auto-trigger** | `dream validate` MUST run automatically on status transitions to DONE. This is not on-demand only — agents MUST invoke it at closure |

**Validation checks:**

| Check | Severity | Detail |
|-------|----------|--------|
| Module Index: table row exists | ERROR | New modules must have a row |
| Module Index: spec file exists on disk | ERROR | Row without file = ghost module |
| State Delta: entry exists for closing plan | ERROR | Gate condition |
| Dependency DAG: no cycles | ERROR | `depends_on:`/`blocks:` must be acyclic |
| Dependency DAG: bidirectional consistency | WARNING | A `depends_on: B` → B should have `blocks: A` |
| `depends_on:`/`blocks:` present for cross-plan modifications | WARNING | Recommended fields missing |
| `modified_by_plans` matches State Delta references | WARNING | Drift between module spec and history |
| Unwritten invalidations | WARNING | Module modifications that may compromise completed plans |
| `invalidation_scope` populated when `invalidated_by` set | ERROR | Required field missing |
| `last_updated` present in all plan and module specs | ERROR | Required field missing |
| `emergency_declared_at` present when `priority: emergency` | ERROR | Required field missing |
| Frontmatter schema validity | ERROR | Unknown fields, wrong types |

### 13.3 Command Reference — P1

P1 commands harden enforcement under stress scenarios.

#### `dream impact {plan_id}`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | DAG walk showing all plans affected by changes to `{plan_id}` |
| **Arguments** | `{plan_id}` (required). `--modules` (also show affected modules from State Delta + Module Index) |
| **Input** | Reads `depends_on:`/`blocks:` from all plans. Reads Module Index and State Deltas |
| **Output** | Direct dependents, transitive dependents, affected modules. Warns about potential invalidations |
| **Mutates** | No |
| **When to call** | Before making breaking changes. At plan closure to identify invalidation targets. When evaluating whether to cut a plan |

**Expected output format:**

```
┌─ Impact Analysis: SP05_billing_engine ──────────────────────────┐
│                                                                  │
│  DIRECT DEPENDENTS (blocks:)                                     │
│  └── PP19_perf_optimization    ⏳ [TODO]  depends_on: SP05      │
│                                                                  │
│  TRANSITIVE DEPENDENTS                                           │
│  └── SP09_analytics            ⏳ [TODO]  depends_on: PP19      │
│                                                                  │
│  MODULES AFFECTED                                                │
│  └── billing_engine            Origin: SP05                      │
│      └── Modified by: PP19 (planned)                             │
│                                                                  │
│  ⚠️  Changing SP05 may invalidate: PP19, SP09                    │
└──────────────────────────────────────────────────────────────────┘
```

#### `dream history {module}`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Generate module-indexed change history from State Delta entries |
| **Arguments** | `{module}` (required — module name) |
| **Input** | Reads State Deltas from root `_overview.md` and `_state_deltas_archive.md` |
| **Output** | Table of changes sorted chronologically. See §5 format |
| **Mutates** | No |
| **When to call** | Before modifying a module to understand its history. When investigating regressions |

#### `dream emergency {plan_id}`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Automate emergency declaration — eliminates manual multi-file edits |
| **Arguments** | `{plan_id}` (required). `--blocks {plan_ids}` (optional — plans to supersede) |
| **Input** | Reads plan's `_overview.md` frontmatter |
| **Output** | Updated frontmatter with `priority: emergency`, `emergency_declared_at:`, and `blocks:`. Updates affected plans' `depends_on:` |
| **Mutates** | Yes — writes to plan frontmatter (and blocked plans' frontmatter) |
| **When to call** | When declaring an emergency. Replaces the previous 6-manual-file-edit process |

**Procedure:**

1. Set `priority: emergency` in `{plan_id}`'s frontmatter
2. Set `emergency_declared_at:` to current ISO 8601 timestamp
3. If `--blocks` provided: update `blocks:` in emergency plan, add `depends_on:` in affected plans
4. Run `dream validate` to check DAG consistency
5. Output confirmation with `dream status` summary

#### `dream archive {plan_id}`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Move completed plan to `_completed/YYYY-QN/` archive |
| **Arguments** | `{plan_id}` (required) |
| **Input** | Reads plan status (must be ✅ DONE or 🚫 CUT). Determines quarter from current date or `last_updated` |
| **Output** | Plan directory moved to `_completed/YYYY-QN/`. Quarter directory created if needed. State Delta archive updated if cap exceeded |
| **Mutates** | Yes — moves directory, may update `_state_deltas_archive.md` |
| **When to call** | After plan closure gates are satisfied |

### 13.4 Command Reference — P2

P2 commands improve experience at scale. These are aspirational — design exploration needed before implementation.

#### `dream impact --hypothetical {description}`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Analyze impact of a proposed (not-yet-existing) change without requiring a plan |
| **Arguments** | `--hypothetical {description}` (free-text description of proposed change). `--modules {module_list}` (modules that would be affected) |
| **Scope** | This is a DESIGN EXPLORATION. The behavioral contract is intentionally loose — implementation may refine |
| **Risk** | Hypothetical analysis can be fabricated. Output MUST be clearly labeled as hypothetical, not factual |

#### `dream gaps --proactive`

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Proactive bus-factor detection — flag modules with `sole_expert:` single-person dependencies |
| **Prerequisite** | Requires `sole_expert:` field in module spec frontmatter (P2 addition) |
| **Scope** | Design exploration. Current `knowledge_gaps:` model is reactive-only |

### 13.5 Integration Points

| Integration | Priority | Detail |
|-------------|----------|--------|
| **CI hook** | P0 | `dream validate` runs in CI on PRs that modify `.agent_plan/day_dream/`. Blocks merge on ERROR-level violations |
| **Pre-commit hook** | P1 | `dream validate --plan {affected_plan}` runs on commit. Validates DAG integrity and frontmatter schema |
| **Auto-trigger on DONE** | P0 | Agents MUST invoke `dream validate` before marking any plan ✅ DONE. This is a protocol requirement, not a convenience feature |
| **Watch mode** | P2 | `dream_mcp` watches `.agent_plan/day_dream/` for changes and surfaces violations in real-time. Aspirational — requires persistent process |

### 13.6 Module Specification

| Attribute | Detail |
|-----------|--------|
| **Module name** | `dream_mcp` |
| **Layer** | `dev` |
| **Type** | MCP server |
| **Plan type** | System Plan, Heavy magnitude, Blueprint tier |
| **P0 scope** | `dream status`, `dream tree`, `dream stale`, `dream validate` — 4 commands |
| **P0 estimate** | ~300–400 LOC. `[KNOWN]` — filesystem reads + YAML parsing + DAG validation |
| **P1 scope** | `dream impact`, `dream history`, `dream emergency`, `dream archive` — 4 commands |
| **P2 scope** | `--hypothetical` impact, proactive gap detection, watch mode, configurable cap |

---

## 14. Implementation Notes

All items needed in skills, templates, agents, and modules to bring the ecosystem in line with this specification. Organized into actionable groups.

### 14.1 Skill Updates

| # | Skill | Change | Priority |
|---|-------|--------|----------|
| 1 | `day-dream` | Update all template path references from `templates/` to `_templates/` | HIGH |
| 2 | `day-dream` | Add dependency graph fields, invalidation protocol, knowledge gap frontmatter to authoring rules | HIGH |
| 3 | `day-dream` | Update folder structure examples to show `SP01_`/`PP01_` prefixes, `_completed/YYYY-QN/`, `_tree.md` | HIGH |
| 4 | `day-dream` | Add `dream validate` auto-trigger to plan closure rules | HIGH |
| 5 | `day-dream` | Add Module Index gate (table row + spec file) to closure checklist | HIGH |
| 6 | `writing-templates` | Update location references from `templates/` to `_templates/` and naming conventions | HIGH |
| 7 | `dream-planning` | Update folder structure, add dependency fields, add invalidation protocol, add Module Index gate, update magnitude routing to 8-slot scale | HIGH |
| 8 | `dream-planning` | Remove `plan.yaml` references — metadata lives in `_overview.md` frontmatter only | HIGH |
| 9 | `dream-planning` | Update `_overview.md` convention to match full frontmatter schema (§2.1) | HIGH |

### 14.2 Template File Updates

| # | Template | Change | Priority |
|---|----------|--------|----------|
| 10 | `overview.template.md` | Add full frontmatter schema: `type`, `origin`, `start_at`, `last_updated`, `depends_on`, `blocks`, `knowledge_gaps`, `priority`, `emergency_declared_at`, invalidation fields | HIGH |
| 11 | `overview.template.md` (root) | Add `## Current Sprint`, `## Module Index` (with Spec File and Knowledge Gaps columns), `## State Deltas`. Plans table: add Priority and Depends On columns | HIGH |
| 12 | `module_spec.template.md` | Add `last_updated`, `modified_by_plans`, `knowledge_gaps` to frontmatter scaffold | HIGH |
| 13 | Create `01_summary.template.md` | Procedure Plan merged summary template (does not yet exist) | HIGH |
| 14 | `80_implementation.template.md` | Update slot notation to 8-slot scale | LOW |
| 15 | `simple.template.md` | Add `origin:` frontmatter | LOW |

### 14.3 Directory & File Changes

| # | Change | Priority |
|---|--------|----------|
| 16 | Rename `templates/` → `_templates/` physically in `.agent_plan/day_dream/` | HIGH |
| 17 | Update 27+ path references across skills, agents, docs from `templates/` to `_templates/` | HIGH |
| 18 | Update compiled `.agent.md` files referencing `templates/` paths | MEDIUM |
| 19 | Create `_state_deltas_archive.md` when first overflow occurs | WHEN NEEDED |
| 20 | Create `YYYY-QN/` subdirectories in `_completed/` when next plan is archived | WHEN NEEDED |
| 21 | Update `_tree.md` header to `<!-- GENERATED — run 'dream tree' to refresh -->` | HIGH |

### 14.4 `dream_mcp` Module Creation

| # | Item | Priority |
|---|------|----------|
| 22 | Create `dream_mcp` module in `modules/dev/dream_mcp/` (dev layer, MCP server) | **P0** |
| 23 | Implement P0 commands: `dream status`, `dream tree`, `dream stale`, `dream validate` | **P0** |
| 24 | Create blueprint plan (`SP{NN}_dream_mcp/`) for phased delivery | **P0** |
| 25 | Implement P1 commands: `dream impact`, `dream history`, `dream emergency`, `dream archive` | P1 |
| 26 | Add CI hook for `dream validate` on PRs modifying `.agent_plan/day_dream/` | P0 |
| 27 | Add pre-commit hook for DAG validation on frontmatter changes | P1 |

### 14.5 Convention Enforcement Changes

| # | Change | Priority |
|---|--------|----------|
| 28 | Root `_overview.md` write restriction: only root MANAGER / `dream_mcp` | HIGH |
| 29 | Module Index gate enforcement: agents self-enforce both table row AND spec file before marking ✅ DONE | HIGH |
| 30 | `dream validate` auto-trigger: agents MUST invoke before any plan closure | HIGH |
| 31 | Invalidation reporting: agents report invalidations at plan closure, parent writes to victim | HIGH |
| 32 | `depends_on:`/`blocks:` treated as RECOMMENDED: `dream validate` warns on omission for cross-plan modifications | HIGH |
| 33 | `emergency_declared_at:` required when `priority: emergency` is set | HIGH |
| 34 | `_tree.md` discipline: agents NEVER hand-edit | HIGH |

### 14.6 Deferred Items (P2+)

| # | Item | Rationale for Deferral |
|---|------|----------------------|
| D1 | Knowledge gap structured objects (`severity:`, `owner:`) | String array is validated MVP. Structure needed at ~30+ concurrent plans |
| D2 | `invalidation_scope` controlled vocabulary | Free-text works at current scale. Vocabulary needed at ~50+ plans |
| D3 | Configurable State Delta cap | 20 is validated default. Configurability is nice-to-have |
| D4 | `dream impact` edge weight/severity | Design exploration needed. Not blocking current usage |
| D5 | Phase-level dependencies | O(n²) validation cost for marginal benefit. Intra-plan sequencing handled by reading order in `_overview.md` |
| D6 | Bus-factor tracking (`sole_expert:` field) | Proactive > reactive, but current gap model works at current scale |
| D7 | `dream impact --hypothetical` | Requires explicit scoping to prevent fabrication. Design exploration needed |
| D8 | Watch mode for `dream_mcp` | Requires persistent process. Aspirational |
| D9 | Content-aware staleness (`dream stale` with hashing/diff) | Timestamp-only is gameable but sufficient for MVP. Content hashing adds complexity |

### 14.7 Summary

| Category | Count | P0 | P1 | Other |
|----------|-------|----|----|-------|
| Skill updates | 9 | 0 | 0 | 9 HIGH |
| Template updates | 6 | 0 | 0 | 4 HIGH, 2 LOW |
| Directory/file changes | 6 | 0 | 0 | 4 HIGH, 1 MEDIUM, 1 WHEN NEEDED |
| `dream_mcp` module | 6 | 4 | 2 | 0 |
| Convention changes | 7 | 0 | 0 | 7 HIGH |
| Deferred (P2+) | 9 | — | — | Tracked |
| **Total** | **43** | **4** | **2** | **37** |

---

## 15. Appendix: Templates

All templates at: `.agent_plan/day_dream/_templates/`

### Simple Tier

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `simple.template.md` | Single-file vision + quick start | ≤200 lines |

### Blueprint Tier

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `blueprint/overview.template.md` | `_overview.md` scaffold with full frontmatter (§2.1) | ≤100 lines |
| `blueprint/task.template.md` | Leaf task scaffold | ≤100 lines |
| `blueprint/00_index.template.md` | Navigation hub with flowchart | ≤150 lines |
| `blueprint/01_executive_summary.template.md` | Vision, goals, non-goals, prior art (System Plan) | ≤150 lines |
| `blueprint/01_summary.template.md` | Merged summary + architecture (Procedure Plan) | ≤200 lines |
| `blueprint/02_architecture.template.md` | System diagrams, components (System Plan only) | ≤200 lines |
| `blueprint/NN_feature.template.md` | Full feature spec (≥3 modules or ext API) | ≤150 lines |
| `blueprint/NN_feature_simple.template.md` | Lightweight feature (80% of cases) | ≤100 lines |
| `blueprint/80_implementation.template.md` | Phased roadmap with 8-slot scale verification | ≤200 lines/phase |
| `blueprint/81_module_structure.template.md` | Reusable vs project-specific modules | ≤150 lines |
| `blueprint/82_cli_commands.template.md` | CLI interface and command reference | ≤150 lines |
| `blueprint/99_references.template.md` | External links | No limit |
| `blueprint/exploration.template.md` | Research/exploration doc | — |
| `blueprint/modules/module_spec.template.md` | Module implementation spec (with `last_updated`, `modified_by_plans`, `knowledge_gaps`) | ≤200 lines |

### Assets

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `assets/asset.template.md` | Non-code artifacts (mockups, diagrams, storyboards) | ≤100 lines (excl. diagrams) |

### Template Selection Quick Reference

```
Quick vision, ≤2 features?          → simple.template.md
Plan directory navigator?           → blueprint/overview.template.md
Leaf task?                          → blueprint/task.template.md
Feature (≤2 modules, no ext API)?   → NN_feature_simple.template.md
Feature (≥3 modules or ext API)?    → NN_feature.template.md
Exec summary (System Plan)?         → 01_executive_summary.template.md
Summary (Procedure Plan)?           → 01_summary.template.md
Architecture?                       → 02_architecture.template.md
Implementation roadmap?             → 80_implementation.template.md
Supporting artifact?                → assets/asset.template.md
```

### Examples

Located at `_templates/examples/`:

| Example | Demonstrates |
|---------|-------------|
| `blueprint_example/` | Complete blueprint folder structure |
| `simple_example.md` | Completed simple-tier document |
| `deep_dive_*.example.md` | Algorithm proof, API contract, architecture, state machine |
| `free_zone_*.example.md` | Assumption graveyard, metaphor map, philosophical tensions |

---

## Design Principles

| Principle | Rule |
|-----------|------|
| **Two primitives** | Plan (directory) and Task (file). Nothing else |
| **Omit, don't N/A** | Optional files don't exist on disk |
| **Human authority** | Human initiates planning; DREAM determines format |
| **Slots, not time** | 8-slot maximum system; each slot ≈ 1 hour AI-agent time |
| **Structure-first** | Show the tree, then explain the rules |
| **ADHD-readable** | Visual-first: tables, ASCII boxes, folder trees, no text walls |
| **Gate-enforced closure** | State Delta + Module Index (table + file) + invalidation report + `dream validate` pass |
| **Convention + tooling** | Convention is the skeleton, `dream_mcp` is the muscle. Convention-only has ~6 month half-life |
| **Recording + predicting** | State Deltas record history; dependency DAG enables impact prediction |
| **Structural vs temporal** | `depends_on:`/`blocks:` = permanent. `🚧 [BLOCKED:reason]` = transient |
| **Source of truth in frontmatter** | `knowledge_gaps:`, `invalidated_by:`, `depends_on:` live in frontmatter. Prose is supplementary |
| **Omit-when-default** | `priority: normal` → omit. Only write explicit values that differ from default |
| **Infrastructure underscore** | `_overview.md`, `_completed/`, `_templates/`, `_tree.md` — underscore = infrastructure |
| **Provenance tracking** | Every plan has `origin:`, every module has `modified_by_plans:` |
| **Archival over deletion** | Completed plans move to `_completed/YYYY-QN/`, never deleted |

---

*End of DREAM v4.05 — Unified Planning System Specification*
