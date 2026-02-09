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

### Index (`00_index.md`)
- Progress Overview with emoji status
- Document navigation table
- "Where to Start" Mermaid flowchart

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
- P0 Hard Limits: 3-5 days, max 5 tasks, no `[RESEARCH]`
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
**Related Feature:** [Feature Title](../blueprint/NN_feature.md)
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
├── blueprint/
│   ├── 00_index.md
│   ├── 01_executive_summary.md
│   ├── 02_architecture.md
│   ├── 03_feature_*.md
│   ├── 80_implementation.md
│   ├── 81_module_structure.md
│   └── modules/
├── assets/
├── exploration/
│   └── _archive/
└── templates/
```

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
