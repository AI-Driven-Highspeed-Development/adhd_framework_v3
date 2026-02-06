# Integration Test Plan — Cross-Module

> Tests that exercise real interactions between multiple modules within the framework workspace. No mocking of ADHD modules (external tools may be mocked).

---

## Test Location

All integration tests go in: `tests/integration/`

Existing: `test_refresh_integration.py` (241 LOC, 6 test classes)

---

## New Integration Test Files

### tests/integration/test_module_discovery_integration.py

Exercises `modules_controller_core` scanning the real `modules/` directory.

```
test_scan_discovers_all_foundation_modules
    - Assert: exceptions_core, logger_util, config_manager, cli_manager,
              modules_controller_core, temp_files_manager, workspace_core
    - All have layer=foundation

test_scan_discovers_all_dev_modules
    - Assert: adhd_mcp, creator_common_core, github_api_core,
              instruction_core, module_creator_core, project_creator_core, uv_migrator_core
    - All have layer=dev

test_scan_reports_correct_total_count
    - Assert: total modules == 14 (or current count)

test_get_module_by_name_real_modules
    - For each known module, assert get_module_by_name returns it
    - Test case-insensitive: "Logger_Util" vs "logger_util"

test_module_info_has_valid_metadata
    - For each module: assert name, version, layer, path are populated
    - Assert path exists on filesystem
    - Assert pyproject.toml exists at path
```

### tests/integration/test_doctor_integration.py

Run `doctor_check()` against the real project.

```
test_doctor_on_real_project_no_errors
    - Run doctor_check()
    - Assert: is_healthy == True (no errors)
    - May have warnings (acceptable)

test_doctor_detects_injected_broken_module
    - Create a fake broken module in tmp_path
    - Monkeypatch MODULES_DIR
    - Assert: doctor detects MISSING_PYPROJECT or INVALID_LAYER
```

### tests/integration/test_deps_integration.py

Run dependency walker against real modules.

```
test_deps_closure_exceptions_core
    - Walk exceptions_core dependencies
    - Assert: zero ADHD deps (it's a leaf)
    - Assert: no violations

test_deps_closure_logger_util
    - Walk logger_util dependencies
    - Should depend on exceptions_core only
    - Assert: no violations

test_deps_closure_adhd_mcp
    - Walk adhd_mcp dependencies
    - Should include modules_controller_core, logger_util, etc.
    - Assert: no cross-layer violations (dev depending on foundation is valid)

test_deps_closure_all_no_violations
    - Walk ALL modules (same as `adhd deps --closure-all`)
    - Assert: zero violations across entire project
```

### tests/integration/test_workspace_integration.py

Generate workspace file from real modules.

```
test_generate_workspace_default
    - Generate workspace file
    - Assert: valid JSON
    - Assert: root folder present
    - Assert: foundation modules present per defaults

test_generate_workspace_include_all
    - Generate with INCLUDE_ALL mode
    - Assert: every module is in the workspace

test_generate_workspace_with_layer_filter
    - Filter to foundation only
    - Assert: only foundation modules in result
    - Assert: no dev modules present
```

### tests/integration/test_filter_integration.py

Test ModuleFilter against real module list.

```
test_filter_include_foundation
    - Filter real modules by layer=foundation
    - Assert: only foundation modules returned

test_filter_exclude_dev
    - Exclude dev layer
    - Assert: no dev modules in result, foundation modules present

test_filter_mcp_only
    - Filter mcp=true
    - Assert: only adhd_mcp returned (it's the only MCP module)

test_filter_require_foundation_and_mcp
    - Require both foundation AND mcp
    - Assert: empty result (no module is both foundation and MCP)
```

### tests/integration/test_migrate_integration.py

Test migration on a synthetic module (not real modules — they're already migrated).

```
test_migrate_synthetic_module_with_init_yaml
    - Create fake module with init.yaml in tmp_path
    - Run migrate
    - Assert: pyproject.toml created, init.yaml removed

test_migrate_dry_run_no_changes
    - Create fake module with init.yaml
    - Run migrate with dry_run=True
    - Assert: init.yaml still exists, no pyproject.toml created

test_migrate_keep_flag_preserves_init_yaml
    - Run migrate with keep=True
    - Assert: both init.yaml and pyproject.toml exist
```

### tests/integration/test_sync_integration.py

Test uv sync wrapper (requires uv on PATH).

```
test_sync_project_succeeds
    - Run ModulesController().sync()
    - Assert: no exception raised
    - Assert: uv.lock exists / was updated

test_sync_frozen_flag_passed
    - Mock subprocess.run
    - Call sync(frozen=True)
    - Assert: --frozen flag in command args
```

---

## Running Integration Tests

```bash
# All integration tests
uv run pytest tests/integration/ -v --tb=short

# Specific test file
uv run pytest tests/integration/test_deps_integration.py -v
```

---

## Fixtures for Integration Tests

### tests/integration/conftest.py (NEW)

```python
import pytest
from pathlib import Path

@pytest.fixture
def framework_root():
    """Return the real framework root."""
    return Path(__file__).parent.parent.parent

@pytest.fixture
def modules_controller(framework_root):
    """Create a ModulesController pointed at the real project."""
    from modules_controller_core import ModulesController
    return ModulesController(root_path=framework_root)
```
