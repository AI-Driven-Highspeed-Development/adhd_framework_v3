# 01 - Executive Summary

> Part of [DREAM Upgrade Blueprint](./00_index.md)

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

The DREAM Upgrade fixes the current blueprint system's human-timescale estimates, forced walking skeletons, and backward-compat obsession (P0), then integrates DREAM v3's decomposition protocol via a new `dream-planning` skill with magnitude-gated structure and context isolation (P1).

---

## 🎯 Problem Statement

The current day-dream blueprint system was designed for human planning cadences. AI agents now author and execute most blueprints, but the system forces human-time estimates ("3-5 days" for 30-minute tasks), mandatory walking skeletons on trivial changes, and backward-compatibility patterns that create spaghetti in actively-developed codebases. Additionally, there's no protocol for decomposing complex work into parallel, context-isolated subtasks — agents either do everything serially or step on each other's context.

---

## 🔍 Prior Art & Existing Solutions

| Library/Tool | What It Does | Decision | License | Rationale |
|--------------|--------------|----------|---------|-----------|
| DREAM v3 spec (internal) | Decomposition protocol with node types, context isolation | WRAP | Internal | Cherry-pick isolation + magnitude concepts; discard L0-L4 hierarchy |
| Current day-dream skill | Blueprint authoring rules | BUILD (update) | Internal | Already works — fix specific pain points, don't rewrite |
| GitHub Issues/Projects | Task decomposition | REJECT | N/A | Too heavyweight, no context isolation, not agent-native |
| Linear/Jira | Project planning | REJECT | Proprietary | Wrong abstraction level for agent-executed work |

**Summary:** We're evolving our own system by fixing the day-dream skill's pain points and wrapping the best DREAM v3 concepts (decomposition, sibling firewall, magnitude routing) into a new `dream-planning` skill.

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Automated plan execution engine | This is a planning protocol, not a runtime orchestrator |
| L0-L4 level **numbering** from DREAM v3 | Directory-based hierarchy with mandatory `_overview.md` replaces rigid level numbers |
| node.yaml + contract.yaml as separate files | Merged into single plan.yaml or inline frontmatter for simplicity |
| State machine / execution.json tracking | Overengineered for current needs; agents report status via markers |
| Migration tooling for existing blueprints | Existing blueprints are few; manual update is faster than building tools |
| GUI or web interface for planning | Terminal/editor-native workflow is sufficient |

---

## ✅ Features Overview

| Priority | Feature | Difficulty | Description |
|----------|---------|------------|-------------|
| P0 | [Fix Estimation](./03_feature_fix_estimation.md) | `[KNOWN]` | AI-agent time defaults with `human_only: true` flag |
| P0 | [Fix Walking Skeleton](./04_feature_fix_walking_skeleton.md) | `[KNOWN]` | Conditional/opt-in — only for cross-boundary integration risk |
| P0 | [Fix Backward Compat](./05_feature_fix_backward_compat.md) | `[KNOWN]` | Clean-code-first directive, folder-separated compat when needed |
| P1 | [DREAM Planning Skill](./06_feature_dream_planning_skill.md) | `[EXPERIMENTAL]` | New skill teaching decomposition protocol with context isolation |
| P1 | [Update Day-Dream Skill](./07_feature_update_day_dream_skill.md) | `[KNOWN]` | Apply P0 fixes + magnitude-gated tier selection to existing skill |
| P1 | [Template Refresh](./08_feature_template_refresh.md) | `[KNOWN]` | Align templates with updated skill rules, remove redundancy |

---

## [Custom] 🎯 Terminology Contract

| Term | Definition | Replaces |
|------|-----------|----------|
| **plan** | A decomposable unit with children (plans or tasks) | "node" (MANAGER type) |
| **task** | A leaf unit, directly executable, no children | "node" (WORKER type) |
| **plan.yaml** | Metadata for a plan (routing + contract merged) | node.yaml + contract.yaml |
| **.task.md** | Specification for a leaf task | .spec.md |
| **magnitude** | Complexity gate: Trivial / Light / Standard / Heavy / Epic | (new) |
| **sibling firewall** | Siblings never read/write each other's content | (new from DREAM v3) |
| **_overview.md** | Mandatory file at every plan directory — purpose, children list, integration map, reading order | (new) |
| **directory = plan** | A directory in the blueprint tree is a plan (has children, always has `_overview.md`) | Replaces L0-L4 numbering |
| **file = task** | A leaf file in the blueprint tree is a task (directly executable) | Replaces L0-L4 numbering |

---

**Next:** [Architecture](./02_architecture.md)

---

**← Back to:** [Index](./00_index.md)
