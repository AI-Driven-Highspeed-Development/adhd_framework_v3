# 09 - Feature: Non-Vibe Code Practice

> Part of [DREAM Upgrade Blueprint](./00_index.md)

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
│  Flow: Check callers → Refactor or Justify → No dead code       │
│        → Ask when unsure → Human reviews INTENT not MESS        │
│                                                                 │
│  Three Pillars:                                                 │
│    1. Unify Before Duplicating                                  │
│    2. No Dead Fallbacks                                         │
│    3. Ask, Don't Guess                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> An enforceable engineering discipline with three pillars that prevents AI agents from writing "runnable but wrong" code — embedded as structural gates in the implementation workflow.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Code duplication | ❌ Silent overlapping functions accumulate | ✅ Unify or explicitly justify |
| Dead fallbacks | ❌ `try(new)/except(old)` never cleaned up | ✅ Annotated with expiry, removed when proven |
| Speculative code | ❌ Agent guesses intent, writes runnable garbage | ✅ Agent surfaces `[UNSURE]` marker, asks human |
| Review burden | ❌ Reviewer must catch subtle incorrectness | ✅ Structural gates catch it before review |

---

## 🔧 The Spec

---

## 🎯 Overview

The "Non-Vibe Code" practice codifies the difference between **careful** and **afraid** agent behavior into three enforceable pillars. AI agents frequently produce code that technically runs but is architecturally wrong — duplicating instead of refactoring, wrapping in defensive fallbacks instead of understanding, and guessing intent instead of asking. This practice embeds correctness-over-completion as a structural gate in the implementation workflow.

The practice targets instruction and skill files — no runtime code changes. It adds standards to the orchestrator's implementation skill (`orch-implementation`), a universal directive to agent common rules, and a cross-reference from the day-dream planning skill.

**Priority:** P1  
**Difficulty:** `[KNOWN]` — instruction/skill text edits, patterns are clear

---

## 📚 Prior Art

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| Feature 05: Fix Backward Compat | Internal pattern | High — established clean-code-first directive | 🔧 Adapt |
| DRY Principle (Don't Repeat Yourself) | Industry pattern | Medium — Pillar 1 extends this to agent context | 🔧 Adapt |
| "Dead Code Elimination" (compiler technique) | Industry pattern | Low — compile-time, not agent-time | ❌ Reject |

### Usage Decision

**Using:** Feature 05's clean-code-first directive as foundation  
**How:** Non-Vibe Code extends Feature 05's backward-compat directive into a full engineering discipline with three actionable pillars and explicit gates  
**Why this over alternatives:** Feature 05 covers the "don't add fallbacks" case but doesn't address duplication or speculative coding — Non-Vibe Code is the complete practice

### Build-vs-Adopt Justification

| Rejected Solution | Reason for Building Custom |
|-------------------|---------------------------|
| Generic linting rules | Can't enforce "ask instead of guess" or "unify before duplicate" at lint time — these are agent behavioral rules, not syntax rules |

---

## 🗺️ System Context

N/A — Instruction/skill text edits only. No module integrations or external APIs.

---

## 📊 Data Flow

N/A — No data transformation. Changes are to markdown instruction files that agents read at prompt time.

---

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- FREE ZONE START -->

## [Custom] 🏛️ The Three Pillars

### Pillar 1: Unify Before Duplicating

Refactor existing code to serve both the old and new case. If unification is unsafe, document **WHY** and flag for human review. Silent duplication = defect.

**"Unify or Justify" Gate:** Before adding any overlapping function, the agent MUST refactor the original OR explicitly justify why not. No third option.

```
✅ CORRECT:  Found existing parse_config(). Extended it to handle both formats.
✅ CORRECT:  Cannot unify — old callers depend on return type. # JUSTIFY: [ticket/reason]
❌ DEFECT:   Added parse_config_v2() alongside parse_config() without checking callers.
```

### Pillar 2: No Dead Fallbacks

No `try(new)/except(old)`. No bare `except` that silently swallows. No unused params "just in case."

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

### Pillar 3: Ask, Don't Guess

When uncertain about intent or impact, emit `[UNSURE]` marker and escalate to human rather than writing speculatively runnable code. Surface blocking questions instead of guessing.

```
✅ CORRECT:  # [UNSURE] Should this also handle nested configs? Escalating.
✅ CORRECT:  # TODO(verify): Assuming UTF-8 — confirm with user if other encodings needed
❌ DEFECT:   def parse(data, encoding="utf-8", nested=True, strict=False):  # Just in case
```

#### Batched Escalation

When agents encounter uncertainties or need human input, they MUST NOT ask immediately upon each encounter. Instead:

- **Collect** all `[UNSURE]` items and questions during the current work phase
- **Batch** them into a single escalation at the end of the phase or at a natural stopping point
- **Present** as a numbered list with context for each item

**Rationale:** Each agent request costs tokens/money. One batched question with 5 items is far cheaper than 5 separate round-trips.

```
✅ CORRECT:  Finish phase, then: "3 items need your input: 1) ... 2) ... 3) ..."
❌ DEFECT:   Stop after each uncertainty to ask a single question
```

## [Custom] ⚖️ Careful vs Afraid

The distinction that drives everything:

| Behavior | Careful (✅) | Afraid (❌) |
|----------|-------------|------------|
| Before editing old code | Checked callers/usages, confirmed impact | Added redundant code without checking |
| When uncertain | Noted uncertainty with `# TODO(verify):`, then proceeded | Wrapped in fallback without understanding |
| When feature overlaps | Refactored original to serve both cases | Duplicated to avoid touching old code |
| When old code is wrong | Fixed it, documented why | Left it, added workaround alongside |
| When asked to extend | Extended in place | Created `_v2` variant next to original |

**The litmus test:** If you can't explain WHY you didn't modify the original, you were afraid, not careful.

## [Custom] ⚡ Git Checkpoint Convention

Being careful means **checkpointing before risky phases** — being afraid means avoiding the risky phase entirely. When an implementation plan includes a phase that touches many files (large refactor, cross-module rename, etc.), the planning agent MUST insert a `⚡ GIT CHECKPOINT` marker before that phase.

The human reviews and approves the plan — that approval is implicit consent to checkpoint. No runtime asking needed.

**Rule:** When planning phases that involve large refactors or risky changes, agents MUST note `⚡ GIT CHECKPOINT` in the implementation plan before that phase.

**Format in implementation plans:**
```
## Phase N: Big Refactor
⚡ GIT CHECKPOINT — commit before this phase (large refactor touching N files)
```

**Why this fits Non-Vibe Code:** This is the "careful but not afraid" principle applied to git workflow. Commit for safety, then proceed boldly with the refactor. Don't skip the refactor out of fear — checkpoint and go.

```
✅ CAREFUL:   ⚡ GIT CHECKPOINT, then refactor 12 files confidently
❌ AFRAID:    Skip the refactor because "too many files to touch"
❌ RECKLESS:  Refactor 12 files with no checkpoint
```

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- FREE ZONE END -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

---

## 🔗 Integration Points

| Connects To | Direction | Data | Protocol |
|-------------|-----------|------|----------|
| `orch-implementation/SKILL.md` | → OUT | Non-Vibe Code standards + POST-CHECK | Markdown skill file |
| `agent_common_rules.instructions.md` | → OUT | Universal directive | Markdown instruction file |
| `day-dream/SKILL.md` | → OUT | Cross-reference pointer | Markdown skill file |

---

## 👥 User Stories

| As a... | I want to... | So that... |
|---------|--------------|------------|
| HyperArch (implementing agent) | Have clear "Unify or Justify" gates in my implementation standards | I don't silently duplicate code |
| HyperSan (reviewing agent) | Have a Non-Vibe Code checklist in POST-CHECK | I can catch afraid-not-careful patterns |
| Any ADHD agent | Have a universal directive against speculative code | I ask instead of guess when uncertain |
| Human reviewer | See `[UNSURE]` markers instead of speculative code | I review intent decisions, not agent guesses |

---

## ✅ Acceptance Criteria

- [ ] `orch-implementation` SKILL.md contains Non-Vibe Code section in Arch's implementation standards (includes Batched Escalation sub-rule under Ask Don't Guess)
- [ ] `orch-implementation` SKILL.md contains Non-Vibe Code POST-CHECK checklist for San
- [ ] `agent_common_rules.instructions.md` contains universal Non-Vibe Code directive
- [ ] `day-dream` SKILL.md Clean-Code-First section cross-references `orch-implementation` for the full practice
- [ ] Three pillars clearly defined and actionable (Unify Before Duplicating, No Dead Fallbacks, Ask Don't Guess)
- [ ] Careful vs Afraid distinction documented with concrete examples
- [ ] Git checkpoint convention documented

---

## 🛠️ Technical Notes

### Constraints

- All changes are instruction/skill markdown edits — no runtime code
- Must not duplicate Feature 05's content; extend and cross-reference instead
- Pillar definitions must be agent-parseable (clear, unambiguous rules)

### Considerations

- The `[UNSURE]` marker from Pillar 3 needs to be a pattern agents actually emit, not just documentation — ensure `agent_common_rules` makes this actionable
- `# FALLBACK: [reason] expires when [condition]` annotation format should be consistent across all agent instructions

---

## ⚠️ Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Agent genuinely can't unify (different return types, different callers) | Must add `# JUSTIFY:` annotation explaining why, flagged for human review |
| Fallback is permanent (e.g., graceful degradation by design) | Use `# FALLBACK: [reason] permanent — [justification]` — still requires annotation |
| Agent is unsure but question is trivial | Use `# TODO(verify):` for low-risk assumptions, `[UNSURE]` for blocking questions |
| Existing codebase already has Non-Vibe patterns | Don't fix proactively — apply going forward, flag existing violations only when touching that code |
| Ask one question per round-trip | Batch all uncertainties, present at end of phase |

---

## ❌ Out of Scope

- Automated tooling to detect Non-Vibe violations (future feature, not P1)
- Rewriting existing code that has afraid-patterns (apply going forward)
- External library API compatibility concerns (different domain)
- Runtime enforcement or linting (these are agent behavioral rules)

---

## 🔗 Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Feature 05: Fix Backward Compat | ✅ Done | Clean-code-first directive is the foundation this extends |
| `orch-implementation` skill | Pending | File to be edited — must exist or be created |
| `agent_common_rules.instructions.md` | Done | File exists, to be extended |
| `day-dream/SKILL.md` | Done | File exists, Clean-Code-First section to be cross-referenced |

---

## 🖼️ Related Assets

*No assets needed — this feature is instruction text, no visual artifacts.*

---

## ❓ Open Questions

- Should `[UNSURE]` markers have a severity level (blocking vs informational)?
- Should there be a maximum number of `# JUSTIFY:` annotations per PR before triggering deeper review?

---

## ✅ Feature Validation Checklist

### Narrative Completeness
- [x] **The Story** section clearly states user problem and value
- [x] **Intent** is unambiguous to a non-technical reader
- [x] **Scope** is explicitly bounded (Out of Scope section filled)

### Technical Completeness
- [x] **Integration Points** table has all connections documented
- [x] **Edge Cases** table covers failure scenarios
- [x] **Dependencies** are listed with status
- [x] **Acceptance Criteria** are testable (not vague)

### Linkage
- [ ] **Related module specs** link back to this feature
- [x] Feature linked from implementation plan

---

**Prev:** [Template Refresh](./08_feature_template_refresh.md) | **Next:** *(none — last feature)*

---

**← Back to:** [Index](./00_index.md)
