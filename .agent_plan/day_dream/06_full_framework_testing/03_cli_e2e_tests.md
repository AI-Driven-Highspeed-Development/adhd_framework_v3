# CLI End-to-End Test Plan

> Real `adhd` CLI invocations against a real or prepared project. These tests validate the full command lifecycle from argparse through to output.

---

## Test Location

`/home/stellar/PublicRepo/ADHD-Framework/testing_site/cli_e2e/`

These are pytest tests that invoke `adhd` via `subprocess.run` from within the framework directory.

---

## Helper: CLI Runner

```python
import subprocess
from pathlib import Path

FRAMEWORK_ROOT = Path("/home/stellar/PublicRepo/ADHD-Framework/adhd_framework_v3")
ADHD_BIN = FRAMEWORK_ROOT / ".venv" / "bin" / "adhd"

def run_adhd(*args, cwd=None, expect_fail=False):
    """Run an adhd CLI command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [str(ADHD_BIN)] + list(args),
        capture_output=True,
        text=True,
        cwd=cwd or str(FRAMEWORK_ROOT),
        timeout=60,
    )
    if not expect_fail:
        assert result.returncode == 0, f"adhd {' '.join(args)} failed:\n{result.stderr}"
    return result.returncode, result.stdout, result.stderr
```

---

## Test Matrix

### 1. `adhd` (no args)

```
test_no_args_shows_help
    - Run: adhd
    - Assert: exit code 0
    - Assert: stdout contains "ADHD Framework CLI"
    - Assert: stdout contains available commands list
```

### 2. `adhd list` / `adhd ls`

```
test_list_shows_all_modules
    - Run: adhd list
    - Assert: exit code 0
    - Assert: output contains "Found N modules"
    - Assert: output contains "logger_util"
    - Assert: output contains "adhd_mcp"

test_list_alias_ls
    - Run: adhd ls
    - Assert: same output as `adhd list`

test_list_show_filters
    - Run: adhd list --show-filters
    - Assert: output lists available filter dimensions (layer, state, mcp)

test_list_filter_include_foundation
    - Run: adhd list -i foundation
    - Assert: output contains foundation modules
    - Assert: output does NOT contain dev-layer modules (adhd_mcp, etc.)

test_list_filter_exclude_dev
    - Run: adhd list -x dev
    - Assert: output does NOT contain dev modules

test_list_filter_include_mcp
    - Run: adhd list -i mcp
    - Assert: output contains adhd_mcp
    - Assert: output contains "[MCP]" tag
```

### 3. `adhd info` / `adhd in`

```
test_info_known_module
    - Run: adhd info -m logger_util
    - Assert: output contains "MODULE INFORMATION: logger_util"
    - Assert: output contains "Layer: foundation"
    - Assert: output contains "Version:"

test_info_unknown_module_suggests
    - Run: adhd info -m logge_util (typo)
    - Assert: exit code 1
    - Assert: stderr contains "Did you mean: logger_util?"

test_info_with_layer_prefix
    - Run: adhd info -m foundation/logger_util
    - Assert: exit code 0 (layer/name format supported)
```

### 4. `adhd sync` / `adhd s`

```
test_sync_succeeds
    - Run: adhd sync
    - Assert: exit code 0
    - Assert: output contains "sync completed"

test_sync_frozen
    - Run: adhd sync --frozen
    - Assert: exit code 0

test_init_alias
    - Run: adhd init
    - Assert: exit code 0
    - Assert: output contains "sync" (it's an alias)
```

### 5. `adhd refresh` / `adhd r`

```
test_refresh_all
    - Run: adhd refresh
    - Assert: exit code 0
    - Assert: output contains "uv sync completed"
    - Assert: output contains "refresh completed"

test_refresh_specific_module
    - Run: adhd refresh -m config_manager
    - Assert: exit code 0

test_refresh_no_sync
    - Run: adhd refresh --no-sync
    - Assert: exit code 0
    - Assert: output does NOT contain "uv sync"

test_refresh_unknown_module
    - Run: adhd refresh -m nonexistent_mod
    - Assert: exit code 1
    - Assert: output contains "not found"
```

### 6. `adhd doctor` / `adhd doc`

```
test_doctor_healthy
    - Run: adhd doctor
    - Assert: exit code 0
    - Assert: output contains "Doctor Report"
    - Assert: output contains "modules checked"

test_doctor_alias_doc
    - Run: adhd doc
    - Assert: same behavior as `adhd doctor`
```

### 7. `adhd deps` / `adhd dp`

```
test_deps_closure_single
    - Run: adhd deps --closure logger_util
    - Assert: exit code 0
    - Assert: output contains "Dependency Tree"
    - Assert: output contains "exceptions_core" or "No layer violations"

test_deps_closure_all
    - Run: adhd deps --closure-all
    - Assert: exit code 0
    - Assert: output contains "Modules checked"
    - Assert: output contains "No layer violations" (assuming healthy project)

test_deps_unknown_module
    - Run: adhd deps --closure nonexistent
    - Assert: exit code 1
    - Assert: output contains "not found"
```

### 8. `adhd workspace` / `adhd ws`

```
test_workspace_generates_file
    - Run: adhd workspace
    - Assert: exit code 0
    - Assert: output contains "Workspace file updated"
    - Assert: .code-workspace file exists

test_workspace_all_flag
    - Run: adhd workspace --all
    - Assert: exit code 0

test_workspace_toggle_module
    - Run: adhd workspace -m logger_util
    - Assert: exit code 0
    - Assert: output contains "toggling" or "visibility"
```

### 9. `adhd migrate` / `adhd mg`

```
test_migrate_dry_run
    - Run: adhd migrate --dry-run
    - Assert: exit code 0
    - Assert: output contains "preview" or "No modules need migration"

test_migrate_no_modules_needing_migration
    - Run: adhd migrate
    - Assert: exit code 0 (all modules already migrated)
```

### 10. `adhd add` / `adhd a`

> See `04_module_adder_tests.md` for comprehensive add tests.
> Basic smoke test here:

```
test_add_invalid_url
    - Run: adhd add "not-a-url"
    - Assert: exit code 1
    - Assert: output contains "Invalid URL"

test_add_pypi_not_available
    - Run: adhd add --pypi some_package
    - Assert: exit code 1 (or informational exit)
    - Assert: output contains "not yet available"
```

---

## Running E2E Tests

```bash
# All E2E tests
cd /home/stellar/PublicRepo/ADHD-Framework/adhd_framework_v3
uv run pytest testing_site/cli_e2e/ -v --tb=short -m "e2e"

# Skip network tests
uv run pytest testing_site/cli_e2e/ -v -m "e2e and not network"
```

---

## Notes

- E2E tests are inherently slower (subprocess spawning, uv sync, git operations)
- Mark all with `@pytest.mark.e2e`
- Mark network-dependent ones additionally with `@pytest.mark.network`
- Consider running with `--timeout=120` to catch hangs
- `adhd create-project` and `adhd create-module` are NOT tested here — they require interactive TTY input (questionary prompts). They would need a dedicated integration harness with pexpect or similar.
