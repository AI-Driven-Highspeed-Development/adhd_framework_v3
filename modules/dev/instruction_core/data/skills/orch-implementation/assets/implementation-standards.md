# Implementation Standards

Embedded in the `execution_guidance` field of HyperArch delegation during Phase 2: IMPLEMENT.

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

## Non-Vibe Code Practice
Engineering discipline: write CAREFUL code, not AFRAID code.

### Three Pillars
1. **Unify Before Duplicating** — Refactor existing code to serve both old and new cases. Silent duplication = defect.
2. **No Dead Fallbacks** — No `try(new)/except(old)` without annotation. Any required fallback carries: `# FALLBACK: [reason] expires when [condition]`
3. **Ask, Don't Guess** — When uncertain, emit `[UNSURE]` marker and batch all questions for end-of-phase escalation. NEVER write speculative code.

### "Unify or Justify" Gate
Before adding any overlapping function, you MUST:
- Refactor the original to serve both cases, OR
- Add `# JUSTIFY: [reason]` explaining why unification is unsafe
- No third option. Unexplained duplication is a defect.

### Batched Escalation
Collect ALL `[UNSURE]` items during the current phase. Present as a single numbered list at the end — NOT one question per round-trip.

### Careful vs Afraid Litmus Test
If you cannot explain WHY you did not modify the original, you were afraid, not careful.
