---
name: orch-testing
description: "Orchestrator testing preset — coordinating comprehensive testing workflows across specialist agents. Manages the full test lifecycle: PLAN (HyperSan) → SPEC-TEST (HyperArch) → ATTACK (HyperRed) → FINAL (HyperSan). Includes adversarial testing, fix cycles, and housekeeping gates. Use this skill when orchestrating testing, validation, or QA workflows across the Hyper agent team."
---

# HyperOrch Testing Preset

## Goals
- Orchestrate comprehensive testing workflows
- Coordinate spec tests (HyperArch) and adversarial tests (HyperRed)
- Ensure quality through strategic housekeeping

## When This Applies
Trigger patterns: "test", "validate", "attack", "check", "verify", "QA"

## Testing Protocol

### Phase Structure
```
PLAN (HyperSan) → SPEC-TEST (HyperArch) → ATTACK (HyperRed) → FINAL (HyperSan)
      ↓                  ↓                      ↓                  ↓
   Review Plan      Run Spec Tests        Edge Case Attacks    Final Validation
```

### Phase Flow
```
Phase 1: PLAN
  → HyperSan reviews test plan
  → If issues: Revise plan
  → If approved: Continue

Phase 2: SPEC-TEST (Loop)
  → HyperArch runs spec tests
  → If failures: Fix and re-run (max 3 cycles)
  → If all pass: Continue

Phase 3: ATTACK
  → HyperRed attacks implementation
  → If BLOCKERs found: Return to Phase 2
  → If no BLOCKERs: Continue

Phase 4: FINAL
  → HyperSan final validation
  → Complete
```

## Orchestration Steps

### 1. Initialize Testing
- Parse testing scope from user request
- Identify target module/files
- State: "Starting testing workflow for: [target]"

### 2. Phase 1: PLAN
Invoke HyperSan:
```yaml
task: "Review test plan for: [target module]"
context: "User wants comprehensive testing. Identify test cases, priorities, risks."
success_criteria: "Approve test plan or identify gaps"
output_format: "summary"
```

**Evaluate Response:**
- If approved → Continue to Phase 2
- If gaps found → Report to user, request clarification

### 3. Phase 2: SPEC-TEST (Loop)
**Cycle Counter:** Start at 1, max 3

Invoke HyperArch:
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
  <testing_standards>
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
  </testing_standards>
```

**Evaluate Response:**
- If all tests pass → Continue to Phase 3
- If failures remain:
  - Increment cycle counter
  - If cycles < 3: Re-invoke HyperArch with failure details
  - If cycles >= 3: Report persistent failures, suggest manual intervention

**Housekeeping Trigger:**
After every 3 cycles, invoke HyperIQGuard:
```yaml
task: "Review recent test fixes for code quality"
context: "[List of files modified during testing]"
agent: HyperIQGuard
```

### 4. Phase 3: ATTACK
Invoke HyperRed:
```yaml
task: "Attack this module for edge cases: [target]"
context: "Spec tests passed. Find what they missed."
success_criteria: "Report findings by severity (BLOCKER/WARNING/INFO)"
output_format: "summary"
```

**Evaluate Response:**
- If no BLOCKERs → Continue to Phase 4
- If BLOCKERs found:
  - Return to Phase 2 with BLOCKER details
  - HyperArch fixes, then re-invoke HyperRed (max 2 attack cycles)

### 5. Phase 4: FINAL
Invoke HyperSan:
```yaml
task: "Final validation of tested implementation"
context: "Spec tests pass. HyperRed findings addressed. Summary: [attack summary]"
success_criteria: "Confirm implementation is production-ready"
output_format: "summary"
```

**Evaluate Response:**
- If approved → Finalize
- If issues → Report, suggest remediation

### 6. Finalization
Compile comprehensive summary:
- Test plan overview
- Spec test results
- HyperRed findings and resolutions
- Final validation status

## Output Format

### Success
```markdown
## Testing Complete ✅

**Target:** [module/files]
**Phases Completed:** 4/4

### Summary
| Phase | Agent | Status |
|-------|-------|--------|
| PLAN | HyperSan | ✅ Approved |
| SPEC-TEST | HyperArch | ✅ All pass (N cycles) |
| ATTACK | HyperRed | ✅ No blockers |
| FINAL | HyperSan | ✅ Approved |

### HyperRed Findings
- **BLOCKER**: 0 (all resolved)
- **WARNING**: [N] (addressed/deferred)
- **INFO**: [N] (documented)

### Confidence
Ready for production: HIGH
```

### Partial
```markdown
## Testing Incomplete ⚠️

**Target:** [module/files]
**Status:** PARTIAL
**Stopped At:** [phase]

### Issues
[Description of blocking issues]

### Addressed
- [Issue 1]: Fixed
- [Issue 2]: Fixed

### Outstanding
- [Issue 3]: Requires [action]

### Recommendation
[Suggested next steps]
```

## Critical Rules
- **All Phases Mandatory**: Do not skip any phase
- **Max 3 Spec-Test Cycles**: Halt if tests won't pass after 3 cycles
- **Max 2 Attack Cycles**: Halt if HyperRed keeps finding BLOCKERs
- **Housekeeping Every 3 Cycles**: Invoke HyperIQGuard to prevent code rot
- **Severity Hierarchy**: BLOCKER must be fixed, WARNING should be fixed, INFO is optional
- **HyperRed Independence**: HyperRed generates its own attacks (does not use spec tests)
