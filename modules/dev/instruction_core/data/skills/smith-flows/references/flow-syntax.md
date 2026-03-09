# Flow DSL Syntax Reference

Detailed syntax specification for the FLOW DSL (Flexible Language for Orchestrating Workflows).

---

## Node Definition

```flow
@node_id |param=value| <<<Content goes here.>>>|.
```

| Element | Purpose |
|---------|---------|
| `@` | Defines a node with an identifier |
| `\|` | Pipe separator for parameters |
| `<<<>>>` | Content block (trim mode: strips leading/trailing newlines) |
| `<<>>` | Content block (preserve mode: keeps whitespace) |
| `\|.` | End of node definition (required) |

### Minimum Valid File

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

Inside `<<<>>>` blocks, `#` is literal text, not a comment.

---

## Style Parameters

| Parameter | Effect |
|-----------|--------|
| `style.title=<<Title>>` | Adds `# Title` header |
| `style.wrap=xml` | Wraps content in XML tags |
| `style.tag=tagname` | Tag name for XML wrapping (requires `style.wrap=xml`) |

### Example

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

## Import Syntax

### Import Nodes from Another File

```flow
# Import all exported nodes
+../_lib/patterns/core_philosophy.flow |.

# Import specific nodes
+./shared.flow |$node_a|$node_b|.
```

The `@out` node from imported files is always ignored.

### File References (Non-Import)

Use `++` to reference files without importing (for dependency tracking):

```flow
@workflow |<<<See instructions in >>|++./path/to/file.md|<<>>>|.
```

---

## Comments

```flow
# Single-line comment (outside content blocks)
```

Inside content blocks, `#` is literal text, not a comment.

---

## Escaping

Escape only when `>>>|` or `>>|` appears literally in content:

```flow
|<<<Use >>>\| for literal>>>|.
```

---

## Critical Constraints

| Rule | Detail |
|------|--------|
| **ONE @out node** | Required, serves as compilation entry point |
| **No circular references** | `$a → $b → $a` causes error |
| **Relative import paths** | Always relative to the `.flow` file location |
| **Never edit compiled output** | Edit `.flow` + `.yaml` source only |
