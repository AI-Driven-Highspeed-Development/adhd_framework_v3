---
name: smith-skills
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

Complete directory layout with scripts, references, and assets subdirectories:
→ See [full-skill-directory.md](assets/full-skill-directory.md)

---

## Good Skill vs Bad Skill

### Bad Skill (Stub)

Example of a poorly written skill — vague description, body is just a pointer, no actual capability:
→ See [bad-skill-example.md](assets/bad-skill-example.md)

### Good Skill (Self-Contained)

Example of a well-written skill — keyword-rich description, self-contained content, actionable steps:
→ See [good-skill-example.md](assets/good-skill-example.md)

---

## Naming Conventions

### Format Rules
- **`kebab-case` only**: lowercase letters and hyphens. No underscores, no camelCase, no spaces.
- The `name` field MUST match the parent directory name exactly.

```
.github/skills/
├── orch-testing/          # name: orch-testing ✓
│   └── SKILL.md
├── dream-vision/          # name: dream-vision ✓
│   └── SKILL.md
└── smith-skills/          # name: smith-skills ✓
    └── SKILL.md
```

### Agent Prefix Convention

All skills use an **agent-prefix** naming pattern: the prefix identifies the owning agent.

| Prefix | Agent Owner | Purpose | Examples |
|--------|-------------|---------|----------|
| `arch-*` | HyperArch | Development workflow skills | `arch-module`, `arch-mcp`, `arch-cli` |
| `smith-*` | HyperAgentSmith | Authoring/format skills | `smith-agents`, `smith-flows`, `smith-instructions`, `smith-prompts`, `smith-skills`, `smith-module-instructions`, `smith-modules-readme` |
| `red-*` | HyperRed | Adversarial testing skills | `red-testing` |
| `dream-*` | HyperDream | Vision and planning skills | `dream-vision`, `dream-planning`, `dream-close`, `dream-create-pp`, `dream-create-sp`, `dream-fix`, `dream-routing`, `dream-update`, `dream-validate` |
| `orch-*` | HyperOrch | Orchestrator presets | `orch-implementation`, `orch-testing`, `orch-discussion`, `orch-routing`, `orch-expedition` |
| `san-*` | HyperSan | Validation and sanity check skills | `san-output` |
| `iq-*` | HyperIQGuard | Code quality skills | *(none yet)* |
| `exped-*` | HyperExped | Framework export skills | `exped-export` |

### Naming Anti-Patterns

| Avoid | Use Instead | Reason |
|-------|-------------|--------|
| `module-dev` | `arch-module` | Use agent prefix (`arch-*` for HyperArch) |
| `writing-flows` | `smith-flows` | Use agent prefix (`smith-*` for HyperAgentSmith) |
| `attack-testing` | `red-testing` | Use agent prefix (`red-*` for HyperRed) |
| `mcp-module-dev` | `arch-mcp` | Use agent prefix, not domain prefix |
| `hyper-san-output` | `san-output` | Use agent prefix pattern, not full agent name |
| `utils`, `helpers` | Descriptive domain name | Too generic for agent matching |
| `my_skill` | `my-skill` | Underscores violate kebab-case |
| `MySkill` | `my-skill` | camelCase/PascalCase not allowed |
| `day-dream` | `dream-vision` | Use agent prefix pattern (`dream-*` for HyperDream) |
| `expedition` | `exped-export` | Use agent prefix pattern (`exped-*` for HyperExped) |
| `module-instructions` | `smith-module-instructions` | Authoring skills use `smith-*` prefix |

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
