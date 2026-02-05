---
applyTo: "**/*.py,**/*.agent.md,**/*.prompt.md"
---

# Python Terminal Commands Execution Guidelines

## Goals
- Prevent "module not found" errors when agents run Python commands via terminals.
- Ensure all Python commands execute within the project's virtual environment (`.venv`).
- Standardize terminal command patterns across all agents and modules.

## Rules

### 1. **ALWAYS Activate Virtual Environment**
When using `run_in_terminal` to execute Python commands, ALWAYS activate `.venv` first.

**Pattern 1 (Recommended)**: Chain activation with command
```bash
source .venv/bin/activate && python <command>
```

**Pattern 2 (Alternative)**: Use venv Python directly
```bash
.venv/bin/python <command>
```

### 2. **Apply to ALL Python Executables**
This rule applies to:
- `python` or `python3` script execution
- `pip install` package installation
- `pytest` test execution
- `python -m <module>` module execution
- Any Python-based CLI tools

### 3. **Examples**

**CORRECT ✓**
```bash
# Running a script
source .venv/bin/activate && python adhd_framework.py refresh

# Installing packages
source .venv/bin/activate && pip install requests

# Running pytest
source .venv/bin/activate && pytest tests/

# Running module
source .venv/bin/activate && python -m stocks_data_manager

# Direct venv usage
.venv/bin/python adhd_framework.py refresh
.venv/bin/pip install requests
```

**INCORRECT ✗**
```bash
# Missing venv activation - WILL FAIL
python adhd_framework.py refresh
pip install requests
pytest tests/
python -m stocks_data_manager
```

### 4. **Windows Alternative**
On Windows systems, use:
```bash
.venv\Scripts\activate && python <command>
```
Or:
```bash
.venv\Scripts\python.exe <command>
```

## Critical Notes
- The virtual environment `.venv` is located at the project root.
- NEVER assume system Python has project dependencies installed.
- If `.venv` doesn't exist, create it first with: `python -m venv .venv`
- Always verify the venv is activated before running Python commands.
