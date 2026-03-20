# Experiment Entry Template

<!-- Schema version tracks template evolution. Do not remove. -->

```
---
experiment_id: EXP___
schema_version: "1.0"
experiment_type: Observational | Interventional
status: DESIGNED | RUNNING | COMPLETE | ABANDONED
verdict: PENDING | CONFIRMED | REJECTED | PARTIALLY CONFIRMED | INCONCLUSIVE
minimum_confirmation_runs: 1
arm_mode: pre-committed | sequential-gated  # optional, for multi-arm experiments
estimated_runtime: "~3 min per arm"  # helps determine inline vs monitoring-plan execution
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## 1. Observation
<!-- Raw data only. What happened? Metrics, logs, errors. No interpretation. -->


## 2. Hypotheses
<!-- Rate each: [LIKELY], [POSSIBLE], [UNLIKELY]. Sort by testability. -->
<!-- For Interventional: one hypothesis per experiment. -->
<!-- For Observational: multiple hypotheses allowed. -->

- **H1** [LIKELY]: 
- **H2** [POSSIBLE]: 

## 3. Predictions
<!-- ⛔ MUST be filled BEFORE execution. -->

| # | If hypothesis is true... | Metric | Expected Value | Tolerance |
|---|--------------------------|--------|----------------|-----------|
| 1 |                          |        |                |           |

## 4. Design
<!-- Type: Observational or Interventional. -->
<!-- Interventional: state the ONE variable changed and its baseline value. -->

- **Type**: 
- **Variable** (if interventional): 
- **Baseline**: 

## 5. Instrumentation
<!-- What to measure, where to log, how to collect. -->


## 6. Execution Log
<!-- Timestamps, environment, anomalies. One entry per run. -->

| Run | Date | Duration | Notes |
|-----|------|----------|-------|
| 1   |      |          |       |

## 7. Analysis
<!-- Compare predictions to measurements. -->

| # | Predicted | Measured | Match? |
|---|-----------|----------|--------|
| 1 |           |          |        |

## 8. Verdict

**Verdict**: PENDING
<!-- One of: CONFIRMED | REJECTED | PARTIALLY CONFIRMED | INCONCLUSIVE -->
<!-- Justification (required): -->

## Unexpected Observations
<!-- Anything not predicted that was observed. Seeds future hypotheses. -->


## Execution Guardrails

- **Resource Budget**: N/A <!-- or: "2 GPU-hours max", "500 API calls" -->
- **Rollback Procedure**: N/A <!-- or: "Revert commit abc123", "Restore backup" -->
- **Early-Stop Clauses**: N/A <!-- or: "Terminate arm if dino_loss > 50 for 10 consecutive steps" -->

## Handoff Notes
<!-- For next agent: current status, what to do next, where data lives. -->

