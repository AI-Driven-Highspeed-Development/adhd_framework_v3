---
name: dream-planning
description: "DREAM decomposition protocol — magnitude-gated routing, plan/task hierarchy, sibling firewall, and context isolation for parallel agent work. Covers when and how to decompose complex tasks, directory-based plan structure with _overview.md convention, MANAGER/WORKER lifecycle patterns, and plan.yaml schema. Use this skill when decomposing work into subtasks, dispatching parallel subagents, or applying context isolation rules."
---

# DREAM Planning Protocol

Decomposition Rules for Engineering Atomic Modules — how to break work into parallelizable, isolated units.

## When to Use
- Assessing whether a task needs decomposition
- Breaking complex work into a plan/task tree
- Dispatching parallel subagents with context boundaries
- Deciding plan structure (single file vs directory hierarchy)

**Scope boundary:** This skill covers *decomposition and routing*. For document authoring rules (templates, Story/Spec pattern, status syntax), see the `day-dream` skill.

---

## Terminology

| Term | Definition |
|------|-----------|
| **Plan** | A decomposable unit containing ambiguity — has children (plans or tasks). Represented as a **directory** with mandatory `_overview.md`. |
| **Task** | A leaf unit — directly executable, no children, no ambiguity. Represented as a **file** (`.md`). |
| **`_overview.md`** | Mandatory file at every plan directory — states purpose, lists children, defines integration map and reading order. |
| **Magnitude** | Complexity classification: Trivial / Light / Standard / Heavy / Epic. |
| **Sibling firewall** | Hard rule: siblings NEVER read or write each other's content. All coordination goes through the parent. |
| **MANAGER** | Agent processing a plan — decomposes, delegates, integrates children. |
| **WORKER** | Agent fulfilling a task — executes directly, produces artifacts. |

---

## Magnitude Routing

Assess magnitude FIRST. This determines whether decomposition is needed.

| Magnitude | Slots | Action | Structure |
|-----------|-------|--------|-----------|
| Trivial | <<1 | Execute immediately | No planning doc needed |
| Light | 1 | Execute directly | Optional single plan file |
| Standard | 2 | Decompose if ≥3 subtasks | Blueprint tier |
| Heavy | 3 | SHOULD decompose | Blueprint tier |
| Epic | 4+ | MUST decompose | Blueprint tier, mandatory decomposition |

**Routing rules:**
- Trivial/Light → Act as WORKER. Execute the task directly.
- Standard → Assess subtask count. If ≥3 subtasks or cross-module, decompose. Otherwise execute.
- Heavy/Epic → Act as MANAGER. Decompose into plan/task tree before any execution.
- Epic at task level → REFUSE and escalate. Epic work cannot be a leaf task.

**Magnitude is agent judgment, not a rigid checklist.** Use these signals:

| Signal | Points Toward |
|--------|--------------|
| Single file change | Trivial/Light |
| Multiple files, one module | Light/Standard |
| Cross-module changes | Standard/Heavy |
| New module or external API | Heavy/Epic |
| Ambiguity in requirements | Standard+ (needs decomposition) |

---

## Decomposition Protocol

When magnitude warrants decomposition (Standard+ with ≥3 subtasks), follow these steps:

```
1. ASSESS    — Classify magnitude, decide if decomposition needed
2. DECOMPOSE — Break into plan/task tree (directories + files)
3. ISOLATE   — Apply sibling firewall to each branch
4. DELEGATE  — Assign tasks to subagents with context boundaries
5. INTEGRATE — Parent collects results, resolves conflicts
6. REPORT    — Mark plan status as done
```

### When to Stop Decomposing

A unit is a **task** (leaf) when:
- It can be fulfilled by a single agent in a single session
- There is no ambiguity about what to produce
- Its magnitude is Standard or below

A unit is a **plan** (container) when:
- It contains ambiguity requiring further breakdown
- It has ≥2 children that can be worked independently
- Its magnitude is Heavy or Epic

**Warning:** A plan with only 1 child is suspicious — it is probably a task disguised as a plan. Flatten it.

---

## Directory-Based Hierarchy

Hierarchy is expressed through the filesystem. No level numbers (L0-L4).

```
project_plan/
├── _overview.md              # REQUIRED — plan navigator
├── plan.yaml                 # Metadata (or inline frontmatter)
│
├── feature_auth/             # Child plan (directory = plan)
│   ├── _overview.md          # REQUIRED
│   ├── 01_login_flow.md      # Child task (file = task)
│   └── 02_token_refresh.md   # Child task
│
├── feature_dashboard/        # Child plan
│   ├── _overview.md          # REQUIRED
│   ├── 01_layout.md          # Child task
│   └── 02_widgets.md         # Child task
│
└── update_readme.md          # Child task (file = task)
```

**Rules:**
- **Directory = plan** — always has `_overview.md`
- **File = task** — leaf, directly executable
- Nesting depth is unlimited but keep it shallow (≤3 levels recommended)
- Agent entering a directory MUST read `_overview.md` first

---

## `_overview.md` Convention

Every plan directory MUST contain `_overview.md`. This is the agent's entry point.

**Required content:**

```markdown
# {Plan Name}

## Purpose
Why this plan exists and what it delivers.

## Children

| Name | Type | Description |
|------|------|-------------|
| feature_auth/ | Plan | Authentication system |
| update_readme.md | Task | Update project README |

## Integration Map
How children's outputs combine into the plan's deliverable.

## Reading Order
1. feature_auth/ (independent)
2. feature_dashboard/ (independent, parallel-safe with auth)
3. update_readme.md (after both features complete)
```

**Agent protocol:** Enter directory → read `_overview.md` → process children in stated order.

---

## `plan.yaml` Schema

Minimal metadata. Keep it short — details belong in `_overview.md`.

```yaml
name: project_plan
magnitude: Heavy
status: WIP           # TODO | WIP | DONE | BLOCKED:reason | CUT
```

Alternative: use inline YAML frontmatter in `_overview.md` instead of a separate file:

```markdown
---
name: project_plan
magnitude: Heavy
status: WIP
---

# Project Plan
...
```

**No other fields are required.** Additional metadata (dependencies, assignments) MAY be added but is not mandated by this protocol.

---

## Context Isolation — Sibling Firewall

The most critical rule in DREAM. Prevents parallel agents from corrupting each other's context.

### Visibility Rules

| Scope | What Agent Can See |
|-------|-------------------|
| **Read** | Own task/plan, all ancestors up to root, skill files |
| **Write** | Own task/plan ONLY |
| **Sibling status** | Yes — via parent's `_overview.md` or reporting |
| **Sibling content** | **NO — NEVER** |

### Parallel Execution Safety

| Scenario | Parallel Safe? | Reason |
|----------|---------------|--------|
| Siblings with no shared writes | YES | No race conditions |
| Siblings needing parent state | NO | Sequential — parent integrates |
| Workers on independent branches | YES | No shared ancestors modified |

### How Siblings Coordinate

Siblings do NOT coordinate directly. The parent MANAGER:
1. Delegates tasks to children
2. Waits for children to report completion
3. Integrates results in its own INTEGRATE phase
4. Resolves any conflicts between sibling outputs

### Updating files

For any request to update a file, check if the upper layers needs to be updated as well. If so, the agent should report this to the parent, and the parent will decide how to proceed (e.g. wait for all siblings to complete, then update in the parent).

---

## MANAGER vs WORKER Lifecycle

### MANAGER (processes a plan)

```
DECOMPOSE  → Verify/create children with _overview.md
DELEGATE   → Assign each child to a subagent with context boundaries
INTEGRATE  → Collect results, merge outputs, resolve conflicts
REPORT     → Mark plan as done, notify parent
```

**MANAGER rules:**
- MUST create `_overview.md` if it does not exist
- MUST NOT fulfill children's tasks directly — delegate
- MUST integrate: no child output is final until parent accepts it
- Max 5 parallel subagents (practical limit for context management)

### WORKER (fulfills a task)

```
VALIDATE   → Check magnitude is not Epic, check dependencies
IMPLEMENT  → Read task spec, create/modify artifacts
VERIFY     → Check acceptance criteria
REPORT     → Mark task as done, notify parent
```

**WORKER rules:**
- MUST refuse Epic-magnitude tasks — escalate to parent for decomposition
- MUST NOT modify sibling tasks or parent plan content
- MUST report completion to parent (status marker update)

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Siblings communicating directly | Route through parent's INTEGRATE phase |
| Epic-magnitude leaf task | Decompose into plan with children |
| Skip magnitude assessment | Always assess magnitude first |
| Plan with only 1 child | Flatten — it is probably a task |
| MANAGER fulfilling tasks directly | Delegate to WORKER subagents |
| Agent reading sibling content | Read sibling STATUS only (via parent) |
| Deep nesting (>3 levels) | Flatten or re-scope the decomposition |
| Heavyweight plan.yaml schemas | Keep minimal: name + magnitude + status |

---

## Cross-References

| Topic | Where |
|-------|-------|
| Document authoring (templates, Story/Spec) | `day-dream` skill |
| Status syntax (TODO/WIP/DONE/BLOCKED/CUT) | `day-dream` skill |
| Estimation defaults (AI-agent time, human_only) | `day-dream` skill |
| Tier selection (Simple vs Blueprint) | `day-dream` skill |
| Orchestrator dispatch mechanics | `orch-routing` skill |
| Implementation quality gates | `orch-implementation` skill |
