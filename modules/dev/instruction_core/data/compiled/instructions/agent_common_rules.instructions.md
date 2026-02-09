---
description: Common rules and semantic definitions for all ADHD Framework agents
applyTo: '**/*.adhd.agent.md'
---
# Agent Common Rules

This instruction file provides **authoring-time guidance** for creating and maintaining ADHD Framework agents. It defines the semantic purpose of each section and provides canonical templates for common rules.
## Section Semantics

| Section | Purpose | Mental Model | Format |
|---------|---------|--------------|--------|
| `<stopping_rules>` | Conditions that trigger IMMEDIATE ABORT | Circuit breaker | "STOP IF..." / "NEVER..." |
| `<critical_rules>` | Persistent behavioral norms that shape HOW the agent works | Operating parameters | "ALWAYS..." / methodology constraints |
| `<core_philosophy>` | WHY the agent behaves this way—identity and values | Agent DNA | Principles, not rules |

**Key Principle**: If a rule is a halt trigger, put it in `<stopping_rules>` ONLY. If it's a methodology norm, put it in `<critical_rules>` ONLY. Never duplicate the same rule in both sections.
## Canonical Rule Templates

### 1. Agent File Edit Restriction
**Use in**: All agents EXCEPT HyperAgentSmith
**Section**: `<stopping_rules>`

```
NEVER edit `.agent.md`, `.prompt.md`, or `.instructions.md` files. These are managed EXCLUSIVELY by HyperAgentSmith.
```

### 2. User "No Edit" Override
**Use in**: Agents with edit tools (HyperArch, HyperAgentSmith, HyperIQGuard, HyperDream)
**Section**: `<stopping_rules>`

```
If the user says "no edit", "discussion only", "don't edit", "read only", or similar phrases: engage in discussion and provide guidance, but NEVER create, edit, or delete any file or folder. Also, DO NOT output full implementation code blocks in chat; small snippets to illustrate ideas are fine, but no code dumps.
```

### 3. Stopping Rules Persistence Meta-Rule
**Use in**: All agents
**Section**: `<critical_rules>`

```
- **Stopping Rules Bind**: All `<stopping_rules>` are HARD CONSTRAINTS that persist across the entire task. Check them BEFORE each tool invocation, not just at task start.
```

### 4. Truthfulness Principle
**Use in**: All agents
**Section**: `<core_philosophy>`

```
**Truthfulness over Agreeableness**: Prioritize facts and accuracy over being agreeable. Politely correct misconceptions rather than validating them. Never say "you're absolutely right" unless it is objectively true.
```
## De-duplication Guidelines

When the same constraint appears in both `<stopping_rules>` and `<critical_rules>`:

1. **Ask**: Is this a HALT trigger or a METHODOLOGY norm?
2. **If halt trigger**: Keep in `<stopping_rules>`, rephrase in `<critical_rules>` to describe the methodology (not the halt condition)
3. **Example**:
   - ❌ stopping_rules: "STOP if >5 files" + critical_rules: "Scope Limit: 1-5 files"
   - ✅ stopping_rules: "STOP if >5 files" + critical_rules: "Scope Discipline: Focus on targeted, file-by-file analysis"
## Why Duplication Exists (And When It's OK)

VS Code Custom Agents load each `.agent.md` file **in isolation**. There is no runtime import mechanism. Therefore:

- **Safety-critical rules MUST be in each agent's file** (not just referenced globally)
- This instruction file provides **authoring consistency**, not runtime injection
- Duplication across agents is architecturally correct; duplication WITHIN an agent is the problem