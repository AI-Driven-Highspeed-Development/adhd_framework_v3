# Temp Files Manager

Lightweight manager for creating, tracking, and cleaning temporary directories.

## Overview

- Centralizes temporary directory creation and cleanup across the project
- Resolves a base temp directory from Config Manager (platform-aware: Unix / Windows)
- Creates uniquely named subdirectories per operation and safely removes them

## Features

- Platform-aware base directory resolution from `.config` (unix_temp / windows_temp)
- Unique subdirectory creation with configurable prefix
- Per-instance tracking pool for cleanup
- Recursive cleanup of individual paths or all tracked paths
- Resilient deletion via `shutil.rmtree(ignore_errors=True)`

## Quickstart

```python
from temp_files_manager import TempFilesManager

tfm = TempFilesManager()                  # base dir from .config
work_dir = tfm.make_dir(prefix="clone")   # creates a unique temp directory

# ... do work in work_dir ...

tfm.cleanup(work_dir)                     # remove this directory
tfm.cleanup_all()                         # remove all tracked directories
```

Override the base directory explicitly:

```python
tfm = TempFilesManager(base_dir="/tmp/my_module")
```

## API

```python
class TempFilesManager:
    def __init__(self, base_dir: str | None = None) -> None: ...
    def make_dir(self, prefix: str = "tmp") -> str: ...
    def cleanup(self, path: str) -> None: ...
    def cleanup_all(self) -> None: ...
```

## Notes

- `make_dir` returns the absolute path to a newly created directory under the resolved base dir.
- `cleanup` is safe to call even if the path was already deleted.
- `cleanup_all` iterates the tracked pool and removes every directory created by the instance.

## Requirements & prerequisites

- `config-manager`
- `logger-util`

## Troubleshooting

- **Missing config keys**: Ensure `.config` has `temp_files_manager.path.unix_temp` (or `windows_temp`), or pass `base_dir` explicitly.
- **Permission errors**: Pick a writable base directory and verify nothing is locking the path.
- **Windows path issues**: Escape backslashes properly in `.config` and confirm the drive exists.
- **Stale directories**: Call `cleanup_all()` at the end of your workflow to avoid leftovers.

## Module structure

```
temp_files_manager/
├─ __init__.py               # exports TempFilesManager
├─ temp_files_manager.py     # implementation
├─ .config_template          # default config schema
├─ pyproject.toml            # package metadata and dependencies
└─ README.md                 # this file
```

## See also

- Config Manager — configuration access for base directory resolution
- Logger Utility — logging used internally
- GitHub API Core — uses temp directories managed here for clone operations
