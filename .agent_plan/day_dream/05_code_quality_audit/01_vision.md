# 01 - Vision & Scope

> Part of [Code Quality Audit Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
┌─────────────────────────────────────────────────────────────────┐
│  Developer reads project_creator.py                             │
│                                                                 │
│  Line 32: FRAMEWORK_ROOT = Path(__file__).parent.parent.parent  │
│                                                                 │
│  💥 "Wait... how many parents? What does this even point to?"   │
│  💥 "What if the file moves? This will break silently."         │
│  💥 "Is this pattern copied elsewhere? How many land mines?"    │
└─────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| AI Agents | 🔥🔥🔥 High | Every refactor |
| New Contributors | 🔥🔥🔥 High | Day 1 confusion |
| Maintainers | 🔥🔥 Medium | When things break |

**Context**: The Folder Structure Revamp (P0-P5) successfully reorganized the project. But rapid development left code smells that increase cognitive load and create maintenance landmines.

### ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  Developer reads project_creator.py                             │
│                                                                 │
│  from workspace_core import get_framework_root                  │
│  FRAMEWORK_ROOT = get_framework_root()                          │
│                                                                 │
│  ✅ Clear intent: "I need the framework root"                   │
│  ✅ Single source of truth: workspace_core owns path resolution │
│  ✅ Tested: workspace_core has tests for this                   │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> We're systematically hunting and fixing code smells so that developers (human and AI) can understand, modify, and trust the codebase without fear of hidden landmines.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Path hack instances | ❌ 1+ | ✅ 0 |
| sys.path manipulation | ❌ 4 (test files) | ✅ 0 (proper test setup) |
| Files >600 LOC | ❌ 2 | ✅ 0 (split or justified) |
| Magic strings/numbers | ❌ Unknown | ✅ Cataloged, converted to constants |
| Dead code | ❌ Unknown | ✅ Removed |

---

## 🔧 The Spec

### Goals

| Goal | Description | Measurable Outcome |
|------|-------------|-------------------|
| **G1: Path Sanity** | Eliminate all `.parent.parent` patterns | Zero path hacks in production code |
| **G2: Code Health** | Fix obvious code smells | All files <600 LOC, functions <50 LOC |
| **G3: Dead Code Removal** | Remove unused code | Zero unused imports/functions detected |
| **G4: Consistency** | Consistent patterns across modules | Unified approach to common problems |
| **G5: Documentation** | Mark technical debt explicitly | All remaining debt has `# DEBT:` comments |

### Non-Goals

| Non-Goal | Why Excluded |
|----------|--------------|
| ❌ Redesign module boundaries | Already done in Folder Structure Revamp |
| ❌ Add new features | This is cleanup, not enhancement |
| ❌ Change public APIs | Behavioral changes out of scope |
| ❌ Performance optimization | Focus on readability, not speed |
| ❌ Add comprehensive tests | Test coverage is separate project |

---

## 🔍 Prior Art & Existing Solutions

| Solution | BUY/BUILD/WRAP | Rationale |
|----------|----------------|-----------|
| **Ruff** (linter) | ✅ BUY | Industry standard, already in dev deps |
| **Pylint** | 🚫 Skip | Ruff covers most cases, less config overhead |
| **Custom scripts** | ✅ BUILD | For ADHD-specific patterns (`.parent` chains) |
| **SonarQube** | 🚫 Skip | Overkill for framework, Ruff sufficient |

### Detection Strategy

1. **Automated**: Use Ruff for standard Python smells
2. **Pattern Search**: Use grep for ADHD-specific patterns (path hacks)
3. **Manual Review**: Module-by-module audit for architectural issues

---

## 🗺️ System Context

This audit operates on the existing module structure:

```
modules/
├── foundation/          # 15 modules - Bootstrap time
│   ├── cli_manager/
│   ├── config_manager/
│   ├── creator_common_core/
│   ├── exceptions_core/
│   ├── github_api_core/
│   ├── instruction_core/
│   ├── logger_util/
│   ├── module_creator_core/
│   ├── modules_controller_core/
│   ├── project_creator_core/
│   ├── questionary_core/
│   ├── temp_files_manager/
│   ├── uv_migrator_core/
│   ├── workspace_core/
│   └── yaml_reading_core/
├── runtime/             # 0 modules (expected for framework)
└── dev/                 # 1 module
    └── adhd_mcp/
```

---

## 📋 Success Criteria

### Exit Criteria for Audit Completion

- [ ] All modules have been scanned and documented
- [ ] All high-severity smells (path hacks, sys.path) eliminated
- [ ] No files exceed 600 LOC (or have documented justification)
- [ ] No functions exceed 50 LOC (or have documented justification)
- [ ] All changes pass HyperSan validation
- [ ] `ruff check .` returns clean
