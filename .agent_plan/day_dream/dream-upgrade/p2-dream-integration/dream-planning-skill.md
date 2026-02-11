# Feature: DREAM Planning Skill

> Part of [P2: DREAM Integration](./_overview.md) · ✅ [DONE]

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌──────────────────────────────────────────────────────────────────┐
│  Agent gets complex task  ──►  💥 NO PROTOCOL 💥                 │
│                                                                  │
│  • No rules for breaking work into parallel subtasks             │
│  • No isolation — subagents step on each other's context         │
│  • No magnitude check — trivial tasks get same overhead as Epic  │
│  • "plan" vs "task" vs "node" vs "feature" — terminology chaos   │
└──────────────────────────────────────────────────────────────────┘
```

### ✨ The Vision

```
After This Feature:
┌──────────────────────────────────────────────────────────────────┐
│  Agent gets complex task  ──►  ✅ DREAM PROTOCOL                 │
│                                                                  │
│  1. Check magnitude → route to right tier                        │
│  2. Decompose into plans (containers) + tasks (leaves)           │
│  3. Apply sibling firewall — each subagent isolated              │
│  4. Execute in parallel where dependencies allow                 │
│  5. Parent integrates results                                    │
└──────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> A new `dream-planning` skill teaching the DREAM decomposition protocol: magnitude-gated structure, plan/task hierarchy, and context isolation for parallel work.

---

## 🔧 The Spec

**Priority:** P2 · **Difficulty:** `[EXPERIMENTAL]`

The `dream-planning` skill is the single source of truth for:
1. **Magnitude routing** — assess complexity, pick planning tier
2. **Plan/task hierarchy** — terminology and rules for decomposable vs leaf units
3. **Context isolation** — sibling firewall for parallel subagent work
4. **Lifecycle** — MANAGER/WORKER decompose, delegate, integrate, report

**Implemented at:** `.github/skills/dream-planning/SKILL.md`

---

## ✅ Acceptance Criteria

- [x] `dream-planning` SKILL.md exists at `.github/skills/dream-planning/SKILL.md`
- [x] Follows Agent Skills standard (YAML frontmatter + body sections)
- [x] Magnitude routing table with 5 levels
- [x] Decomposition protocol with 6 steps (ASSESS → REPORT)
- [x] Context isolation rules with read/write visibility table
- [x] Plan/task terminology defined
- [x] Anti-patterns checklist with ≥5 entries
- [x] Cross-references `day-dream` skill for authoring rules

---

## 🔗 Integration Points

| Connects To | Direction | Data |
|-------------|-----------|------|
| `day-dream` skill | → OUT | Tier decision, terminology |
| HyperDream agent | ← IN | Planning requests |
| Orchestrator | ← IN | Decomposition requests |
| Templates | → OUT | Structure decisions |

---

## [Custom] 📜 SKILL.md Content

Key sections delivered:
1. **When to Use** — decomposition triggers
2. **Terminology** — plan, task, magnitude, sibling firewall, `_overview.md`
3. **Magnitude Routing** — Trivial through Epic with actions
4. **Decomposition Protocol** — ASSESS → DECOMPOSE → ISOLATE → DELEGATE → INTEGRATE → REPORT
5. **Context Isolation Rules** — read/write visibility table
6. **Directory-Based Hierarchy** — directory = plan with `_overview.md`, file = task
7. **`plan.yaml` Schema** — minimal metadata
8. **MANAGER/WORKER Lifecycle** — roles and rules
9. **Anti-Patterns** — 8+ entries

---

**← Back to:** [P2 Overview](./_overview.md) · [DREAM Upgrade](../../dream-upgrade/_overview.md)
