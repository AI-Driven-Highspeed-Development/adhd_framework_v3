# `_overview.md` Frontmatter Schema

Every plan directory has `_overview.md` with YAML frontmatter. **No separate metadata file** — all plan metadata lives in `_overview.md` frontmatter.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plan identifier (snake_case) |
| `type` | enum | `system` or `procedure` |
| `magnitude` | enum | `Trivial` / `Light` / `Standard` / `Heavy` / `Epic` |
| `status` | enum | `TODO` / `WIP` / `DONE` / `BLOCKED:reason` / `CUT` |
| `origin` | string | Path to exploration/doc that triggered this plan |
| `last_updated` | date | `YYYY-MM-DD` (human) or ISO 8601 (machine) |

## Recommended Fields

| Field | Type | Description |
|-------|------|-------------|
| `depends_on` | string[] | Plans this plan structurally requires |
| `blocks` | string[] | Plans that cannot proceed until this completes |
| `knowledge_gaps` | string[] | Missing expertise or unvalidated assumptions |

## Optional / Conditional Fields

| Field | Type | When |
|-------|------|------|
| `start_at` | date | When work began (omit for exploratory) |
| `priority` | enum | `emergency` only (omit for `normal`) |
| `emergency_declared_at` | datetime | REQUIRED when `priority: emergency` |
| `invalidated_by` | string | Plan that caused invalidation (victim plans only) |
| `invalidation_scope` | string | REQUIRED when `invalidated_by` is set |
| `invalidation_date` | date | REQUIRED when `invalidated_by` is set |
