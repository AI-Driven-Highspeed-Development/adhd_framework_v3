---
name: writing-skills
description: "Teaches agents how to write proper SKILL.md files following the Agent Skills open standard (agentskills.io). Covers YAML frontmatter structure, body content guidelines, progressive disclosure, directory layout, naming conventions, and examples of good vs bad skills. Use this skill when creating new agent skills, reviewing skill quality, or learning the skills format."
---

# Writing Agent Skills

A guide for creating well-structured SKILL.md files following the Agent Skills open standard.

## When to Use
- Creating a new agent skill from scratch
- Reviewing or improving existing skills
- Understanding the Agent Skills format specification
- Converting instructions or documentation into skills

---

## What is a Skill?

A skill is a **folder** containing at minimum a `SKILL.md` file. Skills give agents specialized capabilities and workflows. They are loaded **on-demand** based on task relevance, not always-on like custom instructions.

```
skill-name/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: additional documentation
└── assets/           # Optional: templates, resources
```

**Key principle:** One skill per folder. The folder name IS the skill name.

---

## YAML Frontmatter (Required)

Every SKILL.md starts with YAML frontmatter:

```yaml
---
name: skill-name
description: "What this skill does and when to use it."
---
```

### `name` Field (Required)
- **Max 64 characters**
- Lowercase letters, numbers, and hyphens only (`a-z`, `0-9`, `-`)
- Must NOT start or end with `-`
- Must NOT contain consecutive hyphens (`--`)
- **Must match the parent directory name**

**Valid:**
```yaml
name: pdf-processing
name: code-review
name: orch-testing
```

**Invalid:**
```yaml
name: PDF-Processing    # uppercase not allowed
name: -pdf              # cannot start with hyphen
name: pdf--processing   # consecutive hyphens not allowed
name: my skill          # spaces not allowed
```

### `description` Field (Required)
- **Max 1024 characters**
- Describe BOTH what the skill does AND when to use it
- Include specific keywords that help agents identify relevant tasks
- This is the ONLY thing agents see before deciding to load the skill

**Good:**
```yaml
description: "Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction."
```

**Bad:**
```yaml
description: "Helps with PDFs."
```

**Tips for good descriptions:**
- Start with action verbs (Extracts, Coordinates, Creates, Manages)
- List the main capabilities
- End with "Use this skill when..." trigger phrases
- Include domain-specific keywords agents might match on

### Optional Fields

| Field | Purpose | Max Length |
|-------|---------|-----------|
| `license` | License name or reference to bundled file | — |
| `compatibility` | Environment requirements (products, packages, network) | 500 chars |
| `metadata` | Arbitrary key-value pairs for additional properties | — |
| `allowed-tools` | Space-delimited list of pre-approved tools (experimental) | — |

---

## Body Content

The markdown body after the frontmatter contains the skill instructions. There are no strict format restrictions, but follow these guidelines:

### Recommended Structure

```markdown
# Skill Title

## When to Use
- Trigger conditions and scenarios

## Key Concepts
- Important terms and definitions

## Step-by-Step Instructions
1. First step
2. Second step

## Examples
- Input/output examples

## Critical Rules
- Hard constraints and anti-patterns
```

### Writing Effective Instructions

| Do | Don't |
|----|-------|
| Be specific and actionable | Be vague or generic |
| Include concrete examples | Assume the agent knows your context |
| State constraints explicitly | Leave rules implicit |
| Use tables for structured data | Write walls of text |
| Keep under 500 lines | Dump everything into SKILL.md |

### Progressive Disclosure

Skills use a 3-level loading system:

1. **Discovery (~100 tokens):** Only `name` and `description` are loaded at startup
2. **Instructions (<5000 tokens recommended):** Full SKILL.md body loaded when activated
3. **Resources (as needed):** Files in the skill directory loaded only when referenced

**Keep your main SKILL.md under 500 lines.** Move detailed reference material to separate files:

```markdown
See [the reference guide](references/REFERENCE.md) for detailed API documentation.
Run the setup script: `scripts/setup.sh`
```

---

## Directory Layout

### Minimal Skill
```
my-skill/
└── SKILL.md
```

### Full Skill with Resources
```
my-skill/
├── SKILL.md              # Main instructions
├── scripts/              # Executable code
│   ├── setup.sh.template   # Adding .template to make the IDE stop screaming.
│   └── validate.py.template
├── references/           # Additional documentation
│   ├── REFERENCE.md
│   └── api-spec.md
└── assets/               # Static resources
    ├── template.json
    └── schema.yaml
```

### Optional Directories

| Directory | Purpose | Notes |
|-----------|---------|-------|
| `scripts/` | Executable code agents can run | Self-contained, document dependencies |
| `references/` | Additional documentation | Loaded on demand, keep files focused |
| `assets/` | Templates, schemas, data files | Static resources |

---

## Good Skill vs Bad Skill

### Bad Skill (Stub)
```yaml
---
name: testing
description: "Helps with testing."
---

# Testing

See `testing_preset.instructions.md` for the full testing protocol.
```

**Problems:**
- Description is too vague for agent matching
- Body points to another file instead of containing the actual content
- Skill provides no actual capability

### Good Skill (Self-Contained)
```yaml
---
name: testing
description: "Testing and validation workflows — test folder conventions, pytest execution, and CI integration patterns. Use when creating tests, deciding between tests/ and playground/, or running validation."
---

# Testing

## When to Use
- Creating or running unit tests
- Setting up test infrastructure

## Folder Decision Tree
### Step 1: Is this a scratch file?
- YES → `.temp_agent_work/`
- NO → Continue...

## Test Execution
```bash
source .venv/bin/activate && pytest tests/
```

## Critical Rules
- Always activate venv before running Python
- Check existing tests before creating new ones
```

**Why this works:**
- Description is keyword-rich and specific
- Body IS the actual content, not a pointer
- Includes actionable steps and examples
- Self-contained — no external dependencies to understand it

---

## Naming Conventions

### Format Rules
- **`kebab-case` only**: lowercase letters and hyphens. No underscores, no camelCase, no spaces.
- The `name` field MUST match the parent directory name exactly.

```
.github/skills/
├── orch-testing/          # name: orch-testing ✓
│   └── SKILL.md
├── day-dream/             # name: day-dream ✓
│   └── SKILL.md
└── writing-skills/        # name: writing-skills ✓
    └── SKILL.md
```

### Prefix/Suffix Patterns

| Pattern | Purpose | Examples |
|---------|---------|----------|
| `writing-*` | Authoring/format skills — teach how to author or format a specific file type | `writing-flows`, `writing-agents`, `writing-instructions`, `writing-prompts`, `writing-skills`, `writing-templates` |
| `*-dev` | Development workflow skills — teach how to develop/implement a specific type of module or component | `module-dev`, `mcp-module-dev`, `cli-dev` |
| `orch-*` | Orchestrator presets — define orchestration workflow presets | `orch-implementation`, `orch-testing`, `orch-discussion`, `orch-routing` |
| *(none)* | Domain-specific skills — descriptive kebab-case without a required prefix/suffix | `hyper-san-output`, `day-dream`, `dream-planning`, `expedition`, `testing` |

### Naming Anti-Patterns

| Avoid | Use Instead | Reason |
|-------|-------------|--------|
| `xxx-format` | `writing-xxx` | `writing-*` is the canonical prefix for authoring skills |
| `utils`, `helpers` | Descriptive domain name | Too generic for agent matching |
| `my_skill` | `my-skill` | Underscores violate kebab-case |
| `MySkill` | `my-skill` | camelCase/PascalCase not allowed |

---

## Skills vs Instructions vs Prompts

| Feature | Skills | Instructions | Prompts |
|---------|--------|-------------|---------|
| **Loading** | On-demand (by task match) | Always-on or glob-matched | User-invoked |
| **Purpose** | Specialized capabilities | Coding standards/guidelines | One-shot workflows |
| **Portability** | Cross-agent (VS Code, CLI, etc.) | VS Code only | VS Code only |
| **Content** | Instructions + scripts + resources | Instructions only | Instructions only |
| **Standard** | Open (agentskills.io) | VS Code-specific | VS Code-specific |

**Use skills when:** You want reusable, on-demand capabilities loaded by relevance.
**Use instructions when:** You want always-applied coding standards or glob-matched rules.
**Use prompts when:** You want user-triggered one-shot workflows.

---

## Skill Storage Locations

| Location | Type | Scope |
|----------|------|-------|
| `.github/skills/` | Project skills | Shared via repository |
| `~/.copilot/skills/` | Personal skills | User-specific |
| Custom paths via `chat.agentSkillsLocations` | Configurable | Shared across projects |

---

## Checklist for New Skills

Before publishing a skill:

- [ ] `name` field matches parent directory name
- [ ] `name` is lowercase, hyphens only, ≤64 chars
- [ ] `description` is specific and keyword-rich (≤1024 chars)
- [ ] Body contains actual instructions, not pointers to other files
- [ ] SKILL.md is under 500 lines
- [ ] Detailed reference material is in separate files if needed
- [ ] Examples are included for complex procedures
- [ ] Critical rules and constraints are explicitly stated
