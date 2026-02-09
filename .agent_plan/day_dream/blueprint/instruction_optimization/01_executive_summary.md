# 01 - Executive Summary

> Part of [Instruction System Optimization Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌────────────────────────────────────────────────────────────────┐
│  Skills exist but hard to discover                          │
│  No central index, must grep through files manually         │
│  "When NOT to use" guidance buried in individual files      │
└────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------||
| AI Agent (skill selection) | 🔥🔥🔥 High | Every request |
| Developer (finding skills) | 🔥🔥 Medium | When building agents |

### ✨ The Vision

```
After This Feature:
┌────────────────────────────────────────────────────────────────┐
│  Agent needs skill  ────►  ✅ SKILLS_INDEX.md lookup          │
│                                                                │
│  "When to use" + "When NOT to use" in single manifest          │
└────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> Generate a compiled SKILLS_INDEX.md manifest for easy skill discovery, with optional platform profile support for exports.

---

## 🔧 The Spec

---

## 🌟 TL;DR

Skills are hard to discover without grepping through individual SKILL.md files. We add a compiled SKILLS_INDEX.md manifest that includes descriptions, "when to use", and "when NOT to use" guidance. Platform profiles are a nice-to-have for export scenarios.

---

## 🎯 Problem Statement

Skills exist but lack centralized discoverability. Developers and agents must manually search through `.github/skills/*/SKILL.md` files to find relevant capabilities. "When NOT to use" guidance is buried in individual files, leading to suboptimal skill selection.

---

## 🔍 Prior Art & Existing Solutions

| Library/Tool | What It Does | Decision | License | Rationale |
|--------------|--------------|----------|---------|-----------|
| YAML frontmatter | Structured metadata | WRAP | - | Already used in SKILL.md files |
| markdown-it | Markdown parsing | EVALUATE | MIT | Could extract sections programmatically |
| glob/pathlib | File discovery | WRAP (stdlib) | - | Python stdlib, no external deps |

**Summary:** Parse SKILL.md frontmatter and extract key sections using stdlib where possible.

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Line limit enforcement | Cut: overkill for current needs |
| Token budget tracking | Cut: overkill for current needs |
| Instruction audit tool | Cut: good but not immediate priority |
| Real-time skill recommendations | Future consideration after index exists |
| Auto-generated skill documentation | Index aggregates, doesn't generate |

---

## ✅ Features Overview

| Priority | Feature | Difficulty | Description |
|----------|---------|------------|-------------|
| P0 | Code Quality Fixes | `[KNOWN]` | Agent/prompt refactoring: move duplicates to skills, condense, add VS Code fields |
| P0 | Skill Discovery Index | `[KNOWN]` | Compiled SKILLS_INDEX.md with "when to use" and "when NOT to use" |
| P1 | VS Code Platform Profiles | `[KNOWN]` | Split schema: core + optional vscode profile (good to have for exports) |

### Cut Features (2026-02-09)

| Feature | Reason |
|---------|--------|
| Line Limit Enforcement | Overkill for current needs |
| Token Budget Annotations | Overkill for current needs |
| Instruction Audit Tool | Good but not immediate priority |
| Flow Fragment Versioning | Premature optimization |
| Behavioral Compliance Testing | Research-grade, no immediate need |

→ See individual Feature Docs for details.

---

## [Custom] 🎨 Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Skill discoverability | Manual grep | Single SKILLS_INDEX.md file |
| "When NOT to use" visibility | Buried in files | Extracted in index |
| Platform assumptions in core | ~12 references | 0 (with profiles enabled) |

---

## [Custom] 📊 Related User Focus Areas

This blueprint complements the user's broader work:

- **FLOW system utilization** — Better leverage existing flows
- **VS Code v1.109 features** — Adopt new platform capabilities
- **Agent/prompt quality** — Now included in P0 (Code Quality Fixes feature)

---

**← Back to:** [Index](./00_index.md) | **Next:** [Architecture](./02_architecture.md)
