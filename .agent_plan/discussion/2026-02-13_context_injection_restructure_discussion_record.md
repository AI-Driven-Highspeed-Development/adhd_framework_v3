# Discussion Record: Restructuring Context Injection Files

| Field        | Value                                                                          |
| ------------ | ------------------------------------------------------------------------------ |
| Topic        | Restructuring Context Injection Files — taxonomy, Dream SOP, skill-centric design |
| Date         | 2026-02-13                                                                     |
| Participants | HyperArch, HyperSan, HyperDream, HyperAgentSmith                             |
| Rounds       | 1                                                                              |
| Status       | Consensus ✅                                                                    |

---

## Final Synthesis

### 1. Three-Axis Taxonomy

| Axis           | File Type    | Purpose                                      |
| -------------- | ------------ | --------------------------------------------- |
| **Perspective** | `.agent.md`  | Personality only — who the agent *is*         |
| **Truth**       | `.instructions.md` | Universal, framework-wide specifications |
| **Procedure**   | `SKILL.md`   | SOPs — step-by-step workflows                |

### 2. Umbrella Term

All `.md` context files (agents, instructions, skills, prompts) are collectively referred to as **"context injection files"**.

### 3. Decision Rule: Instruction → Skill Migration

> **Instruction → Skill IFF exclusively consumed by one agent's workflow.**
> Multi-agent `applyTo` → stays instruction. Usage audit required first.

### 4. Instructions Scope

Instructions remain appropriate for:

- **(a)** Module-local instructions — stay in their respective module directories.
- **(b)** Format/structure specs consumed by everyone.
- **(c)** Framework philosophy and principles.

### 5. Dream Routing Architecture

A `dream-routing` skill acts as the keystone entry point, containing:

- A `references/` subfolder for templates.
- Routing logic to leaf skills (`dream-create-PP`, `dream-update`, `dream-fix`, etc.).
- Each leaf skill is **self-contained** — no cross-leaf dependencies.

### 6. Transition Safety

- YAML frontmatter marker: `deprecated: true` + `superseded_by: skill-name`.
- `adhd r -f` treats `deprecated: true` as a **compile-time exclusion** gate.
- No dual-visibility — deprecated files are invisible to agents after refresh.

### 7. Edit-Location Rule Preserved

- **Centralized files**: Source of truth remains `modules/dev/instruction_core/data/`.
- **Module-local instructions**: Source of truth stays in their module directory.

### 8. Deferred

Archived-iterations self-refinement → **P2+** (out of scope for initial restructuring).

### 9. Two PPs Created

| Plan | Title                                | Dependency |
| ---- | ------------------------------------ | ---------- |
| PP02 | Context Injection Files Restructuring | —          |
| PP03 | Dream SOP Skills                     | PP02       |

---

## Agent Positions

### HyperArch — Vote: ACCEPT

Fully buildable. Proposed the decision rule: multi-agent `applyTo` = stays instruction, single-agent consumption = becomes skill. Leaf skills must be self-contained with no cross-leaf dependencies.

### HyperSan — Vote: ACCEPT

Demanded usage audit before any migration — no decision rule was initially provided. Accepted Arch's rule with audit as prerequisite. Flagged archived-iterations as scope creep. Clarification: module-local instructions keep source-of-truth in their module directory.

### HyperDream — Vote: ACCEPT

Architecturally elegant three-axis separation. `dream-routing` is the keystone skill. Conceded archived-iterations is P2+. Proposed deprecation markers (`deprecated: true` + `superseded_by`) for transition safety.

### HyperAgentSmith — Vote: ACCEPT

Sharpens taxonomy — agents become lean personality shells, `applyTo` system becomes cleaner. Edit-location rule must survive restructuring. `deprecated: true` serves as compile-time exclusion gate in `adhd r -f`.

---

## Key Divergence Resolved

HyperSan's demand for a concrete decision rule was addressed by HyperArch's **"multi-agent vs single-agent consumption"** rule. All agents accepted with usage audit as prerequisite before any migration occurs.
