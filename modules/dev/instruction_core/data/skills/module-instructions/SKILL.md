---
name: module-instructions
description: "Module instruction authoring workflow for `.instructions.md` files scoped to ADHD modules. Covers required section order, concise AI-targeted style, frontmatter scope rules, and validation checklist. Use this skill when creating or maintaining module-local instruction files."
---

# Module Instruction Authoring

A guide for creating `<module_name>.instructions.md` files that expose module usage patterns and constraints to AI agents.

## When to Use
- Creating a new module instruction file
- Updating instructions after a module API change
- Reviewing module instructions for correctness
- Ensuring a module has proper AI-facing documentation

---

## Core Principles

1. **AI-First**: The audience is AI agents, not humans. Maximum density, minimum noise.
2. **Show, Don't Tell**: Code blocks with correct imports and usage — not prose descriptions.
3. **Absolute Imports Only**: All examples must use package imports, never relative paths or `sys.path`.
4. **Tight Scoping**: The `applyTo` pattern must match only the files that actually use this module.
5. **Single Source**: Each module gets exactly one instruction file. Don't split across multiple files.

---

## Authoring SOP

### Step 1: Identify the Module's Public API
- What classes/functions do consumers import?
- What are the correct import paths?
- What patterns must consumers follow (singletons, init order, etc.)?

### Step 2: Write Required Sections
Follow section order strictly:
1. **Frontmatter** — YAML block with `applyTo` scope
2. **Header** — `<Module Name>:` (with colon)
3. **Purpose** — one or two sentences
4. **Usage** — code blocks showing correct import and usage
5. **Key Concepts/Rules** — bullet points on constraints and behaviors

### Step 3: Set applyTo Scope
- **Global module** (used everywhere): `modules/**/*.py,project/**/*.py,*.py`
- **Module-specific** (helper for certain modules): `modules/**/specific_module/**/*.py`
- When unsure, ask the user for guidance

### Step 4: Validate
- Frontmatter is valid YAML with `applyTo`
- Header ends with colon (`:`)
- Usage examples use correct absolute package imports
- Content is devoid of conversational filler
- Examples are runnable and reflect current API

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Conversational tone ("This module is designed to…") | Direct: "Handles X" |
| Relative imports in examples | Use package imports: `from config_manager import ConfigManager` |
| Missing `applyTo` in frontmatter | Always required — determines when instructions activate |
| Overly broad scope | Scope `applyTo` to files that actually import this module |
| Stale examples after refactor | Update instruction file whenever public API changes |
| Header without colon | Must be `<Module Name>:` (colon is required) |

---

## Reference

- Section spec and frontmatter rules: [module-instruction-spec.md](references/module-instruction-spec.md)
- Blank template: [module-instruction-template.md](assets/module-instruction-template.md)
