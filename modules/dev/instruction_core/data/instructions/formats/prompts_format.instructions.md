---
applyTo: "**/*.prompt.md"
---

# Prompt File Authoring Guidelines

## Goals
- Create reusable prompt templates that guide AI agents through specific tasks.
- Ensure prompts are clear, actionable, and self-contained.
- Standardize the structure of `.prompt.md` files for consistent behavior.

## Required Structure
Each prompt file MUST include:
1) **YAML Header**: Frontmatter with `description` field.
2) **Title**: A clear `# Title` heading.
3) **Task Description**: Explanation of what the prompt accomplishes.
4) **Steps/Instructions**: Clear, numbered steps or sections.
5) **Default Behavior**: State any skip conditions or defaults.

## Template
```markdown
---
description: <Short description for chat input placeholder>
---

# <Prompt Title>

<Brief description of what this prompt does.>

## Task 1: <Section Name>

<Explanation of this task.>

**Steps:**
1. <Step 1>
2. <Step 2>
3. <Step 3>

## Task 2: <Section Name> (if applicable)

<Explanation of this task.>

---

**Default behavior**: <State any default skip conditions or behaviors.>
**To override**: <State how user can modify default behavior.>
```

## Naming Convention
- Use lowercase snake_case ending in `.prompt.md` (e.g., `update_requirements.prompt.md`).
- Place in `modules/dev/instruction_core/data/prompts/`.

## Best Practices
- Be explicit about what gets skipped by default (e.g., "Skip cores unless asked").
- Include clear override instructions for optional behaviors.
- Use imperative tone ("Update...", "Check...", "Verify...").
- Reference relevant `.instructions.md` files for format guidance.
