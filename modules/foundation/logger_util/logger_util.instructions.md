---
applyTo: "modules/**/*.py,project/**/*.py,*.py"
---

Logger Util:
- Purpose: Centralized logging helpers that standardize formatting, verbose toggles, and optional file handlers across the framework using Python's `logging` module.
- Usage:
```python
from modules.foundation.logger_util import Logger, get_central_logger, set_logger_style, log_info
from modules.foundation.logger_util.logger_style import NormalStyle

# Standard usage
log = Logger(name="MyModule", verbose=True, log_to_file=True)
log.debug("Compact style output")

# Style switching
set_logger_style(log, NormalStyle())
log.info("Now using the normal style")

# Central logger (singleton "mother of all loggers")
get_central_logger(verbose=True).debug("Central diagnostics")

# Convenience functions (uses central logger)
log_info("Quick info log")
```
- Verbose handling: pass `verbose=True` (or set `level`) when constructing `Logger` or retrieving the central logger to enable DEBUG output; defaults to INFO.
- Handler safety: `Logger` instances are singletons per name; rely on provided helpers for style/level changes to avoid duplicate handlers.
