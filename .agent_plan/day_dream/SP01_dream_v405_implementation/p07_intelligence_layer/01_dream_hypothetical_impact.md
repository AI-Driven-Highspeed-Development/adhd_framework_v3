---
name: dream_hypothetical_impact
magnitude: Light
status: TODO
---

# Implement `dream impact --hypothetical`

## Intent

Implement the `--hypothetical` flag for `dream impact` that analyzes the impact of a proposed change without requiring an existing plan. Takes a free-text description and optional module list.

## Acceptance Criteria

- [ ] `dream_impact(hypothetical: str, modules: list[str] | None)` returns hypothetical analysis
- [ ] Identifies plans that depend on or modify the specified modules
- [ ] Output clearly labeled as **hypothetical, not factual** (per §13.4 risk note)
- [ ] Graceful handling when no modules specified (best-effort from description)
- [ ] Integrates with existing `dream impact` output format

## Constraints

- `[EXPERIMENTAL]` — behavioral contract intentionally loose per §13.4
- Read-only: no file mutations
- Output MUST include disclaimer that analysis is hypothetical
- May need iteration after real-world usage reveals useful patterns

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| p06 dream impact | Pending | Extends existing impact command |
