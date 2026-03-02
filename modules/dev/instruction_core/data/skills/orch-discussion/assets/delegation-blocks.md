# Discussion Delegation Blocks

All delegation YAML blocks used by HyperOrch during discussion workflow.

## PROPOSE Phase

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

## CHALLENGE Phase

For each participant (sequentially):

```yaml
task: "Respond to this divergent position: [most opposing view]"
context: "[All positions from PROPOSE phase]"
success_criteria: "Address the specific divergence with reasoning"
output_format: "summary"
```

## SYNTHESIZE Phase

Present synthesis to all participants:

```yaml
task: "Do you ACCEPT or REJECT this synthesis: [synthesis]"
context: "[Key points from prior phases]"
success_criteria: "Reply with ACCEPT or REJECT with brief reason"
output_format: "summary"
```

## Post-Discussion Handoff (HyperDream)

After discussion concludes (consensus OR impasse):

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
