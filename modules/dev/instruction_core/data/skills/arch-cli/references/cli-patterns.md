# CLI Patterns Reference

Detailed reference for CLI registration patterns, `CommandArg` fields, and complete examples.

---

## CommandArg Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Argument name. Positional if no `-`, optional if starts with `--` |
| `help` | str | Help text shown in `--help` |
| `short` | str | Short flag alias (e.g., `"-v"` for `--value`) |
| `type` | str | `"str"`, `"int"`, `"float"`, `"bool"` |
| `required` | bool | For optional args, whether required |
| `default` | Any | Default value if not provided |
| `nargs` | str | `"?"` (0 or 1), `"*"` (0+), `"+"` (1+) |
| `choices` | list | Restrict to specific values |
| `action` | str | `"store_true"`, `"store_false"`, `"count"` |

---

## Handler Path Format

```
modules.<layer>.<module_name>.<filename>:<function_name>
```

Examples:
- `"modules.runtime.secret_manager.secret_cli:list_secrets"`
- `"modules.dev.flow_core.flow_cli:compile_flows"`
- `"modules.foundation.config_manager.config_cli:get_value"`

---

## Controller Access Pattern

Lazy-initialize a singleton controller to avoid import-time side effects:

```python
_controller: MyController | None = None

def _get_controller() -> MyController:
    """Get or create the controller instance."""
    global _controller
    if _controller is None:
        _controller = MyController()
    return _controller
```

---

## Complete Registration Example

```python
def register_cli() -> None:
    """Register download_manager commands with CLIManager."""
    cli = CLIManager()
    cli.register_module(ModuleRegistration(
        module_name="download_manager",
        short_name="dl",
        description="File download utilities",
        commands=[
            Command(
                name="fetch",
                help="Download a file from URL",
                handler="modules.runtime.download_manager.download_cli:download_file",
                args=[
                    CommandArg(name="url", help="URL to download"),
                    CommandArg(name="--output", short="-o", help="Output path"),
                    CommandArg(name="--quiet", short="-q", action="store_true", help="Suppress output"),
                    CommandArg(name="--retries", type="int", default=3, help="Number of retries"),
                ],
            ),
            Command(
                name="list",
                help="List downloaded files",
                handler="modules.runtime.download_manager.download_cli:list_downloads",
            ),
        ],
    ))
```

---

## Argument Type Examples

### Positional argument
```python
CommandArg(name="url", help="URL to download")
```

### Optional flag
```python
CommandArg(name="--verbose", short="-v", action="store_true", help="Verbose output")
```

### Optional with value
```python
CommandArg(name="--count", short="-c", type="int", default=1, help="Number of items")
```

### Restricted choices
```python
CommandArg(name="--format", choices=["json", "yaml", "text"], default="json", help="Output format")
```

### Multiple values
```python
CommandArg(name="--tags", nargs="+", help="One or more tags")
```
