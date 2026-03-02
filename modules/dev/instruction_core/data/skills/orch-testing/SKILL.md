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
Invoke HyperSan to review test plan.
→ See [testing-delegation-blocks.md](assets/testing-delegation-blocks.md) for PLAN delegation YAML

**Evaluate Response:**
- If approved → Continue to Phase 2
- If gaps found → Report to user, request clarification

### 3. Phase 2: SPEC-TEST (Loop)
**Cycle Counter:** Start at 1, max 3

Invoke HyperArch with testing standards.
→ See [testing-delegation-blocks.md](assets/testing-delegation-blocks.md) for SPEC-TEST delegation YAML

Testing standards embedded in `execution_guidance`:
→ See [testing-standards.md](assets/testing-standards.md)

**Evaluate Response:**
- If all tests pass → Continue to Phase 3
- If failures remain:
  - Increment cycle counter
  - If cycles < 3: Re-invoke HyperArch with failure details
  - If cycles >= 3: Report persistent failures, suggest manual intervention

**Housekeeping Trigger:**
After every 3 cycles, invoke HyperIQGuard for code quality review.

### 4. Phase 3: ATTACK
Invoke HyperRed for edge case attacks.
→ See [testing-delegation-blocks.md](assets/testing-delegation-blocks.md) for ATTACK delegation YAML

**Evaluate Response:**
- If no BLOCKERs → Continue to Phase 4
- If BLOCKERs found:
  - Return to Phase 2 with BLOCKER details
  - HyperArch fixes, then re-invoke HyperRed (max 2 attack cycles)

### 5. Phase 4: FINAL
Invoke HyperSan for final validation.
→ See [testing-delegation-blocks.md](assets/testing-delegation-blocks.md) for FINAL delegation YAML

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
Template for successful test completion reports:
→ See [testing-success-template.md](assets/testing-success-template.md)

### Partial
Template for incomplete testing reports:
→ See [testing-partial-template.md](assets/testing-partial-template.md)

## Critical Rules
- **All Phases Mandatory**: Do not skip any phase
- **Max 3 Spec-Test Cycles**: Halt if tests won't pass after 3 cycles
- **Max 2 Attack Cycles**: Halt if HyperRed keeps finding BLOCKERs
- **Housekeeping Every 3 Cycles**: Invoke HyperIQGuard to prevent code rot
- **Severity Hierarchy**: BLOCKER must be fixed, WARNING should be fixed, INFO is optional
- **HyperRed Independence**: HyperRed generates its own attacks (does not use spec tests)
