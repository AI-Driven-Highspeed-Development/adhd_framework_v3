# Discussion Record: DREAM v4.02 Design Decisions

## Metadata

| Field        | Value                            |
|--------------|----------------------------------|
| Topic        | DREAM v4.02 Design Decisions     |
| Date         | 2026-02-12                       |
| Participants | HyperArch, HyperSan, HyperDream |
| Rounds       | 1                                |
| Status       | Consensus ✅                     |

---

## Decisions

### D1: 8-Slot System with Fixed Maximums

Trivial=1, Light=2, Standard=3, Heavy=5, Epic=8. These are **maximums** — actual slots can be lower. Each slot ≈ 1h AI-agent time.

### D2: Human Decides Plan-or-Not, DREAM Decides Format

Human initiates planning; DREAM determines folder vs single file. Human override suppresses auto-detection.

### D3: Keep L0–LN as Optional Communication Aids

No formal machinery. L0=plan, L1=sub-plan for 95% of cases.

### D4: Conditional Merge of Exec Summary + Architecture

- **System Plans**: Keep separate (architecture stabilizes early, summary evolves).
- **Procedure Plans**: Merge into `01_summary.md` (both lightweight, co-evolve).

### D5: Keep `NN_` File Prefix Format

Established ADHD-readable convention for glanceability and ordering.

### D6: One Folder Structure, Two Template Profiles

No type system bifurcation. System and Procedure Plans share primitives. Procedure Plans omit architecture/module_structure files (files don't exist on disk, not filled with N/A).

### D7: Document Ordering — Structure First

v4.02 opens with folder structure diagrams, then explains how scope/scale/type modify the structure.

---

## Key Positions by Agent

### HyperArch

- Proposed different folder structures for System vs Procedure initially.
- Shifted to San's one-model approach during CHALLENGE.
- Accepted conditional merge (D4) — initially opposed full merge due to lifecycle mismatch.
- Proposed slot maximums (not targets/ranges).

### HyperSan

- Insisted on fixed slot counts per magnitude (no ranges).
- Flagged spec bifurcation risk for two plan types — proposed template-set differentiation.
- Recommended "omit files entirely" over "fill with N/A".
- Noted need for explicit override mechanism when human skips planning.

### HyperDream

- Initially wanted full merge of exec summary + architecture.
- Initially wanted separate folder structures for System/Procedure.
- Accepted both conditional merge and one-model approach during CHALLENGE.
- Coined "System = noun, Procedure = verb" framing.

---

## Outcome

Created `DREAM_v4.02.md` at `.agent_plan/day_dream/DREAM_v4.02.md` (1066 lines).
