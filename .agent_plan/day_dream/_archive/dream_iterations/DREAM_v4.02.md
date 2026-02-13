# DREAM v4.02 — Unified Planning System Specification

**Version:** 4.02  
**Status:** ✅ Authoritative — supersedes v4.01  
**Updated:** February 2026

---

## TL;DR

**DREAM** (Decomposition Rules for Engineering Atomic Modules) is a protocol for breaking complex work into atomic, parallelizable units that AI agents execute independently. It defines **how to assess complexity** (8-slot magnitude routing), **how to structure plans** (filesystem hierarchy with `_overview.md` convention), and **how agents coordinate** (sibling firewall + MANAGER/WORKER lifecycle). Metadata lives in `_overview.md` frontmatter — no YAML sidecar files.

**What changed from v4.01:** 8-slot maximum system, human-initiated planning, conditional doc merge for procedure plans, structure-first document ordering, explicit System/Procedure profiles.

---

## Table of Contents

1. [Quick Reference Card](#quick-reference-card)
2. [Folder Structure — The Main Event](#folder-structure--the-main-event)
3. [How Variables Shape the Structure](#how-variables-shape-the-structure)
4. [Chapter 1 — Author](#chapter-1--author)
5. [Chapter 2 — Execute & Verify](#chapter-2--execute--verify)
6. [Templates Reference](#templates-reference)
7. [Anti-Patterns](#anti-patterns)
8. [Deprecated (v3 → v4.02)](#deprecated-v3--v402)

---

## Quick Reference Card

| Concept | Rule |
|---------|------|
| **Plan** | Directory with `_overview.md` — decomposable, has children |
| **Task** | Single `.md` file — leaf, directly executable |
| **Bridge** | Plan = dir, Task = file. That's the only two primitives |
| **Metadata** | YAML frontmatter in `_overview.md` (name, magnitude, status) |
| **Status markers** | ⏳`[TODO]` · 🔄`[WIP]` · ✅`[DONE]` · 🚧`[BLOCKED:reason]` · 🚫`[CUT]` |
| **Difficulty labels** | `[KNOWN]` · `[EXPERIMENTAL]` · `[RESEARCH]` (never in P0) |
| **Magnitudes** | Trivial(1) · Light(2) · Standard(3) · Heavy(5) · Epic(8) — slot MAXIMUMS |
| **Tiers** | Simple (≤2 features, no APIs) · Blueprint (≥3 features OR cross-module OR external APIs) |
| **Plan types** | System Plan (architecture + features) · Procedure Plan (workflow + steps) |
| **Levels** | L0–LN optional communication aids. L0=plan, L1=sub-plan covers 95% |
| **Sibling firewall** | Siblings **NEVER** read/write each other's content. Coordinate through parent only |
| **MANAGER** | DECOMPOSE → DELEGATE → INTEGRATE → REPORT |
| **WORKER** | VALIDATE → IMPLEMENT → VERIFY → REPORT |
| **Max parallel agents** | 5 |
| **P0 hard limits** | Max 5 tasks, `[KNOWN]` only, ≤5 slots |
| **Walking skeleton** | Opt-in — required only when cross-boundary, external API, or 3+ module flow |
| **Human authority** | Human decides WHETHER to plan. DREAM decides the FORMAT |
| **Omit, don't N/A** | Optional files don't exist on disk — not filled with "N/A" |

### Slot System — 8-Slot Visual Scale

Each slot ≈ 1 hour AI-agent time. Values are **MAXIMUMS** — actual work can be lower.

```
Trivial   ■□□□□□□□  max 1 slot
Light     ■■□□□□□□  max 2 slots
Standard  ■■■□□□□□  max 3 slots
Heavy     ■■■■■□□□  max 5 slots
Epic      ■■■■■■■■  max 8 slots (MUST decompose)
```

| Magnitude | Max Slots | Action | AI-Agent Time |
|-----------|-----------|--------|---------------|
| **Trivial** | 1 | Execute immediately | ≤1 hour |
| **Light** | 2 | Execute directly | ≤2 hours |
| **Standard** | 3 | Decompose if ≥3 subtasks | ≤3 hours |
| **Heavy** | 5 | **SHOULD** decompose | ≤5 hours |
| **Epic** | 8 | **MUST** decompose | ≤8 hours |

### Planning Authority

```
┌──────────────────────────────────────────────────────────┐
│  WHO DECIDES WHAT                                        │
│                                                          │
│  Human  ──► WHETHER to plan (yes/no)                     │
│  DREAM  ──► HOW to plan (folder vs file, which docs)     │
│                                                          │
│  Human override suppresses auto-format-detection.        │
│  Agents do NOT decide whether planning happens.          │
└──────────────────────────────────────────────────────────┘
```

---

## Folder Structure — The Main Event

> **Bridge:** Every DREAM artifact is either a **Plan** (directory with `_overview.md`) or a **Task** (single `.md` file). The folder tree below shows how these two primitives compose into real projects.

### Full Blueprint — System Plan

A System Plan describes **what to build** — architecture, modules, features, and phased implementation. Architecture stabilizes early while the summary evolves, so they are separate files.

```
.agent_plan/day_dream/
├── _overview.md                         ← Root navigator
│
├── {plan_name}/                         ← Named plan directory
│   ├── _overview.md                     ← REQUIRED — plan navigator (frontmatter metadata)
│   ├── 01_executive_summary.md          ← Vision, goals, non-goals, prior art
│   ├── 02_architecture.md               ← System diagrams, components (stabilizes early)
│   ├── 0N_{feature_name}.md             ← Feature specs (one per feature)
│   ├── 80_implementation.md             ← Phased roadmap with verification
│   ├── 81_module_structure.md           ← Reusable vs project-specific modules
│   ├── 82_cli_commands.md               ← CLI interface (if applicable)
│   ├── 99_references.md                 ← External links
│   │
│   ├── p00_{phase}/                     ← Phase directory (sequential)
│   │   ├── _overview.md                 ← REQUIRED
│   │   ├── 01_{task}.md                 ← Numbered task files
│   │   └── 02_{task}.md
│   ├── p01_{phase}/
│   │   ├── _overview.md
│   │   └── 01_{task}.md
│   │
│   ├── modules/                         ← Module specs (if needed)
│   │   └── {module_name}.md
│   │
│   └── assets/                          ← Supporting artifacts
│       └── {id}_{desc}.asset.md
│
├── exploration/                         ← Research/exploration docs
│   └── _archive/
└── templates/                           ← Template scaffolds (read-only)
```

### Full Blueprint — Procedure Plan

A Procedure Plan describes **how to do something** — a workflow, migration, or operational process. Summary and architecture co-evolve and are lightweight, so they merge into a single file.

```
.agent_plan/day_dream/
├── _overview.md                         ← Root navigator
│
├── {plan_name}/                         ← Named plan directory
│   ├── _overview.md                     ← REQUIRED — plan navigator (frontmatter metadata)
│   ├── 01_summary.md                    ← Merged: vision + architecture (co-evolve)
│   ├── 0N_{step_name}.md               ← Step/stage specs
│   ├── 80_implementation.md             ← Phased roadmap with verification
│   ├── 99_references.md                 ← External links
│   │
│   ├── p00_{phase}/                     ← Phase directory (sequential)
│   │   ├── _overview.md
│   │   └── 01_{task}.md
│   │
│   └── assets/                          ← Supporting artifacts (if needed)
│       └── {id}_{desc}.asset.md
│
├── exploration/
│   └── _archive/
└── templates/
```

**What Procedure Plans OMIT (files don't exist on disk):**

| File | Why Omitted |
|------|-------------|
| `02_architecture.md` | Merged into `01_summary.md` |
| `81_module_structure.md` | Procedures rarely define new modules |
| `82_cli_commands.md` | Procedures rarely define new CLI commands |
| `modules/` directory | No module specs needed |

### Simple Tier (Either Type)

```
.agent_plan/day_dream/
├── {project}_vision.md                  ← Single file, ≤200 lines
└── templates/
```

---

## How Variables Shape the Structure

Three variables modify what appears on disk: **Magnitude**, **Tier**, and **Plan Type**. Each adds or removes files/directories from the full blueprint shown above.

### Variable 1: Magnitude → Controls Decomposition Depth

Magnitude determines HOW DEEP the plan tree goes. Higher magnitude = more structure.

#### Trivial (■□□□□□□□ max 1 slot)

No planning artifacts. Execute immediately.

```
(no files created — work happens inline)
```

#### Light (■■□□□□□□ max 2 slots)

Optional single file. No directory structure.

```
.agent_plan/day_dream/
└── {task}_vision.md          ← Optional, only if documentation value exists
```

#### Standard (■■■□□□□□ max 3 slots)

Plan directory appears if ≥3 subtasks or cross-module. Tasks live directly in plan directory (no phases).

```
{plan_name}/
├── _overview.md
├── 01_executive_summary.md   ← System Plan
│   (or 01_summary.md)        ← Procedure Plan
├── 80_implementation.md
├── 01_{task}.md
├── 02_{task}.md
└── 03_{task}.md
```

#### Heavy (■■■■■□□□ max 5 slots)

Full blueprint with phase directories. Should decompose.

```
{plan_name}/
├── _overview.md
├── 01_executive_summary.md
├── 02_architecture.md         ← System Plan only
├── 03_{feature}.md
├── 80_implementation.md
├── 81_module_structure.md     ← System Plan only
├── p00_{phase}/
│   ├── _overview.md
│   ├── 01_{task}.md
│   └── 02_{task}.md
├── p01_{phase}/
│   ├── _overview.md
│   └── 01_{task}.md
└── assets/
```

#### Epic (■■■■■■■■ max 8 slots — MUST decompose)

Full blueprint with nested plan directories inside phases. Mandatory decomposition with parallel agents.

```
{plan_name}/
├── _overview.md
├── 01_executive_summary.md
├── 02_architecture.md         ← System Plan only
├── 03_{feature_a}.md
├── 04_{feature_b}.md
├── 80_implementation.md
├── 81_module_structure.md     ← System Plan only
├── 82_cli_commands.md         ← If CLI exists
├── 99_references.md
├── p00_{phase}/
│   ├── _overview.md
│   ├── {sub_plan}/            ← Nested plan (parallel-safe)
│   │   ├── _overview.md
│   │   ├── 01_{task}.md
│   │   └── 02_{task}.md
│   └── 01_{task}.md
├── p01_{phase}/
│   ├── _overview.md
│   └── ...
├── modules/
│   ├── {module_a}.md
│   └── {module_b}.md
└── assets/
    └── {id}_{desc}.asset.md
```

### Variable 2: Tier → Controls Documentation Depth

Tier determines WHAT KIND of documentation is created.

| Tier | Trigger | Structure |
|------|---------|-----------|
| **Simple** | ≤2 features, single module, no external APIs | Single `.md` file |
| **Blueprint** | ≥3 features OR ≥2 cross-module deps OR external APIs | Plan directory with structured docs |

```
Simple:
  └── {name}_vision.md               ← Everything in one file

Blueprint:
  └── {name}/                         ← Directory with structured files
      ├── _overview.md
      ├── 01_executive_summary.md     ← (or 01_summary.md for Procedure)
      ├── ...
      └── 80_implementation.md
```

**Human requests planning → DREAM selects tier based on scope.** Human override can force Simple or Blueprint.

### Variable 3: Plan Type → Controls Which Files Exist

One folder structure, two template profiles. The primitives are identical — only which files appear on disk differs.

| File | System Plan | Procedure Plan | Why |
|------|:-----------:|:--------------:|-----|
| `_overview.md` | ✅ | ✅ | Always required |
| `01_executive_summary.md` | ✅ | — | Replaced by `01_summary.md` |
| `01_summary.md` | — | ✅ | Merged exec summary + architecture |
| `02_architecture.md` | ✅ | — | Merged into `01_summary.md` |
| `0N_{feature}.md` | ✅ | ✅ | Feature/step specs |
| `80_implementation.md` | ✅ | ✅ | Always needed |
| `81_module_structure.md` | ✅ | — | Procedures rarely define modules |
| `82_cli_commands.md` | Optional | — | Only if CLI exists |
| `99_references.md` | Optional | Optional | External links |
| `modules/` | Optional | — | Module specs |
| `assets/` | Optional | Optional | Supporting artifacts |
| `pNN_{phase}/` | As needed | As needed | Phase directories |

### Combo Examples

Here are concrete examples showing how the three variables combine:

#### Example A: Simple + Light + System

*"Add retry logic to the HTTP client"*

```
.agent_plan/day_dream/
└── http_retry_vision.md       ← Single file (or no file at all)
```

#### Example B: Blueprint + Standard + System

*"Add OAuth2 support with 3 providers"*

```
.agent_plan/day_dream/oauth2/
├── _overview.md
├── 01_executive_summary.md
├── 02_architecture.md
├── 03_google_provider.md
├── 04_github_provider.md
├── 05_custom_provider.md
└── 80_implementation.md
```

#### Example C: Blueprint + Heavy + Procedure

*"Migrate all modules from pip to uv"*

```
.agent_plan/day_dream/uv_migration/
├── _overview.md
├── 01_summary.md              ← Merged (procedure = co-evolving summary + arch)
├── 03_foundation_modules.md
├── 04_runtime_modules.md
├── 05_dev_modules.md
├── 80_implementation.md
├── p00_prerequisites/
│   ├── _overview.md
│   ├── 01_install_uv.md
│   └── 02_audit_deps.md
├── p01_foundation/
│   ├── _overview.md
│   ├── 01_config_manager.md
│   └── 02_logger_util.md
└── p02_runtime/
    ├── _overview.md
    └── 01_remaining_modules.md
```

#### Example D: Blueprint + Epic + System

*"Build a plugin system with marketplace and sandboxing"*

```
.agent_plan/day_dream/plugin_system/
├── _overview.md
├── 01_executive_summary.md
├── 02_architecture.md
├── 03_plugin_loader.md
├── 04_sandbox_runtime.md
├── 05_marketplace_api.md
├── 80_implementation.md
├── 81_module_structure.md
├── 82_cli_commands.md
├── 99_references.md
├── p00_walking_skeleton/
│   ├── _overview.md
│   ├── 01_plugin_interface.md
│   └── 02_loader_stub.md
├── p01_core_features/
│   ├── _overview.md
│   ├── sandbox/
│   │   ├── _overview.md
│   │   ├── 01_process_isolation.md
│   │   └── 02_resource_limits.md
│   └── 01_dependency_resolver.md
├── p02_marketplace/
│   ├── _overview.md
│   └── 01_api_endpoints.md
├── modules/
│   ├── plugin_loader.md
│   └── sandbox_runtime.md
└── assets/
    ├── 03_plugin_lifecycle_diagram.asset.md
    └── 04_sandbox_architecture.asset.md
```

---

## Chapter 1 — Author

This chapter answers: *"How do I write plan documents?"*

### 1.1 Magnitude Assessment

Assess magnitude **first**. This is agent judgment, not a rigid checklist.

| Signal | Points Toward |
|--------|--------------|
| Single file change | Trivial/Light |
| Multiple files, one module | Light/Standard |
| Cross-module changes | Standard/Heavy |
| New module or external API | Heavy/Epic |
| Ambiguity in requirements | Standard+ (needs decomposition) |

### 1.2 Routing Decision

```
Is magnitude Epic?            ──YES──► MUST decompose (MANAGER role)
                                │
Is magnitude Heavy?            ──YES──► SHOULD decompose (MANAGER role)
                                │
Is magnitude Standard          ──YES──► Decompose if ≥3 subtasks
  AND ≥3 subtasks?                      or cross-module. Otherwise execute.
                                │
Trivial or Light?              ──YES──► Execute directly (WORKER role)
```

Epic at task level → **REFUSE and escalate**. Epic work cannot be a leaf task.

### 1.3 Tier Selection

DREAM selects tier **after human initiates planning**:

| Tier | Use When | Template |
|------|----------|----------|
| **Simple** | ≤2 features, single module, no external APIs | `simple.template.md` |
| **Blueprint** | ≥3 features OR ≥2 cross-module deps OR external APIs | `blueprint/` folder |

Format detection signals (used by DREAM to pick tier):

| Condition | Threshold | Tier |
|-----------|-----------|------|
| Feature count | ≥3 | Blueprint |
| Cross-module imports | ≥2 | Blueprint |
| External API | Any | Blueprint |

Human override can force tier in either direction.

### 1.4 Plan Type Selection

| Plan Type | Use When | Key Difference |
|-----------|----------|----------------|
| **System Plan** | Building/extending software architecture | Separate `01_executive_summary.md` + `02_architecture.md` |
| **Procedure Plan** | Workflow, migration, operational process | Merged `01_summary.md` (exec + arch co-evolve) |

Both types share the same primitives: `_overview.md`, status markers, magnitude, sibling firewall, phase directories, task files.

### 1.5 Tier × Magnitude Matrix

| Combo | Route |
|-------|-------|
| Simple + Trivial/Light | Execute directly — no planning doc |
| Simple + Standard | Single plan file, execute in-session |
| Blueprint + Light/Standard | Blueprint docs, execute sequentially |
| Blueprint + Heavy | Blueprint docs, decompose into plan/task tree |
| Blueprint + Epic | Blueprint docs, mandatory decomposition, parallel agents |

### 1.6 Human vs AI Routing

| Route to **Human** | Route to **AI** |
|--------------------|-----------------|
| Goal alignment ("is this right?") | Goal execution ("build this") |
| Acceptance testing with real users | Unit/integration tests |
| Novel domain knowledge not in codebase | Standard patterns |
| Subjective quality (UX, aesthetics) | Objective quality (lint, compile) |

Mark human-routed tasks with `human_only: true` in frontmatter. These use human time estimates.

### 1.7 Walking Skeleton Policy

Walking skeleton is **opt-in** — not every project needs one.

| **When REQUIRED** (opt-in triggers) | **When NOT needed** (skip) |
|--------------------------------------|----------------------------|
| Cross-boundary integration risk | Single-module changes |
| External API dependency | Skill/template/doc edits |
| Multi-module data flow (3+ modules) | Self-contained features |
| | Magnitude ≤ Light |

### 1.8 The Story → Spec Pattern

Every blueprint document **MUST** follow this two-part structure:

```markdown
## 📖 The Story
{Visual, scannable narrative — NOT a text wall}

---

## 🔧 The Spec
{Technical specification}
```

### 1.9 Story Section Structure (Visual-First)

| Subsection | Purpose | Format |
|------------|---------|--------|
| 😤 **The Pain** | What's broken, who hurts | ASCII box + pain table |
| ✨ **The Vision** | What success looks like | ASCII box showing flow |
| 🎯 **One-Liner** | Elevator pitch | Single blockquote |
| 📊 **Impact** | Before/After metrics | Comparison table |

**Principle:** If you can't draw the pain and vision, you don't understand the feature.

### 1.10 Status Syntax

| Marker | Meaning |
|--------|---------|
| ⏳ `[TODO]` | Not started |
| 🔄 `[WIP]` | In progress |
| ✅ `[DONE]` | Complete |
| 🚧 `[BLOCKED:reason]` | Stuck (use kebab-case, e.g., `[BLOCKED:waiting-on-api]`) |
| 🚫 `[CUT]` | Removed from scope |

### 1.11 Difficulty Labels

| Label | Meaning | P0 Allowed? |
|-------|---------|-------------|
| `[KNOWN]` | Standard patterns, proven libraries | ✅ Yes |
| `[EXPERIMENTAL]` | Needs validation in our context | ⚠️ Conditional |
| `[RESEARCH]` | Active problem, no proven solution | ❌ **NEVER** in P0 |

### 1.12 Acceptance Criteria

Task files **MUST** include `## Acceptance Criteria` with checkbox lists:

```markdown
## Acceptance Criteria

- [ ] Login endpoint returns JWT on valid credentials
- [ ] Invalid credentials return 401 with error message
- [ ] Token expires after configured TTL
```

### 1.13 Blueprint Document Rules

| Document | Required When | Line Limit |
|----------|---------------|------------|
| `_overview.md` | Every plan directory | ≤100 lines |
| `01_executive_summary.md` | Blueprint, System Plan | ≤150 lines |
| `01_summary.md` | Blueprint, Procedure Plan | ≤200 lines |
| `02_architecture.md` | System Plan with ≥3 modules/cross-module/ext API | ≤200 lines |
| `80_implementation.md` | Blueprint tier | ≤200 lines per phase |
| `81_module_structure.md` | System Plan, ADHD projects | ≤150 lines |
| `82_cli_commands.md` | Plan has CLI commands | ≤150 lines |
| Feature (full) | ≥3 modules, external APIs, P0 | ≤300 lines |
| Feature (simple) | ≤2 modules, no external APIs | ≤100 lines |
| Task file | Any leaf task | ≤100 lines |
| Asset file | Supporting artifact | ≤100 lines (excl. diagrams) |

### 1.14 `_overview.md` Convention

Every plan directory **MUST** contain `_overview.md`. This is the agent's entry point.

**Required content:**

```markdown
---
name: {plan_name}
magnitude: {Trivial|Light|Standard|Heavy|Epic}
status: {TODO|WIP|DONE|BLOCKED:reason|CUT}
---

# {Plan Name}

## Purpose
Why this plan exists and what it delivers.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_login_flow.md | Task | ⏳ [TODO] | Login endpoint |
| auth_tokens/ | Plan | 🔄 [WIP] | Token lifecycle |

## Integration Map
How children's outputs combine into the plan's deliverable.

## Reading Order
1. 01_login_flow.md (independent)
2. auth_tokens/ (depends on login)
```

### 1.15 Level Annotation (Optional)

Levels are **L0–LN** — optional communication aids with no formal machinery. Use them when referring to plans in discussion. Do **not** encode them in filenames or metadata.

```
project_plan/          ← L0 (root plan)
├── feature_auth/      ← L1 (sub-plan)
│   ├── oauth/         ← L2
│   │   └── task.md    ← L2 (task)
│   └── task.md        ← L1 (task)
└── task.md            ← L0 (task)
```

L0=plan, L1=sub-plan covers 95% of real use cases. Label when useful, ignore when not.

### 1.16 Executive Summary Requirements

| Rule | Detail |
|------|--------|
| **TL;DR** | Maximum 3 sentences |
| **Prior Art** | **MUST** include `## 🔍 Prior Art & Existing Solutions` with BUY/BUILD/WRAP decisions |
| **Non-Goals** | Minimum 3 items |
| **Features** | Maximum 5 P0 features |
| **Freeze** | Mark 🔒 FROZEN after approval — do not edit |

### 1.17 Estimation Defaults

All durations use **AI-agent time** unless marked `human_only: true`.

| Magnitude | Max Slots | AI-Agent Time | Human Time (ref) |
|-----------|-----------|---------------|-------------------|
| Trivial | 1 | ≤1 hour | 1–2 hours |
| Light | 2 | ≤2 hours | 2–8 hours |
| Standard | 3 | ≤3 hours | 1–3 days |
| Heavy | 5 | ≤5 hours | 3–7 days |
| Epic | 8 | ≤8 hours (must decompose) | Must decompose |

### 1.18 P0 Hard Limits

| Constraint | Limit |
|------------|-------|
| Max tasks | 5 |
| Max slots | 5 |
| Difficulty allowed | `[KNOWN]` only |
| `[RESEARCH]` in P0 | ❌ **NEVER** |

**Anti-Premature-Optimization:** If you cannot describe each P0 component in one sentence without the word "and," it's too complex. Split or defer.

### 1.19 Natural Verification

Every implementation phase **MUST** have a `### How to Verify (Manual)` section:

- Max 3 human-executable steps
- Expected outcome for each step
- Steps **MUST** complete in <30 seconds

```markdown
### How to Verify (Manual)

1. Run `adhd list modules` → expect auth_manager in output
2. Run `adhd test auth` → expect all tests pass
3. Check `modules/runtime/auth_manager/__init__.py` exists → expect file present
```

### 1.20 Phasing Rules

| Phase | Constraint |
|-------|-----------|
| **P0 (Walking Skeleton / Foundation)** | Max 5 tasks, max 5 slots, `[KNOWN]` only. Working passthrough/stub. NO complex logic |
| **P1 (First Enhancement)** | Add ONE simple heuristic or feature. Validate before adding more |
| **P2+** | Gradually layer complexity. Each phase independently deployable |

### 1.21 Mandatory Skeleton Pattern (Documents)

Distinct from walking skeleton (code). This governs document sections:

| Old Pattern | New Pattern |
|-------------|-------------|
| `<!-- Optional: ... -->` | Section present; write "N/A — [reason]" if not applicable |

### 1.22 Custom Sections (FREE ZONE)

- **Prefix:** `## [Custom] 🎨 Title`
- **Maximum:** 5 per document
- **Prohibited content:** P0 tasks, blocking dependencies, architecture changes

### 1.23 Deep Dive Section

Add `## 🔬 Deep Dive` only when algorithms, API contracts, or error handling need explicit design. Delete for straightforward features.

### 1.24 Asset Authoring

**Naming:** `{feature_id}_{description}.asset.md`  
**Types:** `mockup` · `diagram` · `storyboard` · `infrastructure` · `design` · `data-model` · `other`

| Section | Limit |
|---------|-------|
| Context | ~20 lines |
| The Artifact | Mermaid diagram, ASCII mockup, etc. |
| Constraints | ~10 lines |
| Related Features | Links to dependent features |
| **Total** (excl. diagrams) | **≤100 lines** |

**Diagram rules:** Mermaid for all supported chart types. ASCII art only when Mermaid does not support the format. Prefer SVG over PNG/JPG.

### 1.25 Exploration Docs

- Maximum **3 active explorations** at any time
- Each expires after **14 days**
- Archived to `exploration/_archive/` when synthesized or expired

### 1.26 Clean-Code-First Directive

Plans **MUST** specify clean, correct code over minimizing edited lines:

1. **Delete wrong code** — do not wrap in fallbacks
2. **Refactor fully** — no half-migrated paths
3. **One correct path** — not `try (new) catch (old)`
4. **Measure success by correctness** — not lines changed

When backward compatibility IS genuinely needed, use folder separation (`v1/`, `v2/`), never try/catch fallbacks.

---

## Chapter 2 — Execute & Verify

This chapter answers: *"How do agents process plans and tasks?"*

### 2.1 Core Primitives

| Primitive | Representation | Has Children? | Required File |
|-----------|---------------|---------------|---------------|
| **Plan** | Directory | Yes | `_overview.md` |
| **Task** | Single `.md` file | No | — |

### 2.2 Bootstrap Sequence

When an agent enters a plan directory:

```
1. Enter directory
2. Read _overview.md              ← frontmatter (metadata) + children + reading order
3. Check parent's _overview.md    ← boundary check: what is my scope?
4. Decide: MANAGER or WORKER
5. Execute appropriate lifecycle
```

### 2.3 MANAGER Lifecycle (Processes a Plan)

```
DECOMPOSE  ──► Verify/create children with _overview.md
               Break ambiguity into concrete children
                              │
                              ▼
DELEGATE   ──► Assign each child to a subagent
               Max 5 parallel subagents
               Apply sibling firewall to each branch
                              │
                              ▼
INTEGRATE  ──► Collect results, merge outputs
               Resolve conflicts between siblings
               No child output is final until parent accepts
                              │
                              ▼
REPORT     ──► Mark plan status = ✅ [DONE]
               Notify parent
```

**MANAGER rules:**

- **MUST** create `_overview.md` if it does not exist
- **MUST NOT** fulfill children's tasks directly — always delegate
- **MUST** integrate: no child output is final until parent accepts
- **MUST** cap at 5 parallel subagents

### 2.4 WORKER Lifecycle (Fulfills a Task)

```
VALIDATE   ──► Check magnitude ≠ Epic (refuse + escalate if Epic)
               Check dependencies are resolved
                              │
                              ▼
IMPLEMENT  ──► Read task spec, create/modify artifacts
               DO NOT modify sibling tasks or parent plan
                              │
                              ▼
VERIFY     ──► Check acceptance criteria
               Run verification steps
                              │
                              ▼
REPORT     ──► Mark task status = ✅ [DONE]
               Notify parent
```

**WORKER rules:**

- **MUST** refuse Epic-magnitude tasks — escalate to parent
- **MUST NOT** modify sibling tasks or parent plan content
- **MUST** report completion to parent (status marker update)

### 2.5 Sibling Firewall

The most critical rule in DREAM. Prevents parallel agents from corrupting each other's context.

| Scope | What Agent Can See |
|-------|-------------------|
| **Read** | Own task/plan + all ancestors up to root + skill files |
| **Write** | Own task/plan **ONLY** |
| **Sibling status** | Yes — via parent's `_overview.md` |
| **Sibling content** | **NO — NEVER** |

### 2.6 Parallel Execution Safety

| Scenario | Parallel Safe? | Reason |
|----------|---------------|--------|
| Siblings with no shared writes | ✅ Yes | No race conditions |
| Siblings needing parent state | ❌ No | Sequential — parent integrates |
| Workers on independent branches | ✅ Yes | No shared ancestors modified |

### 2.7 How Siblings Coordinate

Siblings do **NOT** coordinate directly. The parent MANAGER:

1. Delegates tasks to children
2. Waits for children to report completion
3. Integrates results in its own INTEGRATE phase
4. Resolves any conflicts between sibling outputs

### 2.8 Updating Shared Files

For any request to update a file owned by a higher layer, the agent **MUST** report this to the parent. The parent decides how to proceed.

### 2.9 Subagent Dispatch

Dispatch is **informal** via orchestrator and skills. The MANAGER describes the task, points to the target directory/file, and states context boundaries. No formal YAML dispatch schema.

### 2.10 Flatten Rule

A plan with only 1 child is suspicious — probably a task disguised as a plan. **SHOULD** flatten single-child plans.

**Exception:** Phases (`pNN_name/`) are always directories. This overrides the flatten rule because sequential ordering **MUST** be preserved in file explorers.

### 2.11 Phase Directories

| Rule | Detail |
|------|--------|
| Naming | `pNN_name/` — zero-padded two digits, underscore separator |
| Examples | `p00_prerequisites/`, `p01_core_commands/`, `p02_polish/` |
| Always directories | Even single-task phases. Never flatten phases |
| Task numbering | `NN_task_name.md` starting at `01_` (`00_` is implicitly `_overview.md`) |
| Capacity | Up to `p99_` — more than sufficient for any plan |

### 2.12 When to Stop Decomposing

A unit is a **task** (leaf) when:
- A single agent can fulfill it in a single session
- There is no ambiguity about what to produce
- Its magnitude is Standard or below

A unit is a **plan** (container) when:
- It contains ambiguity requiring further breakdown
- It has ≥2 children that can be worked independently
- Its magnitude is Heavy or Epic

### 2.13 Validation Checklists

**Feature checklist:**

- [ ] Story section clearly states user problem and value
- [ ] Intent is unambiguous to a non-technical reader
- [ ] Scope is explicitly bounded
- [ ] Integration Points table has all connections
- [ ] Edge Cases cover failure scenarios
- [ ] Acceptance Criteria are testable

**Module checklist:**

- [ ] Implements Features section links to ≥1 feature OR marked as utility
- [ ] All linked features have backlinks to this module spec
- [ ] Responsibilities clearly state DO and DON'T
- [ ] Public API section defines interface contract

---

## Templates Reference

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
| `blueprint/01_executive_summary.template.md` | Vision, goals, non-goals, prior art (System Plan) | ≤150 lines |
| `blueprint/01_summary.template.md` | Merged summary + architecture (Procedure Plan) | ≤200 lines |
| `blueprint/02_architecture.template.md` | System diagrams, logical components (System Plan only) | ≤200 lines |
| `blueprint/NN_feature.template.md` | Full feature spec (≥3 modules or ext API) | ≤150 lines |
| `blueprint/NN_feature_simple.template.md` | Lightweight feature (80% of cases) | ≤100 lines |
| `blueprint/80_implementation.template.md` | Phased roadmap with verification | ≤200 lines/phase |
| `blueprint/81_module_structure.template.md` | Reusable vs project-specific modules (System Plan only) | ≤150 lines |
| `blueprint/82_cli_commands.template.md` | CLI interface and command reference | ≤150 lines |
| `blueprint/99_references.template.md` | External links | No limit |
| `blueprint/exploration.template.md` | Research/exploration doc | — |
| `blueprint/modules/module_spec.template.md` | Detailed module implementation spec | ≤200 lines |

### Assets

| Template | Purpose | Line Limit |
|----------|---------|------------|
| `assets/asset.template.md` | Non-code artifacts (mockups, diagrams) | ≤100 lines (excl. diagrams) |

### Template Selection Flowchart

```
What are you creating?
  │
  ├── Quick vision, ≤2 features? ──────────► simple.template.md
  │
  ├── Plan directory navigator? ───────────► blueprint/overview.template.md
  │
  ├── Leaf task? ──────────────────────────► blueprint/task.template.md
  │
  ├── Feature spec?
  │   ├── ≤2 modules, no ext API? ─────────► NN_feature_simple.template.md
  │   └── ≥3 modules or ext API? ──────────► NN_feature.template.md
  │
  ├── System Plan blueprint?
  │   ├── Executive summary ───────────────► 01_executive_summary.template.md
  │   └── Architecture ────────────────────► 02_architecture.template.md
  │
  ├── Procedure Plan blueprint?
  │   └── Summary (merged) ────────────────► 01_summary.template.md
  │
  ├── Implementation roadmap? ─────────────► 80_implementation.template.md
  │
  └── Supporting artifact? ────────────────► assets/asset.template.md
```

### Slot Notation for Implementation Plans

Duration fields in `80_implementation.md` use the 8-slot visual scale:

```
■□□□□□□□  Trivial  (max 1 slot)
■■□□□□□□  Light    (max 2 slots)
■■■□□□□□  Standard (max 3 slots)
■■■■■□□□  Heavy    (max 5 slots)
■■■■■■■■  Epic     (max 8 slots — must decompose)
```

### Examples

Located at `templates/examples/`:

| Example | Demonstrates |
|---------|-------------|
| `blueprint_example/` | Complete blueprint folder structure |
| `simple_example.md` | Completed simple-tier document |
| `deep_dive_*.example.md` | Algorithm proof, API contract, architecture, state machine |
| `free_zone_*.example.md` | Assumption graveyard, metaphor map, philosophical tensions |

---

## Anti-Patterns

### Planning & Authority

| Don't | Do Instead |
|-------|------------|
| Agent decides whether to plan | Human initiates planning; DREAM decides format |
| Force planning on Trivial/Light work | Execute directly — no planning doc |
| Skip magnitude assessment | Always assess magnitude first |

### Decomposition

| Don't | Do Instead |
|-------|------------|
| Siblings communicating directly | Route through parent's INTEGRATE phase |
| Epic-magnitude leaf task | Decompose into plan with children |
| Plan with only 1 child (non-phase) | Flatten — it is probably a task |
| MANAGER fulfilling tasks directly | Delegate to WORKER subagents |
| Agent reading sibling content | Read sibling STATUS only (via parent) |
| Deep nesting (>3 levels) | Flatten or re-scope |

### Authoring

| Don't | Do Instead |
|-------|------------|
| `[RESEARCH]` in P0 | Defer to P1+ or resolve in exploration |
| Exceed line limits | Split into separate files |
| Edit frozen (🔒) documents | Create new version or update implementation |
| >3 active explorations | Synthesize or abandon oldest |
| Skip verification sections | Always include manual verification |
| Simple tier for complex projects | Upgrade to Blueprint when threshold met |
| Embed code in assets | Assets are for visuals/planning only |
| Orphan assets | Always link to parent feature |
| Human-time estimates for AI tasks | Default to AI-agent time scale |
| Force walking skeleton on all projects | Check opt-in triggers first |
| Text-wall Story sections | ASCII boxes, tables, emoji anchors |
| Fill omitted files with "N/A" | Omit the file from disk entirely |

### Code Quality

| Don't | Do Instead |
|-------|------------|
| Wrap old code in try/catch fallbacks | Delete old code or separate into v1/v2 folders |
| Minimize lines changed over correctness | Prioritize clean, correct code |
| Leave half-migrated paths | Refactor fully — one correct path |

---

## Deprecated (v3 → v4.02)

| Removed | Was | Why Deprecated |
|---------|-----|----------------|
| `node.yaml` | Per-node routing metadata (~15 lines) | Replaced by `_overview.md` frontmatter |
| `contract.yaml` | Per-node execution spec (~40 lines) | Acceptance criteria inline in task files |
| `plan.yaml` | Separate 3-line metadata file | Moved into `_overview.md` frontmatter |
| `.spec.md` files | L4 implementation detail | Tasks include `## Acceptance Criteria` directly |
| `state/` directory | Machine-managed JSON (execution, history) | Status lives in document markers |
| `phases/*.yaml` | Aggregated phase files at project root | Phases are `pNN_name/` directories inline |
| `DREAM_AGENT_CARD.md` | Protocol rules file read first by agents | Protocol lives in skills loaded at activation |
| Complexity Classes A–D | Human review gates (Surface→Dense) | Replaced by difficulty labels |
| YAML dispatch schema | Formal subagent spawn messages | Dispatch is informal via orchestrator/skills |
| `.templates/*.yaml` (v3) | YAML template files for nodes/contracts | Day-dream `templates/` folder is the standard |
| Fixed L0–L4 levels | Rigid 5-level hierarchy with fixed semantics | L0–LN with N = depth. Optional, no fixed semantics |
| `PENDING` / `IN_PROGRESS` status | Plain-text status markers | Emoji+text: ⏳`[TODO]`, 🔄`[WIP]`, etc. |
| Auto-detection for plan-or-not | Agents deciding whether to plan | Human authority — human initiates planning |
| 4-slot magnitude scale | Slots: <<1, 1, 2, 3, 4+ | Replaced by 8-slot maximum system |

### v4.01 → v4.02 Changes

| Change | Was (v4.01) | Now (v4.02) |
|--------|-------------|-------------|
| Slot system | 4-slot max (<<1, 1, 2, 3, 4+) | 8-slot max (1, 2, 3, 5, 8) — each is a MAXIMUM |
| Planning authority | Implicit agent auto-triggers | Human decides WHETHER; DREAM decides FORMAT |
| Exec summary + architecture | Always separate | System Plan: separate; Procedure Plan: merged `01_summary.md` |
| Plan types | Implicit, no formal profiles | Explicit System Plan vs Procedure Plan profiles |
| Document ordering | Route → Structure → Author → Execute | Structure-first: Folder trees → Variables → Author → Execute |
| Omittable files | Not addressed | "Omit, don't N/A" — files simply don't exist on disk |
| `01_summary.template.md` | Did not exist | New template for Procedure Plan merged doc |

---

## Design Principles Summary

| Principle | Rule |
|-----------|------|
| **One protocol, two profiles** | System + Procedure share primitives, differ in which files exist |
| **Omit, don't N/A** | Optional files don't exist on disk — never fill with "N/A" |
| **Human authority** | Human initiates planning; agents don't decide whether to plan |
| **Slots, not time** | 8-slot maximum system; each slot ≈ 1 hour AI-agent time |
| **Structure-first** | Show the tree, then explain the rules |
| **ADHD-readable** | Visual-first: tables, ASCII boxes, folder trees, no text walls |

---

*End of DREAM v4.02 — Unified Planning System Specification*
