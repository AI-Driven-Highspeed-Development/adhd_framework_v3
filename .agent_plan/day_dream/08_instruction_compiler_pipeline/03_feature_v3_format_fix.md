# 03 - Feature: v3 Contamination Fix

> Part of [Instruction Compiler Pipeline Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│  BEFORE                              │  AFTER                               │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  instruction_controller.py L47:      │  Path(__file__).parent / "data"      │
│    root / "cores" / "instruction_    │  ✅ Derives from module location     │
│    core" / "data"                    │  ✅ official sync WORKS again        │
│    💥 Path doesn't exist             │                                      │
│    💥 Sync silently no-ops           │  Zero "cores/" refs in data files    │
│                                      │  ✅ All paths point to               │
│  20+ "cores/" refs in data files     │     modules/dev/instruction_core/    │
│  init.yaml/pip/sys.path mandated     │                                      │
│  adhd_framework_context teaches      │  Zero dead v2 tooling refs           │
│    agents that cores/ exists         │  ✅ pyproject.toml, uv, package      │
│                                      │     imports throughout               │
│  agents_format.instructions.md       │                                      │
│    missing argument-hint, handoffs   │  Agent format spec updated           │
│                                      │  ✅ argument-hint, handoffs, send    │
│                                      │                                      │
│  😤 Every AI agent learns wrong      │  😊 Clean, accurate foundation       │
│     facts from its own instructions  │     for P1 compilation pipeline      │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 🎯 One-Liner

> Fix the broken sync path, purge all v2 contamination (dead paths, dead tooling, wrong vocabulary) from 37 data files, and update the agent format spec to match actual v3 agent files.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| `official_source_path` | ❌ Points to non-existent `cores/instruction_core/data` | ✅ Derived from `Path(__file__).parent / "data"` |
| `cores/` references in data files | ❌ 20+ dead references | ✅ Zero |
| v2 tooling refs (init.yaml, pip, sys.path) | ❌ Present across files | ✅ Zero — replaced with pyproject.toml, uv, package imports |
| Agent format spec completeness | ❌ Missing argument-hint, handoffs, send | ✅ Complete v3 format documented |
| `modules.init.yaml.instructions.md` | ❌ Referenced as active (dead v2 artifact) | ✅ Purged — file listed for deletion |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Fix the silently broken instruction sync pipeline and establish a clean, v3-accurate baseline for all instruction_core data files before the compilation pipeline is built.

**Priority:** P0  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Fix `instruction_controller.py` line 47 broken path: `cores/instruction_core/data` → `Path(__file__).parent / "data"`
- Document the canonical v3 compliance reference (what makes a file v3-clean)
- Batch-fix all 37 files: stale `cores/` paths, `init.yaml` references, `pip`→`uv`, `sys.path.insert`→package imports, dead pattern purge
- Update `agents_format.instructions.md` to include `argument-hint`, `handoffs`, `send` fields
- Purge/delete `modules.init.yaml.instructions.md` references (dead v2 artifact — file no longer exists)
- Verification pass: re-audit all files, run `adhd refresh --full`, verify .github/ reflects corrected content
- Tag a git release before starting (safety checkpoint)

**Out of Scope:**
- Converting any file to `.flow` format (that's P1)
- Creating the `skills/` folder structure (that's [04 - Skills Adoption](./04_feature_skills_adoption.md))
- Modifying per-module `.instructions.md` files in module directories (they're owned by module authors)
- Changing `InstructionController` sync logic beyond the path fix (that's P1)
- Creating `init.yaml` files (dead v2 pattern — NOT part of v3)

---

## [Custom] 🎨 The 3-Layer Contamination Model

This is the framing for understanding what needs to be fixed and why. Each layer compounds the damage of the one below it.

### Layer 1 — Path References (Structural)

Dead `cores/instruction_core/` paths appear in `applyTo` frontmatter, body text, and examples. The `cores/` directory was renamed to `modules/dev/` during the v3 migration (blueprint 04).

**Files affected (confirmed by grep):**

| File | Location of `cores/` reference | Fix |
|------|-------------------------------|-----|
| `instructions/exped/expedition_schemas.instructions.md` | `applyTo` frontmatter (line 2), body (line 136) | → `modules/dev/instruction_core/data/agents/...` |
| `instructions/exped/hyper_exped_reference.instructions.md` | `applyTo` frontmatter (line 2), body (line 82) | → `modules/dev/instruction_core/data/agents/...` |
| `instructions/framework/adhd_framework_context.instructions.md` | Body (line 100): "Source: `cores/instruction_core/data/`" | → `modules/dev/instruction_core/data/` |
| `instructions/formats/instructions_format.instructions.md` | Body (line 57): "Place in `cores/instruction_core/data/instructions/`" | → `modules/dev/instruction_core/data/instructions/` |
| `instructions/formats/prompts_format.instructions.md` | Body (line 51): "Place in `cores/instruction_core/data/prompts/`" | → `modules/dev/instruction_core/data/prompts/` |
| `instructions/workflows/orch_routing_preset.instructions.md` | Body (line 69): "Read the agent's source file at `cores/instruction_core/...`" | → `modules/dev/instruction_core/data/agents/...` |

### Layer 2 — Tooling Mental Model (Behavioral)

Files mandate v2 tooling patterns that don't work in v3:

| Dead v2 Pattern | v3 Replacement | Files Affected |
|-----------------|----------------|----------------|
| `init.yaml` creation/usage | `pyproject.toml` with `[tool.adhd]` | `adhd_framework_context`, format specs, exped refs |
| `pip install` | `uv sync`, `uv add` | Module development instructions |
| `sys.path.insert(0, root)` | Package imports via uv editable install | Module development instructions |
| `requirements.txt` for ADHD deps | `[project].dependencies` in `pyproject.toml` | Multiple module/format instructions |
| `from cores.X import Y` | `from x import Y` (package import) | Framework context, module development |
| GitHub URLs in requirements | `[tool.uv.sources] x = { workspace = true }` | Any init.yaml-referencing file |

### Layer 3 — Structural Vocabulary (Conceptual)

`adhd_framework_context.instructions.md` — the single most-read instruction file — teaches agents:

```
# WRONG (current):
| `cores/` | Framework internals | NEVER create unless extending framework |
```

This tells every AI agent that `cores/` is a valid top-level directory. Agents build their mental model of the project around this. When they then try to navigate to `cores/instruction_core/`, they fail silently or make wrong assumptions.

**Fix:** Remove `cores/` from the folder taxonomy entirely. The v3 structure uses `modules/{foundation,runtime,dev}/` only.

---

## [Custom] 📋 V3 Compliance Reference

A file is v3-compliant when it passes ALL of these checks:

### Structural Accuracy
- [ ] Zero `cores/` path references (use `modules/{layer}/{name}/` instead)
- [ ] Zero `init.yaml` references as something to create or use
- [ ] Zero references to `modules.init.yaml.instructions.md` (dead file)
- [ ] All `applyTo` frontmatter paths resolve to actual files/directories

### Content Accuracy (Tooling)
- [ ] Package manager references use `uv` (not `pip`)
- [ ] Import patterns use package imports: `from x import Y` (not `sys.path.insert`)
- [ ] Dependency declarations use `[project].dependencies` in `pyproject.toml` (not `requirements:` in `init.yaml`, not GitHub URLs)
- [ ] Workspace resolution uses `[tool.uv.sources]` (not `pip install -e`)
- [ ] Module discovery references `pyproject.toml` with `[tool.adhd]` (not `init.yaml`)
- [ ] Layer declaration via `[tool.adhd].layer = "dev"` (not `init.yaml` `type:` field)

### Format Compliance
- [ ] Instructions: Valid `applyTo` frontmatter (or documented reason for omission)
- [ ] Agents: YAML frontmatter with `name`, `description`, `argument-hint`, `tools`, `handoffs` (where applicable)
- [ ] Prompts: Valid prompt format frontmatter

---

## [Custom] 🎨 Full File Audit Matrix

### Instructions (21 files across 7 subdirectories in `data/instructions/`)

| Subdirectory | File | v2 Issues Found | Fix Required |
|--------------|------|-----------------|--------------|
| `agents/` | `agent_common_rules.instructions.md` | — | Format check only |
| `agents/` | `agents_format.instructions.md` | Missing `argument-hint`, `handoffs`, `send` in format spec | Add v3 agent format fields |
| `agents/` | `hyper_san_output.instructions.md` | — | Format check only |
| `exped/` | `expedition_schemas.instructions.md` | `cores/instruction_core/` in `applyTo` (L2), body (L136) | Fix paths → `modules/dev/instruction_core/` |
| `exped/` | `hyper_exped_reference.instructions.md` | `cores/instruction_core/` in `applyTo` (L2), body (L82), `init.yaml` ref (L82) | Fix paths, remove init.yaml ref |
| `formats/` | `instructions_format.instructions.md` | `cores/instruction_core/` path ref (L57) | Fix path → `modules/dev/instruction_core/` |
| `formats/` | `prompts_format.instructions.md` | `cores/instruction_core/` path ref (L51) | Fix path → `modules/dev/instruction_core/` |
| `framework/` | `adhd_framework_context.instructions.md` | `cores/` in folder taxonomy, `cores/instruction_core/` source ref (L100) Potential wrong folder structure description | Remove `cores/` from taxonomy, fix source path |
| `modules/` | `mcp_development.instructions.md` | Potential v2 tooling refs and wrong folder structure description | Audit and fix |
| `modules/` | `module_development.instructions.md` | Potential init.yaml, pip, sys.path refs, and wrong folder structure description | Audit and fix |
| `modules/` | `module_instructions.instructions.md` | Potential init.yaml refs and wrong folder structure description | Audit and fix |
| `modules/` | `modules_readme.instructions.md` | Potential init.yaml refs | Audit and fix |
| `planning/` | `dream_assets.instructions.md` | — | Format check only |
| `planning/` | `dream_blueprint.instructions.md` | — | Format check only |
| `workflows/` | `orch_discussion_preset.instructions.md` | — | Format check only |
| `workflows/` | `orch_expedition_preset.instructions.md` | — | Format check only |
| `workflows/` | `orch_implementation_preset.instructions.md` | — | Format check only |
| `workflows/` | `orch_routing_preset.instructions.md` | `cores/instruction_core/` ref (L69) | Fix path |
| `workflows/` | `orch_testing_preset.instructions.md` | — | Format check only |
| `workflows/` | `python_terminal_commands.instructions.md` | — | Format check only |
| `workflows/` | `testing_folders.instructions.md` | — | Format check only |

### Agent Files (8 files in `data/agents/`)

| File | v2 Issues | Fix Required |
|------|-----------|--------------|
| `hyper_agent_smith.adhd.agent.md` | Verify frontmatter completeness | Check `argument-hint`, `handoffs`, `send` |
| `hyper_architect.adhd.agent.md` | Verify frontmatter completeness | Check `argument-hint`, `handoffs`, `send` |
| `hyper_day_dreamer.adhd.agent.md` | Verify frontmatter completeness | Check `argument-hint`, `handoffs`, `send` |
| `hyper_expedition.adhd.agent.md` | Verify frontmatter completeness + body `cores/` refs | Check all |
| `hyper_iq_guard.adhd.agent.md` | Verify frontmatter completeness | Check `argument-hint`, `handoffs`, `send` |
| `hyper_orchestrator.adhd.agent.md` | Verify frontmatter completeness + body `cores/` refs | Check all |
| `hyper_red.adhd.agent.md` | Verify frontmatter completeness | Check `argument-hint`, `handoffs`, `send` |
| `hyper_san_checker.adhd.agent.md` | Verify frontmatter completeness | Check `argument-hint`, `handoffs`, `send` |

### Prompt Files (3 files in `data/prompts/`)

| File | v2 Issues | Fix Required |
|------|-----------|--------------|
| `pull_modules.prompt.md` | Potential init.yaml/cores refs | Audit and fix |
| `push_modules.prompt.md` | Potential init.yaml/cores refs | Audit and fix |
| `update_requirements.prompt.md` | References `modules.init.yaml.instructions.md` (L53) — dead file | Remove reference, update to v3 pyproject.toml patterns |

### Dead Files to Purge

| File | Status | Action |
|------|--------|--------|
| `modules.init.yaml.instructions.md` references | File already deleted, but still referenced in prompts | Remove all references to this dead file |

### Totals

| Category | Count | Expected v2 Issues |
|----------|-------|-------------------|
| Instructions | 21 | ~10 files with `cores/` or v2 tooling refs |
| Agents | 8 | Format completeness audit |
| Prompts | 3 | ~1 file with dead `modules.init.yaml` ref |
| **Total** | **32 data files** | + 5 format/structural fixes = ~37 discrete edits |

---

## [Custom] 📋 Broken Sync Path Fix

**The critical fix that unblocks everything:**

`instruction_controller.py` line 47 currently reads:
```python
self.official_source_path = self.root_path / "cores" / "instruction_core" / "data"
```

This path (`cores/instruction_core/data`) doesn't exist. The module lives at `modules/dev/instruction_core/`. The sync method `_sync_data_to_target()` checks `if not source_path.exists(): ... return` and silently skips.

**Fix:**
```python
self.official_source_path = Path(__file__).resolve().parent / "data"
```

This derives the source path from the module's own location (`instruction_controller.py` is in `modules/dev/instruction_core/`), making it immune to future directory renames.

**Impact:** Once fixed, `adhd refresh --full` will actually sync the (v3-fixed) data files to `.github/`. This makes P0 the critical unblocking step for the entire pipeline.

---

## [Custom] 📋 Agent Format Spec Update

`agents_format.instructions.md` currently documents the agent YAML frontmatter but is missing fields that exist in actual v3 agent files:

### Current spec (incomplete):
```yaml
---
name: "AgentName"
description: "What it does"
tools: ['tool1', 'tool2']
---
```

### Correct v3 format (from actual agents):
```yaml
---
name: "AgentName"
description: "What it does"
argument-hint: "Hint for user"
tools: ['tool1', 'tool2', ...]
handoffs:
  - label: "[emoji] Label"
    agent: AgentName
    prompt: "Handoff prompt"
    send: false
---
```

**New fields to document:**
| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `argument-hint` | string | Optional | Hint shown to user in VS Code when selecting this agent |
| `handoffs` | list | Optional | Defines which agents this agent can hand off to |
| `handoffs[].label` | string | Required (if handoffs) | Display label for the handoff option |
| `handoffs[].agent` | string | Required (if handoffs) | Target agent name |
| `handoffs[].prompt` | string | Optional | Prompt to send with the handoff |
| `handoffs[].send` | boolean | Optional | Whether to auto-send or let user edit first |

---

## ✅ Acceptance Criteria

- [ ] `instruction_controller.py` `official_source_path` resolves to an existing directory (`modules/dev/instruction_core/data/`)
- [ ] `grep -r "cores/" modules/dev/instruction_core/data/` returns zero matches
- [ ] Zero `init.yaml` creation/usage instructions remain in data files
- [ ] Zero `pip install` references remain (replaced with `uv`)
- [ ] Zero `sys.path.insert` references remain (replaced with package imports)
- [ ] Zero references to `modules.init.yaml.instructions.md` remain
- [ ] `adhd_framework_context.instructions.md` folder taxonomy has no `cores/` entry
- [ ] `agents_format.instructions.md` documents `argument-hint`, `handoffs`, `send` fields
- [ ] All 8 agent files have valid YAML frontmatter
- [ ] All instruction files have valid `applyTo` frontmatter (or documented reason for omission)
- [ ] `adhd refresh --full` runs successfully and populates .github/ with current content
- [ ] Git tag created before modifications begin (`pre-instruction-pipeline-v0`)

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Actual v3 agent files in `data/agents/` | Internal | Done | Source of truth for format spec |
| `instruction_controller.py` source | Internal | Done | Line 47 is the broken path |
| `adhd refresh --full` command | Internal | Done | Exists, will work once path is fixed and `refresh.py` is renamed to `refresh_full.py` |

---

## 🚀 Phase 0 Tasks

| # | Task | Difficulty | Description |
|---|------|-----------|-------------|
| 1 | Fix `instruction_controller.py` broken path | `[KNOWN]` | `cores/instruction_core/data` → `Path(__file__).resolve().parent / "data"`. Unblocks sync. |
| 2 | Document v3 compliance reference | `[KNOWN]` | Canonical checklist: structural accuracy + content accuracy + format compliance |
| 3 | Batch fix all 37 files | `[KNOWN]` | Fix frontmatter `cores/` paths, body `cores/` refs, `init.yaml`→`pyproject.toml`, `pip`→`uv`, `sys.path.insert`→package imports, purge `modules.init.yaml.instructions.md` refs |
| 4 | Update agent format spec | `[KNOWN]` | Add `argument-hint`, `handoffs`, `send` to `agents_format.instructions.md` |
| 5 | Verification pass | `[KNOWN]` | Re-audit all files, run `adhd refresh --full`, verify .github/ reflects corrected content |

---

## ✅ Feature Validation Checklist

### Narrative
- [x] **The Story** clearly states user problem and value
- [x] **Intent** is unambiguous to a non-technical reader
- [x] **3-layer contamination model** frames the problem

### Technical
- [x] **Scope** is explicitly bounded (In/Out of Scope filled)
- [x] **Acceptance Criteria** are testable (not vague)
- [x] **Dependencies** are listed with status
- [x] **Audit matrix** covers all 37 files with specific v2 issues

### v3 Accuracy
- [x] Zero references to creating init.yaml
- [x] Path fix uses `Path(__file__)`, not another hardcoded path
- [x] All v2→v3 replacements are specified (init.yaml→pyproject.toml, pip→uv, etc.)

### Linkage
- [x] Feature linked from [00_index.md](./00_index.md) and [01_executive_summary.md](./01_executive_summary.md)

---

**Prev:** [Architecture](./02_architecture.md) | **Next:** [Feature: Skills Adoption](./04_feature_skills_adoption.md)

---

**← Back to:** [Index](./00_index.md)

