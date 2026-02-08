---
name: "testing"
description: "Testing and validation workflows — test folder conventions, Python terminal execution rules, and validation patterns. Covers where to put tests vs playground files, pytest conventions, venv activation requirements, and CI integration patterns. Use this skill when creating tests, running validation, or setting up test infrastructure."
---

# Testing

Testing conventions and Python execution rules for the ADHD Framework.

## When to Use
- Creating or running unit tests
- Setting up test infrastructure for a module
- Running Python commands in terminals
- Deciding between `tests/` and `playground/` folders

## Key Concepts
- **tests/**: Automated validation (pytest). Use for CI/CD, regression protection
- **playground/**: Interactive exploration. NOT production code. Demo scripts, API experiments
- **Venv Activation**: ALWAYS activate `.venv` before running Python commands
- **Pattern**: `source .venv/bin/activate && python <command>`

## Resources
- See `testing_folders.instructions.md` for folder decision tree
- See `python_terminal_commands.instructions.md` for terminal execution rules
