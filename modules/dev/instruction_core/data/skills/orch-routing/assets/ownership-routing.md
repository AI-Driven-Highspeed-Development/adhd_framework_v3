# Document Ownership Routing Table

| File Pattern | Owner | Location | Notes |
|--------------|-------|----------|-------|
| `*.template.md` | **HyperDream** | `.github/skills/dream-routing/assets/` | Template structures for planning artifacts |
| `*.agent.md` | **HyperAgentSmith** | `.github/agents/` | Agent definition files (compiled from `data/flows/agents/*.flow`) |
| `*.prompt.md` | **HyperAgentSmith** | `instruction_core/data/prompts/` | Prompt files |
| `*.instructions.md` | **HyperAgentSmith** | `.github/instructions/` or module-level | Instruction files |
| Blueprint content | **HyperDream** | `day_dream/blueprint/` | Vision docs, architecture plans |
| Asset content | **HyperDream** | `day_dream/assets/` | Supporting materials for blueprints |
| Implementation code | **HyperArch** | Module source folders | `.py`, `.js`, etc. |

## Routing Hint

Match file extension/pattern FIRST to determine owner. When in doubt:
- If it's about *what to build* (vision, planning, templates) → **HyperDream**
- If it's about *how agents behave* (agent/prompt/instruction files) → **HyperAgentSmith**
- If it's about *building the thing* (code) → **HyperArch**
