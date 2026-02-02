# Embedded Template Implementation

**Type:** design  
**Related Feature:** [02 - Architecture](../02_architecture.md), [03 - Project Creation](../03_feature_project_creation.md), [04 - Module Creation](../04_feature_module_creation.md)  
**Status:** `✅ [DONE]`

---

## Context

This asset documents the actual implementation approach for "embedded templates" as completed in P0. The original vision called for Python string constants embedded directly in creator code. The actual implementation uses a **hybrid approach** with **local template files**.

---

## The Artifact

### Approach: File-Based Templates (Not String Constants)

| Component | Location | Template Files |
|-----------|----------|----------------|
| Project Creator | `project_creator_core/data/templates/` | `pyproject.toml.template`, `gitignore.template`, `readme.md.template`, `app.py.template` |
| Module Creator | `module_creator_core/data/templates/` | `pyproject.toml.template`, `init.py.template`, `main_module.py.template`, `readme.md.template`, `config.template`, `instructions.md.template` |

### Why File-Based Over String Constants?

| Aspect | String Constants | File-Based Templates ✅ |
|--------|------------------|-------------------------|
| Readability | Multi-line strings in Python are awkward | Clean, syntax-highlighted template files |
| Editing | Must escape special chars, hard to preview | Edit naturally, use IDE preview |
| Version Control | Changes mixed with code changes | Template changes isolated in diffs |
| Tooling | No template tooling support | Can use template-specific tools/linting |

### Template Loading Pattern

```python
# Common pattern in both creators:
TEMPLATES_DIR = Path(__file__).parent / "data" / "templates"

def _load_template(name: str) -> str:
    """Load a template file from the templates directory."""
    template_path = TEMPLATES_DIR / name
    if not template_path.exists():
        raise ADHDError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")
```

### Key Benefits Achieved

1. **No External Repos** - Templates live in module's `data/templates/` folder
2. **No Cloning** - `_load_template()` reads local files, instant operation
3. **No Network Dependency** - Works offline, no GitHub rate limits
4. **Easy Customization** - Edit `.template` files without touching Python code
5. **PEP 621 Compliant** - All pyproject.toml templates follow standard format

### Template Variables

Templates use Python `str.format()` placeholders:

| Variable | Used In | Description |
|----------|---------|-------------|
| `{project_name}` | Project templates | The project name |
| `{description}` | All templates | User-provided description |
| `{module_name}` | Module templates | The module name |
| `{module_type}` | Module templates | core/manager/util/plugin/mcp |
| `{class_name}` | Module templates | PascalCase version of module_name |

---

## Constraints

- Templates MUST follow PEP 621 format for pyproject.toml
- Template variables use `str.format()` syntax (not Jinja2)
- Each creator module owns its templates (no shared template repo)

---

## Deprecated Items (P3 Cleanup)

| File | Status | Notes |
|------|--------|-------|
| `project_creator_core/templates.py` | `DEPRECATED_P3` | Old external template loading logic |
| `project_creator_core/preload_sets.py` | `DEPRECATED_P3` | No longer used - projects start empty |
| `project_creator_core/data/project_templates.yaml` | `DEPRECATED_P3` | External template URLs no longer used |
| `project_creator_core/data/module_preload_sets.yaml` | `DEPRECATED_P3` | Preload feature eliminated |

**P3 Cleanup Tasks:**

- [ ] Delete `templates.py` from `project_creator_core`
- [ ] Delete `preload_sets.py` from `project_creator_core`
- [ ] Delete `project_templates.yaml` and `module_preload_sets.yaml`
- [ ] Remove deprecated `create_from_template()` method from `ProjectCreator`

---

## Related Features

- [02 - Architecture](../02_architecture.md) — Architectural decision context
- [03 - Project Creation](../03_feature_project_creation.md) — Uses embedded templates
- [04 - Module Creation](../04_feature_module_creation.md) — Uses embedded templates
- [80 - Implementation](../80_implementation.md) — Task tracking reference
