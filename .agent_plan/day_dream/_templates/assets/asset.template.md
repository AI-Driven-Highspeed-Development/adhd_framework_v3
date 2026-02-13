---
type: asset
asset_type: mockup | diagram | storyboard | infrastructure | design | data-model | other
related_feature: "NN_feature_{id}.md"
created: YYYY-MM-DD
status: draft | review | approved | frozen
---
<!-- ═══════════════════════════════════════════════════════════════════
     ADHD-MANAGED — DO NOT EDIT DIRECTLY
     Source: modules/dev/instruction_core/data/.agent_plan/day_dream/_templates/assets/asset.template.md
     Refresh: adhd r -f
═══════════════════════════════════════════════════════════════════ -->


<!-- 
TEMPLATE USAGE: This template includes extensive guidance comments.
DELETE all <!-- comment --> blocks before finalizing your document.
The line limit (≤100 lines) applies to the FINAL document, not this template.
-->

# 🎨 {Feature ID}_{Description}

> *{One-sentence purpose: What does this artifact communicate?}*

**Status:** 📐 Draft | 🔄 In Review | ✅ Approved | 🔒 Frozen  
**Last Updated:** {YYYY-MM-DD}

---

## 📍 Context

<!-- 
Why does this artifact exist? What decision or feature does it support?
Keep to 2-4 sentences maximum.
-->

**Related Feature:** [{Feature Name}](../blueprint/NN_feature_{id}.md)  
**Requested By:** {Stakeholder/Agent}  
**Decision Context:** {Brief description of what this artifact helps decide}

---

## 🖼️ The Artifact

<!--
The actual visual/non-code content goes here.
Use appropriate format based on Type:

- mockup: ASCII art, Mermaid, or link to external tool
- diagram: Mermaid preferred, ASCII acceptable
- storyboard: Numbered sequence with descriptions
- infrastructure: System topology, deployment diagram
- design: UI flow, component layout
- data-model: ERD, schema, data dictionary
- other: Whatever fits

For external assets (Figma, Excalidraw, etc.):
1. Include a low-fi representation here (ASCII/Mermaid)
2. Link to the source file
-->

```mermaid
{Diagram content OR placeholder}
```

**Source File:** {Link to Figma/Excalidraw/etc., or "Embedded above"}

### Annotations

<!-- Optional: Numbered callouts explaining specific parts -->

| # | Element | Notes |
|---|---------|-------|
| 1 | {Element name} | {Explanation} |
| 2 | {Element name} | {Explanation} |

---

## ⚠️ Constraints

<!-- 
Hard requirements and explicit exclusions for this artifact.
These guide implementation when the artifact is realized.
-->

### Must Have
- {Constraint 1}
- {Constraint 2}

### Must NOT Have
- {Anti-constraint 1}
- {Anti-constraint 2}

### Technical Constraints
<!-- Optional: Performance, accessibility, compatibility requirements -->

- {Technical constraint}

---

## 🔗 Related Features

<!-- 
Links to all features that reference or depend on this artifact.
Updated as features are added.
-->

| Feature | Relationship | Status |
|---------|--------------|--------|
| [{Feature Name}](../blueprint/NN_feature_{id}.md) | Primary (this artifact was created for it) | {TODO/WIP/DONE} |
| [{Feature Name}](../blueprint/NN_feature_{id}.md) | Uses (references this artifact) | {TODO/WIP/DONE} |

---

## 📝 Revision History

<!-- 
Track significant changes to the artifact.
Minor tweaks don't need entries.
-->

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {YYYY-MM-DD} | 1.0 | Initial creation | {Agent/Person} |

---

## ❓ Open Questions

<!-- Remove section if no questions -->

- {Question about the artifact}

---

<!--
ASSET DOCUMENT NOTES:

NAMING CONVENTION: {feature_id}_{description}.asset.md
  Examples: 03_dashboard_mockup.asset.md
            05_data_flow_diagram.asset.md
            login_storyboard.asset.md (standalone, no feature ID)

WHEN TO CREATE:
- Visual design that needs stakeholder approval
- Architecture/flow diagrams that inform implementation
- UI mockups before coding
- Infrastructure topology for deployment planning
- Any non-code artifact that blocks or informs development

TYPE GUIDE:
| Type | Content | Tools |
|------|---------|-------|
| mockup | UI wireframes, screen layouts | ASCII, Mermaid, Excalidraw, Figma |
| diagram | System architecture, flows | Mermaid, draw.io |
| storyboard | User journey sequences | Numbered steps with visuals |
| infrastructure | Deployment, networking | Mermaid, ASCII topology |
| design | Visual design, branding | Figma, external links |
| data-model | ERD, schemas | Mermaid ERD, ASCII tables |
| other | Anything else | As appropriate |

LINE LIMIT: ~100 lines (excluding embedded diagrams)
This is a SUPPORTING artifact, not primary documentation.

LIFECYCLE:
1. Created in Draft by HyperDream
2. Reviewed and iterated
3. Approved by stakeholder/implementing agent
4. Frozen when implementation begins
5. New version created if changes needed post-freeze

EXTERNAL ASSETS:
Always include a low-fidelity representation in the doc itself.
External tools can disappear; the doc should be self-sufficient.
-->