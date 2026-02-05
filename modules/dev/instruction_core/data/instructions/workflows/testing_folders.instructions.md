---
applyTo: "tests/**,**/tests/**,playground/**,**/playground/**,.temp_agent_work/**,.agent_plan/red_team/**"
---

# Testing Folders Guidelines

## Purpose
Define where AI agents should place testing artifacts, exploratory scripts, and attack findings.

**Core Principle**: *"Every folder has one job. When in doubt, use this decision tree."*

## Folder Responsibility Matrix

| Folder | Scope | Purpose | Persistence | Owner |
|--------|-------|---------|-------------|-------|
| `tests/` (project) | Cross-module | Integration tests, E2E workflows | **Permanent** (git-tracked) | HyperArch |
| `<module>/tests/` | Single module | Unit tests, module-isolated tests | **Permanent** (git-tracked) | HyperArch |
| `playground/` (project) | Cross-module | Interactive exploration, demos, prototyping | **Semi-permanent** (git-tracked) | HyperArch/Human |
| `<module>/playground/` | Single module | API exploration, usage demos | **Semi-permanent** (git-tracked) | HyperArch/Human |
| `.temp_agent_work/` | Session | Scratch files, one-off scripts | **Transient** | Any Agent |
| `.agent_plan/red_team/` | Per-module | HyperRed attack scripts, findings | **Session-to-Session** | HyperRed |

## Decision Tree

### Step 1: Is this a one-off scratch file?
- **YES** → Use `.temp_agent_work/` (MUST clean up after session)
- **NO** → Continue to Step 2

### Step 2: Am I HyperRed running adversarial attacks?
- **YES** → Use `.agent_plan/red_team/<module>/` (attacks + findings)
- **NO** → Continue to Step 3

### Step 3: Is this a FORMAL test case for pytest/CI?
- **YES** → Continue to Step 3a
- **NO** → Continue to Step 4

### Step 3a: Does it test ONE module in isolation?
- **YES** → Use `<module>/tests/`
- **NO** → Use `tests/integration/`

### Step 4: Is this exploratory code (demos, experiments)?
- **YES** → Continue to Step 4a
- **NO** → Reconsider: What is this file for?

### Step 4a: Does it explore ONE module's API?
- **YES** → Use `<module>/playground/`
- **NO** → Use `playground/` (project-level)

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

## HyperRed Artifact Conventions

Structure:
- `.agent_plan/red_team/<module_name>/attacks/` - Generated attack scripts (persist for re-runs)
- `.agent_plan/red_team/<module_name>/findings/` - Structured JSON per session (YYYY-MM-DD_findings.json)
- `.agent_plan/red_team/<module_name>/evidence/` - Crash logs, stderr captures (gitignored)

**Git Tracking**: Track `attacks/` and `findings/`. Ignore `evidence/`.

## Cleanup Responsibilities

| Folder | Cleanup Rule |
|--------|--------------|
| `.temp_agent_work/` | **MUST** clean up after every session. Never commit. |
| `.agent_plan/red_team/evidence/` | Prune after fixes verified |
| `playground/` | No mandatory cleanup (human-managed) |
| `tests/` | No cleanup (permanent) |

## Before Creating Test Files

1. **Check existing tests**: Search `<module>/tests/` and `tests/integration/` first
2. **Check HyperRed findings**: Look at `.agent_plan/red_team/<module>/findings/`
3. **Reuse before creating**: Don't duplicate existing test coverage

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
