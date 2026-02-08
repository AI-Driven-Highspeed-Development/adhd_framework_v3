---
applyTo: "**/*.agent.md,modules/dev/instruction_core/data/agents/hyper_expedition.adhd.agent.md,modules/dev/instruction_core/data/agents/hyper_san_checker.adhd.agent.md"
---

# Expedition Pipeline Schema Reference

## Goals
- Define canonical schemas for all expedition artifacts
- Provide validation rules for expedition phases
- Ensure consistent data formats across pipeline

## Pipeline Overview
8-phase expedition with L1 Bundle architecture and 3 stop points.

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
  
  support_structures:
    - type: directory | mcp_config | breadcrumb
      owner: "smith"
      output_path: "path"
  
  sidecar_structures:
    expedition_folder: ".agent_plan/expedition/{target}/"
    registry_manager: "managers/{target}_module_registry_manager/"
    mcp_module: "mcps/{target}_adhd_mcp/"
  
  execution:
    chunk_size: 5
    total_chunks: N
    mode: PAUSE | CONTINUOUS
```

---

## Adaptation Notes Schema

```markdown
# Adaptation Notes: {Framework} Export

**Expedition ID:** exp_YYYYMMDD_project_name  
**Target Framework:** {framework}  
**Generated:** ISO8601

---

## 📂 Path Conventions

| Artifact Type | Source Pattern | Target Pattern |
|---------------|----------------|----------------|
| Agents | `*.adhd.agent.md` | `.github/agents/*.agent.md` |
| Instructions | `*.instructions.md` | `.github/instructions/*.instructions.md` |
| Prompts | `*.prompt.md` | `.github/prompts/*.prompt.md` |
| MCP Config | (generated) | `.vscode/mcp.json` |
| Breadcrumb | (generated) | `CONTRIBUTING.md` |

---

## 🔄 Transformations

| Original | Target Framework | Transformed |
|----------|------------------|-------------|
| `hyper_architect.adhd.agent.md` | vue3 | `hyper_architect.vue3.agent.md` |
| `hyper_architect.adhd.agent.md` | react | `hyper_architect.react.agent.md` |
| `hyper_architect.adhd.agent.md` | unity | `hyper_architect.unity.agent.md` |

---

## 🛑 Stopping Rules Adaptation

| Category | Example | Action |
|----------|---------|--------|
| Semantic | "NEVER edit source files" | VERBATIM |
| Python-specific | "Use pytest" | ADAPT |
| ADHD-specific | "Check pyproject.toml" | REMOVE |
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

## Manifest Schema

```yaml
expedition:
  id: "exp_YYYYMMDD_project_name"
  completed: "ISO8601"
  architecture: "L1 Bundle"
  target:
    path: "/absolute/path"
    name: "project_name"
  
  sidecar:
    path: "/path/to/sidecar"
    registry_manager: "managers/{target}_module_registry_manager/"
    mcp_module: "mcps/{target}_adhd_mcp/"
  
  artifacts:
    - source: "original/path"
      target: "deployed/path"
      hash: "sha256:xxx"
      header_injected: true
  
  verification:
    all_created: true
    headers_present: true
    cross_refs_valid: true
    no_target_pollution: true
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
| `MCP_CONFIG_INVALID` | Verify | error | `.vscode/mcp.json` missing or invalid |
| `BREADCRUMB_MISSING` | Verify | warning | `CONTRIBUTING.md` lacks sidecar pointer |

---

## Stopping Rules Classification

When adapting agents for target:

| Category | Example | Action |
|----------|---------|--------|
| **Semantic** | "NEVER edit source files directly" | VERBATIM copy |
| **Behavioral** | "STOP if user says 'no edit'" | VERBATIM copy |
| **Python-specific** | "Use `python -m pytest`" | ADAPT to target ecosystem |
| **ADHD-specific** | "Check `pyproject.toml` before..." | ADAPT or REMOVE |
| **Tool-specific** | References to ADHD MCP tools | ADAPT or REMOVE |
