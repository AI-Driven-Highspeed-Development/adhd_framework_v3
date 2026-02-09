# 01 - Executive Summary

> Part of [Instruction System Optimization Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌────────────────────────────────────────────────────────────────┐
│  Agent compiles  ──────►  💥 TOKEN EXPLOSION 💥                │
│                                                                │
│  Because: No budget visibility, no conflict detection,         │
│           no line enforcement, VS Code assumptions everywhere  │
└────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| AI Agent (context window) | 🔥🔥🔥 High | Every request |
| Developer (debugging) | 🔥🔥🔥 High | Daily |
| Framework (portability) | 🔥🔥 Medium | On export |

### ✨ The Vision

```
After This Feature:
┌────────────────────────────────────────────────────────────────┐
│  Agent compiles  ──────►  ✅ LEAN, OBSERVABLE, PORTABLE        │
│                                                                │
│  Flow: validate lines → sum budgets → detect conflicts → emit  │
└────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Bring observability and discipline to instruction compilation through line limits, token budgets, conflict detection, and platform-agnostic architecture.

---

## 🔧 The Spec

---

## 🌟 TL;DR

The instruction system lacks visibility into token costs and conflict detection. We add automated line enforcement (≤100 lines), token budget annotations, a skill discovery manifest, and an audit tool—while splitting VS Code-specific features into optional profiles.

---

## 🎯 Problem Statement

Compiled agents can silently exceed context budgets. Instructions from multiple sources can conflict without detection. Platform-specific features (VS Code tool syntax, model declarations) are baked into the core schema, hurting portability. Developers have no visibility into what instructions co-activate or their cumulative token cost.

---

## 🔍 Prior Art & Existing Solutions

| Library/Tool | What It Does | Decision | License | Rationale |
|--------------|--------------|----------|---------|-----------|
| `tiktoken` | OpenAI token counting | WRAP | MIT | Accurate for OpenAI models |
| `anthropic-tokenizer` | Claude token counting | EVALUATE | - | May use for Claude-specific counts |
| ESLint-style validators | Static analysis | BUILD | - | Custom rules for ADHD schema |
| JSON Schema | Validation | WRAP | - | Already in use, extend profiles |

**Summary:** Wrap `tiktoken` for token counting, build custom validation for ADHD-specific rules.

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Runtime content deduplication | Deferred until orchestration layer matures |
| Multi-model token budget optimization | One model at a time; Claude first |
| Auto-fixing line limit violations | Validation only; editing is human/agent task |
| Real-time streaming budget tracking | Phase 2+ concern |

---

## ✅ Features Overview

| Priority | Feature | Difficulty | Description |
|----------|---------|------------|-------------|
| P0 | Line Limit Enforcement | `[KNOWN]` | All compiled agents ≤100 lines, validated at compile time |
| P0 | Token Budget Annotations | `[KNOWN]` | Flow fragments declare `<!-- tokens: ~N -->` |
| P0 | VS Code Platform Profiles | `[KNOWN]` | Split schema: core + optional vscode profile |
| P0 | Skill Discovery Index | `[KNOWN]` | Compiled SKILLS_INDEX.md with "when NOT to use" hints |
| P0 | Instruction Audit Tool | `[KNOWN]` | MCP/CLI showing co-activating instructions + conflicts |
| P1 | Flow Fragment Versioning | `[EXPERIMENTAL]` | Version tracking when flow count >20 |
| P2 | Behavioral Compliance Testing | `[RESEARCH]` | After observability infrastructure |

→ See individual Feature Docs for details.

---

## [Custom] 🎨 Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Compiled agent line count | Unbounded | ≤100 lines |
| Token cost visibility | 0% | 100% of fragments annotated |
| Conflict detection | None | All co-activations visible |
| Platform assumptions in core | ~12 references | 0 |
| Skill discoverability | Manual search | Single index file |

---

## [Custom] 📊 Token Budget Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│  BUDGET MODEL                                               │
│                                                             │
│  fragment_budget = declared_tokens + 10% buffer             │
│  agent_budget = Σ(fragment_budgets) + base_agent_cost       │
│  session_budget = active_agent + active_skills + context    │
│                                                             │
│  WARNING threshold: 70% of model context                    │
│  ERROR threshold: 90% of model context                      │
└─────────────────────────────────────────────────────────────┘
```

---

**← Back to:** [Index](./00_index.md) | **Next:** [Architecture](./02_architecture.md)
