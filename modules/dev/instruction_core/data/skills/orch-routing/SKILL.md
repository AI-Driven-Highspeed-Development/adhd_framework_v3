---
name: orch-routing
description: "Orchestrator routing preset — routing user requests to the correct specialist agent based on task analysis. Supports single-agent, multi-phase, and parallel routing patterns. Maps user intent to the appropriate Hyper agent using keyword matching, context analysis, and domain ownership rules. Use this skill when determining which agent should handle a user request or coordinating cross-domain tasks."
---

# HyperOrch Routing Preset

## Goals
- Route tasks to appropriate specialist agents efficiently
- Construct delegation prompts that enable OBJECTIVE COMPLETION
- Support single-agent, multi-phase, and parallel routing patterns

## When This Applies
Trigger when request does NOT match discussion/implementation/testing patterns:
- Agent-specific requests: "create agent file", "review quality", "attack this"
- Cross-domain coordination: "check then fix", "plan then implement"
- Ambiguous requests requiring clarification or agent discovery

---

## Document Ownership Routing Table

Routes file patterns to their owning agent:
→ See [ownership-routing.md](assets/ownership-routing.md)

---

## Routing Patterns

### 1. Single-Agent Routing
For tasks that map cleanly to ONE specialist:
```yaml
pattern: "[request] → [agent]"
examples:
  - "Create an agent file for X" → HyperAgentSmith
  - "Review code quality in module Y" → HyperIQGuard
  - "Write vision doc for feature Z" → HyperDream
  - "Manage project board tasks" → HyperPM
```

### 2. Multi-Phase Routing
For sequential workflows requiring multiple agents:
```yaml
pattern: "[A] → [B] → [C]"
examples:
  - "Check if X is broken, then fix it"
    → HyperSan (validate) → HyperArch (fix)
  - "Draft vision, then implement"
    → HyperDream (vision) → HyperArch (implement)
  - "Create agent, then test it"
    → HyperAgentSmith (create) → HyperSan (validate)
  - "Maybe also do X please?"
    → HyperSan (assess) → HyperArch (implement) / Halt if not feasible
```

### 3. Parallel Routing
For independent tasks that can run simultaneously:
```yaml
pattern: "[A] + [B]"
examples:
  - "Check quality AND attack edge cases"
    → HyperIQGuard + HyperRed (parallel)
```
**NOTE**: Use parallel only when tasks have NO dependencies.

## Agent Selection Guidance

Maps request indicators to specialist agents:
→ See [agent-selection.md](assets/agent-selection.md)

## Prompt Construction Guidance

### Objective Completion Autonomy

Guidance for instructing subagents to pursue objective completion, not just literal task execution:
→ See [objective-completion-guidance.md](assets/objective-completion-guidance.md)

### Delegation Prompt Template

Canonical YAML template for all delegation prompts:
→ See [delegation-prompt-template.yaml](assets/delegation-prompt-template.yaml)

## Execution Flow

```
1. Classify routing pattern (single / multi-phase / parallel)
2. Identify target agent(s)
3. Construct delegation prompt with FULL context and objective
4. Invoke subagent(s) via runSubagent
5. Collect summary
6. If multi-phase: pass summary to next phase
7. Finalize with combined summary
```

## Output Format

### Single-Agent Routing
→ See [routing-single-output.md](assets/routing-single-output.md)

### Multi-Phase Routing
→ See [routing-multi-output.md](assets/routing-multi-output.md)

## Critical Rules
- **Provide FULL Context**: Subagents cannot read your mind. Include objective, not just task.
- **Enable Autonomy**: Use the Objective Completion Autonomy guidance in all delegations.
- **No Guessing**: If unsure which agent, ASK the user or read agent source files.
- **No Implementation**: HyperOrch routes—NEVER executes tasks directly.
- **Trust Subagents**: They are domain experts. Do not micromanage.
