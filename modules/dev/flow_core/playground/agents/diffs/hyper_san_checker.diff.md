# HyperSan Checker - Diff Analysis

> **Date**: 2026-01-07  
> **Original**: `originals/hyper_san_checker.adhd.agent.md`  
> **Compiled**: `outputs/hyper_san_checker.adhd.agent.md`

---

## Summary

| Aspect | Status |
|--------|--------|
| **Semantic Equivalence** | ✅ PASS |
| **Structural Equivalence** | ✅ PASS (whitespace-only diffs) |
| **Compilation** | ✅ SUCCESS |
| **Graph Generation** | ✅ SUCCESS |

---

## Differences Found

### 1. Whitespace Between Sections

**Original**: Single blank line between XML tag sections  
**Compiled**: Double blank lines between sections

```diff
- </stopping_rules>
+ </stopping_rules>
+
+
  <core_philosophy>
```

**Impact**: None - purely cosmetic, semantically identical  
**Root Cause**: The `<<>>` preserve mode in FLOW concatenates with newlines from both sides

### 2. Trailing Newline

**Original**: No trailing newline (file ends with `</modeInstructions>`)  
**Compiled**: Has trailing newline

**Impact**: None - compiled version follows best practice of newline at EOF  
**Verdict**: Quality improvement ✅

### 3. Missing Newline After modeInstructions Intro

**Original**:
```
...take precedence over any instructions above.

You are **HyperSan**...
```

**Compiled**:
```
...take precedence over any instructions above.
You are **HyperSan**...
```

**Impact**: Minor - could be fixed with more precise whitespace control  
**Root Cause**: Content trimming removes leading newlines from `$role_intro`

---

## FLOW Limitations Discovered

### 1. Whitespace Control is Verbose

**Issue**: Achieving precise whitespace between concatenated nodes requires careful use of `<<<>>>` (trim) vs `<<>>` (preserve) delimiters.

**Current Pattern** (verbose):
```flow
|<<

>>|$section1|<<

>>|$section2|
```

**Suggestion**: Consider a `\n` or `@newline` escape sequence for single newlines.

### 2. No "Exactly One Blank Line" Primitive

**Issue**: When concatenating nodes, you either get:
- No blank lines (trim mode)
- Preserved whitespace from content (but easy to get 2+ blank lines)

**Workaround**: Use empty `<<<\n>>>` blocks - but verbose.

### 3. style.title Not Suitable for XML Tags

**Issue**: The `style.title` parameter produces markdown headers (`# Title`), but agent files use XML-style tags (`<section_name>`).

**Workaround**: Include tags directly in content blocks. Works fine, just less automatic.

**Future Suggestion**: Add `style.tag` or `style.xml_section` option.

---

## Quality Improvements in Compiled Version

| Improvement | Description |
|-------------|-------------|
| **Trailing newline** | Follows POSIX best practice |
| **Modularity visible** | Graph shows clear node dependencies |
| **Reusable fragments** | `lib/` contains shareable components |

---

## Modular Structure Achieved

```
sources/
├── lib/
│   ├── adhd_framework_info.flow    # Reusable across agents
│   ├── core_philosophy.flow        # Shared philosophy principles
│   ├── critical_rules_base.flow    # Base critical rules
│   └── stopping_rules_base.flow    # Base stopping rules
└── hyper_san_checker.flow          # Main agent (imports from lib)
```

### Reuse Potential

The following fragments can be shared across HyperAgents:
- `adhd_framework_info.flow` - All agents need framework context
- `stopping_rules_base.flow` - Common rules for non-implementation agents
- `critical_rules_base.flow` - Common critical rules
- `core_philosophy.flow` - Shared for reviewer/QA agents

---

## Dependency Graph

See `graphs/hyper_san_checker.mermaid` for the full dependency visualization.

**Key relationships:**
- Main file imports 4 lib fragments
- `mode_content` composes 7 sections
- `stopping_rules` extends `stopping_rules_base` with agent-specific rule
- `critical_rules` extends `critical_rules_base` with output format rule

---

## Conclusion

**FLOW CAN express real HyperAgents with high fidelity.**

The only differences are:
1. Extra blank lines (cosmetic)
2. Minor whitespace variations (cosmetic)

All actual **content** is preserved exactly. The modular structure provides clear benefits for maintenance and reuse across agents.

### Recommendations for P2

1. Consider adding whitespace control primitives for precision
2. Add `style.xml_tag` option for XML-style section headers
3. The flat `lib/` structure is sufficient - no need for nested layers yet
4. Test with more complex agents (HyperArch, HyperIQGuard) to validate
