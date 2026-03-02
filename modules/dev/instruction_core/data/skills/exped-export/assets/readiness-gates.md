# Readiness Gate Checks

## Tier 1: Hard Blockers (ALL must pass)

| Code | Check | Description |
|------|-------|-------------|
| `target_exists` | Target accessible | Path exists and readable |
| `not_adhd_to_adhd` | Not ADHD project | Cannot export ADHD→ADHD |
| `scope_bounded` | ≤25 artifacts | Max artifacts per expedition |
| `no_active_lock` | No lock file | Previous expedition complete |
| `not_detached_head` | On branch | Not in detached HEAD state |

## Tier 2: Git State

| Code | Behavior | Description |
|------|----------|-------------|
| `clean_working_directory` | BLOCKER | No uncommitted changes |
| `submodule_clean` | BLOCKER | No dirty submodules |
| `shallow_clone_detected` | WARNING | Incomplete git history |
| `untracked_in_target` | BLOCKER | Untracked files at destinations |
| `on_feature_branch` | WARNING | Not on main/master |
| `ahead_of_remote` | WARNING | Unpushed commits |

## Tier 3: Source Readiness

| Code | Check | Description |
|------|-------|-------------|
| `agents_exist` | Source agents present | `.github/agents/` |
| `instructions_exist` | Source instructions present | instruction_core/data/instructions/ |
