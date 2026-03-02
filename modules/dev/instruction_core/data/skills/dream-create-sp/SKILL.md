---
name: dream-create-sp
description: "Step-by-step SOP for creating an SP (System Plan) blueprint in the DREAM system. Covers folder scaffolding, _overview.md frontmatter, 01_executive_summary.md, 02_architecture.md, 80_implementation.md, 81_module_structure.md, root _overview registration, and validation. Use this skill when creating a new architecture plan for building or extending software systems."
---

# Create a System Plan (SP)

Step-by-step SOP for creating an SP (System Plan) blueprint — the architecture-focused, folder-based plan type in the DREAM system.

## When to Use

- User wants to **build or extend software architecture** (new modules, system design, feature systems)
- The primary deliverable is **new architecture**, not a workflow or migration
- Requires separate executive summary and architecture documents
- Scope qualifies for **Blueprint tier**: ≥3 features OR ≥2 cross-module deps OR external APIs
- Needs `81_module_structure.md` for ADHD module classification

**Not an SP?** If the work is a workflow, migration, or operational process → use `dream-create-pp` (Procedure Plan). If intent is exploratory with no artifact → use `dream-vision`. If scope is One-Page tier (≤2 features, single module, no external APIs) → a single-file plan may suffice.

---

## Prerequisites

- `.agent_plan/day_dream/` directory exists
- Root `.agent_plan/day_dream/_overview.md` exists
- Clear understanding of architecture scope, trigger, and end state
- Magnitude assessed: Trivial / Light / Standard / Heavy / Epic

---

## Step-by-Step SOP

### Step 1: Determine Plan Number

Scan existing plan folders in `.agent_plan/day_dream/` to find the highest plan number **across all types** (SP and PP share one numbering sequence).

```bash
ls -d .agent_plan/day_dream/SP* .agent_plan/day_dream/PP* 2>/dev/null | sort
```

Next plan number = `max_existing + 1`. Numbers are **immutable creation-order** — gaps allowed, reuse forbidden.

**Example:** If `SP01`, `PP02`, `PP03` exist → next is `XX04` regardless of type.

**Naming conflict check:** Call `dream_tree` to view the annotated plan hierarchy and confirm no naming conflicts with existing plans.

---

### Step 2: Create Plan Folder

```
SP{NN}_{snake_case_name}/
```

- `{NN}` — zero-padded two digits (e.g., `04`)
- `{snake_case_name}` — descriptive, lowercase with underscores

**Example:** `SP04_notification_engine/`

---

### Step 3: Create `_overview.md`

The mandatory plan navigator. Every agent entering the directory reads this first.

#### 3a. Frontmatter

```yaml
---
# ── REQUIRED ──
name: {snake_case_name}         # Matches folder suffix
type: system                    # Always "system" for SP
magnitude: Standard             # Trivial | Light | Standard | Heavy | Epic
status: TODO                    # TODO | WIP | DONE | BLOCKED:reason | CUT
origin: {path_to_trigger}      # Path to triggering doc/discussion
last_updated: YYYY-MM-DD       # Today's date

# ── RECOMMENDED (include when applicable) ──
depends_on:                     # Plans this structurally requires
  - PP{NN}_{dependency}
blocks:                         # Plans that wait on this
  - PP{NN}_{blocked_plan}
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
| `type` | enum | ✅ | Always `system` for SP |
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
# SP{NN} — {Plan Name}

## Purpose

{Why this plan exists and what it delivers. 2-3 sentences max.}

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_executive_summary.md | Task | ⏳ [TODO] | Vision, goals, non-goals, prior art |
| 02_architecture.md | Task | ⏳ [TODO] | System diagrams, components |
| 80_implementation.md | Task | ⏳ [TODO] | Phased implementation roadmap |
| 81_module_structure.md | Task | ⏳ [TODO] | Reusable vs project-specific modules |

## Integration Map

{How children's outputs combine. ASCII diagram showing data flow.}

## Reading Order

1. **01_executive_summary.md** — Understand vision, goals, prior art.
2. **02_architecture.md** — System design and components.
3. **81_module_structure.md** — Module classification and ownership.
4. **80_implementation.md** — Phased roadmap with tasks and verification.
```

**Rules:**
- Children Type column: ONLY `Plan` (directory) or `Task` (file) — no other values
- Add phase directories as children when created: `p00_name/ | Plan | ⏳ [TODO] | ...`
- Add optional files as children: `82_cli_commands.md`, `modules/`, etc.
- Line limit: **≤100 lines**

---

### Step 4: Create `01_executive_summary.md`

SP uses a **separate executive summary** distinct from the architecture document. Follows the Story → Spec pattern.

Scaffold from: `dream-routing/assets/blueprint/01_executive_summary.template.md`

#### The Story (Visual Narrative — Required)

| Section | Format |
|---------|--------|
| 😤 The Pain | ASCII box showing current broken state + pain-level table |
| ✨ The Vision | ASCII box showing target architecture after this plan |
| 🎯 One-Liner | Single blockquote, one sentence elevator pitch |
| 📊 Impact | Before/After comparison table with metrics |

#### The Spec (Technical Detail — Required)

| Section | Key Rules |
|---------|-----------|
| 🌟 TL;DR | Max 3 sentences |
| 🎯 System Scope | Trigger (what started it) + End State (what done looks like, verifiable) |
| 🔍 Prior Art & Existing Solutions | ADOPT / ADAPT / REJECT / BUY / BUILD / WRAP decisions, ≥1 entry |
| ❌ Non-Goals | Minimum 3 explicit exclusions |
| ✅ Features Overview | Max 5 P0 items, difficulty labels required |
| 📊 Success Metrics | Metric + target + measurement method |
| 📅 Scope Budget | Duration per phase with hard limits and slot notation |
| ✅ Validation Checklist | Narrative, Scope, Architecture, Grounding checks |

**Line limit:** ≤150 lines for `01_executive_summary.md`

**Difficulty labels:** `[KNOWN]` (proven — P0 only), `[EXPERIMENTAL]` (needs validation — P1+), `[RESEARCH]` (no proven solution — NEVER P0, P2+ only)

---

### Step 5: Create `02_architecture.md`

SP's architecture document contains system diagrams, component relationships, and design decisions — kept separate from the executive summary so architecture can evolve independently.

Scaffold from: `dream-routing/assets/blueprint/02_architecture.template.md`

#### Required Sections

| Section | Key Rules |
|---------|-----------|
| 🏗️ System Overview | High-level architecture with Mermaid diagram |
| 📊 Component Breakdown | Table of components with responsibilities and interfaces |
| 🔗 Data Flow | Mermaid flowchart showing data paths between components |
| 🎯 Key Design Decisions | Decision table with rationale |
| ⚠️ Constraints & Trade-offs | Known limitations and accepted trade-offs |

**Line limit:** ≤200 lines for `02_architecture.md`

---

### Step 6: Create `80_implementation.md`

Phased implementation plan with tasks, exit gates, and verification for each phase.

Scaffold from: `dream-routing/assets/blueprint/80_implementation.template.md`

#### 6a. Frontmatter

```yaml
---
project: "SP{NN} — {Plan Name}"
current_phase: 0
phase_name: "{First Phase Name}"
status: TODO
start_date: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---
```

#### 6b. Status Legend (Include at Document Top)

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

#### 6c. Phase Structure (Repeat for Each Phase)

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

#### 6d. Optional Trailing Sections

```markdown
## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
```

---

### Step 7: Create `81_module_structure.md`

System Plans for ADHD projects MUST include a module structure document classifying modules as reusable or project-specific.

Scaffold from: `dream-routing/assets/blueprint/81_module_structure.template.md`

#### Required Sections

| Section | Key Rules |
|---------|-----------|
| Module Classification | Table mapping each module to Reusable/Project-Specific with rationale |
| Module Dependency Map | Which modules depend on which |
| New Module Specs | For each new module: name, layer, role suffix, purpose |

**Line limit:** ≤150 lines

---

### Step 8: Create Optional Files (If Applicable)

| File | Create When |
|------|-------------|
| `82_cli_commands.md` | Plan has CLI commands |
| `modules/` | Plan creates or modifies ADHD modules (store module spec files here) |
| `0N_feat_{feature}.md` | Plan has discrete feature specs beyond the core structure docs |
| `assets/` | Supporting artifacts (diagrams, mockups, data models) |

---

### Step 9: Register in Root `_overview.md`

Update `.agent_plan/day_dream/_overview.md` in three places:

#### 9a. Plans Table

Add a row to `## Plans`:

```markdown
| [SP{NN}_{name}/](./SP{NN}_{name}/_overview.md) | System | ⏳ [TODO] | normal | {One-line description} |
```

#### 9b. Current Sprint (If Work Starts Immediately)

Add to `## Current Sprint`:

```markdown
| SP{NN}_{name} | p00_{first_phase} | ⏳ [TODO] | {Next action description} |
```

#### 9c. Reading Order

Add to `## Reading Order` at the appropriate position with a brief context note.

---

### Step 10: Validate

Call `dream_validate` targeting the new SP folder to verify frontmatter, status syntax, and structural compliance. Fix any FAIL issues before proceeding.

Also run through the full Validation Checklist below.

---

## Validation Checklist

### Folder & Files
- [ ] Folder named `SP{NN}_{snake_case_name}/` (number is next available across all types)
- [ ] `_overview.md` exists with valid YAML frontmatter
- [ ] `01_executive_summary.md` exists with Story → Spec structure
- [ ] `02_architecture.md` exists with system diagrams
- [ ] `80_implementation.md` exists with at least Phase 0
- [ ] `81_module_structure.md` exists with module classification (ADHD projects)

### Frontmatter
- [ ] `type: system` (not `procedure`)
- [ ] `name` matches folder suffix in snake_case
- [ ] `magnitude` is valid enum (Trivial / Light / Standard / Heavy / Epic)
- [ ] `status` is valid enum (TODO / WIP / DONE / BLOCKED:reason / CUT)
- [ ] `origin` references a trigger doc or discussion
- [ ] `last_updated` is today's date (YYYY-MM-DD)

### Content Quality
- [ ] `_overview.md` ≤100 lines
- [ ] `01_executive_summary.md` ≤150 lines
- [ ] `02_architecture.md` ≤200 lines
- [ ] `80_implementation.md` ≤200 lines per phase
- [ ] `81_module_structure.md` ≤150 lines
- [ ] Children table uses only `Plan` or `Task` in Type column
- [ ] P0 has ≤5 tasks and `[KNOWN]` difficulty only
- [ ] Non-Goals has ≥3 items (in `01_executive_summary.md`)
- [ ] TL;DR ≤3 sentences

### Registration
- [ ] Added to root `_overview.md` Plans table with Type = `System`
- [ ] Added to root `_overview.md` Reading Order
- [ ] Added to Current Sprint (if work starts immediately)

---

## Common Mistakes

| Mistake | Why It's Wrong | Do Instead |
|---------|---------------|------------|
| Using `type: procedure` | Procedure Plans have different file structure | Always `type: system` for SP |
| Reusing a plan number | Numbers are immutable creation-order | Increment to next unused number across all types |
| Using merged `01_summary.md` | That's PP (Procedure Plan) convention | SP uses separate `01_executive_summary.md` + `02_architecture.md` |
| Missing `02_architecture.md` | Architecture doc is required for System Plans | Create even if architecture seems straightforward |
| Missing `81_module_structure.md` | Module classification required for ADHD projects | Include module reusability analysis |
| Missing `origin` field | Every plan must trace to its trigger | Add path to discussion or exploration doc |
| `[RESEARCH]` tasks in P0 | P0 must contain only `[KNOWN]` work | Defer research to P1+ |
| Skipping exit gates | Every phase requires verifiable exit criteria | Add ≥1 testable condition per phase |
| Not registering in root `_overview.md` | Plan becomes invisible to navigation | Update Plans table + Reading Order |
| Creating a single file instead of folder | SP is folder-based with multiple documents | Create directory with `_overview.md` and required files |
| Using `Doc` or `Feature` in Children Type | Only `Plan` and `Task` are valid | `Plan` for directories, `Task` for files |
| Exceeding line limits | Documents become unwieldy | `_overview.md` ≤100, `01_executive_summary.md` ≤150, `02_architecture.md` ≤200 |

---

## SP vs PP Quick Reference

| Aspect | System Plan (SP) | Procedure Plan (PP) |
|--------|------------------|---------------------|
| Use when | Building/extending architecture | Workflow, migration, process |
| Executive summary | `01_executive_summary.md` (separate) | `01_summary.md` (merged with architecture) |
| Architecture doc | `02_architecture.md` (separate) | Merged into `01_summary.md` |
| Module structure | `81_module_structure.md` (required for ADHD) | Not applicable |
| CLI commands | `82_cli_commands.md` (optional) | Not applicable |
| Folder structure | `SP{NN}_{name}/` | `PP{NN}_{name}/` |
| `type` field | `system` | `procedure` |

---

## Templates Reference

Canonical templates for SP blueprint documents live in the `dream-routing` skill:

| Document | Template |
|----------|----------|
| `_overview.md` | `dream-routing/assets/blueprint/overview.template.md` |
| `01_executive_summary.md` | `dream-routing/assets/blueprint/01_executive_summary.template.md` |
| `02_architecture.md` | `dream-routing/assets/blueprint/02_architecture.template.md` |
| `80_implementation.md` | `dream-routing/assets/blueprint/80_implementation.template.md` |
| `81_module_structure.md` | `dream-routing/assets/blueprint/81_module_structure.template.md` |
| `82_cli_commands.md` | `dream-routing/assets/blueprint/82_cli_commands.template.md` |
| Feature doc (full) | `dream-routing/assets/blueprint/NN_feature.template.md` |
| Feature doc (simple) | `dream-routing/assets/blueprint/NN_feature_simple.template.md` |
