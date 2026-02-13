# DREAM v4 — Unified Planning System Reference

**Purpose:** Single source of truth unifying all three DREAM documentation sources  
**Status:** 📐 Draft — Contains unresolved decision blocks  
**Created:** February 2026

---

## Table of Contents

1. [TL;DR](#1-tldr)
2. [System Overview](#2-system-overview)
3. [Core Concepts](#3-core-concepts)
4. [Magnitude Routing](#4-magnitude-routing)
5. [Tier Selection](#5-tier-selection)
6. [Filesystem Structure](#6-filesystem-structure)
7. [Document Authoring](#7-document-authoring)
8. [Agent Protocol](#8-agent-protocol)
9. [Templates Reference](#9-templates-reference)
10. [Estimation](#10-estimation)
11. [Conflicts & Decisions](#11-conflicts--decisions)
12. [Anti-Patterns](#12-anti-patterns)

**Sources Unified:**

| # | Source | Location | Focus |
|---|--------|----------|-------|
| S1 | `dream-planning` skill | `.github/skills/dream-planning/SKILL.md` | Decomposition protocol, hierarchy, agent lifecycle |
| S2 | `day-dream` skill | `.github/skills/day-dream/SKILL.md` | Blueprint authoring, templates, status syntax |
| S3 | `DREAM_v3.md` | `.agent_plan/day_dream/DREAM_v3.md` | Standalone spec: node/contract YAML, L0-L4 levels |

---

## 1. TL;DR

**DREAM** (Decomposition Rules for Engineering Atomic Modules) is a protocol for breaking complex work into atomic, parallelizable units that AI agents can execute independently. It defines **how to assess complexity** (magnitude routing), **how to structure plans** (filesystem hierarchy), and **how agents coordinate** (sibling firewall + MANAGER/WORKER lifecycle). The `day-dream` skill adds **document authoring rules** — templates, status syntax, and the Story/Spec narrative pattern for ADHD-readable blueprints.

---

## 2. System Overview

```
┌──────────────────────────────────────────────────────────┐
│                    USER REQUEST                          │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  MAGNITUDE ASSESS   │  ← How complex is this?
              │  Trivial → Epic     │
              └─────────┬───────────┘
                        │
           ┌────────────┴────────────┐
           │                         │
     Trivial/Light             Standard/Heavy/Epic
           │                         │
           ▼                         ▼
   ┌───────────────┐      ┌──────────────────┐
   │ EXECUTE       │      │ TIER SELECT      │  ← Simple or Blueprint?
   │ directly      │      │ (day-dream)      │
   └───────────────┘      └────────┬─────────┘
                                   │
                          ┌────────┴────────┐
                          │                 │
                       Simple          Blueprint
                          │                 │
                          ▼                 ▼
                   ┌────────────┐   ┌───────────────┐
                   │ Single .md │   │ DECOMPOSE     │  ← Plan/Task tree
                   │ plan file  │   │ (dream-plan)  │
                   └────────────┘   └───────┬───────┘
                                            │
                                            ▼
                                   ┌────────────────┐
                                   │ DELEGATE       │  ← Assign to agents
                                   │ (sibling       │
                                   │  firewall)     │
                                   └───────┬────────┘
                                           │
                                           ▼
                                   ┌────────────────┐
                                   │ INTEGRATE      │  ← Parent merges
                                   └────────────────┘
```

**The system has three layers:**

| Layer | Responsibility | Primary Source |
|-------|---------------|----------------|
| **Routing** | Assess magnitude, decide decompose vs execute | S1 + S3 |
| **Structure** | Organize plans/tasks in filesystem | S1 + S2 + S3 |
| **Authoring** | Write readable documents with templates | S2 |

---

## 3. Core Concepts

### Unified Terminology

| Term | Definition | Agreed By |
|------|-----------|-----------|
| **Plan** | A decomposable unit containing ambiguity. Has children. Represented as a **directory** with `_overview.md`. | S1, S2, S3 |
| **Task** | A leaf unit — directly executable, no children. Represented as a **file** (`.md`). | S1, S2, S3 |
| **MANAGER** | Agent processing a plan — decomposes, delegates, integrates children. | S1, S3 |
| **WORKER** | Agent fulfilling a task — executes directly, produces artifacts. | S1, S3 |
| **Magnitude** | Complexity classification: Trivial / Light / Standard / Heavy / Epic. | S1, S2, S3 |
| **Sibling Firewall** | Hard rule: siblings NEVER read or write each other's content. Coordination goes through parent. | S1, S3 |
| **`_overview.md`** | Mandatory navigator file at every plan directory. Agents read this first. | S1, S2 |
| **Story → Spec** | Document authoring pattern: visual narrative first, then technical specification. | S2 |
| **Tier** | Simple (≤2 features) vs Blueprint (≥3 features or cross-module). | S2 |
| **Difficulty Label** | `[KNOWN]`, `[EXPERIMENTAL]`, `[RESEARCH]` — marks confidence level. | S2 |

### Concepts That Exist in Only One Source

| Term | Source | Definition | Notes |
|------|--------|-----------|-------|
| **L0–L4 Levels** | S3 only | Portfolio → Project → System → Module → Specification | Skills use filesystem nesting instead |
| **`node.yaml`** | S3 only | Routing metadata per node (~15 lines) | Skills use `plan.yaml` (3 lines) |
| **`contract.yaml`** | S3 only | Execution spec per node (~40 lines) | Skills have no equivalent |
| **`.spec.md`** | S3 only | L4 implementation detail file | Skills use task `.md` files |
| **`DREAM_AGENT_CARD.md`** | S3 only | Protocol rules file agents read first | Skills use skill files directly |
| **Complexity Classes A–D** | S3 only | Surface/Isolated/Integrated/Dense | Skills use difficulty labels |
| **`state/` directory** | S3 only | Machine-managed execution/history JSON | Not in skills |
| **`phases/*.yaml`** | S3 only | Parent-aggregated phase files | S2 uses `pNN_name/` directories |

> **DECISION NEEDED:** The concepts in the table above are exclusive to DREAM_v3. The two skills evolved a simpler system (directory-based, `_overview.md` convention, `plan.yaml`). Decide whether to:
> - **(A)** Adopt the skills' simpler system and deprecate DREAM_v3's YAML-heavy approach
> - **(B)** Keep both — use DREAM_v3's schemas for large/enterprise projects, skills' approach for standard work
> - **(C)** Merge — add `contract.yaml`-like acceptance criteria to the skills' task template

> **Human Developer Feedback:**
> - L0 - L4 levels are too rigid, however without a level number it is hard to refer to specific levels. We should make them L0 - LN for comunication purposes.
> - YAML is hard to read, and they should be read by agents and humans not programmatically. We should keep the metadata in markdown files. We can abandon all those YAML files.
---

## 4. Magnitude Routing

All three sources agree on the five magnitude levels. The routing rules are consistent:

### Magnitude Scale

| Magnitude | Slots | Action | Time (AI-Agent) | Time (Human ref) |
|-----------|-------|--------|-----------------|-------------------|
| **Trivial** | <<1 | Execute immediately | 5–15 min | 1–2 hours |
| **Light** | 1 | Execute directly | 15–60 min | 2–8 hours |
| **Standard** | 2 | Decompose if ≥3 subtasks | 1–4 hours | 1–3 days |
| **Heavy** | 3 | SHOULD decompose | 4–8 hours | 3–7 days |
| **Epic** | 4+ | **MUST decompose** | Must decompose | Must decompose |

### Routing Decision

```
Is magnitude Epic?          ──YES──► MUST decompose (MANAGER role)
                             │
Is magnitude Heavy?         ──YES──► SHOULD decompose (MANAGER role)
                             │
Is magnitude Standard       ──YES──► Decompose if ≥3 subtasks
  AND ≥3 subtasks?                    or cross-module. Otherwise execute.
                             │
Trivial or Light?           ──YES──► Execute directly (WORKER role)
```

### Magnitude Assessment Signals (S1)

| Signal | Points Toward |
|--------|--------------|
| Single file change | Trivial/Light |
| Multiple files, one module | Light/Standard |
| Cross-module changes | Standard/Heavy |
| New module or external API | Heavy/Epic |
| Ambiguity in requirements | Standard+ (needs decomposition) |

### Tier × Magnitude Routing (S2)

| Tier + Magnitude | Route |
|------------------|-------|
| Simple + Trivial/Light | Execute directly — no planning doc |
| Simple + Standard | Single plan file, execute in-session |
| Blueprint + Light/Standard | Blueprint docs, execute sequentially |
| Blueprint + Heavy | Blueprint docs, decompose into plan/task tree |
| Blueprint + Epic | Blueprint docs, mandatory decomposition, parallel agents |

### Complexity Classes (S3 Only)

| Class | Name | Human Review? | Source |
|-------|------|--------------|--------|
| A | Surface | No — auto-integrate | S3 |
| B | Isolated | Optional | S3 |
| C | Integrated | **Yes** | S3 |
| D | Dense | **Yes** | S3 |

> **DECISION NEEDED:** DREAM_v3 has a separate "Complexity Class" system (A-D) that gates human review. The skills instead use **Difficulty Labels** (`[KNOWN]`/`[EXPERIMENTAL]`/`[RESEARCH]`) for a different purpose (gating what can go in P0). These are orthogonal concepts — do you want to:
> - **(A)** Keep both systems (complexity classes for review gates, difficulty labels for P0 eligibility)
> - **(B)** Drop complexity classes, rely on difficulty labels only
> - **(C)** Merge into a single classification

---

## 5. Tier Selection

*Source: S2 (day-dream skill)*

| Tier | Use When | Template |
|------|----------|----------|
| **Simple** | ≤2 features, single module, no external APIs | `simple.template.md` |
| **Blueprint** | ≥3 features OR ≥2 cross-module deps OR external APIs | `blueprint/` folder |

### Auto-Detection Rules

```yaml
use_blueprint_tier:
  - feature_count >= 3
  - cross_module_imports >= 2
  - has_external_api: true
```

### Walking Skeleton Policy (S2)

Walking skeleton is **opt-in**, not automatic.

| When REQUIRED | When NOT Needed |
|---------------|-----------------|
| Cross-boundary integration risk | Single-module changes |
| External API dependency | Skill/template/doc edits |
| Multi-module data flow (3+ modules) | Self-contained features |
| | Magnitude ≤ Light |

> **DECISION NEEDED:** DREAM_v3 implies walking skeleton is standard practice (it shows `P0-walking-skeleton.yaml` in phase examples). The day-dream skill explicitly makes it opt-in with trigger criteria. Which approach?
> - **(A)** Opt-in (day-dream's position) — skip when triggers don't apply
> - **(B)** Default-on (DREAM_v3's position) — always have P0 walking skeleton

---

## 6. Filesystem Structure

This is the area of **greatest divergence** between the three sources.

### Side-by-Side Comparison

```
╔═══════════════════════════╦═══════════════════════════════════════╗
║  SKILLS APPROACH (S1+S2)  ║  DREAM_v3 APPROACH (S3)               ║
╠═══════════════════════════╬═══════════════════════════════════════╣
║  my-plan/                 ║  my-project/                          ║
║  ├── _overview.md         ║  ├── node.yaml                        ║
║  ├── plan.yaml            ║  ├── contract.yaml                    ║
║  │                        ║  ├── README.md                        ║
║  ├── feature_auth/        ║  │                                    ║
║  │   ├── _overview.md     ║  ├── phases/            (generated)   ║
║  │   ├── 01_login.md      ║  │   ├── P0-skeleton.yaml             ║
║  │   └── 02_tokens.md     ║  │   └── P1-features.yaml             ║
║  │                        ║  │                                    ║
║  ├── p00_setup/           ║  ├── combat-system/                   ║
║  │   ├── _overview.md     ║  │   ├── node.yaml                    ║
║  │   └── 01_deps.md       ║  │   ├── contract.yaml                ║
║  │                        ║  │   ├── damage-calc.md    (L3)       ║
║  └── update_readme.md     ║  │   └── damage-calc.spec.md (L4)     ║
║                           ║  │                                    ║
║  (no state dir)           ║  └── state/             (machine)     ║
║                           ║      ├── execution.json               ║
║                           ║      └── history.json                 ║
╚═══════════════════════════╩═══════════════════════════════════════╝
```

### Key Differences

| Aspect | Skills (S1+S2) | DREAM_v3 (S3) |
|--------|---------------|----------------|
| **Plan metadata** | `plan.yaml` (3 lines: name, magnitude, status) or frontmatter in `_overview.md` | `node.yaml` (~15 lines) + `contract.yaml` (~40 lines) |
| **Navigator** | `_overview.md` (mandatory per directory) | `README.md` (informational) |
| **Phase layout** | `pNN_name/` directories inline in plan | `phases/` folder at project root, YAML aggregated |
| **Leaf detail** | Single `.md` task file | `.md` (L3) + optional `.spec.md` (L4) |
| **Level naming** | None — nesting depth is the level | Explicit L0–L4 labels |
| **State tracking** | Status markers in documents | `state/` directory with JSON |
| **Task frontmatter** | `name`, `magnitude`, `status` | Full routing in `node.yaml`, execution in `contract.yaml` |

> **DECISION NEEDED:** The filesystem structure is the most significant conflict. Choose:
> - **(A)** **Skills model** — `_overview.md` + `plan.yaml`, no `node.yaml`/`contract.yaml`, no `state/` dir. Simpler, lower overhead, what the templates already generate.
> - **(B)** **DREAM_v3 model** — `node.yaml` + `contract.yaml` + `state/`, explicit L0-L4. More structured, better for tooling/automation.
> - **(C)** **Hybrid** — Use skills' `_overview.md` as navigator but add optional `contract.yaml` for tasks needing formal acceptance criteria. Keep `plan.yaml` over `node.yaml`.

### Blueprint Folder Structure (S2 — Current Templates)

```
.agent_plan/day_dream/
├── _overview.md                    ← Root navigator
├── {plan_name}/
│   ├── _overview.md                ← Mandatory navigator
│   ├── plan.yaml                   ← Metadata (name, magnitude, status)
│   ├── executive_summary.md        ← Vision, goals, non-goals
│   ├── architecture.md             ← System diagrams
│   ├── implementation.md           ← Phase tracking
│   ├── module_structure.md         ← Module organization
│   ├── cli_commands.md             ← If plan has CLI commands
│   │
│   ├── p00_{name}/                 ← Phase directory
│   │   ├── _overview.md
│   │   ├── 01_{task}.md
│   │   └── 02_{task}.md
│   ├── p01_{name}/                 ← Phase directory
│   │   ├── _overview.md
│   │   └── 01_{task}.md
│   │
│   └── assets/                     ← Supporting artifacts
│       └── {id}_{desc}.asset.md
│
├── exploration/                    ← Research/exploration docs
│   └── _archive/
└── templates/                      ← Template scaffolds
```

### Phase Naming Convention (S2)

- Directories: `pNN_{name}/` — zero-padded, e.g. `p00_prerequisites/`, `p01_core/`
- Tasks within: `NN_{task}.md` — numbering starts at `01_` (position `00` is `_overview.md`)
- Phases MUST always be directories (even single-task phases)

> **DECISION NEEDED:** The day-dream skill explicitly states: *"Phases MUST always be directories...This overrides the general DREAM 'flatten single-child' guidance."* The dream-planning skill says: *"A plan with only 1 child is suspicious — flatten it."*
> - **(A)** Phase directories are always directories (day-dream's rule) — override the flatten guidance for phases specifically
> - **(B)** Flatten single-child plans unconditionally (dream-planning's rule) — including phases
> - **(C)** Keep both rules: flatten general plans, but phases are the exception

### `_overview.md` Required Content (S1)

Every plan directory MUST have `_overview.md` containing:

| Section | Purpose |
|---------|---------|
| **Purpose** | Why this plan exists (2-3 sentences) |
| **Children** | Table: Name, Type, Magnitude, Status, Description |
| **Integration Map** | How children's outputs combine |
| **Reading Order** | Numbered list with dependency notes |

---

## 7. Document Authoring

*Primary source: S2 (day-dream skill)*

### The Story → Spec Pattern

Every blueprint document follows:

```markdown
## 📖 The Story
{Visual, scannable narrative — NOT prose}

---

## 🔧 The Spec
{Technical specification}
```

### Story Section Structure (Visual-First)

| Subsection | Purpose | Format |
|------------|---------|--------|
| 😤 **The Pain** | What's broken, who hurts | ASCII box + pain table |
| ✨ **The Vision** | What success looks like | ASCII box showing flow |
| 🎯 **One-Liner** | Elevator pitch | Single blockquote |
| 📊 **Impact** | Before/After metrics | Comparison table |

> **Principle:** If you can't draw the pain and vision, you don't understand the feature.

### Status Syntax

> **DECISION NEEDED:** DREAM_v3 and the skills use different status vocabulary:
>
> | Skills (S1+S2) | DREAM_v3 (S3) | Meaning |
> |---------------|---------------|---------|
> | ⏳ `[TODO]` | `PENDING` | Not started |
> | 🔄 `[WIP]` | `IN_PROGRESS` | In progress |
> | ✅ `[DONE]` | `DONE` | Complete |
> | 🚧 `[BLOCKED:reason]` | `BLOCKED` | Stuck |
> | 🚫 `[CUT]` | *(none)* | Removed from scope |
>
> - **(A)** Use skills' emoji+text format (more scannable, has `[CUT]`)
> - **(B)** Use DREAM_v3's plain text (more machine-parsable)
> - **(C)** Support both — emoji for human docs, plain text in YAML files

### Difficulty Labels

| Label | Meaning | P0 Allowed? |
|-------|---------|-------------|
| `[KNOWN]` | Standard patterns, proven libraries | ✅ Yes |
| `[EXPERIMENTAL]` | Needs validation in our context | ⚠️ Conditional |
| `[RESEARCH]` | Active problem, no proven solution | ❌ NEVER in P0 |

### Blueprint Document Rules

| Document | Required When | Line Limit |
|----------|---------------|------------|
| `_overview.md` | Every plan directory | ≤100 lines |
| `executive_summary.md` | Blueprint tier | ≤150 lines |
| `architecture.md` | ≥3 modules OR cross-module OR external APIs | ≤200 lines |
| `implementation.md` | Blueprint tier | ≤200 lines/phase |
| `module_structure.md` | ADHD projects | ≤150 lines |
| `cli_commands.md` | Plan has CLI commands | ≤150 lines |
| Feature (full) | ≥3 modules, external APIs, P0 priority | ≤300 lines |
| Feature (simple) | ≤2 modules, no external APIs | ≤100 lines |
| Task | Any leaf task | ≤100 lines |
| Asset | Supporting artifact | ≤100 lines (excl. diagrams) |

### Executive Summary Requirements

- **TL;DR:** Maximum 3 sentences
- **Prior Art & Existing Solutions:** REQUIRED — must include BUY/BUILD/WRAP decisions
- **Non-Goals:** Minimum 3 items
- **Features:** Maximum 5 P0 features
- **Freeze:** Mark 🔒 FROZEN after approval

### Natural Verification (S2)

Every implementation phase MUST have a "How to Verify (Manual)" section:
- Max 3 human-executable steps
- Expected outcome for each step
- Steps must complete in <30 seconds

### Custom Sections (FREE ZONE)

- **Prefix:** `## [Custom] 🎨 Title`
- **Maximum:** 5 per document
- **Prohibited content:** P0 tasks, blocking dependencies, architecture changes

### Deep Dive Section (Optional)

Add `## 🔬 Deep Dive` when algorithms, API contracts, or error handling need explicit design. Delete for straightforward features.

---

## 8. Agent Protocol

### Bootstrap Sequence

> **DECISION NEEDED:** The two systems define different bootstrap sequences:
>
> **Skills (S1):**
> ```
> 1. Enter directory
> 2. Read _overview.md
> 3. Process children (in stated reading order)
> ```
>
> **DREAM_v3 (S3):**
> ```
> 1. Read DREAM_AGENT_CARD.md    (protocol rules)
> 2. Read node.yaml              (routing decision)
> 3. Read contract.yaml          (execution spec)
> 4. Read parent contract.yaml   (boundary check)
> 5. Decide WORKER or MANAGER
> 6. Execute lifecycle
> ```
>
> - **(A)** Skills' approach — simpler, `_overview.md` serves as the entry point
> - **(B)** DREAM_v3's approach — more explicit, separates routing from execution
> - **(C)** Merge — Read `_overview.md` first (contains plan.yaml metadata), then check parent's `_overview.md` for boundaries

### MANAGER Lifecycle (Agreed by S1 + S3)

```
DECOMPOSE  → Verify/create children with _overview.md
             (S3 adds: verify node.yaml + contract.yaml)
     │
     ▼
DELEGATE   → Assign each child to a subagent
             Max 5 parallel subagents
             Context boundaries: sibling firewall applies
     │
     ▼
INTEGRATE  → Collect results, merge outputs
             Resolve conflicts between siblings
             (S3 adds: aggregate phase_contributions → phases/*.yaml)
     │
     ▼
REPORT     → Mark plan status = DONE, notify parent
```

**MANAGER rules:**
- MUST create `_overview.md` if missing
- MUST NOT fulfill children's tasks directly — delegate
- MUST integrate: no child output is final until parent accepts
- Max 5 parallel subagents

### WORKER Lifecycle (Agreed by S1 + S3)

```
VALIDATE   → Check magnitude ≠ Epic (else refuse + escalate)
             Check dependencies resolved
     │
     ▼
IMPLEMENT  → Read task spec, create/modify artifacts
             DO NOT modify sibling tasks
     │
     ▼
VERIFY     → Check acceptance criteria
             (S3: check against contract.yaml)
     │
     ▼
REPORT     → Mark task status = DONE, notify parent
```

### Context Isolation — Sibling Firewall (Agreed by S1 + S3)

| Scope | What Agent Can See |
|-------|-------------------|
| **Read** | Own task/plan + all ancestors up to root + skill files |
| **Write** | Own task/plan ONLY |
| **Sibling status** | Yes — via parent's `_overview.md` |
| **Sibling content** | **NO — NEVER** |

### Parallel Execution Safety

| Scenario | Parallel Safe? | Reason |
|----------|---------------|--------|
| Siblings with no shared writes | ✅ Yes | No race conditions |
| Siblings needing parent state | ❌ No | Sequential — parent integrates |
| Workers on independent branches | ✅ Yes | No shared ancestors modified |

### Subagent Dispatch

> **DECISION NEEDED:** DREAM_v3 defines a formal YAML dispatch message format:
> ```yaml
> action: SPAWN_WORKER
> target_node: "combat-system/damage-calculator.md"
> required_reading:
>   - "day_dream/DREAM_AGENT_CARD.md"
>   - "combat-system/contract.yaml"
> permissions:
>   read: [self, ancestors, project_codebase]
>   write: [self]
> on_complete: NOTIFY_PARENT
> ```
> The skills describe the same concept informally (delegate to subagent with context boundaries).
> - **(A)** Keep formal YAML dispatch (useful for tooling/automation)
> - **(B)** Drop it — too verbose for current agent tooling
> - **(C)** Simplify — keep `target_node` + `permissions` only

### Human vs AI Routing (S3)

| Route to HUMAN | Route to AI |
|----------------|-------------|
| Goal alignment ("is this right?") | Goal execution ("build this") |
| Acceptance testing | Unit/integration tests |
| Novel domain knowledge | Standard patterns |
| Subjective quality (UX, aesthetics) | Objective quality (lint, compile) |

---

## 9. Templates Reference

All templates at: `.agent_plan/day_dream/templates/`

### Simple Tier

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `simple.template.md` | Single-file vision + quick start | ≤200 lines |

### Blueprint Tier

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `blueprint/overview.template.md` | `_overview.md` scaffold — plan navigator | ≤100 lines |
| `blueprint/task.template.md` | Leaf task scaffold — atomic work unit | ≤100 lines |
| `blueprint/00_index.template.md` | Navigation hub with flowchart | ≤150 lines |
| `blueprint/01_executive_summary.template.md` | Vision, goals, non-goals | ≤150 lines |
| `blueprint/02_architecture.template.md` | System diagrams, components | ≤200 lines |
| `blueprint/NN_feature.template.md` | Full feature spec | ≤150 lines |
| `blueprint/NN_feature_simple.template.md` | Lightweight feature (80% of cases) | ≤100 lines |
| `blueprint/80_implementation.template.md` | Phased roadmap | ≤200 lines/phase |
| `blueprint/81_module_structure.template.md` | Reusable vs project-specific modules | ≤150 lines |
| `blueprint/82_cli_commands.template.md` | CLI interface reference | ≤150 lines |
| `blueprint/99_references.template.md` | External links | No limit |
| `blueprint/exploration.template.md` | Research/exploration doc | — |
| `blueprint/modules/module_spec.template.md` | Detailed module implementation spec | ≤200 lines |

### Assets

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `assets/asset.template.md` | Non-code artifacts (mockups, diagrams) | ≤100 lines (excl. diagrams) |

**Asset Types:** `mockup` · `diagram` · `storyboard` · `infrastructure` · `design` · `data-model` · `other`  
**Naming:** `{feature_id}_{description}.asset.md`

### Template Selection Quick Guide

```
What are you creating?
  │
  ├── Quick vision, ≤2 features? ──────► simple.template.md
  │
  ├── Plan directory navigator? ────────► blueprint/overview.template.md
  │
  ├── Leaf task? ───────────────────────► blueprint/task.template.md
  │
  ├── Feature spec?
  │   ├── ≤2 modules, no ext API? ──────► NN_feature_simple.template.md
  │   └── ≥3 modules or ext API? ───────► NN_feature.template.md
  │
  ├── Architecture overview? ───────────► 02_architecture.template.md
  │
  ├── Implementation roadmap? ──────────► 80_implementation.template.md
  │
  └── Supporting artifact? ─────────────► assets/asset.template.md
```

### DREAM_v3 Template Files (S3 — Not in current templates/)

| File | Purpose | Status |
|------|---------|--------|
| `.templates/node.template.yaml` | Routing metadata | S3 only — not in day-dream templates |
| `.templates/contract.template.yaml` | Execution specification | S3 only |
| `.templates/phase.template.yaml` | Cross-cutting phase scope | S3 only |
| `.templates/module.template.md` | L3 module specification | S3 only |
| `.templates/spec.template.md` | L4 implementation detail | S3 only |

> **DECISION NEEDED:** DREAM_v3 references its own `.templates/` directory with `node.template.yaml`, `contract.template.yaml`, etc. These don't exist in the current `day_dream/templates/` folder. Do you want to:
> - **(A)** Port them into the main templates folder (alongside blueprint templates)
> - **(B)** Deprecate them in favor of `plan.yaml` + task frontmatter from the skills
> - **(C)** Keep them separate for projects that want the full DREAM_v3 schema

### Examples

Located at `templates/examples/`:

| Example | Demonstrates |
|---------|-------------|
| `blueprint_example/` | Complete blueprint folder structure |
| `simple_example.md` | Completed simple-tier document |
| `deep_dive_*.example.md` | Algorithm proof, API contract, architecture, state machine |
| `free_zone_*.example.md` | Assumption graveyard, metaphor map, philosophical tensions |

---

## 10. Estimation

*Source: S2 (day-dream skill). S3 provides compatible time ranges.*

All durations use **AI-agent time** unless marked `human_only: true`.

| Magnitude | AI-Agent Time | Human Time (ref only) |
|-----------|---------------|----------------------|
| Trivial | 5–15 min | 1–2 hours |
| Light | 15–60 min | 2–8 hours |
| Standard | 1–4 hours | 1–3 days |
| Heavy | 4–8 hours | 3–7 days |
| Epic | Must decompose | Must decompose |

### P0 Hard Limits (S2)

| Constraint | Limit |
|------------|-------|
| Total AI-agent time | 2–8 hours |
| Max tasks | 5 |
| Difficulty allowed | `[KNOWN]` only |
| `[RESEARCH]` in P0 | ❌ NEVER |

### `human_only: true` Flag

| Scenario | Time Scale |
|----------|-----------|
| Code generation, refactoring, file creation | AI-agent time (default) |
| Goal alignment decisions | Human time |
| Subjective quality (UX, aesthetics) | Human time |
| Novel domain knowledge not in codebase | Human time |
| Acceptance testing with real users | Human time |

---

## 11. Conflicts & Decisions

Summary of all identified conflicts between the three sources. Each requires a user decision.

| # | Conflict | Options | Section |
|---|----------|---------|---------|
| **C1** | **Filesystem metadata** — Skills use `plan.yaml` (3 lines) vs DREAM_v3 uses `node.yaml` + `contract.yaml` (~55 lines) | A: Skills' simple model / B: DREAM_v3's full model / C: Hybrid | [§6](#6-filesystem-structure) |
| **C2** | **Level hierarchy** — Skills use implicit filesystem nesting vs DREAM_v3 uses explicit L0-L4 labels | A: Drop levels / B: Keep levels / C: Optional level annotation | [§3](#3-core-concepts) |
| **C3** | **Status markers** — Skills use emoji+text (`⏳ [TODO]`) vs DREAM_v3 uses plain text (`PENDING`) | A: Emoji / B: Plain / C: Both (emoji in docs, plain in YAML) | [§7](#7-document-authoring) |
| **C4** | **Agent bootstrap** — Skills: read `_overview.md` first vs DREAM_v3: read `DREAM_AGENT_CARD.md` first | A: Skills / B: DREAM_v3 / C: Merge | [§8](#8-agent-protocol) |
| **C5** | **Phase management** — Skills: `pNN_name/` directories inline vs DREAM_v3: `phases/*.yaml` at project root, aggregated | A: Inline dirs / B: Aggregated YAML / C: Both | [§6](#6-filesystem-structure) |
| **C6** | **State tracking** — Skills: none (status in docs) vs DREAM_v3: `state/` directory with JSON | A: No state dir / B: Keep state dir | [§6](#6-filesystem-structure) |
| **C7** | **Complexity vs difficulty** — DREAM_v3 has Complexity Classes A-D vs Skills have Difficulty Labels | A: Keep both / B: Labels only / C: Merge | [§4](#4-magnitude-routing) |
| **C8** | **Single-child flatten rule** — dream-planning says flatten vs day-dream says phases are always directories | A: Phases always dirs / B: Always flatten / C: Exception for phases | [§6](#6-filesystem-structure) |
| **C9** | **Walking skeleton** — DREAM_v3 implies default-on vs day-dream makes it opt-in | A: Opt-in / B: Default-on | [§5](#5-tier-selection) |
| **C10** | **Spec files** — DREAM_v3 has `.spec.md` (L4 detail) vs Skills have no equivalent | A: Adopt .spec.md / B: Drop it / C: Optional | [§6](#6-filesystem-structure) |
| **C11** | **DREAM_AGENT_CARD.md** — DREAM_v3 requires it vs Skills don't mention it | A: Keep / B: Drop / C: Merge into _overview.md | [§8](#8-agent-protocol) |
| **C12** | **Subagent dispatch format** — DREAM_v3 has formal YAML dispatch vs Skills describe informally | A: Keep formal / B: Drop it / C: Simplify | [§8](#8-agent-protocol) |
| **C13** | **DREAM_v3 templates** — DREAM_v3 references `.templates/` with YAML schemas that don't exist in current template folder | A: Port to templates/ / B: Deprecate / C: Keep separate | [§9](#9-templates-reference) |

---

## 12. Anti-Patterns

Unified from all three sources.

### Decomposition Anti-Patterns (S1 + S3)

| Don't | Do Instead |
|-------|------------|
| Siblings communicating directly | Route through parent's INTEGRATE phase |
| Epic-magnitude leaf task | Decompose into plan with children |
| Skip magnitude assessment | Always assess magnitude first |
| Plan with only 1 child ⚠️ | Flatten — probably a task *(but see C8 for phase exception)* |
| MANAGER fulfilling tasks directly | Delegate to WORKER subagents |
| Agent reading sibling content | Read sibling STATUS only (via parent) |
| Deep nesting (>3 levels) | Flatten or re-scope the decomposition |
| Heavyweight plan.yaml schemas | Keep minimal: name + magnitude + status |
| MANAGER not spawning subagents | MUST spawn subagent for each PENDING child |
| Skipping DREAM_AGENT_CARD.md (S3) | First read for any spawned agent |

### Authoring Anti-Patterns (S2)

| Don't | Do Instead |
|-------|------------|
| Put `[RESEARCH]` in P0 | Defer to P1+ or resolve in exploration |
| Exceed line limits | Split into separate files |
| Edit frozen documents | Create new version or update implementation |
| Have >3 active explorations | Synthesize or abandon oldest |
| Skip verification sections | Always include manual verification steps |
| Use Simple tier for complex projects | Upgrade to Blueprint when threshold met |
| Embed code in assets | Assets are for visuals/planning only |
| Create orphan assets | Always link to parent feature |
| Use human-time estimates for AI tasks | Default to AI-agent time scale |
| Force walking skeleton on all projects | Check trigger criteria first |
| Text-wall Story sections | Use ASCII boxes, tables, emoji anchors |

### Code Quality Anti-Patterns (S2)

| Don't | Do Instead |
|-------|------------|
| Wrap old code in try/catch fallbacks | Delete old code or separate into v1/v2 folders |
| Minimize lines changed over correctness | Prioritize clean, correct code |
| Leave half-migrated paths | Refactor fully — one correct path |

---

*End of DREAM v4 Unified Reference*
*DREAM_v3.md is preserved alongside this file for historical reference.*
