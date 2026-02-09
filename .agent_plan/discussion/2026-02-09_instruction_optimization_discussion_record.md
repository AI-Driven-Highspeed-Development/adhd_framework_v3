# 📋 Discussion Report: ADHD Framework Instruction Optimization

> **Date**: 2026-02-09  
> **Participants**: HyperArch, HyperSan, HyperDream, HyperAgentSmith  
> **Rounds**: 1 (consensus reached in single round)  
> **Status**: ✅ CONSENSUS REACHED  

---

## 🎯 Problem Statement

How to improve and optimize ADHD Framework instructions for agents/instructions/skills/prompts. The framework has grown organically with sophisticated context-engineering patterns, but faces challenges in:

- Token efficiency and context budget management
- Validation and compliance enforcement
- Discoverability and observability of instruction assets
- Template completeness and platform alignment

---

## 📊 Discussion Rounds

### PROPOSE Phase: Initial Positions

| Agent | Core Position | Key Argument |
|-------|--------------|--------------|
| **HyperArch** | Token-heavy output needs progressive loading and context budgets | Large instruction files consume significant context window. Need lazy loading strategies and explicit token budget annotations. |
| **HyperSan** | No runtime validation, agents exceed line limits, no compliance feedback loop | Current instructions specify limits (e.g., ≤100 lines) but have no enforcement mechanism. Agents violate constraints with no feedback. |
| **HyperDream** | Most context-engineered framework — needs discoverability and observability | ADHD has sophisticated instruction layering but developers struggle to discover what exists and trace what loads when. |
| **HyperAgentSmith** | Templates missing VS Code fields, format validation needed | Agent/instruction templates lack VS Code-specific metadata. No automated validation ensures templates produce valid outputs. |

---

### CHALLENGE Phase: Position Evolution

| Agent | Challenge Response | Position Shift |
|-------|-------------------|----------------|
| **HyperArch** | VS Code alignment is prerequisite for progressive loading. Can't optimize loading without knowing which fields are used by which platform. | ✅ SHIFTED — Platform profiles first, then loading optimization |
| **HyperSan** | Existing agents + skills pattern is sufficient. Tiered instruction model adds complexity without clear benefit. | 🔒 HELD — Focus on validation, not restructuring |
| **HyperDream** | Compliance testing is valuable but P2. Platform-agnosticism principle should be preserved even as we add VS Code profiles. | ⚠️ PARTIALLY SHIFTED — Accept profiles if they're optional metadata |
| **HyperAgentSmith** | Platform profiles vs. core schema split is the right approach. Templates need both: universal fields + platform-specific blocks. | ⚠️ PARTIALLY AGREED — Separate concerns, don't merge |

---

## ✅ Final Consensus Summary

### P0 Priorities (Immediate Action Items)

| # | Decision | Owner | Rationale |
|---|----------|-------|-----------|
| 1 | **Enforce line limits (≤100 lines, automated validation)** | HyperSan | Current ≤100 line guidance is aspirational. Need CI/MCP tool to block violations. |
| 2 | **Token budget annotations (`<!-- tokens: ~N -->`)** | HyperArch | Explicit token costs enable informed decisions about instruction composition. |
| 3 | **VS Code platform profiles (optional metadata block)** | HyperAgentSmith | Keep core schema platform-agnostic. Add optional `## [Platform] VS Code` blocks for IDE-specific config. |
| 4 | **Skill discovery index (SKILLS_INDEX.md with "When NOT to use")** | HyperDream | Skills lack negative guidance. Index should include anti-patterns and skill boundaries. |
| 5 | **Instruction layering audit tool (MCP/CLI, conflict detection)** | HyperArch | Developers can't trace which instructions load for a given context. Need introspection tool. |

---

### Deferred Items

| # | Item | Phase | Reason |
|---|------|-------|--------|
| 1 | Flow versioning for instructions | P1 | Useful but not blocking current workflows |
| 2 | Behavioral compliance testing | P2 | Complex to implement, needs P0 validation foundation first |

---

### Cut Items

| # | Item | Reason for Cutting |
|---|------|--------------------|
| 1 | Runtime deduplication | Premature optimization. Current instruction overlap is manageable. Revisit if token costs become measurably problematic. |

---

## 📝 Key Insights

### Architectural Principles Affirmed

1. **Platform-agnostic core**: VS Code optimizations must be optional overlays, not core requirements
2. **Validation before sophistication**: Enforce existing rules before adding new complexity
3. **Negative guidance value**: "When NOT to use" is as valuable as "when to use" for discoverability

### Open Questions (Future Exploration)

- Should token budgets be calculated dynamically or statically annotated?
- Can flow_core eventually subsume skill discovery patterns?
- What's the threshold for "too many skills loaded" that warrants lazy loading?

---

## 📌 Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Create MCP/CLI tool to validate instruction line limits | HyperSan | ⏳ [TODO] |
| 2 | Define token annotation format and add to instruction template | HyperArch | ⏳ [TODO] |
| 3 | Design optional platform profile schema for agent/instruction templates | HyperAgentSmith | ⏳ [TODO] |
| 4 | Create SKILLS_INDEX.md with discovery guidance and anti-patterns | HyperDream | ⏳ [TODO] |
| 5 | Create instruction layering audit tool (adhd_mcp extension) | HyperArch | ⏳ [TODO] |
| 6 | Blueprint: Instruction optimization vision document | HyperDream | ⏳ [TODO] |

---

## 🔗 Related Documents

| Document | Relevance |
|----------|-----------|
| `.github/skills/` | Skill files that need discovery index |
| `.github/instructions/` | Instruction files subject to line limits |
| `modules/dev/adhd_mcp/` | MCP extension point for audit tools |
| `.github/instructions/instructions_format.instructions.md` | Format spec needing token annotations |
