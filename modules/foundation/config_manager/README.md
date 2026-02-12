# Config Manager

Singleton JSON configuration system with automatic typed-accessor code generation.

## Overview

- Reads `.config` (JSON) and generates strongly-typed dataclass accessors
- Singleton instance provides project-wide configuration access via `cm.config`
- Discovers module `.config_template` files and consolidates them into a single `.config`

## Features

- Auto-generated nested dataclasses mirroring JSON structure (`config_keys.py`)
- Runtime save and regeneration via `save_config()`
- Raw dict access on every node via `___DATA___` and `dict_get()`
- Template consolidation: scans modules for `.config_template` and merges into `.config`
- Preserves existing config values during regeneration by default

## Quickstart

```python
from config_manager import ConfigManager

cm = ConfigManager()
value = cm.config.my_module.path.data

# Update and persist (regenerates typed keys)
cm.save_config({"database": {"host": "db.local", "port": 5433}})

# Singleton guarantee
assert ConfigManager() is cm
```

Generate `.config` from module templates:

```python
from config_manager import ConfigTemplate

ct = ConfigTemplate()
ct.generate_config(preserve_existing=True)
ct.list_config_summary()
```

## API

```python
class ConfigManager:                                        # singleton
    def __init__(self, config_path: str = ".config", verbose: bool = False) -> None: ...
    config: ConfigKeys                                      # generated typed accessors root
    raw_config: dict                                        # raw JSON dict
    def save_config(self, key_value: dict[str, Any] = None) -> None: ...

class ConfigTemplate:
    def __init__(self, config_file_path: str = ".config") -> None: ...
    def generate_config(self, preserve_existing: bool = True) -> bool: ...
    def list_config_summary(self) -> None: ...
    def find_config_templates(self) -> dict[str, str]: ...
    def consolidate_configs(self) -> dict[str, Any]: ...
    def merge_with_existing(self, preserve_existing: bool = True) -> dict[str, Any]: ...
```

## Notes

- `config_keys.py` is auto-generated — do not edit it manually.
- First-level key class names may append `_P`/`_U`/`_M` suffixes for Plugin/Util/Manager disambiguation.
- Lists of dicts use union schemas to derive item shapes.
- Each generated class has `___DATA___: Dict[str, Any]` for raw dict access.

## Requirements & prerequisites

- `logger-util`
- `modules-controller-core`
- `pyyaml>=6.0`

## Troubleshooting

- **Import errors for generated keys**: Ensure `ConfigManager()` has been initialized at least once to generate `config_keys.py`.
- **Changes not reflected**: Call `cm.save_config(...)` or re-initialize `ConfigManager()`.
- **JSON parse errors**: Confirm `.config` is valid JSON.
- **Path issues**: The module assumes `os.getcwd()` is the project root.
- **Template not picked up**: Ensure your module has a `.config_template` file and is discoverable by Modules Controller.

## Module structure

```
config_manager/
├─ __init__.py                   # exports ConfigManager, ConfigTemplate
├─ config_manager.py             # singleton manager and key generation
├─ config_template.py            # template discovery and consolidation
├─ config_keys.py                # generated typed accessors (do not edit)
├─ config_manager.instructions.md  # agent instructions
├─ refresh.py                    # refresh hook
├─ pyproject.toml                # package metadata and dependencies
└─ README.md                     # this file
```

## See also

- Logger Utility — logging used internally
- Modules Controller Core — module discovery for template scanning
- CLI Manager — uses Config Manager for configuration access
