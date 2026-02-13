---
name: context_injection_restructure
type: procedure
magnitude: Standard
status: WIP
origin: discussion/context_injection_files_taxonomy
last_updated: 2026-02-13
depends_on: []
blocks: []
knowledge_gaps:
  - "Full applyTo→agent mapping not yet audited — P0 resolves this"
---

# PP02 — Context Injection Files Restructuring

## Purpose

Restructure ADHD Framework context injection files (`.instructions.md`, `.agent.md`, `SKILL.md`) using a 3-axis taxonomy: **Agents = perspective** (personality only), **Instructions = universal truth** (framework-wide specs), **Skills = procedure** (SOPs). Migrate single-agent instruction files to skills, document the taxonomy, and clean up deprecated files — without breaking any agent's context coverage.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_summary.md | Task | ✅ [DONE] | Merged summary: pain, vision, taxonomy spec, approach |
| 80_implementation.md | Task | 🔄 [WIP] | Tracking doc in active use: P0/P1 complete, P2/P3 not started |
| p00_usage_audit/ | Plan | ✅ [DONE] | Audit completed: instruction inventory, consumers, and STAY/MIGRATE classification |
| P1 taxonomy documentation | Task | ✅ [DONE] | Implemented via `context_injection_taxonomy.instructions.md` and Phase 1 records in `80_implementation.md` (no separate child folder) |
| p02_migration_execution/ | Plan | ⏳ [TODO] | Create skills, deprecate old instructions, update flows |
| p03_deprecation_cleanup/ | Plan | ⏳ [TODO] | Remove deprecated files, verify compilation, coverage |

## Integration Map

```
p00_usage_audit/ ──► classification matrix
                          │
P1 taxonomy documentation (tracked by existing artifacts) ──► taxonomy instruction file
                          │
          ┌───────────────┘
          ▼
p02_migration_execution/ ──► new skills + deprecated instructions
                          │
          ┌───────────────┘
          ▼
p03_deprecation_cleanup/ ──► clean codebase, verified compilation
```

## Reading Order

1. **01_summary.md** — Start here. Understand the pain, taxonomy, and approach.
2. **80_implementation.md** — Phased roadmap with tasks and verification.
3. **p00_usage_audit/** — First execution phase (strict prerequisite for all others).
4. **P1 taxonomy documentation** — Implemented in `modules/dev/instruction_core/data/instructions/framework/context_injection_taxonomy.instructions.md`; execution evidence tracked in `80_implementation.md`.
5. **p02_migration_execution/** — Depends on p00 classification + p01 taxonomy.
6. **p03_deprecation_cleanup/** — Depends on p02 completion.
