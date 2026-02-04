# 04 - Research: PyPI & Distribution Options

> Part of [Workspace Monorepo Migration Blueprint](./00_index.md)
>
> **Status:** ⏳ [TODO] | **Difficulty:** `[KNOWN]` to `[EXPERIMENTAL]`

---

## 📖 The Story

### 😤 The Pain

```
┌─────────────────────────────────────────────────────────────────┐
│  User Questions:                                                │
│                                                                 │
│  ❓ "Can I upload PRIVATE packages to PyPI?"                    │
│  ❓ "Can I update packages rapidly like a git repo?"            │
│  ❓ "What are my options for sharing packages?"                 │
│                                                                 │
│  Without understanding distribution, can't make informed        │
│  decisions about package sharing strategy.                      │
└─────────────────────────────────────────────────────────────────┘
```

### ✨ The Vision

> Clear understanding of ALL distribution options with recommendation for ADHD Framework.

### 🎯 Key Questions Answered

| Question | Answer |
|----------|--------|
| Can PyPI host private packages? | ❌ No, public only |
| What are private alternatives? | GitHub Packages, git+https, self-hosted |
| Can we update rapidly like git? | ✅ Yes, with git-based installs |
| What's best for ADHD? | 🎯 Recommendation below |

---

## 🔧 The Spec

---

## 🌐 What is PyPI?

### The Basics

**PyPI** (Python Package Index) is the official repository for Python packages.

| Attribute | Value |
|-----------|-------|
| **URL** | https://pypi.org/ |
| **Packages** | 500,000+ |
| **Cost** | Free |
| **Hosting** | Python Software Foundation |
| **Access** | **PUBLIC ONLY** |

### How Publishing Works

```
┌─────────────────────────────────────────────────────────────────┐
│  PUBLISHING FLOW                                                │
│                                                                 │
│  Source Code                                                    │
│       ↓                                                         │
│  uv build (or python -m build)                                  │
│       ↓                                                         │
│  dist/                                                          │
│    ├── package-name-1.0.0.tar.gz    ← Source distribution       │
│    └── package_name-1.0.0-py3-none-any.whl  ← Wheel (binary)    │
│       ↓                                                         │
│  uv publish (or twine upload)                                   │
│       ↓                                                         │
│  PyPI (pypi.org)                                                │
│       ↓                                                         │
│  Users: pip install package-name                                │
└─────────────────────────────────────────────────────────────────┘
```

### Publishing Commands

```bash
# 1. Build the package
uv build

# 2. Publish to PyPI (needs API token)
uv publish

# Or with explicit credentials
uv publish --token pypi-xxxxx

# Test with TestPyPI first
uv publish --repository testpypi
```

### TestPyPI

A separate instance for testing your publishing workflow:

| Attribute | Value |
|-----------|-------|
| **URL** | https://test.pypi.org/ |
| **Purpose** | Test uploads before real PyPI |
| **Data** | Periodically wiped |

```bash
# Upload to test
uv publish --repository testpypi

# Install from test
pip install --index-url https://test.pypi.org/simple/ my-package
```

---

## 🔒 Can PyPI Host Private Packages?

### Short Answer: **NO**

PyPI is **public only**. Every package uploaded is visible to everyone.

```
┌─────────────────────────────────────────────────────────────────┐
│  PyPI.org                                                       │
│  ─────────                                                      │
│                                                                 │
│  ✅ Public packages (default)                                   │
│  ❌ Private packages (NOT SUPPORTED)                            │
│  ❌ Access control (NOT SUPPORTED)                              │
│  ❌ Org-level visibility (NOT SUPPORTED)                        │
│                                                                 │
│  If you upload to PyPI, ANYONE can install it.                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why?

PyPI's mission is to be the **public** repository for Python packages. Private hosting is out of scope.

---

## 🏢 Private Package Alternatives

### Option 1: GitHub Packages `[KNOWN]`

**What:** Private package registry hosted by GitHub.

| Attribute | Value |
|-----------|-------|
| **Cost** | Free for public repos, included with GitHub plans for private |
| **Authentication** | GitHub token (PAT or GITHUB_TOKEN) |
| **Supports** | npm, Maven, Docker, NuGet, RubyGems, **Python** (limited) |

**Limitation:** GitHub Packages Python support is rudimentary. Not a full PyPI-compatible server.

**Alternative:** Use GitHub as a Git repository source (see Option 6).

---

### Option 2: GitLab Package Registry `[KNOWN]`

**What:** PyPI-compatible registry built into GitLab.

| Attribute | Value |
|-----------|-------|
| **Cost** | Free (GitLab.com) or self-hosted |
| **Authentication** | GitLab token |
| **PyPI Compatible** | ✅ Yes |

```bash
# Configure
uv config set-keyring gitlab https://gitlab.com/api/v4/projects/PROJECT_ID/packages/pypi

# Or in pyproject.toml
[tool.uv]
index-url = "https://gitlab.com/api/v4/projects/PROJECT_ID/packages/pypi/simple"
```

---

### Option 3: AWS CodeArtifact `[KNOWN]`

**What:** Managed package repository service from AWS.

| Attribute | Value |
|-----------|-------|
| **Cost** | Pay-per-use (~$0.05/GB storage, ~$0.05/10k requests) |
| **Authentication** | AWS IAM |
| **PyPI Compatible** | ✅ Yes |

```bash
# Get auth token
aws codeartifact get-authorization-token --domain my-domain --query authorizationToken --output text

# Configure pip/uv
export UV_INDEX_URL="https://aws:TOKEN@my-domain-111122223333.d.codeartifact.us-east-1.amazonaws.com/pypi/my-repo/simple/"
```

**Best for:** Organizations already on AWS with IAM infrastructure.

---

### Option 4: Google Artifact Registry `[KNOWN]`

**What:** Managed package repository service from Google Cloud.

| Attribute | Value |
|-----------|-------|
| **Cost** | Pay-per-use (~$0.10/GB storage) |
| **Authentication** | Google Cloud IAM |
| **PyPI Compatible** | ✅ Yes |

```bash
# Configure
gcloud artifacts print-settings python --repository=my-repo --location=us-central1
```

**Best for:** Organizations already on GCP.

---

### Option 5: Self-Hosted (devpi, pypiserver) `[EXPERIMENTAL]`

**What:** Run your own PyPI-compatible server.

#### devpi

Full-featured, includes caching of PyPI packages.

```bash
# Install
pip install devpi-server devpi-web

# Start server
devpi-server --start --init

# Use
pip install --index-url http://localhost:3141/root/pypi/simple/ my-package
```

#### pypiserver

Simpler, lightweight option.

```bash
# Install
pip install pypiserver

# Serve packages from a directory
pypi-server run -p 8080 ~/packages/

# Use
pip install --index-url http://localhost:8080/simple/ my-package
```

**Best for:** Complete control, air-gapped environments.

**Difficulty:** `[EXPERIMENTAL]` — Requires server maintenance.

---

### Option 6: Git-Based Installs ⭐ RECOMMENDED FOR ADHD

**What:** Install directly from Git repositories without publishing.

```toml
# In pyproject.toml dependencies
[project]
dependencies = [
    # Basic: latest commit on default branch
    "my-package @ git+https://github.com/org/repo.git",
    
    # Specific tag (release)
    "my-package @ git+https://github.com/org/repo.git@v1.0.0",
    
    # Specific branch (track development)
    "my-package @ git+https://github.com/org/repo.git@main",
    
    # Specific commit (pinned)
    "my-package @ git+https://github.com/org/repo.git@abc123def",
    
    # Subdirectory within repo (monorepo)
    "my-package @ git+https://github.com/org/repo.git#subdirectory=packages/my-package",
]
```

#### With `[tool.uv.sources]` (Cleaner Syntax)

```toml
[project]
dependencies = ["my-package"]

[tool.uv.sources]
my-package = { git = "https://github.com/org/repo.git", tag = "v1.0.0" }

# Or tracking a branch
my-package = { git = "https://github.com/org/repo.git", branch = "main" }

# Or with subdirectory
my-package = { git = "https://github.com/org/repo.git", subdirectory = "packages/my-package" }
```

#### Private Repos

For private GitHub repos, authentication is handled via:

1. **SSH:** `git+ssh://git@github.com/org/repo.git`
2. **HTTPS with token:** `git+https://${GITHUB_TOKEN}@github.com/org/repo.git`
3. **Git credential helper:** Pre-configured in git config

| Attribute | Value |
|-----------|-------|
| **Cost** | Free (just GitHub hosting) |
| **Setup** | Zero (just URLs) |
| **Private** | ✅ Yes (with auth) |
| **Rapid Updates** | ✅ Yes (push to branch) |
| **Version Pinning** | ✅ Yes (tags, commits) |

**Best for:** ADHD Framework — already using GitHub, zero infrastructure needed.

---

### Option 7: Private PyPI Services (Gemfury, Packagr) `[KNOWN]`

**What:** Hosted private PyPI as a service.

| Service | Cost | Notes |
|---------|------|-------|
| **Gemfury** | $9/month | Simple, supports many languages |
| **Packagr** | $10/month | Python-focused |

**Best for:** Teams wanting hosted solution without self-hosting.

---

## ⚡ Can We Update Rapidly Like Git?

### The Problem with Traditional PyPI

```
Traditional PyPI Release Cycle:
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  Code Change → Bump Version → Build → Upload → Users Update  │
│       ↓            ↓            ↓        ↓          ↓        │
│     1 min       manual      1 min    1 min      manual       │
│                                                              │
│  Total: 5-10 minutes + manual steps per release              │
│  💥 NOT suitable for rapid iteration                         │
└──────────────────────────────────────────────────────────────┘
```

### Rapid Update Strategies

#### Strategy 1: Git Branch Tracking ⭐

```toml
[tool.uv.sources]
my-package = { git = "https://github.com/org/repo.git", branch = "main" }
```

Update workflow:
```bash
# Developer pushes to main
git push origin main

# Consumer updates
uv lock --upgrade-package my-package
uv sync
```

| Metric | Value |
|--------|-------|
| Time to update | ~30 seconds |
| Manual steps | `uv lock --upgrade-package` |
| Version bumps needed | ❌ No |

#### Strategy 2: Editable Installs (Development)

For local development, editable installs reflect changes **immediately**:

```bash
# In workspace, changes are instant
# No commands needed — Python imports the source directly
```

| Metric | Value |
|--------|-------|
| Time to update | **0 seconds** |
| Manual steps | None |
| Use case | Local development |

#### Strategy 3: Living at HEAD

For consumers who want the latest always:

```toml
# pyproject.toml
[project]
dependencies = ["adhd-framework"]

[tool.uv.sources]
adhd-framework = { git = "https://github.com/org/adhd_framework.git", branch = "main" }
```

CI/automation:
```bash
# Run regularly (nightly, weekly)
uv lock --upgrade
uv sync
```

**Warning:** Can break if main has breaking changes. Best with good CI.

#### Strategy 4: Tag-Based Releases (Semantic)

For production, pin to tags:

```toml
[tool.uv.sources]
adhd-framework = { git = "https://github.com/org/adhd_framework.git", tag = "v3.1.0" }
```

Release workflow:
```bash
# Developer tags a release
git tag v3.1.0
git push origin v3.1.0

# Consumer updates
# Edit pyproject.toml to new tag
uv lock
uv sync
```

| Metric | Value |
|--------|-------|
| Time to release | ~1 minute (just git tag) |
| Version bumps | ✅ Yes (tag name) |
| Stability | ✅ High (immutable tags) |

---

## 🎯 Recommendation for ADHD Framework

### The Question

> "Can we upload private packages to PyPI for selected users?"

### The Answer

**Don't use PyPI at all.** Use **Git-based installs**.

### Recommended Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  ADHD Framework Distribution Strategy                           │
│                                                                 │
│  INTERNAL (within monorepo):                                    │
│    → UV workspace (already in place)                            │
│    → Editable installs (instant updates)                        │
│                                                                 │
│  EXTERNAL (other projects using ADHD):                          │
│    → Git-based dependency                                       │
│    → Tag pinning for stability                                  │
│    → Branch tracking for bleeding edge                          │
│                                                                 │
│  ❌ NOT RECOMMENDED:                                            │
│    → PyPI (public, not suitable for internal tools)             │
│    → Private PyPI hosting (unnecessary complexity)              │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Works

| Requirement | Solution |
|-------------|----------|
| Private packages | GitHub private repo + git auth |
| Rapid updates | Branch tracking or editable installs |
| Version control | Git tags |
| Zero infrastructure | Just GitHub |
| Selective access | GitHub repo permissions |

### Example: External Project Using ADHD

```toml
# some_external_project/pyproject.toml
[project]
name = "my-ai-project"
dependencies = [
    "adhd-framework",
]

[tool.uv.sources]
adhd-framework = { 
    git = "https://github.com/AI-Driven-Highspeed-Dev/adhd_framework_v3.git",
    tag = "v3.0.0"  # Or branch = "main" for bleeding edge
}
```

---

## 📊 Comparison Matrix

| Option | Private | Rapid Updates | Cost | Complexity | ADHD Fit |
|--------|---------|---------------|------|------------|----------|
| PyPI | ❌ No | ❌ Slow | Free | Low | ❌ |
| GitHub Packages | ✅ Yes | ⚠️ Medium | Free | Medium | ⚠️ |
| AWS CodeArtifact | ✅ Yes | ⚠️ Medium | $$ | High | ❌ |
| GCP Artifact | ✅ Yes | ⚠️ Medium | $$ | High | ❌ |
| Self-hosted | ✅ Yes | ⚠️ Medium | $+ | High | ❌ |
| **Git-based** | ✅ Yes | ✅ Fast | Free | Low | ✅ **BEST** |

---

## 🔗 References

- **UV Git dependencies:** https://docs.astral.sh/uv/concepts/dependencies/#git-dependencies
- **PyPI:** https://pypi.org/help/
- **TestPyPI:** https://test.pypi.org/
- **devpi:** https://devpi.net/
- **pypiserver:** https://pypiserver.readthedocs.io/

---

**← Back to:** [Blueprint Index](./00_index.md) | **Next:** [Feature: Monorepo Structure](./05_feature_monorepo_structure.md)
