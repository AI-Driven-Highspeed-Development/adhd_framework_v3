---
name: dream-close
description: "Step-by-step SOP for closing and completing DREAM plans — exit gate verification, status rollup, State Deltas documentation, root _overview cleanup, and optional archival. Use this skill when completing, archiving, or formally closing a plan."
---

# Close a Plan

Step-by-step SOP for closing a DREAM plan — verifying all exit gates, rolling up status, documenting State Deltas, updating root navigation, and archiving.

## When to Use

- All plan work is complete — every phase finished, every task resolved
- Plan is ready to be marked DONE and archived
- Formally closing a plan that was fully CUT (all children CUT)
- Performing the final step after the last phase's exit gate is met

**Not a close?** If updating status mid-execution → use `dream-update`. If creating a new plan → use `dream-create-pp` or `dream-create-sp`.

---

## Prerequisites

- Plan exists in `.agent_plan/day_dream/` with `status: WIP` (or all children `CUT`)
- All phases have been executed — no ⏳ `[TODO]` or 🔄 `[WIP]` tasks remain
- Root `.agent_plan/day_dream/_overview.md` exists

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

---

## Closure Gate Criteria

ALL of the following must be true before a plan can close:

| Gate | Requirement |
|------|-------------|
| **All children resolved** | Every child is ✅ `[DONE]` or 🚫 `[CUT]` — no ⏳ or 🔄 remaining |
| **All exit gates checked** | Every phase's exit gate checkboxes are all `[x]` |
| **State Delta prepared** | Entry drafted documenting what changed in the codebase |
| **Module Index updated** | If this plan introduced new modules: table row AND spec file exist in root `_overview.md` |
| **Invalidations identified** | List of any previously-DONE plans whose assumptions this work compromises |
| **`last_updated` current** | Set to today's date in plan frontmatter |
| **`dream validate` passes** | Plan structure passes validation (when available) |

If ANY gate is not met → STOP. Resolve the gap before proceeding.

---

## Step-by-Step SOP

### Step 1: Verify ALL Phase Exit Gates

Open `80_implementation.md` (for PP plans) or the plan file itself (for SP plans). For EACH phase, confirm every exit gate checkbox is checked:

```markdown
### Exit Gate
- [x] Condition 1 met
- [x] Condition 2 met
- [x] Condition 3 met
```

If any checkbox is unchecked, either:
- Complete the missing work, OR
- Document why the gate no longer applies and mark the associated task 🚫 `[CUT]`

---

### Step 2: Verify ALL Task Rows Are Resolved

Scan every task table in `80_implementation.md`. Every row must be ✅ `[DONE]` or 🚫 `[CUT]`:

```markdown
| ✅ | Task one | `scope` | `[KNOWN]` |
| ✅ | Task two | `scope` | `[KNOWN]` |
| 🚫 | Removed task | `scope` | `[KNOWN]` |
```

**No ⏳ `[TODO]` or 🔄 `[WIP]` rows may remain.** If unfinished work exists:
- Complete it, OR
- Mark it 🚫 `[CUT]` and add to the Cut List with rationale

---

### Step 3: Complete Final Phase Checklist

Mark all items in the last phase's completion checklist:

```markdown
### P{N} Completion Checklist
- [x] Exit gate met
- [x] All tasks marked ✅ or 🚫
- [x] Manual verification steps pass
```

---

### Step 4: Create State Deltas Entry

Draft a State Delta entry documenting what this plan changed in the codebase. This will be appended to root `_overview.md`.

#### State Deltas Format

```markdown
### ✅ {PlanFolder} — {Month} {Year}

- {module}: {what changed}
- {module}: {what changed}
- {new_module}: new module, {purpose}
```

**Rules:**

| Rule | Detail |
|------|--------|
| Format | `{module}: {what changed}` per line |
| Prefix | `✅` for DONE plans, `🚫` for fully-CUT plans |
| Scope | List every module or artifact modified by this plan |
| Granularity | One line per module — summarize, don't itemize every file |
| New modules | Prefix with `new module,` before the description |
| Active cap | Root `_overview.md` keeps 20 most recent entries |
| Overflow | Oldest entries move to `_state_deltas_archive.md` |

**Example:**

```markdown
### ✅ {PlanFolder} — {Mon YYYY}

- {module}: {what changed}
- {module}: {what changed}
- {new_module}: new module, {purpose}
```

---

### Step 5: Update Plan Frontmatter

#### For PP Plans (`_overview.md`)

```yaml
status: DONE
last_updated: YYYY-MM-DD    # Today's date
```

#### For SP Plans (plan file)

```yaml
status: DONE
last_updated: YYYY-MM-DD
```

#### For `80_implementation.md` (PP Plans)

```yaml
status: DONE
last_updated: YYYY-MM-DD
```

---

### Step 6: Update Children Table Status

In the plan's `_overview.md`, update the Children table so every child reflects its final status:

```markdown
| 01_summary.md | Task | ✅ [DONE] | Merged exec summary + architecture |
| 80_implementation.md | Task | ✅ [DONE] | Phased implementation roadmap |
| p00_phase_name/ | Plan | ✅ [DONE] | Phase 0 deliverables |
| p01_phase_name/ | Plan | ✅ [DONE] | Phase 1 deliverables |
| p02_phase_name/ | Plan | 🚫 [CUT] | Descoped — see Cut List |
```

---

### Step 7: Update Root `_overview.md`

Update `.agent_plan/day_dream/_overview.md` in four places:

#### 7a. Plans Table

Change the plan's Status column to DONE:

```markdown
| [PP{NN}_{name}/](./PP{NN}_{name}/_overview.md) | Procedure | ✅ [DONE] | normal | {One-line description} |
```

#### 7b. Current Sprint Table

Remove the plan's rows from the Current Sprint table (completed plans are not current work).

#### 7c. State Deltas Section

Append the State Delta entry drafted in Step 4:

```markdown
## State Deltas

### ✅ {PlanFolder} — {Mon YYYY}

- {module}: {what changed}
- {module}: {what changed}
```

If there are already 20 entries, move the oldest entry to `_state_deltas_archive.md` before appending.

#### 7d. Reading Order

Update the plan's entry with a completion note or remove if no longer relevant for navigation.

---

### Step 8: Check for Invalidations

Review whether this plan's changes compromise assumptions of any previously-DONE plan:

1. Read other DONE plans' key assumptions
2. If this plan modifies behavior they relied on → that plan is invalidated

#### Reporting Invalidations

If invalidations exist, update the **victim plan's** `_overview.md` frontmatter:

```yaml
invalidated_by: {XX}{nn}
invalidation_scope: "{what is compromised}"
invalidation_date: YYYY-MM-DD
```

And update the victim's status in root `_overview.md` Plans table:

```markdown
| [SP{NN}_{name}/](./SP{NN}_{name}/_overview.md) | System | ✅ [DONE:invalidated-by:{XX}{nn}] | normal | ... |
```

**Sibling firewall note:** The CLOSING agent writes to the victim plan (authorized exception for invalidation reporting).

---

### Step 9: Archive (Optional)

Move the completed plan to the archive directory if keeping the active directory clean:

```bash
mv .agent_plan/day_dream/PP{NN}_{name}/ .agent_plan/day_dream/_completed/YYYY-QN/PP{NN}_{name}/
```

#### Archival Rules

| Rule | Detail |
|------|--------|
| Archive directory | `_completed/YYYY-QN/` (e.g., `_completed/YYYY-QN/`) |
| Create directory if needed | `mkdir -p .agent_plan/day_dream/_completed/YYYY-QN/` |
| Links still work | Root `_overview.md` links update to `_completed/` path |
| Alternative | Plans CAN stay in place — archival is optional for clean navigation |
| When to archive | When active directory has >10 plans, or plan is >3 months old |
| When to keep in place | Active reference material, frequently cited by other plans |

---

### Step 10: Final Validation

Run through the full Validation Checklist below.

---

## Validation Checklist

### Closure Gates
- [ ] ALL phase exit gate checkboxes checked (`[x]`)
- [ ] ALL task rows are ✅ `[DONE]` or 🚫 `[CUT]` (no ⏳ or 🔄 remaining)
- [ ] Final phase completion checklist fully checked
- [ ] State Delta entry drafted

### Plan Frontmatter
- [ ] `status: DONE` in plan's `_overview.md`
- [ ] `last_updated` is today's date
- [ ] `80_implementation.md` frontmatter status is `DONE` (PP plans)
- [ ] Children table reflects final status of each child

### Root `_overview.md`
- [ ] Plans table status updated to `✅ [DONE]`
- [ ] Plan removed from Current Sprint table
- [ ] State Delta entry appended to State Deltas section
- [ ] Reading Order updated

### Invalidations
- [ ] Checked for invalidated plans (can be "none found")
- [ ] Victim plans updated with `invalidated_by` fields (if any)
- [ ] Victim plan status updated in root `_overview.md` (if any)

### Module Index (If Applicable)
- [ ] New modules have table row in root Module Index
- [ ] New modules have spec file in plan's `modules/` directory
- [ ] Module spec frontmatter includes `origin` and `knowledge_gaps`

### Archive (Optional)
- [ ] Plan moved to `_completed/YYYY-QN/` (if archiving)
- [ ] Root `_overview.md` links updated to archived path (if archiving)

---

## Common Mistakes

| Mistake | Why It's Wrong | Do Instead |
|---------|---------------|------------|
| Closing with ⏳ or 🔄 tasks remaining | Violates closure gate — all children must be resolved | Mark remaining tasks ✅ or 🚫 first |
| Skipping State Delta | Gate condition — plan CANNOT mark DONE without one | Always append a State Delta entry |
| Forgetting to remove from Current Sprint | Stale entries create confusion | Remove completed plan rows from sprint table |
| Not checking for invalidations | Silently breaks assumptions of other plans | Review DONE plans for compromised assumptions |
| Deleting the plan instead of archiving | Loses history, breaks references | Move to `_completed/` or keep in place |
| Appending >20 State Deltas without overflow | Root `_overview.md` becomes unwieldy | Move oldest to `_state_deltas_archive.md` |
| Closing a fully-CUT plan as DONE | CUT plans have their own status | Use 🚫 `[CUT]` status, not ✅ `[DONE]` |
| Updating invalidated plan without `invalidation_scope` | "Partially invalidated" is meaningless | State WHAT is compromised specifically |
