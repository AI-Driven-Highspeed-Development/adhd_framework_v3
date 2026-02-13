---
name: writing-instructions
description: "Instructions-file authoring workflow for `.instructions.md` files. Defines required structure, `applyTo` patterns, naming conventions, and best practices for concise enforceable rules. Use this skill when creating or updating instruction files."
---

# Instructions File Authoring

A guide for creating `.instructions.md` files that provide automatic rule enforcement when editing matching files.

## When to Use
- Creating a new instruction file for a module or format
- Updating `applyTo` patterns for existing instructions
- Reviewing instruction file structure for completeness
- Understanding how instructions auto-apply in the ADHD Framework

---

## Core Principles

1. **Auto-Apply by Pattern**: Instructions activate automatically when a file matching the `applyTo` glob is opened. Scope tightly to avoid over-matching.
2. **AI-Targeted Content**: The audience is AI agents, not humans. Be extremely concise — bullet points and code blocks, no prose filler.
3. **Imperative Tone**: Use "MUST", "NEVER", "ALWAYS" — not "should" or "consider".
4. **Enforceable Rules Only**: Every statement must be actionable. Avoid aspirational guidance that can't be verified.
5. **Examples Over Explanations**: Show correct vs incorrect patterns rather than describing them.

---

## Authoring SOP

### Step 1: Determine Scope
- What files should these rules apply to?
- Write the `applyTo` glob pattern (see [instruction-spec.md](references/instruction-spec.md))
- Be specific — `modules/**/*.py` not `**/*`

### Step 2: Write Required Sections
Follow section order:
1. **YAML Header** — frontmatter with `applyTo`
2. **Title** — clear `# Title` heading
3. **Goals** — what the instructions enforce (2-4 bullets)
4. **Rules/Guidelines** — the actual enforceable rules
5. **Template/Examples** — if applicable

### Step 3: Add Examples
- Show correct patterns with code blocks
- Show incorrect patterns with explanations of why they fail
- Prefer side-by-side good/bad examples

### Step 4: Validate
- Frontmatter is valid YAML
- `applyTo` pattern matches intended files and ONLY intended files
- All rules are actionable and verifiable

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Overly broad `applyTo` pattern | Scope to specific directories or file types |
| Conversational tone | Use imperative: "MUST", "NEVER" |
| Rules that can't be checked | Make every rule verifiable by inspection |
| Missing examples | Add code blocks showing correct usage |
| Duplicating rules from other instructions | Reference the other file instead |

---

## Reference

- Structure spec and applyTo patterns: [instruction-spec.md](references/instruction-spec.md)
- Blank template: [instruction-template.md](assets/instruction-template.md)
