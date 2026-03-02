# Directory-Based Hierarchy

Hierarchy is expressed through the filesystem. No level numbers.

```
SP01_{plan_name}/
├── _overview.md              # REQUIRED — plan navigator with frontmatter
├── 01_executive_summary.md   # System Plan only
├── 02_architecture.md        # System Plan only
├── 0N_feat_{feature}.md      # feat_ prefix RECOMMENDED
├── 80_implementation.md
├── pNN_{phase}/              # Phase directories
│   ├── _overview.md
│   └── NN_{task}.md
├── modules/
│   └── {module_name}.md
└── assets/
```

## Rules
- **Directory = plan** — always has `_overview.md`
- **File = task** — leaf, directly executable
- Phase directories: `pNN_name/` — ALWAYS directories, even single-task phases
- Task numbering starts at `01_` (position `00_` is implicitly `_overview.md`)
- Nesting ≤3 levels recommended
