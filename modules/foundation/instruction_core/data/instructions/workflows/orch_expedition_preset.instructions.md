---
applyTo: "**/hyper_orchestrator.adhd.agent.md"
---

# HyperOrch Expedition Preset

## Goals
- Orchestrate 8-phase expedition pipeline with 3 mandatory stop points
- Ensure L1 Bundle architecture: target stays pristine, sidecar owns infrastructure
- Coordinate HyperExped, HyperSan, HyperDream, HyperSmith, HyperArch agents

## When This Applies
Trigger patterns: "expedition", "export adhd", "export agents", "run expedition", "deploy to", "export to [project]"

## L1 Bundle Architecture
| Location | Assets |
|----------|--------|
| **Sidecar** | MCPs, registry managers, `.agent_plan/`, expedition profiles |
| **Target** | `.github/` (agents, instructions, prompts), `.vscode/mcp.json`, `CONTRIBUTING.md` |

**CRITICAL:** NO `.agent_plan/` in target. All planning artifacts stay in sidecar.

## Pipeline Structure
```
Phase 1: Scout → Phase 2: Readiness Gate → Phase 3: Planning → Phase 4: Feasibility Gate
    ↓
🛑 STOP POINT 1 (User confirms manifest before execution)
    ↓
Phase 5: Execution → Phase 6: Verification
    ↓
🛑 STOP POINT 2 (User confirms registry manager creation)
    ↓
Phase 7: Registry Manager Creation
    ↓
🛑 STOP POINT 3 (User confirms MCP creation)
    ↓
Phase 8: MCP Module Creation → ✅ Complete
```

## Orchestration Steps

### 1. Initialize Expedition
- Parse target path from user request
- State: "Starting expedition workflow for: [target_path]"
- Create expedition folder: `.agent_plan/expedition/{target_name}/`

### 2. Phase 1: SCOUT
Invoke HyperExped:
```yaml
task: "Scout target project for expedition"
context: "Target path: [path]. Generate Scout Report with YAML frontmatter."
output_location: ".agent_plan/expedition/{target}/scout_report.md"
output_format: "Scout Report (see expedition.instructions.md)"
```

**Evaluate:**
- If recommendation is `ABORT` → Report reason, HALT
- If recommendation is `PROCEED` or `PROCEED_WITH_CAUTION` → Continue

### 3. Phase 2: READINESS GATE
Invoke HyperSan:
```yaml
task: "3-tier readiness validation for expedition"
context: "Scout report: [summary]. Validate: hard blockers, git state, source readiness."
success_criteria: "All Tier 1 pass, no Tier 2 blockers"
output_format: "summary"
```

**Evaluate:**
- If FAILED → Report blockers with remediation, HALT
- If PASSED → Continue

### 4. Phase 3: PLANNING
Invoke HyperExped + HyperDream (collaborate):
```yaml
task: "Generate expedition scope and adaptation notes"
context: "Scout report passed readiness. Target: [path], Framework: [detected]"
output_files:
  - ".agent_plan/expedition/{target}/expedition_scope.yaml"
  - ".agent_plan/expedition/{target}/adaptation_notes.md"
```

### 5. Phase 4: FEASIBILITY GATE
Invoke HyperSan:
```yaml
task: "Validate expedition scope against target state"
context: "Scope: [summary]. Validate: paths exist, no collisions, chunk sizes valid"
success_criteria: "Plan is executable without conflicts"
output_format: "summary"
```

**Evaluate:**
- If `NEEDS_FIX` → Return to Planning with fixes
- If `PASS` → Continue to STOP POINT 1

### 6. 🛑 STOP POINT 1: Pre-Execution Confirmation
**Present to user:**
```markdown
## 📋 EXPEDITION MANIFEST

**Target:** [path]
**Framework:** [detected]
**Artifacts:** [count] files in [chunk_count] chunks

### Will Create in Target:
- `.github/agents/` → [count] agents
- `.github/instructions/` → [count] instructions
- `.vscode/mcp.json` → MCP configuration
- `CONTRIBUTING.md` → Sidecar breadcrumb

### Will Create in Sidecar:
- `managers/{target}_module_registry_manager/`
- `mcps/{target}_adhd_mcp/`

**Proceed with execution?** (yes/no)
```

**Await explicit "yes" before continuing.**

### 7. Phase 5: EXECUTION
Invoke HyperExped (orchestrates) + HyperSmith (creates):
```yaml
task: "Execute chunked export with git checkpoint"
context: "Approved scope. Create git checkpoint first."
chunk_size: 5
mode: "PAUSE"  # Require confirmation per chunk
```

**For each chunk:**
- Display chunk contents
- Await user confirmation
- Execute via HyperSmith
- Report success/failure

### 8. Phase 6: VERIFICATION
Invoke HyperSan:
```yaml
task: "Verify expedition artifacts"
context: "Execution complete. Validate: all created, headers present, refs valid, no target pollution"
success_criteria: "All artifacts verified, no .agent_plan in target"
output_format: "summary"
```

**If FAILED:** Report issues, suggest rollback via `git reset --hard HEAD~1`

### 9. 🛑 STOP POINT 2: Pre-Registry Confirmation
```markdown
## 🏗️ REGISTRY MANAGER CREATION

Execution verified. Ready to create per-target registry manager.

**Will Create:** `managers/{target}_module_registry_manager/`

This module configures sidecar to understand target's ecosystem patterns.

**Proceed with registry manager creation?** (yes/no)
```

### 10. Phase 7: REGISTRY MANAGER
Invoke HyperArch:
```yaml
task: "Create per-target module registry manager"
context: "Target: [name], Ecosystem: [type]. Extend exped_module_registry_manager_core."
output_location: "managers/{target}_module_registry_manager/"
```

### 11. 🛑 STOP POINT 3: Pre-MCP Confirmation
```markdown
## 🔌 MCP MODULE CREATION

Registry manager created. Ready to create per-target MCP module.

**Will Create:** `mcps/{target}_adhd_mcp/`

This MCP serves target project via `.vscode/mcp.json` configuration.

**Proceed with MCP creation?** (yes/no)
```

### 12. Phase 8: MCP MODULE
Invoke HyperArch:
```yaml
task: "Create per-target ADHD MCP module"
context: "Target: [name]. Use exped_adhd_mcp template. Include workspace_path validation."
output_location: "mcps/{target}_adhd_mcp/"
```

### 13. Finalization
Generate manifest at `.agent_plan/expedition/{target}/manifest.yaml`

**Present completion summary:**
```markdown
## ✅ EXPEDITION COMPLETE

**Target:** [path]
**Phases Completed:** 8/8

### Created in Target (L1 Bundle):
- [list of files]

### Created in Sidecar:
- `managers/{target}_module_registry_manager/`
- `mcps/{target}_adhd_mcp/`
- `.agent_plan/expedition/{target}/manifest.yaml`

### Next Steps:
1. Open target in VS Code
2. Verify MCP connection via `.vscode/mcp.json`
3. Test adapted agents in target project
```

## Abort Handling
At any stop point, if user says "no", "abort", "cancel":
```markdown
## ⏸️ EXPEDITION PAUSED

Stopped at: [phase/stop point]
Artifacts created so far: [list]
Expedition can be resumed by re-running with same target.

To rollback target changes: `cd [target_path] && git reset --hard HEAD~1`
```

## Critical Rules
- **All 3 Stop Points Mandatory**: NEVER skip user confirmation
- **No Target Pollution**: NEVER create `.agent_plan/` in target
- **Chunk Limits**: Max 5 artifacts per execution chunk
- **Git Checkpoint**: ALWAYS create before execution phase
- **HyperOrch Never Creates Files**: Delegate to HyperSmith and HyperArch
- **Workspace Isolation**: Validate workspace_path in all MCP calls
