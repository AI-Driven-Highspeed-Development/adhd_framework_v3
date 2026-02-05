---
applyTo: "**/hyper_san_checker.adhd.agent.md"
---

# HyperSan Output Format Instructions

## Goals
- Standardize HyperSan output for consistent parsing by other agents.
- Enable efficient machine-readable output for subagent calls.
- Provide actionable fix recommendations based on severity and difficulty.

## Output Mode Detection
HyperSan MUST detect its invocation context:
- **SUBAGENT mode**: Called via `runSubagent` by another agent (e.g., HyperArch).
- **DIRECT mode**: User interacting directly in chat.

## Severity Levels
| Level | Meaning | Action Required |
|-------|---------|-----------------|
| `BLOCKER` | Critical issue preventing implementation | MUST fix before proceeding |
| `WARNING` | Significant concern that should be addressed | SHOULD fix |
| `SUGGESTION` | Minor improvement opportunity | MAY fix |

## Fix Difficulty Levels
| Difficulty | Criteria | Fix Recommendation |
|------------|----------|-------------------|
| `EASY` | Single-line change, config tweak, simple rename | Fix for ALL severity levels |
| `MEDIUM` | Multi-file changes, moderate refactoring | Fix for `WARNING` and `BLOCKER` only |
| `HARD` | Architectural changes, major refactoring, 3+ modules affected | Fix for `BLOCKER` only |

## Difficulty Reasoning (Required)
Each issue MUST include a brief explanation of why it's classified at that difficulty:
- **EASY examples**: "single-line config change", "rename variable", "add missing import"
- **MEDIUM examples**: "update 2 files with consistent changes", "refactor method signature"
- **HARD examples**: "requires redesigning module interface", "affects 4+ downstream consumers"

## SUBAGENT Mode Output (JSON)
When invoked as subagent, output ONLY valid JSON with NO surrounding text:

```json
{
  "status": "VALID|NEEDS_FIX|INVALID",
  "passed": true,
  "issues": [
    {
      "severity": "BLOCKER|WARNING|SUGGESTION",
      "difficulty": "EASY|MEDIUM|HARD",
      "difficulty_reason": "brief explanation why this difficulty",
      "description": "clear issue description",
      "fix_suggested": true,
      "fix_hint": "brief guidance on how to fix"
    }
  ],
  "summary": "one-line summary of overall status"
}
```

### JSON Field Definitions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | Overall status: `VALID` (no issues), `NEEDS_FIX` (has issues), `INVALID` (fundamentally flawed) |
| `passed` | boolean | Yes | `true` if no blockers and implementation can proceed |
| `issues` | array | Yes | List of issues found (empty array if none) |
| `summary` | string | Yes | One-line human-readable summary |

### Issue Object Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `severity` | string | Yes | `BLOCKER`, `WARNING`, or `SUGGESTION` |
| `difficulty` | string | Yes | `EASY`, `MEDIUM`, or `HARD` |
| `difficulty_reason` | string | Yes | Brief explanation of difficulty classification |
| `description` | string | Yes | Clear description of the issue |
| `fix_suggested` | boolean | Yes | Whether a fix is recommended based on severity+difficulty matrix |
| `fix_hint` | string | If fix_suggested | Brief guidance on how to resolve |

## DIRECT Mode Output (Conversational)
When user interacts directly, use structured conversational format:

```
**Status**: VALID | NEEDS_CLARIFICATION | SUGGEST_ALTERNATIVE | INVALID

**Goal**: [What user is trying to achieve]

**Issues Found**:
- [BLOCKER][EASY] Description (Reason: single-line fix)
  → **Fix**: guidance
- [WARNING][MEDIUM] Description (Reason: 2 files affected)
  → **Fix**: guidance
- [SUGGESTION][HARD] Description (Reason: requires API redesign)
  → *No fix suggested due to difficulty*

**Summary**: [Brief overall assessment]

**Next Steps**: [Recommended actions or agent handoffs]
```

## Pass Criteria
HyperSan returns `passed: true` when:
- No `BLOCKER` issues exist, OR
- All `BLOCKER` issues have been addressed

## Examples

### Example: Clean Pass (SUBAGENT)
```json
{
  "status": "VALID",
  "passed": true,
  "issues": [],
  "summary": "Sanity Check Passed: LGTM"
}
```

### Example: Issues Found (SUBAGENT)
```json
{
  "status": "NEEDS_FIX",
  "passed": false,
  "issues": [
    {
      "severity": "BLOCKER",
      "difficulty": "EASY",
      "difficulty_reason": "single import statement addition",
      "description": "Missing import for ConfigManager in unity_controller.py",
      "fix_suggested": true,
      "fix_hint": "Add 'from managers.config_manager import ConfigManager' at top of file"
    },
    {
      "severity": "WARNING",
      "difficulty": "MEDIUM",
      "difficulty_reason": "requires updating 2 caller files",
      "description": "Function get_module() lacks type hints",
      "fix_suggested": true,
      "fix_hint": "Add return type annotation and parameter hints"
    },
    {
      "severity": "SUGGESTION",
      "difficulty": "HARD",
      "difficulty_reason": "would require refactoring module interface used by 5 consumers",
      "description": "Consider using dependency injection for better testability",
      "fix_suggested": false,
      "fix_hint": null
    }
  ],
  "summary": "1 blocker, 1 warning, 1 suggestion found. Fix blocker before proceeding."
}
```
