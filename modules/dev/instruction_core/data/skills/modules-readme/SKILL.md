---
name: modules-readme
description: "Module README authoring workflow for ADHD Framework modules. Covers required section order, tone and style conventions, import rules for examples, cross-linking guidance, requirements guidance, validation checklist, and a canonical README template. Use this skill when creating or updating module README.md files, reviewing README quality, or understanding ADHD README conventions."
---

# Module README Authoring

A guide for writing consistent, skimmable, and useful README.md files for ADHD Framework modules.

## When to Use
- Creating a README for a new module
- Updating an existing module README after API changes
- Reviewing README quality and completeness
- Understanding the required section order and conventions

---

## Core Principles

1. **Short and Skimmable**: Keep READMEs concise — users need quick orientation, not essays.
2. **Consistent Structure**: All modules follow the same section order for predictability.
3. **Working Examples**: Quickstart snippets must be runnable with correct imports.
4. **Cross-Linking**: Help users discover related modules via "See also" sections.

---

## README Authoring SOP

### Step 1: Use the Template

Copy the template from [readme-template.md](assets/readme-template.md) and adapt it for your module.

### Step 2: Follow Required Section Order

Sections MUST appear in this exact order (omit only if truly not applicable):

1. **Title** — `# <Human-friendly Module Name>` with one-sentence intro
2. **Overview** — 3–5 concise bullets on purpose and usage
3. **Features** — bulleted key capabilities
4. **Quickstart** — one or two code snippets showing the happy path
5. **API** — minimal surface outline of public classes and main methods
6. **Notes** (optional) — implementation or behavioral caveats
7. **Requirements & prerequisites** — external packages only
8. **Troubleshooting** — 3–6 common issues with fixes
9. **Module structure** — short tree of files with one-line comments
10. **See also** — 2–4 related modules

### Step 3: Apply Tone and Style

- Single-sentence intro under the title (e.g., "Small," "Lightweight," etc.)
- Short sentences, concrete language; minimize buzzwords
- Present tense
- Prefer code over prose where helpful

### Step 4: Use Correct Imports

- Package imports: `from <package_name> import <ExportedClass>` (e.g., `from logger_util import Logger`)
- Check `__init__.py` for `__all__` or explicit exports
- No star imports

### Step 5: Validate

Run the checklist below before finalizing.

---

## Requirements Guidance

- All dependencies (ADHD modules and PyPI packages) are declared in `pyproject.toml` under `[project].dependencies`
- ADHD workspace dependencies are resolved via `[tool.uv.sources]` in the root workspace
- No version pins unless a strict version is required to avoid known breakage

---

## Cross-Linking

- In "See also", reference sibling modules by human name (e.g., "YAML Reading Core", "Temp Files Manager")
- Use file links only when it clarifies navigation; plain names are fine within the repo

---

## Full Structure and Template

See [readme-structure.md](references/readme-structure.md) for the detailed format specification and [readme-template.md](assets/readme-template.md) for a copy-paste starter.

---

## Validation Checklist

- [ ] Title + one-line intro present and concise
- [ ] Sections follow the required order
- [ ] Quickstart imports are correct and runnable
- [ ] API section reflects current public surface
- [ ] Requirements match module `pyproject.toml` dependencies; no version pins unless necessary
- [ ] Module structure matches actual files
- [ ] "See also" lists 2–4 relevant modules

---

## Maintenance

- Update the README when public APIs change or when adding/removing key features
- Keep examples aligned with exported import paths; adjust `__init__.py` exports where it improves DX
- Keep cross-links fresh when modules are added/renamed
