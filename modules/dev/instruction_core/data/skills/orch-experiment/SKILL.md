---
name: orch-experiment
description: "Orchestrator experiment preset — coordinating scientific experiment workflows across specialist agents. Manages structured hypothesis testing: OBSERVE → HYPOTHESIZE → PREDICT → DESIGN → INSTRUMENT → EXECUTE → ANALYZE → RECORD. Guides causal isolation reasoning, predictions-before-execution, and four post-experiment verdicts (CONFIRMED/REJECTED/PARTIALLY CONFIRMED/INCONCLUSIVE). Use this skill when orchestrating experiments, debugging via scientific method, or running structured hypothesis-driven investigations."
---

# HyperOrch Experiment Preset

## Reasoning Over Compliance

This skill guides scientific reasoning — it is not a compliance checklist. Every rule here exists for a specific reason. When reviewing or executing experiments:

1. **Understand the purpose** of each rule before applying it.
2. **Evaluate whether the purpose is served**, not just whether the letter is followed.
3. **Explain your reasoning** when a rule's purpose is met through non-obvious means.
4. **Flag genuine violations** — cases where the purpose is defeated, even if the letter is technically followed.

An agent that mechanically applies rules without reasoning is no better than a linter. An agent that reasons about experimental design and catches real methodological flaws is invaluable.

## Goals
- Orchestrate structured hypothesis-driven experiment workflows
- Ensure scientific rigor through reasoned application of experimental principles
- Coordinate specialist agents through the 8-step experiment loop
- Maintain experiment records for cross-session continuity

## When This Applies
Trigger patterns: "experiment", "hypothesis", "debug scientifically", "root cause", "investigate", "why does", "measure", "bisect", "A/B test", "reproduce"

## Experiment Protocol

### Phase Structure
```
OBSERVE → HYPOTHESIZE → PREDICT → DESIGN → INSTRUMENT → EXECUTE → ANALYZE → RECORD
   ↓          ↓            ↓         ↓          ↓           ↓          ↓         ↓
 Symptom   Falsifiable   Metric   Classify   Add Probes   Run It    Verdict   Update
  Data      Claims      Targets   Obs/Int    & Logging              & Learn   Registry
```

### Orchestration Flow
```
DESIGN-REVIEW (HyperSan, once) → EXECUTE (HyperArch, autonomous) → ANALYZE (HyperSan, post-hoc)
```

- **DESIGN-REVIEW**: HyperSan validates the experiment design — reasoning about whether predictions are meaningful, causal isolation is achievable, and guardrails are proportionate to risk.
- **EXECUTE**: HyperArch receives full experiment context and runs all arms end-to-end. Collects all probe data, compiles measurement table, returns results.
- **ANALYZE**: HyperSan compares predictions to measurements, proposes verdict. HyperOrch delegates recording/cleanup to HyperArch if needed.

Experiment authoring (Steps 1–5) happens BEFORE orchestration begins — the experiment entry must exist with Steps 1–5 filled before HyperOrch starts.

## The 8-Step Loop

### Step 1: OBSERVE
Describe exact symptom with measurable data. No interpretation, no guessing.
- What happened? When? How often?
- Attach metrics, logs, error messages — raw data only.

### Step 2: HYPOTHESIZE
List ALL plausible explanations as falsifiable claims.
- Rate each: `[LIKELY]`, `[POSSIBLE]`, `[UNLIKELY]` — prior belief, never modified retroactively.
- Sort by testability (easiest to test first), not likelihood.

### Step 3: PREDICT ⛔ ABSOLUTE GATE
State specific predictions BEFORE execution. Use the 5-column prediction table:

| # | If hypothesis is true... | Metric | Expected Value | Tolerance |
|---|--------------------------|--------|----------------|-----------|

**Why this is absolute**: Post-hoc rationalization is cognitively invisible — humans and agents naturally construct explanations that fit observed data. Without pre-registered predictions, you cannot distinguish genuine understanding from pattern-matching on noise. This gate has no reasoning exceptions because the failure mode is undetectable from inside.

### Step 4: DESIGN
Classify experiment type and create minimal design:
→ See [experiment_types.md](assets/experiment_types.md) for classification rules

Set `minimum_confirmation_runs`:

| Category | Runs | Examples |
|----------|------|---------|
| Stochastic | 2+ | Perf benchmarks, load tests, flaky repros |
| Deterministic | 1 | Bug reproduction, logic errors |
| Unreproducible | 0 (observational only) | Production incidents, one-time failures |

### Step 5: INSTRUMENT
Add measurement or intervention code, tagged for clean removal.
- **Observational**: add `# PROBE` tagged instrumentation
  → See [probing_guideline.md](assets/probing_guideline.md) for principles, tag convention, and cleanup
- **Interventional**: add `# INTERVENTION` tagged code changes or use branch/config strategy
  → See [intervention_procedure.md](assets/intervention_procedure.md) for tiered strategy and cleanup gates

### Step 6: EXECUTE
Run the experiment. Collect data. Log everything.
- Record execution environment, timestamps, any anomalies.

### Step 7: ANALYZE
Compare predictions to measurements. Force a verdict into one of four categories:

`CONFIRMED` | `REJECTED` | `PARTIALLY CONFIRMED` | `INCONCLUSIVE`

**Why only four**: Soft verdicts like "LIKELY CONFIRMED" let agents avoid committing to a conclusion. If the evidence clearly supports the hypothesis, say CONFIRMED. If not, say what it actually is. Suggestive-but-not-conclusive evidence is INCONCLUSIVE with a recommendation narrative — that's honest, and it drives the next experiment.

`PARTIALLY CONFIRMED`: Some predictions match, others don't, but the evidence itself is clear (not noisy — the predictions were partially right).

### Step 8: RECORD
Update all records and clean up experiment artifacts:
- Experiment entry with verdict and analysis
- Registry/index with summary
- Handoff notes if context boundary approaching
- **Cleanup gate** (verdict-driven):
  - CONFIRMED → promote instrumentation/intervention to permanent code
  - REJECTED → revert all `# PROBE` and `# INTERVENTION` changes
  - INCONCLUSIVE → carry forward with justification in registry
- Reference exact probe output file path in experiment entry

## Scientific Guardrails

These are the principles that make experiments trustworthy. Each carries its rationale so you can reason about intent.

### Predictions Before Execution ⛔ ABSOLUTE
Predictions MUST be written before Step 6.

**Why absolute**: Post-hoc rationalization is cognitively invisible. This is the one rule where "the purpose is obviously served" reasoning fails, because you cannot detect the bias from inside. Always enforced.

### Causal Isolation Principle
**Purpose**: When an experiment changes something and observes an effect, you need to be able to attribute the effect to a specific cause.

**The test**: "If a metric moves, can I determine which change caused it?"

**Typical application**: Each interventional arm changes one variable from baseline — this is the simplest way to ensure attribution.

**Reasoning beyond the simple case**: The principle is about *attributability*, not about counting variables. Designs that test multiple variables CAN satisfy causal isolation if the design allows decomposition:
- **Factorial designs**: If arms A (X only), B (Y only), and C (X+Y) all exist, arm C's interaction effect is isolable by comparing C against A and B individually. The individual arms provide the causal baseline.
- **Confounded designs**: If ONLY arm C (X+Y) exists with no individual arms, a metric change cannot be attributed. This violates the principle regardless of how many variables were changed.

**When reviewing**: Ask "can the experimenter determine what caused each observed effect?" — not "did each arm change exactly one variable?"

### Confirmation Sufficiency
**Purpose**: A single stochastic run can be misleading due to random variation.

**The test**: "Is the observed result distinguishable from noise?"

Deterministic experiments (same seed, same hardware = same result) need one run. Stochastic experiments need enough runs to establish a pattern. The experimenter should justify their run count relative to expected variance.

### Registry Awareness
**Purpose**: Avoid re-testing hypotheses that prior experiments already resolved.

**The test**: "Has this hypothesis (or a substantially similar one) already been tested?"

Read the experiment registry before designing new experiments. Previously REJECTED hypotheses need new evidence or a meaningfully different angle to justify re-testing.

## Orchestration Steps

### 1. Initialize Experiment
- Parse symptom/question from user request
- Check for existing experiment registry — read before creating new hypotheses
- State: "Starting experiment workflow for: [observation]"

### 1b. Resume Gate
If a completed experiment entry is provided (Steps 1-5 already filled):
- Verify Steps 1-5 are present and complete
- If DESIGN-REVIEW was already done (e.g., experiment previously approved), skip directly to Phase 2 (EXECUTE)
- Otherwise proceed to Phase 1 (DESIGN-REVIEW)
- State: "Resuming experiment [id] from Phase [N]"

### 2. Phase 1: DESIGN-REVIEW
Invoke HyperSan to validate experiment design. HyperSan should reason about:
- **Predictions quality**: Are they specific enough to be falsifiable? Do they have clear metrics and tolerances?
- **Causal isolation**: Can observed effects be attributed? (Apply the reasoning from Scientific Guardrails, not a mechanical variable count.)
- **Confirmation sufficiency**: Is the run count justified for the expected variance?
- **Guardrail proportionality**: Are execution guardrails proportionate to known risks? (An experiment with known explosion risk should have early-stop clauses. A stable diagnostic run may not need them.)

**If substantial issues**: Return to experiment author with specific reasoning. Max 2 revision cycles.
**If sound**: Proceed to Phase 2 autonomously.

### 3. Phase 2: EXECUTE
HyperOrch MUST invoke `runSubagent(HyperArch)` for this phase. If `runSubagent` is unavailable or fails, report the delegation failure to the user — do not improvise alternative execution.

Invoke HyperArch to run the experiment:
```yaml
task: "Execute experiment and collect measurements"
context: "[Full experiment entry, instrumentation plan, execution guardrails]"
agent: HyperArch
delivers: "Measurement table, execution log, any early-stop records"
```

HyperArch runs ALL arms end-to-end within a single delegation. No inter-arm returns to HyperOrch. HyperArch evaluates infrastructure aborts and early-stop clauses during execution.

### 4. Phase 3: ANALYZE
Invoke HyperSan to review measurements against predictions:
```yaml
task: "Compare predictions to measurements, propose verdict"
agent: HyperSan
output: "Verdict with justification, prediction-vs-measurement table"
```

If recording or cleanup is needed, HyperOrch delegates to HyperArch:
```yaml
task: "Record verdict, update registry, write handoff notes, run cleanup gate"
agent: HyperArch
gate: "Experiment entry complete, registry updated"
```

### 5. Decision Gate
- **Verdict = CONFIRMED**: Proceed to fix/implementation (hand off to `orch-implementation`)
- **Verdict = REJECTED / INCONCLUSIVE**: Loop back to Step 2 with new/refined hypotheses
- **Hypothesis space exhausted**: Report findings, recommend broader investigation
- **Context boundary**: Write handoff notes, ensure registry is current

## Execution Guardrails

### Infrastructure Aborts (mandatory)
True aborts — HyperArch stops the experiment immediately. These are not judgment calls:
- OOM / out-of-memory
- NaN loss or numeric divergence
- Process crash / segfault
- Wrong config loaded (detected via config hash mismatch)
- Instrumentation missing (expected probe files not created)

### Early-Stop Clauses (optional, declared in experiment spec)
Pre-registered conditions evaluated by HyperArch during execution. If triggered, the arm is recorded as `terminated: [reason]` — this is DATA, not an emergency.

```yaml
early_stop_if: "any arm dino_loss > 50 for 10 consecutive steps"
```

**Judgment guidance**: Experiments with known instability risks (e.g., prior gradient explosions) benefit from early-stop clauses. Stable diagnostic runs may not need them. The experimenter should reason about proportionality — guardrails should match the risk profile, not be applied uniformly.

Prediction deviations are data for ANALYZE, not abort triggers.

### Resource Budget (optional)
Compute time, API calls, storage. `N/A` with justification is valid.

## Multi-Arm Extension
For experiments testing multiple configurations:
→ See [multi_arm_extension.md](assets/multi_arm_extension.md) for naming, structure, and verdict rules

The experiment spec declares its arm execution mode:
- **`pre-committed`**: All arms run unconditionally. Analysis happens post-hoc.
- **`sequential-gated`**: Arms run in order with pre-registered stop conditions between them.

HyperArch respects the declared mode. HyperOrch does NOT inject Go/No-Go gates between arms.

## Long-Running Execution Protocol

HyperArch decides execution strategy based on estimated runtime:

- **Under ~15 minutes**: Execute inline and return results directly.
- **Over ~15 minutes**: Return a **monitoring plan** instead of blocking. Includes: exact command(s) launched, expected output locations, key metrics to watch, estimated completion time. HyperOrch relays the monitoring plan to the user.

When results are available, HyperOrch resumes at Phase 3 (ANALYZE).

HyperOrch NEVER constructs launch commands — this is HyperArch's responsibility.

## Agent Handoff Protocol
When context is approaching capacity:
1. Update experiment registry with current status
2. Write handoff notes in current experiment entry
3. Ensure all generated data files are saved
4. Next agent reads registry → latest experiment → continues from last step

## Output Format

### Experiment Complete
```
## Experiment Result: [experiment_id]
**Verdict**: [CONFIRMED|REJECTED|PARTIALLY CONFIRMED|INCONCLUSIVE]
**Hypothesis**: [one-line summary]
**Key Finding**: [what the data showed]
**Next Action**: [fix/new hypothesis/escalate]
```

### Loop Continuing
```
## Experiment Loop Status
**Completed**: [N] experiments
**Current Verdict**: [verdict]
**Next Hypothesis**: [what to test next]
**Registry**: [path to registry]
```

## Critical Rules
- **All 8 Steps Mandatory**: Do not skip any step in the loop
- **Predictions Gate is Hard**: Step 3 before Step 6 — no exceptions
- **One-Variable Rule is Hard**: Interventional = exactly one change from baseline
- **Four Verdicts Only**: CONFIRMED, REJECTED, PARTIALLY CONFIRMED, INCONCLUSIVE
- **No LIKELY Tier on Verdicts**: Agents misuse it — use INCONCLUSIVE instead
- **Registry First**: Read existing experiments before creating new hypotheses
- **No Direct Execution**: HyperOrch delegates ALL execution via `runSubagent` — never runs experiments itself
- **Max 2 Design Revisions**: If DESIGN-REVIEW fails twice, halt and report
- **Handoff Before Context Loss**: Always update registry before context boundary
- **DESIGN-REVIEW is the Only Gate**: Once passed, execution proceeds autonomously — no orchestrator-injected checkpoints

## Template
Base experiment entry template:
→ See [experiment_entry.base.template.md](assets/experiment_entry.base.template.md)
