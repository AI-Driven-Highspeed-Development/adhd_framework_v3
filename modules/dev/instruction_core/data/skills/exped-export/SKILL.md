---
name: exped-export
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

Full YAML frontmatter schema for scout reports with detected project, blockers, warnings, and adaptation hints:
→ See [scout-report-schema.yaml](assets/scout-report-schema.yaml)

---

## Readiness Gate Checks

Three tiers of gate checks: Hard Blockers, Git State, and Source Readiness:
→ See [readiness-gates.md](assets/readiness-gates.md)

---

## Expedition Scope Schema

Full YAML schema for expedition scope with artifact lists and execution config:
→ See [expedition-scope-schema.yaml](assets/expedition-scope-schema.yaml)

---

## ADHD-Managed Header Format

All exported files must include the ADHD-managed header with source, expedition ID, hash, and modification rules. User Customization Zones are preserved during sync.
→ See [adhd-managed-header.md](assets/adhd-managed-header.md)

---

## Error Codes

Error codes by pipeline phase with severity levels:
→ See [error-codes.md](assets/error-codes.md)

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

Config files and key conventions per ecosystem (JS/Node, Python, Rust, Go, C#, Unity, ADHD):
→ See [ecosystem-files.md](assets/ecosystem-files.md)

### ADHD Concept → Target Mapping

Guidance for mapping ADHD directories to target ecosystem conventions (Vue3, React, Unity, Rust, Go):
→ See [concept-mapping.md](assets/concept-mapping.md)

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
