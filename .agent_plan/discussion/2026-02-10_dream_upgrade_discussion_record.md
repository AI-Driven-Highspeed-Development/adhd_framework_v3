# Discussion Record: Upgrade day_dream system with DREAM v3 integration

| Field        | Value                                                  |
| ------------ | ------------------------------------------------------ |
| Topic        | Upgrade day_dream system with DREAM v3 integration     |
| Date         | 2026-02-10                                             |
| Participants | HyperArch, HyperDream, HyperAgentSmith                |
| Rounds       | 1                                                      |
| Status       | Consensus ✅                                            |

---

## Round 1

### PROPOSE Phase

- **HyperArch:** Adopt DREAM's context isolation + sibling firewall, flatten folder layout to uniform shape. Merge node.yaml/contract.yaml into single spec.yaml. Gate DREAM structure by magnitude (Light = single spec, Standard+ = full decomposition). AI-agent time estimates with human_only flag. Risk: ceremony creep recreating walking-skeleton problem at meta level.
- **HyperDream:** Merge current Story/Spec with DREAM's best parts. Discard node.yaml/contract.yaml split, "node" terminology (use plans/tasks), L0-L4 hierarchy. Fix 3 systemic biases: human estimates, backward-compat posture, forced walking skeleton. Walking skeleton opt-in for cross-boundary integration risk only.
- **HyperAgentSmith:** Three surgical updates to existing skills. Absorb DREAM into new dream-planning skill. Replace "node" with clearer term. Current templates stay as rendering target. Skill provides deterministic create/update/decompose protocol.

### CHALLENGE Phase

- **HyperArch → Smith:** Keeping templates as immutable render target creates split-brain (skill defines protocol, templates define shape, they'll drift). Uniform structure = one thing to maintain.
- **HyperDream → Arch:** Uniform folder-per-unit front-loads ceremony, violating simple-P0 principle. Two-task plan shouldn't need same scaffolding as twelve-unit blueprint. Complexity should scale with magnitude.
- **HyperAgentSmith → Arch:** Templates aren't a second brain — they're rendering targets like compiler output. Skill owns protocol; templates are scaffolds. Any design has this boundary — theirs makes it explicit and human-editable.

### SYNTHESIZE Phase — Consensus Reached

1. **Terminology:** "plan" (has children) + "task" (leaf). plan.yaml for metadata. .task.md for specs. No "node/unit/block".
2. **Magnitude-gated structure:** Simple (Trivial/Light) = single file. Blueprint (Standard+) = full decomposition with DREAM isolation.
3. **DREAM adopted:** Context isolation, sibling firewall, magnitude routing. L0-L4 discarded.
4. **Fixes:** AI-agent time estimates (default), conditional walking skeleton, clean-code-first directive, folder-separated compat paths.
5. **Architecture:** New dream-planning skill (protocol). Updated day-dream skill (fixes). Templates = passive scaffolds.

### Votes

| Agent          | Vote   | Reason                                                       |
| -------------- | ------ | ------------------------------------------------------------ |
| HyperArch      | ACCEPT | Skill-as-authority mitigates drift risk                      |
| HyperDream     | ACCEPT | Clean separation, adopts DREAM without over-engineering      |
| HyperAgentSmith| ACCEPT | Protocol/template separation produces clearer instructions   |

---

## Outcome

Blueprint set created at `.agent_plan/day_dream/blueprint/` using current existing templates. The blueprint implements the consensus decisions from this discussion.
