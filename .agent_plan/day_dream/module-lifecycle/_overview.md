# Module Lifecycle — Remove & Update Commands

> ⏳ **[TODO]** — Add `adhd remove` and `adhd update` commands to complete the module lifecycle.

---

## Purpose

The ADHD CLI currently supports `adhd add` to bring external modules into a workspace, but has no way to remove or update them. This plan adds the reverse operations: `adhd remove <name>` to cleanly unregister and delete a module, and `adhd update <name>` to swap a module with its latest version using a safe atomic-swap pattern. Batch update via `--layer` is also included.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| [executive-summary.md](./executive-summary.md) | Task | ⏳ [TODO] | Vision, goals, non-goals, prior art |
| [architecture.md](./architecture.md) | Task | ⏳ [TODO] | System design — module lifecycle data flow |
| [p0-prerequisites/](./p0-prerequisites/_overview.md) | Plan | ⏳ [TODO] | P0: Reverse dep lookup + pyproject_patcher remove |
| [p1-core-commands/](./p1-core-commands/_overview.md) | Plan | ⏳ [TODO] | P1: Remove, Update, Safety features |
| [p2-batch-operations/](./p2-batch-operations/_overview.md) | Plan | ⏳ [TODO] | P2: Batch update with `--layer` flag |
| [implementation.md](./implementation.md) | Task | ⏳ [TODO] | Phased task tracking |
| [module-structure.md](./module-structure.md) | Task | ⏳ [TODO] | Module organization — extending `module_adder_core` |
| [cli-commands.md](./cli-commands.md) | Task | ⏳ [TODO] | CLI interface reference |

## Integration Map

```mermaid
flowchart TB
    ES[executive-summary.md] --> ARCH[architecture.md]
    ARCH --> P0[p0-prerequisites/]
    P0 --> P1[p1-core-commands/]
    P1 --> P2[p2-batch-operations/]
    P0 --> IMPL[implementation.md]
    P1 --> IMPL
    P2 --> IMPL
    ARCH --> MOD[module-structure.md]
    ARCH --> CLI[cli-commands.md]
```

Phases are sequential: P0 prerequisites → P1 core commands → P2 batch operations.

## Reading Order

1. [executive-summary.md](./executive-summary.md) — Understand the what/why
2. [architecture.md](./architecture.md) — System design and data flow
3. [cli-commands.md](./cli-commands.md) — CLI interface reference
4. [p0-prerequisites/](./p0-prerequisites/_overview.md) — Foundation work
5. [p1-core-commands/](./p1-core-commands/_overview.md) — Core remove + update
6. [p2-batch-operations/](./p2-batch-operations/_overview.md) — Batch update
7. [implementation.md](./implementation.md) — Task tracking
8. [module-structure.md](./module-structure.md) — Where code lives
