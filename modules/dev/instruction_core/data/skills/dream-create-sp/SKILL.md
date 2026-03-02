---
name: dream-create-sp
description: "Step-by-step SOP for creating an SP (System Plan) in the DREAM system. Covers single-file plan creation, frontmatter, content structure, root _overview registration, and validation. Use this skill when creating a focused, single-deliverable plan with fewer than 3 tasks."
---

# Create a System Plan (SP)

Step-by-step SOP for creating an SP (System Plan) — the single-file plan type in the DREAM system.

## When to Use

- Single deliverable with a focused, clear scope
- Fewer than 3 tasks
- Magnitude is Trivial, Light, or Standard
- No multi-phase execution needed — work can be tracked in one document
- No cross-module dependencies requiring separate architecture docs

**Not an SP?** If the work requires >3 tasks, multiple phases, or cross-module coordination → use `dream-create-pp` (Procedure Plan). If magnitude is Heavy or Epic → upgrade to PP. If intent is exploratory with no artifact → use `dream-vision`.

---

## Prerequisites

- `.agent_plan/day_dream/` directory exists
- Root `.agent_plan/day_dream/_overview.md` exists
- Scope is well-defined — one clear deliverable, straightforward execution

---

## Step-by-Step SOP

### Step 1: Determine Plan Number

Scan existing plans in `.agent_plan/day_dream/` to find the highest plan number **across all types** (SP and PP share one numbering sequence).

```bash
ls .agent_plan/day_dream/SP* .agent_plan/day_dream/PP* 2>/dev/null | sort
```

Next plan number = `max_existing + 1`. Numbers are **immutable creation-order** — gaps allowed, reuse forbidden.

**Example:** If `SP{NN}`, `PP{NN}`, `PP{NN}` exist → next is `XX{NN+1}`.

**Naming conflict check:** Call `dream_tree` to view the annotated plan hierarchy and confirm no naming conflicts with existing plans.

---

### Step 2: Create Plan File

Create a **single file** (not a folder) placed directly in `.agent_plan/day_dream/`:

```
SP{NN}_{snake_case_name}.md
```

- `{NN}` — zero-padded two digits (e.g., `04`)
- `{snake_case_name}` — descriptive, lowercase with underscores

**Example:** `SP{NN}_{name}.md`

---

### Step 3: Write Frontmatter and Content

#### 3a. Frontmatter

```yaml
---
name: {snake_case_name}         # Matches file suffix (e.g., {name})
type: system                    # Always "system" for SP
magnitude: Light                # Trivial | Light | Standard (max for SP)
status: TODO                    # TODO | WIP | DONE | BLOCKED:reason | CUT
origin: {path_or_description}  # What triggered this plan
last_updated: YYYY-MM-DD       # Today's date
---
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | ✅ | snake_case, matches filename suffix |
| `type` | enum | ✅ | Always `system` for SP |
| `magnitude` | enum | ✅ | Trivial / Light / Standard — Heavy or Epic → upgrade to PP |
| `status` | enum | ✅ | TODO / WIP / DONE / BLOCKED:reason / CUT |
| `origin` | string | ✅ | Path to trigger doc or brief description |
| `last_updated` | date | ✅ | YYYY-MM-DD format |

SP frontmatter has **no recommended/optional fields**. If you need `depends_on`, `blocks`, or `knowledge_gaps`, the plan likely belongs as a PP.

#### 3b. Content Structure

```markdown
# SP{NN} — {Plan Name}

## Purpose

{Why this plan exists and what it delivers. 1-2 sentences.}

## Scope

**Trigger:** {What event or decision initiated this plan}
**End State:** {What "done" looks like — observable, verifiable}

## Non-Goals

- {Explicit exclusion 1}
- {Explicit exclusion 2}

## Tasks

| Status | Task | Difficulty |
|--------|------|------------|
| ⏳ | {Task description} | `[KNOWN]` |
| ⏳ | {Task description} | `[KNOWN]` |

## Verification

| What to Try | Expected Result |
|-------------|-----------------|
| {Action to verify} | {Expected outcome} |

## Decisions

| Decision | Rationale |
|----------|-----------|
| {Choice made} | {Why} |
```

#### Content Rules

| Rule | Detail |
|------|--------|
| Line limit | ≤150 lines total |
| Max tasks | 3 — four or more → upgrade to PP |
| Difficulty | `[KNOWN]` and `[EXPERIMENTAL]` only — `[RESEARCH]` → upgrade to PP |
| Non-Goals | Minimum 2 items |
| Verification | At least 1 verifiable check |
| Purpose | 1-2 sentences max |
| Scope | Must include both Trigger and End State |
| Decisions section | Optional — include only if non-obvious choices were made |

#### Status Markers

| Marker | Meaning |
|--------|---------|
| ⏳ `[TODO]` | Not started |
| 🔄 `[WIP]` | In progress |
| ✅ `[DONE]` | Complete |
| 🚧 `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 `[CUT]` | Removed from scope |

---

### Step 4: Register in Root `_overview.md`

Update `.agent_plan/day_dream/_overview.md` in two places:

#### 4a. Plans Table

Add a row to `## Plans`:

```markdown
| [SP{NN}_{name}.md](./SP{NN}_{name}.md) | System | ⏳ [TODO] | normal | {One-line description} |
```

Note: Link points to the file directly (no `_overview.md` since SP is a single file).

#### 4b. Reading Order

Add to `## Reading Order` at the appropriate position:

```markdown
N. **SP{NN}_{name}.md** — {Brief context note}
```

SP plans do NOT need a Current Sprint entry — they are compact enough to track via status alone.

---

### Step 5: Validate

Call `dream_validate` targeting the new SP file to verify frontmatter, status syntax, and structural compliance. Fix any FAIL issues before proceeding.

Also run through the full Validation Checklist below.

---

## Validation Checklist

### File
- [ ] Named `SP{NN}_{snake_case_name}.md` (number is next available across all types)
- [ ] Placed directly in `.agent_plan/day_dream/` (not in a subfolder)
- [ ] Is a single `.md` file (not a directory)

### Frontmatter
- [ ] `type: system` (not `procedure`)
- [ ] `name` matches filename suffix in snake_case
- [ ] `magnitude` is Trivial, Light, or Standard (not Heavy or Epic)
- [ ] `status` is valid enum
- [ ] `origin` references a trigger
- [ ] `last_updated` is today's date

### Content
- [ ] ≤150 lines total
- [ ] ≤3 tasks
- [ ] No `[RESEARCH]` difficulty tasks
- [ ] Non-Goals has ≥2 items
- [ ] At least 1 verification check
- [ ] Purpose is 1-2 sentences
- [ ] Scope has both Trigger and End State

### Registration
- [ ] Added to root `_overview.md` Plans table with Type = `System`
- [ ] Added to root `_overview.md` Reading Order

---

## Common Mistakes

| Mistake | Why It's Wrong | Do Instead |
|---------|---------------|------------|
| Creating a folder instead of a file | SP is single-file, not a directory | Create `SP{NN}_{name}.md` as a flat file |
| Using `type: procedure` | SP uses `type: system` | Always `type: system` for SP |
| More than 3 tasks | Too complex for Simple tier | Upgrade to PP (`dream-create-pp`) |
| Magnitude Heavy or Epic | SP caps at Standard | Upgrade to PP |
| Adding `depends_on` or `knowledge_gaps` | Those signal PP-level complexity | Upgrade to PP if dependencies exist |
| Missing Non-Goals | All plans need scope boundaries | Include ≥2 explicit exclusions |
| Adding phase directories | SP has no phases — it's a single file | If phases are needed, it's a PP |
| Skipping verification | Every plan needs a completion check | Include ≥1 verifiable action |
| Reusing a plan number | Numbers are immutable across all types | Increment to next unused number |

---

## Upgrade Triggers

An SP should be upgraded to a PP when ANY of these become true:

| Trigger | Action |
|---------|--------|
| Tasks grow to >3 | Create PP folder with `dream-create-pp`, migrate content |
| Cross-module dependencies emerge | Upgrade — PP handles coordination |
| Multiple phases needed | Upgrade — PP has phase structure |
| Magnitude reaches Heavy or Epic | Upgrade — SP caps at Standard |
| `depends_on` another plan | Upgrade — SP doesn't track dependencies |
| `[RESEARCH]` tasks needed | Upgrade — PP can phase research into P2+ |

**How to upgrade:** Create the PP with `dream-create-pp`, migrate content from the SP file into `01_summary.md` and `80_implementation.md`, update root `_overview.md` registration, and delete the old SP file.
