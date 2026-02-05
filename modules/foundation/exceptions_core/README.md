# Exceptions Core

Lightweight module that defines `ADHDError`, the canonical application error type for predictable failures.

## Overview
- Provides a single base exception that represents anticipated operational failures
- Encourages `raise ... from exc` usage so call stacks retain the original cause
- Keeps unexpected bugs (TypeError, AttributeError, etc.) unhandled to preserve crash diagnostics

## Features
- **Unified error type** – callers can catch `ADHDError` to handle known failure modes in one place
- **Context preservation** – docs emphasize `raise ADHDError(...) from exc` to keep tracebacks intact
- **Zero dependencies** – only standard library

## Quickstart

```python
from cores.exceptions_core.adhd_exceptions import ADHDError

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
- Python standard library only

## Troubleshooting
- **`ADHDError` lacks original traceback** – ensure you use `raise ADHDError(...) from exc` when wrapping.
- **Catching ADHDError hides bugs** – keep catches narrow and re-raise when you cannot remediate.
- **Need richer context** – embed remediation tips inside the error message; the exception carries only the string you provide.

## Module structure

```
cores/exceptions_core/
├─ __init__.py          # package marker
├─ adhd_exceptions.py   # ADHDError definition
├─ .config_template     # config schema placeholder
├─ init.yaml            # module metadata
└─ README.md            # this file
```

## See also
- GitHub API Core – wraps gh failures in `ADHDError`
- Creator Common Core – raises `ADHDError` when repo provisioning fails
- Modules Controller Core – propagates errors when YAML metadata cannot be read