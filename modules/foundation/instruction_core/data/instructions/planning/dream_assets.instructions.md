---
applyTo: "**/.agent_plan/day_dream/assets/**"
---

# Day Dream Asset Authoring Guidelines

## Purpose
Asset files capture non-code artifacts that support planning: mockups, diagrams, storyboards, infrastructure sketches, data models, and design documents.

---

## Asset Types

| Type | Use For | Example Filename |
|------|---------|------------------|
| `mockup` | UI wireframes, screen layouts | `03_dashboard_mockup.asset.md` |
| `diagram` | Architecture, flow, component diagrams | `02_auth_flow_diagram.asset.md` |
| `storyboard` | User journey sequences | `04_onboarding_storyboard.asset.md` |
| `infrastructure` | Deployment, server topology | `01_infra_layout.asset.md` |
| `design` | Visual design specs, style guides | `05_theme_design.asset.md` |
| `data-model` | Entity relationships, schemas | `03_user_data_model.asset.md` |
| `other` | Anything not above | `06_research_notes.asset.md` |

---

## Naming Convention

```
{feature_id}_{description}.asset.md
```

- **feature_id**: Two-digit number matching related feature (e.g., `03` for feature `03_dashboard.md`)
- **description**: Lowercase, underscore-separated description
- **Example**: `03_dashboard_mockup.asset.md`, `02_api_sequence_diagram.asset.md`

---

## Required Sections

Every asset file MUST include:

```markdown
# {Asset Title}

**Type:** {mockup|diagram|storyboard|infrastructure|design|data-model|other}  
**Related Feature:** [Feature Title](../blueprint/NN_feature.md)  
**Status:** `⏳ [TODO]` | `🔄 [WIP]` | `✅ [DONE]` | `🚧 [BLOCKED:reason]` | `🚫 [CUT]`

## Context
Why this asset exists and what problem it addresses.

## The Artifact
The actual content: Mermaid diagram, ASCII mockup, embedded image reference, etc.

## Constraints
Limitations, assumptions, or fixed requirements this asset respects.

## Related Features
Links to other features or assets this depends on or affects.
```

---

## Content Guidelines

### Diagrams
- Use **Mermaid** for all flowcharts, sequences, ER diagrams, state machines
- Maximum diagram complexity: Fit on one screen (no scrolling)
- For complex systems, split into multiple focused diagrams

### Mockups
- ASCII art for quick sketches
- Reference external tools (Figma, Excalidraw) with links for detailed mockups
- Include dimensions/constraints inline

### Embedded Images
- Store in `assets/images/` subfolder
- Reference with relative paths: `![Alt](images/filename.png)`
- Prefer vector (SVG) over raster (PNG/JPG) where possible

---

## Line Limits

| Section | Limit |
|---------|-------|
| Context | ~20 lines |
| Constraints | ~10 lines |
| Related Features | ~10 lines |
| **Total (excluding diagrams)** | **≤100 lines** |

Diagrams and embedded images do NOT count toward line limit.

---

## Linking Convention

### From Feature to Asset
```markdown
## Related Assets
- [Dashboard Mockup](../assets/03_dashboard_mockup.asset.md)
- [API Flow Diagram](../assets/03_api_flow_diagram.asset.md)
```

### From Asset to Feature
```markdown
**Related Feature:** [Dashboard Feature](../blueprint/03_feature_dashboard.md)
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Embed code in assets | Assets are for visuals/planning, not implementation |
| Create orphan assets | Always link to parent feature |
| Exceed 100 lines | Split into focused sub-assets |
| Use PNG for diagrams | Use Mermaid or SVG for editability |
| Skip the Context section | Always explain WHY this asset exists |
