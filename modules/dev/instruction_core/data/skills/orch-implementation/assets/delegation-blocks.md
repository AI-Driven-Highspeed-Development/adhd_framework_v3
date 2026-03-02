# Implementation Delegation Blocks

All delegation YAML blocks used by HyperOrch during the implementation workflow.

## Phase 1: PRE-CHECK (HyperSan)

```yaml
task: "Pre-implementation sanity check for: [feature description]"
context: "User wants to implement: [full request]. Target: [module/files if known]"
success_criteria: "Validate feasibility, check for conflicts, identify risks"
output_format: "summary"
```

## Phase 2: IMPLEMENT (HyperArch)

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
  → See implementation-standards.md for full standards block
```

## Phase 3: POST-CHECK (HyperSan)

```yaml
task: "Post-implementation validation"
context: "Implementation complete. Changes: [HyperArch summary]"
success_criteria: "Validate implementation quality, correctness, and Non-Vibe Code compliance"
output_format: "summary"
```

### Non-Vibe Code Validation Checklist (HyperSan)
- [ ] No unexplained duplication — every new function checked against existing codebase
- [ ] No bare `except` or `try(new)/except(old)` without `# FALLBACK:` annotation
- [ ] All `# JUSTIFY:` annotations have concrete reasons (not "just in case")
- [ ] `[UNSURE]` markers surfaced for blocking questions — no speculative code
- [ ] No unused parameters added defensively
- [ ] Fallbacks with `expires when` have actionable conditions

## Phase 4: DOC-UPDATE (HyperDream) — Conditional

**Trigger:** Source request references `**/day_dream/**/80_implementation.md`

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
