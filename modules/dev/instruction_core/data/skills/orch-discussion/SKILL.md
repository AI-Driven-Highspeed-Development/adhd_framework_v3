---
name: orch-discussion
description: "Orchestrator discussion preset — structured multi-agent discussion protocol for collaborative problem solving. Coordinates N-way discussions between specialist agents through Propose, Challenge, and Synthesize phases to reach consensus. Use this skill when facilitating multi-agent discussions, debates, design evaluations, or collaborative analysis requiring multiple perspectives."
---

# HyperOrch Discussion Preset

## Goals
- Facilitate structured N-way discussions between agents
- Reach consensus through Propose → Challenge → Synthesize phases
- Handle impasse gracefully with clear documentation

## When This Applies
Trigger patterns: "discuss", "debate", "compare", "n-way", "what should we", "which approach"

## Discussion Protocol

### Identification

1. **TOPIC**: Extract the main topic from the user request. This is the subject all participants will discuss.
2. **PARTICIPANTS**: Identify which agents should participate based on the topic. For discussions without participants:
    - If user said "auto-invite" or "auto" → Infer relevant agents from topic, proceed without asking
    - Otherwise → Propose participant list, wait for user confirmation before proceeding, advice user to use "auto-invite" for next time if want to skip the confirmation step.

### Phase Structure
Each discussion round has 3 phases:
1. **PROPOSE**: Each participant states their position (1-3 sentences)
2. **CHALLENGE**: Each participant responds to ONE divergent view
3. **SYNTHESIZE**: HyperOrch drafts consensus, participants confirm or reject

### Execution Flow

```
Round N (max 3):
  PROPOSE → All agents state position (sequential)
  CHALLENGE → Agents respond to divergences (sequential)
  SYNTHESIZE → Draft consensus
    → All ACCEPT? → Exit with consensus
    → Disagreement? → Next round
    → Max rounds hit? → Exit with impasse
```

## Orchestration Steps

### 1. Initialize Discussion
- Parse topic from user request
- Identify participants (default: HyperArch, HyperSan if not specified)
- Maximum 4 participants per discussion
- State: "Starting discussion on: [topic] with [participants]"

### 2. PROPOSE Phase
For each participant (sequentially):
```yaml
task: "State your position on: [topic]"
objective: "[The larger goal this discussion serves]"
context: "[Prior round summary if any]"
autonomy_guidance: |
  Your goal is OBJECTIVE COMPLETION, not just answering the question.
  If your expertise reveals related considerations, include them.
  Report all insights, including any discovered concerns.
success_criteria: "Provide 1-3 sentence position statement"
output_format: "summary"
```

Collect all positions. Identify agreements and divergences.
Report summary of positions to user with table.

- Highlight each agent's position.
- Highlight agreed points.
- Highlight divergent views for next phase.

### 3. CHALLENGE Phase
For each participant (sequentially):
```yaml
task: "Respond to this divergent position: [most opposing view]"
context: "[All positions from PROPOSE phase]"
success_criteria: "Address the specific divergence with reasoning"
output_format: "summary"
```

Collect all challenges. Note any shifts in position.
Report summary of challenges to user with table.

- Highlight how each agent responded to divergences.
- Note any position changes or reinforced stances.

### 4. SYNTHESIZE Phase
HyperOrch drafts synthesis:
- Identify common ground
- Propose resolution for divergences
- Draft consensus statement

Present to all participants:
```yaml
task: "Do you ACCEPT or REJECT this synthesis: [synthesis]"
context: "[Key points from prior phases]"
success_criteria: "Reply with ACCEPT or REJECT with brief reason"
output_format: "summary"
```

### 5. Evaluate Exit Condition
- **All ACCEPT**: Exit with consensus
- **Any REJECT**: Increment round, return to PROPOSE phase (max 3 rounds)
- **Max rounds reached**: Exit with impasse summary

## Output Format

### Consensus Reached
```markdown
## Discussion Summary

**Topic:** [topic]
**Participants:** [list]
**Rounds:** [N]
**Status:** Consensus ✅

### Final Synthesis
[Agreed position]

### Key Points
| Agent | Final Position | Vote |
|-------|----------------|------|
| [name] | [position] | ACCEPT |
```

### Impasse
```markdown
## Discussion Summary

**Topic:** [topic]
**Participants:** [list]
**Rounds:** 3 (max reached)
**Status:** Impasse ⚠️

### Divergent Positions
| Agent | Final Position |
|-------|----------------|
| [name] | [position] |

### Recommendation
[HyperOrch's suggested path forward]
```

## Post-Discussion Actions

### Discussion Record Creation
After the discussion workflow concludes (consensus OR impasse), HyperOrch MUST:

1. **Handoff to HyperDream**: Call HyperDream to create a discussion record file
2. **Location**: Records are stored in `.agent_plan/discussion/`
3. **Content**: Pass the complete discussion summary (topic, participants, rounds, outcome, key positions) to HyperDream
4. **Naming**: HyperDream determines the appropriate filename based on topic and date

```yaml
handoff_template:
  to: HyperDream
  task: "Create a discussion record for the completed discussion"
  context: "[Full discussion summary from Output Format section]"
  output_path: ".agent_plan/discussion/"
  filename_pattern: "[YYYY-MM-DD]_[hh:mm]_[topic_slug]_discussion_record.md"
  success_criteria: "Discussion record file created with all key information preserved"
  header_metadata:
    topic: "[topic]"
    datetime: "[YYYY-MM-DD hh:mm]"
    participants: "[list]"
    rounds: "[N]"
    status: "[Consensus or Impasse]"
  header_format: "markdown table"
```

> **Note**: HyperDream is responsible for writing/creating the actual file. HyperOrch only initiates the handoff.

## Critical Rules
- **Max 3 Rounds**: Hard cap. No exceptions.
- **Sequential Execution**: One agent at a time to prevent crosstalk.
- **No HyperOrch Voting**: Orchestrator facilitates, does not vote.
- **Summary Discipline**: Each phase summary max 1000 chars.
