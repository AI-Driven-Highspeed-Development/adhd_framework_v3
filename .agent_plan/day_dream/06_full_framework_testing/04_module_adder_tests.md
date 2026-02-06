# module_adder_core Test Plan

> Comprehensive testing for the new `module_adder_core` module covering Mode 1 (standalone repo) and Mode 2 (monorepo subfolder). Mode 3 (PyPI) is deferred.

---

## Test Layers

1. **Unit tests** (mocked git, mocked filesystem) — fast, no network
2. **Integration tests** (real git clone against test repos) — requires network + test repos

---

## Unit Tests

Location: `modules/dev/module_adder_core/tests/`

### test_module_adder.py

#### Mode 1: Standalone Repo (Mocked)

```
test_add_from_repo_success
    - Mock git clone to populate tmp_path with valid module
    - Assert: AddModuleResult.success == True
    - Assert: module moved to modules/<layer>/<name>/
    - Assert: .git/ directory removed
    - Assert: .gitignore preserved

test_add_from_repo_no_pyproject_skip_prompt
    - Mock git clone to populate tmp_path WITHOUT pyproject.toml
    - skip_prompt=True
    - Assert: pyproject.toml created with defaults (layer=runtime, inferred name)

test_add_from_repo_no_pyproject_interactive
    - Mock git clone without pyproject.toml
    - Mock QuestionaryCore responses (name, layer, etc.)
    - Assert: pyproject.toml created with user-provided values

test_add_from_repo_invalid_layer
    - Mock git clone with pyproject.toml containing layer="invalid"
    - Assert: AddModuleResult.success == False
    - Assert: error message mentions valid layers

test_add_from_repo_collision_detection
    - Pre-create modules/runtime/test_module/
    - Mock git clone
    - Assert: AddModuleResult.success == False
    - Assert: error mentions "already exists"

test_add_from_repo_clone_failure
    - Mock git clone returning non-zero exit code
    - Assert: AddModuleResult.success == False
    - Assert: error message sanitized (URL redacted)

test_add_from_repo_clone_timeout
    - Mock subprocess.run raising TimeoutExpired
    - Assert: AddModuleResult.success == False

test_add_from_repo_keep_git_flag
    - Mock git clone
    - Call with keep_git=True
    - Assert: .git/ directory NOT removed
    - Assert: .github/ directory NOT removed

test_add_from_repo_strips_github_dir
    - Mock git clone with .github/ directory present
    - Call with keep_git=False (default)
    - Assert: .github/ removed
    - Assert: .gitignore preserved
    - Assert: .gitattributes preserved

test_add_from_repo_no_adhd_section_prompts_layer
    - Mock git clone with pyproject.toml that has [project] but no [tool.adhd]
    - Mock QuestionaryCore to select "dev"
    - Assert: [tool.adhd] section injected into pyproject.toml
    - Assert: layer == "dev"

test_add_from_repo_invalid_url_format
    - Call with repo_url="not-a-url"
    - Assert: failure with URL validation error
```

#### Mode 2: Monorepo Subfolder (Mocked)

```
test_add_from_monorepo_success
    - Mock git clone to populate tmp_path with repo containing packages/alpha/
    - Call with subfolder="packages/alpha"
    - Assert: only packages/alpha/ content moved to target
    - Assert: rest of repo discarded

test_add_from_monorepo_subfolder_not_found
    - Mock git clone
    - Call with subfolder="packages/nonexistent"
    - Assert: failure with "subfolder not found" error

test_add_from_monorepo_no_pyproject_in_subfolder
    - Mock git clone with subfolder that has no pyproject.toml
    - skip_prompt=True
    - Assert: pyproject.toml scaffolded in subfolder

test_add_from_monorepo_preserves_subfolder_gitignore
    - Mock git clone with .gitignore inside the subfolder
    - Assert: subfolder's .gitignore preserved in final location
    - Assert: repo-root .git/ NOT copied into subfolder
```

#### Mode 3: PyPI (Stub)

```
test_add_from_pypi_raises_not_implemented
    - Call add_from_pypi("some-package")
    - Assert: raises NotImplementedError
    - Assert: message contains "not yet available"
```

### test_pyproject_patcher.py

Tests for the root `pyproject.toml` patching logic.

```
test_add_to_root_pyproject_new_dep
    - Create a minimal root pyproject.toml with existing deps
    - Call patcher with new package name
    - Assert: package added to dependencies list
    - Assert: package added to [tool.uv.sources] with workspace=true
    - Assert: existing content unchanged

test_add_to_root_pyproject_duplicate_dep
    - Pre-populate root pyproject.toml with the package already in deps
    - Call patcher
    - Assert: no duplicate added
    - Assert: warning logged

test_add_to_root_pyproject_duplicate_source
    - Pre-populate [tool.uv.sources] with the package
    - Assert: no duplicate added

test_add_to_root_pyproject_preserves_formatting
    - Create pyproject.toml with specific indentation and comments
    - Call patcher
    - Assert: only the new dep/source lines differ
    - Assert: comments and indentation preserved

test_add_to_root_pyproject_missing_deps_section
    - Create pyproject.toml without dependencies = [...]
    - Assert: error raised (not silently creating section)

test_add_to_root_pyproject_missing_sources_section
    - Create pyproject.toml without [tool.uv.sources]
    - Assert: error raised
```

### test_pyproject_scaffolder.py

Tests for the interactive pyproject.toml generator.

```
test_scaffold_with_all_defaults
    - Call scaffolder with skip_prompt=True
    - Assert: generated TOML is valid
    - Assert: name inferred from folder
    - Assert: version == "0.0.1"
    - Assert: layer == "runtime"
    - Assert: no mcp flag

test_scaffold_with_mcp_flag
    - Mock user selecting mcp=True
    - Assert: [tool.adhd] contains mcp = true

test_scaffold_with_custom_values
    - Mock user providing name, version, layer, description
    - Assert: all values reflected in output

test_scaffold_output_is_valid_toml
    - Generate pyproject.toml
    - Parse it back with tomllib
    - Assert: no parse errors
    - Assert: [project], [tool.adhd], [build-system] sections present

test_scaffold_name_inference_from_folder
    - folder name "my-cool-module" -> package name "my_cool_module"
    - folder name "MyModule" -> "my_module"
```

---

## Integration Tests (Real Git, Real Network)

Location: `/home/stellar/PublicRepo/ADHD-Framework/testing_site/module_adder_integration/`

These use the real GitHub test repos created per `05_test_repo_setup.md`.

### Prerequisites

- Test repos exist on GitHub
- Network connectivity available
- `testing_site/` directory exists

### Test Cases

```
test_add_standalone_with_valid_pyproject [network]
    - Run: adhd add https://github.com/AI-Driven-Highspeed-Development/testing_standalone_module -y
    - Assert: exit code 0
    - Assert: module appears in modules/runtime/ (test repo has layer=runtime)
    - Assert: .git/ directory absent
    - Assert: .gitignore present (if repo had one)
    - Assert: adhd list includes the new module
    - Cleanup: remove the added module from modules/

test_add_standalone_no_pyproject [network]
    - Run: adhd add https://github.com/AI-Driven-Highspeed-Development/testing_standalone_no_pyproject -y
    - Assert: exit code 0
    - Assert: pyproject.toml auto-generated with defaults
    - Assert: module appears in modules/runtime/ (default layer)
    - Cleanup: remove

test_add_monorepo_subfolder [network]
    - Run: adhd add https://github.com/AI-Driven-Highspeed-Development/testing_monorepo --path packages/alpha -y
    - Assert: exit code 0
    - Assert: only alpha/ content in target directory
    - Assert: module name matches alpha's pyproject.toml name
    - Cleanup: remove

test_add_monorepo_subfolder_no_pyproject [network]
    - Run: adhd add https://github.com/AI-Driven-Highspeed-Development/testing_monorepo --path packages/beta -y
    - Assert: exit code 0
    - Assert: pyproject.toml scaffolded
    - Cleanup: remove

test_add_monorepo_invalid_subfolder [network]
    - Run: adhd add https://github.com/AI-Driven-Highspeed-Development/testing_monorepo --path packages/nonexistent -y
    - Assert: exit code 1
    - Assert: error mentions "subfolder not found"

test_add_duplicate_module [network]
    - Run: adhd add testing_standalone_module twice
    - First: succeeds
    - Second: exit code 1, error mentions "already exists"
    - Cleanup: remove

test_add_with_keep_git [network]
    - Run: adhd add https://github.com/AI-Driven-Highspeed-Development/testing_standalone_module --keep-git -y
    - Assert: .git/ directory present
    - Cleanup: remove
```

---

## Cleanup Strategy

Integration tests that add real modules to the workspace MUST clean up after themselves:

```python
@pytest.fixture
def clean_added_module():
    """Remove any module added during the test."""
    added_paths = []
    yield added_paths  # test appends to this list
    for path in added_paths:
        if path.exists():
            shutil.rmtree(path)
    # Re-run uv sync to clean lockfile
    subprocess.run(["uv", "sync"], cwd=str(FRAMEWORK_ROOT), check=False)
```

Alternatively, operate entirely within `testing_site/` by copying the framework there first. This is safer but more expensive.

---

## Test Repo Specifications

See `05_test_repo_setup.md` for exact contents of each test repo.
