---
applyTo: "**/*.flow"
---

# Flow DSL Format Rules

Guidelines for authoring `.flow` files using the FLOW DSL (Flexible Language for Orchestrating Workflows).

## File Structure

Every `.flow` file MUST have:
1. Header comment block (source, purpose, exports)
2. Import section (if using shared fragments)
3. Node definitions
4. Exactly ONE `@out` node (entry point)

## Node Definition Syntax

```flow
@node_id |param=value| <<<content>>>|.
```

- `@` — Node identifier prefix
- `|` — Pipe separator between parameters
- `|.` — Node terminator (required)

## Content Blocks

| Syntax | Behavior |
|--------|----------|
| `<<<content>>>` | Trim leading AND trailing newlines |
| `<<content>>` | Preserve all whitespace |
| `<<<content>>` | Trim leading, preserve trailing |
| `<<content>>>` | Preserve leading, trim trailing |

## Variable References

| Symbol | Usage | Requirement |
|--------|-------|-------------|
| `$name` | Backward reference | Node defined ABOVE |
| `^name` | Forward reference | Node defined BELOW |

To insert references inside content blocks:
```flow
|<<<text >>|$ref|<< more text>>>|.
```

## Style Parameters

| Parameter | Effect |
|-----------|--------|
| `style.title=<<Title>>` | Prepends `# Title` header |
| `style.wrap=xml` | Wraps in XML tags |
| `style.tag=tagname` | XML tag name (requires `style.wrap=xml`) |

## Import Syntax

```flow
# Import all nodes from file
+./path/to/file.flow |.

# Import specific nodes
+./path/to/file.flow |$node1|$node2|.

# Reference file without importing (for dependency tracking)
|<<<See >>|++./file.md|<<>>>|.
```

## Sidecar Pattern

Agent `.flow` files require a companion `.yaml` sidecar:

- **`.flow`** — Body content (nodes, workflow, rules)
- **`.yaml`** — Frontmatter metadata (name, description, tools, handoffs)

Both files share the same base name: `agent_name.flow` + `agent_name.yaml`

## Comments

```flow
# Single-line comment (outside content blocks)
```

Inside `<<<>>>` blocks, `#` is literal text, not a comment.

## Escaping

Escape only when `>>>|` or `>>|` appears literally in content:
```flow
|<<<Use >>>\| for literal>>>|.
```

## Critical Constraints

- **ONE @out node** — Required, serves as compilation entry point
- **No circular references** — `$a → $b → $a` causes error
- **Relative import paths** — Always relative to the `.flow` file
- **Never edit compiled output** — Edit `.flow` + `.yaml` source only

## Refresh Command

After editing `.flow` files:
```bash
adhd r -f
```

## Reference

Full DSL manual: `modules/dev/flow_core/manual.md`
