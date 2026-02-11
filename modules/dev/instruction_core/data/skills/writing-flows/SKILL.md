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

## What is a Flow File?

A `.flow` file is the **source of truth** for agent body content. It compiles to `.agent.md` output. Flow files use a pipe-based DSL that enables modular, reusable agent instructions.

**Key principle:** NEVER edit compiled `.agent.md` files — edit the `.flow` source + `.yaml` sidecar.

---

## Basic Syntax

### Node Definition

```flow
@node_id |param=value| <<<Content goes here.>>>|.
```

- `@` — Defines a node with an identifier
- `|` — Pipe separator for parameters
- `<<<>>>` — Content block (trim mode: strips leading/trailing newlines)
- `<<>>` — Content block (preserve mode: keeps whitespace)
- `|.` — End of node definition

### Minimum File

```flow
@out 
|<<<
Hello, World!
>>>|.
```

Only `@out` is required — it's the entry point for compilation.

---

## Content Blocks

| Opener | Closer | Behavior |
|--------|--------|----------|
| `<<<` | `>>>` | Trim leading AND trailing newlines |
| `<<` | `>>` | Preserve leading AND trailing whitespace |
| `<<<` | `>>` | Trim leading, preserve trailing |
| `<<` | `>>>` | Preserve leading, trim trailing |

---

## Variable References

| Symbol | Direction | Usage |
|--------|-----------|-------|
| `$name` | Backward | Node defined ABOVE current position |
| `^name` | Forward | Node defined BELOW current position |

```flow
@greeting |<<<Hello!>>>|.

@out |$greeting|.
```

Inside content blocks, `$name` is literal text. To insert a reference mid-content:

```flow
@out |<<<Welcome! >>|$greeting|<< How are you?>>>|.
```

---

## Style Parameters

| Parameter | Effect |
|-----------|--------|
| `style.title=<<Title>>` | Adds `# Title` header |
| `style.wrap=xml` | Wraps content in XML tags |
| `style.tag=tagname` | Tag name for XML wrapping |

```flow
@rules
|style.wrap=xml|style.tag=critical_rules
|<<<
- Rule one
- Rule two
>>>|.
```

Compiles to:

```xml
<critical_rules>
- Rule one
- Rule two
</critical_rules>
```

---

## Imports

Import nodes from other `.flow` files:

```flow
# Import all exported nodes
+../_lib/patterns/core_philosophy.flow |.

# Import specific nodes
+./shared.flow |$node_a|$node_b|.
```

The `@out` node from imported files is always ignored.

### File References (Non-Import)

Use `++` to reference files without importing:

```flow
@workflow |<<<See instructions in >>|++./path/to/file.md|<<>>>|.
```

---

## Agent `.flow` Structure

Standard agent structure:

```flow
# Header comment block
# Source of truth: THIS FILE + sidecar (agent_name.yaml)
# Compiles to: data/compiled/agents/agent_name.adhd.agent.md

# =============================================================================
# Imports
# =============================================================================
+../_lib/patterns/core_philosophy.flow |.
+../_lib/patterns/stopping_rules_base.flow |.

# =============================================================================
# Role Introduction
# =============================================================================
@role_intro |<<<You are the **AgentName**, the Role Description.>>>|.

# =============================================================================
# Stopping Rules
# =============================================================================
@stopping_rules
|style.wrap=xml|style.tag=stopping_rules
|<<<STOP IMMEDIATELY if...>>>
|$no_edit_user_override
|.

# =============================================================================
# Core Philosophy
# =============================================================================
@core_philosophy
|style.wrap=xml|style.tag=core_philosophy
|<<<1. **Principle**: ...>>>
|$truthfulness_principle
|.

# =============================================================================
# Workflow
# =============================================================================
@workflow
|style.wrap=xml|style.tag=workflow
|<<<
### 0. **SELF-IDENTIFICATION**
...
>>>|.

# =============================================================================
# Critical Rules
# =============================================================================
@critical_rules
|style.wrap=xml|style.tag=critical_rules
|$stopping_rules_bind
|<<<- **Rule**: ...>>>
|.

# =============================================================================
# Mode Content Assembly
# =============================================================================
@mode_content
|$role_intro
|<<
>>|$stopping_rules
|<<
>>|$core_philosophy
|<<
>>|$workflow
|<<
>>|$critical_rules
|.

# =============================================================================
# Outer modeInstructions Wrapper
# =============================================================================
@modeInstructions
|style.wrap=xml|style.tag=modeInstructions
|<<<You are currently running in "AgentName" mode...>>>
|<<
>>|$mode_content
|.

# =============================================================================
# Entry Point
# =============================================================================
@out
|$modeInstructions
|.
```

---

## Sidecar Pattern (`.yaml`)

Every agent `.flow` has a companion `.yaml` file with frontmatter metadata:

**`.flow` contains:** Body content (role, workflow, rules)

**`.yaml` contains:** 
```yaml
name: AgentName
description: One-line description
argument-hint: "What user should type"
tools: ['tool1', 'tool2']
```

Place both files in `data/flows/agents/`.

---

## Shared Fragments (`_lib/`)

Reusable patterns live in `data/flows/_lib/patterns/`:

| Fragment | Exported Node | Purpose |
|----------|---------------|---------|
| `core_philosophy.flow` | `@truthfulness_principle` | Standard truthfulness rule |
| `stopping_rules_base.flow` | `@no_edit_user_override`, `@stopping_rules_bind` | Common stopping patterns |
| `critical_rules_base.flow` | Shared critical rules | Common constraints |

Import with relative paths:
```flow
+../_lib/patterns/core_philosophy.flow |.
```

---

## Refresh Command

After editing `.flow` or `.yaml` files:

```bash
adhd r -f
```

This compiles all Flow sources and syncs to `.github/`.

---

## Critical Rules

| Rule | Violation |
|------|-----------|
| **Source Files Only** | NEVER edit compiled `.agent.md` — edit `.flow` + `.yaml` |
| **@out Required** | Every `.flow` must have exactly one `@out` node |
| **No Cycles** | `$a` → `$b` → `$a` causes circular dependency error |
| **Path Accuracy** | Import paths are relative to the `.flow` file location |

---

## Reference

- Full DSL manual: `modules/dev/flow_core/manual.md`
- Real examples: `modules/dev/instruction_core/data/flows/agents/*.flow`
- Format rules: `flow_format.instructions.md`
