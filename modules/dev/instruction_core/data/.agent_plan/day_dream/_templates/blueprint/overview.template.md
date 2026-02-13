---
# REQUIRED fields (plan is invalid without these)
name: {plan_name}           # snake_case identifier
type: system                # system | procedure
magnitude: Standard         # Trivial | Light | Standard | Heavy | Epic
status: TODO                # TODO | WIP | DONE | BLOCKED | CUT
origin: exploration/xxx.md  # Path to triggering doc
last_updated: YYYY-MM-DD    # Last modification date

# RECOMMENDED fields (omit if not applicable)
# depends_on: []            # Plans this requires - uncomment if needed
# blocks: []                # Plans that wait for this - uncomment if needed
# knowledge_gaps: []        # Missing expertise - uncomment if needed
---

<!--
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ⚠️  SCAFFOLD — This template provides STRUCTURE, not protocol.              ║
║  Protocol rules live in skills: day-dream (authoring) and dream-planning     ║
║  (decomposition). Templates are passive — copy, fill, customize.             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
-->

<!--
PURPOSE: Template for _overview.md files — the mandatory navigator at every
plan directory. Agents entering a directory MUST read _overview.md first.

See dream-planning skill for the full _overview.md convention and plan/task
hierarchy rules.
-->

# {Plan Name}

## Purpose

{Why this plan exists and what it delivers. 2-3 sentences max.}

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| {child-plan/} | Plan | ⏳ [TODO] | {What this sub-plan delivers} |
| {child-task.md} | Task | ⏳ [TODO] | {What this task produces} |

<!-- Type: Plan (directory with _overview.md) or Task (single .md file). NO other values allowed. -->

## Integration Map

{How children's outputs combine into this plan's deliverable.}

```
{child-plan/} output ──┐
                        ├──► {combined result}
{child-task.md} output ─┘
```

## Reading Order

<!-- Mark parallel-safe items. Agents use this to determine execution order. -->

1. {child-plan/} — {dependency note or "independent"}
2. {child-task.md} — {dependency note or "parallel-safe with above"}
