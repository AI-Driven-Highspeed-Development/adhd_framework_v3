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

**Scope boundary:** This skill covers *decomposition, routing, and plan metadata*. For document authoring rules (templates, Story/Spec pattern, assets), see the `day-dream` skill.

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

## `_overview.md` Frontmatter Schema

Every plan directory has `_overview.md` with YAML frontmatter. **No separate metadata file** — all plan metadata lives in `_overview.md` frontmatter.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plan identifier (snake_case) |
| `type` | enum | `system` or `procedure` |
| `magnitude` | enum | `Trivial` / `Light` / `Standard` / `Heavy` / `Epic` |
| `status` | enum | `TODO` / `WIP` / `DONE` / `BLOCKED:reason` / `CUT` |
| `origin` | string | Path to exploration/doc that triggered this plan |
| `last_updated` | date | `YYYY-MM-DD` (human) or ISO 8601 (machine) |

### Recommended Fields

| Field | Type | Description |
|-------|------|-------------|
| `depends_on` | string[] | Plans this plan structurally requires |
| `blocks` | string[] | Plans that cannot proceed until this completes |
| `knowledge_gaps` | string[] | Missing expertise or unvalidated assumptions |

### Optional / Conditional Fields

| Field | Type | When |
|-------|------|------|
| `start_at` | date | When work began (omit for exploratory) |
| `priority` | enum | `emergency` only (omit for `normal`) |
| `emergency_declared_at` | datetime | REQUIRED when `priority: emergency` |
| `invalidated_by` | string | Plan that caused invalidation (victim plans only) |
| `invalidation_scope` | string | REQUIRED when `invalidated_by` is set |
| `invalidation_date` | date | REQUIRED when `invalidated_by` is set |

### Full Example

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

### Required Content After Frontmatter

```markdown
# {Plan Name}

## Purpose
Why this plan exists and what it delivers.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_login_flow.md | Task | ⏳ [TODO] | Login endpoint |
| auth_tokens/ | Plan | 🔄 [WIP] | Token lifecycle |

⚠️ **Type column:** ONLY `Plan` (directory) or `Task` (file) are valid values. 'Doc', 'Feature', 'Module', etc. are INVALID.

## Integration Map
How children's outputs combine into the plan's deliverable.

## Reading Order
1. 01_login_flow.md (independent)
2. auth_tokens/ (depends on login)
```

---

## Directory-Based Hierarchy

Hierarchy is expressed through the filesystem. No level numbers.

```
SP01_{plan_name}/
├── _overview.md              # REQUIRED — plan navigator with frontmatter
├── 01_executive_summary.md   # System Plan only
├── 02_architecture.md        # System Plan only
├── 0N_feat_{feature}.md      # feat_ prefix RECOMMENDED
├── 80_implementation.md
├── pNN_{phase}/              # Phase directories
│   ├── _overview.md
│   └── NN_{task}.md
├── modules/
│   └── {module_name}.md
└── assets/
```

**Rules:**
- **Directory = plan** — always has `_overview.md`
- **File = task** — leaf, directly executable
- Phase directories: `pNN_name/` — ALWAYS directories, even single-task phases
- Task numbering starts at `01_` (position `00_` is implicitly `_overview.md`)
- Nesting ≤3 levels recommended

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

### MANAGER (Processes a Plan)

```
DECOMPOSE  → Verify/create children with _overview.md
DELEGATE   → Assign each child to subagent (max 5 parallel), apply sibling firewall
INTEGRATE  → Collect results, merge outputs, resolve sibling conflicts
REPORT     → Mark plan ✅ [DONE], satisfy closure gates, notify parent
```

| Rule | Detail |
|------|--------|
| MUST create `_overview.md` | If it does not exist |
| MUST NOT fulfill children's tasks | Always delegate |
| MUST integrate | No child output is final until parent accepts |
| MUST satisfy closure gates | State Delta + Module Index + invalidation report |
| Max parallel subagents | 5 |

### WORKER (Fulfills a Task)

```
VALIDATE   → Check magnitude ≠ Epic (refuse + escalate), check dependencies
IMPLEMENT  → Read task spec, create/modify artifacts
VERIFY     → Check acceptance criteria
REPORT     → Mark task ✅ [DONE], notify parent
```

| Rule | Detail |
|------|--------|
| MUST refuse Epic tasks | Escalate to parent for decomposition |
| MUST NOT modify sibling tasks | Or parent plan content |
| MUST report completion | Status marker update to parent |

### Plan Closure Gates

| Gate | Detail |
|------|--------|
| All children resolved | Every child is ✅ DONE or 🚫 CUT |
| State Delta appended | Entry in root `_overview.md` |
| Module Index updated | New modules have BOTH table row AND spec file |
| `last_updated` updated | In plan's frontmatter |
| Invalidations reported | List plans this work compromises |
| Plan archived | Moved to `_completed/YYYY-QN/` |
| `dream validate` passes | Auto-triggered before closure |

### Decomposition Termination

| Becomes a Task when... | Becomes a Plan when... |
|------------------------|----------------------|
| Single agent, single session | Contains ambiguity needing breakdown |
| No ambiguity about output | ≥2 independent children |
| Magnitude ≤ Standard | Magnitude Heavy or Epic |

A plan with only 1 child is suspect — SHOULD flatten. Exception: phase directories (`pNN_`) always stay as directories.

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
| Document authoring (templates, Story/Spec) | `day-dream` skill |
| Estimation defaults (AI-agent time, human_only) | `day-dream` skill |
| Tier selection (Simple vs Blueprint) | `day-dream` skill |
| Template catalog and format | `writing-templates` skill |
| Orchestrator dispatch mechanics | `orch-routing` skill |
| Implementation quality gates | `orch-implementation` skill |
