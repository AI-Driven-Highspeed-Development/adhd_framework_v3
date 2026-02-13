---
name: writing-agents
description: "Agent definition authoring workflow for ADHD Framework. Covers required `.agent.md` section order, YAML frontmatter fields, modeInstructions structure, stopping rules, core philosophy, workflow, and critical rules layout. Use this skill when creating or modifying agent definitions."
---

# Agent Definition Authoring

A guide for creating and modifying `.agent.md` agent definition files in the ADHD Framework.

## When to Use
- Creating a new agent definition from scratch
- Modifying an existing agent's sections or metadata
- Reviewing agent structure for correctness
- Understanding YAML frontmatter fields and section ordering

---

## Core Principles

1. **Strict Section Order**: Agents follow a mandatory section sequence. Out-of-order sections confuse runtime parsing.
2. **No Duplication Across Tags**: Never repeat rules across `<stopping_rules>`, `<core_philosophy>`, and `<critical_rules>`. Place each rule in the MOST appropriate section only.
3. **Self-Identification First**: Every agent workflow starts with step 0 — announcing identity to distinguish from prior agents in chat history.
4. **Imperative Tone**: Use direct commands ("STOP if…", "NEVER do…"), not suggestions.
5. **Flow Source of Truth**: If the agent is compiled from `.flow` files, NEVER edit the `.agent.md` directly — edit the `.flow` + `.yaml` sidecar.

---

## Authoring SOP

### Step 1: Plan the Agent
- Define the agent's **single responsibility** and role boundary
- Identify which **tools** the agent needs access to
- Determine **handoff targets** (which agents it can delegate to)

### Step 2: Write YAML Frontmatter
- Set required fields: `name`, `description`, `tools`
- Add optional fields: `argument-hint`, `handoffs`
- See [agent-sections.md](references/agent-sections.md) for field reference

### Step 3: Write Sections in Order
Follow the mandatory section order:
1. Role Definition — who the agent is, its sole directive
2. `<stopping_rules>` — hard constraints that halt execution
3. `<core_philosophy>` — guiding principles
4. `<workflow>` — numbered steps starting with self-identification
5. `<critical_rules>` — implementation constraints

### Step 4: Wrap in modeInstructions
All content goes inside `<modeInstructions>` XML tags with the standard opening line.

### Step 5: Review
- Verify no rule duplication across sections
- Confirm all handoff targets exist
- Check tool list is accurate

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Repeating rules across stopping/philosophy/critical | Place each rule in ONE section only |
| Missing self-identification step | Always include Step 0 in workflow |
| Editing compiled `.agent.md` directly | Edit `.flow` + `.yaml` source, then `adhd r -f` |
| Vague stopping rules | Use concrete conditions: "STOP if X happens" |
| Missing `tools` in frontmatter | Always declare tools even if empty list |
| Overly long workflow steps | Break into sub-steps; keep each step focused |

---

## Reference

- Section order and YAML fields: [agent-sections.md](references/agent-sections.md)
- Blank agent template: [agent-template.md](assets/agent-template.md)
- Flow-based agents: Load the `writing-flows` skill
