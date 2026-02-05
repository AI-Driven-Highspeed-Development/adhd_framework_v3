---
applyTo: "cores/instruction_core/data/agents/hyper_expedition.adhd.agent.md"
---

# HyperExped Reference Guide

## Purpose
HyperExped exports ADHD Framework agents/instructions to **external projects** (Vue3, React, Unity, Rust, Go, ANY framework). This file provides runtime reference for edge cases and structure mapping.

## Pipeline Context

HyperExped operates within an **8-phase expedition pipeline** orchestrated by HyperOrch:

```
Scout(1) → Readiness(2) → Planning(3) → Feasibility(4) → 🛑 → Execution(5) → Verify(6) → 🛑 → Registry(7) → 🛑 → MCP(8)
```

**HyperExped Responsibilities:**
| Phase | Role | Output |
|-------|------|--------|
| 1: Scout | **Owner** | `scout_report.md` |
| 3: Planning | **Contributor** (with Dream) | `expedition_scope.yaml`, `adaptation_notes.md` |
| 5: Execution | **Coordinator** | Delegates to Smith |

## L1 Bundle Architecture

**Key Principle:** Target projects remain pristine. Sidecar owns all ADHD infrastructure.

| Location | Assets |
|----------|--------|
| **Sidecar** | MCPs, registry managers, `.agent_plan/`, expedition profiles |
| **Target** | `.github/` (agents, instructions, prompts), `.vscode/mcp.json`, `CONTRIBUTING.md` |

**CRITICAL:** NO `.agent_plan/` in target. All planning artifacts stay in sidecar.

## Execution Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Chunk size | ≤5 files/batch | Enables granular review and rollback |
| Max artifacts | ≤25 per expedition | Prevents overwhelming scope |
| Mode | PAUSE (default) | Human confirmation per chunk |

## Special Files by Ecosystem

HyperExped must **dynamically discover** what special files the target uses. Do NOT assume ADHD patterns.

| Ecosystem | Config Files | Other Special Files & Conventions |
|-----------|--------------|-----------------------------------|
| JavaScript/Node | `package.json`, `tsconfig.json`, `vite.config.ts`, `next.config.js` | `package-lock.json`, `.nvmrc`, `src/index.ts` (entry), `app/` or `pages/` (routes) |
| Python | `pyproject.toml`, `setup.py`, `requirements.txt` | `__init__.py`, `conftest.py`, `manage.py` (Django) |
| Rust | `Cargo.toml` | `Cargo.lock`, `src/lib.rs` or `src/main.rs`, `build.rs` |
| Go | `go.mod` | `go.sum`, `main.go`, `internal/`, `cmd/` |
| C#/.NET | `*.csproj`, `*.sln` | `Directory.Build.props`, `Program.cs`, `appsettings.json` |
| Java/Kotlin | `build.gradle`, `pom.xml` | `settings.gradle`, `src/main/java/`, `Application.kt` |
| Unity | `ProjectSettings/ProjectSettings.asset` | `Packages/manifest.json`, `Assets/`, `Editor/`, `*.asmdef` |
| ADHD Framework | `init.yaml`, `.config_template` | `refresh.py`, `data/` — **triggers "Why are you here?" check** |

## ADHD Concept → Target Mapping

| ADHD Concept | Vue3/Nuxt | React/Next.js | Unity | Rust | Go |
|--------------|-----------|---------------|-------|------|-----|
| `utils/` | `src/utils/` | `lib/utils/` | `Assets/Scripts/Utils/` | `src/utils/` | `internal/utils/` |
| `managers/` | `src/composables/` | `hooks/` or `services/` | `Assets/Scripts/Managers/` | `src/services/` | `internal/services/` |
| `cores/` | `src/core/` | `lib/core/` | `Assets/Scripts/Core/` | `src/core/` | `pkg/core/` |
| `playground/` | `playground/` | `examples/` | `Assets/Examples/` | `examples/` | `examples/` |

> ⚠️ **These are GUIDANCE, not prescription.** Observe actual target structure first. If Vue3 project uses `helpers/`, export to `helpers/`.

## Export Locations

| Artifact Type | Primary Location | Fallback |
|---------------|------------------|----------|
| Agents | `.github/agents/` | `docs/ai-agents/` |
| Instructions | `.github/instructions/` | `docs/instructions/` |
| Prompts | `.github/prompts/` | `docs/prompts/` |
| If inaccessible | N/A | `.agent_plan/expedition/<project>/` |

## Edge Cases

### Case: ADHD-to-ADHD Export
If target has `init.yaml` + `cores/instruction_core/`:
```
🤨 HOLD UP — TARGET IS ALREADY AN ADHD PROJECT

Did you perhaps mean to:
1. 📋 Copy specific agents? → Use normal file copy
2. 🔄 Sync instruction_core? → Use git submodules or symlinks
3. 🆕 Create NEW agents? → Use HyperAgentSmith directly
4. 🚀 Proceed anyway (I know what I'm doing)
```

### Case: Empty Project
Suggest minimal structure, propose "bootstrap mode" with full ADHD pattern adoption.

### Case: Poorly Structured Project
Present options: Restructure First / Proceed Anyway (fallback location) / Minimal Export / Abort.

### Case: Non-VS Code Environment
HALT and warn: `.agent.md` format is VS Code-specific. Offer to export as generic markdown guides.

### Case: Monorepo
Ask user to specify target package. Export to package-specific `.github/` OR root.

## Improvisation Protocol

1. **Observe**: `list_dir` and `read_file` to understand existing structure
2. **Identify Patterns**: Look for existing `utils/`, `helpers/`, `lib/`, `docs/` folders
3. **Propose Mapping**: Present to user with Accept/Modify options
4. **Get Approval**: NEVER auto-place without confirmation
5. **Document**: Record mapping in export plan
