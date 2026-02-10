# FLOW Template Experiment Findings

## Experiment Overview

Tested refactoring HyperSan agent to use:
1. `style.title` for workflow steps
2. Agent template with slot-based composition

## Part 1: style.title for Workflow Steps

### Finding: Not Ideal for Nested Headers

**Problem**: `style.title` uses layer-based heading levels:
- Layer 0 = H1 (`#`)
- Layer 1 = H2 (`##`)
- etc.

The workflow steps in the original agent use `### N. **TITLE**` (H3) format consistently. When defined as separate nodes at layer 0, they rendered as H1 instead.

**Issue with numbered titles**: Values like `0. SELF-IDENTIFICATION` starting with a number need to be quoted with string delimiters:
```flow
# FAILS: Parser sees "0" as number literal
|style.title=0. SELF-IDENTIFICATION

# WORKS: Quote with string delimiters  
|style.title=<<<0. SELF-IDENTIFICATION>>>
```

### Recommendation

For **content that needs consistent heading levels regardless of nesting**, use inline markdown headers:
```flow
@workflow
|style.wrap=xml|style.tag=workflow
|<<<
### 0. **SELF-IDENTIFICATION**
Content...

### 1. **Next Step**
Content...
>>>|.
```

`style.title` is best for **top-level sections** where layer 0 = H1 is appropriate.

---

## Part 2: Forward References in Templates

### Finding: Inline Forward Refs Add Newlines

**Problem**: Composing forward refs inline with string literals causes unwanted newlines:
```flow
# Template has:
|<<<You are in ">>>|^agent_mode_name|<<<" mode.>>>|

# Output has unexpected newlines:
You are in "
HyperSan
" mode.
```

**Cause**: The resolver concatenates content blocks, and the forward ref content gets its own block with trim behavior, causing line breaks.

### Solution

Avoid inline forward refs in templates. Instead, have the slot provide the full line:
```flow
# Template:
@modeInstructions
|style.wrap=xml|style.tag=modeInstructions
|^agent_mode_intro_line|<<
>>|$mode_content
|.

# Agent file:
@agent_mode_intro_line |<<<You are currently running in "HyperSan" mode...>>>|.
```

---

## Part 3: Template Architecture

### Finding: Import Order Matters

Templates that use backward references (`$`) to library nodes must be imported AFTER those library files:

```flow
# CORRECT ORDER:
+./lib/patterns/stopping_rules_base.flow |.  # Defines @stopping_rules_base
+./lib/patterns/core_philosophy.flow |.       # Defines @core_philosophy
+./lib/templates/adhd_agent.flow |.           # Uses $stopping_rules_base, $core_philosophy

# WRONG: Template imported first will fail on $stopping_rules_base
+./lib/templates/adhd_agent.flow |.
+./lib/patterns/stopping_rules_base.flow |.
```

### Template Design Pattern

The template CANNOT contain imports for its dependencies. The importing file must:
1. Import all library files (patterns, provider, adhd)
2. Import the template
3. Define slots
4. Reference `$agent_output`

---

## Comparison: Original vs Template-Based

| Metric | Original (v1) | Template-Based (v3) |
|--------|---------------|---------------------|
| **Source Lines** | 185 | 146 |
| **Reduction** | - | **21% fewer lines** |
| **Compiled Lines** | 134 | 138 |
| **Semantic Diff** | - | **Equivalent** (only blank line differences) |

### Benefits of Template Approach

1. **DRY**: Composition logic defined once in template
2. **Consistency**: All agents follow same structure
3. **Maintainability**: Update template to change all agents
4. **Clarity**: Agent file focuses only on agent-specific content

### Template Files Created

- `lib/templates/adhd_agent.flow` - 131 lines (reusable composition template)

---

## FLOW Limitations Discovered

1. **`style.title` layer dependence**: Cannot specify fixed heading level
   - Workaround: Use inline markdown headers

2. **Inline forward refs in strings**: Add unwanted newlines
   - Workaround: Have slot provide full line/section

3. **Template import order**: Templates using `$` refs need libraries imported first
   - This is by design (lexical scoping), but can be confusing

4. **No conditional slots**: Empty slots (`|<<<>>>|.`) still add content
   - Workaround: Define empty placeholder nodes

---

## Recommendations for FLOW Improvements

### High Priority
1. Add `style.level=N` to force specific heading level for `style.title`
2. Document inline forward ref behavior and workarounds

### Medium Priority
3. Consider allowing templates to declare (but not import) dependencies
4. Add conditional composition: `|?^slot` (include only if slot non-empty)

### Low Priority  
5. Add `style.heading=raw` to preserve original heading syntax in content
