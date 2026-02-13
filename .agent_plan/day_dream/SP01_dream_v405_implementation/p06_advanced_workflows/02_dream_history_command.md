---
name: dream_history_command
magnitude: Trivial
status: TODO
---

# Implement `dream history`

## Intent

Implement the `dream history` MCP tool that generates module-indexed change history from State Delta entries. Shows chronological changes for a specific module.

## Acceptance Criteria

- [ ] `dream_history(module: str)` returns chronological change table
- [ ] Reads State Deltas from root `_overview.md` and `_state_deltas_archive.md`
- [ ] Filters entries mentioning the target module
- [ ] Output sorted newest-first with plan name, date, and change description
- [ ] Returns clear message when module has no history
- [ ] Handles missing `_state_deltas_archive.md` gracefully (not an error)

## Constraints

- `[KNOWN]` — text parsing + filtering
- Read-only: no file mutations
- Simpler than other P1 commands — State Delta format is well-defined in §4
