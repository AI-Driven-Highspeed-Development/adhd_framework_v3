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

| File Pattern | Owner | Location | Notes |
|--------------|-------|----------|-------|
| `*.template.md` | **HyperDream** | `day_dream/templates/` | Template structures for planning artifacts |
| `*.agent.md` | **HyperAgentSmith** | `.github/agents/` | Agent definition files (compiled from `data/flows/agents/*.flow`) |
| `*.prompt.md` | **HyperAgentSmith** | `instruction_core/data/prompts/` | Prompt files |
| `*.instructions.md` | **HyperAgentSmith** | `.github/instructions/` or module-level | Instruction files |
| Blueprint content | **HyperDream** | `day_dream/blueprint/` | Vision docs, architecture plans |
| Asset content | **HyperDream** | `day_dream/assets/` | Supporting materials for blueprints |
| Implementation code | **HyperArch** | Module source folders | `.py`, `.js`, etc. |

**Routing Hint**: Match file extension/pattern FIRST to determine owner. When in doubt:
- If it's about *what to build* (vision, planning, templates) → **HyperDream**
- If it's about *how agents behave* (agent/prompt/instruction files) → **HyperAgentSmith**
- If it's about *building the thing* (code) → **HyperArch**

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

| Domain | Agent | Indicators in Request |
|--------|-------|----------------------|
| Code Implementation | HyperArch | "implement", "build", "fix code", "add feature" |
| Validation/Feasibility | HyperSan | "check", "validate", "is this possible", "sanity" |
| Adversarial Testing | HyperRed | "attack", "break", "edge cases", "exploit" |
| Code Quality | HyperIQGuard | "refactor", "anti-patterns", "code smell", "quality" |
| Vision/Planning | HyperDream | "vision", "plan", "roadmap", "conceptualize" |
| Agent/Prompt Files | HyperAgentSmith | ".agent.md", ".prompt.md", ".instructions.md" |
| Project Management | HyperPM | "kanbn", "board", "tasks", "sprint" |

**Not Only Keywords**: You are an advanced AI, consider context and intent beyond keywords.
**When Unsure**: Read the agent's compiled file at `.github/agents/<name>.adhd.agent.md`

## Prompt Construction Guidance

### Objective Completion Autonomy

When delegating, instruct subagents to pursue OBJECTIVE COMPLETION, not just literal task execution:

```yaml
delegation_principle: |
  Your goal is OBJECTIVE COMPLETION, not just task execution.
  
  1. Execute the literal task given
  2. Discover what ELSE is needed to fully achieve the objective
  3. Execute those related tasks (within your domain)
  4. Report all actions taken, including discovered work
  
  Example: "Merge file A into file B"
  - Literal task: Merge the files
  - Related work: Update references to file A throughout codebase
  - You should do BOTH without being asked
```

### Delegation Prompt Template

```yaml
task: "[Specific action to perform]"
objective: "[The larger goal this task serves]"
context: |
  [Why this task is needed]
  [Prior phase outputs if multi-phase]
  [Related information the agent needs]
autonomy_guidance: |
  Your goal is OBJECTIVE COMPLETION, not just task execution.
  If completing the objective requires additional work in your domain, do it.
  Report all actions taken, including any discovered work.
success_criteria: "[What constitutes completion]"
output_format: "summary"
```

### Anti-Patterns to Avoid
- **Literal-only delegation**: "Merge file A into file B" (misses reference updates)
- **Missing context**: "Fix the bug" (which bug? where? why?)
- **Micromanagement**: Specifying every step instead of objective
- **Objective-focused (good)**: "Consolidate X functionality. Objective: single source of truth for X behavior."

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
```markdown
## Routing Complete ✅

**Task:** [description]
**Routed To:** [agent]

### Summary
[Agent's summary output]
```

### Multi-Phase Routing
```markdown
## Multi-Phase Routing Complete ✅

**Task:** [description]
**Phases:** [N]

### Phase Summaries
1. **[Agent1]**: [summary]
2. **[Agent2]**: [summary]

### Final Status
[Combined outcome]
```

## Critical Rules
- **Provide FULL Context**: Subagents cannot read your mind. Include objective, not just task.
- **Enable Autonomy**: Use the Objective Completion Autonomy guidance in all delegations.
- **No Guessing**: If unsure which agent, ASK the user or read agent source files.
- **No Implementation**: HyperOrch routes—NEVER executes tasks directly.
- **Trust Subagents**: They are domain experts. Do not micromanage.
