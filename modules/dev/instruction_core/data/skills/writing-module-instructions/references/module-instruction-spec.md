# Module Instruction Specification

Required section order, frontmatter scope rules, and conventions for module `.instructions.md` files.

---

## Required Section Order

Each module instruction file MUST include sections in this exact order:

| Order | Section | Purpose |
|-------|---------|---------|
| 1 | Frontmatter | YAML block defining file scope (`applyTo`) |
| 2 | Header | `<Module Name>:` (with trailing colon) |
| 3 | Purpose | One or two sentences describing the module's role |
| 4 | Usage | Code blocks showing correct import and usage patterns |
| 5 | Key Concepts/Rules | Bullet points on configuration, singletons, constraints |

---

## Frontmatter Rules

```yaml
---
applyTo: "modules/**/*.py,project/**/*.py,*.py"
---
```

| Rule | Detail |
|------|--------|
| `applyTo` is mandatory | Determines when this instruction set activates |
| Target `.py` files only | Don't match non-code files |
| Include root files | Add `*.py` to cover entry points like `adhd_framework.py` |
| Scope tightly | If the module is only used by specific modules, narrow the pattern |

### Scope Patterns

| Module Usage | Pattern |
|-------------|---------|
| Global (used everywhere) | `modules/**/*.py,project/**/*.py,*.py` |
| Module-specific | `modules/**/specific_module/**/*.py` |
| Layer-specific | `modules/foundation/**/*.py` |

---

## Tone and Style

| Rule | Detail |
|------|--------|
| **Target audience** | AI agents, not humans |
| **Format** | Bullet points and code blocks primarily |
| **Imports** | ALWAYS use full absolute package imports |
| **No filler** | Avoid "This module is designed to…" — just say "Handles X" |
| **Concise** | Maximum density, minimum noise |

---

## Validation Checklist

- [ ] Frontmatter is present and valid YAML
- [ ] Header ends with colon (`:`)
- [ ] Usage examples use correct, absolute imports
- [ ] Content is concise and devoid of conversational filler
- [ ] `applyTo` scope matches intended consumers

---

## Maintenance

- Update the instruction file when public APIs change
- Ensure usage examples remain valid after refactors
- Re-check `applyTo` scope if module consumers change
