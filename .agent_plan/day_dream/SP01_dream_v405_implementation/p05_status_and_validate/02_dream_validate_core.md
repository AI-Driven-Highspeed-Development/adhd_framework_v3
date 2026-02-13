---
name: dream_validate_core
magnitude: Standard
status: TODO
---

# Implement `dream validate` — Core Checks

## Intent

Implement the core validation checks for `dream validate`: frontmatter schema validation, Module Index gate (table row + spec file), State Delta gate, and field presence checks. This is the largest single task in P0.

## Acceptance Criteria

- [ ] `dream_validate(plan: str | None)` returns categorized violations (ERROR/WARNING)
- [ ] Frontmatter schema check: required fields present, correct types, no unknown fields
- [ ] Module Index gate: new modules have both table row AND spec file on disk
- [ ] State Delta gate: closing plans have State Delta entry
- [ ] `last_updated` presence check on all plan and module specs
- [ ] `emergency_declared_at` required when `priority: emergency`
- [ ] `invalidation_scope` required when `invalidated_by` is set
- [ ] `--plan` flag scopes validation to single plan (optional)
- [ ] Clear ERROR vs WARNING categorization per §13.2 table

## Constraints

- `[KNOWN]` — schema validation, file existence checks
- Uses shared parsing infrastructure from p04
- Read-only: no file mutations
- Must be composable — DAG checks (task 03) extend this
