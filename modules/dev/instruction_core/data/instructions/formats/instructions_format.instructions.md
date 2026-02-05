---
applyTo: "**/*.instructions.md"
---

# Instructions File Authoring Guidelines

## Goals
- Create rule sets that automatically apply when editing matching files.
- Ensure consistent code style, structure, and conventions across the project.
- Provide clear, enforceable guidelines for AI agents.

## Required Structure
Each instructions file MUST include:
1) **YAML Header**: Frontmatter with `applyTo` glob pattern.
2) **Title**: A clear `# Title` heading.
3) **Goals Section**: What these instructions aim to achieve.
4) **Rules/Guidelines**: The actual rules to enforce.
5) **Template/Examples**: If applicable, provide templates.

## Template
```markdown
---
applyTo: "<glob pattern for target files>"
---

# <Instructions Title>

## Goals
- <Goal 1>
- <Goal 2>

## Rules
1. **<Rule Name>**: <Description>
2. **<Rule Name>**: <Description>

## Template (if applicable)
\`\`\`
<Template content>
\`\`\`

## Examples (if applicable)
<example>
<Good example>
</example>
```

## applyTo Patterns
The `applyTo` field uses glob patterns to match files:
- `**/*.py` - All Python files
- `cores/**/*.py` - Python files in cores/
- `**/*.agent.md` - All agent definition files
- `**/init.yaml` - All init.yaml files
- `cores/**/README.md, managers/**/README.md` - Multiple patterns (comma-separated)

## Naming Convention
- Use lowercase snake_case ending in `.instructions.md` (e.g., `logger_util.instructions.md`).
- Place in `cores/instruction_core/data/instructions/`.

## Best Practices
- Be specific with `applyTo` patterns to avoid over-matching.
- Use imperative tone ("MUST", "NEVER", "ALWAYS").
- Provide clear examples of correct vs incorrect patterns.
- Keep rules concise and actionable.
