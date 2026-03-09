# Artifact Directory Structure

```
.agent_plan/red_team/<module_name>/
├── attacks/     # Generated attack scripts (persist for re-runs)
├── findings/    # Structured JSON per session (YYYY-MM-DD_findings.json)
└── evidence/    # Crash logs, stderr captures (gitignored)
```

**Git Tracking**: Track `attacks/` and `findings/`. Ignore `evidence/`.

## Findings Output

Write findings to `.agent_plan/red_team/<module>/findings/YYYY-MM-DD_findings.json`.
Always update `latest_findings.json` as a reference point.

## Severity Levels

| Severity | Criteria |
|----------|----------|
| **critical** | Data loss, security vulnerability, silent corruption |
| **high** | Crash, unhandled exception, resource leak |
| **medium** | Wrong result, degraded performance, poor error message |
| **low** | Cosmetic, non-standard behavior, minor inconsistency |
