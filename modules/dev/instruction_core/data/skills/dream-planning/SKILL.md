---
name: dream-planning
description: "DREAM decomposition protocol — 8-slot magnitude routing, plan types (SP/PP), _overview.md frontmatter schema, sibling firewall, MANAGER/WORKER lifecycle, and context isolation. Covers magnitude assessment, plan/task hierarchy, directory-based decomposition, status syntax, difficulty labels, dependency tracking, and plan closure gates. Use this skill when decomposing tasks, dispatching subagents, or applying context isolation rules."
---

# DREAM Planning Protocol

Decomposition Rules for Engineering Atomic Modules — how to break work into parallelizable, isolated units.

## When to Use
- Assessing whether a task needs decomposition
- Breaking complex work into a plan/task tree
- Dispatching parallel subagents with context boundaries
- Classifying plan types (System or Procedure)
- Writing plan `_overview.md` with correct frontmatter

**Scope boundary:** This skill covers *decomposition, routing, and plan metadata*. For document authoring rules (templates, Story/Spec pattern, assets), see the `dream-vision` skill.

---

## Operations Dispatch

This skill defines the **decomposition protocol** — how to break work into plans and tasks.

For step-by-step operations on plan artifacts (creating, updating, closing plans), use the `dream-routing` skill.

---

## Terminology

| Term | Definition |
|------|-----------|
| **Plan** | Directory with mandatory `_overview.md` — decomposable, has children |
| **Task** | Single `.md` file — leaf, directly executable, no children |
| **System Plan (SP)** | Plan building/extending software architecture. Prefix: `SP` |
| **Procedure Plan (PP)** | Plan for workflow, migration, operational process. Prefix: `PP` |
| **Magnitude** | 8-slot complexity scale: Trivial(1) · Light(2) · Standard(3) · Heavy(5) · Epic(8) |
| **Sibling firewall** | Siblings NEVER read/write each other's content — coordinate through parent only |
| **MANAGER** | Agent processing a plan — decomposes, delegates, integrates children |
| **WORKER** | Agent fulfilling a task — executes directly, produces artifacts |

---

## Plan Types

| Plan Type | Use When | Prefix | Key Difference |
|-----------|----------|--------|----------------|
| **System Plan** | Building/extending software architecture | `SP` | Separate `01_executive_summary.md` + `02_architecture.md` |
| **Procedure Plan** | Workflow, migration, operational process | `PP` | Merged `01_summary.md` (exec summary + architecture co-evolve) |

**Naming:** `{TYPE}{NN}_{plan_name}/` — numbers are IMMUTABLE creation-order across all types. Gaps allowed.

**Tiebreaker:** Triggered by existing plan AND primary deliverable modifies existing code → Procedure Plan.

---

## Magnitude Routing

Assess magnitude FIRST. This gates all decomposition decisions. Values are MAXIMUMS — each slot ≈ 1 hour AI-agent time.

```
■□□□□□□□  Trivial   max 1 slot   Execute immediately
■■□□□□□□  Light     max 2 slots  Execute directly
■■■□□□□□  Standard  max 3 slots  Decompose if ≥3 subtasks
■■■■■□□□  Heavy     max 5 slots  SHOULD decompose
■■■■■■■■  Epic      max 8 slots  MUST decompose
```

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
| Ambiguity in requirements | Standard+ |

---

## Status Syntax

Status markers for plan/task tracking (TODO, WIP, DONE, BLOCKED, CUT, invalidated):
→ See [status-syntax.md](assets/status-syntax.md)

---

## Difficulty Labels

| Label | Meaning | P0 Allowed? |
|-------|---------|-------------|
| `[KNOWN]` | Standard patterns, proven libraries | ✅ Yes |
| `[EXPERIMENTAL]` | Needs validation in our context | ⚠️ Conditional |
| `[RESEARCH]` | Active problem, no proven solution | ❌ NEVER in P0 |

---

## `_overview.md` Frontmatter Schema

Every plan directory has `_overview.md` with YAML frontmatter. **No separate metadata file** — all plan metadata lives in `_overview.md` frontmatter.

Required, recommended, and optional/conditional field tables:
→ See [overview-frontmatter-schema.md](assets/overview-frontmatter-schema.md)

### Full Example

Complete frontmatter YAML with all field categories:
→ See [overview-frontmatter-example.yaml](assets/overview-frontmatter-example.yaml)

### Required Content After Frontmatter

Purpose, Children table, Integration Map, and Reading Order sections:
→ See [overview-content-template.md](assets/overview-content-template.md)

---

## Directory-Based Hierarchy

Filesystem-based hierarchy example with rules for directories, files, phases, and nesting:
→ See [directory-hierarchy-example.md](assets/directory-hierarchy-example.md)

---

## Context Isolation — Sibling Firewall

### Visibility Rules

| Scope | What Agent Can See |
|-------|-------------------|
| **Read** | Own task/plan + all ancestors up to root + skill files |
| **Write** | Own task/plan ONLY |
| **Sibling status** | Yes — via parent's `_overview.md` |
| **Sibling content** | **NO — NEVER** |

### Parallel Safety

| Scenario | Parallel Safe? |
|----------|---------------|
| Siblings with no shared writes | ✅ Yes |
| Siblings needing parent state | ❌ No — sequential, parent integrates |
| Workers on independent branches | ✅ Yes |

Siblings do NOT coordinate directly. The parent MANAGER delegates → waits → integrates → resolves conflicts.

When an agent needs to update a file owned by a higher layer, it MUST report to the parent. The parent decides how to proceed.

---

## MANAGER / WORKER Lifecycle

MANAGER (DECOMPOSE → DELEGATE → INTEGRATE → REPORT), WORKER (VALIDATE → IMPLEMENT → VERIFY → REPORT), Plan Closure Gates, and Decomposition Termination rules:
→ See [manager-worker-lifecycle.md](assets/manager-worker-lifecycle.md)

---

## MCP Tool Integration

Before decomposition, assess the current plan landscape:

| When | Tool | Purpose |
|------|------|---------|
| Before decomposition | `dream_status` | Sprint dashboard — understand active, blocked, and pending plans |
| Before decomposition | `dream_tree` | Annotated hierarchy — see existing plan structure and numbering |
| Before modifying plans with dependents | `dream_impact` | DAG walk — identify direct + transitive dependents |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Siblings communicating directly | Route through parent's INTEGRATE phase |
| Epic-magnitude leaf task | Decompose into plan with children |
| Skip magnitude assessment | Always assess magnitude first |
| Plan with only 1 child | Flatten — probably a task |
| MANAGER fulfilling tasks directly | Delegate to WORKER subagents |
| Agent reading sibling content | Read sibling STATUS only (via parent) |
| Deep nesting (>3 levels) | Flatten or re-scope |
| Separate metadata files | Use `_overview.md` frontmatter only |
| Omit `origin` field | Every plan must trace to its trigger doc |
| Skip `dream validate` at closure | Auto-trigger is a protocol requirement |

---

## Cross-References

| Topic | Where |
|-------|-------|
| Document authoring (templates, Story/Spec) | `dream-vision` skill |
| Estimation defaults (AI-agent time, human_only) | `dream-vision` skill |
| Tier selection (One-Page vs Blueprint) | `dream-vision` skill |
| Template catalog and format | `dream-routing` skill (assets/) |
| Orchestrator dispatch mechanics | `orch-routing` skill |
| Implementation quality gates | `orch-implementation` skill |
