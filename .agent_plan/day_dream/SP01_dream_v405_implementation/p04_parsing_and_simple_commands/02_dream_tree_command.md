---
name: dream_tree_command
magnitude: Light
status: TODO
---

# Implement `dream tree`

## Intent

Implement the `dream tree` MCP tool that generates `_tree.md` — an annotated folder tree of the day-dream directory with status markers inline. Replace the `NotImplementedError` stub from p03.

## Acceptance Criteria

- [ ] `dream_tree(active_only: bool)` generates annotated directory tree
- [ ] Output written to `.agent_plan/day_dream/_tree.md` with header `<!-- GENERATED — run 'dream tree' to refresh -->`
- [ ] Each plan/task annotated with status marker from frontmatter
- [ ] `--active-only` flag excludes `_completed/` and `_templates/`
- [ ] Generation timestamp included in output
- [ ] Handles missing/malformed `_overview.md` gracefully (warns, doesn't crash)

## Constraints

- `[KNOWN]` — directory walking + string formatting
- Uses shared `tree_scanner` and `output_formatter` from task 01
- Mutating: writes `_tree.md` (only mutation in P0 besides validate)

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| 01_shared_parsing_infrastructure | Pending | Needs tree scanner |
