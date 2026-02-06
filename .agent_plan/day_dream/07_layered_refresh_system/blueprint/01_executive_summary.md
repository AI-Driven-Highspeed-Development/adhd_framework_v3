# 01 - Executive Summary

> Part of [Layered Refresh System Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain

```
Current Reality:
┌──────────────────────────────────────────────────────────────────┐
│  adhd refresh  ──────►  Runs ALL modules in DISCOVERY ORDER  💥  │
│                                                                  │
│  Because: No dependency awareness, no ordering guarantee,        │
│           no distinction between light and heavy refresh work    │
└──────────────────────────────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Framework Developer | 🔥🔥🔥 High | Every refresh (multiple times daily) |
| Module Author | 🔥🔥 Medium | When adding new modules with deps |

### ✨ The Vision

```
After This Feature:
┌──────────────────────────────────────────────────────────────────┐
│  adhd refresh  ──────►  ✅ Correct dependency order              │
│                                                                  │
│  Flow: topo-sorted by declared deps                              │
│        (exceptions_core → logger_util → config_manager → ...)    │
│        Light refresh.py runs always                              │
│        Heavy refresh_full.py runs on --full only                 │
└──────────────────────────────────────────────────────────────────┘
```

### 🎯 One-Liner

> We're building a dependency-ordered refresh system with tiered scripts so framework developers get correct execution order and can separate light from heavy refresh work.

---

## 🔧 The Spec

---

## 🌟 TL;DR

The refresh system will execute modules in pure dependency order using `graphlib.TopologicalSorter` on declared `pyproject.toml` dependencies. Each module can optionally provide `refresh.py` (light refresh) and/or `refresh_full.py` (heavy, on `--full` only). Both scripts are optional — most modules won't have either, and missing scripts are silently skipped. No new config formats — everything discovered from existing fields and filename conventions.

---

## 🎯 Problem Statement

Today, `adhd refresh` iterates over all discovered modules and runs their `refresh.py` scripts in filesystem discovery order. This has two problems:

1. **No ordering guarantee** — A module may refresh before its dependencies, causing stale or broken state.
2. **No tiered refresh** — A single `refresh.py` must contain both quick sync operations and expensive rebuild operations. There's no way to run just the light stuff vs everything.

The workaround is manually running individual refresh scripts or hoping discovery order happens to be correct. Neither scales.

---

## 🔍 Prior Art & Existing Solutions

| Library/Tool | What It Does | Decision | License | Rationale |
|--------------|--------------|----------|---------|-----------|
| `make` / `ninja` | Dependency-aware incremental builds | WRAP (concept) | Various | We borrow the dependency ordering concept but don't introduce a build tool |
| `tox` / `nox` | Multi-environment test runners with session deps | REJECT | MIT | Overkill — we need ordering, not venv management |
| Python `graphlib.TopologicalSorter` | Stdlib topo sort (Python 3.9+) | BUILD (use stdlib) | PSF | Zero dependencies, exactly what we need |
| npm lifecycle hooks (`preinstall`, `postinstall`) | Per-package hook scripts with naming conventions | WRAP (concept) | N/A | Inspired tiered script naming via file convention |

**Summary:** We're building custom with stdlib only. The core algorithm is `graphlib.TopologicalSorter` for ordering. Tiered scripts are a naming convention, no library needed.

**Solution Sizing Rationale:** Stdlib `graphlib` covers 100% of ordering needs. Tiered scripts are filename-based discovery (<20 LOC). No external libraries warranted.

---

## ❌ Non-Goals (Explicit Exclusions)

| Non-Goal | Rationale |
|----------|-----------|
| Parallel execution of independent modules | Adds concurrency complexity for unclear benefit. Modules are fast. Defer indefinitely. |
| Staleness/change detection (mtime, hashing, `.refresh_stamp`) | `refresh.py` is a custom script — no generic way to detect when it needs to run. Explicitly ruled out. |
| Remote/distributed refresh | This is a local dev tool. No network awareness needed. |
| Automatic dependency discovery via import scanning | Too fragile. Declared deps in `pyproject.toml` are the source of truth. |
| GUI or web dashboard for refresh status | CLI-only tool. Terminal output is sufficient. |

---

## ✅ Features Overview

| Feature | Difficulty | Description |
|---------|------------|-------------|
| [Dependency Ordering](./03_feature_dependency_ordering.md) | `[KNOWN]` | Pure topological sort by declared `pyproject.toml` dependencies |
| [Tiered Scripts](./04_feature_tiered_scripts.md) | `[KNOWN]` | `refresh.py` (light, always) + `refresh_full.py` (heavy, on `--full`) per module |

→ See individual Feature Docs for details.

---

## 📊 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Refresh order correctness | 100% — deps always refresh before dependents | Manual: verify log output ordering |
| No new dependencies | 0 added to framework `pyproject.toml` | Inspect deps list |
| Implementation size | <200 LOC added/modified | `git diff --stat` |
| Backward compatibility | Existing `adhd refresh` behavior preserved for modules with only `refresh.py` | Manual test |

---

## 📅 Scope Budget

Single implementation phase. Estimated 3-5 days. All items `[KNOWN]` difficulty.

---

## ✅ Executive Summary Validation Checklist

### Narrative Completeness
- [x] The Story section clearly states user problem and value
- [x] Intent is unambiguous to a non-technical reader
- [x] Scope is explicitly bounded

### Technical Completeness
- [x] Prior Art section has BUY/BUILD/WRAP decisions
- [x] Non-Goals has ≥3 items
- [x] Features table has difficulty labels
- [x] No `[RESEARCH]` in scope

### Linkage
- [x] Features link to individual feature docs
- [x] Document linked from 00_index.md

---

**← Back to:** [Index](./00_index.md)
