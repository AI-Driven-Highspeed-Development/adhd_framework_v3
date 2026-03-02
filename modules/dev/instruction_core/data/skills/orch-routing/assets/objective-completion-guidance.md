# Objective Completion Autonomy

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

### Anti-Patterns to Avoid
- **Literal-only delegation**: "Merge file A into file B" (misses reference updates)
- **Missing context**: "Fix the bug" (which bug? where? why?)
- **Micromanagement**: Specifying every step instead of objective
- **Objective-focused (good)**: "Consolidate X functionality. Objective: single source of truth for X behavior."
