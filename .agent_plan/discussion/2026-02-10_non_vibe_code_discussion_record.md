# Discussion Record — Non-Vibe Code Practice

| Field        | Value                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------ |
| Topic        | Non-Vibe Code Practice — expanding Clean-Code-First into comprehensive engineering discipline |
| Date         | 2026-02-10                                                                                 |
| Participants | HyperArch, HyperDream, HyperSan                                                           |
| Rounds       | 1                                                                                          |
| Status       | Consensus ✅                                                                                |

---

## PROPOSE Phase

### HyperArch

Most dangerous anti-pattern is **"defensive duplication"** — creating new methods that reimplement existing logic rather than refactoring the original. This stems from fear of breaking things, but produces divergent code paths that silently rot.

**Proposals:**

- **"Unify or Justify" gate** — before adding any new function that overlaps with an existing one, the implementer must either unify into a single implementation or document a concrete justification for the duplication.
- **Fallback annotation requirement** — all fallback paths must carry a `# FALLBACK:` annotation that includes an **expiration condition** (e.g., `# FALLBACK: remove when min Python >= 3.11`). Fallbacks without expiration are dead code waiting to happen.

### HyperDream

**"Non-Vibe Code"** is a correctness-over-completion contract. The name captures the opposite of vibe coding: every line must be intentional, verified, and justified — not generated on vibes and hoped to work.

**Three Pillars proposed:**

1. **No Dead Fallbacks** — every fallback path must be reachable, tested, and annotated with an expiration condition.
2. **Unify Before Duplicating** — check existing implementations before writing new ones. If overlap exists, refactor first.
3. **Ask, Don't Guess** — when uncertain about behavior, semantics, or compatibility, use an `[UNSURE]` marker and escalate rather than writing speculative code.

**Implementation stance:**

- Elevate to a first-class engineering instruction (not just a style guideline).
- The `[UNSURE]` marker becomes a formal vocabulary item — agents encountering uncertainty must tag it rather than silently guessing.
- Shared gate embedded in both HyperArch and HyperSan checklists so it's enforced at implementation AND review time.

### HyperSan

**Red flags identified from real incidents:**

- **Dead-code duplication** — new wrapper functions that shadow existing ones, neither removed nor consolidated.
- **Silent swallow patterns** — `except: pass` or fallback returns that hide real failures.
- **Speculative compatibility** — code added "just in case" for scenarios that were never verified to exist.

**Key distinction:**

> **Careful** = checked usages + noted uncertainty explicitly.
> **Afraid** = added redundant code without verification.

**Proposal:** Embed Non-Vibe Code checks into the POST-CHECK gate of `orch-implementation`. This ensures every implementation pass is reviewed for these anti-patterns before completion.

---

## CHALLENGE Phase

No challenge needed — strong alignment across all three participants on both the problem definition and the proposed solution structure.

---

## SYNTHESIZE — Consensus

### Three Pillars Adopted

| # | Pillar                     | Mechanism                                            |
|---|----------------------------|------------------------------------------------------|
| 1 | **Unify Before Duplicating** | "Unify or Justify" gate — refactor or document why   |
| 2 | **No Dead Fallbacks**        | `# FALLBACK:` annotation with expiration condition   |
| 3 | **Ask, Don't Guess**         | `[UNSURE]` marker — escalate instead of speculating  |

### Votes

| Agent      | Vote   |
| ---------- | ------ |
| HyperArch  | ACCEPT |
| HyperDream | ACCEPT |
| HyperSan   | ACCEPT |

---

## Outcome

- New feature `09_feature_non_vibe_code.md` created.
- Current P1 (DREAM Integration) moved to **P2**.
- New **P1: Non-Vibe Code Practice** established with 4 tasks:
  1. `orch-implementation` skill updates (PRE-CHECK + POST-CHECK gates)
  2. `agent_common_rules` directive addition
  3. Day-dream cross-reference in blueprint
  4. Feature document finalization
