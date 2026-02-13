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

| Name | Type | Magnitude | Status | Description |
|------|------|-----------|--------|-------------|
| {child-plan/} | Plan | {Standard/Heavy} | ⏳ [TODO] | {What this sub-plan delivers} |
| {child-task.md} | Task | {Trivial/Light/Standard} | ⏳ [TODO] | {What this task produces} |

<!-- Type: Plan = directory (has its own _overview.md), Task = file (leaf, directly executable) -->
<!-- Magnitude: Trivial | Light | Standard | Heavy | Epic. See dream-planning skill. -->

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
