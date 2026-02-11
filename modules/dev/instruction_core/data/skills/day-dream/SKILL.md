---
name: day-dream
description: "Vision and planning workflows — creating blueprint plans, architecture assets, and day-dream documents for the ADHD Framework. Covers tier selection (simple vs blueprint), document authoring rules, Story/Spec pattern, status syntax, feature templates, implementation plans, asset creation, and validation checklists. Use this skill when creating visions, roadmaps, blueprints, or planning new features."
---

# Day Dream

Blueprint authoring and vision planning for the ADHD Framework.

## When to Use
- Creating a new blueprint (day-dream) plan
- Authoring feature specs, architecture docs, or implementation plans
- Building supporting assets (diagrams, data models, mockups)
- Conceptualizing long-term vision or roadmaps

---

## Tier Selection

Templates are tiered based on project complexity:

| Tier | Use When | Template |
|------|----------|----------|
| **Simple** | ≤2 features, single module, no external APIs | `simple.template.md` |
| **Blueprint** | ≥3 features OR ≥2 cross-module deps OR external APIs | `blueprint/` folder |

### Auto-Detection Rules

```yaml
use_blueprint_tier:
  - feature_count >= 3
  - cross_module_imports >= 2
  - has_external_api: true
```

### Magnitude Routing

After selecting a tier, assess **magnitude** (Trivial → Epic) to determine planning depth:

| Tier + Magnitude | Route |
|------------------|-------|
| Simple + Trivial/Light | Execute directly — no planning document needed |
| Simple + Standard | Single plan file, execute in-session |
| Blueprint + Light/Standard | Blueprint docs, execute sequentially |
| Blueprint + Heavy | Blueprint docs, decompose into plan/task tree |
| Blueprint + Epic | Blueprint docs, mandatory decomposition, parallel agents |

> **Full magnitude table and decomposition protocol:** See the `dream-planning` skill.

---

## Templates Location

All templates at: `.agent_plan/day_dream/templates/`

### Simple Tier
| Template | Purpose | Line Limit |
|----------|---------|------------|
| `simple.template.md` | Single-file vision + quick start | ≤200 lines |

### Blueprint Tier
| Template | Purpose | Line Limit |
|----------|---------|------------|
| `blueprint/00_index.template.md` | Navigation hub with flowchart | ≤150 lines |
| `blueprint/01_executive_summary.template.md` | Vision, goals, non-goals | ≤150 lines |
| `blueprint/02_architecture.template.md` | System diagrams, logical components | ≤200 lines |
| `blueprint/NN_feature.template.md` | Per-feature details | ≤150 lines |
| `blueprint/NN_feature_simple.template.md` | Lightweight feature (80% of cases) | ≤100 lines |
| `blueprint/80_implementation.template.md` | Phased roadmap | ≤200 lines per phase |
| `blueprint/81_module_structure.template.md` | Reusable vs Project-Specific modules | ≤150 lines |
| `blueprint/82_cli_commands.template.md` | CLI interface and command reference | ≤150 lines |
| `blueprint/modules/module_spec.template.md` | Detailed module implementation spec | ≤200 lines |
| `blueprint/99_references.template.md` | External links | No limit |
| `blueprint/overview.template.md` | Plan directory navigator (`_overview.md` scaffold) | ≤100 lines |
| `blueprint/task.template.md` | Leaf task scaffold | ≤100 lines |

### Assets
| Template | Purpose | Line Limit |
|----------|---------|------------|
| `assets/asset.template.md` | Non-code artifacts | ≤100 lines (excluding diagrams) |

**Asset Types:** `mockup`, `diagram`, `storyboard`, `infrastructure`, `design`, `data-model`, `other`
**Naming:** `{feature_id}_{description}.asset.md`

---

## Status Syntax

Use hybrid emoji + text markers:

| Emoji | Text | Meaning |
|-------|------|---------|
| ⏳ | `[TODO]` | Not started |
| 🔄 | `[WIP]` | In progress |
| ✅ | `[DONE]` | Complete |
| 🚧 | `[BLOCKED:reason]` | Stuck (kebab-case reason) |
| 🚫 | `[CUT]` | Removed from scope |

---

## Difficulty Labels

Every feature/task MUST have a difficulty label:

| Label | Meaning | P0 Allowed? |
|-------|---------|-------------|
| `[KNOWN]` | Standard patterns, proven libraries | ✅ Yes |
| `[EXPERIMENTAL]` | Needs validation in our context | ⚠️ Conditional |
| `[RESEARCH]` | Active problem, no proven solution | ❌ NEVER in P0 |

---

## The Story → Spec Pattern

Every blueprint document follows this structure:

```markdown
## 📖 The Story
{Visual, scannable narrative — NOT a text wall}

---

## 🔧 The Spec
<!-- Technical specification begins here -->
```

### Story Section Requirements (Visual-First for ADHD readers)

| Principle | Do This | Not This |
|-----------|---------|----------|
| **Format** | ASCII boxes, tables, emoji anchors | Paragraphs of prose |
| **Scannability** | 10-second grasp of problem/solution | Reading required |
| **Structure** | Pain → Vision → One-Liner → Impact | Unstructured narrative |

**Required Subsections:**

| Subsection | Purpose | Visual Format |
|------------|---------|---------------|
| 😤 **The Pain** | What's broken, who hurts | ASCII box + pain table |
| ✨ **The Vision** | What success looks like | ASCII box showing flow |
| 🎯 **One-Liner** | Elevator pitch | Single blockquote |
| 📊 **Impact** | Before/After metrics | Comparison table |

**Why Visual > Text Walls:**
- ADHD readers skip prose, scan visuals
- ASCII boxes create spatial memory anchors
- Tables enable instant comparison
- Emoji provide visual hierarchy

**If you can't draw the pain and vision, you don't understand the feature.**

---

## Blueprint Document Rules

### Mandatory Skeleton Pattern

| Old Pattern | New Pattern |
|-------------|-------------|
| `<!-- Optional: ... -->` | Section present; write "N/A — [reason]" if not applicable |

**Rationale:** "Optional" is interpreted as "skip if uncertain." Mandatory skeleton forces documentation of decisions.

### Template Selection

| Template | Use When | Line Target |
|----------|----------|-------------|
| `NN_feature_simple.template.md` | ≤2 modules, no external APIs, not P0 | 80-100 lines |
| `NN_feature.template.md` | ≥3 modules, external APIs, P0 priority | 150-300 lines |

### Plan Navigator (`_overview.md`)
- Progress overview with emoji status
- Document navigation table
- "Where to Start" Mermaid flowchart
- Every plan directory MUST have an `_overview.md` (see `dream-planning` skill)

### Executive Summary (`01_executive_summary.md`)
- TL;DR: Maximum 3 sentences
- **Prior Art & Existing Solutions**: REQUIRED section
- Non-Goals: Minimum 3 items
- Features: Maximum 5 P0 features
- Freeze after approval with 🔒 FROZEN

### Architecture (`02_architecture.md`)
- Required when: ≥3 modules OR cross-module deps OR external APIs
- Key Design Principles table
- Logical Components: Purpose, Boundary, Implemented By
- System Diagram: Mermaid, must fit one screen

### Implementation (`80_implementation.md`)
- YAML frontmatter required
- P0 Hard Limits: 2-8 hours (AI-agent time), max 5 tasks, no `[RESEARCH]`
- **Natural Verification**: Every phase MUST have a "How to Verify (Manual)" section
  - Max 3 human-executable steps
  - Expected outcome for each step
  - Steps must complete in <30 seconds

### Module Structure (`81_module_structure.md`)
- REQUIRED for ADHD projects
- Defines Reusable vs Project-Specific modules
- Phase annotations `(P0)`, `(P1)`

### Module Specs (`modules/{module_name}.md`)
- **Required:** `## Implements Features` (bidirectional traceability)
- Links to feature docs that this module serves

### Custom Sections (FREE ZONE)
- **Prefix:** `## [Custom] 🎨 Title`
- **Maximum**: 5 custom sections per document
- **Prohibited**: P0 tasks, blocking dependencies, architecture changes

### Deep Dive Section
Optional for implementation-heavy features:
- Algorithm Choices, API Contract Draft, Error Handling Strategy
- **Delete if**: Straightforward features, obvious implementation

---

## Estimation Defaults

All blueprint durations use AI-agent time unless marked `human_only: true`.

| Magnitude | AI-Agent Time | Human Time (reference only) |
|-----------|---------------|----------------------------|
| Trivial | 5-15 minutes | 1-2 hours |
| Light | 15-60 minutes | 2-8 hours |
| Standard | 1-4 hours | 1-3 days |
| Heavy | 4-8 hours | 3-7 days |
| Epic | Must decompose | Must decompose |

### `human_only` Flag

When a task fundamentally requires human action (UX judgment, stakeholder approval, manual testing of physical devices), mark it with `human_only: true`. These tasks use human time estimates:

| Scenario | Route |
|----------|-------|
| Code generation, refactoring, file creation | AI-agent time (default) |
| Goal alignment decisions ("is this right?") | Human time |
| Subjective quality (UX, aesthetics) | Human time |
| Novel domain knowledge not in codebase | Human time |
| Acceptance testing with real users | Human time |

---

## Walking Skeleton Policy

Walking skeleton is **opt-in** — not every project needs one. (Distinct from "Mandatory Skeleton Pattern" which governs document section structure.)

**When REQUIRED (opt-in triggers):**

| Trigger | Example |
|---------|---------|
| Cross-boundary integration risk | Frontend + backend must connect in P0 |
| External API dependency | Must validate API works before building around it |
| Multi-module data flow | Data must flow through 3+ modules end-to-end |

**When NOT needed (skip it):**

| Scenario | Why Skip |
|----------|----------|
| Single-module changes | No integration boundary to test |
| Skill/template/doc edits | Testable by reading output |
| Self-contained features | Can be tested at any phase |
| Tasks with magnitude ≤ Light | Too small for skeleton overhead |

---

## Clean-Code-First Directive

Prioritize clean, correct code over minimizing edited lines or maintaining backward compatibility to broken patterns.

1. **Delete wrong code** — do not wrap it in fallbacks
2. **Refactor fully** — do not leave half-migrated paths
3. **One correct path** — not `try (new) catch (old)`
4. **Measure success by correctness** — not by lines changed

> **Full practice:** See the `orch-implementation` skill's **Non-Vibe Code Practice** section for the complete 3-pillar discipline (Unify Before Duplicating, No Dead Fallbacks, Ask Don't Guess) and the "Unify or Justify" gate.

### Folder-Separation for Backward Compatibility

When backward compatibility IS genuinely needed (external users depend on an API):

**DO — separate by folder:**
```
feature/
├── v2/          ← new correct implementation
│   └── handler.py
└── v1/          ← old implementation (delete when migration done)
    └── handler.py
```

**DON'T — fallback wrappers:**
```python
# ❌ NEVER do this
try:
    result = new_correct_handler(data)
except:
    result = old_broken_handler(data)
```

---

## Asset Authoring

### Asset Types

| Type | Use For | Example |
|------|---------|---------|
| `mockup` | UI wireframes, screen layouts | `03_dashboard_mockup.asset.md` |
| `diagram` | Architecture, flow, component diagrams | `02_auth_flow_diagram.asset.md` |
| `storyboard` | User journey sequences | `04_onboarding_storyboard.asset.md` |
| `infrastructure` | Deployment, server topology | `01_infra_layout.asset.md` |
| `design` | Visual design specs, style guides | `05_theme_design.asset.md` |
| `data-model` | Entity relationships, schemas | `03_user_data_model.asset.md` |

### Naming Convention
```
{feature_id}_{description}.asset.md
```

### Required Sections

```markdown
# {Asset Title}

**Type:** {type}
**Related Feature:** [Feature Title](../NN_feature.md)
**Status:** `⏳ [TODO]` | `🔄 [WIP]` | `✅ [DONE]`

## Context
Why this asset exists.

## The Artifact
The actual content: Mermaid diagram, ASCII mockup, etc.

## Constraints
Limitations and assumptions.

## Related Features
Links to dependent features/assets.
```

### Content Guidelines
- Use **Mermaid** for diagrams (max: fit one screen)
- ASCII art for quick mockups
- Store images in `assets/images/` subfolder
- Prefer SVG over PNG/JPG

### Line Limits

| Section | Limit |
|---------|-------|
| Context | ~20 lines |
| Constraints | ~10 lines |
| Total (excluding diagrams) | **≤100 lines** |

---

## Validation Checklists

### Feature Checklist
```markdown
- [ ] The Story section clearly states user problem and value
- [ ] Intent is unambiguous to a non-technical reader
- [ ] Scope is explicitly bounded
- [ ] Integration Points table has all connections
- [ ] Edge Cases cover failure scenarios
- [ ] Acceptance Criteria are testable
```

### Module Checklist
```markdown
- [ ] Implements Features section links to ≥1 feature OR marked as utility
- [ ] All linked features have backlinks to this module spec
- [ ] Responsibilities clearly state DO and DON'T
- [ ] Public API section defines interface contract
```

---

## Folder Structure

### Simple Tier
```
.agent_plan/day_dream/
├── {project}_vision.md
└── templates/
```

### Blueprint Tier
```
.agent_plan/day_dream/
├── _overview.md                    ← Root navigator
├── {plan_name}/                    ← Named plan directory
│   ├── _overview.md                ← Mandatory navigator
│   ├── plan.yaml                   ← Metadata (name, magnitude, status)
│   ├── executive_summary.md        ← Blueprint docs in plan root
│   ├── architecture.md
│   ├── cli_commands.md             ← If plan has CLI commands
│   ├── implementation.md           ← Phase tracking
│   ├── module_structure.md         ← Module organization
│   ├── p00_{name}/                 ← Phase directory
│   │   ├── _overview.md
│   │   ├── 01_{task}.md            ← Numbered task files
│   │   └── 02_{task}.md
│   ├── p01_{name}/                 ← Phase directory
│   │   ├── _overview.md
│   │   ├── 01_{task}.md
│   │   └── 02_{task}.md
│   └── p02_{name}/                 ← Phase directory
│       ├── _overview.md
│       ├── 01_{task}.md
│       └── 02_{task}.md
├── assets/                         ← Supporting artifacts
├── exploration/                    ← Research/exploration docs
│   └── _archive/
└── templates/                      ← Template scaffolds
```

### Phase Naming Convention

- Phase children use `pNN_{name}/` prefix with zero-padded two-digit numbers and underscore separator (e.g., `p00_prerequisites/`, `p01_core_commands/`)
- Task files within phases use `NN_{task_name}.md` numbering (e.g., `01_remove_command.md`, `02_safety_features.md`) — the `00_` position is implicitly held by `_overview.md` (sorts first), so task numbering starts at `01_`
- Phases MUST always be **directories** (never files), even if they contain only one task
- This overrides the general DREAM "flatten single-child" guidance — sequential ordering must be preserved in file explorers (VS Code sorts folders before files, breaking visual order if phases mix files and directories)
- Single-task phases contain: `_overview.md` + one task `.md` file
- Zero-padding supports up to 99 phases (`p00_` through `p99_`) — more than sufficient for any plan

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Put `[RESEARCH]` in P0 | Defer to P1+ or resolve in exploration |
| Exceed line limits | Split into separate files |
| Edit frozen documents | Create new version or update implementation |
| Have >3 active explorations | Synthesize or abandon oldest |
| Skip verification sections | Always include manual verification |
| Use Simple tier for complex projects | Upgrade to Blueprint when threshold met |
| Embed code in assets | Assets are for visuals/planning |
| Create orphan assets | Always link to parent feature |
| Use human-time estimates for AI tasks | Default to AI-agent time scale |
| Force walking skeleton on all projects | Check trigger criteria first — skip if not needed |
| Wrap old code in try/catch fallbacks | Delete old code or separate into v1/v2 folders |
| Minimize lines changed over correctness | Prioritize clean, correct code |

---

## Cross-References

| Topic | Where |
|-------|-------|
| Magnitude routing & decomposition protocol | `dream-planning` skill |
| Plan/task hierarchy & `_overview.md` convention | `dream-planning` skill |
| MANAGER/WORKER lifecycle | `dream-planning` skill |
| Sibling firewall & context isolation | `dream-planning` skill |
| Orchestrator dispatch mechanics | `orch-routing` skill |
| Implementation quality gates | `orch-implementation` skill |
