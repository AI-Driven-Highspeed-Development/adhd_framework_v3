# Probing Guideline

Domain-agnostic probing guideline for observational experiments (Step 5: INSTRUMENT).

## 7 Principles

### 1. Singleton Access
Single global entry point (activate/get/deactivate). No threading probe objects through function signatures. Domain doesn't matter: web servers, compilers, data pipelines all benefit.

### 2. Guard Pattern
Every probe callsite is a no-op when probe isn't active (`if probe: probe.log(...)`). Zero overhead in production.

### 3. Manifest-Controlled Sampling
Configuration file (not code) controls which probe sites fire and on which iterations/requests/events. Separates "what to observe" from "where observation points exist."

### 4. Summaries, Not Dumps
Log derived scalars (counts, means, min/max, percentiles), never raw objects. Keeps output small regardless of domain.

### 5. Structured Line Output
One JSON object per event (JSONL). Human-readable, grep-able, machine-parseable.

### 6. Budget Constraint
Probe output designed small by default (~200 bytes/event). Manifest caps volume.

### 7. Probe Import Isolation
Probe imports MUST use conditional import with no-op fallback. If the probe library doesn't exist, the module still works.

```python
try:                                    # PROBE
    from project.debug_lab.probe import get_probe  # PROBE
except ImportError:                     # PROBE
    get_probe = lambda: None            # PROBE
```

## Tag Convention

**Tag**: `# PROBE` (observation only)

- Every instrumented line MUST end with `# PROBE`
- Multi-line expressions: EVERY continuation line carries `# PROBE`
- Optional extended form: `# PROBE:probe_id` for selective cleanup when multiple experiments coexist

### Language Adaptation

| Language | Tag Syntax |
|----------|-----------|
| Python | `# PROBE` |
| JavaScript/TypeScript | `// PROBE` |
| Rust/C/C++/Java/Go | `// PROBE` |
| Shell/Bash/YAML | `# PROBE` |
| HTML/XML | `<!-- PROBE -->` |
| CSS | `/* PROBE */` |
| SQL | `-- PROBE` |

## Guard Pattern Example (Python)

```python
from project.debug_lab.probe import get_probe  # PROBE
p = get_probe()  # PROBE
if p is not None:  # PROBE
    p.log("endpoint_latency", step=request_count,  # PROBE
          p50=latency_p50,  # PROBE
          p99=latency_p99,  # PROBE
          error_rate=errors / total)  # PROBE
```

## Cleanup Procedure

### 1. Lint
Pre-cleanup validation: verify no untagged lines exist between tagged lines in the same block. If validation fails, abort automated cleanup, fall back to manual.

### 2. List
```bash
grep -rn "# PROBE" <scope>
```
Review all instrumented lines.

### 3. Remove
```bash
sed -i '/# PROBE/d' <files>
```
Or language-appropriate equivalent.

### 4. Verify
Run test suite. If tests fail, a probe line was load-bearing → reclassify as `# INTERVENTION`, fix the violation.

## Critical Invariant

Probe lines must NEVER be load-bearing. Removing every `# PROBE` line must leave working code. The verify step IS the enforcement. If anything breaks, the line is an intervention mislabeled as a probe.

## Probe Data Lifecycle

- Each experiment gets its own output path (one file per experiment)
- Step 8 (RECORD) must reference the exact probe file used
- No global/shared probe output — prevents data mixing between experiments
