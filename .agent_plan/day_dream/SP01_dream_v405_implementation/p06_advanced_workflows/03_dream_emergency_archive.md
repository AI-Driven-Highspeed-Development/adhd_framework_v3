---
name: dream_emergency_archive_commands
magnitude: Standard
status: TODO
---

# Implement `dream emergency` + `dream archive`

## Intent

Implement the two mutating P1 commands: `dream emergency` (automate emergency declaration with frontmatter updates) and `dream archive` (move completed plans to `_completed/YYYY-QN/`). Grouped because both are the only P1 commands that write to files.

## Acceptance Criteria

### `dream emergency`

- [ ] `dream_emergency(plan_id: str, blocks: list[str] | None)` updates frontmatter
- [ ] Sets `priority: emergency` and `emergency_declared_at:` (ISO 8601) in target plan
- [ ] If `--blocks` provided: updates `blocks:` in emergency plan, adds `depends_on:` in affected plans
- [ ] Runs `dream validate` after mutations to verify DAG consistency
- [ ] Outputs confirmation with `dream status` summary

### `dream archive`

- [ ] `dream_archive(plan_id: str)` moves completed plan to archive
- [ ] Validates plan status is ✅ DONE or 🚫 CUT before moving
- [ ] Determines quarter from `last_updated` or current date
- [ ] Creates `_completed/YYYY-QN/` directory if needed
- [ ] Moves plan directory to archive location
- [ ] Updates `_state_deltas_archive.md` if State Delta cap (20) exceeded

## Constraints

- `[EXPERIMENTAL]` — mutating commands need careful testing against real plan trees
- Both commands modify filesystem — must handle errors gracefully (partial writes)
- `dream emergency` writes to multiple files atomically (or reports partial failure)
