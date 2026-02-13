---
name: writing-templates
description: "Template file creation for ADHD Framework day-dream artifacts. Covers what templates are (scaffolds for visions, blueprints, assets), naming conventions (snake_case.template.md), placement rules (.agent_plan/day_dream/_templates/), tier selection (Simple vs Blueprint), plan type file matrices (SP/PP), frontmatter schema references, line limits, and template selection. Use this skill when creating new templates, understanding template tiers, or scaffolding day-dream documents."
---

# Writing Templates

A guide for creating `.template.md` files that scaffold day-dream artifacts in the ADHD Framework.

## When to Use
- Creating a new template for visions, blueprints, or assets
- Understanding the difference between Simple and Blueprint tiers
- Scaffolding standardized document structures for System or Procedure Plans
- Organizing templates in the correct folder hierarchy

---

## What is a Template?

A template is a **scaffold file** that provides structure for day-dream artifacts. Templates contain placeholder sections that users fill in.

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

Templates live in `.agent_plan/day_dream/_templates/`:

```
.agent_plan/day_dream/_templates/
├── simple.template.md                         # Simple tier scaffold
├── blueprint/                                 # Blueprint tier templates
│   ├── overview.template.md                   # _overview.md scaffold with frontmatter
│   ├── task.template.md                       # Leaf task scaffold
│   ├── 00_index.template.md
│   ├── 01_executive_summary.template.md       # System Plan
│   ├── 01_summary.template.md                # Procedure Plan
│   ├── 02_architecture.template.md            # System Plan only
│   ├── NN_feature.template.md
│   ├── NN_feature_simple.template.md
│   ├── 80_implementation.template.md
│   ├── 81_module_structure.template.md
│   ├── 82_cli_commands.template.md
│   ├── 99_references.template.md
│   ├── exploration.template.md
│   └── modules/
│       └── module_spec.template.md
├── assets/
│   └── asset.template.md
└── examples/
    ├── blueprint_example/
    └── simple_example.md
```

The underscore prefix (`_templates/`) follows the DREAM convention: underscore = infrastructure directory.

---

## Tier Selection

### Simple Tier

**Use when:** ≤2 features, single module, no external APIs.

| Constraint | Value |
|------------|-------|
| Max lines | 200 |
| Files | Single file |
| Architecture diagrams | Not required |

**Location:** `_templates/simple.template.md`

### Blueprint Tier

**Use when:** ≥3 features OR ≥2 cross-module deps OR external APIs.

**Structure:** Multi-file with numbered prefixes. Plan type (System or Procedure) determines which files are present:

| File | System Plan | Procedure Plan |
|------|:-----------:|:--------------:|
| `_overview.md` | ✅ | ✅ |
| `01_executive_summary.md` | ✅ | — |
| `01_summary.md` | — | ✅ |
| `02_architecture.md` | ✅ | — |
| `0N_feat_{feature}.md` | ✅ | ✅ |
| `80_implementation.md` | ✅ | ✅ |
| `81_module_structure.md` | ✅ | — |

Omitted files do NOT exist on disk. Never create a file to write "N/A."

**Location:** `_templates/blueprint/`

---

## Template Line Limits

| Template | Line Limit |
|----------|------------|
| `_templates/simple.template.md` | ≤200 |
| `_templates/blueprint/overview.template.md` | ≤100 |
| `_templates/blueprint/task.template.md` | ≤100 |
| `_templates/blueprint/01_executive_summary.template.md` | ≤150 |
| `_templates/blueprint/01_summary.template.md` | ≤200 |
| `_templates/blueprint/02_architecture.template.md` | ≤200 |
| `_templates/blueprint/NN_feature.template.md` | ≤150 |
| `_templates/blueprint/NN_feature_simple.template.md` | ≤100 |
| `_templates/blueprint/80_implementation.template.md` | ≤200/phase |
| `_templates/blueprint/81_module_structure.template.md` | ≤150 |
| `_templates/blueprint/modules/module_spec.template.md` | ≤200 |
| `_templates/assets/asset.template.md` | ≤100 (excl. diagrams) |

---

## Key Frontmatter References

Templates should scaffold the correct frontmatter for each document type.

### Plan `_overview.md` Frontmatter

The `_templates/blueprint/overview.template.md` must scaffold ALL required fields:

| Field | Classification |
|-------|---------------|
| `name` | REQUIRED |
| `type` | REQUIRED (`system` or `procedure`) |
| `magnitude` | REQUIRED |
| `status` | REQUIRED |
| `origin` | REQUIRED |
| `last_updated` | REQUIRED |
| `start_at` | OPTIONAL |
| `depends_on` | RECOMMENDED |
| `blocks` | RECOMMENDED |
| `knowledge_gaps` | RECOMMENDED |
| `priority` | OPTIONAL (emergency only) |
| `emergency_declared_at` | CONDITIONAL (required when emergency) |
| `invalidated_by` | CONDITIONAL |
| `invalidation_scope` | CONDITIONAL |
| `invalidation_date` | CONDITIONAL |

> Full schema details: See the `dream-planning` skill.

### Module Spec Frontmatter

The `_templates/blueprint/modules/module_spec.template.md` must scaffold:

| Field | Classification |
|-------|---------------|
| `module` | REQUIRED |
| `last_updated` | REQUIRED |
| `modified_by_plans` | REQUIRED |
| `knowledge_gaps` | RECOMMENDED |

---

## Template Syntax

Use placeholders in curly braces:

```markdown
# 🎯 {Project Name}

> *{One emotional hook sentence}*

**Version:** 1.0 | **Status:** 📐 Draft
```

### Placeholder Guidelines

| Pattern | Usage |
|---------|-------|
| `{Name}` | User-provided value |
| `{optional: description}` | Can be omitted |
| `{YYYY-MM-DD}` | Date format hint |

---

## Template Selection Quick Reference

```
Quick vision, ≤2 features?          → _templates/simple.template.md
Plan directory navigator?           → _templates/blueprint/overview.template.md
Leaf task?                          → _templates/blueprint/task.template.md
Feature (≤2 modules, no ext API)?   → _templates/blueprint/NN_feature_simple.template.md
Feature (≥3 modules or ext API)?    → _templates/blueprint/NN_feature.template.md
Exec summary (System Plan)?         → _templates/blueprint/01_executive_summary.template.md
Summary (Procedure Plan)?           → _templates/blueprint/01_summary.template.md
Architecture?                       → _templates/blueprint/02_architecture.template.md
Implementation roadmap?             → _templates/blueprint/80_implementation.template.md
Module spec?                        → _templates/blueprint/modules/module_spec.template.md
Supporting artifact?                → _templates/assets/asset.template.md
```

---

## Creating a New Template

1. **Determine tier:** Simple or Blueprint?
2. **Choose plan type context:** System Plan or Procedure Plan?
3. **Use snake_case naming:** `{purpose}.template.md`
4. **Place correctly:** In `.agent_plan/day_dream/_templates/` subtree
5. **Include required frontmatter scaffold:** Match the schema for the document type
6. **Respect line limits:** Per the table above
7. **Add placeholder instructions:** Use HTML comments for template rules

---

## Critical Rules

| Rule | Detail |
|------|--------|
| **Correct Placement** | ONLY in `.agent_plan/day_dream/_templates/` |
| **Snake Case Names** | `my_template.template.md`, NOT `MyTemplate.template.md` |
| **Line Limits** | Per template type table |
| **Frontmatter Scaffolding** | Templates for `_overview.md` and module specs MUST scaffold correct frontmatter |
| **Omit-don't-N/A** | Templates for files conditional on plan type should not exist for the wrong type |
| **Infrastructure prefix** | The `_templates/` directory uses underscore prefix per DREAM convention |

---

## Cross-References

| Topic | Where |
|-------|-------|
| Full frontmatter schema | `dream-planning` skill |
| Document authoring rules | `day-dream` skill |
| Plan types (System vs Procedure) | `dream-planning` skill |
| SKILL.md format | `writing-skills` skill |
