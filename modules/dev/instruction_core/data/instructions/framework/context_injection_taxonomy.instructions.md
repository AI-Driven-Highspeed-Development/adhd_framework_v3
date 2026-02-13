---
applyTo: "**/*.md,**/*.py"
---

# Context Injection Taxonomy

## Umbrella Term

Use **context injection files** as the umbrella term for all AI context artifacts injected into agent workflows.

## 3-Axis Taxonomy

### 1) Agent Axis (`.agent.md`)

- Defines **perspective**: personality, tone, authority boundaries, and stopping rules.
- Answers: *"Who am I and how should I behave?"*

### 2) Instruction Axis (`.instructions.md`)

- Defines **truth constraints**: framework rules, policies, formats, and shared standards.
- Answers: *"What is universally true or required?"*

### 3) Skill Axis (`SKILL.md`)

- Defines **procedure**: workflow SOPs, execution checklists, and repeatable methods.
- Answers: *"How do I execute this workflow step-by-step?"*

## Decision Rule

Move **Instruction → Skill** **iff** content is **exclusive to a single-agent workflow**.

- Single-agent workflow only → **MIGRATE** to skill
- Multi-agent or universal framework truth → **STAY** as instruction

## Concrete Examples from P0 Audit

### STAY examples (multi-agent / universal)

- `adhd_framework_context.instructions.md` → STAY (framework-wide truth for all agents)
- `config_manager.instructions.md` → STAY (shared coding constraints across implementation/review agents)
- `exceptions.instructions.md` → STAY (shared error policy across coding/review agents)
- `agent_common_rules.instructions.md` → STAY (common baseline for all `.adhd.agent.md` flows)

### MIGRATE examples (single-agent workflow)

- `module_development.instructions.md` → MIGRATE (HyperArch-exclusive implementation workflow)
- `mcp_development.instructions.md` → MIGRATE (HyperArch-exclusive MCP workflow)
- `hyper_san_output.instructions.md` → MIGRATE (HyperSan-exclusive output contract)
- `agents_format.instructions.md` → MIGRATE (HyperAgentSmith-exclusive authoring workflow)

## Boundary: Module-Local Instructions

Module-local instructions remain **module-local source-of-truth** and are not re-homed by this taxonomy decision.

- Keep module-local authoring/editing at the module path.
- Centralized taxonomy governs framework-level placement decisions, not module ownership transfer.
