# Full Framework Testing Blueprint — Overview

> **Goal:** End-to-end validation of the entire ADHD Framework v3: every CLI command, every module API, every cross-module interaction.

---

## Scope

This testing effort covers:

1. **Unit tests** — Per-module isolated tests (mocked dependencies)
2. **Integration tests** — Cross-module interactions within the framework workspace
3. **CLI end-to-end tests** — Real `adhd` commands against a real project
4. **module_adder_core tests** — Mode 1 (standalone repo) and Mode 2 (monorepo subfolder); Mode 3 (PyPI) explicitly excluded for now

### Out of Scope

- PyPI acquisition mode (no ADHD-compatible packages exist)
- `create-project` / `create-module` interactive wizards (require TTY + questionary; tested manually)
- Performance/load testing
- Multi-platform testing (Linux only)

---

## Infrastructure

| Resource | Path / URL | Purpose |
|---|---|---|
| Testing workspace | `/home/stellar/PublicRepo/ADHD-Framework/testing_site/` | Isolated scratch area for E2E tests |
| Test repos | `https://github.com/AI-Driven-Highspeed-Development/testing_*` | Remote repos for `adhd add` testing |
| Agent scratch notes | `/home/stellar/PublicRepo/ADHD-Framework/adhd_framework_v3/.temp_agent_work/` | Working notes and intermediate artifacts |
| Framework source | `/home/stellar/PublicRepo/ADHD-Framework/adhd_framework_v3/` | The codebase under test |

### GitHub Test Repos (to be created)

| Repo Name | Purpose | Contents |
|---|---|---|
| `testing_standalone_module` | Mode 1: standalone repo with valid pyproject.toml | Minimal Python module with `[tool.adhd]` layer=runtime |
| `testing_standalone_no_pyproject` | Mode 1: standalone repo WITHOUT pyproject.toml | Plain Python files, no pyproject.toml (triggers scaffolding) |
| `testing_monorepo` | Mode 2: monorepo with multiple subfolders | `packages/alpha/` and `packages/beta/` — alpha has pyproject.toml, beta does not |

**Total: 3 repos** — minimal, reasonable, sufficient to cover all git-based add modes.

---

## Blueprint Files

| File | Contents |
|---|---|
| `00_overview.md` | This file |
| `01_unit_tests.md` | Module-by-module unit test plan |
| `02_integration_tests.md` | Cross-module integration test plan |
| `03_cli_e2e_tests.md` | CLI end-to-end test plan |
| `04_module_adder_tests.md` | module_adder_core-specific test plan (Modes 1 & 2) |
| `05_test_repo_setup.md` | Exact steps to create the 3 GitHub test repos |
| `06_execution_checklist.md` | Run-order, pass/fail tracking sheet |

---

## Test Runner Configuration

All tests run via `pytest` from the framework venv:

```bash
cd /home/stellar/PublicRepo/ADHD-Framework/adhd_framework_v3
uv run pytest                              # existing unit tests
uv run pytest tests/                       # root integration tests
uv run pytest modules/                     # per-module tests
uv run pytest --tb=short -q               # CI-style compact output
```

E2E tests that operate on `testing_site/` are shell scripts or pytest fixtures that invoke the real `adhd` CLI binary.

---

## Test Categories & Tags

| Tag | Meaning | Requires |
|---|---|---|
| `unit` | Isolated, mocked, fast | Nothing external |
| `integration` | Multiple modules, real filesystem | `uv sync` in framework |
| `e2e` | Real CLI, real git operations | GitHub access, `testing_site/`, test repos |
| `network` | Requires internet (git clone, gh API) | Network connectivity |
| `slow` | >10 seconds | Patience |

---

## Pre-Conditions

Before running any tests:

1. `cd /home/stellar/PublicRepo/ADHD-Framework/adhd_framework_v3 && uv sync` — Ensure all deps installed
2. `gh auth status` — Ensure GitHub CLI authenticated
3. Test repos created per `05_test_repo_setup.md`
4. `testing_site/` directory created
