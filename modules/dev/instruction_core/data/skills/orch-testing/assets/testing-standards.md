# Testing Standards

Embedded in the `execution_guidance` field of HyperArch delegation during Phase 2: SPEC-TEST.

## Test Execution
- Say: "Starting spec test cycle #[N]" to track progress
- Capture output, errors, and unexpected behavior
- Document each result clearly
- Apply fixes one at a time, keep changes minimal

## Testing Folder Guidelines
| Artifact | Location |
|----------|----------|
| Scratch test scripts | `.temp_agent_work/` (clean up after) |
| HyperRed attacks | `.agent_plan/red_team/<module>/` |
| Formal unit tests | `<module>/tests/` |
| Integration tests | `tests/integration/` |

## Before Creating Test Files
1. Check existing tests: `<module>/tests/` and `tests/integration/`
2. Check HyperRed findings: `.agent_plan/red_team/<module>/findings/`
3. Reuse before creating—do NOT duplicate test coverage

## Bug Fixing Rules
- One bug at a time: Fix, verify, then move to next
- Minimal fixes only: Do NOT refactor unrelated code
- Document what was changed and why
