---
applyTo: "**/.agent_plan/day_dream/**"
---

# Blueprint Document Authoring Guidelines

## Goals
- Standardize vision, implementation, architecture, feature, and exploration documents.
- Enforce constraints that keep planning documents focused and actionable.
- Ensure consistency across all HyperDream-generated artifacts.

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
| `blueprint/deep_dive_reference.md` | Reference for Deep Dive subsections | Reference doc |
| `blueprint/exploration.template.md` | Pre-vision research | ≤200 lines |

### Assets (Multi-Modal Artifacts)
| Template | Purpose | Line Limit |
|----------|---------|------------|
| `assets/asset.template.md` | Non-code artifacts (mockups, diagrams, storyboards, etc.) | ≤100 lines |

**Asset Types:** `mockup`, `diagram`, `storyboard`, `infrastructure`, `design`, `data-model`, `other`  
**Naming:** `{feature_id}_{description}.asset.md` (e.g., `03_dashboard_mockup.asset.md`)

### Examples

Completed samples at: `templates/examples/`

| Example | Demonstrates |
|---------|--------------|
| `simple_example.md` | Simple tier vision document |
| `blueprint_example/` | Full Blueprint tier folder structure |
| `free_zone_*.example.md` | Custom sections (Philosophical Tensions, Assumption Graveyard, Metaphor Map) |
| `deep_dive_*.example.md` | Deep Dive subsections (Algorithm Choices, API Contract, Error Handling) |

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

**Example:** `⏳ [TODO]`, `🔄 [WIP]`, `✅ [DONE]`

---

## Difficulty Labels

Every feature/task MUST have a difficulty label:

| Label | Meaning | P0 Allowed? |
|-------|---------|-------------|
| `[KNOWN]` | Standard patterns, proven libraries | ✅ Yes |
| `[EXPERIMENTAL]` | Needs validation in our context | ⚠️ Conditional |
| `[RESEARCH]` | Active problem, no proven solution | ❌ NEVER in P0 |

---

## Document Rules

### Internal Document Structure

Every blueprint document follows the **Story → Spec** pattern:

```markdown
## 📖 The Story
{Visual, scannable narrative — NOT a text wall}

---

## 🔧 The Spec
<!-- Technical specification begins here -->
```

**The Story Requirements (Visual-First for ADHD readers):**

| Principle | Do This | Not This |
|-----------|---------|----------|
| **Format** | ASCII boxes, tables, emoji anchors | Paragraphs of prose |
| **Scannability** | 10-second grasp of problem/solution | Reading required |
| **Structure** | Pain → Vision → One-Liner → Impact | Unstructured narrative |
| **Length** | CAN be longer if visual & useful | Short text walls |

**Required Subsections:**

| Subsection | Purpose | Visual Format |
|------------|---------|---------------|
| 😤 **The Pain** | What's broken, who hurts | ASCII box showing blocked flow + pain table |
| ✨ **The Vision** | What success looks like | ASCII box showing working flow |
| 🎯 **One-Liner** | Elevator pitch | Single blockquote sentence |
| 📊 **Impact** | Before/After metrics | Comparison table with ❌/✅ |

**Example Story Section:**

```markdown
### 😤 The Pain

┌─────────────────────────────────────────┐
│  User wants X  ──────►  💥 BLOCKED 💥   │
│  Because: [root cause]                  │
└─────────────────────────────────────────┘

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| Developer | 🔥🔥🔥 High | Daily |

### ✨ The Vision

┌─────────────────────────────────────────┐
│  User wants X  ──────►  ✅ SUCCESS      │
│  Flow: step → step → result             │
└─────────────────────────────────────────┘

### 🎯 One-Liner

> We're building [thing] so [persona] can [outcome] without [pain].

### 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| Time to X | ❌ 10 min | ✅ 10 sec |
```

**Why Visual > Text Walls:**
- ADHD readers skip prose, scan visuals
- ASCII boxes create spatial memory anchors
- Tables enable instant comparison
- Emoji provide visual hierarchy
- Before/After format shows transformation

**If you can't draw the pain and vision, you don't understand the feature**

**The Spec Requirements:**
- Everything after the horizontal rule
- Technical details, diagrams, tables
- Implementation-focused content

### Mandatory Skeleton Pattern

Sections marked as "optional" in previous templates are now **mandatory skeletons**:

| Old Pattern | New Pattern |
|-------------|-------------|
| `<!-- Optional: ... -->` | Section present; write "N/A — [reason]" if not applicable |
| `<!-- OPTIONAL -->` | Always include; document why N/A |

**Rationale:** "Optional" is interpreted as "skip if uncertain." Mandatory skeleton forces documentation of decisions.

**Example:**
```markdown
## 🗺️ System Context

N/A — Single module with no external integrations. All logic contained in `{manager}/`.
```

### Template Selection (Simple vs Full)

| Template | Use When | Line Target |
|----------|----------|-------------|
| `NN_feature_simple.template.md` | ≤2 modules, no external APIs, not P0, no deep technical decisions | 80-100 lines |
| `NN_feature.template.md` | ≥3 modules, external APIs, P0 priority, needs Deep Dive | 150-300 lines |

**Upgrade Triggers:** Expand simple → full when complexity increases.

### Simple Tier
- Single file, ~50-200 lines
- Must include: Hook, What's Here, Quick Start, API Reference
- Optional: Edge Cases, When to Upgrade

### Blueprint Tier

#### Index (`00_index.md`)
- Progress Overview with emoji status
- Document navigation table
- "Where to Start" Mermaid flowchart

#### Executive Summary (`01_executive_summary.md`)
- TL;DR: Maximum 3 sentences
- **Prior Art & Existing Solutions**: REQUIRED section with BUY/BUILD/WRAP decisions
- Non-Goals: Minimum 3 items
- Features: Maximum 5 P0 features
- Freeze after approval with 🔒 FROZEN

#### Architecture (`02_architecture.md`)
- Required when: ≥3 modules OR cross-module deps OR external APIs
- Key Design Principles: 3-5 principles table
- Logical Components: Purpose, Boundary, Implemented By
- Project Structure: Target end-state with phase annotations `(P0)`, `(P1)`
- System Diagram: Mermaid, must fit one screen

#### Feature (`NN_feature.md`)
- Create when feature description exceeds ~40 lines
- Optional: System Context diagram, Data Flow, Integration Points
- Related Assets: Link to mockups/diagrams in `../assets/` folder (see `dream_assets.instructions.md`)

#### Module Structure (`81_module_structure.md`)
- REQUIRED for ADHD projects.
- Defines Reusable vs Project-Specific modules.
- Proposed file tree with phase annotations.
- Uses **mandatory skeleton** pattern for module lists.

#### Module Specs (`modules/{module_name}.md`)
- **Required section:** `## Implements Features` (bidirectional traceability)
- Links to feature docs that this module serves
- If utility-only, explicitly state: "N/A — Utility module providing [capability]"
- Creates bidirectional traceability: features ↔ modules

#### CLI Commands (`82_cli_commands.md`)
- OPTIONAL.
- Required if project exposes a CLI.
- Admin vs User command reference tables.

##### Custom Sections (FREE ZONE)
Authors may add project-specific sections with these rules:
- **Prefix Convention**: Use `## [Custom] 🎨 Title` (e.g., `## [Custom] 🎨 Analytics Events`)
- **Free Zone**: Content between `<!-- FREE ZONE START -->` and `<!-- FREE ZONE END -->` markers
- **Examples**: See `templates/examples/free_zone_*.example.md` (Philosophical Tensions, Assumption Graveyard, Metaphor Map)
- **Maximum**: 5 custom sections per document
- **Prohibited in Custom**: P0 tasks, blocking dependencies, architecture changes

##### Deep Dive Section (`## 🔬 Deep Dive`)
Optional section for implementation-heavy features:
- **When to use**: Algorithm choices, API contracts, complex error handling, performance tradeoffs
- **When to delete**: Straightforward features, obvious implementation path, simple CRUD
- **Subsections**: Algorithm Choices, API Contract Draft, Error Handling Strategy
- **Examples**: See `templates/examples/deep_dive_*.example.md`

#### Asset (`*.asset.md`)
- Lightweight template for non-code artifacts
- Types: mockup, diagram, storyboard, infrastructure, design, data-model
- Naming: `{feature_id}_{description}.asset.md`
- Required sections: Context, The Artifact, Constraints, Related Features
- Line limit: ~100 lines (excluding embedded diagrams)
- **Full specification**: See `dream_assets.instructions.md` for detailed rules

#### Implementation (`80_implementation.md`)
- YAML frontmatter required
- Target Folder Structure: Per-phase NEW/MODIFIED files
- P0 Hard Limits: 3-5 days, max 5 tasks, no `[RESEARCH]`
- Error Handling Implementation section
- **Natural Verification**: Every phase MUST have a "How to Verify (Manual)" section.
    - **Rationale**: Automated tests are code, and code can have bugs. Humans need a direct, intuitive way to confirm each stage works before proceeding.
    - **Format**:
        - Max 3 human-executable steps (1-2 for P0/P1)
        - Expected outcome for each step
        - Steps must complete in <30 seconds
        - Use table: "What to try" | "Expected result"
    - **Verification Method Priority**:
        1. **Production entry point** (preferred) — The actual app (`./app.py`, CLI) tests the real code path.
        2. **Native tooling** — Browser, `curl`, terminal commands, REPL.
        3. **Playground** (fallback) — Only when production testing is genuinely impossible.

#### Exploration
- Max 3 active, 14-day expiration
- Archive to `exploration/_archive/` when done
- Uses **Story/Spec** pattern (Story = what decision is blocked)

---

## Validation Checklists

Every blueprint document includes an embedded validation checklist:

### Checklist Categories

| Category | Validates |
|----------|-----------|
| **Narrative** | The Story section, intent clarity, scope bounds |
| **Technical** | Endpoints, error cases, dependencies |
| **Linkage** | Bidirectional references between docs |

### Checklist Rules

1. **Mandatory:** Cannot mark document as "ready" with unchecked items
2. **Position:** At bottom of document, before navigation links
3. **Format:** Checkbox list with clear pass/fail criteria
4. **Tier-specific:** Different checklists for features vs modules vs implementation

### Example Feature Checklist

```markdown
## ✅ Feature Validation Checklist

### Narrative Completeness
- [ ] The Story section clearly states user problem and value
- [ ] Intent is unambiguous to a non-technical reader
- [ ] Scope is explicitly bounded

### Technical Completeness
- [ ] Integration Points table has all connections
- [ ] Edge Cases cover failure scenarios
- [ ] Acceptance Criteria are testable
```

### Example Module Checklist

```markdown
## ✅ Module Validation Checklist

### Traceability
- [ ] Implements Features section links to ≥1 feature OR marked as utility
- [ ] All linked features have backlinks to this module spec

### Completeness
- [ ] Responsibilities clearly state DO and DON'T
- [ ] Public API section defines interface contract
```

---

## Folder Structure

### Simple Tier Output
```
.agent_plan/day_dream/
├── {project}_vision.md      # Single-file vision
└── templates/               # Templates (DO NOT EDIT)
```

### Blueprint Tier Output
```
.agent_plan/day_dream/
├── blueprint/               # Multi-file structure
│   ├── 00_index.md
│   ├── 01_executive_summary.md
│   ├── 02_architecture.md
│   ├── 03_feature_*.md
│   ├── 80_implementation.md
│   ├── 81_module_structure.md
│   ├── 82_cli_commands.md
│   ├── 99_references.md
│   └── modules/
│       └── {module_name}.md
├── assets/                  # Non-code artifacts
│   ├── {feature_id}_{description}.asset.md
│   └── ...
├── exploration/             # Pre-vision research
│   └── _archive/
└── templates/               # Templates (DO NOT EDIT)
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Put `[RESEARCH]` in P0 | Defer to P1+ or resolve in exploration first |
| Exceed line limits | Split into separate files |
| Edit frozen documents | Create new version or update implementation |
| Have >3 active explorations | Synthesize or abandon oldest |
| Skip verification sections | Always include manual verification steps |
| Use Simple tier for complex projects | Upgrade to Blueprint when threshold met |
