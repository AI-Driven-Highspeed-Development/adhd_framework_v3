---
name: dream-validate
description: "Step-by-step SOP for validating DREAM plan structure — frontmatter completeness, status consistency, cross-reference integrity, line limits, and structural compliance. Use this skill when checking, auditing, or validating plans for correctness."
---

# Validate Plan Structure

Step-by-step SOP for auditing DREAM plans — checking frontmatter, status consistency, structural compliance, cross-references, line limits, and content quality.

## When to Use

- Verifying a plan is structurally correct before or after changes
- Auditing all active plans for compliance
- Checking a plan after creation, update, or fix operations
- Preparing a plan for closure (pre-closure validation)
- Running a periodic health check on the plan tree

**Not a validate?** If actively fixing errors found during validation → use `dream-fix`. If closing a plan → use `dream-close`.

> **MCP tool available:** Call `dream_validate` for automated validation — covers frontmatter, status syntax, line limits, and DAG cycle detection. The manual protocol below details each check for when deeper inspection or custom auditing is needed.

---

## Prerequisites

- Target plan(s) identified — specific plan folder or "all plans"
- Plan directory exists in `.agent_plan/day_dream/` (or `_archive/` / `_completed/`)
- Root `.agent_plan/day_dream/_overview.md` exists

---

## Validation Protocol

Run checks in the order listed. Record each check result as PASS, WARN, or FAIL.

### Check 1: Frontmatter Validation

Verify `_overview.md` frontmatter has all required fields with valid values.

#### Required Fields

| Field | Type | Valid Values |
|-------|------|-------------|
| `name` | string | snake_case, must match folder suffix |
| `type` | enum | `system`, `procedure` |
| `magnitude` | enum | `Trivial`, `Light`, `Standard`, `Heavy`, `Epic` |
| `status` | enum | `TODO`, `WIP`, `DONE`, `BLOCKED:reason`, `CUT` |
| `origin` | string | Path to triggering document |
| `last_updated` | date | `YYYY-MM-DD` format |

#### Recommended Fields (WARN if missing)

| Field | Type |
|-------|------|
| `depends_on` | string[] |
| `blocks` | string[] |
| `knowledge_gaps` | string[] |

#### Conditional Fields

| Field | Condition | Severity if Missing |
|-------|-----------|--------------------|
| `priority` | Only `emergency` — omit for normal | PASS if omitted |
| `emergency_declared_at` | Required when `priority: emergency` | FAIL |
| `invalidated_by` | Victim plans only | PASS if omitted |
| `invalidation_scope` | Required when `invalidated_by` is set | FAIL |
| `invalidation_date` | Required when `invalidated_by` is set | FAIL |

#### `80_implementation.md` Frontmatter

| Field | Type | Severity |
|-------|------|----------|
| `current_phase` | integer | FAIL if missing |
| `phase_name` | string | FAIL if missing |
| `status` | enum | FAIL if missing |
| `last_updated` | date | FAIL if missing |

#### Validation Rules

| Check | PASS | FAIL |
|-------|------|------|
| `name` matches folder suffix | `PP{NN}_{name}` → `name: {name}` | Mismatch |
| `type` is valid enum | `system` or `procedure` | Any other value |
| `status` is bare enum | `WIP` (no emoji, no brackets) | `🔄 [WIP]` in frontmatter |
| `last_updated` is valid date | `YYYY-MM-DD` | `Feb 16`, `16/02/2026` |
| `magnitude` is valid enum | Exact case: `Standard` | `standard`, `STANDARD`, `Med` |

---

### Check 2: Status Consistency

Verify status markers are well-formed and logically consistent across the plan hierarchy.

#### Status Marker Format

| Marker | Valid Format |
|--------|-------------|
| ⏳ `[TODO]` | Emoji + space + bracketed code |
| 🔄 `[WIP]` | Emoji + space + bracketed code |
| ✅ `[DONE]` | Emoji + space + bracketed code |
| ✅ `[DONE:invalidated-by:XXnn]` | Emoji + space + bracketed code with suffix |
| 🚧 `[BLOCKED:reason]` | Emoji + space + brackets, kebab-case reason |
| 🚫 `[CUT]` | Emoji + space + bracketed code |

#### Consistency Checks

| Check | Rule | Severity |
|-------|------|----------|
| Task → Phase | If ALL tasks in phase are ✅/🚫 → phase exit gate should be fully checked | WARN |
| Phase → Plan | If ALL phases DONE → plan status should be `DONE` | WARN |
| Frontmatter vs display | Frontmatter bare enum must match displayed status | FAIL |
| Children table vs child | Children table status must match child's frontmatter status | FAIL |
| Root Plans table vs plan | Root `_overview.md` status must match plan's `_overview.md` status | FAIL |
| BLOCKED has reason | `BLOCKED:reason` with kebab-case, never bare `BLOCKED` | FAIL |
| CUT in Cut List | CUT tasks should have entry in Cut List section | WARN |

---

### Check 3: Structural Validation

Verify required sections exist and are in correct order.

#### `_overview.md` Required Structure

| # | Section | Required |
|---|---------|----------|
| 1 | YAML frontmatter | ✅ |
| 2 | `# {Plan Name}` heading | ✅ |
| 3 | `## Purpose` | ✅ |
| 4 | `## Children` (4-column table) | ✅ |
| 5 | `## Integration Map` | ✅ |
| 6 | `## Reading Order` | ✅ |

#### `80_implementation.md` Required Structure

| # | Section | Required |
|---|---------|----------|
| 1 | YAML frontmatter | ✅ |
| 2 | Title heading | ✅ |
| 3 | Status Legend | ✅ |
| 4 | At least one Phase section | ✅ |
| 5 | Exit Gate per phase | ✅ |
| 6 | Tasks table per phase | ✅ |
| 7 | Verification per phase | ✅ |
| 8 | Completion Checklist per phase | ✅ |
| 9 | Decisions Log | ✅ |
| 10 | Cut List | ✅ |

#### Children Table Validation

| Check | Rule | Severity |
|-------|------|----------|
| Column count | Exactly 4: Name, Type, Status, Description | FAIL |
| Type values | Only `Plan` or `Task` — never `Doc`, `Feature`, `Module` | FAIL |
| Type correctness | `Plan` = directory with `_overview.md`; `Task` = single `.md` file | FAIL |

---

### Check 4: Cross-Reference Validation

Verify links between documents are intact and consistent.

#### Checks

| Check | How | Severity |
|-------|-----|----------|
| Children table → filesystem | Every entry in Children table has a matching file/directory | FAIL |
| Filesystem → Children table | Every `.md` file and subdirectory appears in Children table | WARN |
| Root Plans table → plan folder | Every plan in root `_overview.md` Plans table exists | FAIL |
| Plan folder → Root Plans table | Every plan directory has an entry in root `_overview.md` | WARN |
| `depends_on` targets exist | Referenced plans are real plan directories | FAIL |
| `blocks` is bidirectional | If A `depends_on: B`, B should have `blocks: A` | WARN |
| Back-links valid | Footer links point to correct parent | WARN |
| Root Current Sprint | Sprint entries reference existing plans with correct status | WARN |

---

### Check 5: Line Limit Validation

Verify documents do not exceed maximum allowed lines.

#### Limits

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

#### Check Process

1. Count lines for each document: `wc -l <file>`
2. For `80_implementation.md`, count lines per phase section (not total)
3. Record FAIL for any document exceeding its limit

---

### Check 6: Content Quality

Verify content completeness and quality markers.

| Check | Rule | Severity |
|-------|------|----------|
| Exit gates defined | Every phase has `### Exit Gate` with checkbox items | FAIL |
| Verification sections | Every phase has `### Verification` or `### How to Verify` | WARN |
| Decisions Log exists | `80_implementation.md` has Decisions Log section | WARN |
| Cut List exists | `80_implementation.md` has Cut List section | WARN |
| Purpose is substantive | `## Purpose` is not empty or "TBD" | WARN |
| `N/A` has reason | Inapplicable sections use `N/A — [reason]` not bare `N/A` | WARN |
| No `[RESEARCH]` in P0 | Phase 0 tasks must be `[KNOWN]` only | FAIL |
| P0 task limit | Phase 0 has ≤5 tasks | FAIL |

---

## Validation Output Format

Report findings using this format. Group by severity, then by check category.

### Summary

```
Plan: {PlanFolder}
Date: YYYY-MM-DD
Result: PASS | WARN | FAIL

  FAIL: {count}
  WARN: {count}
  PASS: {count}
```

### Detail Format

```
[FAIL] Check 1 — Frontmatter: `status` field missing in _overview.md
[FAIL] Check 3 — Structure: `## Purpose` section missing in _overview.md
[WARN] Check 2 — Status: CUT task "Feature X" not in Cut List
[WARN] Check 4 — Cross-Ref: {PlanA} has depends_on: {PlanB}, but {PlanB} missing blocks: {PlanA}
[PASS] Check 5 — Line Limits: All documents within limits
[PASS] Check 6 — Content: All quality checks passed
```

### Overall Result Rules

| Condition | Result |
|-----------|--------|
| Zero FAIL, zero WARN | **PASS** |
| Zero FAIL, any WARN | **WARN** — plan is functional but has hygiene issues |
| Any FAIL | **FAIL** — plan has structural errors that must be fixed |

---

## Full Plan Audit

To validate ALL active plans at once:

### Step 1: List All Plans

```bash
ls -d .agent_plan/day_dream/[A-Z]*/ | grep -v _archive | grep -v _completed
```

### Step 2: Run Protocol Per Plan

For each plan directory, run Checks 1–6 above.

### Step 3: Cross-Plan Checks

After individual plan validation, run these cross-plan checks:

| Check | Rule | Severity |
|-------|------|----------|
| Plan numbering | No duplicate plan numbers (PPnn, SPnn) | FAIL |
| Dependency cycles | No circular `depends_on` chains | FAIL |
| Root `_overview.md` completeness | All plans appear in root Plans table | WARN |
| State Deltas count | Root `_overview.md` has ≤20 active State Deltas | WARN |
| Orphan plans | No plan directories without root `_overview.md` entry | WARN |

### Step 4: Produce Audit Summary

```
Full Audit: {date}
Plans checked: {count}
  PASS: {count}
  WARN: {count}
  FAIL: {count}

Failing plans: {list}
Cross-plan issues: {list or "none"}
```

---

## Common Issues Found

Most frequent validation failures and their fixes:

| Issue | Frequency | How to Fix |
|-------|-----------|------------|
| Missing `last_updated` in frontmatter | Very common | Add field with today's date in `YYYY-MM-DD` format |
| Children table Type column has `Doc` or `Feature` | Common | Replace with `Plan` (directory) or `Task` (file) |
| Status mismatch between root and plan `_overview.md` | Common | Sync root Plans table to match plan's actual status |
| Emoji in frontmatter `status` field | Common | Use bare enum only: `WIP` not `🔄 [WIP]` |
| Missing `## Purpose` section | Occasional | Add section with substantive content |
| `BLOCKED` without kebab-case reason | Occasional | Add reason: `BLOCKED:reason-here` |
| Phase 0 with `[RESEARCH]` tasks | Occasional | Defer to P1+ or resolve before planning |
| Documents exceeding line limits | Occasional | Move reference content to `assets/` subfolder |
| `depends_on` referencing deleted plan | Rare | Remove stale reference from frontmatter |
| Dependency cycle (A→B→A) | Rare | Break cycle — restructure dependency direction |
