# STOP POINT 1: Pre-Execution Confirmation

**Present to user:**

```markdown
## 📋 EXPEDITION MANIFEST

**Target:** [path]
**Framework:** [detected]
**Artifacts:** [count] files in [chunk_count] chunks

### Will Create in Target:
- `.github/agents/` → [count] agents
- `.github/instructions/` → [count] instructions
- `.vscode/mcp.json` → MCP configuration
- `CONTRIBUTING.md` → Sidecar breadcrumb

### Will Create in Sidecar:
- `managers/{target}_module_registry_manager/`
- `mcps/{target}_adhd_mcp/`

**Proceed with execution?** (yes/no)
```

**Await explicit "yes" before continuing.**
