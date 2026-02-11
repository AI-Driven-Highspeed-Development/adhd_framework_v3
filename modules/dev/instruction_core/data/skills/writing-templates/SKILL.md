---
name: writing-templates
description: "Template file creation for ADHD Framework day-dream artifacts. Covers what templates are (scaffolds for visions, blueprints, assets), naming conventions (snake_case.template.md), placement rules (.agent_plan/day_dream/templates/), tier selection (Simple vs Blueprint), required and optional sections, line limits, and markdown format. Use this skill when creating new templates, understanding template tiers, or scaffolding day-dream documents."
---

# Writing Templates

A guide for creating `.template.md` files that scaffold day-dream artifacts in the ADHD Framework.

## When to Use
- Creating a new template for visions, blueprints, or assets
- Understanding the difference between Simple and Blueprint tiers
- Scaffolding standardized document structures
- Organizing templates in the correct folder hierarchy

---

## What is a Template?

A template is a **scaffold file** that provides structure for day-dream artifacts. Templates use pure markdown (no YAML frontmatter) and contain placeholder sections that users fill in.

**Key principle:** Templates are NOT compiled — they are copied and customized.

---

## Naming Convention

| Rule | Example |
|------|---------|
| Use `snake_case` | `feature_spec.template.md` |
| End with `.template.md` | NOT `.md` or `.template` alone |
| Descriptive names | `api_reference.template.md`, NOT `doc.template.md` |

---

## Placement

Templates live in `.agent_plan/day_dream/templates/`:

```
.agent_plan/day_dream/templates/
├── simple.template.md           # Simple tier scaffold
├── blueprint/                   # Blueprint tier templates
│   ├── 00_index.template.md
│   ├── 01_executive_summary.template.md
│   ├── 02_architecture.template.md
│   ├── NN_feature.template.md
│   └── modules/                 # Module-specific blueprints
├── assets/                      # Asset templates
└── examples/                    # Example templates
```

---

## Tier Selection

### Simple Tier

**Use when:**
- Single responsibility (one clear purpose)
- ≤3 public functions
- No complex state management
- No multi-module coordination
- Quick documentation needed

**Constraints:**
- Max 150 lines (excluding comments)
- Single file
- No architecture diagrams

**Location:** `templates/simple.template.md`

### Blueprint Tier

**Use when:**
- 4+ features
- Cross-module data flows
- External API integrations
- Multiple user types
- Async/background processing

**Structure:** Multi-file with numbered prefixes:
```
blueprint/
├── 00_index.template.md           # Navigation hub
├── 01_executive_summary.template.md
├── 02_architecture.template.md
├── 80_implementation.template.md
├── NN_feature.template.md         # Feature template (N = sequence)
└── 99_references.template.md
```

**Location:** `templates/blueprint/`

---

## Template Structure

### Required Sections

| Section | Purpose |
|---------|---------|
| Title with emoji | Visual identification (`# 🎯 {Name}`) |
| Status line | Version and state (`📐 Draft \| ✅ Ready \| 🔒 Frozen`) |
| Navigation map | "What's Here" table for quick reference |
| Quick Start | 5-minute onboarding |

### Optional Sections

| Section | When to Include |
|---------|-----------------|
| API Reference | If module has public functions |
| Edge Cases | If gotchas exist |
| Config Options | If configurable |
| Changelog | For versioned artifacts |

### Upgrade Criteria Section

Every Simple template MUST include upgrade triggers:

```yaml
upgrade_triggers:
  features_count: ">= 4"
  custom_modules: ">= 3"
  external_apis: ">= 2"
  has_async: true
  multi_user_types: true
```

---

## Template Syntax

Use placeholders in curly braces:

```markdown
# 🎯 {Project Name}

> *{One emotional hook sentence}*

**Version:** 1.0 | **Status:** 📐 Draft

## 🚀 Quick Start

```python
from {module} import {main_function}
result = {main_function}(input)
```
```

### Placeholder Guidelines

| Pattern | Usage |
|---------|-------|
| `{Name}` | User-provided value |
| `{optional: description}` | Can be omitted |
| `<!-- OPTIONAL: ... -->` | Section can be removed |
| `{YYYY-MM-DD}` | Date format hint |

---

## Line Limits

| Tier | Limit |
|------|-------|
| Simple | 150 lines max |
| Blueprint (per file) | 300 lines recommended |
| Comments | Don't count toward limit |

---

## Comments in Templates

Use HTML comments for instructions:

```markdown
<!--
TEMPLATE RULES:

PURPOSE: For small utilities, single-purpose modules

CONSTRAINTS:
- Max 150 lines
- Max 3 main functions

WHEN TO USE:
- New utils/
- Simple plugins
-->
```

---

## Creating a New Template

1. **Determine tier:** Simple or Blueprint?
2. **Choose placement:** Root, `blueprint/`, or subfolder
3. **Use snake_case naming:** `{purpose}.template.md`
4. **Include required sections:** Title, status, navigation, quick start
5. **Add upgrade criteria:** For Simple tier
6. **Document constraints:** In HTML comments at bottom

---

## Critical Rules

| Rule | Violation |
|------|-----------|
| **No YAML Frontmatter** | Templates use pure markdown |
| **Snake Case Names** | `my_template.template.md`, NOT `MyTemplate.template.md` |
| **Correct Placement** | ONLY in `.agent_plan/day_dream/templates/` |
| **Line Limits** | Simple ≤150 lines, Blueprint ≤300 per file |
| **Upgrade Path** | Simple templates MUST define upgrade triggers |

---

## Reference

- Example Simple: `templates/simple.template.md`
- Example Blueprint: `templates/blueprint/*.template.md`
- Day-dream skill: `skills/day-dream/SKILL.md`
