---
name: attack-testing
description: "HyperRed adversarial testing skill — attack patterns, edge case discovery, boundary testing, stress testing, and breaking code. Covers HyperRed artifact conventions (.agent_plan/red_team/), findings output format, attack script organization, adversarial testing approaches, and pre-attack checklists. Use this skill when running adversarial tests, discovering edge cases, stress-testing modules, or producing Red Team findings."
---

# Adversarial Testing

HyperRed attack patterns, edge case discovery, and breaking code.

## When to Use
- Running adversarial tests against a module
- Discovering edge cases and boundary conditions
- Stress-testing module APIs and interfaces
- Producing Red Team findings and evidence
- Planning attack strategies before breaking code

---

## Attack Workflow

### Pre-Attack Checklist
1. **Check existing findings**: Look at `.agent_plan/red_team/<module>/findings/`
2. If previous findings exist, review before re-attacking (avoid duplicate work)
3. Read the module's public API surface — imports, class signatures, function signatures
4. Identify input boundaries, state transitions, and error handling paths
5. Create attack scripts in `.agent_plan/red_team/<module>/attacks/`

### Attack Execution
1. Start with boundary testing (min/max/zero/empty/None)
2. Escalate to type confusion and invalid state attacks
3. Run stress tests if applicable
4. Log all evidence to `evidence/` folder
5. Write structured findings

---

## Attack Patterns

Reference tables for Boundary, Type Confusion, State, Error Handling, and Stress testing patterns:
→ See [attack-vectors.md](assets/attack-vectors.md)

---

## Artifact Conventions

Directory structure, git tracking rules, findings output location, and severity levels:
→ See [artifact-structure.md](assets/artifact-structure.md)

### Findings JSON Schema

Structured JSON format for recording findings per session:
→ See [findings-schema.json](assets/findings-schema.json)

---

## Cleanup

| Folder | Cleanup Rule |
|--------|--------------|
| `.agent_plan/red_team/evidence/` | Prune after fixes verified |
| `.agent_plan/red_team/attacks/` | Keep for regression re-runs |
| `.agent_plan/red_team/findings/` | Keep permanently (git-tracked) |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Write implementation tests (unit/integration) | Those belong to HyperArch in `<module>/tests/` |
| Test happy paths only | Focus on unhappy paths, edge cases, boundary conditions |
| Fix the bugs you find | Report findings — HyperArch implements fixes |
| Skip checking previous findings | Always review existing findings first |
| Write vague finding descriptions | Include exact reproduction steps and evidence |
| Attack without reading the API surface | Read module imports and signatures first |

---

## Cross-References

| Topic | Where |
|-------|-------|
| Multi-agent testing loops (Orch + Red + Arch) | `orch-testing` skill |
| Findings output format details | `san-output` skill |
| Module development and test folder conventions | `module-dev` skill |
