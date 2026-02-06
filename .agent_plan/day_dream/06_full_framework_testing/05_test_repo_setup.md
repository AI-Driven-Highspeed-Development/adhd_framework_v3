# Test Repository Setup Guide

> Exact steps to create the 3 GitHub test repos needed for module_adder integration tests.

---

## Org: AI-Driven-Highspeed-Development

All repos are **private** (no reason to be public, reduces noise).

---

## Repo 1: `testing_standalone_module`

A minimal ADHD-compatible Python module in its own repo.

### Create

```bash
cd /home/stellar/PublicRepo/ADHD-Framework/testing_site/
mkdir testing_standalone_module && cd testing_standalone_module
git init
```

### Files

**pyproject.toml**
```toml
[project]
name = "testing-standalone-module"
version = "0.0.1"
description = "Test module for ADHD framework integration testing"
requires-python = ">=3.11"
dependencies = []

[tool.adhd]
layer = "runtime"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**__init__.py**
```python
"""Testing standalone module — used by ADHD framework integration tests."""
```

**testing_standalone_module.py**
```python
"""Minimal module implementation for testing."""

def hello():
    return "hello from testing_standalone_module"
```

**.gitignore**
```
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
```

### Push

```bash
git add -A
git commit -m "Initial: minimal ADHD-compatible test module"
gh repo create AI-Driven-Highspeed-Development/testing_standalone_module --private --source=. --push
```

---

## Repo 2: `testing_standalone_no_pyproject`

A plain Python directory with NO pyproject.toml. Used to test interactive scaffolding.

### Create

```bash
cd /home/stellar/PublicRepo/ADHD-Framework/testing_site/
mkdir testing_standalone_no_pyproject && cd testing_standalone_no_pyproject
git init
```

### Files

**__init__.py**
```python
"""A module without pyproject.toml — tests ADHD scaffolding flow."""
```

**some_code.py**
```python
"""Some example code."""

def compute(x, y):
    return x + y
```

**.gitignore**
```
__pycache__/
*.py[cod]
```

**NO pyproject.toml** — this is intentional.

### Push

```bash
git add -A
git commit -m "Initial: test module without pyproject.toml"
gh repo create AI-Driven-Highspeed-Development/testing_standalone_no_pyproject --private --source=. --push
```

---

## Repo 3: `testing_monorepo`

A monorepo with multiple packages in subdirectories. Used for Mode 2 testing.

### Create

```bash
cd /home/stellar/PublicRepo/ADHD-Framework/testing_site/
mkdir testing_monorepo && cd testing_monorepo
git init
```

### Directory Structure

```
testing_monorepo/
  README.md
  packages/
    alpha/
      __init__.py
      alpha_module.py
      pyproject.toml
      .gitignore
    beta/
      __init__.py
      beta_code.py
      (NO pyproject.toml)
```

### Files

**README.md**
```markdown
# Testing Monorepo

This repo contains multiple packages for ADHD framework integration testing.
- `packages/alpha/` — has pyproject.toml
- `packages/beta/` — no pyproject.toml (tests scaffolding)
```

**packages/alpha/pyproject.toml**
```toml
[project]
name = "testing-alpha"
version = "0.1.0"
description = "Alpha package from test monorepo"
requires-python = ">=3.11"
dependencies = []

[tool.adhd]
layer = "foundation"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**packages/alpha/__init__.py**
```python
"""Alpha package — has valid pyproject.toml."""
```

**packages/alpha/alpha_module.py**
```python
"""Alpha module implementation."""

def alpha_func():
    return "alpha"
```

**packages/alpha/.gitignore**
```
__pycache__/
*.egg-info/
```

**packages/beta/__init__.py**
```python
"""Beta package — no pyproject.toml, tests scaffolding."""
```

**packages/beta/beta_code.py**
```python
"""Beta module implementation."""

def beta_func():
    return "beta"
```

### Push

```bash
git add -A
git commit -m "Initial: test monorepo with alpha (has pyproject) and beta (no pyproject)"
gh repo create AI-Driven-Highspeed-Development/testing_monorepo --private --source=. --push
```

---

## Verification

After creating all repos, verify they're accessible:

```bash
gh repo list AI-Driven-Highspeed-Development --limit 30 | grep testing_
```

Expected output:
```
AI-Driven-Highspeed-Development/testing_standalone_module     ...
AI-Driven-Highspeed-Development/testing_standalone_no_pyproject  ...
AI-Driven-Highspeed-Development/testing_monorepo              ...
```

---

## Cleanup (Manual, Owner Responsibility)

These repos are test artifacts. The owner will remove them manually after testing.

```bash
# DO NOT run these automatically — manual cleanup only
gh repo delete AI-Driven-Highspeed-Development/testing_standalone_module --yes
gh repo delete AI-Driven-Highspeed-Development/testing_standalone_no_pyproject --yes
gh repo delete AI-Driven-Highspeed-Development/testing_monorepo --yes
```

Also clean up `testing_site/`:
```bash
rm -rf /home/stellar/PublicRepo/ADHD-Framework/testing_site/
```
