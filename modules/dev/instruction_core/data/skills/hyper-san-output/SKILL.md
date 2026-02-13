---
name: hyper-san-output
description: "HyperSan output contract for direct and subagent contexts. Defines severity and difficulty matrices, required issue fields, JSON schema for subagent mode, structured conversational output for direct mode, pass criteria, and fix recommendation rules. Use this skill when producing HyperSan review results, parsing HyperSan output, or implementing sanity check workflows."
---

# HyperSan Output Format

Standardized output format for HyperSan sanity checks, enabling consistent parsing by other agents and actionable results for direct users.

## When to Use
- Producing HyperSan review output (as HyperSan)
- Parsing HyperSan results (as a consuming agent like HyperArch or HyperOrch)
- Implementing sanity check workflows that follow the HyperSan contract
- Understanding severity/difficulty classification for issues

---

## Output Mode Detection

HyperSan MUST detect its invocation context:
- **SUBAGENT mode**: Called via `runSubagent` by another agent (e.g., HyperArch) → output JSON only
- **DIRECT mode**: User interacting directly in chat → output structured conversational format

---

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
| `HARD` | Architectural changes, major refactoring, 3+ modules | Fix for `BLOCKER` only |

## Difficulty Reasoning (Required)

Each issue MUST include a brief explanation of why it's classified at that difficulty:
- **EASY**: "single-line config change", "rename variable", "add missing import"
- **MEDIUM**: "update 2 files with consistent changes", "refactor method signature"
- **HARD**: "requires redesigning module interface", "affects 4+ downstream consumers"

---

## Pass Criteria

HyperSan returns `passed: true` when:
- No `BLOCKER` issues exist, OR
- All `BLOCKER` issues have been addressed

---

## Output Formats

See [output-schema.md](references/output-schema.md) for the complete JSON schema (subagent mode) and structured conversational format (direct mode) with field definitions and examples.

---

## Critical Rules

- **SUBAGENT mode**: Output ONLY valid JSON with NO surrounding text.
- **DIRECT mode**: Use the structured conversational format with severity/difficulty tags.
- **Every issue** MUST have `severity`, `difficulty`, and `difficulty_reason`.
- **fix_suggested** is determined by the severity × difficulty matrix — not subjective judgment.
- **fix_hint** is required when `fix_suggested` is `true`.
