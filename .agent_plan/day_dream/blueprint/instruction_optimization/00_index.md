# 🎯 Instruction System Optimization: Project Blueprint

> *Taming context windows through intelligent instruction layering, budget-aware compilation, and platform-agnostic architecture*

**Document Type:** Technical Design Document / Project Blueprint  
**Version:** 1.0  
**Created:** 2026-02-09  
**Status:** 📐 Planning

---

## 📊 Progress Overview

| Phase | Status | Notes |
|-------|--------|-------|
| P0: Code Quality + Skill Discovery | ⏳ | Agent/prompt cleanup + SKILLS_INDEX.md generation |
| P1: Platform Profiles | ⏳ | VS Code platform profiles (good to have) |
| P2: Future | 🚫 | Deferred (line limits, token budgets, audit tool cut from this blueprint) |

### Status Legend

| Icon | Meaning |
|------|---------|
| ⏳ | TODO |
| 🔄 | WIP |
| ✅ | DONE |
| 🚫 | CUT |

---

## 📐 Planning Standards

This blueprint follows **HyperDream phasing rules**:

| Principle | Meaning |
|-----------|---------|
| **Walking Skeleton First** | Phase 0 proves plumbing works with hardcoded stubs |
| **Difficulty Honesty** | Each item labeled `[KNOWN]`, `[EXPERIMENTAL]`, or `[RESEARCH]` |
| **Research ≠ Foundation** | `[RESEARCH]` items never in Phase 0 |
| **Incremental Value** | Each phase delivers usable functionality |

---

## 📑 Document Index

| # | Document | Required | Purpose (When to Read) |
|---|----------|----------|------------------------|
| 00 | [Index](./00_index.md) | ✓ | **Navigation hub** — Start here if lost |
| 01 | [Executive Summary](./01_executive_summary.md) | ✓ | **Vision & scope** — Read to understand what/why |
| 02 | [Architecture](./02_architecture.md) | ✓ | **System design** — Read to understand how pieces fit |
| 03 | [Feature: Code Quality Fixes](./03_feature_code_quality_fixes.md) | ✓ | **P0** — Agent/prompt refactoring and cleanup |
| 05 | [Feature: VS Code Platform Profiles](./05_feature_vscode_platform_profiles.md) | | **P1** — Platform-agnostic core schema (good to have) |
| 06 | [Feature: Skill Discovery Index](./06_feature_skill_discovery_index.md) | ✓ | **P0** — Compiled SKILLS_INDEX.md manifest |
| 80 | [Implementation](./80_implementation.md) | ✓ | **Task tracking** — Read to start/track work |

---

## 💭 Vision Statement

> *"Improve instruction discoverability through a compiled skill index. Optionally support platform-agnostic architecture for export scenarios."*

**Revised Scope (2026-02-09):** Focus narrowed to skill discovery and optional platform profiles. Line limits, token budgets, and audit tooling cut as overkill for current needs.

---

## 🧭 How to Navigate This Blueprint

### Reading Order Decision Tree

```mermaid
flowchart TD
    START[📚 You are here] --> Q1{What do you need?}
    
    Q1 -->|"Understand the project"| PATH_UNDERSTAND
    Q1 -->|"Implement P0"| PATH_IMPL
    Q1 -->|"Review/approve"| PATH_REVIEW
    
    PATH_UNDERSTAND[🎯 Understanding Path]
    PATH_UNDERSTAND --> ES[01 - Executive Summary]
    ES --> ARCH[02 - Architecture]
    ARCH --> F06[06 - Skill Index]
    
    PATH_IMPL[🔧 Implementation Path]
    PATH_IMPL --> IMPL[80 - Implementation]
    IMPL --> F06B[06 - Skill Index]
    F06B --> F05[05 - VS Code Profiles]
    
    PATH_REVIEW[✅ Review Path]
    PATH_REVIEW --> ES2[01 - Executive Summary]
    ES2 --> IMPL2[80 - Implementation]
```

### Document Purpose Quick Reference

| Doc | When to Read | One-Line Purpose |
|-----|--------------|------------------|
| **00 - Index** | First visit, lost | Navigation hub, project overview |
| **01 - Exec Summary** | Deciding whether to work on this | Goals, non-goals, scope |
| **02 - Architecture** | Understanding system design | Components, data flow, boundaries |
| **05 - VS Code Profiles** | Platform separation (P1) | Core vs platform-specific schema |
| **06 - Skill Index** | Building discovery manifest (P0) | SKILLS_INDEX.md compilation |
| **80 - Implementation** | Starting work | Phased tasks, checklists |

---

## [Custom] 🎨 Feature Dependencies

```mermaid
flowchart LR
    subgraph P0["P0: Immediate"]
        F06[Skill Discovery Index]
    end
    
    subgraph P1["P1: Good to Have"]
        F05[VS Code Platform Profiles]
    end
    
    F06 -.->|informs| F05
```

### Cut Features (2026-02-09)

| Feature | Reason |
|---------|--------|
| Line Limit Enforcement | Overkill for current needs |
| Token Budget Annotations | Overkill for current needs |
| Instruction Audit Tool | Good but not immediate priority |

---

**← Navigation:** [Executive Summary](./01_executive_summary.md) | [Implementation](./80_implementation.md)
