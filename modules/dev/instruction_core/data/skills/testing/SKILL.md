---
name: testing
description: "Testing and validation workflows — test folder conventions, Python terminal execution rules, and validation patterns for the ADHD Framework. Covers where to put tests vs playground files, pytest conventions, venv activation requirements, HyperRed artifact conventions, and CI integration patterns. Use this skill when creating tests, running validation, deciding between tests/ and playground/, or executing Python commands in terminals."
---

# Testing

Testing conventions, folder guidelines, and Python execution rules.

## When to Use
- Creating or running unit tests
- Setting up test infrastructure for a module
- Running Python commands in terminals
- Deciding between `tests/` and `playground/` folders
- Managing HyperRed adversarial testing artifacts

---

## Testing Folder Decision Tree

### Step 1: Is this a one-off scratch file?
- **YES** → Use `.temp_agent_work/` (MUST clean up after session)
- **NO** → Continue

### Step 2: Am I HyperRed running adversarial attacks?
- **YES** → Use `.agent_plan/red_team/<module>/`
- **NO** → Continue

### Step 3: Is this a FORMAL test case for pytest/CI?
- **YES** → Step 3a: Does it test ONE module in isolation?
  - **YES** → Use `<module>/tests/`
  - **NO** → Use `tests/integration/`
- **NO** → Continue

### Step 4: Is this exploratory code (demos, experiments)?
- **YES** → Step 4a: Does it explore ONE module's API?
  - **YES** → Use `<module>/playground/`
  - **NO** → Use `playground/` (project-level)
- **NO** → Reconsider: What is this file for?

---

## Folder Responsibility Matrix

| Folder | Scope | Purpose | Persistence | Owner |
|--------|-------|---------|-------------|-------|
| `tests/` (project) | Cross-module | Integration tests, E2E workflows | **Permanent** (git-tracked) | HyperArch |
| `<module>/tests/` | Single module | Unit tests, module-isolated tests | **Permanent** (git-tracked) | HyperArch |
| `playground/` (project) | Cross-module | Interactive exploration, demos | **Semi-permanent** (git-tracked) | HyperArch/Human |
| `<module>/playground/` | Single module | API exploration, usage demos | **Semi-permanent** (git-tracked) | HyperArch/Human |
| `.temp_agent_work/` | Session | Scratch files, one-off scripts | **Transient** | Any Agent |
| `.agent_plan/red_team/` | Per-module | HyperRed attack scripts, findings | **Session-to-Session** | HyperRed |

---

## Quick Reference

| Scenario | Folder |
|----------|--------|
| Quick debug script | `.temp_agent_work/` |
| HyperRed edge case attacks | `.agent_plan/red_team/<module>/` |
| Unit tests for a module | `<module>/tests/` |
| Cross-module integration tests | `tests/integration/` |
| API exploration | `<module>/playground/` or `playground/` |
| Demo for users | `<module>/playground/` or `playground/` |
| Prototype before formalizing | `playground/` |

---

## tests/ vs playground/

| I want to... | Use |
|--------------|-----|
| Validate code works correctly | `tests/` |
| Explore how an API works | `playground/` |
| Create a demo for users | `playground/` |
| Regression protection | `tests/` |
| Quick prototype | `playground/` |
| CI/CD integration | `tests/` |

**Rule**: If it should run in CI → `tests/`. If it's for humans to explore → `playground/`.

---

## HyperRed Artifact Conventions

```
.agent_plan/red_team/<module_name>/
├── attacks/     # Generated attack scripts (persist for re-runs)
├── findings/    # Structured JSON per session (YYYY-MM-DD_findings.json)
└── evidence/    # Crash logs, stderr captures (gitignored)
```

**Git Tracking**: Track `attacks/` and `findings/`. Ignore `evidence/`.

---

## Cleanup Responsibilities

| Folder | Cleanup Rule |
|--------|--------------|
| `.temp_agent_work/` | **MUST** clean up after every session. Never commit. |
| `.agent_plan/red_team/evidence/` | Prune after fixes verified |
| `playground/` | No mandatory cleanup (human-managed) |
| `tests/` | No cleanup (permanent) |

---

## Before Creating Test Files

1. **Check existing tests**: Search `<module>/tests/` and `tests/integration/` first
2. **Check HyperRed findings**: Look at `.agent_plan/red_team/<module>/findings/`
3. **Reuse before creating**: Don't duplicate existing test coverage

---

## Python Terminal Commands

### Rule 1: ALWAYS Activate Virtual Environment

When using `run_in_terminal` to execute Python commands, ALWAYS activate `.venv` first.

**Pattern 1 (Recommended)**: Chain activation with command
```bash
source .venv/bin/activate && python <command>
```

**Pattern 2 (Alternative)**: Use venv Python directly
```bash
.venv/bin/python <command>
```

### Rule 2: Apply to ALL Python Executables

This rule applies to:
- `python` or `python3` script execution
- `pip install` package installation
- `pytest` test execution
- `python -m <module>` module execution
- Any Python-based CLI tools

### Examples

**CORRECT:**
```bash
# Running a script
source .venv/bin/activate && python adhd_framework.py refresh

# Installing packages
source .venv/bin/activate && pip install requests

# Running pytest
source .venv/bin/activate && pytest tests/

# Running module
source .venv/bin/activate && python -m stocks_data_manager
```

**INCORRECT:**
```bash
# Missing venv activation
python adhd_framework.py refresh
pip install requests
pytest tests/
```

### Why This Matters
- Prevents "module not found" errors
- Ensures consistent dependency resolution
- All Python commands execute within the project's virtual environment
