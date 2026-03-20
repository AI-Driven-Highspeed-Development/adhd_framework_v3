# Experiment Types

Two types. Every experiment MUST be classified as one before execution.

---

## Observational

**Definition**: Measures existing behavior without changing it. Probes, logging, profiling — read-only instrumentation.

**When to use**:
- Gathering initial data about a symptom
- Testing multiple hypotheses in a single run
- Measuring baselines before an intervention
- Situations where changing behavior is risky or impossible

**Batching rules**:
- Multiple hypotheses CAN be tested in one run
- No variables changed → no confounding risk
- Each hypothesis still needs its own prediction row

**Examples**:
- Adding request timing logs to diagnose slow API responses
- Profiling memory usage across modules to find a leak
- Querying database execution plans without changing indexes
- Monitoring error rates across service endpoints

---

## Interventional

**Definition**: Changes runtime behavior to test a causal claim. Modifies code, configuration, environment, or data.

**One-variable rule** (MANDATORY):
- Exactly ONE variable differs from baseline
- Everything else stays identical
- If you change 3 things and the metric moves, you don't know which mattered

**Baseline requirement**:
- State the baseline value explicitly in the experiment entry
- State the new value explicitly
- The diff between baseline and experiment must be exactly one variable

**Examples**:
- Changing a cache TTL from 60s to 300s to test response time impact
- Switching a database query from sequential scan to index scan
- Increasing worker thread count from 4 to 8
- Replacing a sorting algorithm to compare throughput

---

## Quick Decision

```
Does this experiment change any runtime behavior?
  │
  ├── NO  → Observational
  │         (multiple hypotheses OK, batch measurements)
  │
  └── YES → Interventional
              (ONE variable rule, state baseline explicitly)
```

---

## Hybrid Warning

If an observational experiment reveals findings that suggest an intervention:
1. Complete the observational experiment with its own verdict
2. Create a NEW experiment entry for the intervention
3. Do NOT retrofit an observational experiment into an interventional one mid-run

The two experiments can reference each other but remain separate entries with separate verdicts.
