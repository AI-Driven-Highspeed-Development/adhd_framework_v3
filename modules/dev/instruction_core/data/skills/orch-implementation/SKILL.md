---
name: orch-implementation
description: "Orchestrator implementation preset — coordinating implementation tasks across specialist agents with mandatory quality gates. Manages the full lifecycle: PRE-CHECK (HyperSan) → IMPLEMENT (HyperArch) → POST-CHECK (HyperSan) → DOC-UPDATE (HyperDream). Includes coding standards, anti-hallucination checks, and verification. Use this skill when orchestrating code implementation across the Hyper agent team."
---

# HyperOrch Implementation Preset

## Goals
- Orchestrate implementation workflows with mandatory quality gates
- Ensure pre and post sanity checks via HyperSan
- Maintain context efficiency through delegation

## When This Applies
Trigger patterns: "implement", "build", "create", "fix", "add feature", "modify"

## Implementation Protocol

### Phase Structure
```
PRE-CHECK (HyperSan) → IMPLEMENT (HyperArch) → POST-CHECK (HyperSan) → [DOC-UPDATE (HyperDream)]
    ↓                        ↓                       ↓                        ↓
  Validate              Build Feature           Validate Result        Update Blueprint
  Feasibility                                                          (Conditional)
```

### Phase Flow
```
Phase 1: PRE-CHECK
  → HyperSan validates feasibility
  → If FAILED: Report blockers, HALT
  → If PASSED: Continue

Phase 2: IMPLEMENT
  → HyperArch implements feature
  → If FAILED: Report issues, suggest fixes
  → If PASSED: Continue

Phase 3: POST-CHECK
  → HyperSan validates implementation
  → If FAILED: Return to Phase 2 (max 2 retries)
  → If PASSED: Continue

Phase 4: DOC-UPDATE (Conditional)
  → Trigger: Source is blueprint implementation doc (**/day_dream/**/80_implementation.md)
  → HyperDream updates the implementation doc
  → Mark completed tasks, update status
  → If NOT triggered: Skip to Finalize
```

## Orchestration Steps

### 1. Initialize Implementation
- Parse feature description from user request
- Identify target module/files if specified
- State: "Starting implementation workflow for: [feature]"

### 2. Phase 1: PRE-CHECK
Invoke HyperSan:
```yaml
task: "Pre-implementation sanity check for: [feature description]"
context: "User wants to implement: [full request]. Target: [module/files if known]"
success_criteria: "Validate feasibility, check for conflicts, identify risks"
output_format: "summary"
```

**Evaluate Response:**
- If `passed: true` or no blockers → Continue to Phase 2
- If `passed: false` or blockers found → Report to user, HALT workflow

### 3. Phase 2: IMPLEMENT
Invoke HyperArch:
```yaml
task: "Implement: [feature description]"
objective: "[The larger goal this implementation serves]"
context: "Pre-check passed. Notes: [HyperSan summary]"
autonomy_guidance: |
  Your goal is OBJECTIVE COMPLETION, not just task execution.
  If completing the objective requires additional work in your domain, do it.
  Report all actions taken, including any discovered work.
success_criteria: "Complete implementation following ADHD patterns"
output_format: "summary"
execution_guidance: |
  <implementation_standards>
  ## Pre-Coding Verification
  - Search codebase for existing solutions—do NOT reinvent
  - Read source files to confirm API signatures—do NOT guess
  - Check `utils/` and `managers/` for existing utilities
  
  ## Coding Standards
  - **Structure**: OOP, Type Hints always, docstrings minimal (module/class level)
  - **File Size**: ~400 lines target, 600 max. Refactor if exceeded
  - **Imports**: Absolute imports only. NEVER invent imports—search first
  - **Module Design**: No side-effects on import. Declare ADHD deps in `pyproject.toml`
  
  ## Patterns
  - Use `ADHDError` for application errors
  - Use `Logger` from `logger_util`—NEVER use `print()` in MCPs
  - Use `ConfigManager` for paths—NEVER hardcode
  - Use `.temp_agent_work/` for scratch files (clean up after)
  
  ## Anti-Hallucination Checklist
  Before writing code, confirm:
  1. ✓ Searched codebase for existing solutions
  2. ✓ Read source files to verify API signatures
  3. ✓ Checked `utils/` and `managers/` for utilities
  4. ✓ Verified import paths exist
  
  ## Quality Checklist (Before Completion)
  - [ ] No circular imports
  - [ ] Type hints present and accurate
  - [ ] No hardcoded paths (use ConfigManager)
  - [ ] No `print()` statements in MCPs
  - [ ] Temp/debug code removed
  </implementation_standards>
```

**Evaluate Response:**
- If SUCCESS → Continue to Phase 3
- If FAILED → Report issues, suggest user intervention

### 4. Phase 3: POST-CHECK
Invoke HyperSan:
```yaml
task: "Post-implementation validation"
context: "Implementation complete. Changes: [HyperArch summary]"
success_criteria: "Validate implementation quality and correctness"
output_format: "summary"
```

**Evaluate Response:**
- If `passed: true` → Continue to Phase 4 (if applicable) or Finalize
- If `passed: false`:
  - Increment retry counter
  - If retries < 2: Return to Phase 2 with fix instructions
  - If retries >= 2: Report issues, suggest manual intervention

### 5. Phase 4: DOC-UPDATE (Conditional)
**Trigger Condition:** Source request references a blueprint implementation doc matching `**/day_dream/**/80_implementation.md`

If triggered, invoke HyperDream:
```yaml
task: "Update implementation doc to reflect completed work"
context: |
  Implementation completed successfully for: [feature description]
  Source doc: [path to 80_implementation.md]
  Changes made: [HyperArch summary]
success_criteria: |
  - Mark implemented tasks as complete (checkbox or status update)
  - Update any status/phase indicators
  - Add implementation notes if relevant
  - Preserve unimplemented items for future work
output_format: "summary"
```

**Skip Condition:** If the request does NOT reference a blueprint implementation doc, skip directly to Finalization.

### 6. Finalization
Compile summary:
- List all changes made
- Note any warnings from validation
- Suggest next steps (testing, documentation)

## Output Format

### Success
```markdown
## Implementation Complete ✅

**Feature:** [description]
**Phases Completed:** 3/3 (or 4/4 if DOC-UPDATE triggered)

### Summary
- **PRE-CHECK**: [HyperSan summary]
- **IMPLEMENT**: [HyperArch summary]
- **POST-CHECK**: [HyperSan summary]
- **DOC-UPDATE**: [HyperDream summary] *(if triggered)*

### Files Modified
- [file1]
- [file2]

### Next Steps
- Run tests: `pytest [module]/tests/`
- Consider HyperRed adversarial testing
```

### Partial/Failed
```markdown
## Implementation Incomplete ⚠️

**Feature:** [description]
**Status:** [PARTIAL/FAILED]
**Phase Failed:** [phase name]

### Issue
[Description of failure]

### Recommendation
[Suggested action]
```

## Optional Extensions

### Quality Gate (After POST-CHECK)
If significant changes or user requests quality review:
```yaml
task: "Review implementation for anti-patterns"
context: "[List of changed files]"
agent: HyperIQGuard
```

### Adversarial Testing (User-Requested)
If user explicitly asks for attack testing:
```yaml
task: "Attack this implementation for edge cases"
context: "[Module path, feature description]"
agent: HyperRed
```

## Critical Rules
- **PRE-CHECK is Mandatory**: Never skip to implementation
- **POST-CHECK is Mandatory**: Never skip validation
- **Max 2 Retries**: If POST-CHECK fails twice, halt and report
- **No Direct Implementation**: HyperOrch NEVER writes code
- **Preserve HyperArch Autonomy**: HyperArch handles internal delegation (can invoke HyperSan/HyperRed itself)
- **DOC-UPDATE is Conditional**: Only trigger when source references `**/day_dream/**/80_implementation.md`
