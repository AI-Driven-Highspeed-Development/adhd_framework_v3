---
name: dream_status_command
magnitude: Light
status: TODO
---

# Implement `dream status`

## Intent

Implement the `dream status` MCP tool that displays the current sprint dashboard: emergency plans first, then active, then blocked, with aggregate warning counts. Replace the `NotImplementedError` stub from p03.

## Acceptance Criteria

- [ ] `dream_status(gaps: bool)` returns structured status report
- [ ] Emergency plans listed first, ordered by `emergency_declared_at`
- [ ] Active (WIP/TODO) and blocked plans displayed in separate sections
- [ ] Summary counts appended: knowledge gaps, stale modules, gate violations
- [ ] `--gaps` flag includes full knowledge gap details per plan
- [ ] Output format matches §13.2 box-drawing example
- [ ] Handles empty plan tree (no plans) gracefully

## Constraints

- `[KNOWN]` — aggregation + formatting over parsed frontmatter
- Uses shared `tree_scanner`, `frontmatter_parser`, `output_formatter` from p04
- Read-only: no file mutations
- Internally calls `dream stale` count and `dream validate` count for summary

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| p04 parsing infrastructure | Pending | Needs scanner + parser + formatter |
