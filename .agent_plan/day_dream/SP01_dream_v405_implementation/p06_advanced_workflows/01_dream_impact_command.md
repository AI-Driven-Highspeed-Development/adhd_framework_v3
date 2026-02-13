---
name: dream_impact_command
magnitude: Standard
status: TODO
---

# Implement `dream impact`

## Intent

Implement the `dream impact` MCP tool that performs a DAG walk showing all plans affected by changes to a given plan. Reports direct dependents, transitive dependents, and affected modules.

## Acceptance Criteria

- [ ] `dream_impact(plan_id: str, modules: bool)` returns impact analysis
- [ ] Direct dependents listed from `blocks:` relationships
- [ ] Transitive dependents computed via recursive DAG walk
- [ ] `--modules` flag includes affected modules from State Delta + Module Index
- [ ] Warns about potential invalidations for completed plans in the dependency chain
- [ ] Output format matches §13.3 box-drawing example
- [ ] Handles unknown `plan_id` with clear error message

## Constraints

- `[KNOWN]` — DAG traversal reuses graph built by `dream validate`
- Read-only: no file mutations
- Uses shared parsing + DAG infrastructure from p04/p05

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| p05 validate DAG | Pending | Reuses DAG construction from validate |
