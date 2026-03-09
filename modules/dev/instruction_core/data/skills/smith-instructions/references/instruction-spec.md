# Instruction File Specification

Required structure, frontmatter rules, and naming conventions for `.instructions.md` files.

---

## Required Structure

Each instructions file MUST include sections in this order:

| Order | Section | Purpose |
|-------|---------|---------|
| 1 | YAML Header | Frontmatter with `applyTo` glob pattern |
| 2 | Title | Clear `# Title` heading |
| 3 | Goals | What these instructions aim to achieve (2-4 bullets) |
| 4 | Rules/Guidelines | The actual enforceable rules |
| 5 | Template/Examples | Templates or correct/incorrect examples (if applicable) |

---

## Frontmatter

```yaml
---
applyTo: "<glob pattern for target files>"
---
```

The `applyTo` field is **mandatory**. It determines which files trigger this instruction set.

---

## applyTo Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**/*.py` | All Python files in workspace |
| `modules/**/*.py` | Python files under modules/ |
| `**/*.agent.md` | All agent definition files |
| `**/*.flow` | All flow DSL files |
| `modules/**/README.md` | README files in module directories |
| `modules/**/*.py,project/**/*.py,*.py` | Multiple patterns (comma-separated) |

### Scoping Guidelines

- **Global module** (used everywhere): `modules/**/*.py,project/**/*.py,*.py`
- **Module-specific**: `modules/**/specific_module/**/*.py`
- **Format-specific**: `**/*.agent.md` or `**/*.flow`
- Target `.py` files specifically — avoid matching non-code files
- Include `*.py` for root entry points like `adhd_framework.py`

---

## Naming Convention

- Use **lowercase snake_case** ending in `.instructions.md`
- Examples: `logger_util.instructions.md`, `config_manager.instructions.md`
- Place in `modules/dev/instruction_core/data/instructions/`
- Subdirectories by category: `formats/`, `modules/`, `framework/`, `agents/`

---

## Best Practices

| Practice | Detail |
|----------|--------|
| Be specific with `applyTo` | Avoid over-matching unrelated files |
| Use imperative tone | "MUST", "NEVER", "ALWAYS" — not "should" |
| Provide examples | Show correct vs incorrect patterns |
| Keep rules concise | One rule per bullet, actionable and verifiable |
| No conversational filler | Skip "This file is designed to..." phrasing |
