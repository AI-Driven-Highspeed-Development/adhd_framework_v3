# Testing Delegation Blocks

All delegation YAML blocks used by HyperOrch during the testing workflow.

## Phase 1: PLAN (HyperSan)

```yaml
task: "Review test plan for: [target module]"
context: "User wants comprehensive testing. Identify test cases, priorities, risks."
success_criteria: "Approve test plan or identify gaps"
output_format: "summary"
```

## Phase 2: SPEC-TEST (HyperArch) — Loop

**Cycle Counter:** Start at 1, max 3

```yaml
task: "Execute spec tests for: [target]"
objective: "[The larger goal this testing serves]"
context: "Test plan approved. Cycle #[N]. [Prior cycle summary if any]"
autonomy_guidance: |
  Your goal is OBJECTIVE COMPLETION, not just running tests.
  If testing reveals related issues in your domain, fix them.
  Report all actions taken, including any discovered work.
success_criteria: "Run tests, fix failures, report results"
output_format: "summary"
execution_guidance: |
  → See testing-standards.md for full standards block
```

### Housekeeping Trigger (every 3 cycles)

```yaml
task: "Review recent test fixes for code quality"
context: "[List of files modified during testing]"
agent: HyperIQGuard
```

## Phase 3: ATTACK (HyperRed)

```yaml
task: "Attack this module for edge cases: [target]"
context: "Spec tests passed. Find what they missed."
success_criteria: "Report findings by severity (BLOCKER/WARNING/INFO)"
output_format: "summary"
```

## Phase 4: FINAL (HyperSan)

```yaml
task: "Final validation of tested implementation"
context: "Spec tests pass. HyperRed findings addressed. Summary: [attack summary]"
success_criteria: "Confirm implementation is production-ready"
output_format: "summary"
```
