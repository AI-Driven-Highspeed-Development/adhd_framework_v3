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
SETUP (HyperArch) → DESIGN-REVIEW (HyperSan) → EXECUTE (HyperArch) → ANALYZE (HyperSan) → RECORD (HyperArch)
```

- **SETUP**: HyperArch creates experiment entry, instruments, prepares config
- **DESIGN-REVIEW**: HyperSan validates design (predictions written? type classified? one-variable rule met?)
- **EXECUTE**: HyperArch runs the experiment, collects data
- **ANALYZE**: HyperSan compares predictions to measurements, proposes verdict
- **RECORD**: HyperArch updates registry, writes handoff notes

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

### 2. Phase 1: SETUP
Invoke HyperArch to scaffold experiment:
```yaml
task: "Create experiment entry from observation"
context: "[Observation data, prior experiments if any]"
agent: HyperArch
gate: "Experiment entry created with Steps 1-4 filled"
```

### 3. Phase 2: DESIGN-REVIEW ⛔
Invoke HyperSan to validate experiment design:
```yaml
task: "Validate experiment design"
agent: HyperSan
checks:
  - "Predictions written before execution? (Step 3 complete)"
  - "Experiment type classified? (Observational/Interventional)"
  - "One-variable rule met? (if Interventional)"
  - "minimum_confirmation_runs set?"
  - "Safety slots addressed? (budget, rollback, abort)"
```
**If FAILED**: Return to Phase 1 with specific issues. Max 2 revision cycles.

### 4. Phase 3: EXECUTE
Invoke HyperArch to run the experiment:
```yaml
task: "Execute experiment and collect measurements"
context: "[Experiment entry, instrumentation plan]"
agent: HyperArch
gate: "Measurements collected, execution log filled"
```

### 5. Phase 4: ANALYZE
Invoke HyperSan to review measurements against predictions:
```yaml
task: "Compare predictions to measurements, propose verdict"
agent: HyperSan
output: "Verdict with justification, prediction-vs-measurement table"
```

### 6. Phase 5: RECORD
Invoke HyperArch to finalize:
```yaml
task: "Record verdict, update registry, write handoff notes"
agent: HyperArch
gate: "Experiment entry complete, registry updated"
```

### 7. Decision Gate
- **Verdict = CONFIRMED**: Proceed to fix/implementation (hand off to `orch-implementation`)
- **Verdict = REJECTED / INCONCLUSIVE**: Loop back to Step 2 with new/refined hypotheses
- **Hypothesis space exhausted**: Report findings, recommend broader investigation
- **Context boundary**: Write handoff notes, ensure registry is current

## Hard-Mandatory Gates
- **Predictions-before-execution**: Step 3 MUST be complete before Step 6. Violation = invalid experiment.
- **One-variable rule**: Interventional experiments change exactly ONE variable from baseline. No exceptions.

## Opt-In Safety Slots
Required sections in template but `N/A` with justification is valid:
- **Resource budget**: Compute time, API calls, storage
- **Rollback procedure**: How to undo if experiment damages state
- **Abort criteria**: When to stop early

## Multi-Arm Extension
For experiments testing multiple configurations of one variable:
→ See [multi_arm_extension.md](assets/multi_arm_extension.md)

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
- **No Direct Execution**: HyperOrch NEVER runs experiments itself
- **Max 2 Design Revisions**: If DESIGN-REVIEW fails twice, halt and report
- **Handoff Before Context Loss**: Always update registry before context boundary

## Template
Base experiment entry template:
→ See [experiment_entry.base.template.md](assets/experiment_entry.base.template.md)
