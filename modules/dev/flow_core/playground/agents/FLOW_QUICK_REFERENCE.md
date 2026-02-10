# FLOW Quick Reference (Agent Edition)

**Condensed reference for AI agents. For human tutorial, see FLOW_TUTORIAL.md (1194 lines).**

---

## Core Syntax

```flow
@node_name |<<<content>>>|.          # Basic node
@out |$node_name|.                   # Entry point (required)
# comment                            # Ignored line
```

### Node Definition Patterns

| Pattern | Syntax | Purpose |
|---------|--------|---------|
| Single-line | `@name \|<<<text>>>\|.` | Inline definition |
| Multi-line | `@name \|<<<\n  text\n>>>\|.` | Block content |
| Multi-item | `@name \|<<<A>>>\|<<<B>>>\|.` | Direct concatenation |
| Styled | `@name \|style.wrap=xml\|<<<text>>>\|.` | Apply formatting |

### References

| Type | Syntax | Timing | Use Case |
|------|--------|--------|----------|
| Backward | `$node` | After definition | Standard reuse |
| Forward | `^slot` | Before definition | Template slots |

### Imports

```flow
+./path/to/file.flow |.              # Import FLOW file
++./path/to/file.md |.               # Include raw file content
```

---

## String Delimiters (Critical)

**4 combinations control whitespace trimming:**

| Delimiter | Leading | Trailing | Pattern | Use Case |
|-----------|---------|----------|---------|----------|
| `<<<...>>>` | Trim | Trim | 3-3 | Default clean blocks |
| `<<<...>>` | Trim | **Keep** | 3-2 | Need trailing newline |
| `<<...>>>` | **Keep** | Trim | 2-3 | Preserve indentation |
| `<<...>>` | **Keep** | **Keep** | 2-2 | Raw passthrough |

**Rule:** Left chevron count controls leading, right controls trailing.

### Common Usage Patterns

```flow
# Add explicit newline between nodes
@combined |$node_a|<<\n>>|$node_b|.

# Double newline for paragraphs
@doc |$intro|<<\n\n>>|$body|.

# Preserve code indentation
@code |<<    def foo():>>|.

# Trailing newline for next line
@line1 |<<<First line\n>>|.
```

---

## Style Parameters

### Syntax

```flow
@node |style.param=value|style.param2=value2|<<<content>>>|.
```

### Available Styles

#### Wrapper Styles

| Style | Secondary Params | Output |
|-------|------------------|--------|
| `wrap=xml` | `tag=name` | `<name>content</name>` |
| `wrap=codeblock` | `tag=lang` | ` ```lang\ncontent\n``` ` |
| `wrap=blockquote` | - | `> line1\n> line2` |
| `wrap=details` | `summary=text` | `<details><summary>text</summary>\ncontent\n</details>` |

#### Formatting Styles

| Style | Value | Output | Notes |
|-------|-------|--------|-------|
| `title` | Text | `# Text\ncontent` | Heading level = node depth |
| `divider` | - | `content\n\n---` | Adds horizontal rule after |
| `list` | `bullet` | `- item` | Each pipe becomes list item |
| `list` | `numbered` | `1. item\n2. item` | Sequential numbering |
| `list` | `task` | `- [ ] item` | Unchecked checkbox |
| `list` | `task-done` | `- [x] item` | Checked checkbox |

### Style Application Order

1. **PRE phase**: `title` (emitted before content)
2. **WRAP phase**: `xml`, `codeblock`, `blockquote`, `details`
3. **POST phase**: `divider` (emitted after content)

---

## Forward References (Templates)

### Template Pattern

**template.flow:**
```flow
@template |<<<Hello, >>>|^name|<<<! You have >>>|^count|<<< items.>>>|.
```

**usage.flow:**
```flow
+./template.flow |.
@name |<<<Alice>>>|.
@count |<<<5>>>|.
@out |$template|.
```

**Output:** `Hello, Alice! You have 5 items.`

### VSCode Chat Agent Frontmatter Pattern

**lib/provider/chatagent_frontmatter.flow:**
```flow
@chatagent_frontmatter
|<<<--->>>|<<\n>>
|^agent_name_line|<<\n>>
|^agent_description_line|<<\n>>
|^agent_argument_hint_line|<<\n>>
|^agent_tools_line|<<\n>>
|^agent_handoffs_lines|<<\n>>
|<<<--->>>
|.
```

**agent.flow:**
```flow
+./lib/provider/chatagent_frontmatter.flow |.
@agent_name_line |<<<name: "MyAgent">>>|.
@agent_description_line |<<<description: 'Does things.'>>>|.
# ... fill other slots
@out |$chatagent_frontmatter|<<\n\n>>|$mode_content|.
```

---

## 3-Layer Library Pattern

```
lib/
├── provider/    # Layer 1: AI provider formats (VSCode/Claude/OpenAI)
├── patterns/    # Layer 2: Universal patterns (stopping_rules/workflow)
└── adhd/        # Layer 3: Framework-specific content
```

### Layer Responsibilities

| Layer | Changes When | Examples |
|-------|-------------|----------|
| `provider/` | Switch AI platform | `chatagent_frontmatter.flow`, `claude_system_prompt.flow` |
| `patterns/` | Never (universal) | `stopping_rules_base.flow`, `workflow_template.flow` |
| `adhd/` | Project-specific | `framework_info.flow`, `module_references.flow` |

### Standard Import Order

```flow
# Layer 3 (framework)
+./lib/adhd/framework_info.flow |.

# Layer 2 (universal patterns)
+./lib/patterns/core_philosophy.flow |.
+./lib/patterns/stopping_rules_base.flow |.

# Layer 1 (provider template)
+./lib/provider/chatagent_frontmatter.flow |.
```

---

## Compilation Commands

```bash
# Compile to stdout
python cores/flow_core/flow_cli.py compile file.flow

# Save to file
python cores/flow_core/flow_cli.py compile file.flow -o output.md

# Validate syntax (reports all errors)
python cores/flow_core/flow_cli.py validate file.flow

# Dependency graph (mermaid/dot/json)
python cores/flow_core/flow_cli.py graph file.flow --format mermaid
python cores/flow_core/flow_cli.py graph file.flow --format dot
python cores/flow_core/flow_cli.py graph file.flow --format json

# Debug tokens/AST
python cores/flow_core/flow_cli.py tokenize file.flow --verbose
python cores/flow_core/flow_cli.py parse file.flow --verbose
```

---

## Common Agent File Structure

```flow
# ============================================================================
# 1. IMPORTS
# ============================================================================
+./lib/adhd/framework_info.flow |.
+./lib/patterns/stopping_rules_base.flow |.
+./lib/patterns/workflow_base.flow |.
+./lib/provider/chatagent_frontmatter.flow |.

# ============================================================================
# 2. PROVIDER TEMPLATE SLOTS
# ============================================================================
@agent_name_line |<<<name: "AgentName">>>|.
@agent_description_line |<<<description: 'Agent purpose.'>>>|.
@agent_argument_hint_line |<<<argument-hint: "What to do">>>|.
@agent_tools_line |<<<tools: ['read_file', 'search']>>>|.
@agent_handoffs_lines |<<<handoffs: []>>>|.

# ============================================================================
# 3. AGENT-SPECIFIC CONTENT
# ============================================================================
@role_intro |<<<You are **AgentName**, expert in X.>>>|.

@custom_rule |<<<STOP if condition X occurs.>>>|.

# ============================================================================
# 4. WRAPPED SECTIONS
# ============================================================================
@stopping_rules
|style.wrap=xml|style.tag=stopping_rules
|$stopping_rules_base|<<\n>>|$custom_rule
|.

@workflow
|style.wrap=xml|style.tag=workflow
|$workflow_base
|.

# ============================================================================
# 5. COMPOSITION
# ============================================================================
@mode_content
|$role_intro|<<\n\n>>
|$stopping_rules|<<\n\n>>
|$workflow
|.

@modeInstructions
|style.wrap=xml|style.tag=modeInstructions
|<<<You are running in "AgentName" mode.\n\n>>
|$mode_content
|.

# ============================================================================
# 6. OUTPUT
# ============================================================================
@out
|$chatagent_frontmatter|<<\n\n>>
|$modeInstructions
|.
```

---

## Critical Constraints & Gotchas

### Syntax Rules

- **MUST terminate nodes with `|.`** - Parser error otherwise
- **Node names are case-sensitive** - `@Node` ≠ `@node`
- **`@out` required** - Defines entry point for compilation
- **No circular references** - Compiler detects and rejects
- **Forward refs must be filled** - `^slot` must be defined somewhere

### Path Rules

- **Imports are relative to current file** - Use `+./path` not `+path`
- **File includes use `++` prefix** - `++./file.md` not `+./file.md`

### Delimiter Selection

- **Wrong delimiter loses whitespace** - Match need to pattern
- **Use `<<\n>>` for explicit newlines** - Not just `\n`
- **Preserve trailing with `>>` not `>>>`** - For continuation lines

### Style Constraints

- **`wrap=xml` requires `tag=name`** - Specify tag name
- **`wrap=codeblock` requires `tag=lang`** - Specify language
- **`wrap=details` optional `summary=text`** - Default "Details"
- **Multiple wrappers not supported** - One wrap style per node
- **Title text cannot contain pipes** - Use string escaping if needed

### Reference Constraints

- **Cannot reference across compilation boundaries** - Each file compiles independently
- **Forward refs resolve at compile-time** - Not runtime
- **Undefined backward reference = error** - Must exist before use
- **Undefined forward reference = error** - Must be filled by importer or later in file

---

## Pattern: Extending Base Content

```flow
# Import base patterns
+./lib/patterns/stopping_rules_base.flow |.

# Define additional content
@stopping_rule_specific
|<<<STOP if agent-specific condition occurs.>>>
|.

# Combine base + specific
@stopping_rules
|style.wrap=xml|style.tag=stopping_rules
|$stopping_rules_base|<<\n>>|$stopping_rule_specific
|.
```

---

## Pattern: Conditional Sections

```flow
# Define optional sections
@section_debug |<<<Debug info...>>>|.
@section_prod |<<<Production info...>>>|.

# Include only what's needed
@output_debug |$section_debug|.
@output_prod |$section_prod|.

# Choose at compile time by changing @out
@out |$output_prod|.
```

---

## Pattern: Hierarchical Lists

```flow
# Sub-items (indented automatically)
@sub_items
|style.list=bullet
|<<<Sub-item A>>>
|<<<Sub-item B>>>
|.

# Main items with nested sub-items
@main_items
|style.list=bullet
|<<<Main item 1>>>
|$sub_items
|<<<Main item 2>>>
|.
```

**Output:**
```markdown
- Main item 1
- Sub-item A
- Sub-item B
- Main item 2
```

---

## Anti-Patterns (DO NOT)

| ❌ Don't | ✅ Do | Reason |
|---------|-------|--------|
| `@node \|<<<text>>>` | `@node \|<<<text>>>\|.` | Missing terminator |
| `@out \|$undefined\|.` | Define before use | Undefined reference |
| `<<<Line\n>>>` for trailing | `<<<Line\n>>` | Wrong delimiter |
| `@a \|$b\|.` + `@b \|$a\|.` | Break cycle | Circular reference |
| `+lib/file.flow \|.` | `+./lib/file.flow \|.` | Wrong relative path |
| Invent new patterns | Use existing library | Maintainability |

---

## Debugging Workflow

1. **Syntax error?** → Run `validate file.flow`
2. **Wrong output?** → Check delimiter choice (trim vs preserve)
3. **Missing content?** → Run `graph file.flow` to trace dependencies
4. **Undefined node?** → Check import order and node names (case-sensitive)
5. **Circular dependency?** → Run `graph file.flow` to visualize cycle
6. **Unexpected whitespace?** → Run `tokenize file.flow --verbose` to inspect

---

## File Type Conventions

| Extension | Purpose | Compile Target |
|-----------|---------|----------------|
| `.flow` | Source file | N/A (intermediate) |
| `.agent.md` | Compiled agent | From `agent_name.flow` |
| `.prompt.md` | Compiled prompt | From `prompt_name.flow` |
| `.instructions.md` | Compiled instructions | From `instruction_name.flow` |

---

## Quick Decision Tree

**Need to:**
- **Reuse content?** → Define node, use `$ref`
- **Create template?** → Use `^slot`, fill in importer
- **Format content?** → Apply `style.wrap=...`
- **Add heading?** → Use `style.title=...`
- **Preserve whitespace?** → Choose delimiter (2-2, 2-3, 3-2, 3-3)
- **Join with newline?** → Use `|<<\n>>|` between items
- **Share across agents?** → Move to `lib/patterns/`
- **Provider-specific?** → Move to `lib/provider/`
- **Project-specific?** → Move to `lib/adhd/`

---

## Minimal Working Example

**hello.flow:**
```flow
@greeting |<<<Hello, World!>>>|.
@out |$greeting|.
```

**Compile:**
```bash
python cores/flow_core/flow_cli.py compile hello.flow
```

**Output:**
```
Hello, World!
```

---

**End of Quick Reference. Total: ~280 lines (vs 1194 in tutorial).**
**For detailed explanations and examples, see FLOW_TUTORIAL.md.**
