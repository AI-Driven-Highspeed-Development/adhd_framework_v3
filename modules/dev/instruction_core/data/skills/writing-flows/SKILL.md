---
name: writing-flows
description: "Flow DSL syntax and agent authoring patterns for the ADHD Framework. Covers node definition (@node_id), pipe operators (|param=value|), content blocks (<<<>>>), variable references ($backward, ^forward), imports (+./path.flow), style parameters, .flow + .yaml sidecar pattern, shared _lib/ fragments, and the adhd r -f refresh command. Use this skill when creating or editing .flow files, building new agents, or understanding Flow compilation."
---

# Writing Flow Files

A guide for creating `.flow` source files using the FLOW DSL (Flexible Language for Orchestrating Workflows).

## When to Use
- Creating a new agent from scratch
- Editing existing agent `.flow` source files
- Understanding Flow DSL syntax
- Building shared fragments for `_lib/`

---

## Core Principles

1. **Source of Truth**: `.flow` + `.yaml` sidecar are the source files. NEVER edit compiled `.agent.md` output.
2. **One Entry Point**: Every `.flow` file must have exactly one `@out` node — the compilation entry point.
3. **Modular Composition**: Break content into small, named nodes. Compose them via variable references (`$name`, `^name`).
4. **Reuse via Imports**: Extract common patterns to `_lib/` fragments. Import them — don't copy-paste.
5. **No Circular Dependencies**: `$a → $b → $a` causes a compilation error. Design your node graph as a DAG.

---

## Flow Authoring SOP

### Step 1: Plan the Structure
- Determine the purpose: agent, shared fragment, or standalone
- For agents: follow the standard section structure (role, stopping rules, philosophy, workflow, critical rules)
- Identify which `_lib/` fragments to import

### Step 2: Create the Files
- **Agent flows**: Create `<agent_name>.flow` + `<agent_name>.yaml` in `data/flows/agents/`
- **Shared fragments**: Create in `data/flows/_lib/patterns/`
- Use the [agent-flow-template.flow](assets/agent-flow-template.flow) as a starting point

### Step 3: Write Node Definitions
- Define nodes with `@node_id |<<<content>>>|.`
- Use `style.wrap=xml` and `style.tag=tagname` to wrap sections in XML tags
- See [flow-syntax.md](references/flow-syntax.md) for full syntax reference

### Step 4: Compose with Variables
- Reference earlier nodes with `$name` (backward) or `^name` (forward)
- Insert references mid-content by closing and reopening content blocks
- See [variable-system.md](references/variable-system.md) for scoping rules

### Step 5: Import Shared Fragments
```flow
+../_lib/patterns/core_philosophy.flow |.
+../_lib/patterns/stopping_rules_base.flow |.
```

### Step 6: Assemble and Define @out
- Create a `@mode_content` node that chains all sections
- Wrap in `@modeInstructions` with XML tag
- Define `@out` referencing the top-level wrapper

### Step 7: Write Sidecar YAML
```yaml
name: AgentName
description: One-line description
argument-hint: "What user should type"
tools: ['tool1', 'tool2']
```

### Step 8: Compile and Verify
```bash
adhd r -f
```
This compiles all Flow sources and syncs output to `.github/`.

---

## Agent Flow Structure

Standard agent `.flow` files follow this section order:

| Section | Node Pattern | XML Tag |
|---------|-------------|---------|
| Imports | `+../_lib/patterns/*.flow \|.` | — |
| Role Introduction | `@role_intro` | — |
| Stopping Rules | `@stopping_rules` | `<stopping_rules>` |
| Core Philosophy | `@core_philosophy` | `<core_philosophy>` |
| Workflow | `@workflow` | `<workflow>` |
| Critical Rules | `@critical_rules` | `<critical_rules>` |
| Mode Content Assembly | `@mode_content` | — |
| Mode Instructions Wrapper | `@modeInstructions` | `<modeInstructions>` |
| Entry Point | `@out` | — |

See [agent-flow-template.flow](assets/agent-flow-template.flow) for a complete starter template.

---

## Sidecar Pattern

Every agent `.flow` has a companion `.yaml` sidecar:

| File | Contains |
|------|----------|
| `.flow` | Body content — nodes, workflow, rules |
| `.yaml` | Frontmatter metadata — name, description, tools, handoffs |

Both files share the same base name and live in `data/flows/agents/`.

---

## Shared Fragments (`_lib/`)

Reusable patterns live in `data/flows/_lib/patterns/`:

| Fragment | Exported Node(s) | Purpose |
|----------|-------------------|---------|
| `core_philosophy.flow` | `@truthfulness_principle` | Standard truthfulness rule |
| `stopping_rules_base.flow` | `@no_edit_user_override`, `@stopping_rules_bind` | Common stopping patterns |
| `critical_rules_base.flow` | Shared critical rules | Common constraints |

Import with relative paths:
```flow
+../_lib/patterns/core_philosophy.flow |.
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Editing compiled `.agent.md` | Edit `.flow` + `.yaml` source, then `adhd r -f` |
| Missing `@out` node | Every `.flow` must have exactly one `@out` |
| Circular variable references | Design node graph as a DAG — no `$a → $b → $a` |
| Wrong import paths | Paths are relative to the `.flow` file location |
| `$name` inside content block | Close content block first: `>>>|$name|<<<` |
| Forgetting `|.` terminator | Every node definition must end with `|.` |
| Forgetting sidecar `.yaml` | Agents need both `.flow` and `.yaml` files |
| Copy-pasting shared content | Extract to `_lib/` and import instead |

---

## Critical Rules

| Rule | Detail |
|------|--------|
| **Source Files Only** | NEVER edit compiled `.agent.md` — edit `.flow` + `.yaml` |
| **@out Required** | Exactly one per file, serves as compilation entry point |
| **No Cycles** | Circular references cause compilation errors |
| **Relative Paths** | Import paths are always relative to the `.flow` file |

---

## Reference

- Flow DSL syntax: [flow-syntax.md](references/flow-syntax.md)
- Variable system: [variable-system.md](references/variable-system.md)
- Agent template: [agent-flow-template.flow](assets/agent-flow-template.flow)
- Full DSL manual: `modules/dev/flow_core/manual.md`
- Real examples: `modules/dev/instruction_core/data/flows/agents/*.flow`
