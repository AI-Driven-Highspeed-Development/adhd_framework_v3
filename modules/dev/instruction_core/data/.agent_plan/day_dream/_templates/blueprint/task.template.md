<!--
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ⚠️  SCAFFOLD — This template provides STRUCTURE, not protocol.              ║
║  Protocol rules live in skills: day-dream (authoring) and dream-planning     ║
║  (decomposition). Templates are passive — copy, fill, customize.             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
-->

<!--
PURPOSE: Template for leaf task files — atomic work units that a single agent
can fulfill in one session. Tasks are files (not directories) and have no children.

See dream-planning skill for magnitude assessment and WORKER lifecycle.
-->

---
name: "{task-name}"
magnitude: Light        # Trivial | Light | Standard (tasks cannot be Epic)
status: TODO            # TODO | WIP | DONE | BLOCKED:reason | CUT
---

# {Task Name}

## Intent

{What this task achieves in 1-2 sentences. Must be unambiguous.}

## Acceptance Criteria

- [ ] {Criterion 1 — specific and testable}
- [ ] {Criterion 2 — specific and testable}

## Constraints

- {Technical or scope constraint}
- {Another constraint, or "None" if unconstrained}

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| {sibling task or external dep} | Pending / Done | {Brief note} |

<!-- Remove Dependencies section if this task has none. -->
