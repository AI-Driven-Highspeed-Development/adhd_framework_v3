# Exceptions Core

Lightweight module defining `ADHDError`, the base exception for all anticipated framework failures.

## Overview
- Provides a single base exception representing predictable operational failures
- Encourages `raise ... from exc` to preserve original tracebacks
- Keeps unexpected bugs (TypeError, AttributeError, etc.) unhandled for fast diagnostics

## Features
- **Unified error type** – callers catch `ADHDError` to handle known failure modes in one place
- **Context preservation** – designed for `raise ADHDError(...) from exc` to keep tracebacks intact
- **Zero dependencies** – standard library only

## Quickstart

```python
from exceptions_core import ADHDError

def fetch_remote(path: str) -> str:
    try:
        return do_network_call(path)
    except NetworkError as exc:
        raise ADHDError(f"Failed to fetch {path}: {exc}") from exc

try:
    fetch_remote("config.yml")
except ADHDError as exc:
    logger.error(exc)
```

## API

```python
class ADHDError(Exception):
    """Base exception for anticipated, application-specific failures."""
    pass
```

## Notes
- Reserve `ADHDError` for recoverable, expected situations (API failures, validation issues, CLI errors).
- Never swallow unexpected exceptions; letting them crash keeps debugging fast.

## Requirements & prerequisites
- Python standard library only (no external dependencies)

## Troubleshooting
- **`ADHDError` lacks original traceback** – ensure you use `raise ADHDError(...) from exc` when wrapping.
- **Catching ADHDError hides bugs** – keep catches narrow and re-raise when you cannot remediate.
- **Need richer context** – embed remediation tips inside the error message; the exception carries only the string you provide.

## Module structure

```
exceptions_core/
├─ __init__.py              # exports ADHDError
├─ adhd_exceptions.py       # ADHDError definition
├─ exceptions.instructions.md  # agent instructions
├─ pyproject.toml           # module metadata
└─ README.md                # this file
```

## See also
- Modules Controller Core – raises `ADHDError` for module discovery failures
- GitHub API Core – wraps API failures in `ADHDError`
- Creator Common Core – raises `ADHDError` when repo provisioning fails