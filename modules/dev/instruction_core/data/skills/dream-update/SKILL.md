---
name: dream-update
description: "Step-by-step SOP for updating existing DREAM plans — status changes, phase progression, scope modifications, plan resurrection, and content updates. Covers frontmatter updates, status syntax, phase transitions, and root _overview synchronization. Use this skill when modifying, progressing, or resurrecting an existing plan."
---

# Update an Existing Plan

Step-by-step SOPs for modifying, progressing, or resurrecting DREAM plans — status changes, phase transitions, scope modifications, and resurrection of CUT/archived plans.

## When to Use

- Changing a plan or task status (TODO → WIP → DONE, etc.)
- Progressing to the next phase of an implementation plan
- Modifying scope — adding, removing, or changing tasks or phases
- Resurrecting a CUT or archived plan back to active status
- Updating plan content (decisions log, knowledge gaps, dependencies)

**Not an update?** If creating a new plan from scratch → use `dream-create-pp` or `dream-create-sp`. If closing a completed plan → use `dream-close`.

---

## Prerequisites

- Target plan exists in `.agent_plan/day_dream/` (or in `_archive/` for resurrection)
- Root `.agent_plan/day_dream/_overview.md` exists
- You know which operation type you are performing (status, phase, scope, or resurrection)

---

## Status Syntax Reference

| Marker | Meaning |
|--------|---------|
| ⏳ `[TODO]` | Not started |
| 🔄 `[WIP]` | In progress |
| ✅ `[DONE]` | Complete |
| ✅ `[DONE:invalidated-by:XXnn]` | Complete but assumptions compromised by plan `XXnn` |
| 🚧 `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 `[CUT]` | Removed from scope |

**Rules:**
- Status markers use emoji prefix + bracketed code in task tables
- `BLOCKED:reason` uses kebab-case (e.g., `BLOCKED:awaiting-api-access`)
- `invalidated-by` uses the plan folder prefix (e.g., `SP01`, `PP03`)
- Frontmatter `status` field uses bare enum: `TODO` / `WIP` / `DONE` / `BLOCKED:reason` / `CUT`

---

## Frontmatter Fields Affected by Operation

| Operation | Fields Updated |
|-----------|---------------|
| **Status Update** | `status`, `last_updated` |
| **Phase Progression** | `current_phase`, `phase_name`, `last_updated` (in `80_implementation.md` frontmatter) |
| **Scope Modification** | `last_updated`, `magnitude` (if scope changes magnitude) |
| **Plan Resurrection** | `status`, `last_updated`, `knowledge_gaps` (if applicable) |
| **Dependency Change** | `depends_on`, `blocks`, `last_updated` |
| **Knowledge Gap Update** | `knowledge_gaps`, `last_updated` |

### `_overview.md` Frontmatter (Plan-Level)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | ✅ | snake_case, matches folder suffix |
| `type` | enum | ✅ | `system` or `procedure` |
| `magnitude` | enum | ✅ | Trivial / Light / Standard / Heavy / Epic |
| `status` | enum | ✅ | TODO / WIP / DONE / BLOCKED:reason / CUT |
| `origin` | string | ✅ | Path to triggering doc |
| `last_updated` | date | ✅ | YYYY-MM-DD — update on EVERY change |
| `depends_on` | string[] | Recommended | Plans this structurally requires |
| `blocks` | string[] | Recommended | Plans that wait on this |
| `knowledge_gaps` | string[] | Recommended | Missing expertise or unvalidated assumptions |

### `80_implementation.md` Frontmatter (Phase Tracking)

| Field | Type | Notes |
|-------|------|-------|
| `current_phase` | integer | Zero-indexed phase number |
| `phase_name` | string | Human-readable name of current phase |
| `status` | enum | TODO / WIP / DONE |
| `last_updated` | date | YYYY-MM-DD |

---

## Operation A: Status Update

Change the status of a plan or individual task.

### Step 1: Identify Current Status

Read the plan's `_overview.md` frontmatter `status` field (for plan-level) or task row in `80_implementation.md` (for task-level).

### Step 2: Validate Transition

Allowed status transitions:

| From | Allowed To |
|------|-----------|
| `TODO` | `WIP`, `BLOCKED:reason`, `CUT` |
| `WIP` | `DONE`, `BLOCKED:reason`, `CUT` |
| `BLOCKED:reason` | `WIP`, `CUT` |
| `CUT` | Only via **Resurrection** (Operation D) |
| `DONE` | Only via **Invalidation** (see below) |

**Invalid transitions:** `TODO` → `DONE` (must pass through `WIP`). `DONE` → `WIP` (use invalidation instead).

### Step 3: Update Plan Frontmatter

In the plan's `_overview.md`, update:

```yaml
status: WIP          # New status
last_updated: 2026-02-16  # Today's date
```

### Step 4: Update Task Rows (If Task-Level)

In `80_implementation.md`, update the task's Status column:

```markdown
| ✅ | Task description | `scope` | `[KNOWN]` |
```

Use the correct emoji prefix: ⏳ (TODO), 🔄 (WIP), ✅ (DONE), 🚧 (BLOCKED), 🚫 (CUT).

### Step 5: Update Phase Completion Checklist

If marking a task DONE, check the corresponding box in the phase's completion checklist:

```markdown
- [x] Exit gate met
```

### Step 6: Sync Root `_overview.md`

Update the plan's row in `.agent_plan/day_dream/_overview.md`:

- **Plans table:** Update the Status column
- **Current Sprint table:** Update status and Next Action columns (if plan is in sprint)

---

## Operation B: Phase Progression

Move to the next phase of an implementation plan.

### Step 1: Verify Current Phase Exit Gate

Read the current phase in `80_implementation.md`. ALL exit gate checkboxes MUST be checked:

```markdown
### Exit Gate
- [x] Condition 1 met
- [x] Condition 2 met
```

If any checkbox is unchecked → STOP. Complete the missing gate requirements first.

### Step 2: Verify All Tasks Resolved

Every task in the current phase must be ✅ `[DONE]` or 🚫 `[CUT]`. No ⏳ `[TODO]` or 🔄 `[WIP]` tasks may remain.

### Step 3: Complete Phase Checklist

Mark all items in the phase's completion checklist:

```markdown
### P{N} Completion Checklist
- [x] Exit gate met
- [x] All tasks marked ✅ or 🚫
- [x] Manual verification steps pass
```

### Step 4: Update `80_implementation.md` Frontmatter

```yaml
current_phase: 2              # Increment to next phase number
phase_name: "Core Leaf Skills" # Name of the new phase
status: WIP                    # Reset to WIP for new phase
last_updated: 2026-02-16      # Today's date
```

### Step 5: Update Plan `_overview.md`

Update `last_updated` in the plan's `_overview.md` frontmatter.

### Step 6: Sync Root `_overview.md`

Update the Current Sprint table with the new phase and next action:

```markdown
| PP03_dream_sop_skills | p02_core_leaf_skills | 🔄 [WIP] | Create dream-update SKILL.md |
```

---

## Operation C: Scope Modification

Add, remove, or change tasks or phases in a plan.

### Step 1: Assess Impact

Determine if the modification changes the plan's magnitude:

| Change | Magnitude Impact |
|--------|-----------------|
| Add 1-2 tasks to existing phase | Usually none |
| Add a new phase | May increase magnitude |
| Remove tasks/phases | May decrease magnitude |
| Add cross-module dependency | Likely increases magnitude |

### Step 2: Update Tasks (Adding)

Add new task rows to the appropriate phase in `80_implementation.md`:

```markdown
| ⏳ | New task description | `scope` | `[KNOWN]` |
```

Respect phase limits: P0 max 5 tasks, `[KNOWN]` only.

### Step 3: Update Tasks (Removing — Cut)

Do NOT delete task rows. Mark them CUT and add to the Cut List:

```markdown
| 🚫 | Removed task description | `scope` | `[KNOWN]` |
```

Add to the Cut List at the bottom of `80_implementation.md`:

```markdown
## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| Task description | 2026-02-16 | Reason for cutting |
```

### Step 4: Update Decisions Log

Record scope changes in the Decisions Log:

```markdown
## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-02-16 | Added phase P4 for integration testing | Discovered cross-module risk | Agent analysis |
```

### Step 5: Update Children Table

If adding/removing phases (directories), update the Children table in `_overview.md`:

```markdown
| p04_integration_testing/ | Plan | ⏳ [TODO] | Cross-module integration verification |
```

### Step 6: Update Magnitude (If Changed)

If scope changes push the plan to a different magnitude, update `magnitude` in `_overview.md` frontmatter.

### Step 7: Update `last_updated`

In both `_overview.md` and `80_implementation.md` frontmatter.

---

## Operation D: Plan Resurrection

Bring back a CUT or archived plan to active status.

### Step 1: Locate the Plan

- **CUT plans:** Still in `.agent_plan/day_dream/` with `status: CUT`
- **Archived plans:** In `.agent_plan/day_dream/_archive/` or `_completed/YYYY-QN/`

### Step 2: Move Back (If Archived)

Move the plan folder from `_archive/` or `_completed/` back to `.agent_plan/day_dream/`:

```bash
mv .agent_plan/day_dream/_archive/PP04_old_plan/ .agent_plan/day_dream/PP04_old_plan/
```

**Keep the original plan number.** Do NOT reassign a new number.

### Step 3: Reset Status

Update the plan's `_overview.md` frontmatter:

```yaml
status: TODO           # or WIP if resuming immediately
last_updated: 2026-02-16
```

### Step 4: Review and Update Content

- Check if assumptions still hold — update `knowledge_gaps` if not
- Check `depends_on` — verify dependencies still exist and are valid
- Review task statuses — previously-completed tasks remain ✅, uncompleted reset to ⏳

### Step 5: Re-Register in Root `_overview.md`

Add the plan back to three sections:

1. **Plans table:** Add row with current status
2. **Current Sprint:** Add if work starts immediately
3. **Reading Order:** Insert at appropriate position

### Step 6: Update Dependency Targets

If the resurrected plan `blocks` other plans, verify those plans' `depends_on` arrays still reference it.

---

## Validation Checklist

### After Any Update
- [ ] `last_updated` is today's date in ALL modified frontmatter files
- [ ] Status markers use correct emoji prefix + bracketed code
- [ ] Root `_overview.md` Plans table reflects current plan status
- [ ] Root `_overview.md` Current Sprint reflects current phase (if applicable)

### After Status Update
- [ ] Status transition is valid (see allowed transitions table)
- [ ] Task-level and plan-level statuses are consistent
- [ ] Phase completion checklist updated (if tasks marked DONE)

### After Phase Progression
- [ ] ALL exit gate checkboxes are checked for completed phase
- [ ] ALL tasks in completed phase are ✅ or 🚫 (no ⏳ or 🔄 remaining)
- [ ] `current_phase` and `phase_name` incremented in `80_implementation.md`
- [ ] Phase completion checklist fully checked

### After Scope Modification
- [ ] Cut items added to Cut List (not deleted)
- [ ] Decisions Log entry added
- [ ] Magnitude updated if scope changed substantially
- [ ] Children table updated if phases added/removed

### After Resurrection
- [ ] Plan folder is in `.agent_plan/day_dream/` (not archive)
- [ ] Original plan number preserved
- [ ] Plan re-registered in root `_overview.md` (Plans + Reading Order)
- [ ] Dependencies and blockers validated
- [ ] Knowledge gaps reviewed and updated

---

## Common Mistakes

| Mistake | Why It's Wrong | Do Instead |
|---------|---------------|------------|
| Skipping `TODO` → `WIP` and going straight to `DONE` | Status must progress through `WIP` | Mark `WIP` first, then `DONE` after verification |
| Progressing phase with unchecked exit gates | Exit gates are hard constraints | Complete ALL gate conditions before progressing |
| Deleting task rows instead of marking CUT | Loses history and audit trail | Mark 🚫 `[CUT]` and add to Cut List |
| Forgetting to sync root `_overview.md` | Plan becomes invisible/stale in navigation | Always update Plans table + Current Sprint |
| Reassigning a new number to resurrected plan | Numbers are immutable creation-order | Keep the original plan number |
| Updating `_overview.md` but not `80_implementation.md` | Creates frontmatter inconsistency | Update ALL affected frontmatter files |
| Changing magnitude without recording rationale | Scope changes need documentation | Add entry to Decisions Log |
