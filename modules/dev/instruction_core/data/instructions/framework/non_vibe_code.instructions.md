---
applyTo: "modules/**/*.py,project/**/*.py,*.py"
---

# Non-Vibe Code Practice

## Goals
- Prevent AI agents from writing "runnable but wrong" code — code that technically works but is architecturally incorrect.
- Enforce engineering discipline: write CAREFUL code, not AFRAID code.
- Embed correctness-over-completion as a structural gate in implementation workflows.

## The Problem

AI agents frequently produce code that technically runs but is silently wrong:
- **Duplicating** instead of refactoring existing code to serve both cases.
- **Wrapping in defensive fallbacks** instead of understanding the actual behavior.
- **Guessing intent** instead of asking when uncertain.

The result: code that passes tests but accumulates technical debt, confuses future readers, and silently diverges from intended architecture.

## The Three Pillars

### 1. Unify Before Duplicating

Refactor existing code to serve both old and new cases. Silent duplication is a defect.

**"Unify or Justify" Gate**: Before adding any overlapping function, you MUST:
- Refactor the original to serve both cases, OR
- Add `# JUSTIFY: [reason]` explaining why unification is unsafe.
- No third option. Unexplained duplication is a defect.

```
✅ CORRECT:  Found existing parse_config(). Extended it to handle both formats.
✅ CORRECT:  Cannot unify — old callers depend on return type. # JUSTIFY: [reason]
❌ DEFECT:   Added parse_config_v2() alongside parse_config() without checking callers.
```

### 2. No Dead Fallbacks

No `try(new)/except(old)` without annotation. No bare `except` that silently swallows. No unused parameters added "just in case."

Any fallback that MUST exist carries an annotation:
```
# FALLBACK: [reason] expires when [condition]
```
Remove the moment the new path is proven.

```
✅ CORRECT:  new_parser(data)  # No fallback — old parser deleted
✅ CORRECT:  try: new_parser(data)
             except FormatError:
                 old_parser(data)  # FALLBACK: legacy files exist, expires when migration completes
❌ DEFECT:   try: new_parser(data)
             except: old_parser(data)  # No reason, no expiry, bare except
```

For permanent fallbacks (graceful degradation by design), use:
```
# FALLBACK: [reason] permanent — [justification]
```

### 3. Ask, Don't Guess

When uncertain about intent or impact, emit an `[UNSURE]` marker and escalate to human rather than writing speculatively runnable code.

```
✅ CORRECT:  # [UNSURE] Should this also handle nested configs? Escalating.
✅ CORRECT:  # TODO(verify): Assuming UTF-8 — confirm with user if other encodings needed
❌ DEFECT:   def parse(data, encoding="utf-8", nested=True, strict=False):  # Just in case
```

Use `# TODO(verify):` for low-risk assumptions. Use `[UNSURE]` for blocking questions.

#### Contextual Questions

Agents' thinking tokens are not visible to users. Every question must be self-contained with full context: what you were trying to do, why you need the answer, what options you're considering, and relevant background.

Without context, the user sees: "Should I use option A or B?" — but doesn't know what A and B are for, what you've already tried, or why it matters.

```
✅ CORRECT:  "Task 3/7 needs config key `api_timeout`. I'm implementing rate limiting in the API module. Should this be 30s (default) or 60s (for slow networks)?"
❌ DEFECT:   "Should this be 30s or 60s?"
```

## Batched Escalation

Collect ALL `[UNSURE]` items and questions during the current work phase. Present as a single numbered list at the end — NOT one question per round-trip.

**Rationale**: Each agent request costs tokens/money. One batched question with 5 items is far cheaper than 5 separate round-trips.

```
✅ CORRECT:  Finish phase, then: "3 items need your input: 1) ... 2) ... 3) ..."
❌ DEFECT:   Stop after each uncertainty to ask a single question
```

### Skip-and-Continue on Blockers

When executing a batch of tasks and one task is blocked (needs user clarification, missing dependency, external decision), do NOT stop immediately. Instead:

1. **Skip** the blocked task.
2. **Execute** all remaining non-blocking tasks first.
3. **Batch** all blockers into a single numbered list presented AFTER completing everything that CAN be done.

The user unblocks everything at once and the next pass picks up the remaining work.

```
✅ CORRECT:  Task 3/7 blocked (missing config key). Skipped. Completed tasks 1,2,4,5,6,7.
             "1 blocker: Task 3 needs config key X — what value?"
❌ DEFECT:   Task 3/7 blocked. Stopped everything to ask about config key X.
             (Tasks 4–7 could have been done in this same request.)
```

## The Litmus Test

> **If you cannot explain WHY you did not modify the original, you were afraid, not careful.**

| Behavior | Careful (✅) | Afraid (❌) |
|----------|-------------|------------|
| Before editing old code | Checked callers/usages, confirmed impact | Added redundant code without checking |
| When uncertain | Noted uncertainty with `# TODO(verify):`, then proceeded | Wrapped in fallback without understanding |
| When feature overlaps | Refactored original to serve both cases | Duplicated to avoid touching old code |
| When old code is wrong | Fixed it, documented why | Left it, added workaround alongside |
| When asked to extend | Extended in place | Created `_v2` variant next to original |
