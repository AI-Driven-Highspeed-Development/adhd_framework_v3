# SP01 — Implementation Roadmap

## 📖 The Story

Implementing DREAM v4.05 is too large for a single pass. Without phased delivery, agents face context overload, risk regressions, and lose verification checkpoints. By decomposing into 8 phases — foundation, skills, agents, skeleton, parsing, status/validate, workflows, intelligence — each phase delivers testable value before the next begins. This roadmap ensures incremental progress with natural verification gates at every step.

## Phase Plan

| Phase | Name | Slots | Status | Depends On | Description |
|-------|------|-------|--------|------------|-------------|
| p00 | Foundation | 1 | ✅ [DONE] | — | Directory rename, PP template, template schema updates |
| p01 | Skill Updates | 1.5 | ✅ [DONE] | p00 | Rewrite 3 skill files to v4.05 conventions |
| p02 | Agent & Instruction Updates | 1 | ✅ [DONE] | p00 | Fix 27+ stale `templates/` path references |
| p03 | dream_mcp Skeleton | 0.5 | ⏳ [TODO] | — | Module scaffold + command specs (no implementation) |
| p04 | P0: Parsing & Simple Commands | 2 | ⏳ [TODO] | p03 | Shared infra + `dream tree` + `dream stale` |
| p05 | P0: Status & Validate | 3 | ⏳ [TODO] | p04 | `dream status` dashboard + `dream validate` engine |
| p06 | P1: Advanced Workflows | 3 | ⏳ [TODO] | p05 | `dream impact`, `history`, `emergency`, `archive` |
| p07 | P2: Intelligence Layer | 2 | ⏳ [TODO] | p06 | Hypothetical impact + proactive gap detection |

**Total:** 14 slots — p00–p03: 4 slots `[KNOWN]`, p04–p05: 5 slots `[KNOWN]`, p06: 3 slots `[KNOWN]`/`[EXPERIMENTAL]`, p07: 2 slots `[EXPERIMENTAL]`/`[RESEARCH]`.

## Dependency Graph

```
p00_foundation ──► p01_skill_updates
               └─► p02_agent_instruction_updates

p03_dream_mcp_skeleton ─► p04_parsing ─► p05_status_validate ─► p06_workflows ─► p07_intelligence
```

p01 and p02 execute in parallel after p00 completes. p03 is independent of p00–p02. p04–p07 form a sequential chain after p03.

---

## Phase Details

### p00 — Foundation (1 slot) `[KNOWN]` ✅ [DONE]

**Deliverables:**
1. `_templates/` directory exists (renamed from `templates/`)
2. `_templates/blueprint/01_summary.template.md` created (PP merged summary)
3. Template frontmatter updated to v4.05 schema (overview, module_spec, 80_implementation, simple)

**Tasks:** 3 — rename directory, create PP template, update schemas.

### How to Verify (Manual)

1. `ls .agent_plan/day_dream/_templates/` → lists `simple.template.md`, `blueprint/`, `assets/`, `examples/`
2. `ls .agent_plan/day_dream/templates/` → "No such file or directory"
3. Open `_templates/blueprint/01_summary.template.md` → PP-specific scaffold exists, ≤200 lines

---

### p01 — Skill Updates (1.5 slots) `[KNOWN]` ✅ [DONE]

**Depends on:** p00 (template paths must exist before skills reference them).

**Deliverables:**
1. `dream-planning` SKILL.md — 8-slot magnitude, full frontmatter, no `plan.yaml`, Plan Types
2. `day-dream` SKILL.md — `_templates/` paths, dependency/invalidation/knowledge-gap rules, Module Index gate
3. `writing-templates` SKILL.md — all `templates/` → `_templates/` path updates

**Tasks:** 3 — one per skill, all parallelizable after p00.

### How to Verify (Manual)

1. `grep -c "plan.yaml" .github/skills/dream-planning/SKILL.md` → 0
2. `grep -c "day_dream/templates/" .github/skills/day-dream/SKILL.md` → 0
3. `grep -c "day_dream/_templates/" .github/skills/writing-templates/SKILL.md` → ≥4

---

### p02 — Agent & Instruction Updates (1 slot) `[KNOWN]` ✅ [DONE]

**Depends on:** p00 (rename must complete before references are valid).

**Deliverables:**
1. `.flow` source files updated (`templates/` → `_templates/`)
2. Compiled `.agent.md` files regenerated via `adhd compile`
3. Synced skill copies current (via refresh or manual update)

**Tasks:** 2 — update flows + recompile, then sweep remaining refs.

### How to Verify (Manual)

1. `grep -r "day_dream/templates/" . --include="*.md" --include="*.flow" | grep -v _archive | grep -v DREAM_v4` → 0 matches
2. `adhd compile` → succeeds without errors
3. Synced skills in `instruction_core/data/skills/` match `.github/skills/` versions

---

### p03 — dream_mcp Skeleton (0.5 slots) `[KNOWN]` ⏳ [TODO]

**Independent** — no dependencies on other phases.

**Deliverables:**
1. `modules/dev/dream_mcp/` exists with standard ADHD MCP module structure
2. `dream_mcp.py` has P0 tool signatures (`status`, `tree`, `stale`, `validate`) as `NotImplementedError` stubs
3. `README.md` documents full P0/P1/P2 command roadmap

**Tasks:** 1 — scaffold module via ADHD MCP tools, populate specs.

### How to Verify (Manual)

1. `ls modules/dev/dream_mcp/` → `__init__.py`, `dream_mcp.py`, `refresh.py`, `pyproject.toml`, `README.md`
2. `python -c "import modules.dev.dream_mcp"` → no import error
3. Open `README.md` → P0/P1/P2 command roadmap documented

---

### p04 — P0: Parsing & Simple Commands (2 slots) `[KNOWN]` ⏳ [TODO]

**Depends on:** p03 (module skeleton must exist).

**Deliverables:**
1. Shared parsing library: YAML frontmatter parser, plan tree scanner, output formatter
2. Working `dream tree` command — generates annotated `_tree.md`
3. Working `dream stale` command — flags stale module specs

**Tasks:** 3 — shared infra (prerequisite), then tree + stale (parallel-safe).

### How to Verify (Manual)

1. Call `dream_tree()` → `_tree.md` generated with status annotations and timestamp
2. Call `dream_stale(weeks=0)` → returns all modules as stale (threshold=0 catches everything)
3. Call `dream_stale(weeks=52)` → returns empty list (nothing stale within a year)

---

### p05 — P0: Status & Validate (3 slots) `[KNOWN]` ⏳ [TODO]

**Depends on:** p04 (parsing infrastructure must exist).

**Deliverables:**
1. Working `dream status` command — sprint dashboard with emergency/active/blocked
2. Working `dream validate` command — comprehensive gate validation (core + DAG)

**Tasks:** 3 — status (independent), validate core, validate DAG (sequential).

### How to Verify (Manual)

1. Call `dream_status()` → shows current plans categorized by status with summary counts
2. Call `dream_validate()` → returns validation report with ERROR/WARNING categories
3. Introduce a cycle in `depends_on` → `dream_validate()` reports ERROR for cycle

---

### p06 — P1: Advanced Workflows (3 slots) `[KNOWN]`/`[EXPERIMENTAL]` ⏳ [TODO]

**Depends on:** p05 (DAG infrastructure from validate needed for impact).

**Deliverables:**
1. Working `dream impact` command — DAG walk with transitive deps
2. Working `dream history` command — module change history
3. Working `dream emergency` + `dream archive` commands — mutating workflows

**Tasks:** 3 — impact (read-only), history (read-only), emergency+archive (mutating, grouped).

### How to Verify (Manual)

1. Call `dream_impact("SP01")` → shows direct and transitive dependents
2. Call `dream_history("dream_mcp")` → shows chronological change entries
3. Call `dream_archive("SP01")` on a DONE plan → plan moved to `_completed/2026-Q1/`

---

### p07 — P2: Intelligence Layer (2 slots) `[EXPERIMENTAL]`/`[RESEARCH]` ⏳ [TODO]

**Depends on:** p06 (extends impact command, needs mature infrastructure).

**Deliverables:**
1. `dream impact --hypothetical` — proposed change analysis without existing plan
2. `dream gaps --proactive` — bus-factor detection via `sole_expert:` field

**Tasks:** 2 — both independent, both design explorations.

### How to Verify (Manual)

1. Call `dream_impact(hypothetical="add caching to billing")` → returns analysis labeled as hypothetical
2. Call `dream_gaps(proactive=True)` → returns bus-factor risks (or empty if no `sole_expert:` fields)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `adhd compile` fails after flow edits | Low | Medium | Test compile after each flow edit, not batch |
| Synced skills don't auto-refresh | Medium | Low | Manual update as fallback in p02 |
| Template schema changes break existing plans | Low | Low | Templates are scaffolds; existing plans keep their content |

## Completion Criteria

All seven phases ✅ DONE (p00–p02 complete, p03–p07 pending). Zero stale `templates/` references outside `_archive/`. `dream_mcp` fully functional through P0 and P1. P2 intelligence layer validated. State Delta appended to root `_overview.md`.
