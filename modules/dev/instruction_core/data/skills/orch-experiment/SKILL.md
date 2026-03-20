---
name: orch-experiment
description: "Orchestrator experiment preset — coordinating scientific experiment workflows across specialist agents. Manages structured hypothesis testing: OBSERVE → HYPOTHESIZE → PREDICT → DESIGN → INSTRUMENT → EXECUTE → ANALYZE → RECORD. Enforces predictions-before-execution, one-variable rule for interventional experiments, and four post-experiment verdicts (CONFIRMED/REJECTED/PARTIALLY CONFIRMED/INCONCLUSIVE). Use this skill when orchestrating experiments, debugging via scientific method, or running structured hypothesis-driven investigations."
---

# HyperOrch Experiment Preset

## Goals
- Orchestrate structured hypothesis-driven experiment workflows
- Enforce scientific rigor: predictions before execution, one-variable rule
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

- **DESIGN-REVIEW**: HyperSan validates the experiment spec upfront — predictions, type, one-variable rule, confirmation runs, guardrails. This is the ONLY gate before execution.
- **EXECUTE**: HyperArch receives full experiment context and runs all arms end-to-end. No inter-arm returns to HyperOrch. Collects all probe data, compiles measurement table, returns results.
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

### Step 3: PREDICT ⛔ GATE
State specific predictions BEFORE execution. Use the 5-column prediction table:

| # | If hypothesis is true... | Metric | Expected Value | Tolerance |
|---|--------------------------|--------|----------------|-----------|

**HARD GATE**: Predictions MUST be written before Step 6. No exceptions. Prevents post-hoc rationalization.

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
- **Observational** experiments: add `# PROBE` tagged instrumentation
  → See [probing_guideline.md](assets/probing_guideline.md) for principles, tag convention, and cleanup
- **Interventional** experiments: add `# INTERVENTION` tagged code changes or use branch/config strategy
  → See [intervention_procedure.md](assets/intervention_procedure.md) for tiered strategy and cleanup gates

### Step 6: EXECUTE
Run the experiment. Collect data. Log everything.
- Record execution environment, timestamps, any anomalies.

### Step 7: ANALYZE
Compare predictions to measurements. Force a verdict:

`CONFIRMED` | `REJECTED` | `PARTIALLY CONFIRMED` | `INCONCLUSIVE`

- No LIKELY tier. No "LIKELY CONFIRMED". Agents misuse them.
- Suggestive-but-not-conclusive → `INCONCLUSIVE` with recommendation narrative.
- `PARTIALLY CONFIRMED`: Some predictions match, others don't, but evidence is clear.

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

## Orchestration Steps

### 1. Initialize Experiment
- Parse symptom/question from user request
- Check for existing experiment registry — read before creating new hypotheses
- State: "Starting experiment workflow for: [observation]"

### 1b. Resume Gate
If a completed experiment entry is provided (Steps 1-5 already filled):
- Verify Steps 1-5 are present and complete
- If DESIGN-REVIEW was already done (e.g., experiment previously approved), skip directly to Phase 2 (EXECUTE)
- Otherwise skip to Phase 1 (DESIGN-REVIEW)
- State: "Resuming experiment [id] from Phase [N]"

### 2. Phase 1: DESIGN-REVIEW ⛔
Invoke HyperSan to validate experiment design:
```yaml
task: "Validate experiment design"
agent: HyperSan
checks:
  - "Predictions written before execution? (Step 3 complete)"
  - "Experiment type classified? (Observational/Interventional)"
  - "One-variable rule met? (if Interventional)"
  - "minimum_confirmation_runs set?"
  - "Execution guardrails addressed? (infrastructure aborts, early-stop clauses, resource budget)"
```
**If FAILED**: Return to experiment author with specific issues. Max 2 revision cycles.
**If PASSED**: Proceed to Phase 2 autonomously. No further gates before execution.

### 3. Phase 2: EXECUTE
HyperOrch MUST invoke `runSubagent(HyperArch)` for this phase. If `runSubagent` is unavailable or fails, report the delegation failure to the user — do not improvise alternative execution.

Invoke HyperArch to run the experiment:
```yaml
task: "Execute experiment and collect measurements"
context: "[Full experiment entry, instrumentation plan, execution guardrails]"
agent: HyperArch
delivers: "Measurement table, execution log, any early-stop records"
```

HyperArch runs ALL arms end-to-end within a single delegation. No inter-arm returns to HyperOrch. HyperArch evaluates infrastructure aborts and early-stop clauses during execution. See **Execution Guardrails** and **Long-Running Execution Protocol** for behavioral details.

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

## Hard-Mandatory Gates
- **Predictions-before-execution**: Step 3 MUST be complete before Step 6. Violation = invalid experiment.
- **One-variable rule**: Interventional experiments change exactly ONE variable from baseline. No exceptions.

## Execution Guardrails

### Infrastructure Aborts (mandatory)
True aborts — HyperArch stops the experiment immediately:
- OOM / out-of-memory
- NaN loss or numeric divergence
- Process crash / segfault
- Wrong config loaded (detected via config hash mismatch)
- Instrumentation missing (expected probe files not created)

### Early-Stop Clauses (optional, declared in experiment spec)
Pre-registered conditions evaluated by HyperArch during execution. If triggered, the arm is recorded as `terminated: [reason]` — this is DATA, not an emergency.

Declared in the experiment entry under `early_stop_if`:
```yaml
early_stop_if: "any arm dino_loss > 50 for 10 consecutive steps"
```

Prediction deviations are data for ANALYZE, not abort triggers.

### Resource Budget (optional)
Compute time, API calls, storage. `N/A` with justification is valid.

## Multi-Arm Extension
For experiments testing multiple configurations of one variable:
→ See [multi_arm_extension.md](assets/multi_arm_extension.md) for naming, structure, and verdict rules

The experiment spec declares its arm execution mode:
- **`pre-committed`**: All arms run unconditionally. HyperArch executes every arm regardless of intermediate results.
- **`sequential-gated`**: Arms run in order with pre-registered stop conditions between them (declared in the experiment spec, NOT added by the orchestrator).

HyperArch respects the declared mode. HyperOrch does NOT inject Go/No-Go gates between arms.

## Long-Running Execution Protocol

HyperArch decides execution strategy based on estimated runtime:

- **Under ~15 minutes**: Execute inline and return results directly. No monitoring plan. No user involvement.
- **Over ~15 minutes**: Return a **monitoring plan** instead of blocking. The monitoring plan includes: exact command(s) launched, expected output locations, key metrics to watch, estimated completion time. HyperOrch relays the monitoring plan to the user.

When results are available (user provides output or points to probe files), HyperOrch resumes at Phase 3 (ANALYZE).

HyperOrch NEVER constructs launch commands — this is HyperArch's responsibility even for "simple" commands.

## Anti-Patterns

| # | Anti-Pattern | Do Instead |
|---|-------------|------------|
| 1 | "The root cause is obviously X" | Write hypothesis, predict, run, THEN fix |
| 2 | Changing 3 things at once (interventional) | One variable per interventional experiment |
| 3 | "The math says so" — skipping measurement | Math is hypothesis source, not evidence |
| 4 | Skipping the prediction step | Every run after OBSERVE needs a prediction |
| 5 | CONFIRMED after one stochastic run | Minimum 2 runs for stochastic confirmation |
| 6 | Re-testing previously REJECTED hypotheses | Read experiment registry first |
| 7 | "Fix" doesn't change the target metric | Not a fix — record as REJECTED |

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
