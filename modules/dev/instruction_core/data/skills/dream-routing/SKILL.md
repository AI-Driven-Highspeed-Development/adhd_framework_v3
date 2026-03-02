---
name: dream-routing
description: "Central dispatch for DREAM operations — routes user intents to the correct dream-* leaf skill. Covers intent classification, plan type detection (SP/PP), disambiguation rules, and dispatch table. Use this skill when a user requests any DREAM operation: creating, updating, closing, fixing, or validating plans."
---

# Dream Routing

Central dispatch for all DREAM operations. Classifies user intent and routes to the correct leaf skill.

## When to Use
- A user requests ANY dream operation (create, update, close, fix, validate)
- Determining which dream-* skill to load
- Disambiguating vague plan-related requests
- Classifying SP vs PP plan type

**Scope boundary:** This skill routes to leaf skills. It does NOT contain SOPs, does NOT create artifacts, and does NOT replace `dream-vision` or `dream-planning` (those are independent skills with their own scope).

---

## Intent Classification — Dispatch Table

| User Intent | Target Skill | Example Triggers |
|-------------|-------------|------------------|
| Create a new PP (Procedure Plan) blueprint | `dream-create-pp` | "Create a PP for X", "New blueprint plan", "Procedure plan for Y" |
| Create a new SP (System Plan) blueprint | `dream-create-sp` | "Create an SP for X", "System plan for Y", "New architecture plan" |
| Update/resurrect an existing plan | `dream-update` | "Update PP{NN}", "Resurrect plan X", "Revise the overview" |
| Close/complete a plan | `dream-close` | "Close SP{NN}", "Mark plan done", "Finish PP{NN}" |
| Fix plan validation errors | `dream-fix` | "Fix frontmatter in PP{NN}", "Fix the plan", "Repair validation errors" |
| Validate plan structure | `dream-validate` | "Validate all plans", "Check PP{NN}", "Run dream validate" |
| Explore/discuss (no artifact) | `dream-vision` | "Let's think about feature X", "Vision for Y", "Explore an idea" |
| Decompose work into task tree | `dream-planning` | "Break this into subtasks", "Plan the phases", "Decompose this work" |

### Routing Priority

When multiple intents could match, use this priority order:
1. **Explicit skill name** — user says "use dream-close" → route directly
2. **Explicit plan ID** — "Fix PP{NN}" → resolve plan, then route by verb
3. **Action verb** — "Create", "Close", "Fix" → match dispatch table
4. **Fallback** — ambiguous → disambiguate (see rules below)

---

## Plan Type Detection

Determine SP vs PP BEFORE routing to a create skill.

| Signal | Route To |
|--------|----------|
| Single deliverable, <3 tasks | SP (System Plan) |
| Multi-phase, parallel work, >3 tasks | PP (Procedure Plan) |
| Building/extending software architecture | SP |
| Workflow, migration, operational process | PP |
| Triggered by existing plan AND modifies existing code | PP (tiebreaker) |
| Unclear from context | **Ask the user** |

### Quick Decision

```
Is the primary deliverable NEW architecture?
  YES → SP (System Plan)
  NO  → Is it a workflow, migration, or process change?
    YES → PP (Procedure Plan)
    NO  → Ask user: "Is this new architecture (SP) or a process/migration (PP)?"
```

---

## Disambiguation Rules

When user intent is ambiguous, resolve before routing.

| Ambiguous Request | Resolution |
|-------------------|------------|
| "Create a plan" (no type) | Ask: "System Plan (SP) for new architecture, or Procedure Plan (PP) for workflow/migration?" |
| "Fix the plan" (no target) | Ask: "Which plan? List active plans or provide plan ID (e.g., PP{NN}, SP{NN})" |
| "Update" (content vs status) | Check context — if discussing content changes → `dream-update`; if marking done → `dream-close` |
| "Plan for X" (create vs discuss) | If X is concrete and scoped → route to create; if X is exploratory → `dream-vision` |
| "Check the plan" (validate vs review) | If asking about structural correctness → `dream-validate`; if reviewing content → `dream-update` |
| "New blueprint" (SP or PP?) | Apply Plan Type Detection rules above |

### Never Guess

If disambiguation rules don't resolve the intent, ask. One clarifying question is faster than undoing a wrong operation.

---

## Dispatch Protocol

Execute these steps in order for every DREAM request:

1. **Classify** — Match user intent against the dispatch table
2. **Detect plan type** — If creating, determine SP or PP
3. **Disambiguate** — If ambiguous, apply disambiguation rules; ask if still unclear
4. **Resolve target** — If a plan ID is mentioned, verify it exists
5. **Load leaf skill** — Route to the target skill from the dispatch table
6. **Execute** — Follow the leaf skill's SOP

### Routing Failures

| Failure | Recovery |
|---------|----------|
| Target skill doesn't exist yet | Inform user the skill is planned but not yet implemented; suggest manual approach |
| Plan ID not found | List active plans; ask user to confirm or correct |
| Multiple intents in one request | Process sequentially — route first intent, then second |

---

## Leaf Skill Status

| Skill | Status | Notes |
|-------|--------|-------|
| `dream-vision` | Exists | Exploration, discussion, no artifacts |
| `dream-planning` | Exists | Decomposition, magnitude routing, plan metadata |
| `dream-create-pp` | Planned | PP creation SOP |
| `dream-create-sp` | Planned | SP creation SOP |
| `dream-update` | Planned | Plan content updates, resurrection |
| `dream-close` | Planned | Plan closure gates, archival |
| `dream-fix` | Exists | Validation error repair |
| `dream-validate` | Exists | Structure and metadata validation |

For planned skills that don't yet exist, fall back to `dream-vision` (for exploratory work) or `dream-planning` (for structural work) as appropriate.

---

## Templates

All DREAM document templates are bundled with this skill in `assets/`.

| Template | Purpose |
|----------|---------|
| `simple.template.md` | Simple tier — single-file plan |
| `blueprint/overview.template.md` | Blueprint `_overview.md` scaffold |
| `blueprint/01_executive_summary.template.md` | SP executive summary |
| `blueprint/01_summary.template.md` | PP merged summary |
| `blueprint/02_architecture.template.md` | SP architecture document |
| `blueprint/80_implementation.template.md` | Implementation plan |
| `blueprint/NN_feature.template.md` | Feature document (full) |
| `blueprint/NN_feature_simple.template.md` | Feature document (simple) |
| `assets/asset.template.md` | Supporting asset scaffold |

Full template catalog: `assets/` subdirectory of this skill.

---

## What This Skill Does NOT Do

| Boundary | Reason |
|----------|--------|
| Does NOT contain SOPs for operations | SOPs live in leaf skills (`dream-create-pp`, etc.) |
| Does NOT create artifacts | Artifact creation is the leaf skill's job |
| Does NOT replace `dream-vision` | `dream-vision` is an independent skill for exploration/authoring |
| Does NOT replace `dream-planning` | `dream-planning` is an independent skill for decomposition |
| Does NOT enforce conventions | Convention enforcement is tooling (`dream validate`, CI) |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Route without classifying intent | Always match against dispatch table first |
| Guess SP vs PP when unclear | Ask the user |
| Skip disambiguation for vague requests | Apply disambiguation rules, then ask |
| Process multiple intents simultaneously | Route sequentially — first intent, then second |
| Route to a planned skill that doesn't exist | Fall back to `dream-vision` or `dream-planning` |
| Embed SOP steps in this skill | Keep SOPs in leaf skills only |

---

## Cross-References

| Topic | Where |
|-------|-------|
| Document authoring (templates, Story/Spec) | `dream-vision` skill |
| Decomposition, magnitude routing, plan metadata | `dream-planning` skill |
| Template format and naming conventions | `dream-routing` skill (assets/) |
| Orchestrator dispatch mechanics | `orch-routing` skill |
