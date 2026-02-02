# 📋 Discussion Report: Module Scale Management

> **Date**: 2026-02-02  
> **Participants**: HyperSan, HyperArch, HyperDream  
> **Status**: ✅ CONSENSUS REACHED  
> **Decision**: Layered Module Management Strategy

---

## 🎯 Problem Statement

Managing cognitive load across a large module ecosystem (~78 modules) where the user operates as both **framework developer** and **project developer** (dual-citizenship).

### Scale Breakdown
| Category | Count | Description |
|----------|-------|-------------|
| Framework | 14 | Core ADHD framework modules |
| Pulled | 23 | External modules pulled via adhd-pull |
| Project | 41 | Project-specific modules |
| Focused | 7 | Currently active modules |
| Forgotten | 3 | Unpushed changes, lost in noise |

### Why Previous Approaches Failed
- **Simple filters**: Tried for 2 months, didn't stick
- **Workspace generation**: Too manual, cognitive overhead
- **Git pushing reminders**: Solved wrong problem (symptom, not cause)
- **focus_modules MCP tool**: Wrong direction (enforcement vs information)

---

## ✅ Final Consensus: Layered Module Management

| Priority | Layer | Mechanism | Investment |
|----------|-------|-----------|------------|
| **P0.0** | L4: Workspace Profiles | Multiple `.code-workspace` files | Documentation only |
| **P0.1** | L1: Origin Tags | Tag modules `framework/external/local` | Schema/convention |
| **P0.2** | L0: Proactive Attention | "N modules need attention" on MCP start | MCP enhancement |
| **P1** | L2: Dirty Filter | `adhd dirty` CLI command | CLI + MCP tool |
| **P2** | L3: Gravity Zones | Auto-promote touched, time-decay others | Design spike needed |

---

## 🧭 Guiding Principles

1. **Proactive > Reactive** — Surface information before user asks
2. **Information > Enforcement** — Show state, don't block actions  
3. **Gravity > Walls** — Attention follows action naturally
4. **Support Dual-Citizenship** — Framework work and project work coexist

---

## 📝 Amendments to Initial Proposal

### Terminology
- **Rename**: "ownership" → "origin" (avoids collision with git/legal "ownership")
- **Origin values**: `framework` | `external` | `local`

### Implementation Details
- **Origin derivation**: May be path-derived from folder structure:
  - `cores/` → `framework`
  - `pulled/` or external git URLs → `external`  
  - `project/`, `managers/`, `plugins/`, `utils/` → `local`
- **Session start**: Defined as first MCP discovery call (`list_modules` or `get_project_info`)
- **L3 Gravity Zones**: Requires design spike before implementation (complex state tracking)

---

## 🔧 Decision: workspace_core Module

| Aspect | Decision |
|--------|----------|
| **Keep/Remove** | KEEP for now |
| **Rationale** | Still generates `.code-workspace` files |
| **Simplification** | Default to ALL modules visible (no smart filtering) |
| **Enhancement** | Add comment header explaining right-click focus workflow |
| **Future** | L3 gravity zones may eventually replace manual workspace management |

---

## 📌 Action Items

| # | Item | Owner | Priority | Status |
|---|------|-------|----------|--------|
| 1 | Document workspace profile pattern (L4) | User | P0.0 | ⏳ TODO |
| 2 | Define origin convention (L1) - path-derived | Arch | P0.1 | ⏳ TODO |
| 3 | Add "needs attention" summary to MCP session start (L0) | Impl | P0.2 | ⏳ TODO |
| 4 | Add `adhd dirty` CLI command (L2) | Impl | P1 | ⏳ TODO |
| 5 | Design spike for gravity zones (L3) | Dream | P2 | ⏳ TODO |

---

## 🗳️ Participant Sign-off

| Agent | Vote | Notes |
|-------|------|-------|
| HyperSan | ✅ ACCEPT | With origin terminology amendment |
| HyperArch | ✅ ACCEPT | With path-derivation amendment |
| HyperDream | ✅ ACCEPT | With L3 design spike deferral |

---

## 📎 Related Documents

- Future: `.agent_plan/day_dream/gravity_zones/` (L3 design spike)
- Future: `mcps/adhd_mcp/` enhancement for L0 proactive attention

---

*Discussion concluded 2026-02-02. Implementation may proceed per priority order.*
