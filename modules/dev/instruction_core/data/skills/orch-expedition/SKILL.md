---
name: orch-expedition
description: "Orchestrator expedition preset — coordinating the 8-phase expedition pipeline for exporting ADHD agents to external projects. Manages L1 Bundle architecture with 3 mandatory stop points, agent delegation (HyperExped, HyperSan, HyperDream, HyperSmith, HyperArch), and verification gates. Use this skill when orchestrating an expedition export to a non-ADHD project."
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

All phase delegation YAML blocks (Phases 1–8):
→ See [phase-delegation-blocks.md](assets/phase-delegation-blocks.md)

### 1. Initialize Expedition
- Parse target path from user request
- State: "Starting expedition workflow for: [target_path]"
- Create expedition folder: `.agent_plan/expedition/{target_name}/`

### 2–5. Phases 1–4 (Scout → Feasibility Gate)
- **Phase 1 SCOUT**: HyperExped scouts target. If `ABORT` → HALT.
- **Phase 2 READINESS GATE**: HyperSan validates. If FAILED → HALT.
- **Phase 3 PLANNING**: HyperExped + HyperDream collaborate on scope.
- **Phase 4 FEASIBILITY GATE**: HyperSan validates scope. If `NEEDS_FIX` → return to Planning.

### 6. STOP POINT 1: Pre-Execution Confirmation
Present expedition manifest to user and await explicit "yes".
→ See [stop-point-1.md](assets/stop-point-1.md)

### 7–8. Phases 5–6 (Execution → Verification)
- **Phase 5 EXECUTION**: HyperExped + HyperSmith execute chunked export (max 5 per chunk, PAUSE mode).
- **Phase 6 VERIFICATION**: HyperSan verifies all artifacts. If FAILED → suggest rollback.

### 9. STOP POINT 2: Pre-Registry Confirmation
→ See [stop-point-2.md](assets/stop-point-2.md)

### 10. Phase 7: REGISTRY MANAGER (HyperArch)
Create per-target module registry manager.

### 11. STOP POINT 3: Pre-MCP Confirmation
→ See [stop-point-3.md](assets/stop-point-3.md)

### 12. Phase 8: MCP MODULE (HyperArch)
Create per-target ADHD MCP module.

### 13. Finalization
Generate manifest and present completion summary:
→ See [expedition-complete-template.md](assets/expedition-complete-template.md)

## Abort Handling
At any stop point, if user says "no", "abort", "cancel":
→ See [expedition-abort-template.md](assets/expedition-abort-template.md)

## Critical Rules
- **All 3 Stop Points Mandatory**: NEVER skip user confirmation
- **No Target Pollution**: NEVER create `.agent_plan/` in target
- **Chunk Limits**: Max 5 artifacts per execution chunk
- **Git Checkpoint**: ALWAYS create before execution phase
- **HyperOrch Never Creates Files**: Delegate to HyperSmith and HyperArch
- **Workspace Isolation**: Validate workspace_path in all MCP calls
