# SP01 — Module Structure

## Module Classification

SP01 touches two ADHD modules. Classification per the reusable/project-specific distinction:

| Module | Layer | Classification | Rationale |
|--------|-------|---------------|-----------|
| `instruction_core` | `dev` | Reusable (existing) | Core framework module — syncs skills, compiles agents. SP01 modifies data files within it, not the module code itself |
| `dream_mcp` | `dev` | Reusable (new) | Framework-level MCP server for DREAM convention enforcement. Usable in any ADHD project |

## Module Details

### instruction_core (Modified)

| Attribute | Detail |
|-----------|--------|
| **Location** | `modules/dev/instruction_core/` |
| **What SP01 Changes** | Path references in `data/flows/agents/*.flow`, recompiled `data/compiled/agents/*.md`, re-synced `data/skills/**/SKILL.md` |
| **What SP01 Does NOT Change** | Module code (`instruction_controller.py`, `refresh_full.py`, `__init__.py`) |
| **Risk** | Low — data-only changes, no API surface modification |
| **Spec File** | `modules/instruction_core.md` |

### dream_mcp (New — Skeleton Only)

| Attribute | Detail |
|-----------|--------|
| **Location** | `modules/dev/dream_mcp/` (does not exist yet) |
| **What SP01 Creates** | Module scaffold: `__init__.py`, `pyproject.toml`, `README.md`, `dream_mcp.py` (stubs), `refresh.py` |
| **What SP01 Does NOT Create** | Working command implementations — separate follow-up System Plan |
| **Risk** | Low — scaffold only, no behavioral surface |
| **Spec File** | `modules/dream_mcp.md` |

## Non-Module Artifacts

The following artifacts are modified by SP01 but are NOT ADHD modules (not under `modules/{layer}/{name}/`). They are tracked in phase task files, not in the Module Index:

| Artifact | Location | Modified By Phase |
|----------|----------|-------------------|
| dream-planning skill | `.github/skills/dream-planning/SKILL.md` | p01 |
| day-dream skill | `.github/skills/day-dream/SKILL.md` | p01 |
| writing-templates skill | `.github/skills/writing-templates/SKILL.md` | p01 |
| `_templates/` directory | `.agent_plan/day_dream/_templates/` | p00 |
| Compiled agent files | `instruction_core/data/compiled/agents/*.md` | p02 (derived) |
| Synced skill copies | `instruction_core/data/skills/**/SKILL.md` | p02 (derived) |

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Skills tracked in phase tasks, not Module Index | Skills are `.github/skills/` artifacts, not `modules/` entries per DREAM v4.05 §3.1 |
| `instruction_core` in Module Index despite data-only changes | Module spec must track ALL plan modifications per §3.4 `modified_by_plans` enforcement |
| `dream_mcp` skeleton vs full implementation | Separation of concerns — scaffold is `[KNOWN]`, implementation complexity warrants its own System Plan |
