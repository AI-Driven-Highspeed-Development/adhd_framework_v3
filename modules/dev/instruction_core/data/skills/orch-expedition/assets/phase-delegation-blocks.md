# Expedition Phase Delegation Blocks

All phase delegation YAML blocks used by HyperOrch during the expedition pipeline.

## Phase 1: SCOUT (HyperExped)

```yaml
task: "Scout target project for expedition"
context: "Target path: [path]. Generate Scout Report with YAML frontmatter."
output_location: ".agent_plan/expedition/{target}/scout_report.md"
output_format: "Scout Report (see expedition skill)"
```

## Phase 2: READINESS GATE (HyperSan)

```yaml
task: "3-tier readiness validation for expedition"
context: "Scout report: [summary]. Validate: hard blockers, git state, source readiness."
success_criteria: "All Tier 1 pass, no Tier 2 blockers"
output_format: "summary"
```

## Phase 3: PLANNING (HyperExped + HyperDream)

```yaml
task: "Generate expedition scope and adaptation notes"
context: "Scout report passed readiness. Target: [path], Framework: [detected]"
output_files:
  - ".agent_plan/expedition/{target}/expedition_scope.yaml"
  - ".agent_plan/expedition/{target}/adaptation_notes.md"
```

## Phase 4: FEASIBILITY GATE (HyperSan)

```yaml
task: "Validate expedition scope against target state"
context: "Scope: [summary]. Validate: paths exist, no collisions, chunk sizes valid"
success_criteria: "Plan is executable without conflicts"
output_format: "summary"
```

## Phase 5: EXECUTION (HyperExped + HyperSmith)

```yaml
task: "Execute chunked export with git checkpoint"
context: "Approved scope. Create git checkpoint first."
chunk_size: 5
mode: "PAUSE"  # Require confirmation per chunk
```

## Phase 6: VERIFICATION (HyperSan)

```yaml
task: "Verify expedition artifacts"
context: "Execution complete. Validate: all created, headers present, refs valid, no target pollution"
success_criteria: "All artifacts verified, no .agent_plan in target"
output_format: "summary"
```

## Phase 7: REGISTRY MANAGER (HyperArch)

```yaml
task: "Create per-target module registry manager"
context: "Target: [name], Ecosystem: [type]. Extend exped_module_registry_manager_core."
output_location: "managers/{target}_module_registry_manager/"
```

## Phase 8: MCP MODULE (HyperArch)

```yaml
task: "Create per-target ADHD MCP module"
context: "Target: [name]. Use exped_adhd_mcp template. Include workspace_path validation."
output_location: "mcps/{target}_adhd_mcp/"
```
