# Good Skill (Self-Contained)

```yaml
---
name: testing
description: "Testing and validation workflows — test folder conventions, pytest execution, and CI integration patterns. Use when creating tests, deciding between tests/ and playground/, or running validation."
---

# Testing

## When to Use
- Creating or running unit tests
- Setting up test infrastructure

## Folder Decision Tree
### Step 1: Is this a scratch file?
- YES → `.temp_agent_work/`
- NO → Continue...

## Test Execution
```bash
source .venv/bin/activate && pytest tests/
```

## Critical Rules
- Always activate venv before running Python
- Check existing tests before creating new ones
```

**Why this works:**
- Description is keyword-rich and specific
- Body IS the actual content, not a pointer
- Includes actionable steps and examples
- Self-contained — no external dependencies to understand it
