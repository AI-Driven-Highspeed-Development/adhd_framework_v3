# 03 - Code Smells Catalog

> Part of [Code Quality Audit Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
┌───────────────────────────────────────────────────────────────────┐
│  Codebase has grown organically through rapid development.        │
│  No systematic way to find common issues.                         │
│  Different agents may miss different smell categories.            │
│                                                                   │
│  💥 "I fixed the obvious issue but missed 5 related ones"         │
│  💥 "Every module has slightly different patterns"                │
└───────────────────────────────────────────────────────────────────┘
```

### ✨ The Vision

```
┌───────────────────────────────────────────────────────────────────┐
│  Comprehensive checklist of smell categories.                     │
│  Detection patterns for automated and manual scanning.            │
│  Severity levels to prioritize fixes.                             │
└───────────────────────────────────────────────────────────────────┘
```

---

## 🔧 The Spec

## 🔴 Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 **Critical** | Active landmine, will break on refactor | Fix in P0/P1 |
| 🟠 **High** | Significant maintainability issue | Fix in P1 |
| 🟡 **Medium** | Code quality concern | Fix in P2 |
| 🟢 **Low** | Nice to have, polish | Optional |

---

## 🎯 Code Smell Categories

### 1. Path Manipulation Hacks 🔴 Critical

**Description**: Fragile path resolution using relative parent traversal or hardcoded paths.

#### Patterns to Detect

| Pattern | Severity | Detection Method |
|---------|----------|------------------|
| `.parent.parent.parent` | 🔴 Critical | Grep: `\.parent\.parent` |
| `Path(__file__).resolve().parent...` | 🔴 Critical | Grep: `__file__.*parent` |
| Hardcoded `/home/`, `/Users/` | 🔴 Critical | Grep: `(/home/\|/Users/)` |
| `os.path.join(os.path.dirname(__file__), "..", "..")` | 🔴 Critical | Grep: `dirname.*\.\.` |

#### Known Instances

| File | Line | Pattern | Fix Strategy |
|------|------|---------|--------------|
| project_creator.py | 32 | `Path(__file__).parent.parent.parent` | Use workspace_core |

#### Recommended Fix Pattern

```python
# ❌ Before
FRAMEWORK_ROOT = Path(__file__).parent.parent.parent

# ✅ After
from workspace_core import get_framework_root
FRAMEWORK_ROOT = get_framework_root()
```

**Note**: `workspace_core` needs a `get_framework_root()` function if it doesn't exist.

---

### 2. sys.path Manipulation 🔴 Critical

**Description**: Runtime modification of import paths, making imports unpredictable.

#### Patterns to Detect

| Pattern | Severity | Detection Method |
|---------|----------|------------------|
| `sys.path.insert(0, ...)` | 🔴 Critical | Grep: `sys\.path\.insert` |
| `sys.path.append(...)` | 🔴 Critical | Grep: `sys\.path\.append` |
| `importlib` hacks | 🟠 High | Manual review |

#### Known Instances

| File | Line | Context | Fix Strategy |
|------|------|---------|--------------|
| `.agent_plan/red_team/*/attack_*.py` | Various | Test files | Use pytest with proper conftest.py |

#### Recommended Fix Pattern

```python
# ❌ Before (in test file)
sys.path.insert(0, str(PROJECT_ROOT))
from module import thing

# ✅ After (in conftest.py)
# Configure pytest to add PROJECT_ROOT to path
# Or use proper package installation with -e
```

**Note**: Test files in `.agent_plan/red_team/` may be acceptable since they're sandboxed attack simulations.

---

### 3. File Length Violations 🟠 High

**Description**: Files exceeding maintainability thresholds.

#### Thresholds

| Threshold | Severity | Action |
|-----------|----------|--------|
| >600 LOC | 🟠 High | Must split or document justification |
| >400 LOC | 🟡 Medium | Review for splitting opportunities |
| >300 LOC | 🟢 Low | Monitor |

#### Known Instances

| File | LOC | Category | Action |
|------|-----|----------|--------|
| config_keys.py | 1011 | Auto-generated | ✅ **ACCEPTABLE** — auto-gen, no cognitive load |
| adhd_controller.py | 745 | Main logic | 🔴 Must split |
| modules_controller.py | 465 | Controller | 🟡 Review |
| helpers.py (adhd_mcp) | 455 | Helpers | 🟡 Review |
| api.py (github_api) | 453 | API wrapper | 🟡 Review |

#### Detection Command

```bash
find modules/ -name "*.py" -exec wc -l {} \; | sort -rn | head -20
```

---

### 4. Function Length Violations 🟠 High

**Description**: Functions exceeding cognitive load thresholds.

#### Thresholds

| Threshold | Severity | Action |
|-----------|----------|--------|
| >50 LOC | 🟠 High | Must refactor |
| >30 LOC | 🟡 Medium | Review for extraction |
| >20 LOC | 🟢 Low | Monitor complexity |

#### Detection Command

```bash
# Use AST analysis or ruff rule
ruff check . --select=PLR0915  # Too many statements
```

---

### 5. Deep Nesting 🟡 Medium

**Description**: Code with >3 levels of indentation indicating complex control flow.

#### Patterns to Detect

| Pattern | Severity | Detection Method |
|---------|----------|------------------|
| >3 indentation levels | 🟡 Medium | Manual review, AST |
| Nested try/except | 🟡 Medium | Grep: `except.*try` |
| Callback pyramids | 🟠 High | Manual review |

#### Recommended Fix Patterns

```python
# ❌ Before
if condition1:
    if condition2:
        if condition3:
            if condition4:
                do_thing()

# ✅ After (guard clauses)
if not condition1:
    return
if not condition2:
    return
if not condition3:
    return
if condition4:
    do_thing()
```

---

### 6. Dead Code 🟡 Medium

**Description**: Unused imports, functions, variables, or classes.

#### Patterns to Detect

| Pattern | Severity | Detection Method |
|---------|----------|------------------|
| Unused imports | 🟡 Medium | Ruff: F401 |
| Unused variables | 🟡 Medium | Ruff: F841 |
| Unused functions | 🟡 Medium | Manual + IDE |
| Commented-out code | 🟢 Low | Grep: `#.*def \|#.*class ` |

#### Detection Commands

```bash
# Ruff catches most
ruff check . --select=F401,F841

# For unused functions - use IDE "Find Usages" or manual
```

---

### 7. Code Duplication 🟡 Medium

**Description**: Copy-pasted logic across modules.

#### Common Duplication Patterns in ADHD

| Pattern | Where to Look | Detection |
|---------|---------------|-----------|
| Path resolution | All modules | Grep: `Path(__file__)` |
| Logger initialization | All modules | Grep: `Logger(name=` |
| Config loading | Multiple modules | Grep: `ConfigManager()` |
| Error handling boilerplate | All modules | Manual review |

#### Detection Strategy

1. Search for similar function signatures
2. Look for copy-paste indicators (similar variable names)
3. Use `jscpd` or similar tool for automated detection

---

### 8. Magic Numbers/Strings 🟡 Medium

**Description**: Hardcoded values without named constants.

#### Patterns to Detect

| Pattern | Severity | Detection Method |
|---------|----------|------------------|
| Hardcoded file paths | 🟠 High | Grep: `".*\.py"\|".*\.yaml"` |
| Hardcoded URLs | 🟠 High | Grep: `https?://` |
| Numeric literals (non-obvious) | 🟡 Medium | Manual review |
| Timeout values | 🟡 Medium | Grep: `timeout=\d` |

#### Recommended Fix Pattern

```python
# ❌ Before
response = requests.get(url, timeout=30)
if len(items) > 100:
    paginate()

# ✅ After
DEFAULT_TIMEOUT_SECONDS = 30
MAX_ITEMS_PER_PAGE = 100

response = requests.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
if len(items) > MAX_ITEMS_PER_PAGE:
    paginate()
```

---

### 9. Stale Comments 🟢 Low

**Description**: Comments that don't match the code they describe.

#### Patterns to Detect

| Pattern | Severity | Detection Method |
|---------|----------|------------------|
| TODO without issue link | 🟡 Medium | Grep: `# TODO(?!:.*#\d)` |
| FIXME without context | 🟡 Medium | Grep: `# FIXME` |
| Docstrings mismatching function | 🟡 Medium | Manual review |
| Commented-out code | 🟢 Low | Manual review |

---

### 10. God Classes 🟡 Medium

**Description**: Classes doing too many things, violating Single Responsibility.

#### Indicators

| Indicator | Threshold | Detection |
|-----------|-----------|-----------|
| Methods count | >15 methods | AST analysis |
| Lines in class | >300 LOC | Manual count |
| Mixed responsibilities | N/A | Manual review |
| Too many dependencies | >7 imports | Review imports |

#### Likely Candidates

| Class | File | Methods (est.) | Review Priority |
|-------|------|----------------|-----------------|
| `ModulesController` | modules_controller.py | 15+ | 🟡 |
| `ProjectCreator` | project_creator.py | 10+ | 🟡 |
| `ConfigManager` | config_manager.py | 10+ | 🟡 |

---

### 11. Circular Dependencies 🟠 High

**Description**: Import cycles between modules.

#### Detection Strategy

1. Run `python -c "import module"` and watch for ImportError
2. Use `pydeps` tool for visualization
3. Manual review of import statements

#### Detection Command

```bash
# Install pydeps and generate graph
pydeps modules/foundation --cluster --no-show
```

---

### 12. Inconsistent Error Handling 🟡 Medium

**Description**: Mixed patterns for exception handling across modules.

#### Patterns to Check

| Pattern | Expected | Check |
|---------|----------|-------|
| Custom exceptions | Use `ADHDError` | Grep: `raise (?!ADHDError)` |
| Bare except | Never use | Grep: `except:` |
| Exception swallowing | Avoid | Grep: `except.*pass` |
| Logging before raise | Always | Manual review |

---

## 📋 Master Detection Checklist

### Automated (Ruff)

```bash
ruff check . --select=F,E,W,C90,I,N,UP,B,A,C4,DTZ,T10,EM,ISC,ICN,PIE,PT,Q,RSE,RET,SIM,TID,ARG,ERA,PL
```

### Grep Commands

```bash
# Path hacks
grep -rn "\.parent\.parent" modules/
grep -rn "sys\.path\.(insert|append)" modules/

# Magic strings
grep -rn "https://" modules/ --include="*.py" | grep -v "# " | grep -v '"""'

# Dead code indicators
grep -rn "# TODO" modules/
grep -rn "# FIXME" modules/
grep -rn "# HACK" modules/
```

### Manual Review Points

For each module:
- [ ] File length under 600 LOC?
- [ ] Functions under 50 LOC?
- [ ] Nesting under 4 levels?
- [ ] Single responsibility?
- [ ] Consistent with sibling modules?

---

## 📊 Smell Inventory Template

Use this template when scanning each module:

```markdown
### Module: {module_name}

**Scan Date**: YYYY-MM-DD  
**Scanned By**: {agent}

| Category | Found | Severity | Location | Notes |
|----------|-------|----------|----------|-------|
| Path Hacks | ❌ None | - | - | - |
| sys.path | ❌ None | - | - | - |
| File Length | ⚠️ 1 | 🟡 | api.py (453) | Approaching limit |
| Function Length | ❌ None | - | - | - |
| Deep Nesting | ❌ None | - | - | - |
| Dead Code | ⚠️ 2 | 🟡 | L45, L89 | Unused imports |
| Duplication | ❌ None | - | - | - |
| Magic Values | ⚠️ 1 | 🟡 | L102 | Hardcoded timeout |
| Stale Comments | ❌ None | - | - | - |
| God Classes | ❌ None | - | - | - |
| Circular Deps | ❌ None | - | - | - |
| Error Handling | ❌ None | - | - | - |

**Action Items**:
1. Fix unused imports (L45, L89)
2. Extract timeout to constant (L102)
```
