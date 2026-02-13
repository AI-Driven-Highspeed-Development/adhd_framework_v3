---
name: shared_parsing_infrastructure
magnitude: Light
status: TODO
---

# Shared Parsing Infrastructure

## Intent

Build the shared library layer that all `dream_mcp` commands consume: YAML frontmatter parser, recursive plan tree scanner, and structured output formatter. This is the foundation — no command works without it.

## Acceptance Criteria

- [ ] `frontmatter_parser.py` — parses YAML frontmatter from `_overview.md` files, returns typed dict with all §2.1 fields
- [ ] `tree_scanner.py` — recursively walks `.agent_plan/day_dream/`, returns list of Plan/Task nodes with metadata
- [ ] `output_formatter.py` — renders structured box-drawing output (matches §13.2 format examples)
- [ ] All three modules importable with no external deps beyond `pyyaml`
- [ ] Unit tests cover: valid frontmatter, missing fields, malformed YAML, empty directories

## Constraints

- `[KNOWN]` — stdlib + pyyaml, standard filesystem patterns
- Parser must handle both required and optional frontmatter fields gracefully
- Scanner must distinguish Plan (directory with `_overview.md`) from Task (`.md` file)
- Scanner must skip `_templates/`, `_completed/`, `_tree.md`

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| p03 skeleton | Pending | Module directory must exist |
