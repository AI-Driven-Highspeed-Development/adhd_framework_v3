# Test Execution Checklist

> Run order, dependencies, and pass/fail tracking.

---

## Phase 0 — Setup

| # | Task | Command | Status |
|---|---|---|---|
| 0.1 | Ensure venv synced | `cd adhd_framework_v3 && uv sync --dev` | [ ] |
| 0.2 | Verify gh auth | `gh auth status` | [ ] |
| 0.3 | Create testing_site/ | `mkdir -p /home/stellar/PublicRepo/ADHD-Framework/testing_site` | [ ] |
| 0.4 | Create test repo 1 | See `05_test_repo_setup.md` Repo 1 | [ ] |
| 0.5 | Create test repo 2 | See `05_test_repo_setup.md` Repo 2 | [ ] |
| 0.6 | Create test repo 3 | See `05_test_repo_setup.md` Repo 3 | [ ] |
| 0.7 | Verify test repos | `gh repo list AI-Driven-Highspeed-Development \| grep testing_` | [ ] |

---

## Phase 1 — Existing Tests (Baseline)

Verify current tests still pass before any changes.

| # | Test Suite | Command | Expected | Status |
|---|---|---|---|---|
| 1.1 | CLI manager unit | `uv run pytest modules/foundation/cli_manager/tests/ -v` | All pass | [ ] |
| 1.2 | Module filter unit | `uv run pytest modules/foundation/modules_controller_core/tests/ -v` | All pass | [ ] |
| 1.3 | MCP tools unit | `uv run pytest modules/dev/adhd_mcp/tests/ -v` | All pass | [ ] |
| 1.4 | Refresh integration | `uv run pytest tests/integration/ -v` | All pass | [ ] |
| 1.5 | Lint check | `uv run ruff check .` | No errors | [ ] |
| 1.6 | Layer validation | `uv run python adhd_framework.py deps --closure-all` | No violations | [ ] |

---

## Phase 2 — New Unit Tests

Write and run per-module unit tests.

| # | Module | Test File | Depends On | Status |
|---|---|---|---|---|
| 2.1 | logger_util | `test_logger.py` | — | [ ] |
| 2.2 | config_manager | `test_config_manager.py` | — | [ ] |
| 2.3 | modules_controller_core | `test_modules_controller.py` | — | [ ] |
| 2.4 | modules_controller_core | `test_dependency_walker.py` | — | [ ] |
| 2.5 | temp_files_manager | `test_temp_files.py` | — | [ ] |
| 2.6 | workspace_core | `test_workspace_builder.py` | — | [ ] |
| 2.7 | creator_common_core | `test_creator_common.py` | — | [ ] |
| 2.8 | github_api_core | `test_github_api.py` | — | [ ] |
| 2.9 | module_creator_core | `test_module_creator.py` | — | [ ] |
| 2.10 | project_creator_core | `test_project_creator.py` | — | [ ] |
| 2.11 | uv_migrator_core | `test_uv_migrator.py` | — | [ ] |

Items 2.1-2.11 are independent and can be written/run in parallel.

---

## Phase 3 — New Integration Tests

| # | Test File | Depends On | Status |
|---|---|---|---|
| 3.1 | `test_module_discovery_integration.py` | Phase 2.3 | [ ] |
| 3.2 | `test_doctor_integration.py` | Phase 2.3 | [ ] |
| 3.3 | `test_deps_integration.py` | Phase 2.4 | [ ] |
| 3.4 | `test_workspace_integration.py` | Phase 2.6 | [ ] |
| 3.5 | `test_filter_integration.py` | Phase 2.3 | [ ] |
| 3.6 | `test_migrate_integration.py` | Phase 2.11 | [ ] |
| 3.7 | `test_sync_integration.py` | Phase 2.3 | [ ] |

---

## Phase 4 — CLI E2E Tests

| # | Command Group | Depends On | Status |
|---|---|---|---|
| 4.1 | `adhd` (no args) | Phase 1 | [ ] |
| 4.2 | `adhd list` + filters | Phase 3.1 | [ ] |
| 4.3 | `adhd info` | Phase 3.1 | [ ] |
| 4.4 | `adhd sync` / `adhd init` | Phase 3.7 | [ ] |
| 4.5 | `adhd refresh` | Phase 3.1 | [ ] |
| 4.6 | `adhd doctor` | Phase 3.2 | [ ] |
| 4.7 | `adhd deps` | Phase 3.3 | [ ] |
| 4.8 | `adhd workspace` | Phase 3.4 | [ ] |
| 4.9 | `adhd migrate` | Phase 3.6 | [ ] |
| 4.10 | `adhd add` (error cases) | Phase 1 | [ ] |

---

## Phase 5 — module_adder_core Tests

### Unit (no network)

| # | Test file | Depends On | Status |
|---|---|---|---|
| 5.1 | `test_module_adder.py` — Mode 1 mocked | Phase 3 (extraction done) | [ ] |
| 5.2 | `test_module_adder.py` — Mode 2 mocked | Phase 3 | [ ] |
| 5.3 | `test_module_adder.py` — Mode 3 stub | Phase 3 | [ ] |
| 5.4 | `test_pyproject_patcher.py` | — | [ ] |
| 5.5 | `test_pyproject_scaffolder.py` | — | [ ] |

### Integration (network required)

| # | Test scenario | Repo Used | Depends On | Status |
|---|---|---|---|---|
| 5.6 | Add standalone (valid pyproject) | testing_standalone_module | Phase 0.4, 5.1 | [ ] |
| 5.7 | Add standalone (no pyproject) | testing_standalone_no_pyproject | Phase 0.5, 5.1 | [ ] |
| 5.8 | Add monorepo subfolder (valid) | testing_monorepo (alpha) | Phase 0.6, 5.2 | [ ] |
| 5.9 | Add monorepo subfolder (no pyproject) | testing_monorepo (beta) | Phase 0.6, 5.2 | [ ] |
| 5.10 | Add monorepo invalid subfolder | testing_monorepo | Phase 0.6, 5.2 | [ ] |
| 5.11 | Add duplicate module | testing_standalone_module | Phase 5.6 | [ ] |
| 5.12 | Add with --keep-git | testing_standalone_module | Phase 5.6 | [ ] |

---

## Phase 6 — Full Regression

| # | Command | Purpose | Status |
|---|---|---|---|
| 6.1 | `uv run pytest modules/ tests/ -v --tb=short` | All unit + integration | [ ] |
| 6.2 | `uv run ruff check .` | Lint | [ ] |
| 6.3 | `uv run ruff format --check .` | Format | [ ] |
| 6.4 | `uv run python adhd_framework.py deps --closure-all` | Layer violations | [ ] |
| 6.5 | Manual: `adhd list`, `adhd doctor`, `adhd info -m logger_util` | Smoke test | [ ] |

---

## Summary Metrics

| Metric | Target |
|---|---|
| Modules with unit tests | 14/15 (skip exceptions_core) |
| Integration test files | 7 new + 1 existing = 8 |
| CLI E2E test groups | 10 command groups |
| module_adder unit tests | ~25 test functions |
| module_adder integration tests | 7 scenarios |
| GitHub test repos | 3 |
| Total new test files | ~20 |
| Estimated new test LOC | ~2500-3500 |
