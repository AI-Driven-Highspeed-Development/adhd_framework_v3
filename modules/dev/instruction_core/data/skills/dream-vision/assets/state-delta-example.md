# State Deltas

Append-only entries in root `_overview.md` logging codebase changes when a plan closes. **Gate condition** — a plan CANNOT mark ✅ DONE without appending one.

```markdown
## State Deltas

### ✅ PP{NN}_{name} — {Mon YYYY}
- {module}: {what changed}
- {new_module}: new module, {purpose}
```

| Rule | Detail |
|------|--------|
| Active cap | 20 most recent entries in root `_overview.md` |
| Overflow | Oldest moves to `_state_deltas_archive.md` (auto-generated, NEVER hand-maintained) |
| Format | `{module}: {what changed}` per line |
