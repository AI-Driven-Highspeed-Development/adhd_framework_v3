# Agent Recreation Testing

> **Purpose**: Validate FLOW can express real HyperAgents before committing to full migration.

## Test Plan

### Objective

Recreate actual HyperAgents using FLOW syntax and compare compiled output against the original hand-written markdown. This proves the language can express real-world complexity.

### What We're Testing

1. **Expressiveness**: Can FLOW capture all structural elements of a real agent?
2. **Output Quality**: Is compiled output equivalent to (or better than) hand-written?
3. **Modularity**: Can common fragments be extracted and reused?
4. **Dependency Graphs**: Do graphs accurately reflect the agent's structure?

---

## Directory Structure

```
agents/
├── README.md                          # This file
├── originals/                         # Reference copies of original agents
│   └── hyper_san_checker.adhd.agent.md
├── sources/                           # FLOW source files
│   ├── lib/                           # Shared reusable fragments (3-layer)
│   │   ├── provider/                  # AI provider/IDE-specific format
│   │   │   └── chatagent_frontmatter.flow  # VSCode Chat Agent YAML format
│   │   ├── patterns/                  # Universal AI agent patterns
│   │   │   ├── stopping_rules_base.flow
│   │   │   ├── core_philosophy.flow
│   │   │   └── critical_rules_base.flow
│   │   └── adhd/                      # ADHD framework-specific content
│   │       └── framework_info.flow
│   └── hyper_san_checker.flow         # Main agent file
├── outputs/                           # Compiled results (.md)
│   └── hyper_san_checker.adhd.agent.md
├── graphs/                            # Dependency graphs
│   └── hyper_san_checker.mermaid
└── diffs/                             # Diff documentation
    └── hyper_san_checker.diff.md
```

### Library Layers

| Layer | Purpose | When to Modify |
|-------|---------|----------------|
| **provider/** | AI provider/IDE-specific format | When switching AI providers (VSCode → OpenAI, etc.) |
| **patterns/** | Universal AI agent structural patterns | Framework-agnostic, exportable to any project |
| **adhd/** | ADHD framework-specific rules and info | Only for this Python ADHD implementation |

**Layer Contents:**
- **provider/**: Frontmatter format, tool syntax, handoff syntax for VSCode Chat Agent
- **patterns/**: Stopping rules patterns, philosophy statements, workflow templates
- **adhd/**: Framework context, module conventions, init.yaml rules

---

## Workflow

### 1. Copy Original Agent
```bash
cp cores/instruction_core/data/agents/hyper_san_checker.adhd.agent.md \
   cores/flow_core/playground/agents/originals/
```

### 2. Create FLOW Source
Analyze the original agent and recreate using FLOW syntax:
- Use `@node` for each major section
- Extract reusable fragments to `lib/`
- Use `$ref` to compose the final agent

### 3. Compile
```bash
cd cores/flow_core/playground/agents
python ../../flow_cli.py compile sources/hyper_san_checker.flow \
    --output outputs/hyper_san_checker.adhd.agent.md
```

### 4. Generate Graph
```bash
python ../../flow_cli.py graph sources/hyper_san_checker.flow \
    --format mermaid > graphs/hyper_san_checker.mermaid
```

### 5. Document Differences
Create `diffs/<agent>.diff.md` with:
- Comparison between original and compiled
- Structural differences
- FLOW limitations discovered
- Quality improvements (if any)

---

## FLOW Syntax Quick Reference

```flow
# Node definition (content trimmed)
@node_name
|<<<
Content here
>>>|.

# Node with title
@section
|style.title=<<Section Title>>
|<<<
Content with header
>>>|.

# Reference another node
@out
|$node_name
|.

# Import from another file
+./lib/common.flow |.

# File reference (for graphs)
++./path/to/file.md
```

---

## Current Status

| Agent | Original | FLOW Source | Compiled | Diff |
|-------|----------|-------------|----------|------|
| HyperSan | ✅ | ✅ Complete | ✅ Success | ✅ Documented |
| HyperIQGuard | ❌ | ❌ | ❌ | ❌ |
| HyperArch | ❌ | ❌ | ❌ | ❌ |

---

## Findings Log

### Discovered Limitations

1. **Whitespace Control**: Precise single-blank-line control requires verbose delimiter patterns
2. **Mixed Delimiters**: Work correctly (`<<<...>>`, `<<...>>>`) but cumulative whitespace from multiple preserve blocks can cause extra blank lines
3. **style.title**: Produces markdown headers, not XML-style tags needed by agent files
4. **Graph Node IDs**: Full paths make graph verbose - could use relative paths

### Quality Improvements

1. **Modularity**: Clear 3-layer separation in `lib/` (provider, patterns, adhd)
2. **Trailing newline**: Compiled output follows POSIX best practice
3. **Dependency visibility**: Graph shows all node relationships
4. **Semantic Equivalence**: Compiled output matches original content (whitespace-only differences)
