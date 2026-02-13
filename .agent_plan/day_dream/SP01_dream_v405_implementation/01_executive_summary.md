# SP01 — Executive Summary

## 📖 The Story

### 😤 The Pain

```
┌──────────────────────────────────────────────────────────────┐
│  DREAM v4.05 spec is written and approved...                 │
│  but the ecosystem still runs on v4.01 conventions.          │
│                                                              │
│  Agent reads skill  ──►  Gets outdated magnitude scale       │
│  Agent opens template ──►  Missing frontmatter fields        │
│  Agent checks folder  ──►  `templates/` not `_templates/`    │
│  Agent writes plan   ──►  No SP/PP type distinction          │
│  Agent closes plan   ──►  No Module Index gate enforced      │
└──────────────────────────────────────────────────────────────┘
```

| Pain Point | Who Hurts | Severity |
|------------|-----------|----------|
| Stale magnitude scale in skills | All planning agents | HIGH |
| 27+ broken `templates/` path refs | HyperDream, HyperAgentSmith | HIGH |
| No `dream_mcp` enforcement tool | All agents (conventions drift) | MEDIUM |
| Missing PP template | Procedure Plan authors | MEDIUM |
| No Plan Type distinction | Planning agents | HIGH |

### ✨ The Vision

```
DREAM v4.05 Spec
      │
      ├──► Skills (dream-planning, day-dream, writing-templates)
      │       └── Fully aligned, 8-slot scale, SP/PP types, _templates/ paths
      │
      ├──► Templates (_templates/)
      │       └── Full frontmatter schema, PP summary template, 8-slot notation
      │
      ├──► Agents & Docs (compiled agents, flows, synced skills)
      │       └── Zero stale path references
      │
      └──► dream_mcp (modules/dev/dream_mcp/)
              └── Skeleton with P0 command stubs ready for follow-up plan
```

### 🎯 One-Liner

> Align the entire ADHD planning ecosystem — skills, templates, agents, and tooling — with DREAM v4.05 so that every agent reads current conventions, not stale ones.

### 📊 Impact

| Metric | Before (v4.01) | After (v4.05 aligned) |
|--------|-----------------|----------------------|
| Stale path references | 27+ across ecosystem | 0 |
| Magnitude scale | 4-level (ambiguous) | 8-slot with maximums |
| Plan type support | Single type | SP + PP with distinct templates |
| Closure gate enforcement | Manual, convention-only | Module Index + State Delta + `dream validate` |
| dream_mcp | Does not exist | Skeleton with P0 stubs |

---

## 🔧 The Spec

### TL;DR

Update 3 skills, 5+ templates, 27+ path references, and scaffold the `dream_mcp` module to bring the ADHD ecosystem into full alignment with DREAM v4.05. Four phases, ~4 slots, all `[KNOWN]` work.

### Goals

1. **Skills reflect v4.05** — 8-slot magnitude, full frontmatter, SP/PP types, `_templates/` paths
2. **Templates are current** — PP summary template exists, frontmatter schema complete
3. **Zero stale references** — All `templates/` → `_templates/` across agents, flows, synced copies
4. **dream_mcp skeleton exists** — Module scaffold ready for follow-up P0 implementation plan

### Non-Goals

1. **Implementing dream_mcp commands** — Only the skeleton; P0 commands are a separate SP
2. **Rewriting agent behavior** — Only fixing path references and convention alignment
3. **Changing DREAM v4.05 spec itself** — The spec is authoritative; we align TO it
4. **CI/pre-commit hooks** — Part of dream_mcp implementation, not this plan
5. **Retroactive plan migration** — Existing completed plans stay as-is

### 🔍 Prior Art & Existing Solutions

| Option | Verdict | Rationale |
|--------|---------|-----------|
| Manual grep + sed | BUILD (chosen) | Simple find-replace for path refs; known patterns |
| Automated migration script | SKIP | Overkill for one-time 27-ref update |
| Ignore drift, fix on encounter | SKIP | Convention drift compounds; 6-month half-life proven |

### P0 Features

| # | Feature | Phase | Difficulty |
|---|---------|-------|------------|
| 1 | Directory rename + template updates | p00 | `[KNOWN]` |
| 2 | Skill rewrites (3 skills) | p01 | `[KNOWN]` |
| 3 | Path reference fixes (27+ refs) | p02 | `[KNOWN]` |
| 4 | dream_mcp module skeleton | p03 | `[KNOWN]` |

🔒 FROZEN — Scope approved. No additional features without human override.
