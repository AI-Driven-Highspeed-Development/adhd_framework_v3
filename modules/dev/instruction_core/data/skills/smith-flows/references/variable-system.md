# Flow Variable System Reference

Variable references enable node composition — the core mechanism for building modular, reusable flow content.

---

## Variable Directions

| Symbol | Direction | Requirement |
|--------|-----------|-------------|
| `$name` | Backward reference | Node must be defined ABOVE current position |
| `^name` | Forward reference | Node must be defined BELOW current position |

---

## Basic Usage

```flow
@greeting |<<<Hello!>>>|.

@out |$greeting|.
```

Result: `Hello!`

---

## Inserting References Inside Content Blocks

Inside content blocks, `$name` is treated as literal text. To insert a variable reference mid-content, close and reopen the content block:

```flow
@out |<<<Welcome! >>|$greeting|<< How are you?>>>|.
```

Result: `Welcome! Hello! How are you?`

---

## Multiple References

Chain multiple references with pipes:

```flow
@part_a |<<<First part.>>>|.
@part_b |<<<Second part.>>>|.

@combined
|$part_a
|<<
>>|$part_b
|.
```

The `|<<\n>>|` pattern inserts a newline separator between referenced nodes.

---

## Imported Variables

When importing from another file, imported node names become available as `$name`:

```flow
+../_lib/patterns/core_philosophy.flow |.

@philosophy
|style.wrap=xml|style.tag=core_philosophy
|<<<1. **Principle**: Description>>>
|$truthfulness_principle
|.
```

The `$truthfulness_principle` node is provided by the imported file.

---

## Scoping Rules

| Rule | Detail |
|------|--------|
| Variables are file-scoped | A node defined in one file is not visible in another unless imported |
| Import brings nodes into scope | `+./file.flow \|.` makes all exported nodes from that file available |
| Selective import | `+./file.flow \|$node_a\|$node_b\|.` imports only named nodes |
| `@out` is never imported | The `@out` node from imported files is always excluded |
| No circular dependencies | `$a → $b → $a` across files causes a compilation error |
