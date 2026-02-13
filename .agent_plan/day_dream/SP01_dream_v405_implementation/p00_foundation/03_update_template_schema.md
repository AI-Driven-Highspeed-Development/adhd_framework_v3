---
task: p00_03
title: Update Template Frontmatter & Notation
status: DONE
difficulty: "[KNOWN]"
---

# Update Template Frontmatter & Notation

## Scope

Update existing template files to match v4.05 schema changes. Covers items #10-12, #14-15 from §14.2.

## Specific Changes

| # | File | Change | §14.2 Item |
|---|------|--------|-----------|
| 1 | `_templates/blueprint/overview.template.md` | Add full frontmatter schema: `type`, `origin`, `start_at`, `last_updated`, `depends_on`, `blocks`, `knowledge_gaps`, `priority`, `emergency_declared_at`, invalidation fields | #10 |
| 2 | `_templates/blueprint/overview.template.md` | Add `## Current Sprint`, `## Module Index` (with Spec File + Knowledge Gaps columns), `## State Deltas` sections for root overview variant. Add Priority + Depends On columns to Plans table | #11 |
| 3 | `_templates/blueprint/modules/module_spec.template.md` | Add `last_updated`, `modified_by_plans`, `knowledge_gaps` to frontmatter scaffold | #12 |
| 4 | `_templates/blueprint/80_implementation.template.md` | Update slot notation from old scale to 8-slot scale (Trivial/Light/Standard/Heavy/Epic) | #14 |
| 5 | `_templates/simple.template.md` | Add `origin:` to frontmatter | #15 |

## How to Verify (Manual)

1. Open `overview.template.md` — frontmatter should list all v4.05 fields from §2.1
2. Open `module_spec.template.md` — frontmatter should have `modified_by_plans` array
3. Open `80_implementation.template.md` — slot scale should show 8-slot system

## Acceptance Criteria

- [x] `overview.template.md` frontmatter matches §2.1 schema (all REQUIRED + RECOMMENDED fields as placeholders)
- [x] `overview.template.md` includes root-variant sections (Current Sprint, Module Index, State Deltas)
- [x] `module_spec.template.md` frontmatter includes `last_updated`, `modified_by_plans`, `knowledge_gaps`
- [x] `80_implementation.template.md` uses `■□□□□□□□` (8-slot) notation
- [x] `simple.template.md` frontmatter includes `origin:`
