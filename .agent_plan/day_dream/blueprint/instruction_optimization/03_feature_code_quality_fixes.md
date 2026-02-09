# 03 - Feature: Code Quality Fixes

> Part of [Instruction System Optimization Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌───────────────────────────────────────────────────────────────┐
│  Agent files have accumulated cruft:                          │
│  • Duplicated content that belongs in skills                  │
│  • Verbose sections that could be condensed                   │
│  • Missing VS Code v1.109 fields                              │
└───────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Context window | 🔥🔥🔥 High | Every agent call |
| Maintainability | 🔥🔥 Medium | Each agent update |

### ✨ The Vision

```
After This Feature:
┌───────────────────────────────────────────────────────────────┐
│  ✅ Duplicates moved to skills (single source of truth)       │
│  ✅ Verbose sections condensed (-60+ lines total)             │
│  ✅ VS Code v1.109 fields added for modern features           │
└───────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Refactor agent/prompt files: move duplicates to skills, condense verbose sections, add missing VS Code fields.

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Duplicated content | ~35 lines | 0 (moved to skills) |
| Verbose sections | ~43 lines | ~10 (condensed) |
| VS Code v1.109 compliance | Partial | Full |

---

## 🔧 The Spec

---

## 🎯 Overview

Agent and prompt files have accumulated content that should live elsewhere or be condensed. This feature covers three priorities of cleanup work.

**Priority:** P0  
**Difficulty:** `[KNOWN]`

---

## 📊 User Stories

| As a... | I want... | So that... |
|---------|-----------|------------|
| Agent | Minimal, focused instructions | Context window is used efficiently |
| Maintainer | Single source of truth | Updates don't require multiple edits |
| VS Code user | Modern YAML fields | New platform features work correctly |

---

## ✅ Acceptance Criteria

### Priority 1 — Refactor (Move to Skills)

| Agent | Content to Move | Target Skill | Lines Saved |
|-------|-----------------|--------------|-------------|
| HyperOrch | "Document Ownership Routing Table" | `orch-routing` skill | -15 |
| HyperRed | "Artifact Locations" | `testing` skill | -20 |

**Acceptance:** Content exists in skill, agent references skill.

### Priority 2 — Trim (Condense)

| Agent | Section to Condense | Action | Lines Saved |
|-------|---------------------|--------|-------------|
| HyperArch | Adversarial Awareness + Discovery Checklist | Merge & condense | -8 |
| HyperDream | "Solution Selection" decision tree | Move to skill OR condense | -25 |
| HyperSan | Output Format JSON example | Remove (already in instruction file) | -10 |

**Acceptance:** Information preserved, line count reduced.

### Priority 3 — Polish

| Target | Change | Notes |
|--------|--------|-------|
| HyperAgentSmith | Remove duplicate Edit Locations rule | -1 line |
| All prompts | Add `agent` field | VS Code v1.109 feature |
| HyperOrch YAML | Add `agents` field | Subagent allowlist |
| HyperRed YAML | Add `model` field | Model specification |

**Acceptance:** Fields present, no duplicate rules.

---

## 🗺️ Change Summary

```
Total lines saved: ~79
├── Refactor to skills: -35 lines
├── Condense sections:  -43 lines  
└── Remove duplicate:   -1 line

New YAML fields added: 3
├── agent (all prompts)
├── agents (HyperOrch)
└── model (HyperRed)
```

---

## ✅ Verification (Manual)

| What to Verify | Expected Result |
|----------------|-----------------|
| HyperOrch references `orch-routing` skill | Routing table not duplicated in agent |
| HyperRed references `testing` skill | Artifact locations not duplicated |
| HyperArch agent is shorter | Adversarial + Discovery < 10 lines |
| Prompt YAML has `agent` field | All `.prompt.md` files compliant |
| HyperOrch YAML has `agents` field | Subagent allowlist present |

---

**← Back to:** [Index](./00_index.md) | **Next:** [Architecture](./02_architecture.md)
