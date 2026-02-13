---
task: p02_01
title: Update Flow Sources & Recompile Agents
status: DONE
difficulty: "[KNOWN]"
---

# Update Flow Sources & Recompile Agents

## Scope

Update `.flow` source files that reference `templates/` paths, then recompile to regenerate the compiled `.agent.md` files. This is the correct update order — flow sources are the source of truth, compiled agents are derived.

## Specific Changes

### Flow Source Files

| # | File | Refs | Change |
|---|------|------|--------|
| 1 | `modules/dev/instruction_core/data/flows/agents/hyper_agent_smith.flow` | 2 | `templates/` → `_templates/` (lines ~87, ~158) |
| 2 | `modules/dev/instruction_core/data/flows/agents/hyper_day_dreamer.flow` | 2 | `templates/` → `_templates/` (lines ~85, ~121) |

### Recompilation

| # | Action | Command |
|---|--------|---------|
| 3 | Recompile all flow files | `adhd compile` or `adhd refresh --full` |
| 4 | Verify compiled agents reflect updated paths | Check `hyper_agent_smith.adhd.agent.md` and `hyper_day_dreamer.adhd.agent.md` |

### Expected Compiled Agent Changes (auto-generated from flows)

| File | Expected Path Updates |
|------|----------------------|
| `instruction_core/data/compiled/agents/hyper_agent_smith.adhd.agent.md` | Lines ~50 and ~105 |
| `instruction_core/data/compiled/agents/hyper_day_dreamer.adhd.agent.md` | Lines ~50 and ~76 |

## How to Verify (Manual)

1. `grep "day_dream/templates/" modules/dev/instruction_core/data/flows/agents/*.flow` — should return 0
2. Run `adhd compile` — should succeed without errors
3. `grep "day_dream/templates/" modules/dev/instruction_core/data/compiled/agents/*.md` — should return 0

## Acceptance Criteria

- [x] Flow source files updated (zero `templates/` refs)
- [x] `adhd compile` succeeds
- [x] Compiled agent files reflect `_templates/` paths
