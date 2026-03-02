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
For each participant (sequentially), delegate position statement.
→ See [delegation-blocks.md](assets/delegation-blocks.md) for PROPOSE delegation YAML

Collect all positions. Identify agreements and divergences.
Report summary of positions to user with table.

- Highlight each agent's position.
- Highlight agreed points.
- Highlight divergent views for next phase.

### 3. CHALLENGE Phase
For each participant (sequentially), delegate response to divergent position.
→ See [delegation-blocks.md](assets/delegation-blocks.md) for CHALLENGE delegation YAML

Collect all challenges. Note any shifts in position.
Report summary of challenges to user with table.

- Highlight how each agent responded to divergences.
- Note any position changes or reinforced stances.

### 4. SYNTHESIZE Phase
HyperOrch drafts synthesis:
- Identify common ground
- Propose resolution for divergences
- Draft consensus statement
- **If outcome diverges from human's original proposal**: Include an Intent Interpretation block (see Output Format) in the synthesis draft. State what the agents believe the human intended, why they diverged, and list assumptions for the human to validate. This is mandatory — the human cannot catch agent misunderstandings without it.

Present to all participants for ACCEPT/REJECT vote.
→ See [delegation-blocks.md](assets/delegation-blocks.md) for SYNTHESIZE delegation YAML

### 5. Evaluate Exit Condition
- **All ACCEPT**: Exit with consensus
- **Any REJECT**: Increment round, return to PROPOSE phase (max 3 rounds)
- **Max rounds reached**: Exit with impasse summary

## Output Format

### Consensus Reached
Template for presenting discussion consensus with key points and intent interpretation:
→ See [consensus-output-template.md](assets/consensus-output-template.md)

### Impasse
Template for presenting discussion impasse when max rounds (3) reached without consensus:
→ See [impasse-output-template.md](assets/impasse-output-template.md)

## Post-Discussion Actions

### Discussion Record Creation
After the discussion workflow concludes (consensus OR impasse), HyperOrch MUST hand off to HyperDream to create a discussion record.
→ See [delegation-blocks.md](assets/delegation-blocks.md) for the post-discussion handoff YAML

## Critical Rules
- **Max 3 Rounds**: Hard cap. No exceptions.
- **Sequential Execution**: One agent at a time to prevent crosstalk.
- **No HyperOrch Voting**: Orchestrator facilitates, does not vote.
- **Summary Discipline**: Each phase summary max 1000 chars.
- **Intent Transparency**: When agents reject or modify the human's original proposal, the conclusion MUST include an explicit interpretation of the human's intent and reasoning for divergence. Omitting this is a defect — the human cannot catch misunderstandings without it. Common misalignment causes to check: scale mismatch, over/under-engineering, unknown tools or libraries, missing context, domain assumptions.
