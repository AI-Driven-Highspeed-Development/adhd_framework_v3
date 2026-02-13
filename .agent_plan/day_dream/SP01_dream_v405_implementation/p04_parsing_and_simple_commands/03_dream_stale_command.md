---
name: dream_stale_command
magnitude: Trivial
status: TODO
---

# Implement `dream stale`

## Intent

Implement the `dream stale` MCP tool that flags module specs where `last_updated` exceeds a staleness threshold. Replace the `NotImplementedError` stub from p03.

## Acceptance Criteria

- [ ] `dream_stale(weeks: int, module: str | None)` returns list of stale modules
- [ ] Default threshold: 4 weeks from current date
- [ ] Optional module name filter scopes to single module
- [ ] Output includes: module name, last update date, owning plan, days stale
- [ ] Returns empty list (not error) when no modules are stale
- [ ] Handles missing `last_updated` field as always-stale (with warning)

## Constraints

- `[KNOWN]` — date comparison, frontmatter reads
- Uses shared `frontmatter_parser` from task 01
- Read-only: no file mutations
