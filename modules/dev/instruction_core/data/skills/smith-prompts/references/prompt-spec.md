# Prompt File Specification

Required frontmatter, structure, and conventions for `.prompt.md` files.

---

## Required Structure

Each prompt file MUST include sections in this order:

| Order | Section | Purpose |
|-------|---------|---------|
| 1 | YAML Header | Frontmatter with `description` field |
| 2 | Title | Clear `# Title` heading |
| 3 | Task Description | What the prompt accomplishes (1-2 sentences) |
| 4 | Steps/Instructions | Numbered steps grouped by task |
| 5 | Default Behavior | Skip conditions and override instructions |

---

## Frontmatter

```yaml
---
description: <Short description for chat input placeholder>
---
```

The `description` field is **mandatory**. It appears as the placeholder text in VS Code's chat input when the prompt is selected.

---

## Task Sections

Group related steps under task headings:

```markdown
## Task 1: <Section Name>

<Explanation of this task.>

**Steps:**
1. <Step 1>
2. <Step 2>
3. <Step 3>

## Task 2: <Section Name>

<Explanation of this task.>

**Steps:**
1. <Step 1>
2. <Step 2>
```

---

## Default Behavior Block

Every prompt MUST end with:

```markdown
**Default behavior**: <State what gets skipped or assumed by default>
**To override**: <State how user can modify default behavior>
```

Examples:
```markdown
**Default behavior**: Skip core modules unless explicitly asked.
**To override**: Say "include cores" to process all modules.
```

---

## Naming Convention

- Use **lowercase snake_case** ending in `.prompt.md`
- Examples: `update_requirements.prompt.md`, `module_review.prompt.md`
- Place in `modules/dev/instruction_core/data/prompts/`

---

## Best Practices

| Practice | Detail |
|----------|--------|
| Explicit skip conditions | State what's omitted by default |
| Override instructions | Tell user how to change defaults |
| Imperative verbs | "Update…", "Check…", "Verify…" |
| Reference instructions | Point to `.instructions.md` for format rules |
| Concise descriptions | Frontmatter description should be one line |
