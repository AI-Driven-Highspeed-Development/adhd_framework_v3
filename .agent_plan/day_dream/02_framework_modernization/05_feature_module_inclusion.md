# 05 - Feature: Module Inclusion

> Part of [Framework Modernization Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Module Inclusion:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  "I want to add an existing module to my project"                          │
│          │                                                                 │
│          ▼                                                                 │
│  ┌─────────────────────────────────────┐                                   │
│  │ CURRENT WORKFLOW                    │                                   │
│  │                                     │                                   │
│  │  1. Clone module repo manually      │  ← MANUAL STEP                    │
│  │  2. Put in correct directory        │  ← KNOW CONVENTION                │
│  │  3. Edit project init.yaml:         │  ← MANUAL EDIT                    │
│  │     modules:                        │                                   │
│  │       - https://github.com/...      │  ← GITHUB URL                     │
│  │  4. Run `adhd init`                 │  ← CUSTOM COMMAND                 │
│  │                                     │                                   │
│  │  OR after UV migration:             │                                   │
│  │  ???  (unclear how to add modules)  │  ← NO CLEAR PATH                  │
│  └─────────────────────────────────────┘                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Developer adding existing modules | 🔥🔥 Medium | Weekly |
| Developer sharing modules between projects | 🔥🔥🔥 High | Common pattern |

### ✨ The Vision

```
After Modernization:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  "I want to add an existing module to my project"                          │
│          │                                                                 │
│          ▼                                                                 │
│  ┌─────────────────────────────────────┐                                   │
│  │ NEW WORKFLOW                        │                                   │
│  │                                     │                                   │
│  │  Option A (Local module):           │                                   │
│  │    git clone <module_repo> cores/   │                                   │
│  │    uv sync                          │  ← AUTO-DETECTED BY GLOB          │
│  │                                     │                                   │
│  │  Option B (External dependency):    │                                   │
│  │    uv add <package-name>            │  ← STANDARD UV COMMAND            │
│  │                                     │                                   │
│  │  Option C (Path dependency):        │                                   │
│  │    uv add --path ../other-module    │  ← FOR LOCAL DEVELOPMENT          │
│  │                                     │                                   │
│  └─────────────────────────────────────┘                                   │
│                                                                            │
│  ✅ STANDARD UV WORKFLOWS - NO CUSTOM TOOLING NEEDED                       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Module inclusion becomes standard UV workflow: clone + `uv sync` for workspace members, `uv add` for dependencies.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Steps to add module | ❌ 4 manual steps | ✅ 2 standard steps |
| Custom tooling required | ❌ Yes (adhd init) | ✅ No (uv sync) |
| Format to learn | ❌ GitHub URLs in YAML | ✅ Standard uv commands |

---

## 🔧 The Spec

---

## 🎯 Overview

Module inclusion should NOT require custom ADHD commands. Instead, document and enable standard UV workflows:

1. **Workspace members**: Clone to appropriate directory, `uv sync`
2. **External dependencies**: `uv add <package>`
3. **Local path dependencies**: `uv add --path <path>`

Optionally, provide a convenience command `adhd include-module` that wraps these workflows.

**Priority:** P1  
**Difficulty:** `[KNOWN]`

---

## 📚 Prior Art

### Existing Solutions

| Solution | Type | Relevance | Status |
|----------|------|-----------|--------|
| `uv add` | Tool | High | ✅ Adopt |
| `uv add --path` | Tool | High | ✅ Adopt |
| Workspace glob patterns | Pattern | High | ✅ Adopt |

### Usage Decision

**Using:** UV's native dependency commands  
**How:** Document patterns, provide optional convenience wrapper  
**Why:** Standard tooling > custom tooling

---

## 👥 User Stories

| As a... | I want to... | So that... |
|---------|--------------|------------|
| Developer | Add existing ADHD module | I can reuse code |
| Developer | Add external pip package | I can use third-party libs |
| Developer | Add local module for development | I can work on multiple modules |

---

## ✅ Acceptance Criteria

- [ ] Cloning module to workspace directory + `uv sync` works
- [ ] `uv add <package>` works for external deps
- [ ] Documentation explains all three patterns
- [ ] (Optional) `adhd include-module` convenience command works

---

## 📊 Inclusion Patterns

### Pattern 1: Workspace Member (ADHD Module)

```bash
# Clone to workspace directory
git clone https://github.com/org/my_module.git cores/my_module

# Sync workspace (auto-detects new member)
uv sync

# Now importable!
python -c "from my_module import something"
```

**Why this works:** Root pyproject.toml has `members = ["cores/*"]`, so new directories are automatically included.

### Pattern 2: External Dependency

```bash
# Add PyPI package
uv add requests

# Add specific version
uv add "requests>=2.28"
```

### Pattern 3: Path Dependency (Local Development)

```bash
# Add local module not in workspace
uv add --path ../shared-utils

# This adds to pyproject.toml:
# [tool.uv.sources]
# shared-utils = { path = "../shared-utils" }
```

---

## 🛠️ Technical Notes

### Optional Convenience Command

```python
# adhd_framework.py (potential addition)
def include_module(self, args) -> None:
    """Include an existing module in the workspace."""
    source = args.source  # URL or path
    target_type = args.type  # core, manager, util, plugin
    
    if source.startswith("http"):
        # Clone from URL
        target_dir = self._get_type_directory(target_type)
        repo_name = extract_repo_name(source)
        clone_path = target_dir / repo_name
        subprocess.run(["git", "clone", source, str(clone_path)])
    else:
        # Local path
        subprocess.run(["uv", "add", "--path", source])
    
    # Sync workspace
    subprocess.run(["uv", "sync"])
```

### CLI Design (If Implemented)

```bash
# Clone and include ADHD module
adhd include-module https://github.com/org/my_module.git --type core

# Include local module
adhd include-module ../my_module --type util
```

---

## ⚠️ Edge Cases

| Scenario | Handling |
|----------|----------|
| Module directory doesn't match glob | Warning, suggest correct location |
| Module has no pyproject.toml | Error: must be UV-compatible |
| Module name conflicts | Error with clear message |
| Circular dependencies | UV handles this natively |

---

## ❌ Out of Scope

| Item | Rationale |
|------|-----------|
| Auto-discovery from GitHub | Standard git clone is clear enough |
| Module marketplace/registry | Overkill for current needs |
| Version pinning UI | `uv add package==version` works |

---

## 🔗 Dependencies

| Depends On | For |
|------------|-----|
| Root workspace with glob patterns | Auto-detection of new members |
| Modules have pyproject.toml | UV compatibility |

---

## [Custom] 🤔 Build vs Document Decision

**Question:** Should we build `adhd include-module` or just document UV patterns?

| Option | Pros | Cons |
|--------|------|------|
| Document only | Zero new code, standard tooling | Less discoverable |
| Build command | Guided workflow, validation | More code to maintain |

**Recommendation:** Start with documentation (P1), consider command for P2 if users request it.

---

**← Back to:** [04 - Feature: Module Creation](./04_feature_module_creation.md)  
**Next:** [06 - Feature: Refresh Modernization](./06_feature_refresh_modernization.md)
