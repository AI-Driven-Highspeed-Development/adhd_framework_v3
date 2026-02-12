# Logger Utility

Centralized, pluggable logging for console and files built on Python's `logging` module.

## Overview

- Named per-name singleton loggers with optional verbose (DEBUG) mode
- Pluggable console styles: CompactStyle (default) and NormalStyle
- Optional file logging with daily timestamped filenames
- Central logger and convenience functions for quick one-liner logging

## Features

- Pluggable console styles
  - `CompactStyle` (default): succinct, TTY-aware colors, single-letter level indicators
  - `NormalStyle`: verbose classic formatting
- Per-name singleton: `Logger(name="X")` always returns the same wrapper
- Runtime style switching via `set_style()` or `set_logger_style()`
- File logging with `ConcurrentFileHandler` using `fcntl` for process safety
- Async file writes via `QueueHandler` / `QueueListener`
- Central logger (`get_central_logger()`) and convenience shorthands (`log_debug`, `log_info`, etc.)
- Global overrides: `LEVEL_OVERRIDE`, `LOG_TO_FILE_OVERRIDE`, `LOG_FILE_PATH_OVERRIDE`

## Quickstart

```python
from logger_util import Logger, set_logger_style, NormalStyle

# Per-name singleton wrapper
log = Logger(name="MyModule", verbose=True)
log.debug("Debug in compact style (default)")

# Switch to normal style at runtime
set_logger_style(log, NormalStyle())
log.info("Now in normal style")

# File logging (default path: ./logs/MyModule_YYYYMMDD.log)
Logger(name="MyModule", log_to_file=True).info("Also logged to file")
```

Quick one-liner logging via convenience functions:

```python
from logger_util import log_info, log_error

log_info("Application started")
log_error("Something went wrong")
```

## API

```python
class Logger:                                               # per-name singleton
    def __init__(self, name: str = "Logger", level: str | None = None,
                 log_to_file: bool | None = None, log_file_path: str | None = None,
                 verbose: bool | None = None, style: LoggerStyle | None = None) -> None: ...
    def configure(self, *, level: str | None = None, log_to_file: bool | None = None,
                  log_file_path: str | None = None, verbose: bool | None = None,
                  style: LoggerStyle | None = None) -> None: ...
    def get_logger(self) -> logging.Logger: ...
    def set_style(self, style: LoggerStyle) -> None: ...
    def set_level(self, level: str) -> None: ...
    def debug(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...
    def critical(self, message: str) -> None: ...
    def add_custom_handler(self, handler: logging.Handler) -> None: ...
    def remove_all_handlers(self) -> None: ...

# Module-level functions
def get_central_logger(verbose: bool = False, log_to_file: bool = True) -> logging.Logger: ...
def set_logger_style(logger: logging.Logger | Logger, style: LoggerStyle | None = None) -> None: ...
def log_debug(message: str) -> None: ...
def log_info(message: str) -> None: ...
def log_warning(message: str) -> None: ...
def log_error(message: str) -> None: ...
def log_critical(message: str) -> None: ...

# Styles
class LoggerStyle(ABC): ...                                 # abstract base
class NormalStyle(LoggerStyle): ...                          # verbose classic
class CompactStyle(LoggerStyle): ...                         # succinct colored
```

## Notes

- Stream handler is created on demand by `apply_style` and reused.
- File handlers always use NormalStyle regardless of console style.
- Child loggers inherit handlers; avoid adding duplicate handlers to children.
- `get_central_logger()` returns a stdlib `logging.Logger`, not a `Logger` wrapper.

## Requirements & prerequisites

- `rich>=13.0`

## Troubleshooting

- **Duplicate messages**: Don't attach multiple handlers to the same logger name.
- **No color output**: Ensure you are running in a TTY; some terminals and CI strip ANSI codes.
- **Missing log files**: Ensure `./logs/` is writable or set `log_file_path` explicitly.
- **Too verbose**: Use `verbose=False` or set level to `"INFO"`.
- **Central logger not logging debug**: Call `get_central_logger(verbose=True)` on first use.

## Module structure

```
logger_util/
├─ __init__.py                  # exports Logger, styles, helpers
├─ logger.py                    # Logger class and module-level functions
├─ logger_style.py              # LoggerStyle base + NormalStyle
├─ compact_style.py             # CompactStyle + apply_style
├─ logger_util.instructions.md  # agent instructions
├─ pyproject.toml               # package metadata and dependencies
└─ README.md                    # this file
```

## See also

- Config Manager — uses Logger for all internal logging
- Exceptions Core — exception types that integrate with logging
- CLI Manager — uses Logger internally
