# Required Content After Frontmatter

Every `_overview.md` must include the following sections after YAML frontmatter:

```markdown
# {Plan Name}

## Purpose
Why this plan exists and what it delivers.

## Children

| Name | Type | Status | Description |
|------|------|--------|-------------|
| 01_login_flow.md | Task | ⏳ [TODO] | Login endpoint |
| auth_tokens/ | Plan | 🔄 [WIP] | Token lifecycle |

⚠️ **Type column:** ONLY `Plan` (directory) or `Task` (file) are valid values. 'Doc', 'Feature', 'Module', etc. are INVALID.

## Integration Map
How children's outputs combine into the plan's deliverable.

## Reading Order
1. 01_login_flow.md (independent)
2. auth_tokens/ (depends on login)
```
