---
name: expedition
description: "Framework export workflows — exporting ADHD agents and instructions to external projects (Vue3, React, Unity, Rust, Go, any framework). Covers the 8-phase expedition pipeline, L1 Bundle architecture, artifact schemas, scout reports, readiness gates, chunk execution, verification, and ADHD-managed headers. Use this skill when exporting ADHD capabilities to non-ADHD projects or working with expedition artifacts."
---

# Expedition

Export ADHD Framework agents and instructions to external projects.

## When to Use
- Exporting agents/instructions to a Vue3, React, Unity, Rust, Go, or other external project
- Running the 8-phase expedition pipeline
- Creating or validating expedition artifacts (scout reports, scopes, manifests)
- Adapting ADHD patterns for non-ADHD ecosystems

## Key Concepts
- **L1 Bundle Architecture**: Target projects remain pristine; sidecar owns all ADHD infrastructure
- **8-Phase Pipeline**: Scout → Readiness → Planning → Feasibility → 🛑 → Execution → Verification → 🛑 → Registry → 🛑 → MCP
- **Chunk execution**: ≤5 files/batch, ≤25 artifacts per expedition

---

## Pipeline Overview

```
Scout → Readiness → Planning → Feasibility → 🛑 → Execution → Verification → 🛑 → Registry → 🛑 → MCP
```

## Artifact Locations

| Artifact | Location | Notes |
|----------|----------|-------|
| Scout Report | `SIDECAR/.agent_plan/expedition/{target}/scout_report.md` | YAML frontmatter + markdown |
| Expedition Scope | `SIDECAR/.agent_plan/expedition/{target}/expedition_scope.yaml` | Full YAML |
| Adaptation Notes | `SIDECAR/.agent_plan/expedition/{target}/adaptation_notes.md` | Markdown |
| Manifest | `SIDECAR/.agent_plan/expedition/{target}/manifest.yaml` | Generated post-verify |
| Registry Manager | `SIDECAR/managers/{target}_module_registry_manager/` | Python module |
| MCP Module | `SIDECAR/mcps/{target}_adhd_mcp/` | Python module |

**Target receives (L1 Bundle):** `.github/`, `.vscode/mcp.json`, `CONTRIBUTING.md`

---

## Scout Report Schema

```yaml
---
expedition_id: "exp_YYYYMMDD_project_name"
target_path: "/absolute/path/to/target"
scout_timestamp: "ISO8601"

detected_project:
  type: known_framework | custom_framework | multi_framework | bare_project | monorepo
  primary_language: "string"
  languages_present: ["list"]
  frameworks:
    - name: "Vue3"
      version: "3.x"
      config_file: "vite.config.ts"
      confidence: high | medium | low
  observed_patterns:
    config_files: [{path, type}]
    build_system:
      detected: "npm | pnpm | yarn | cargo | go"
      lock_file: "string"
    directory_style: "feature-based | layer-based | hybrid"
    existing_agent_config: [{path, type}]

structure_health: healthy | degraded | incompatible

blockers:
  - code: "ERROR_CODE"
    message: "Human-readable message"
    severity: critical

warnings:
  - code: "WARN_CODE"
    message: "Human-readable message"
    suggestion: "How to fix"

recommendation: PROCEED | PROCEED_WITH_CAUTION | ABORT
abort_reason: "Only if recommendation is ABORT"

adaptation_hints:
  suggested_agent_location: ".github/agents/"
  suggested_instruction_location: ".github/instructions/"
  test_command: "npm test"
  build_command: "npm build"
---

# Scout Report: {project_name}

## 📁 Project Structure Analysis
{prose description}

## 🎯 Export Compatibility
{analysis}

## ⚠️ Concerns
{list of concerns}
```

---

## Readiness Gate Checks

### Tier 1: Hard Blockers (ALL must pass)
| Code | Check | Description |
|------|-------|-------------|
| `target_exists` | Target accessible | Path exists and readable |
| `not_adhd_to_adhd` | Not ADHD project | Cannot export ADHD→ADHD |
| `scope_bounded` | ≤25 artifacts | Max artifacts per expedition |
| `no_active_lock` | No lock file | Previous expedition complete |
| `not_detached_head` | On branch | Not in detached HEAD state |

### Tier 2: Git State
| Code | Behavior | Description |
|------|----------|-------------|
| `clean_working_directory` | BLOCKER | No uncommitted changes |
| `submodule_clean` | BLOCKER | No dirty submodules |
| `shallow_clone_detected` | WARNING | Incomplete git history |
| `untracked_in_target` | BLOCKER | Untracked files at destinations |
| `on_feature_branch` | WARNING | Not on main/master |
| `ahead_of_remote` | WARNING | Unpushed commits |

### Tier 3: Source Readiness
| Code | Check | Description |
|------|-------|-------------|
| `agents_exist` | Source agents present | instruction_core/data/agents/ |
| `instructions_exist` | Source instructions present | instruction_core/data/instructions/ |

---

## Expedition Scope Schema

```yaml
expedition:
  id: "exp_YYYYMMDD_project_name"
  created: "ISO8601"
  target:
    path: "/absolute/path"
    type: "vue3 | react | unity | rust | go | other"
  
  artifacts:
    agents:
      - source: "modules/dev/instruction_core/data/agents/xxx.adhd.agent.md"
        target: ".github/agents/xxx.agent.md"
        adaptation: transform | copy
        transformations:
          - add_framework_prefix
          - update_cross_refs
          - inject_header
    
    instructions:
      - source: "path/to/source.instructions.md"
        target: ".github/instructions/target.instructions.md"
        adaptation: transform | copy
    
    prompts:
      - source: "path/to/source.prompt.md"
        target: ".github/prompts/target.prompt.md"
        adaptation: copy
  
  execution:
    chunk_size: 5
    total_chunks: N
    mode: PAUSE | CONTINUOUS
```

---

## ADHD-Managed Header Format

All exported files MUST include this header:

```markdown
<!-- ═══════════════════════════════════════════════════════════════════
     ADHD-MANAGED FILE
     
     Source: {sidecar_path}
     Expedition: {expedition_id}
     Created: {timestamp}
     Hash: sha256:{hash}
     
     ⚠️ MODIFICATION RULES:
     - Lines between USER CUSTOMIZATION markers are YOURS to edit
     - All other lines will be overwritten on sync
     - To prevent sync: delete this header (file becomes unmanaged)
═══════════════════════════════════════════════════════════════════ -->
```

**User Customization Zone:**
```markdown
<!-- USER CUSTOMIZATION START -->
{user's custom content preserved during sync}
<!-- USER CUSTOMIZATION END -->
```

---

## Error Codes

| Code | Phase | Severity | Description |
|------|-------|----------|-------------|
| `NO_GIT` | Scout | critical | Target not a git repo |
| `ADHD_TO_ADHD` | Readiness | critical | Cannot export to ADHD project |
| `DIRTY_WORKING_DIR` | Readiness | blocker | Uncommitted changes |
| `SCOPE_EXCEEDED` | Readiness | critical | Too many artifacts |
| `COLLISION_DETECTED` | Feasibility | critical | File would overwrite |
| `HEADER_MISSING` | Verify | error | Exported file lacks header |
| `TARGET_POLLUTED` | Verify | critical | `.agent_plan/` found in target |

---

## HyperExped Reference

### Purpose
HyperExped exports ADHD Framework agents/instructions to external projects. This section provides runtime reference for edge cases and structure mapping.

### HyperExped Responsibilities
| Phase | Role | Output |
|-------|------|--------|
| 1: Scout | **Owner** | `scout_report.md` |
| 3: Planning | **Contributor** (with Dream) | `expedition_scope.yaml`, `adaptation_notes.md` |
| 5: Execution | **Coordinator** | Delegates to Smith |

### Execution Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Chunk size | ≤5 files/batch | Enables granular review and rollback |
| Max artifacts | ≤25 per expedition | Prevents overwhelming scope |
| Mode | PAUSE (default) | Human confirmation per chunk |

### Special Files by Ecosystem

| Ecosystem | Config Files | Key Conventions |
|-----------|--------------|-----------------|
| JavaScript/Node | `package.json`, `tsconfig.json`, `vite.config.ts` | `src/index.ts` (entry), `app/` or `pages/` (routes) |
| Python | `pyproject.toml`, `setup.py`, `requirements.txt` | `__init__.py`, `conftest.py`, `manage.py` (Django) |
| Rust | `Cargo.toml` | `src/lib.rs` or `src/main.rs`, `build.rs` |
| Go | `go.mod` | `main.go`, `internal/`, `cmd/` |
| C#/.NET | `*.csproj`, `*.sln` | `Program.cs`, `appsettings.json` |
| Unity | `ProjectSettings/ProjectSettings.asset` | `Packages/manifest.json`, `Assets/`, `*.asmdef` |
| ADHD Framework | `pyproject.toml`, `.config_template` | Triggers "Why are you here?" check |

### ADHD Concept → Target Mapping

| ADHD Concept | Vue3/Nuxt | React/Next.js | Unity | Rust | Go |
|--------------|-----------|---------------|-------|------|-----|
| `utils/` | `src/utils/` | `lib/utils/` | `Assets/Scripts/Utils/` | `src/utils/` | `internal/utils/` |
| `managers/` | `src/composables/` | `hooks/` or `services/` | `Assets/Scripts/Managers/` | `src/services/` | `internal/services/` |
| `modules/dev/` | `src/core/` | `lib/core/` | `Assets/Scripts/Core/` | `src/core/` | `pkg/core/` |

> These are GUIDANCE, not prescription. Observe actual target structure first.

### Export Locations

| Artifact Type | Primary Location | Fallback |
|---------------|------------------|----------|
| Agents | `.github/agents/` | `docs/ai-agents/` |
| Instructions | `.github/instructions/` | `docs/instructions/` |
| Prompts | `.github/prompts/` | `docs/prompts/` |

### Edge Cases

**ADHD-to-ADHD Export**: If target already has `[tool.adhd]`, present options: copy specific agents, sync via submodules, create new agents, or proceed anyway.

**Empty Project**: Suggest minimal structure, propose "bootstrap mode."

**Poorly Structured Project**: Present options: Restructure First / Proceed Anyway / Minimal Export / Abort.

**Non-VS Code Environment**: HALT and warn — `.agent.md` format is VS Code-specific.

**Monorepo**: Ask user to specify target package.

### Stopping Rules Classification

| Category | Example | Action |
|----------|---------|--------|
| **Semantic** | "NEVER edit source files directly" | VERBATIM copy |
| **Behavioral** | "STOP if user says 'no edit'" | VERBATIM copy |
| **Python-specific** | "Use `python -m pytest`" | ADAPT to target ecosystem |
| **ADHD-specific** | "Check pyproject.toml" | REMOVE |
