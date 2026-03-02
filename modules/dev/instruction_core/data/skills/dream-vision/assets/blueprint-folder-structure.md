# Blueprint Folder Structure

```
.agent_plan/day_dream/
├── _overview.md                    ← Root navigator
├── _tree.md                        ← Generated folder tree (NEVER hand-edit)
├── _state_deltas_archive.md        ← Overflow State Deltas (auto-generated)
│
├── SP{NN}_{plan_name}/               ← System Plan
│   ├── _overview.md                ← REQUIRED navigator with frontmatter
│   ├── 01_executive_summary.md
│   ├── 02_architecture.md
│   ├── 0N_feat_{feature}.md        ← feat_ prefix RECOMMENDED
│   ├── 80_implementation.md
│   ├── 81_module_structure.md
│   ├── pNN_{phase}/
│   │   ├── _overview.md
│   │   └── NN_{task}.md
│   ├── modules/
│   └── assets/
│
├── PP{NN}_{plan_name}/               ← Procedure Plan
│   ├── _overview.md
│   ├── 01_summary.md               ← Merged exec summary + architecture
│   ├── 0N_feat_{step_name}.md
│   ├── 80_implementation.md
│   └── pNN_{phase}/
│
├── _completed/                     ← Archive (YYYY-QN/ subdirs)
├── exploration/                    ← Research docs (max 3 active, 14-day expiry)
│   └── _archive/
# NOTE: Templates are now in .github/skills/dream-routing/assets/ (not in day_dream/)
```

### Phase Naming
- `pNN_name/` — zero-padded two digits, underscore separator
- Phases are ALWAYS directories (even single-task)
- Task numbering: `NN_{name}.md` starting at `01_`
- No `feat_` prefix on task files — that prefix is for plan-root feature files only
