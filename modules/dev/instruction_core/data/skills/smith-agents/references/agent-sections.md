# Agent Sections Reference

Required section order and YAML frontmatter fields for `.agent.md` files.

---

## Required Section Order

Each agent definition file MUST include sections in this logical flow:

| Order | Section | XML Tag | Purpose |
|-------|---------|---------|---------|
| 1 | YAML Header | — | Frontmatter with name, description, tools, handoffs |
| 2 | Mode Instructions Block | `<modeInstructions>` | Wraps entire agent content |
| 3 | Role Definition | — | Clear statement of who the agent is and its sole directive |
| 4 | Specialist Awareness | `<specialist_awareness>` | (Optional) Table of agents to hand off to |
| 5 | Stopping Rules | `<stopping_rules>` | Hard constraints that halt execution |
| 6 | Core Philosophy | `<core_philosophy>` | Guiding principles and values |
| 7 | Workflow | `<workflow>` | Numbered steps starting with Step 0 (self-identification) |
| 8 | Critical Rules | `<critical_rules>` | Implementation constraints and anti-patterns |

---

## YAML Frontmatter Fields

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | Yes | Agent display name (e.g., `HyperArch`) |
| `description` | string | Yes | Short description of the agent's role |
| `argument-hint` | string | Optional | Hint shown to user in VS Code when selecting this agent |
| `tools` | list | Yes | Tool identifiers the agent can use |
| `handoffs` | list | Optional | Defines which agents this agent can hand off to |

### Handoff Fields

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `handoffs[].label` | string | Yes | Display label for the handoff option |
| `handoffs[].agent` | string | Yes | Target agent name |
| `handoffs[].prompt` | string | Optional | Prompt to send with the handoff |
| `handoffs[].send` | boolean | Optional | Whether to auto-send (`true`) or let user edit first (`false`) |

---

## Section Placement Rules

Rules must go in the MOST appropriate section — never duplicate across sections.

| Content Type | Correct Section |
|-------------|-----------------|
| "STOP if X happens" conditions | `<stopping_rules>` |
| Values and principles ("Truthfulness over Agreeableness") | `<core_philosophy>` |
| Implementation constraints ("NEVER use print()") | `<critical_rules>` |
| Process steps and actions | `<workflow>` |
| Agent delegation rules | `<specialist_awareness>` or `<workflow>` |

---

## Stopping Rules Format

```markdown
<stopping_rules>
STOP IMMEDIATELY if <most critical condition>.
STOP if <secondary condition>.
NEVER <absolute prohibition>.
</stopping_rules>
```

- Use "STOP IMMEDIATELY" for highest priority
- Use "STOP if" for standard halting conditions
- Use "NEVER" for absolute prohibitions

---

## Workflow Format

```markdown
<workflow>
### 0. **SELF-IDENTIFICATION**
Before starting any task, say out loud: "I am NOW <AgentName>, the <Role>."

### 1. <Step Title>
- <Action>
- <Check>

### 2. <Step Title>
...
</workflow>
```

- Step 0 is always self-identification
- Steps are numbered sequentially
- Each step has a bold title and action items
