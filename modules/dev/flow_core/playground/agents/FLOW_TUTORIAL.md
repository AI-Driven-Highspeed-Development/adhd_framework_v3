# FLOW Language Tutorial

> **A Complete Guide to Writing Composable AI Instruction Files**

This tutorial teaches you how to write FLOW files—a domain-specific language (DSL) for creating modular, reusable AI agent definitions, prompts, and instructions.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Basic Syntax](#2-basic-syntax)
3. [String Delimiters](#3-string-delimiters-critical)
4. [Content Composition](#4-content-composition)
5. [Style Parameters](#5-style-parameters)
6. [Forward References (Slots/Templates)](#6-forward-references-slotstemplates)
7. [Library Organization (3-Layer Pattern)](#7-library-organization-3-layer-pattern)
8. [Complete Example](#8-complete-example)
9. [Common Patterns](#9-common-patterns)
10. [Compilation Commands](#10-compilation-commands)
11. [Common Mistakes & Gotchas](#11-common-mistakes--gotchas)

---

## 1. Introduction

### What is FLOW?

FLOW is a **domain-specific language** for composing AI instruction files. It allows you to define reusable fragments of prompts, agent behaviors, and instructions, then compose them into complete files through references and imports.

**FLOW compiles to:**
- `.agent.md` - Agent behavior definitions
- `.prompt.md` - Prompt templates
- `.instructions.md` - Instruction sets

### Why FLOW?

| Problem | FLOW Solution |
|---------|---------------|
| Copy-paste of common sections (stopping rules, workflows) | Define once, reference everywhere with `$node` |
| Updating shared content across multiple agents | Update the source file, recompile all dependents |
| Provider-specific formatting (VSCode, Claude, etc.) | Swap provider library, keep agent logic unchanged |
| Visualizing dependencies between fragments | Generate dependency graphs with `graph` command |

### Before FLOW vs After FLOW

**Before FLOW (manual repetition):**
```markdown
<!-- agent_a.md -->
<stopping_rules>
STOP IMMEDIATELY if you see a security vulnerability.
STOP if `init.yaml` is missing or malformed.
NEVER create, edit, or delete any file.
</stopping_rules>

<!-- agent_b.md - same content copied -->
<stopping_rules>
STOP IMMEDIATELY if you see a security vulnerability.
STOP if `init.yaml` is missing or malformed.
NEVER create, edit, or delete any file.
</stopping_rules>
```

**After FLOW (single source of truth):**
```flow
# lib/patterns/stopping_rules_base.flow
@stopping_rules_base
|<<<
STOP IMMEDIATELY if you see a security vulnerability.
STOP if `init.yaml` is missing or malformed.
NEVER create, edit, or delete any file.
>>>|.

# agent_a.flow
+./lib/patterns/stopping_rules_base.flow |.

@stopping_rules
|style.wrap=xml|style.tag=stopping_rules
|$stopping_rules_base
|.

# agent_b.flow - same import, automatic updates
+./lib/patterns/stopping_rules_base.flow |.

@stopping_rules
|style.wrap=xml|style.tag=stopping_rules
|$stopping_rules_base
|.
```

---

## 2. Basic Syntax

### Node Definitions

Nodes are named fragments of content. Everything in FLOW is a node.

```flow
@node_name
|<<<content goes here>>>
|.
```

**Breakdown:**
- `@node_name` - Declares a node with the given name
- `|` - Pipe separator (starts each parameter/content block)
- `<<<...>>>` - String delimiters (see [Section 3](#3-string-delimiters-critical))
- `|.` - Node terminator (ends the definition)

**Single-line equivalent:**
```flow
@greeting |<<<Hello, world!>>>|.
```

### Comments

Lines starting with `#` are comments (ignored by the compiler):

```flow
# This is a comment describing the node below
@greeting |<<<Hello!>>>|.
```

### The `@out` Node

The `@out` node is the **entry point** for compilation. It defines what content is produced when the file is compiled:

```flow
@greeting |<<<Hello!>>>|.
@farewell |<<<Goodbye!>>>|.

# Only @greeting will be compiled because @out references it
@out |$greeting|.
```

### Backward References (`$`)

Reference a node defined **above** the current position:

```flow
@part_one |<<<First part>>>|.
@part_two |<<<Second part>>>|.

# Reference both nodes
@combined |$part_one|$part_two|.

@out |$combined|.
```

**Output:**
```
First partSecond part
```

### Forward References (`^`)

Reference a node defined **later** in the file (or by an importer). This is used for templates with "slots" to be filled:

```flow
# Template with a forward reference (slot)
@template |<<<Welcome, >>>|^username|<<<! You have >>>|^message_count|<<< messages.>>>|.

# Fill the slots later
@username |<<<Alice>>>|.
@message_count |<<<5>>>|.

@out |$template|.
```

**Output:**
```
Welcome, Alice! You have 5 messages.
```

### Imports

Import nodes from other FLOW files:

```flow
# Import all exported nodes from another file
+./path/to/other.flow |.

# Now you can reference nodes from that file
@combined |$imported_node|.
```

### File Includes

Embed the raw content of an external file (not a FLOW file):

```flow
@documentation
|<<<Documentation:
>>>
|++./README.md
|.
```

The content of `README.md` is inserted literally.

---

## 3. String Delimiters (CRITICAL)

FLOW has **four delimiter combinations** controlling whitespace handling. This is one of the most important concepts to master.

### Delimiter Reference Table

| Delimiter | Leading Whitespace | Trailing Whitespace | Use Case |
|-----------|-------------------|--------------------|-----------------------|
| `<<<...>>>` | **Trim** | **Trim** | Default, clean blocks |
| `<<<...>>` | **Trim** | **Preserve** | Need trailing newline |
| `<<...>>>` | **Preserve** | **Trim** | Need leading indent |
| `<<...>>` | **Preserve** | **Preserve** | Raw passthrough |

### Asymmetric Pairing Logic

- **Left delimiter** (`<<<` vs `<<`): Controls **leading** whitespace
  - `<<<` = 3 chevrons = **Trim** leading
  - `<<` = 2 chevrons = **Preserve** leading
  
- **Right delimiter** (`>>>` vs `>>`): Controls **trailing** whitespace
  - `>>>` = 3 chevrons = **Trim** trailing
  - `>>` = 2 chevrons = **Preserve** trailing

### Examples

#### Example 1: Default Trim-Trim (`<<<...>>>`)

```flow
@clean_block
|<<<
  This text has leading spaces and trailing newline.
  It will be trimmed on both ends.
>>>|.
```

**Output:** `This text has leading spaces and trailing newline.\n  It will be trimmed on both ends.`

(Leading and trailing whitespace from the delimiters is trimmed, but internal whitespace is preserved.)

#### Example 2: Preserve Trailing (`<<<...>>`)

```flow
@with_trailing_newline
|<<<Line one
Line two
>>|.
```

**Output:** `Line one\nLine two\n` (trailing newline preserved)

**Use case:** When the next content should start on a new line.

#### Example 3: Preserve Leading (`<<...>>>`)

```flow
@indented_code
|<<    indented_line>>>|.
```

**Output:** `    indented_line` (leading spaces preserved)

**Use case:** Preserving code indentation.

#### Example 4: Raw Passthrough (`<<...>>`)

```flow
@raw_content
|<<
Exactly as written.
  With all whitespace.
>>|.
```

**Output:** `\nExactly as written.\n  With all whitespace.\n`

**Use case:** Embedding pre-formatted content that must not be modified.

### Practical Tip: Joining with Newlines

When composing nodes, use `<<\n>>` to add explicit newlines:

```flow
@section_one |<<<First section content>>>|.
@section_two |<<<Second section content>>>|.

@combined
|$section_one|<<
>>|$section_two
|.
```

**Output:**
```
First section content
Second section content
```

The `<<\n>>` (or simply pressing Enter between `<<` and `>>`) adds exactly one newline.

---

## 4. Content Composition

### The Pipe Separator

Each pipe `|` separates content items within a node:

```flow
@multi_item
|<<<Part A>>>
|<<<Part B>>>
|<<<Part C>>>
|.
```

Content items are **concatenated directly** (no separator added):

**Output:** `Part APart BPart C`

### Adding Separators Between Items

To add newlines or other separators, use explicit strings:

```flow
@with_newlines
|<<<Part A>>>|<<
>>|<<<Part B>>>|<<
>>|<<<Part C>>>
|.
```

**Output:**
```
Part A
Part B
Part C
```

### Mixing References and Strings

```flow
@greeting |<<<Hello>>>|.
@name |<<<World>>>|.

@message
|$greeting
|<<<, >>>
|$name
|<<<! Welcome.>>>
|.

@out |$message|.
```

**Output:** `Hello, World! Welcome.`

### Composition Pattern: Section Blocks

For multi-section documents, use double newlines for paragraph separation:

```flow
@intro |<<<Introduction paragraph.>>>|.
@body |<<<Main body content.>>>|.
@conclusion |<<<Final thoughts.>>>|.

@document
|$intro|<<

>>|$body|<<

>>|$conclusion
|.
```

**Output:**
```
Introduction paragraph.

Main body content.

Final thoughts.
```

---

## 5. Style Parameters

Style parameters transform content during compilation. They're added after the node name with the syntax `|style.param=value`.

### Available Styles

| Style | Parameters | Effect |
|-------|------------|--------|
| `style.title` | Title text | Adds Markdown heading (level = node depth) |
| `style.wrap=xml` | `style.tag=name` | Wraps in `<name>...</name>` |
| `style.wrap=codeblock` | `style.tag=lang` | Wraps in ` ```lang ... ``` ` |
| `style.wrap=blockquote` | - | Prefixes each line with `> ` |
| `style.wrap=details` | `style.summary=text` | Wraps in `<details><summary>` |
| `style.list=type` | bullet/numbered/task/task-done | Formats as Markdown list |
| `style.divider` | - | Adds `---` after content |

### Example: Title Style

```flow
@section
|style.title=Welcome Section
|<<<This is the content under the heading.>>>
|.

@out |$section|.
```

**Output:**
```markdown
# Welcome Section
This is the content under the heading.
```

The heading level depends on node nesting depth (layer 0 = H1, layer 1 = H2, etc.).

### Example: XML Wrapping

```flow
@rules
|style.wrap=xml|style.tag=stopping_rules
|<<<
STOP if you see security issues.
STOP if config is missing.
>>>
|.

@out |$rules|.
```

**Output:**
```xml
<stopping_rules>
STOP if you see security issues.
STOP if config is missing.
</stopping_rules>
```

### Example: Code Block Wrapping

```flow
@code_sample
|style.wrap=codeblock|style.tag=python
|<<<
def hello():
    print("Hello, world!")
>>>
|.

@out |$code_sample|.
```

**Output:**
````markdown
```python
def hello():
    print("Hello, world!")
```
````

### Example: Blockquote Wrapping

```flow
@quote
|style.wrap=blockquote
|<<<
This is a quote.
It spans multiple lines.
>>>
|.

@out |$quote|.
```

**Output:**
```markdown
> This is a quote.
> It spans multiple lines.
```

### Example: Details (Collapsible)

```flow
@expandable
|style.wrap=details|style.summary=Click to expand
|<<<
Hidden content that appears when expanded.
>>>
|.

@out |$expandable|.
```

**Output:**
```html
<details>
<summary>Click to expand</summary>

Hidden content that appears when expanded.

</details>
```

### Example: List Formatting

```flow
@todo_list
|style.list=task
|<<<Buy groceries>>>
|<<<Write documentation>>>
|<<<Review pull request>>>
|.

@out |$todo_list|.
```

**Output:**
```markdown
- [ ] Buy groceries
- [ ] Write documentation
- [ ] Review pull request
```

List types:
- `bullet` → `- Item`
- `numbered` → `1. Item`, `2. Item`, ...
- `task` → `- [ ] Item`
- `task-done` → `- [x] Item`

### Example: Divider

```flow
@section_with_divider
|style.divider
|<<<Content followed by a horizontal rule.>>>
|.

@out |$section_with_divider|.
```

**Output:**
```markdown
Content followed by a horizontal rule.

---
```

### Combining Styles

Multiple styles can be combined:

```flow
@fancy_section
|style.title=Important Notice
|style.wrap=blockquote
|style.divider
|<<<This content gets a heading, blockquote formatting, and a divider.>>>
|.
```

---

## 6. Forward References (Slots/Templates)

Forward references create **template patterns** where a base file defines the structure and importing files fill in the slots.

### Basic Template Pattern

**Template file (`template.flow`):**
```flow
# Template with slots (forward references)
@greeting_template
|<<<Dear >>>|^recipient_name|<<<,

>>>|^greeting_body|<<<

Sincerely,
>>>|^sender_name
|.
```

**Using file (`letter.flow`):**
```flow
# Import the template
+./template.flow |.

# Fill the slots
@recipient_name |<<<John>>>|.
@greeting_body |<<<I hope this message finds you well.>>>|.
@sender_name |<<<Alice>>>|.

# Use the template (slots are now filled)
@out |$greeting_template|.
```

**Output:**
```
Dear John,

I hope this message finds you well.

Sincerely,
Alice
```

### VSCode Chat Agent Frontmatter Template

Real-world example from the ADHD framework:

**Template (`lib/provider/chatagent_frontmatter.flow`):**
```flow
# Forward references for complete YAML lines
@chatagent_frontmatter
|<<<--->>>
|^agent_name_line
|^agent_description_line
|^agent_argument_hint_line
|^agent_tools_line
|^agent_handoffs_lines
|<<<--->>>
|.
```

**Agent file (`my_agent.flow`):**
```flow
+./lib/provider/chatagent_frontmatter.flow |.

# Fill each slot with a complete YAML line
@agent_name_line |<<<name: "MyAgent">>>|.
@agent_description_line |<<<description: 'Does useful things.'>>>|.
@agent_argument_hint_line |<<<argument-hint: "What to do">>>|.
@agent_tools_line |<<<tools: ['read_file', 'search']>>>|.
@agent_handoffs_lines |<<<handoffs: []>>>|.

@out |$chatagent_frontmatter|.
```

**Output:**
```yaml
---
name: "MyAgent"
description: 'Does useful things.'
argument-hint: "What to do"
tools: ['read_file', 'search']
handoffs: []
---
```

### When to Use Forward vs Backward References

| Reference | Symbol | Use When |
|-----------|--------|----------|
| Backward `$` | `$node` | Referencing something already defined |
| Forward `^` | `^slot` | Creating a template slot to be filled later |

---

## 7. Library Organization (3-Layer Pattern)

For maintainable agent systems, organize reusable fragments into three layers:

```
lib/
├── provider/    # Layer 1: AI provider-specific formats
├── patterns/    # Layer 2: Universal agent patterns  
└── adhd/        # Layer 3: Framework-specific content
```

### Layer 1: Provider (`lib/provider/`)

Contains **provider-specific** formatting that changes when switching AI platforms.

Examples:
- `chatagent_frontmatter.flow` - VSCode Chat Agent YAML format
- `claude_system_prompt.flow` - Claude-specific system prompt structure
- `openai_function_format.flow` - OpenAI function calling format

**Key insight:** When migrating to a different AI provider, only this layer needs updating.

### Layer 2: Patterns (`lib/patterns/`)

Contains **universal agent patterns** that work across all providers.

Examples:
- `stopping_rules_base.flow` - Common stopping behaviors
- `core_philosophy.flow` - Reasoning principles
- `critical_rules_base.flow` - Critical constraints
- `workflow_template.flow` - Standard workflow structure

### Layer 3: Framework-Specific (`lib/adhd/`)

Contains content specific to **your framework or project**.

Examples:
- `framework_info.flow` - Links to framework documentation
- `project_patterns.flow` - Project-specific conventions
- `module_references.flow` - Common module paths

### Import Order

In your agent files, import from all three layers:

```flow
# Layer 3: Framework-specific
+./lib/adhd/framework_info.flow |.

# Layer 2: Universal patterns
+./lib/patterns/core_philosophy.flow |.
+./lib/patterns/stopping_rules_base.flow |.

# Layer 1: Provider-specific (template with slots)
+./lib/provider/chatagent_frontmatter.flow |.

# Now define agent-specific content and fill slots...
```

---

## 8. Complete Example

Let's build a complete agent from scratch.

### Step 1: Create Library Fragments

**`lib/patterns/stopping_rules_base.flow`:**
```flow
@stopping_rules_base
|<<<
STOP if you see a security vulnerability.
STOP if guessing APIs or paths—always verify.
NEVER edit protected files without permission.
>>>|.
```

**`lib/patterns/workflow_base.flow`:**
```flow
@workflow_base
|<<<
### 1. Context Gathering
- Read relevant files using `read_file`
- Search codebase using `search`
- Understand the problem fully before acting

### 2. Planning
- Break down the task into steps
- Identify potential risks
- Consider alternatives

### 3. Execution
- Implement changes incrementally
- Verify each step works
- Document your changes
>>>|.
```

**`lib/provider/chatagent_frontmatter.flow`:**
```flow
@chatagent_frontmatter
|<<<--->>>
|^agent_name_line
|^agent_description_line
|^agent_tools_line
|<<<--->>>
|.
```

### Step 2: Create the Main Agent File

**`my_helper_agent.flow`:**
```flow
# My Helper Agent
# A simple demonstration agent

# =============================================================================
# Imports
# =============================================================================
+./lib/patterns/stopping_rules_base.flow |.
+./lib/patterns/workflow_base.flow |.
+./lib/provider/chatagent_frontmatter.flow |.

# =============================================================================
# Fill Provider Template Slots
# =============================================================================
@agent_name_line |<<<name: "MyHelper">>>|.
@agent_description_line |<<<description: 'A helpful assistant for coding tasks.'>>>|.
@agent_tools_line |<<<tools: ['read_file', 'search', 'run_in_terminal']>>>|.

# =============================================================================
# Agent-Specific Content
# =============================================================================
@role_intro
|<<<
You are **MyHelper**, a friendly coding assistant.

Your goal is to help developers write clean, maintainable code.
>>>|.

# Wrap stopping rules in XML tag
@stopping_rules
|style.wrap=xml|style.tag=stopping_rules
|$stopping_rules_base
|.

# Wrap workflow in XML tag
@workflow
|style.wrap=xml|style.tag=workflow
|$workflow_base
|.

# =============================================================================
# Compose Final Output
# =============================================================================
@mode_content
|$role_intro|<<

>>|$stopping_rules|<<

>>|$workflow
|.

@modeInstructions
|style.wrap=xml|style.tag=modeInstructions
|<<<You are currently running in "MyHelper" mode.

>>|$mode_content
|.

@out
|$chatagent_frontmatter|<<

>>|$modeInstructions
|.
```

### Step 3: Compile and Verify

```bash
# Compile to see the output
python cores/flow_core/flow_cli.py compile my_helper_agent.flow

# Save to file
python cores/flow_core/flow_cli.py compile my_helper_agent.flow -o my_helper.agent.md

# View dependency graph
python cores/flow_core/flow_cli.py graph my_helper_agent.flow --format mermaid
```

**Expected Output:**
```markdown
---
name: "MyHelper"
description: 'A helpful assistant for coding tasks.'
tools: ['read_file', 'search', 'run_in_terminal']
---

<modeInstructions>
You are currently running in "MyHelper" mode.

You are **MyHelper**, a friendly coding assistant.

Your goal is to help developers write clean, maintainable code.

<stopping_rules>
STOP if you see a security vulnerability.
STOP if guessing APIs or paths—always verify.
NEVER edit protected files without permission.
</stopping_rules>

<workflow>
### 1. Context Gathering
- Read relevant files using `read_file`
- Search codebase using `search`
- Understand the problem fully before acting

### 2. Planning
- Break down the task into steps
- Identify potential risks
- Consider alternatives

### 3. Execution
- Implement changes incrementally
- Verify each step works
- Document your changes
</workflow>
</modeInstructions>
```

---

## 9. Common Patterns

### Pattern 1: Agent File Structure

Standard structure for agent files:

```flow
# 1. Imports (library fragments)
+./lib/adhd/framework_info.flow |.
+./lib/patterns/stopping_rules_base.flow |.
+./lib/provider/chatagent_frontmatter.flow |.

# 2. Slot definitions (for provider template)
@agent_name_line |<<<name: "AgentName">>>|.
# ... other slots

# 3. Agent-specific nodes
@role_intro |<<<...>>>|.
@custom_rules |<<<...>>>|.

# 4. Wrapped sections (stopping_rules, workflow, etc.)
@stopping_rules |style.wrap=xml|style.tag=stopping_rules|$stopping_rules_base|.|

# 5. Composition nodes
@mode_content |$role_intro|<<\n>>|$stopping_rules|...|.
@modeInstructions |style.wrap=xml|style.tag=modeInstructions|$mode_content|.

# 6. Final output
@out |$chatagent_frontmatter|<<\n>>|$modeInstructions|.
```

### Pattern 2: Extending Base Rules

Add agent-specific rules to base patterns:

```flow
+./lib/patterns/stopping_rules_base.flow |.

# Additional stopping rule specific to this agent
@stopping_rule_no_code
|<<<
STOP if you find yourself writing implementation code.
>>>|.

# Combine base + specific
@stopping_rules
|style.wrap=xml|style.tag=stopping_rules
|$stopping_rules_base|<<
>>|$stopping_rule_no_code
|.
```

### Pattern 3: Conditional Sections

Include sections only when relevant using composition:

```flow
@section_a |<<<Section A content>>>|.
@section_b |<<<Section B content>>>|.

# Include both
@full_doc |$section_a|<<\n\n>>|$section_b|.

# Include only section_a
@partial_doc |$section_a|.
```

### Pattern 4: Nested Lists

Create hierarchical lists:

```flow
@sub_items
|style.list=bullet
|<<<First sub-item>>>
|<<<Second sub-item>>>
|.

@main_items
|style.list=bullet
|<<<Main item one>>>
|$sub_items
|<<<Main item two>>>
|.
```

---

## 10. Compilation Commands

### Compile to Markdown

```bash
# Output to stdout
python cores/flow_core/flow_cli.py compile file.flow

# Save to file
python cores/flow_core/flow_cli.py compile file.flow -o output.md
```

### Validate Syntax

```bash
# Check for errors without compiling
python cores/flow_core/flow_cli.py validate file.flow
```

Reports all errors found (not just the first one).

### Generate Dependency Graph

```bash
# Mermaid format (default)
python cores/flow_core/flow_cli.py graph file.flow --format mermaid

# DOT format (for Graphviz)
python cores/flow_core/flow_cli.py graph file.flow --format dot

# JSON format (for programmatic use)
python cores/flow_core/flow_cli.py graph file.flow --format json
```

### Tokenize (Debugging)

```bash
# Show tokens
python cores/flow_core/flow_cli.py tokenize file.flow

# Verbose with line/column info
python cores/flow_core/flow_cli.py tokenize file.flow --verbose
```

### Parse (Debugging)

```bash
# Show AST structure
python cores/flow_core/flow_cli.py parse file.flow --verbose
```

---

## 11. Common Mistakes & Gotchas

### ❌ Mistake 1: Forgetting `|.` Terminator

```flow
# WRONG - missing terminator
@node |<<<content>>>

# CORRECT
@node |<<<content>>>|.
```

### ❌ Mistake 2: Referencing Undefined Nodes

```flow
# WRONG - $undefined doesn't exist
@out |$undefined|.

# CORRECT - define before referencing
@greeting |<<<Hello>>>|.
@out |$greeting|.
```

### ❌ Mistake 3: Wrong Delimiter for Whitespace

```flow
# WRONG - content gets trimmed, newline lost
@with_newline |<<<Line one
>>>|.

# CORRECT - use >> to preserve trailing
@with_newline |<<<Line one
>>|.
```

### ❌ Mistake 4: Circular References

```flow
# WRONG - infinite loop
@a |$b|.
@b |$a|.
```

The compiler will detect and report circular dependencies.

### ❌ Mistake 5: Forgetting to Import

```flow
# WRONG - $external_node not defined
@out |$external_node|.

# CORRECT - import first
+./external.flow |.
@out |$external_node|.
```

### ❌ Mistake 6: Wrong Path in Imports

```flow
# WRONG - path is relative to current file, not project root
+lib/patterns/base.flow |.

# CORRECT - use explicit relative path
+./lib/patterns/base.flow |.
```

### ⚠️ Gotcha: Forward References Must Be Filled

If you use `^slot` in a file, that slot MUST be defined somewhere (either in the same file or by an importing file). Otherwise, compilation fails.

### ⚠️ Gotcha: Style Order Matters

Styles are applied in phases: PRE (title) → WRAP → POST (divider). Understanding this helps predict output:

```flow
@section
|style.title=Heading
|style.wrap=blockquote
|<<<Content>>>
|.
```

**Output:**
```markdown
# Heading
> Content
```

The title is emitted BEFORE the wrapped content.

### ⚠️ Gotcha: Node Names Are Case-Sensitive

```flow
@Greeting |<<<Hello>>>|.
@greeting |<<<Hi>>>|.  # Different node!

@out |$greeting|.  # Outputs "Hi", not "Hello"
```

---

## Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════════╗
║                     FLOW QUICK REFERENCE                          ║
╠═══════════════════════════════════════════════════════════════════╣
║ SYNTAX                                                            ║
║   @name         Define node                                       ║
║   |.            End node                                          ║
║   $name         Reference node (backward)                         ║
║   ^name         Forward reference (slot)                          ║
║   +./file.flow  Import FLOW file                                  ║
║   ++./file.md   Include raw file                                  ║
║   # comment     Comment line                                      ║
╠═══════════════════════════════════════════════════════════════════╣
║ STRING DELIMITERS                                                 ║
║   <<<...>>>     Trim both ends (default)                          ║
║   <<<...>>      Trim leading, preserve trailing                   ║
║   <<...>>>      Preserve leading, trim trailing                   ║
║   <<...>>       Preserve both ends (raw)                          ║
╠═══════════════════════════════════════════════════════════════════╣
║ STYLES                                                            ║
║   style.title=Text          → Markdown heading                    ║
║   style.wrap=xml            → <tag>...</tag>                      ║
║   style.wrap=codeblock      → ```lang ... ```                     ║
║   style.wrap=blockquote     → > quoted                            ║
║   style.wrap=details        → <details>...</details>              ║
║   style.tag=name            → Tag/language name                   ║
║   style.summary=text        → Details summary                     ║
║   style.list=bullet         → - item                              ║
║   style.list=numbered       → 1. item                             ║
║   style.list=task           → - [ ] item                          ║
║   style.list=task-done      → - [x] item                          ║
║   style.divider             → --- after content                   ║
╠═══════════════════════════════════════════════════════════════════╣
║ CLI COMMANDS                                                      ║
║   compile file.flow         → Output markdown                     ║
║   compile file.flow -o out  → Save to file                        ║
║   validate file.flow        → Check for errors                    ║
║   graph file.flow           → Dependency graph (mermaid)          ║
║   tokenize file.flow        → Debug tokens                        ║
║   parse file.flow           → Debug AST                           ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Next Steps

1. **Explore existing examples** in `playground/samples/` and `playground/agents/sources/`
2. **Study the library structure** in `playground/agents/sources/lib/`
3. **Create your first agent** by copying and modifying an existing one
4. **Use the graph command** to visualize dependencies and understand structure

Happy FLOW-ing! 🌊
