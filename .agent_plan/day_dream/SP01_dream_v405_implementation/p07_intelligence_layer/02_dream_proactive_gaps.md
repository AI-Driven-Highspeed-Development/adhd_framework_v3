---
name: dream_proactive_gaps
magnitude: Light
status: TODO
---

# Implement `dream gaps --proactive`

## Intent

Implement the `dream gaps --proactive` MCP tool for proactive bus-factor detection — flag modules with single-person dependencies via a `sole_expert:` field in module spec frontmatter.

## Acceptance Criteria

- [ ] `dream_gaps(proactive: bool)` returns bus-factor risk analysis
- [ ] Reads `sole_expert:` field from module spec frontmatter (P2 schema addition)
- [ ] Flags modules where `sole_expert:` has only one person
- [ ] Aggregates with existing `knowledge_gaps:` for combined risk view
- [ ] Output clearly distinguishes reactive gaps (existing) from proactive detection (new)

## Constraints

- `[RESEARCH]` — current `knowledge_gaps` model is reactive-only per §13.4
- Requires `sole_expert:` field in module spec frontmatter (schema extension)
- Read-only: no file mutations
- Design exploration — may change shape after validation

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| p06 P1 commands | Pending | Needs mature parsing + validation infrastructure |
