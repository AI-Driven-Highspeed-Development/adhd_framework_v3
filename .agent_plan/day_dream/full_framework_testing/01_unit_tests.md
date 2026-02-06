# Unit Test Plan — Per-Module

> Each module gets isolated unit tests. Dependencies are mocked. No network, no real filesystem (use `tmp_path`).

---

## Coverage Status (Current vs Target)

| Module | Layer | Has Tests? | Target Coverage |
|---|---|---|---|
| exceptions_core | foundation | No (trivial) | Skip — single class, no logic |
| logger_util | foundation | No | New: test Logger init, style switching, level filtering |
| config_manager | foundation | No | New: test ConfigManager singleton, template merging, key generation |
| cli_manager | foundation | **Yes** (396 LOC) | Expand: test dispatch, type mapping edge cases |
| modules_controller_core | foundation | **Yes** (442 LOC, filter only) | Expand: test scan, require_module, doctor_check, workspace generation |
| temp_files_manager | foundation | No | New: test create/cleanup lifecycle |
| workspace_core | foundation | No | New: test WorkspaceBuilder step pipeline, file output |
| creator_common_core | dev | No | New: test to_snake_case, list_templates, QuestionaryCore (mocked questionary) |
| github_api_core | dev | No | New: test GithubApi.require_gh, URL utils |
| instruction_core | dev | No | Skip — refresh-only, tested via integration |
| module_creator_core | dev | No | New: test validate_module_name, template loading |
| project_creator_core | dev | No | New: test preload set parsing, template info |
| uv_migrator_core | dev | No (empty dir) | New: test TOML generation, requirement parsing, layer inference |
| adhd_mcp | dev | **Yes** (391 LOC) | Expand: test MCP tool registration, git controller |
| module_adder_core | dev | **N/A (new)** | New: full test suite (see 04_module_adder_tests.md) |

---

## New Test Files to Create

### foundation/logger_util/tests/test_logger.py

```
test_logger_creates_with_name
test_logger_respects_log_level
test_compact_style_format
test_normal_style_format
test_get_central_logger_returns_same_instance
test_set_logger_style_switches_format
```

### foundation/config_manager/tests/test_config_manager.py

```
test_config_manager_is_singleton
test_config_manager_loads_toml_file
test_config_manager_returns_defaults_when_no_file
test_config_template_merges_correctly
test_config_keys_generator_produces_expected_keys
```

### foundation/modules_controller_core/tests/test_modules_controller.py

(Supplements existing test_module_filter.py)

```
test_scan_all_modules_discovers_layers
test_scan_all_modules_skips_non_module_dirs
test_get_module_by_name_case_insensitive
test_get_module_by_name_with_layer_prefix
test_get_module_by_name_returns_none_for_unknown
test_require_module_returns_module           # NEW API
test_require_module_raises_with_suggestions  # NEW API
test_doctor_check_reports_missing_pyproject
test_doctor_check_reports_invalid_layer
test_doctor_check_healthy_project
test_generate_workspace_file_default_mode
test_generate_workspace_file_include_all_mode
test_generate_workspace_file_with_filter
```

### foundation/modules_controller_core/tests/test_dependency_walker.py

```
test_walk_simple_chain
test_walk_detects_cross_layer_violation
test_walk_handles_circular_dependency
test_walk_max_depth_enforced
test_format_dependency_tree_output
test_format_all_violations_output           # NEW API
```

### foundation/temp_files_manager/tests/test_temp_files.py

```
test_create_temp_dir
test_cleanup_removes_dir
test_context_manager_auto_cleans
```

### foundation/workspace_core/tests/test_workspace_builder.py

```
test_generate_workspace_file_creates_valid_json
test_workspace_includes_root_folder
test_workspace_deduplicates_entries
test_workspace_handles_relative_paths
```

### dev/creator_common_core/tests/test_creator_common.py

```
test_to_snake_case_basic
test_to_snake_case_with_hyphens
test_to_snake_case_with_mixed_case
test_list_templates_extracts_all
test_list_templates_empty_dict
test_questionary_core_multiple_choice (mocked questionary.select)
test_questionary_core_confirm (mocked questionary.confirm)
```

### dev/github_api_core/tests/test_github_api.py

```
test_require_gh_found (mock shutil.which returning path)
test_require_gh_not_found (mock shutil.which returning None)
test_github_repo_dataclass
```

### dev/module_creator_core/tests/test_module_creator.py

```
test_validate_module_name_valid
test_validate_module_name_invalid_chars
test_validate_module_name_reserved_words
test_module_creation_params_defaults
```

### dev/project_creator_core/tests/test_project_creator.py

```
test_parse_preload_sets_from_yaml
test_preload_set_dataclass
test_module_source_dataclass
test_list_project_templates
```

### dev/uv_migrator_core/tests/test_uv_migrator.py

```
test_parse_init_yaml_basic
test_parse_init_yaml_with_requirements
test_parse_requirements_txt
test_github_url_to_package_name
test_convert_requirements_simple
test_infer_layer_from_metadata
test_generate_pyproject_toml_content
test_module_name_to_package_name
```

---

## Test Fixture Strategy

### Shared fixtures (add to module's conftest.py where needed)

```python
@pytest.fixture
def mock_modules_dir(tmp_path):
    """Create a fake modules/ directory with foundation/runtime/dev layers."""
    for layer in ("foundation", "runtime", "dev"):
        (tmp_path / "modules" / layer).mkdir(parents=True)
    return tmp_path

@pytest.fixture
def fake_module(tmp_path):
    """Create a minimal valid module directory."""
    mod = tmp_path / "modules" / "runtime" / "test_module"
    mod.mkdir(parents=True)
    (mod / "__init__.py").touch()
    (mod / "pyproject.toml").write_text(...)
    return mod
```

### Mocking guidelines

- Always mock `subprocess.run` for git/uv commands
- Always mock `shutil.which` for tool detection
- Use `tmp_path` for all filesystem operations (never write to real project)
- Mock `ConfigManager` in any module that imports it
- Mock `questionary` calls in QuestionaryCore tests

---

## Running Unit Tests

```bash
# All unit tests
uv run pytest modules/ tests/ -m "not e2e and not network" --tb=short

# Single module
uv run pytest modules/foundation/modules_controller_core/tests/ -v

# With coverage (if pytest-cov is added)
uv run pytest modules/ --cov=modules --cov-report=term-missing
```
