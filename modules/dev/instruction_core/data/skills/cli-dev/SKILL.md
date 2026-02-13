---
name: cli-dev
description: "CLI command registration and development patterns for ADHD Framework modules. Covers CLIManager integration, handler function signatures, register_cli() conventions, CommandArg spec, argument naming constraints, user feedback rules, and refresh integration. Use this skill when creating or modifying *_cli.py files, registering CLI commands, or understanding the ADHD CLI architecture."
---

# CLI Development

A guide for building CLI command registration scripts that integrate with the ADHD Framework's centralized `CLIManager`.

## When to Use
- Creating a new `*_cli.py` file for a module
- Registering commands with the centralized `CLIManager`
- Adding arguments or subcommands to existing CLI modules
- Understanding handler signature requirements
- Debugging CLI command routing issues

---

## Core Principles

1. **Centralized Registration**: All CLI commands register through `CLIManager` — never create standalone argparse scripts.
2. **Consistent Handler Signature**: Every handler accepts `args: argparse.Namespace` and returns `int`.
3. **User Feedback Always**: Silent commands are NOT acceptable. Use `_print_result()` for JSON output.
4. **Package Imports**: Use `from modules.runtime.cli_manager import CLIManager, ModuleRegistration, Command, CommandArg`.
5. **Refresh Integration**: The module's `refresh.py` MUST call `register_cli()`.

---

## CLI Development SOP

### Step 1: Create the `*_cli.py` File

Every `*_cli.py` MUST contain:
- Handler functions that accept `argparse.Namespace` and return `int`
- A `register_cli()` function that registers commands with `CLIManager`

### Step 2: Write Handler Functions

Each handler MUST:
- Accept `args: argparse.Namespace` as its sole parameter
- Return `int` (0 = success, non-zero = error)
- Access arguments via `args.<argname>`
- Return `_print_result(result)` where result has at least `{"success": bool}`

### Step 3: Register Commands

Define `register_cli() -> None` using `CLIManager().register_module(ModuleRegistration(...))`.

Handler path format: `"modules.<layer>.<module_name>.<filename>:<function_name>"`

### Step 4: Wire Refresh Integration

In the module's `refresh.py`:
```python
from .<module>_cli import register_cli
register_cli()
```

### Step 5: Choose a Short Name

Pick a concise, unique 2–4 letter alias for the module (e.g., `"fl"` for flow, `"ic"` for instruction_core).

---

## Reserved Argument Names

CLI commands MUST NOT use these argument names (they collide with argparse namespace):

| Reserved | Use Instead |
|----------|-------------|
| `module` | `target_module`, `module_name` |
| `command` | `target_command`, `cmd_name` |

---

## CommandArg Reference

See [cli-patterns.md](references/cli-patterns.md) for the full `CommandArg` field reference, decorator patterns, and complete registration examples.

---

## Quick Reference: _print_result Pattern

```python
def _print_result(result: dict) -> int:
    """Print result as JSON and return exit code."""
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("success", True) else 1
```

Every handler MUST return `_print_result(result)`.

---

## Critical Rules

- **Never** create standalone argparse scripts — always use `CLIManager`.
- **Never** use reserved argument names (`module`, `command`).
- **Never** have silent handlers — always output via `_print_result()`.
- **Always** wire `register_cli()` in `refresh.py`.
- **Always** use the handler path format: `modules.<layer>.<module>.<file>:<func>`.

---

## Checklist

- [ ] File named `*_cli.py` with handler functions and `register_cli()`
- [ ] All handlers accept `argparse.Namespace`, return `int`
- [ ] All handlers return `_print_result(result)`
- [ ] `register_cli()` uses correct handler path format
- [ ] Short name is 2–4 chars and unique
- [ ] No reserved argument names used
- [ ] `refresh.py` calls `register_cli()`
- [ ] Template matches [cli-template.py.template](assets/cli-template.py.template)
