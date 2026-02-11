# Discussion Record: Task Time Estimation System Redesign

| Field | Value |
|-------|-------|
| **Date** | 2026-02-11 |
| **Topic** | Task Time Estimation System Redesign |
| **Participants** | HyperArch, HyperDream |
| **Rounds** | 1 |
| **Status** | ✅ Consensus |

---

## Positions

### HyperArch
- Favored **Option 2** (time slots)
- Key argument: Agents need "work units per session" not hours; discovery can 10x effort
- Initially wanted complexity flag
- Accepted deferring complexity to P1 (YAGNI principle)

### HyperDream
- Favored **Option 2**
- Key argument: Walking skeleton principle — embarrassingly simple is right for P0
- Offered advisory-only complexity field as compromise
- Arch already accepted deferral before compromise was needed

---

## Final Consensus

1. **Replace hours/minutes with "actions"** (4 slots per day baseline)

2. **Tasks cost 1-3 slots**; Epic (4+) must decompose

3. **Magnitude retained** as cognitive complexity signal mapped to slots:
   | Magnitude | Slots |
   |-----------|-------|
   | Trivial | <<1 slot |
   | Light | 1 slot |
   | Standard | 2 slots |
   | Heavy | 3 slots |
   | Epic | 4+ → **DECOMPOSE** |

4. **Complexity annotations deferred to P1**

---

## Artifacts Updated

| Artifact | Change |
|----------|--------|
| `80_implementation.md` | Durations + Decisions Log |
| `03_feature_fix_estimation.md` | Proposed Time Scale section |
| `day-dream/SKILL.md` | Estimation Defaults section |

---

## Rationale Summary

The hour-based estimation was abandoned because AI agent work sessions don't map cleanly to wall-clock time. Discovery tasks can 10x in scope unexpectedly. Slot-based "action budgets" give agents a clearer signal: "you have N work units today" rather than "this should take 2 hours."

The magnitude field pulls double duty as a cognitive complexity indicator while also mapping to slot costs, keeping the schema minimal for P0.
