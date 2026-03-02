# Document Rules & Line Limits

| Document | Required When | Line Limit |
|----------|---------------|------------|
| `_overview.md` | Every plan directory | ≤100 lines |
| `01_executive_summary.md` | Blueprint, System Plan | ≤150 lines |
| `01_summary.md` | Blueprint, Procedure Plan | ≤200 lines |
| `02_architecture.md` | System Plan with ≥3 modules/cross-module/ext API | ≤200 lines |
| `80_implementation.md` | Blueprint tier | ≤200 lines per phase |
| `81_module_structure.md` | System Plan, ADHD projects | ≤150 lines |
| Feature (full) | ≥3 modules, external APIs, P0 | ≤300 lines |
| Feature (simple) | ≤2 modules, no ext APIs | ≤100 lines |
| Task file | Any leaf task | ≤100 lines |
| Asset file | Supporting artifact | ≤100 lines (excl. diagrams) |

## Children Table Schema

The Children table in `_overview.md` has exactly 4 columns:

| Column | Description |
|--------|-------------|
| Name | File or directory name |
| Type | `Plan` (directory with `_overview.md`) or `Task` (single `.md` file) |
| Status | Status marker (⏳ [TODO], 🔄 [WIP], ✅ [DONE], etc.) |
| Description | One-line summary |

⚠️ **Type column values: ONLY `Plan` or `Task` are valid.** Values like 'Doc', 'Feature', 'Module', etc. are INVALID per §1.2's two-primitive rule.

## Authoring Rules

| Rule | Detail |
|------|--------|
| **Mandatory Skeleton** | Sections are present; write "N/A — [reason]" for inapplicable. Do NOT mark optional |
| **Executive Summary** | TL;DR max 3 sentences. Prior Art required. Non-Goals min 3. Max 5 P0 features. Freeze with 🔒 FROZEN |
| **Acceptance Criteria** | Task files MUST include `## Acceptance Criteria` with checkbox lists |
| **Custom Sections** | Prefix: `## [Custom] 🎨 Title`. Max 5 per doc. Prohibited: P0 tasks, blocking deps, arch changes |
| **Deep Dive** | `## 🔬 Deep Dive` only for algorithms, API contracts, error handling. Delete for straightforward features |
| **Clean-Code-First** | Delete wrong code, refactor fully, one correct path. Never try/catch fallbacks |
