# DREAM v4.02 — Concept Report: System Performance Analysis

> **Type:** 3-Agent Structured Discussion Report  
> **Status:** ✅ Consensus Reached  
> **Reference:** [`DREAM_v4.02_concept_demo.md`](DREAM_v4.02_concept_demo.md)

---

## Discussion Metadata

| Field | Value |
|-------|-------|
| **Date** | February 12, 2026 |
| **Format** | Structured 3-Agent Discussion (Propose → Challenge → Synthesize) |
| **Rounds** | 3 |
| **Status** | ✅ **Consensus** |
| **Subject** | DREAM v4.02 performance under the NovaMart thought experiment |

**Participants:**

| Agent | Role | Domain |
|-------|------|--------|
| HyperDream | Visionary Architect | Planning philosophy, compromise design |
| HyperArch | Implementation Architect | Spec-level fixes, boundary enforcement |
| HyperSan | Validation & QA | Gap identification, gate conditions |

**Input Artifact:** NovaMart concept demo — 7 months, 7 plans, 12 modules, 4 meetings, 3 revamps.

---

## What DREAM v4.02 Got Right

```
┌─────────────────────────────────────────────────────────────────────┐
│  VERDICT: The core framework is SOUND.                              │
│  6 design decisions validated under sustained real-world pressure.  │
└─────────────────────────────────────────────────────────────────────┘
```

| # | What Worked | Evidence from NovaMart |
|---|------------|----------------------|
| 1 | **System Plan vs Procedure Plan distinction** | 3 System Plans (core_shop, customer_engagement, marketplace) described WHAT to build. 3 Procedure Plans (checkout_redesign, payment_migration, multitenancy) described HOW to migrate. Zero ambiguity in classification. |
| 2 | **`_overview.md` as single entry point** | Root `_overview.md` stayed navigable across all 7 stages — lists plan name + type + status only, never deep trees. |
| 3 | **Status markers sufficient at plan level** | ⏳🔄✅🚫🚧 told the full story at every folder level. Scanning any tree instantly reveals project state. |
| 4 | **Phased execution with `pNN_` directories** | "p00 DONE, p01 WIP, p02 TODO" gives instant progress reading. Phases prevented scope creep within plans. |
| 5 | **"Omit, don't N/A" principle** | Procedure Plans used merged `01_summary.md` — no awkward empty `02_architecture.md`. Clean and intentional. |
| 6 | **Human authority on planning decisions** | All plan creation/cut/scope decisions came from meetings and team judgment. Agents executed within plan boundaries, never created plans autonomously. |

---

## What Needs Improvement

### 7 Areas of Consensus

The discussion identified 7 problem areas. These decompose into **9 concrete spec additions**, all reaching consensus.

```
┌──────────────────────────────────────────────────────────────┐
│  PROBLEM AREAS                                               │
│                                                              │
│  1. Completed plans create noise        → Additions #1       │
│  2. Module specs go stale silently      → Additions #2       │
│  3. No verification on plan closure     → Additions #3, #4   │
│  4. Plans lack provenance (origin)      → Addition  #5       │
│  5. Module history scattered            → Addition  #6       │
│  6. Plan type selection ambiguity       → Addition  #7       │
│  7. Current state hard to find          → Additions #8, #9   │
└──────────────────────────────────────────────────────────────┘
```

---

### 9 Proposed Spec Additions — Summary Table

| # | Addition | Severity | Effort | Where in Spec |
|---|---------|----------|--------|---------------|
| 1 | `_completed/` archival directory for DONE plans | WARNING | EASY | Chapter 2 (Structure) |
| 2 | `last_updated` frontmatter on module specs | BLOCKER→FIX | EASY | Chapter 1 (Author, §1.14) |
| 3 | Reconciliation checklist on Procedure Plan close | BLOCKER→FIX | MEDIUM | Chapter 2 (Execute, new §) |
| 4 | State Delta append to root `_overview.md` on plan close — **GATE CONDITION** | BLOCKER→FIX | MEDIUM | Chapter 2 (Execute, plan closure rules) |
| 5 | `origin:` field in `_overview.md` frontmatter | WARNING | EASY | Chapter 1 (Author, §1.14) |
| 6 | Module index table in root `_overview.md` | WARNING | MEDIUM | Chapter 1 (Author, §1.14) |
| 7 | Plan type tiebreaker rule | WARNING | EASY | Chapter 1 (Author, §1.4) |
| 8 | `## Current Sprint` section at TOP of root `_overview.md` | WARNING | EASY | Chapter 1 (Author, §1.14) |
| 9 | Recording rule: decisions that create/modify/cut plans MUST be recorded | WARNING | EASY | Chapter 1 (Author, §1.25) |

---

### Addition #1 — `_completed/` Archival Directory

**Problem:** After 7 months, 5 completed plans consume ~80% of folder footprint. Newcomers face signal-to-noise issues scanning the root.

**Rule to add:**
> When a plan reaches ✅ DONE or 🚫 CUT, move its directory to `.agent_plan/day_dream/_completed/`. The root `_overview.md` retains a summary row with status and completion date. Active plans remain in root.

**NovaMart example:**
```
.agent_plan/day_dream/
├── _overview.md                    ← Still lists ALL plans (active + completed)
├── _completed/
│   ├── core_shop/                  ← ✅ DONE — Nov 2025
│   ├── checkout_redesign/          ← ✅ DONE — Sep 2025
│   ├── customer_engagement/        ← ✅ DONE — Dec 2025
│   ├── payment_gateway_migration/  ← ✅ DONE — Nov 2025
│   ├── multitenancy_migration/     ← ✅ DONE — Jan 2026
│   └── mobile_optimization_vision.md  ← 🚫 CUT — Nov 2025
├── marketplace/                    ← 🔄 WIP (only active plan visible)
├── exploration/
└── templates/
```

---

### Addition #2 — `last_updated` Frontmatter on Module Specs

**Problem:** When checkout was redesigned (Revamp 1), `core_shop/modules/checkout.md` needed updating. No mechanism detects stale specs.

**Rule to add:**
> Every module spec file MUST contain `last_updated: YYYY-MM-DD` in its YAML frontmatter. Any plan that modifies a module's behavior MUST update this field in the owning plan's module spec.

**NovaMart example:**
```yaml
# core_shop/modules/checkout.md — frontmatter
---
module: checkout
last_updated: 2025-09-15      # ← Updated when checkout_redesign landed
modified_by_plans:
  - checkout_redesign          # ← Audit trail
  - payment_gateway_migration
---
```

---

### Addition #3 — Reconciliation Checklist on Procedure Plan Close

**Problem:** Procedure Plans modify existing modules but have no mandatory step to verify that all touched module specs are updated.

**Rule to add:**
> When a Procedure Plan is marked ✅ DONE, the author MUST complete a reconciliation checklist in the plan's `_overview.md`:
>
> ```markdown
> ## Reconciliation
> - [x] checkout.md (core_shop) — updated to reflect state machine
> - [x] inventory_sync.md (core_shop) — updated reservation semantics
> - [x] cart.md (core_shop) — no changes needed
> ```

**NovaMart example** (checkout_redesign closure):
```markdown
## Reconciliation
- [x] checkout.md (core_shop/modules/) — last_updated: 2025-09-15
- [x] inventory_sync.md (core_shop/modules/) — last_updated: 2025-09-15
- [x] cart.md (core_shop/modules/) — reviewed, no changes
```

---

### Addition #4 — State Delta in Root `_overview.md` (GATE CONDITION)

**Problem:** After 7 months and 7 plans, understanding "what is checkout's current state?" requires reading 4 separate plans chronologically. No accumulating summary exists.

**Rule to add:**
> **GATE CONDITION:** A plan CANNOT be marked ✅ DONE without appending a State Delta entry to the root `_overview.md`. State Deltas are append-only entries logging what changed in the codebase.
>
> ```markdown
> ## State Deltas
>
> ### ✅ checkout_redesign — Sep 2025
> - checkout: linear flow → reservation-based state machine
> - inventory_sync: new module, pessimistic locking + TTL
>
> ### ✅ payment_gateway_migration — Nov 2025
> - checkout: direct Stripe calls → PaymentProvider abstraction
> - payment: new module with Stripe/PayPal/Mollie adapters
> ```

**NovaMart example** — scanning State Deltas tells you checkout's full history in 30 seconds:
```
checkout journey (read top-to-bottom):
  core_shop (Jul)      → basic linear flow
  checkout_redesign    → state machine + reservations
  payment_migration    → PaymentProvider abstraction layer
  multitenancy         → vendor-scoped order queries
```

---

### Addition #5 — `origin:` Field in `_overview.md` Frontmatter

**Problem:** Plans appear in the folder tree with no link to what triggered them. You have to grep exploration docs to find the meeting that greenlit the marketplace.

**Rule to add:**
> Plan `_overview.md` frontmatter MUST include `origin:` referencing the exploration doc, meeting, or decision that created it.

**NovaMart example:**
```yaml
# marketplace/_overview.md — frontmatter
---
plan: marketplace
type: system
origin: exploration/meeting_2025_11_12_marketplace.md
---
```

---

### Addition #6 — Module Index Table in Root `_overview.md`

**Problem:** Module #3 (checkout) was introduced by `core_shop`, redesigned by `checkout_redesign`, rewired by `payment_gateway_migration`, and scoped by `multitenancy_migration`. No single place maps module → plans.

**Rule to add:**
> Root `_overview.md` MUST contain a Module Index table mapping each module to its origin plan and all modifier plans.

**NovaMart example:**
```markdown
## Module Index

| Module | Origin Plan | Modified By |
|--------|------------|-------------|
| product_catalog | core_shop | multitenancy_migration |
| cart | core_shop | payment_gateway_migration |
| checkout | core_shop | checkout_redesign, payment_gateway_migration, multitenancy_migration |
| user_auth | core_shop | multitenancy_migration |
| inventory_sync | core_shop | checkout_redesign |
| vendor_portal | marketplace | — |
```

---

### Addition #7 — Plan Type Tiebreaker Rule

**Problem:** Some plans could be classified as either System or Procedure. The spec lacks a disambiguation rule for edge cases.

**Rule to add:**
> **Tiebreaker:** If a plan is triggered by an existing plan AND its primary deliverable modifies existing code (rather than creating new modules), it is a **Procedure Plan**.

**NovaMart example:**
- `checkout_redesign` — triggered by `core_shop`, primary deliverable modifies existing checkout code → **Procedure Plan** ✅
- `marketplace` — not triggered by existing plan, introduces new module (`vendor_portal`) → **System Plan** ✅

---

### Addition #8 — `## Current Sprint` Section at Top of Root `_overview.md`

**Problem:** Root `_overview.md` lists all plans (active + completed), but finding "what is the team doing RIGHT NOW?" requires scanning the full table.

**Rule to add:**
> Root `_overview.md` MUST have a `## Current Sprint` section as its FIRST content section, containing 3-5 bullets of actively worked items.

**NovaMart example:**
```markdown
## Current Sprint

- 🔄 marketplace/p01 — order splitting logic (Agent-B)
- ⏳ marketplace/p02 — payout system, commission engine
- 🔄 marketplace/05_order_routing.md — multi-vendor cart
```

---

### Addition #9 — Decision Recording Rule

**Problem:** Meeting 3 greenlit the marketplace and cut the recommendation engine. If the meeting doc gets archived without capturing these decisions in plans, context is lost.

**Rule to add:**
> Decisions that create, modify, or cut plans MUST be recorded in the exploration/meeting doc with explicit links to affected plans. This is documentation-time, not optional.

**NovaMart example:**
```markdown
# meeting_2025_11_12_marketplace.md

## Decisions
- ✅ CREATE: marketplace/ (System Plan, Epic)
- 🚫 CUT: customer_engagement/05_recommendation_engine.md
- 🚫 CUT: mobile_optimization_vision.md
```

---

## The Deeper Insight: Execution vs Comprehension

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│   DREAM v4.02 is a FORWARD-EXECUTION engine.                         │
│   It excels at: authoring plans, executing tasks, tracking status.    │
│                                                                        │
│   It is weaker at BACKWARD-COMPREHENSION.                             │
│   Understanding "what is module X's current state?"                   │
│   requires reading N plans chronologically.                           │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Why Not a Living Document?

The instinctive fix — a "living architecture doc" that stays current — was rejected by all three agents:

> A living doc is itself a plan that never completes. It would go stale for the same reasons module specs go stale: no gate condition forces updates.

### The Architectural Fix (3-part)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  1. BOUNDARY        DREAM owns planning truth.                     │
│                     Code + READMEs own runtime truth.              │
│                     Don't duplicate across boundaries.             │
│                                                                     │
│  2. STATE DELTAS    Append-only changelog in root _overview.md.    │
│                     Bridges the comprehension gap WITHOUT          │
│                     creating a parallel document system.           │
│                     GATE CONDITION: can't close without it.        │
│                                                                     │
│  3. ARCHIVAL        Move completed plans to _completed/.           │
│                     Reduces noise-to-signal ratio.                 │
│                     Root stays scannable at scale.                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Key principle:** The fix adds **3 lightweight conventions** (State Delta, reconciliation checklist, archival) rather than a new artifact type. Conventions enforced by gate conditions > conventions that rely on discipline.

---

## Scale Projections

| Metric | 7 Plans (demo) | 15 Plans | 30 Plans |
|--------|---------------|----------|----------|
| Root `_overview.md` entries | 7 (manageable) | 15 (needs archival) | 30 (breaks without `_completed/`) |
| Total files (approx) | ~115 | ~250 | ~500 |
| Plans touching checkout module | 4 | 6–8 | 10+ |
| Time to understand checkout's current state | Read 4 plans (~15 min) | With module index + State Deltas: scan root (~3 min) | Same with archival: scan active root (~3 min) |

```
Without fixes:           With fixes:
                         
  Plans                    Plans
  30 ┤ ██████████████       30 ┤ ████ active
     │ ██████████████          │ ████
     │ ██████████████          │ ████
  15 ┤ ████████               │ ████
     │ ████████            15 ┤ ███
     │ ████████               │ ███
   7 ┤ ████                   │ ███
     │ ████                 7 ┤ ██
     └──── root scan          └──── root scan
     All in root =            _completed/ absorbs
     noise grows              DONE/CUT plans
     linearly                 Active stays ≤5-8
```

---

## Agent Positions Summary

| Agent | Role | Key Contribution |
|-------|------|-----------------|
| **HyperDream** | Visionary | "State Delta in root `_overview.md`" compromise — lightweight append-only changelog that bridges the comprehension gap without creating a parallel document system |
| **HyperArch** | Implementation | Three-part spec fix (`last_updated` + reconciliation checklist + State Delta); established the boundary — "code is the living doc, not DREAM" |
| **HyperSan** | Validation | Identified the execution-vs-comprehension gap; elevated State Delta from optional convention to **mandatory gate condition** — plan cannot mark ✅ DONE without it |

---

## Next Steps

### Versioning Decision

| Option | Description | Tradeoff |
|--------|------------|----------|
| **v4.02 Amendment** | Incorporate all 9 additions now | Fast. Risk: spec grows before battle-testing. |
| **v4.03 Release** | Batch into next minor version | Clean. Risk: delay. |
| **Hybrid** | Ship BLOCKER→FIX (#2, #3, #4) as v4.02.1 hotfix; defer WARNING items to v4.03 | Balanced. Recommended. |

### Template Updates Required

| Template | Change | Priority |
|----------|--------|----------|
| `overview.template.md` | Add `origin:` frontmatter, `## Current Sprint`, `## State Deltas`, Module Index table | HIGH |
| `81_module_structure.template.md` | Add `last_updated:` frontmatter to module spec example | HIGH |
| Plan closure checklist (NEW) | Reconciliation checklist template for Procedure Plan close | HIGH |
| `simple.template.md` | Add `origin:` frontmatter | LOW |

### Ship-Now vs Needs-Design

```
┌─────────────────────────────────────────────────────┐
│  SHIP IMMEDIATELY (no design needed)                │
│                                                     │
│  #1  _completed/ directory        → mkdir + mv      │
│  #2  last_updated frontmatter     → add to template │
│  #5  origin: field                → add to template │
│  #7  Plan type tiebreaker         → add to spec §1.4│
│  #8  ## Current Sprint            → add to template │
│  #9  Decision recording rule      → add to spec     │
│                                                     │
├─────────────────────────────────────────────────────┤
│  NEEDS DESIGN (interaction details TBD)             │
│                                                     │
│  #3  Reconciliation checklist     → checklist format │
│  #4  State Delta + gate condition → gate enforcement │
│  #6  Module index table           → maintenance rules│
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

*Report generated from 3-agent structured discussion on the DREAM v4.02 concept demo (NovaMart thought experiment). All 9 proposed additions reached consensus.*
