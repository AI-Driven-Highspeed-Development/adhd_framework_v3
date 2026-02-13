# README Structure Reference

Detailed specification for each required section in a module README.

---

## Required Section Order

| # | Section | Required | Description |
|---|---------|----------|-------------|
| 1 | Title | Yes | `# <Human-friendly Name>` + one-sentence intro |
| 2 | Overview | Yes | 3–5 bullets: what it is, when to use, key behavior |
| 3 | Features | Yes | Bulleted key capabilities |
| 4 | Quickstart | Yes | 1–2 runnable code snippets (happy path) |
| 5 | API | Yes | Minimal outline of public classes and main methods |
| 6 | Notes | No | Implementation or behavioral caveats |
| 7 | Requirements & prerequisites | Yes | External packages only |
| 8 | Troubleshooting | Yes | 3–6 common issues with fixes |
| 9 | Module structure | Yes | Short file tree with one-line comments |
| 10 | See also | Yes | 2–4 related modules |

---

## Section Details

### 1. Title
```markdown
# Module Name

One-sentence description starting with a succinct adjective or phrase.
```

### 2. Overview
```markdown
## Overview
- What this module is
- When to use it
- Key behavior or design decision
```

### 3. Features
```markdown
## Features
- Feature one
- Feature two
```

### 4. Quickstart
```markdown
## Quickstart
```python
from <package_import_path> import <MainClass>

obj = MainClass(...)
obj.do_work(...)
```
```

**Import rules:**
- Use package imports: `from <package_name> import <ExportedClass>`
- Check `__init__.py` for `__all__` or explicit exports
- No star imports

### 5. API
```markdown
## API
```python
class MainClass:
    def __init__(...): ...
    def do_work(self, arg: Type) -> Return: ...
```
```

### 6. Notes (Optional)
```markdown
## Notes
- Implementation caveat or behavioral note
```

### 7. Requirements & prerequisites
```markdown
## Requirements & prerequisites
- dependency-name
```
List external packages only. ADHD module dependencies are resolved via workspace.

### 8. Troubleshooting
```markdown
## Troubleshooting
- **Issue**: Fix description
- **Issue**: Fix description
```

### 9. Module structure
```markdown
## Module structure
```
module_name/
├─ __init__.py          # exports
├─ main_file.py         # main implementation
├─ README.md            # this file
├─ tests/               # unit tests (optional)
└─ playground/          # exploration scripts (optional)
```
```

### 10. See also
```markdown
## See also
- Related Module A
- Related Module B
```
Reference sibling modules by human name. Use file links only when it clarifies navigation.
