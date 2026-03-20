# Multi-Arm Extension

For experiments with multiple arms beyond a simple baseline-vs-intervention pair.

---

## What Multi-Arm Means

A standard interventional experiment tests ONE new value against a baseline. Multi-arm experiments extend this in two ways:

### Parameter sweeps
Multiple arms test different values of the SAME variable against baseline. Causal isolation is straightforward — all arms differ from baseline in the same dimension.

### Factorial / interaction designs
Arms test individual variables AND their combinations. For example: A (X only), B (Y only), C (X+Y). Causal isolation is maintained because individual arms provide baselines for decomposing the combination arm's effects. The combination arm reveals interaction effects that neither individual arm can.

**The test remains**: "If a metric moves in any arm, can I determine what caused it?"

---

## When to Use

- Parameter sweeps (testing learning rates 0.001, 0.01, 0.1)
- A/B/C comparisons (three caching strategies)
- Threshold tuning (timeout values of 5s, 10s, 30s)
- Configuration selection (pool sizes of 4, 8, 16, 32)
- Factorial ablations (testing components individually and in combination)
- Interaction detection (does X+Y behave differently than X and Y predict separately?)

---

## Arm Naming Convention

```
[experiment_id]_arm_[letter]

Example:
EXP007_arm_A  (baseline: pool_size=4)
EXP007_arm_B  (pool_size=8)
EXP007_arm_C  (pool_size=16)
EXP007_arm_D  (pool_size=32)
```

Arm A is always the baseline (current/default value).

---

## Shared Baseline Requirement

All arms MUST share:
- Same instrumentation and measurement method
- Same environment and configuration (except the variable(s) under test)
- Same execution procedure
- Same prediction table structure

For factorial designs, the baseline is the control arm (no changes). Each subsequent arm must be clearly traceable back to baseline with an explicit description of what changed and why.

---

## Arm Execution Modes

The experiment spec declares which mode to use. If not specified, default to `pre-committed`.

### `pre-committed`

All arms are declared upfront and run unconditionally in sequence. No inter-arm evaluation by the orchestrator.

**Use for**: factorial ablations, interaction tests, experiments where each arm answers a distinct sub-question, experiments where the designer explicitly pre-registered all arms as READY.

HyperArch runs all arms, collects all data, analysis happens post-hoc.

Optional `early_stop_if` clause (declared in experiment spec) lets HyperArch terminate an arm early if a pre-registered condition is met — recorded as "terminated: [reason]", not as abort.

### `sequential-gated`

Arms run one at a time with evaluation between them:

```
Run Arm A (baseline) → Evaluate
  │
  ├── Results valid? → Run Arm B → Evaluate
  │                       │
  │                       ├── Clear winner already? → STOP (record verdict)
  │                       │
  │                       └── Unclear → Run Arm C → Evaluate → ...
  │
  └── Baseline broken? → FIX baseline first, do not proceed
```

**Use for**: parameter sweeps, search-mode experiments, experiments where later arms depend on earlier results.

**Stop early if**:
- One arm clearly dominates (outside tolerance of all others)
- Baseline is broken (fix that first)
- Resource budget exhausted

**Continue if**:
- Results are within tolerance — need more arms to differentiate
- Data quality is suspect — verify instrumentation before adding arms

---

## Seed Recording (Stochastic Experiments)

For experiments with random components, record seeds per arm:

| Arm | Variable Value | Seed | Run 1 Result | Run 2 Result |
|-----|---------------|------|--------------|--------------|
| A   | pool_size=4   | 42   |              |              |
| B   | pool_size=8   | 42   |              |              |
| C   | pool_size=16  | 42   |              |              |

Use the SAME seed across arms for the SAME run number. This isolates the variable from random variation.

---

## Example Structure

```markdown
## Multi-Arm Experiment: Connection Pool Sizing

**Variable**: database connection pool size
**Baseline (Arm A)**: pool_size=4
**arm_mode**: pre-committed

| Arm | pool_size | Avg Response (ms) | P99 (ms) | Error Rate |
|-----|-----------|-------------------|----------|------------|
| A   | 4         |                   |          |            |
| B   | 8         |                   |          |            |
| C   | 16        |                   |          |            |
| D   | 32        |                   |          |            |
```

---

## Verdict for Multi-Arm

The verdict applies to the overall experiment question, not individual arms:
- **CONFIRMED**: One arm clearly outperforms baseline beyond tolerance
- **REJECTED**: No arm meaningfully differs from baseline
- **PARTIALLY CONFIRMED**: Some metrics improve, others degrade
- **INCONCLUSIVE**: Results too noisy or insufficient runs to determine
