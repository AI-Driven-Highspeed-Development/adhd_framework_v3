# 81 - Module Structure

> Part of [{Project Name} Blueprint](./00_index.md)

---

## 📖 The Story

<!--
REQUIRED: Visual, scannable narrative — NOT a text wall.
Use ASCII boxes, tables, and emoji anchors. A PM should grasp the problem/solution in 10 seconds.
If you can't draw the pain and vision, you don't understand the feature.
-->

### 😤 The Pain

<!-- What's broken? Who hurts? Show it visually! -->

```
Current Reality:
┌─────────────────────────────────────────┐
│  User wants {X}  ──────►  💥 BLOCKED 💥 │
│                                         │
│  Because: {root cause}                  │
└─────────────────────────────────────────┘
```

| Who Hurts | Pain Level | Frequency |
|-----------|------------|-----------|
| {persona} | 🔥🔥🔥 High | Daily |
| {persona} | 🔥🔥 Medium | Weekly |

### ✨ The Vision

<!-- What does success look like? Show the transformation! -->

```
After This Feature:
┌─────────────────────────────────────────┐
│  User wants {X}  ──────►  ✅ SUCCESS    │
│                                         │
│  Flow: {step} → {step} → {result}       │
└─────────────────────────────────────────┘
```

### 🎯 One-Liner

> {The elevator pitch in ONE sentence — what we're building and why it matters}

---

## 🔧 The Spec

<!-- Technical specification begins here -->

---

## 🏗️ ADHD Module Organization

<!-- 
CONSTRAINT: This document is a MUST HAVE for ADHD framework projects.
It defines the physical organization of the codebase.
-->

### 📦 Reusable Modules

<!-- 
MANDATORY SKELETON: List all reusable modules OR state "N/A — No reusable modules planned."
Modules that are generic and could be used in other projects.
Examples: cores, generic managers, utility plugins.
-->

| Module | Path | Purpose | Reuse Potential |
|--------|------|---------|------------------|
| [{Module Name}](./modules/{module_name}.md) | `{path}/` | {Brief description of its reusable purpose} | {Other projects that could use this} |

<!-- If no reusable modules: -->
<!-- N/A — All modules are project-specific. No reuse planned. -->

### 🎯 Project-Specific Modules

<!-- 
MANDATORY SKELETON: Always include.
Modules that contain logic unique to this project.
Examples: project-specific managers, specialized plugins, main app logic.
-->

| Module | Path | Purpose |
|--------|------|---------|
| [{Module Name}](./modules/{module_name}.md) | `{path}/` | {Brief description of its project-specific role} |

---

## 📂 File Tree (Proposed)

<!-- 
skip core modules, they are universal for all ADHD projects.
No need for standard files like pyproject.toml or .config_template in this diagram, because those are standard across all ADHD projects.
-->

```text
{project_root}/
├── managers/
│   └── {manager_name}/
│       ├── {manager_name}.py
│       ├── important_python_file.py
│       └── data/
│           └── some_module_owned_non_changeable_data_file
├── plugins/
│   └── {plugin_name}/
│       ├── {plugin_name}.py
│       ├── important_python_file.py
│       └── (similar structure as managers)
├── project/
│   └── data/
|       └── {module_name}/
|           └── data_files...
└── {main_app}.py
```

---

## 🔗 Module Dependencies

<!-- 
Mermaid diagram showing dependencies between modules.
-->

## 📊 Data Flow Diagram
<!-- 
Mermaid diagram showing data flow.
-->

---

## ✅ Module Structure Validation Checklist

<!-- MANDATORY: Complete before implementation phase. -->

### Completeness
- [ ] **Reusable Modules** table filled OR marked "N/A — No reusable modules"
- [ ] **Project-Specific Modules** table lists all implementation modules
- [ ] **Proposed File Tree** reflects current phase target

### Traceability  
- [ ] Each listed module has a corresponding spec in `modules/`
- [ ] Module dependencies diagram is present and accurate

---

**Next**: [Implementation](./80_implementation.md)
