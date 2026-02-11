# Feature: Non-Vibe Code Practice

> Part of [DREAM Upgrade](./_overview.md) · ✅ [DONE] · Priority: P1

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌─────────────────────────────────────────────────────────────────┐
│  AI agent implements a feature  ──────►  💥 "WORKS" BUT WRONG   │
│                                                                 │
│  Because: Agent is AFRAID to touch old code                     │
│           → duplicates instead of refactoring                   │
│           → wraps in try/except instead of understanding        │
│           → guesses intent instead of asking                    │
│                                                                 │
│  Result: Code that runs but is silently incorrect               │
└─────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Human reviewers | 🔥🔥🔥 High | Every AI-assisted PR |
| Future agents reading the code | 🔥🔥🔥 High | Compounds over time |
| Project correctness | 🔥🔥 Medium | Silent — only caught in review |

### ✨ The Vision

```
After This Feature:
┌─────────────────────────────────────────────────────────────────┐
│  AI agent implements a feature  ──────►  ✅ CORRECT & CLEAN     │
│                                                                 │
│  Three Pillars:                                                 │
│    1. Unify Before Duplicating                                  │
│    2. No Dead Fallbacks                                         │
│    3. Ask, Don't Guess                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> An enforceable engineering discipline with three pillars that prevents AI agents from writing "runnable but wrong" code — embedded as structural gates in the implementation workflow.

---

## 🔧 The Spec

**Priority:** P1 · **Difficulty:** `[KNOWN]`

**In Scope:**
- Non-Vibe Code section in `orch-implementation` skill (Arch standards + San POST-CHECK)
- Universal directive in `agent_common_rules.instructions.md`
- Cross-reference from `day-dream` Clean-Code-First section
- Dedicated `non_vibe_code.instructions.md`
- Agent flow references in HyperArch, HyperSan, HyperIQGuard

**Out of Scope:**
- Automated tooling to detect violations (future feature)
- Rewriting existing code with afraid-patterns
- Runtime enforcement or linting

---

## ✅ Acceptance Criteria

- [x] `orch-implementation` SKILL.md contains Non-Vibe Code section with all 3 pillars
- [x] `orch-implementation` SKILL.md contains Non-Vibe Code POST-CHECK checklist
- [x] `agent_common_rules.instructions.md` contains universal directive
- [x] `day-dream` SKILL.md cross-references `orch-implementation` for full practice
- [x] Git checkpoint convention documented
- [x] `non_vibe_code.instructions.md` created with full practice spec
- [x] Agent flows reference Non-Vibe Code in `@critical_rules`

---

## [Custom] 🏛️ The Three Pillars

### Pillar 1: Unify Before Duplicating

Refactor existing code to serve both old and new case. If unsafe, document **WHY** with `# JUSTIFY:` annotation.

**"Unify or Justify" Gate:** Before adding any overlapping function, agent MUST refactor the original OR justify why not.

### Pillar 2: No Dead Fallbacks

No `try(new)/except(old)`. Any necessary fallback carries:
```
# FALLBACK: [reason] expires when [condition]
```

### Pillar 3: Ask, Don't Guess

When uncertain, emit `[UNSURE]` marker and batch escalation at end of phase. No speculative code.

## [Custom] ⚖️ Careful vs Afraid

| Behavior | Careful (✅) | Afraid (❌) |
|----------|-------------|------------|
| Before editing old code | Checked callers/usages | Added redundant code |
| When uncertain | `# TODO(verify):`, then proceeded | Wrapped in fallback |
| When feature overlaps | Refactored original | Duplicated to avoid touching old code |
| When old code is wrong | Fixed it, documented why | Left it, added workaround |

## [Custom] ⚡ Git Checkpoint Convention

When planning phases with large refactors, agents MUST note `⚡ GIT CHECKPOINT` before that phase.

---

**← Back to:** [DREAM Upgrade Overview](./_overview.md)
