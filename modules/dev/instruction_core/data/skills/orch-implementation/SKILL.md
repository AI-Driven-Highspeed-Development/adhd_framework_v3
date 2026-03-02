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

### 2–5. Phase Delegations

All phase delegation YAML blocks (PRE-CHECK, IMPLEMENT, POST-CHECK, DOC-UPDATE) with evaluation criteria:
→ See [delegation-blocks.md](assets/delegation-blocks.md)

Implementation standards embedded in the IMPLEMENT phase `execution_guidance`:
→ See [implementation-standards.md](assets/implementation-standards.md)

**Evaluation Logic:**
- **PRE-CHECK**: If `passed: true` → Phase 2. If blockers → HALT.
- **IMPLEMENT**: If SUCCESS → Phase 3. If FAILED → report.
- **POST-CHECK**: If `passed: true` → Phase 4 or Finalize. If `passed: false` → retry (max 2).
- **DOC-UPDATE**: Conditional — only when source references `**/day_dream/**/80_implementation.md`.

### 6. Finalization
Compile summary:
- List all changes made
- Note any warnings from validation
- Suggest next steps (testing, documentation)

## Output Format

### Success
→ See [implementation-success-template.md](assets/implementation-success-template.md)

### Partial/Failed
→ See [implementation-failed-template.md](assets/implementation-failed-template.md)

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
- **Non-Vibe Code Enforced**: POST-CHECK MUST validate Non-Vibe Code compliance (see checklist in Phase 3)

## ⚡ Git Checkpoint Convention

When an implementation plan includes phases that touch many files (large refactors, cross-module renames, destructive changes), the planning agent MUST insert a `⚡ GIT CHECKPOINT` marker before that phase.

**When to checkpoint:**
- Before phases with new file creation across multiple modules
- Before destructive changes (renames, deletions, large refactors)
- Before any phase touching ≥5 files

**Format in implementation plans:**
```
## Phase N: [Description]
⚡ GIT CHECKPOINT — commit before this phase ([reason])
```

**Rule:** Human approval of the plan is implicit consent to checkpoint. No runtime asking needed. Commit for safety, then proceed boldly — do NOT skip the refactor out of fear.
