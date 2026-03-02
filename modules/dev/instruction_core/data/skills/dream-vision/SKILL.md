---
name: dream-vision
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

## Operations Dispatch

This skill defines the **format and authoring conventions** for DREAM documents.

For step-by-step operations (creating, updating, closing, fixing plans), use the `dream-routing` skill which dispatches to specialized SOPs.

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

All templates bundled with the `dream-routing` skill at: `dream-routing/assets/`

Simple tier, Blueprint tier, and Asset template tables with purposes and line limits:
→ See [template-catalog.md](assets/template-catalog.md)

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

Every blueprint document follows a two-part structure (Story + Spec) with required subsections for pain, vision, one-liner, and impact:
→ See [story-spec-pattern.md](assets/story-spec-pattern.md)

---

## Document Rules & Line Limits

Line limits per document type, Children table schema, and authoring rules (skeleton, acceptance criteria, custom sections, deep dive, clean-code-first):
→ See [document-line-limits.md](assets/document-line-limits.md)

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

Frontmatter fields and usage example:
→ See [invalidation-frontmatter-example.yaml](assets/invalidation-frontmatter-example.yaml)

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

The Module Index (table in root `_overview.md`) maps every module to its origin plan. A phase introducing a new module CANNOT mark ✅ DONE until the table row and spec file both exist.

### Module Spec Frontmatter

Module spec YAML frontmatter format and gate conditions:
→ See [module-spec-frontmatter-example.yaml](assets/module-spec-frontmatter-example.yaml)

---

## State Deltas

Append-only entries in root `_overview.md` logging codebase changes when a plan closes. Gate condition — a plan CANNOT mark ✅ DONE without appending one.

Format, active cap, and overflow rules:
→ See [state-delta-example.md](assets/state-delta-example.md)

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

Duration estimates by magnitude (AI-agent time) and `human_only` flag usage:
→ See [estimation-defaults.md](assets/estimation-defaults.md)

---

## Folder Structure

### Blueprint Tier

Full directory layout for System Plans, Procedure Plans, completed archive, exploration, and templates:
→ See [blueprint-folder-structure.md](assets/blueprint-folder-structure.md)

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

## MCP Tool Integration

Use `dream_mcp` tools to ground vision work in the current plan landscape:

| When | Tool | Purpose |
|------|------|---------|
| Before creating visions | `dream_status` | View sprint dashboard — active, blocked, and pending plans |
| Before creating visions | `dream_tree` | See annotated plan hierarchy with status |
| Before modifying module specs | `dream_stale` | Flag module specs not updated recently |
| Before modifying plans with dependencies | `dream_impact` | DAG walk showing direct + transitive dependents |

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
| Template catalog & format | `dream-routing` skill (assets/) |
| Orchestrator dispatch mechanics | `orch-routing` skill |
| Implementation quality gates | `orch-implementation` skill |
