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

**Causal isolation principle**:
The purpose of an interventional experiment is to attribute observed effects to specific causes. The simplest way to ensure this is changing one variable per arm from baseline. But the real test is: **"If a metric moves, can I determine which change caused it?"**

- **Simple case**: Each arm changes one variable from baseline. Attribution is direct.
- **Factorial designs**: Arms A (X only), B (Y only), C (X+Y) are valid when individual arms exist in the same experiment — arm C reveals interaction effects that are isolable by comparison against A and B.
- **Confounded designs**: An arm that changes multiple variables with no individual-variable arms to compare against defeats causal isolation. This is a genuine violation regardless of how it's framed.

**Baseline requirement**:
- State the baseline value explicitly in the experiment entry
- State the new value explicitly
- The relationship between baseline, individual arms, and any combination arms must be clear

**Examples**:
- Changing a cache TTL from 60s to 300s to test response time impact
- A/B: testing index scan vs sequential scan; C: testing both together (with A and B providing individual baselines)
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
