# Executive Summary

> Part of [DREAM Upgrade](./_overview.md) · ✅ [DONE]

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌──────────────────────────────────────────────────────────────────┐
│  Agent creates blueprint  ──►  💥 FRICTION EVERYWHERE 💥        │
│                                                                  │
│  • "P0: 3-5 days" for a 30-minute agent task                    │
│  • Walking skeleton forced on trivial changes                    │
│  • Backward-compat try/catch spaghetti in clean codebases       │
│  • Edit index.md + summary.md + feature.md for one status change│
│  • No protocol for decomposing complex work into parallel tasks  │
└──────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| AI Agents (HyperDream, HyperArch) | 🔥🔥🔥 High | Every blueprint |
| Human reviewers | 🔥🔥 Medium | Every review cycle |

### ✨ The Vision

```
After DREAM Upgrade:
┌──────────────────────────────────────────────────────────────────┐
│  Agent gets task  ──►  Magnitude check  ──►  Right structure    │
│                                                                  │
│  Trivial/Light → single file, done in minutes                    │
│  Standard+ → decompose into plans/tasks with context isolation   │
│  Estimates match AI speed • Walking skeleton only when needed    │
│  One source of truth per fact • Clean code, no compat spaghetti │
└──────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Upgrade the planning system so AI agents plan at AI speed with decomposition-aware, single-source-of-truth blueprints.

---

## 🔧 The Spec

---

## 🌟 TL;DR

The DREAM Upgrade fixed the blueprint system's human-timescale estimates, forced walking skeletons, and backward-compat obsession (P0), embedded Non-Vibe Code engineering discipline (P1), then integrated DREAM v3's decomposition protocol via a new `dream-planning` skill with magnitude-gated structure and context isolation (P2).

---

## 🎯 Problem Statement

The current day-dream blueprint system was designed for human planning cadences. AI agents now author and execute most blueprints, but the system forced human-time estimates, mandatory walking skeletons, and backward-compatibility patterns that create spaghetti. Additionally, there was no protocol for decomposing complex work into parallel, context-isolated subtasks.

---

## 🔍 Prior Art & Existing Solutions

| Library/Tool | What It Does | Decision | Rationale |
|--------------|--------------|----------|-----------|
| DREAM v3 spec (internal) | Decomposition protocol with node types, context isolation | WRAP | Cherry-pick isolation + magnitude concepts; discard L0-L4 hierarchy |
| Current day-dream skill | Blueprint authoring rules | BUILD (update) | Already works — fix specific pain points, don't rewrite |
| GitHub Issues/Projects | Task decomposition | REJECT | Too heavyweight, no context isolation, not agent-native |
| Linear/Jira | Project planning | REJECT | Wrong abstraction level for agent-executed work |

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Automated plan execution engine | Planning protocol, not runtime orchestrator |
| L0-L4 level numbering from DREAM v3 | Directory-based hierarchy with `_overview.md` replaces rigid numbers |
| node.yaml + contract.yaml as separate files | Merged into single plan.yaml / inline frontmatter |
| State machine / execution.json tracking | Overengineered; agents report status via markers |
| Migration tooling for existing blueprints | Few existing blueprints; manual update faster |
| GUI or web interface for planning | Terminal/editor-native workflow sufficient |

---

## ✅ Features Overview

| Priority | Feature | Difficulty | Status | Description |
|----------|---------|------------|--------|-------------|
| P0 | [Fix Estimation](./p0-fix-blueprint-system/fix-estimation.md) | `[KNOWN]` | ✅ [DONE] | AI-agent time defaults with `human_only: true` flag |
| P0 | [Fix Walking Skeleton](./p0-fix-blueprint-system/fix-walking-skeleton.md) | `[KNOWN]` | ✅ [DONE] | Conditional/opt-in — only for cross-boundary integration risk |
| P0 | [Fix Backward Compat](./p0-fix-blueprint-system/fix-backward-compat.md) | `[KNOWN]` | ✅ [DONE] | Clean-code-first directive, folder-separated compat |
| P1 | [Non-Vibe Code](./p1-non-vibe-code.md) | `[KNOWN]` | ✅ [DONE] | Correctness-over-completion discipline (3 pillars) |
| P2 | [DREAM Planning Skill](./p2-dream-integration/dream-planning-skill.md) | `[EXPERIMENTAL]` | ✅ [DONE] | New decomposition protocol skill |
| P2 | [Update Day-Dream Skill](./p2-dream-integration/update-day-dream-skill.md) | `[KNOWN]` | ✅ [DONE] | Apply P0 fixes + magnitude-gated tier selection |
| P2 | [Template Refresh](./p2-dream-integration/template-refresh.md) | `[KNOWN]` | ✅ [DONE] | Align templates with updated skill rules |

---

## [Custom] 🎯 Terminology Contract

| Term | Definition | Replaces |
|------|-----------|----------|
| **plan** | A decomposable unit with children (plans or tasks) | "node" (MANAGER type) |
| **task** | A leaf unit, directly executable, no children | "node" (WORKER type) |
| **plan.yaml** | Metadata for a plan (routing + contract merged) | node.yaml + contract.yaml |
| **magnitude** | Complexity gate: Trivial / Light / Standard / Heavy / Epic | (new) |
| **sibling firewall** | Siblings never read/write each other's content | (new from DREAM v3) |
| **_overview.md** | Mandatory file at every plan directory | (new) |
| **directory = plan** | A directory is a plan (has children, always has `_overview.md`) | L0-L4 numbering |
| **file = task** | A leaf file is a task (directly executable) | L0-L4 numbering |

---

**← Back to:** [DREAM Upgrade Overview](./_overview.md)
