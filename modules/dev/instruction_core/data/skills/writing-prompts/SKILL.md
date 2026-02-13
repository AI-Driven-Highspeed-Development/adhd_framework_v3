---
name: writing-prompts
description: "Prompt-file authoring workflow for `.prompt.md` files. Defines required frontmatter and structure, reusable prompt layout, default behavior blocks, and concise imperative best practices. Use this skill when creating or modifying prompt templates."
---

# Prompt File Authoring

A guide for creating `.prompt.md` prompt templates that guide AI agents through specific tasks.

## When to Use
- Creating a new reusable prompt template
- Modifying an existing prompt's structure or steps
- Reviewing prompt files for completeness
- Understanding prompt format conventions

---

## Core Principles

1. **Self-Contained**: Each prompt must include everything an agent needs to execute the task — no implicit context.
2. **Explicit Defaults**: Always state what gets skipped by default and how to override.
3. **Imperative Steps**: Use action verbs: "Update…", "Check…", "Verify…" — not "You might want to…".
4. **Numbered Sequences**: Steps must be ordered and numbered for deterministic execution.
5. **Reference, Don't Repeat**: Point to `.instructions.md` files for format rules rather than duplicating them.

---

## Authoring SOP

### Step 1: Define the Task
- What does this prompt accomplish?
- Write a one-line `description` for the frontmatter
- This description appears as the chat input placeholder in VS Code

### Step 2: Write Required Sections
Follow section order:
1. **YAML Header** — frontmatter with `description`
2. **Title** — clear `# Title` heading
3. **Task Description** — what the prompt does (1-2 sentences)
4. **Steps/Instructions** — numbered, actionable steps grouped by task
5. **Default Behavior** — what gets skipped and how to override

### Step 3: Add Default Behavior Block
Every prompt MUST end with:
```markdown
**Default behavior**: <What is skipped or assumed by default>
**To override**: <How user changes the default>
```

### Step 4: Validate
- Description field is present and concise
- Steps are numbered and use imperative verbs
- Default behavior is explicitly stated
- References to instruction files are correct

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing default behavior block | Always state what's skipped and how to override |
| Vague steps ("Handle the config") | Use specific actions: "Read `init.yaml` and extract the `version` field" |
| Duplicating format rules from instructions | Reference the `.instructions.md` file instead |
| Missing `description` in frontmatter | Required — it's the VS Code placeholder text |
| Steps without numbers | Always number steps for deterministic execution |

---

## Reference

- Structure spec and frontmatter: [prompt-spec.md](references/prompt-spec.md)
- Blank template: [prompt-template.md](assets/prompt-template.md)
