---
project: "{Project Name}"
current_phase: 0
phase_name: "Walking Skeleton"
status: TODO
start_date: "{YYYY-MM-DD}"
last_updated: "{YYYY-MM-DD}"
---

# 80 - Implementation Plan

> Part of [{Project Name} Blueprint](./00_index.md)

<!-- 
⚠️  CODE EXAMPLES & FOLDER STRUCTURES WARNING ⚠️
════════════════════════════════════════════════════════════════════════════════
Examples in this document are ILLUSTRATIVE, not PRESCRIPTIVE.

• Folder structures show INTENT, actual paths may differ
• Commands show CONCEPT, actual syntax depends on tooling
• Task descriptions are GOALS, not step-by-step instructions

The implementation agent (HyperArch) will determine actual file locations,
command syntax, and implementation details based on current codebase state.
════════════════════════════════════════════════════════════════════════════════
-->

---

## 📊 Status Legend

| Icon | Status | Meaning |
|------|--------|---------|
| ⏳ | `[TODO]` | Not started |
| 🔄 | `[WIP]` | In progress |
| ✅ | `[DONE]` | Complete |
| ✅ | `[DONE:invalidated-by:XXnn]` | Complete but invalidated |
| 🚧 | `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 | `[CUT]` | Removed from scope |

---

## ⚙️ Phase 0: {Foundation / Walking Skeleton}

**Goal:** *"{One sentence goal — foundation tasks or integration proof}"*

**Duration:** ■■□□□□□□ Light (max 2 slots)

<!--
🦴 Walking Skeleton is CONDITIONAL — include it as P0 only when:
  - Multiple modules must integrate through untested boundaries
  - A new data flow spans 3+ components end-to-end
  - The integration path itself is the primary risk
Otherwise, P0 is foundation tasks (skill updates, config, scaffolding).
-->

### Exit Gate

- [ ] `{executable command}` → `{expected output}`

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ⏳ | {Task description} | `{module/}` | `[KNOWN]` |
| ⏳ | {Task description} | `{module/}` | `[KNOWN]` |

### P0 Hard Limits

- ❌ No `[RESEARCH]` or `[EXPERIMENTAL]` items
- ❌ Max 5 tasks
- ❌ Must fit within slot budget (≤5 slots)

### Target Folder Structure (P0)

```
{project_root}/
└── managers/{manager}/           (NEW)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `{command}` | {outcome} |

### P0 Completion Checklist

- [ ] Exit gate command runs successfully
- [ ] All tasks marked ✅
- [ ] No `[RESEARCH]` or `[EXPERIMENTAL]` items
- [ ] ≤5 tasks total
- [ ] Slot budget respected
- [ ] Manual verification steps pass

---

## 🏗️ Phase 1: {Phase Name}

**Goal:** *"{One sentence goal}"*  
**Duration:** ■■■□□□□□ Standard (max 3 slots)

### Exit Gate

- [ ] `{executable command}` → `{expected output}`

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ⏳ | {Task description} | `{module/}` | `[KNOWN]` |
| ⏳ | {Task description} | `{module/}` | `[EXPERIMENTAL]` |

### Target Folder Structure (P1)

```
{project_root}/
├── plugins/{plugin}/             (NEW)
└── managers/{manager}.py         (MODIFIED)
```

### Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| `{command}` | {outcome} |

### P1 Completion Checklist

- [ ] Exit gate command runs successfully
- [ ] All `[EXPERIMENTAL]` items validated or cut
- [ ] Manual verification steps pass
- [ ] Linked module specs updated

---

## 📡 Phase 2+: {Phase Name}

**Goal:** *"{One sentence goal}"*  
**Duration:** ■■■■■□□□ Heavy (max 5 slots)

### Tasks

| Status | Task | Module | Difficulty |
|--------|------|--------|------------|
| ⏳ | {Task description} | `{module/}` | `[RESEARCH]` |

---

## ⚠️ Error Handling Implementation

<!-- Philosophy in architecture.md; specifics here -->

### Error Types

| Error Class | When Raised | Recovery |
|-------------|-------------|----------|
| `{ErrorName}` | {Condition} | {retry/skip/fail} |

### Logging Requirements

| Level | When | Example |
|-------|------|---------|
| ERROR | {Condition} | `"Failed to {action}: {reason}"` |
| WARNING | {Condition} | `"Retrying {action} ({n}/3)"` |
| INFO | {Condition} | `"{action} completed"` |

---

## 📝 Decisions Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| {YYYY-MM-DD} | {Decision made} | {Why} | {Agent/Human} |

---

## ✂️ Cut List

| Feature | Cut Date | Reason |
|---------|----------|--------|
| {Feature name} | {Date} | {Why cut} |

---

## 🔬 Exploration Log

| Date | Topic | Status | Synthesized To |
|------|-------|--------|----------------|
| {YYYY-MM-DD} | {Topic} | {SYNTHESIZED/ABANDONED} | {doc#section} |

---

**← Back to:** [Index](./00_index.md)

<!--
NOTES:
1. Update YAML frontmatter when changing phases
2. Status flow: ⏳ → 🔄 → ✅
3. Target Folder Structure: NEW/MODIFIED files per phase only
4. Task size: completable in 1-5 slots. Epic tasks (8 slots max) must decompose.
5. Duration format (8-bar DREAM v4.05):
   ■□□□□□□□  Trivial   (max 1 slot)
   ■■□□□□□□  Light     (max 2 slots)
   ■■■□□□□□  Standard  (max 3 slots)
   ■■■■■□□□  Heavy     (max 5 slots)
   ■■■■■■■■  Epic      (max 8 slots → must decompose)
6. Walking skeleton is CONDITIONAL — only for cross-boundary integration risk. Otherwise P0 = foundation.
-->
