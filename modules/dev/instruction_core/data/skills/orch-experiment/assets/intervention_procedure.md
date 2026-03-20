# Intervention Procedure

Domain-agnostic procedure for interventional experiments — when experiments require behavior changes beyond observation.

## Tag: `# INTERVENTION`

Sibling tag to `# PROBE`, NOT a subtype.

**Why separate tags**: An intervention mutates behavior; a probe only observes. They have different cleanup procedures, different risk profiles, and different lifecycle rules. `grep '# PROBE'` finds probes. `grep '# INTERVENTION'` finds interventions. No regex needed.

## Tiered Strategy

| Duration | Scope | Strategy | Cleanup Gate |
|----------|-------|----------|-------------|
| Minutes–hours | Single file | `# INTERVENTION` tags + `git stash`/`git checkout` | Remove tags or pop stash |
| Hours–days | Multiple files | `experiment/<experiment_id>` branch | Merge (if CONFIRMED) or delete branch |
| Days–weeks | Cross-cutting | YAML config with `experiment_id` + `expires` field | Expired configs fail loudly at startup |

## Tag-Based Interventions (Short-Lived)

- Every modified line ends with `# INTERVENTION`
- Cleanup: manual/IDE-assisted ONLY, never automated `sed`
- Why no `sed`: intervention lines interleave with non-intervention logic (if/else blocks straddle both). Automated removal produces orphaned code.

## Branch-Based Interventions (Medium-Lived)

- Branch naming: `experiment/<experiment_id>` (e.g., `experiment/EXP_042_adaptive_timeout`)
- One-variable rule maps perfectly: one branch, one variable changed, clean diff
- Rollback: `git switch main && git branch -d experiment/EXP_042_adaptive_timeout`
- Experiment entry Safety section should reference the branch

## Config-Based Interventions (Long-Lived)

YAML config file (e.g., `experiment.yaml` or within existing config):

```yaml
experiments:
  EXP_042_adaptive_timeout:
    experiment_id: EXP_042
    expires: 2026-04-01
    params:
      timeout_ms: 5000
      retry_count: 3
```

- `expires` field is MANDATORY — config without expiry is rejected by validation
- Expired configs should fail loudly at startup (not silently ignored)
- Prevents config-flag half-life decay

## Experiment Graduation (CONFIRMED → Permanent)

| Strategy | Promotion Action |
|----------|-----------------|
| Tag-based | Remove `# INTERVENTION` tags, code becomes permanent |
| Branch-based | Merge branch into main via normal merge process |
| Config-based | Remove `experiment_id` and `expires` fields, promote parameters to main config schema |

This is a deliberate promotion step, documented in the experiment registry.

## Step 8 Cleanup Mandate (Verdict-Driven)

| Verdict | Action |
|---------|--------|
| CONFIRMED | Promote intervention to permanent (remove tags/merge branch/promote config) |
| REJECTED | Revert intervention completely (remove tags/delete branch/remove config) |
| PARTIALLY CONFIRMED | Promote confirmed parts, revert rejected parts, document reasoning |
| INCONCLUSIVE | Carry forward with explicit justification in registry, re-evaluate at next experiment |

## Hybrid Case (Observation + Intervention)

Both tags compose. The experiment branch/config has behavior changes (`# INTERVENTION`), plus `# PROBE` tagged instrumentation.

**Cleanup order**: Remove probes first (automated safe), then handle intervention (manual/merge/promote).

## Anti-Patterns

| Bad | Good |
|-----|------|
| Labeling behavior changes as `# PROBE` | Use `# INTERVENTION` for anything that changes output |
| `sed`-based removal of `# INTERVENTION` lines | Manual/IDE-assisted removal only |
| Config experiment without `expires` | Always set expiry date |
| Merging experiment branch without CONFIRMED verdict | Only merge on CONFIRMED |
| Leaving `# INTERVENTION` tags after experiment concludes | Step 8 mandates cleanup/promote/revert |
