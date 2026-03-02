---
name: dream-create-pp
description: "Step-by-step SOP for creating a PP (Parallel Plan) blueprint in the DREAM system. Covers folder scaffolding, _overview.md frontmatter, 01_summary.md, 80_implementation.md, root _overview registration, and validation. Use this skill when creating a new multi-phase blueprint plan."
---

# Create a Procedure Plan (PP)

Step-by-step SOP for creating a PP (Procedure Plan) blueprint — the multi-phase, folder-based plan type in the DREAM system.

## When to Use

- User wants a **multi-phase plan** with >3 tasks or parallel work streams
- The work is a **workflow, migration, or operational process** (not new architecture from scratch)
- Multiple deliverables requiring phased execution with exit gates
- Triggered by existing plan AND primary deliverable modifies existing code (PP tiebreaker)
- Scope qualifies for **Blueprint tier**: ≥3 features OR ≥2 cross-module deps OR external APIs

**Not a PP?** If ≤2 tasks with single deliverable and straightforward scope → use `dream-create-sp` (Simple Plan). If intent is exploratory with no artifact → use `dream-vision`.

---

## Prerequisites

- `.agent_plan/day_dream/` directory exists
- Root `.agent_plan/day_dream/_overview.md` exists
- Clear understanding of procedure scope, trigger, and end state
- Magnitude assessed: Trivial / Light / Standard / Heavy / Epic

---

## Step-by-Step SOP

### Step 1: Determine Plan Number

Scan existing plan folders in `.agent_plan/day_dream/` to find the highest plan number **across all types** (SP and PP share one numbering sequence).

```bash
ls -d .agent_plan/day_dream/SP* .agent_plan/day_dream/PP* 2>/dev/null | sort
```

Next plan number = `max_existing + 1`. Numbers are **immutable creation-order** — gaps allowed, reuse forbidden.

**Example:** If `SP{NN}`, `PP{NN}`, `PP{NN}` exist → next is `XX{NN+1}` regardless of type.

**Naming conflict check:** Call `dream_tree` to view the annotated plan hierarchy and confirm no naming conflicts with existing plans.

---

### Step 2: Create Plan Folder

```
PP{NN}_{snake_case_name}/
```

- `{NN}` — zero-padded two digits (e.g., `04`)
- `{snake_case_name}` — descriptive, lowercase with underscores

**Example:** `PP{NN}_{name}/`

---

### Step 3: Create `_overview.md`

The mandatory plan navigator. Every agent entering the directory reads this first.

#### 3a. Frontmatter

```yaml
---
# ── REQUIRED ──
name: {snake_case_name}         # Matches folder suffix (e.g., {name})
type: procedure                 # Always "procedure" for PP
magnitude: Standard             # Trivial | Light | Standard | Heavy | Epic
status: TODO                    # TODO | WIP | DONE | BLOCKED:reason | CUT
origin: {path_to_trigger}      # Path to triggering doc/discussion
last_updated: YYYY-MM-DD       # Today's date

# ── RECOMMENDED (include when applicable) ──
depends_on:                     # Plans this structurally requires
  - PP{NN}_{dependency}
blocks:                         # Plans that wait on this
  - SP{NN}_{blocked_plan}
knowledge_gaps:                 # Missing expertise or unvalidated assumptions
  - "Description of unknown"

# ── OPTIONAL ──
# start_at: YYYY-MM-DD         # When work began
# priority: emergency           # ONLY "emergency" — omit for normal
---
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | ✅ | snake_case, matches folder suffix |
| `type` | enum | ✅ | Always `procedure` for PP |
| `magnitude` | enum | ✅ | Trivial / Light / Standard / Heavy / Epic |
| `status` | enum | ✅ | TODO / WIP / DONE / BLOCKED:reason / CUT |
| `origin` | string | ✅ | Path to triggering doc (relative to project root) |
| `last_updated` | date | ✅ | YYYY-MM-DD format |
| `depends_on` | string[] | Recommended | Full folder names of dependency plans |
| `blocks` | string[] | Recommended | Full folder names of blocked plans |
| `knowledge_gaps` | string[] | Recommended | Descriptive strings of unknowns |
| `start_at` | date | Optional | When work began |
| `priority` | enum | Optional | Only `emergency` — omit for normal |

#### 3b. Content Sections

```markdown
# PP{NN} — {Plan Name}

## Purpose

{Why this plan exists and what it delivers. 2-3 sentences max.}

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_summary.md | Task | ⏳ [TODO] | Merged exec summary + architecture |
| 80_implementation.md | Task | ⏳ [TODO] | Phased implementation roadmap |

## Integration Map

{How children's outputs combine. ASCII diagram showing data flow.}

## Reading Order

1. **01_summary.md** — Understand pain, vision, approach.
2. **80_implementation.md** — Phased roadmap with tasks and verification.
```

**Rules:**
- Children Type column: ONLY `Plan` (directory) or `Task` (file) — no other values
- Add phase directories as children when created: `p00_name/ | Plan | ⏳ [TODO] | ...`
- Line limit: **≤100 lines**

---

### Step 4: Create `01_summary.md`

PP uses a **merged summary** combining executive summary and architecture into one document. Follows the Story → Spec pattern.

Scaffold from: `dream-routing/assets/blueprint/01_summary.template.md`

#### The Story (Visual Narrative — Required)

| Section | Format |
|---------|--------|
| 😤 The Pain | ASCII box showing current broken state + pain-level table |
| ✨ The Vision | ASCII box showing target flow after this procedure |
| 🎯 One-Liner | Single blockquote, one sentence elevator pitch |
| 📊 Impact | Before/After comparison table with metrics |

#### The Spec (Technical Detail — Required)

| Section | Key Rules |
|---------|-----------|
| 🌟 TL;DR | Max 3 sentences |
| 🎯 Procedure Scope | Trigger (what started it) + End State (what done looks like, verifiable) |
| 🔍 Prior Art | ADOPT / ADAPT / REJECT decisions for existing solutions, ≥1 entry |
| ❌ Non-Goals | Minimum 3 explicit exclusions |
| 🏗️ Approach & Architecture | Mermaid flowchart + components-affected table + key design decisions |
| ✅ Features / Steps Overview | Max 5 P0 items, difficulty labels required |
| 📊 Success Metrics | Metric + target + measurement method |
| 📅 Scope Budget | Duration per phase with hard limits and slot notation |
| ✅ Validation Checklist | Narrative, Scope, Architecture, Grounding checks |

**Line limit:** ≤200 lines for `01_summary.md`

**Difficulty labels:** `[KNOWN]` (proven — P0 only), `[EXPERIMENTAL]` (needs validation — P1+), `[RESEARCH]` (no proven solution — NEVER P0, P2+ only)

---

### Step 5: Create `80_implementation.md`

Phased implementation plan with tasks, exit gates, and verification for each phase.

Scaffold from: `dream-routing/assets/blueprint/80_implementation.template.md`

#### 5a. Frontmatter

```yaml
---
project: "PP{NN} — {Plan Name}"
current_phase: 0
phase_name: "{First Phase Name}"
status: TODO
start_date: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---
```

#### 5b. Status Legend (Include at Document Top)

```markdown
## 📊 Status Legend

| Icon | Status | Meaning |
|------|--------|---------|
| ⏳ | `[TODO]` | Not started |
| 🔄 | `[WIP]` | In progress |
| ✅ | `[DONE]` | Complete |
| 🚧 | `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 | `[CUT]` | Removed from scope |
```

#### 5c. Phase Structure (Repeat for Each Phase)

```markdown
## ⚙️ Phase {N}: {Phase Name}

**Goal:** *"{One sentence goal}"*

**Duration:** ■■■□□□□□ Standard (max 3 slots)

### Exit Gate

- [ ] `{verifiable command or condition}` → `{expected result}`

### Tasks

| Status | Task | Scope | Difficulty |
|--------|------|-------|------------|
| ⏳ | {Task description} | `{module/scope}` | `[KNOWN]` |

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `{action}` | {outcome} |

### P{N} Completion Checklist

- [ ] Exit gate met
- [ ] All tasks marked ✅
- [ ] Manual verification steps pass
```

#### Phase Rules

| Rule | Detail |
|------|--------|
| P0 hard limits | Max 5 tasks, `[KNOWN]` only, max 5 slots |
| P1+ limits | May include `[EXPERIMENTAL]`, max 5 slots |
| `[RESEARCH]` | NEVER in P0 — P2+ only |
| Duration bar | `■` = filled slots, `□` = remaining (of 8 total) |
| Line limit | ≤200 lines per phase |
| Each phase | Must have exit gate, tasks table, verification, completion checklist |

#### 5d. Optional Trailing Sections

```markdown
## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
```

---

### Step 6: Register in Root `_overview.md`

Update `.agent_plan/day_dream/_overview.md` in three places:

#### 6a. Plans Table

Add a row to `## Plans`:

```markdown
| [PP{NN}_{name}/](./PP{NN}_{name}/_overview.md) | Procedure | ⏳ [TODO] | normal | {One-line description} |
```

#### 6b. Current Sprint (If Work Starts Immediately)

Add to `## Current Sprint`:

```markdown
| PP{NN}_{name} | p00_{first_phase} | ⏳ [TODO] | {Next action description} |
```

#### 6c. Reading Order

Add to `## Reading Order` at the appropriate position with a brief context note.

---

### Step 7: Validate

Call `dream_validate` targeting the new PP folder to verify frontmatter, status syntax, and structural compliance. Fix any FAIL issues before proceeding.

Also run through the full Validation Checklist below.

---

## Validation Checklist

### Folder & Files
- [ ] Folder named `PP{NN}_{snake_case_name}/` (number is next available across all types)
- [ ] `_overview.md` exists with valid YAML frontmatter
- [ ] `01_summary.md` exists with Story → Spec structure
- [ ] `80_implementation.md` exists with at least Phase 0

### Frontmatter
- [ ] `type: procedure` (not `system` or `simple`)
- [ ] `name` matches folder suffix in snake_case
- [ ] `magnitude` is valid enum (Trivial / Light / Standard / Heavy / Epic)
- [ ] `status` is valid enum (TODO / WIP / DONE / BLOCKED:reason / CUT)
- [ ] `origin` references a trigger doc or discussion
- [ ] `last_updated` is today's date (YYYY-MM-DD)

### Content Quality
- [ ] `_overview.md` ≤100 lines
- [ ] `01_summary.md` ≤200 lines
- [ ] `80_implementation.md` ≤200 lines per phase
- [ ] Children table uses only `Plan` or `Task` in Type column
- [ ] P0 has ≤5 tasks and `[KNOWN]` difficulty only
- [ ] Non-Goals has ≥3 items (in `01_summary.md`)
- [ ] TL;DR ≤3 sentences

### Registration
- [ ] Added to root `_overview.md` Plans table
- [ ] Added to root `_overview.md` Reading Order
- [ ] Added to Current Sprint (if work starts immediately)

---

## Common Mistakes

| Mistake | Why It's Wrong | Do Instead |
|---------|---------------|------------|
| Using `type: system` | System Plans have different file structure | Always `type: procedure` for PP |
| Reusing a plan number | Numbers are immutable creation-order | Increment to next unused number across all types |
| Separate `01_executive_summary.md` + `02_architecture.md` | Those are SP (System Plan) conventions | PP uses merged `01_summary.md` |
| Missing `origin` field | Every plan must trace to its trigger | Add path to discussion or exploration doc |
| `[RESEARCH]` tasks in P0 | P0 must contain only `[KNOWN]` work | Defer research to P1+ |
| Skipping exit gates | Every phase requires verifiable exit criteria | Add ≥1 testable condition per phase |
| Not registering in root `_overview.md` | Plan becomes invisible to navigation | Update Plans table + Reading Order |
| Using `Doc` or `Feature` in Children Type | Only `Plan` and `Task` are valid | `Plan` for directories, `Task` for files |
| Exceeding line limits | Documents become unwieldy | `_overview.md` ≤100, `01_summary.md` ≤200 |

---

## Templates Reference

Canonical templates for PP blueprint documents live in the `dream-routing` skill:

| Document | Template |
|----------|----------|
| `_overview.md` | `dream-routing/assets/blueprint/overview.template.md` |
| `01_summary.md` | `dream-routing/assets/blueprint/01_summary.template.md` |
| `80_implementation.md` | `dream-routing/assets/blueprint/80_implementation.template.md` |
| Feature doc (full) | `dream-routing/assets/blueprint/NN_feature.template.md` |
| Feature doc (simple) | `dream-routing/assets/blueprint/NN_feature_simple.template.md` |
