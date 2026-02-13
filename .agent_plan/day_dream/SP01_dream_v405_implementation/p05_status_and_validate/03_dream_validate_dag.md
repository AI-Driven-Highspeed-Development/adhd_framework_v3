---
name: dream_validate_dag
magnitude: Light
status: TODO
---

# Implement `dream validate` — DAG Checks

## Intent

Extend `dream validate` with dependency graph analysis: cycle detection in `depends_on`/`blocks` relationships and bidirectional consistency warnings. This layers on top of the core checks from task 02.

## Acceptance Criteria

- [ ] Build dependency graph from all plans' `depends_on` and `blocks` fields
- [ ] Cycle detection: ERROR when `depends_on`/`blocks` form a cycle (report cycle path)
- [ ] Bidirectional consistency: WARNING when A `depends_on: B` but B lacks `blocks: A`
- [ ] Cross-plan modification check: WARNING when plans modify same module without `depends_on`/`blocks`
- [ ] `modified_by_plans` drift: WARNING when module spec doesn't match State Delta references
- [ ] Unwritten invalidation: WARNING when module changes may compromise completed plans

## Constraints

- `[KNOWN]` — standard graph algorithms (DFS cycle detection)
- Extends validate output from task 02 — same violation list, same ERROR/WARNING taxonomy
- Read-only: no file mutations

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| 02_dream_validate_core | Pending | Must integrate with core check pipeline |
