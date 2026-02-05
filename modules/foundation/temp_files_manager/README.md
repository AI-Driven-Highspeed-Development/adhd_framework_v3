# Temp Files Manager

Small, dependency‑light manager for creating, tracking, and cleaning temporary directories used by other modules (e.g., GitHub operations). It centralizes temp path selection via project configuration and provides a tiny, safe API.

## Overview
- Centralizes where temporary working folders are created across the project
- Resolves a base temp directory from `.config` under `temp_files_manager.path`
- Creates uniquely named subdirectories for each operation and cleans them up safely

## Features
- Base dir resolution from config (Windows and Unix):
	- `.config.temp_files_manager.path.unix_temp` on Linux/macOS
	- `.config.temp_files_manager.path.windows_temp` on Windows
- Create and track per-operation temp directories
- Recursive cleanup of a specific path or all tracked paths
- Small, dependency-light implementation

## Quickstart

Basic creation and cleanup:

```python
from managers.temp_files_manager.temp_files_manager import TempFilesManager

tfm = TempFilesManager()  # base dir resolved from .config
work_dir = tfm.make_dir(prefix="clone")

# ... do work that writes into work_dir ...

tfm.cleanup(work_dir)  # remove this temp directory
```

Clean up everything tracked so far:

```python
tfm.cleanup_all()
```

Override the base directory explicitly (bypasses config resolution):

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
- Base directories are read from `.config.temp_files_manager.path`. Example snippet:

```json
{
	"module_name": "temp_files_manager",
	"path": {
		"data": "./project/data/temp_files_manager",
		"unix_temp": "/tmp/adhd-framework",
		"windows_temp": "C:\\Temp\\adhd-framework"
	}
}
```

- `make_dir` returns the absolute path to a newly created directory under the resolved base dir.
- `cleanup` removes a path recursively; it is safe to call even if the path was already deleted.
- `cleanup_all` iterates over the tracked pool and removes every directory created by the instance.
- Implementation relies on `shutil.rmtree(..., ignore_errors=True)` for resilience and logs every action via Logger Utility.

## Requirements & prerequisites
- Python standard library only

## Troubleshooting
- **Missing config keys** – ensure `.config.temp_files_manager.path.unix_temp` or `.windows_temp` exists, or pass `base_dir` to the constructor.
- **Permission errors** – pick a writable base directory and verify antivirus tools aren’t locking the path.
- **Windows path issues** – escape backslashes properly in `.config` and confirm the drive exists.

## Module structure

```
managers/temp_files_manager/
├─ __init__.py                 # package marker
├─ .config_template            # default config schema for this module
├─ temp_files_manager.py       # implementation
├─ init.yaml                   # module metadata
└─ README.md                   # this file
```

## See also
- YAML Reading Core: read/write YAML files in your temporary workspace
- GitHub API Core: fetch/clone files into temp directories managed here