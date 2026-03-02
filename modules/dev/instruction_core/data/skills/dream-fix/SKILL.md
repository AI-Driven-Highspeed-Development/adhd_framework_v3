---
name: dream-fix
description: "Step-by-step SOP for fixing DREAM plan validation errors — frontmatter issues, status syntax errors, missing sections, line limit violations, broken cross-references, and structural problems. Use this skill when fixing, repairing, or correcting existing plan documents."
---

# Fix Plan Validation Errors

Step-by-step SOPs for repairing broken DREAM plan documents — frontmatter issues, status syntax errors, missing sections, line limit violations, and cross-reference problems.

## When to Use

- Plan has validation errors (frontmatter missing fields, wrong types)
- Status markers are malformed or inconsistent
- Required sections are missing or in wrong order
- Documents exceed line limits
- Cross-references are broken (children table vs actual files, root `_overview.md` out of sync)
- Plan fails `dream validate` checks

**Not a fix?** If updating plan content or status during normal work → use `dream-update`. If closing a completed plan → use `dream-close`.

---

## Prerequisites

- Target plan identified — know which plan and which document has errors
- Know what is broken — call `dream_validate` to identify issues, or use manual inspection / error reports
- Plan exists in `.agent_plan/day_dream/` (or `_archive/` / `_completed/`)

---

## Fix Category A: Frontmatter Fixes

Repair missing, invalid, or malformed YAML frontmatter in plan documents.

### Step 1: Identify the Document Type

| Document | Where Frontmatter Lives |
|----------|------------------------|
| Plan-level metadata | `{PlanFolder}/_overview.md` |
| Implementation tracking | `{PlanFolder}/80_implementation.md` |
| Executive summary (SP) | `{PlanFolder}/01_executive_summary.md` |
| Merged summary (PP) | `{PlanFolder}/01_summary.md` |

### Step 2: Validate Against Schema

#### `_overview.md` Required Fields

| Field | Type | Valid Values |
|-------|------|-------------|
| `name` | string | snake_case, matches folder suffix |
| `type` | enum | `system`, `procedure` |
| `magnitude` | enum | `Trivial`, `Light`, `Standard`, `Heavy`, `Epic` |
| `status` | enum | `TODO`, `WIP`, `DONE`, `BLOCKED:reason`, `CUT` |
| `origin` | string | Path to triggering document |
| `last_updated` | date | `YYYY-MM-DD` format |

#### `_overview.md` Recommended Fields

| Field | Type | Notes |
|-------|------|-------|
| `depends_on` | string[] | Plans this structurally requires |
| `blocks` | string[] | Plans that wait on this |
| `knowledge_gaps` | string[] | Missing expertise |

#### `_overview.md` Conditional Fields

| Field | Type | When Required |
|-------|------|---------------|
| `priority` | enum | Only when `emergency` — omit for `normal` |
| `emergency_declared_at` | datetime | REQUIRED when `priority: emergency` |
| `invalidated_by` | string | Victim plans only |
| `invalidation_scope` | string | REQUIRED when `invalidated_by` is set |
| `invalidation_date` | date | REQUIRED when `invalidated_by` is set |

#### `80_implementation.md` Required Fields

| Field | Type | Valid Values |
|-------|------|-------------|
| `current_phase` | integer | Zero-indexed phase number |
| `phase_name` | string | Human-readable phase name |
| `status` | enum | `TODO`, `WIP`, `DONE` |
| `last_updated` | date | `YYYY-MM-DD` |

### Step 3: Apply Fixes

For each missing or invalid field:

1. **Missing field** → Add field with correct value. Infer from context where possible.
2. **Wrong type** → Convert to correct type (e.g., string `"3"` → integer `3`).
3. **Invalid enum value** → Replace with nearest valid value.
4. **Bad date format** → Convert to `YYYY-MM-DD`.
5. **Missing YAML delimiters** → Ensure frontmatter is wrapped in `---` markers.

### Step 4: Validate Fix

Re-read the frontmatter. Confirm all required fields present with valid types.

---

## Fix Category B: Status Syntax Fixes

Repair malformed or inconsistent status markers.

### Valid Status Markers

| Marker | Meaning |
|--------|---------|
| ⏳ `[TODO]` | Not started |
| 🔄 `[WIP]` | In progress |
| ✅ `[DONE]` | Complete |
| ✅ `[DONE:invalidated-by:XXnn]` | Complete but assumptions compromised |
| 🚧 `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 `[CUT]` | Removed from scope |

### Common Status Errors

| Error | Fix |
|-------|-----|
| Missing emoji prefix | Add correct emoji: ⏳🔄✅🚧🚫 |
| Wrong emoji for status | Match emoji to status code |
| `BLOCKED` without reason | Add kebab-case reason: `BLOCKED:awaiting-api` |
| `BLOCKED` reason with spaces | Convert to kebab-case: `awaiting api` → `awaiting-api` |
| `invalidated-by` without plan ID | Add plan prefix: `DONE:invalidated-by:{XX}{nn}` |
| Bare text status (no brackets) | Wrap in brackets: `DONE` → `[DONE]` |
| Frontmatter uses emoji | Frontmatter `status` is bare enum only: `WIP` not `🔄 [WIP]` |

### Status Consistency Rules

| Level | Rule |
|-------|------|
| **Task → Phase** | If ALL tasks in a phase are ✅/🚫 → phase should be DONE |
| **Phase → Plan** | If ALL phases are DONE → plan should be DONE |
| **Task rows** | Use emoji + brackets in markdown tables |
| **Frontmatter** | Use bare enum value only (no emoji, no brackets) |
| **Children table** | Use emoji + brackets (same as task rows) |
| **Root `_overview.md`** | Plans table uses emoji + brackets |

### Fix Process

1. Scan all status markers in the document
2. Fix format errors (emoji, brackets, kebab-case)
3. Check consistency between task statuses and phase/plan status
4. Update frontmatter `status` field to match actual state
5. Update `last_updated` to today's date

---

## Fix Category C: Structural Fixes

Repair missing required sections or wrong section order.

### Required Sections by Document Type

#### `_overview.md`

| Section | Required | Order |
|---------|----------|-------|
| YAML frontmatter | ✅ | First |
| `# {Plan Name}` | ✅ | After frontmatter |
| `## Purpose` | ✅ | 1st section |
| `## Children` | ✅ | 2nd section |
| `## Integration Map` | ✅ | 3rd section |
| `## Reading Order` | ✅ | 4th section |

#### `80_implementation.md`

| Section | Required | Notes |
|---------|----------|-------|
| YAML frontmatter | ✅ | Phase tracking fields |
| `# 80 — Implementation Plan` | ✅ | Title |
| Status Legend table | ✅ | Reference for markers |
| Phase sections (`## ⚙️ Phase N:`) | ✅ | At least one phase |
| Exit Gate per phase | ✅ | Checkbox list |
| Tasks table per phase | ✅ | Status/Task/Scope/Difficulty columns |
| Verification per phase | ✅ | Manual verification steps |
| Completion Checklist per phase | ✅ | Checkbox list |
| Decisions Log | ✅ | Can be empty |
| Cut List | ✅ | Can be empty |

#### Children Table Format

Exactly 4 columns:

| Column | Valid Values |
|--------|-------------|
| Name | File or directory name |
| Type | `Plan` (directory) or `Task` (file) ONLY |
| Status | Status marker with emoji |
| Description | One-line summary |

**Invalid Type values:** `Doc`, `Feature`, `Module`, `Asset` — replace with `Plan` or `Task`.

### Fix Process

1. Compare document sections against the required list above
2. Add missing sections with placeholder content: `N/A — [reason]`
3. Reorder sections if in wrong order
4. Fix Children table Type column — only `Plan` or `Task` are valid

---

## Fix Category D: Line Limit Fixes

Repair documents that exceed line limits.

### Line Limits

| Document | Max Lines |
|----------|-----------|
| `_overview.md` | 100 |
| `01_executive_summary.md` | 150 |
| `01_summary.md` | 200 |
| `02_architecture.md` | 200 |
| `80_implementation.md` | 200 per phase |
| Feature (full) | 300 |
| Feature (simple) | 100 |
| Task file | 100 |
| Asset file | 100 (excl. diagrams) |

### Fix Process

1. Count lines: `wc -l <file>`
2. If over limit, apply reduction strategies in order:
   a. **Move reference material** to `assets/` subfolder with `→ See [file](assets/file.md)` pointer
   b. **Compress verbose prose** — convert paragraphs to tables
   c. **Remove redundant examples** — keep 1, cut extras
   d. **Split into multiple documents** — extract sections to child files
3. After reduction, verify no required sections were removed
4. Re-count to confirm compliance

---

## Fix Category E: Cross-Reference Fixes

Repair broken links between plan documents.

### Common Cross-Reference Issues

| Issue | Where to Check | Fix |
|-------|---------------|-----|
| Children table lists file that doesn't exist | `_overview.md` Children table | Remove row or create the missing file |
| File exists but not in Children table | `_overview.md` Children table | Add row for the file |
| Root `_overview.md` has wrong plan status | Root `_overview.md` Plans table | Update status to match plan's `_overview.md` |
| Root `_overview.md` missing plan entry | Root `_overview.md` Plans table | Add row for the plan |
| Root Current Sprint has stale entries | Root `_overview.md` Sprint table | Update or remove completed/stale entries |
| Back-link at bottom of file points to wrong path | Document footer | Fix the relative path |
| `depends_on` references non-existent plan | Plan `_overview.md` frontmatter | Remove reference or correct plan ID |

### Fix Process

1. List actual files in the plan directory
2. Compare against Children table entries in `_overview.md`
3. Add missing entries, remove entries for deleted files
4. Verify root `_overview.md` Plans table matches plan's actual status
5. Check `depends_on` and `blocks` arrays — verify referenced plans exist
6. Update `last_updated` in all modified files

---

## Validation Checklist

After applying fixes, call `dream_validate` to confirm all issues are resolved. Then verify manually:

### Frontmatter
- [ ] All required fields present with valid types
- [ ] `last_updated` set to today's date
- [ ] `status` field uses bare enum (no emoji in frontmatter)
- [ ] Date fields use `YYYY-MM-DD` format

### Status Markers
- [ ] All markers use correct emoji prefix
- [ ] All markers use bracket syntax in markdown
- [ ] `BLOCKED:reason` uses kebab-case
- [ ] Task ↔ phase ↔ plan statuses are consistent

### Structure
- [ ] All required sections present
- [ ] Sections in correct order
- [ ] Children table Type column uses only `Plan` or `Task`

### Line Limits
- [ ] Document within line limit for its type
- [ ] Extracted content properly linked from parent

### Cross-References
- [ ] Children table matches actual filesystem contents
- [ ] Root `_overview.md` reflects current plan state
- [ ] `depends_on` / `blocks` reference existing plans

---

## Common Mistakes

| Mistake | Why It's Wrong | Do Instead |
|---------|---------------|------------|
| Adding emoji to frontmatter status | Frontmatter is YAML data — emoji breaks parsing | Use bare enum: `status: WIP` |
| Fixing status without updating `last_updated` | Stale dates break auditability | Always set `last_updated` to today |
| Removing sections instead of adding `N/A` | Violates mandatory skeleton rule | Write `N/A — [reason]` for inapplicable sections |
| Using `Doc` or `Feature` in Children Type column | Only `Plan` and `Task` are valid primitives | Use `Plan` (directory) or `Task` (file) |
| Fixing plan but not updating root `_overview.md` | Root goes out of sync | Always sync root after plan-level fixes |
| Trimming content to meet line limits by cutting required sections | Required sections are mandatory | Move content to `assets/` instead of deleting |
| Fixing one status marker but leaving others inconsistent | Partial fix creates worse confusion | Scan and fix ALL markers in the document |
