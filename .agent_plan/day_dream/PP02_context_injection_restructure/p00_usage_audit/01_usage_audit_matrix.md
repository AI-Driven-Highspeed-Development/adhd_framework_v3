# P00 — Usage Audit Matrix (Two-Scope Inventory)

> Part of [PP02 — Context Injection Files Restructuring](../_overview.md)

---

## Decision Rule Used

- **Instruction → Skill** iff the content is **exclusively consumed by one agent workflow**.
- **STAY as instruction** when content is **multi-agent or universal framework truth**.

---

## Inventory A — Centralized Source (Baseline for P0): 11

Source root: `modules/dev/instruction_core/data/instructions/`

1. `framework/adhd_framework_context.instructions.md`
2. `framework/non_vibe_code.instructions.md`
3. `formats/instructions_format.instructions.md`
4. `formats/prompts_format.instructions.md`
5. `formats/flow_format.instructions.md`
6. `modules/mcp_development.instructions.md`
7. `modules/modules_readme.instructions.md`
8. `modules/module_development.instructions.md`
9. `modules/module_instructions.instructions.md`
10. `agents/hyper_san_output.instructions.md`
11. `agents/agents_format.instructions.md`

---

## Inventory B — Runtime-Visible in `.github/instructions/` (Acceptance Scope): 17

Acceptance scope is explicitly **runtime-visible files** after P1 sync:

- **16 pre-existing runtime-visible instruction files**
- **+1 new taxonomy file from P1** (`context_injection_taxonomy.instructions.md`)

Runtime-visible inventory groups:

- **Centralized-synced** (11): mirrors Inventory A
- **Module/flow-synced extras** (5): `agent_common_rules`, `cli_manager`, `config_manager`, `exceptions`, `logger_util`
- **P1 addition** (1): `context_injection_taxonomy`

---

## Classification Matrix (Runtime Acceptance Scope = 17)

| File | Location/Scope | applyTo or sync source | Consumers | STAY/MIGRATE | Rationale |
|------|----------------|------------------------|------------------|--------------|-----------|
| `adhd_framework_context.instructions.md` | centralized + runtime | Source: centralized/framework; broad framework context | All agents | STAY | Universal framework truth; not single-agent |
| `non_vibe_code.instructions.md` | centralized + runtime | `modules/**/*.py,project/**/*.py,*.py` | HyperArch, HyperSan, HyperIQGuard | STAY | Cross-agent coding guardrails |
| `instructions_format.instructions.md` | centralized + runtime | `**/*.instructions.md` | HyperAgentSmith | MIGRATE | Single-agent authoring workflow |
| `prompts_format.instructions.md` | centralized + runtime | `**/*.prompt.md` | HyperAgentSmith | MIGRATE | Single-agent prompt-authoring SOP |
| `flow_format.instructions.md` | centralized + runtime | `**/*.flow` | HyperAgentSmith | MIGRATE | Single-agent flow-authoring SOP |
| `mcp_development.instructions.md` | centralized + runtime | `modules/**/*_mcp.py` | HyperArch | MIGRATE | Exclusive implementation workflow |
| `modules_readme.instructions.md` | centralized + runtime | `modules/**/README.md` | HyperAgentSmith, HyperDream | STAY | Multi-agent documentation workflow |
| `module_development.instructions.md` | centralized + runtime | `modules/**/*.py` | HyperArch | MIGRATE | Exclusive implementation workflow |
| `module_instructions.instructions.md` | centralized + runtime | `modules/**/*.instructions.md` | HyperAgentSmith | MIGRATE | Exclusive instruction-authoring workflow |
| `hyper_san_output.instructions.md` | centralized + runtime | `**/hyper_san_checker.adhd.agent.md` | HyperSan | MIGRATE | Exclusive HyperSan output contract |
| `agents_format.instructions.md` | centralized + runtime | `**/*.agent.md` | HyperAgentSmith | MIGRATE | Single-agent agent-authoring workflow |
| `agent_common_rules.instructions.md` | runtime extra (flow-synced) | Source: `data/flows/instructions/agent_common_rules.flow` | All `.adhd.agent.md` agents | STAY | Shared baseline rules across agents |
| `cli_manager.instructions.md` | runtime extra (module-synced) | `modules/**/*_cli.py` | HyperArch | MIGRATE | Exclusive implementation pattern |
| `config_manager.instructions.md` | runtime extra (module-synced) | `modules/**/*.py,project/**/*.py,*.py` | HyperArch, HyperSan, HyperIQGuard | STAY | Shared coding constraints |
| `exceptions.instructions.md` | runtime extra (module-synced) | `modules/**,project/**,**.py` | HyperArch, HyperSan, HyperIQGuard | STAY | Shared error-handling policy |
| `logger_util.instructions.md` | runtime extra (module-synced) | `modules/**/*.py,project/**/*.py,*.py` | HyperArch, HyperSan, HyperIQGuard | STAY | Shared logging policy |
| `context_injection_taxonomy.instructions.md` | centralized + runtime (P1) | `**/*.md,**/*.py` | All agents and contributors | STAY | Canonical taxonomy/decision-rule source |

---

## Module-Local Boundary (Explicit)

- Module-local instruction files remain **module-local source-of-truth**.
- This audit and classification scope targets centralized/runtime framework instruction visibility only.

---

## Acceptance Clarification (Mismatch Resolved)

- **P0 baseline centralized count** is unambiguously **11**.
- **Runtime acceptance count** is unambiguously **17** after P1 sync (16 existing + taxonomy file).
- This dual-scope definition resolves prior ambiguity around “all 17 instruction files.”
