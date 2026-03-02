# Error Codes

| Code | Phase | Severity | Description |
|------|-------|----------|-------------|
| `NO_GIT` | Scout | critical | Target not a git repo |
| `ADHD_TO_ADHD` | Readiness | critical | Cannot export to ADHD project |
| `DIRTY_WORKING_DIR` | Readiness | blocker | Uncommitted changes |
| `SCOPE_EXCEEDED` | Readiness | critical | Too many artifacts |
| `COLLISION_DETECTED` | Feasibility | critical | File would overwrite |
| `HEADER_MISSING` | Verify | error | Exported file lacks header |
| `TARGET_POLLUTED` | Verify | critical | `.agent_plan/` found in target |
