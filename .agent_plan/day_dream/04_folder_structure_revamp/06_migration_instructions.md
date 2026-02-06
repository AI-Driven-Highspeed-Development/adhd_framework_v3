# 06 - Migration: Instruction Files

> Part of [Folder Structure Revamp Blueprint](./00_index.md)

---

## 📖 The Story

### 😤 The Pain → ✨ The Vision

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE                        │  AFTER                         │
├────────────────────────────────┼────────────────────────────────┤
│  applyTo: cores/**,managers/** │  applyTo: modules/**           │
│       ↓                        │       ↓                        │
│  💥 6 patterns per file        │  ✅ 1 unified pattern          │
│       ↓                        │       ↓                        │
│  Docs mention "type"           │  Docs mention "layer"          │
└────────────────────────────────┴────────────────────────────────┘
```

### 🎯 One-Liner

> Update all 14 instruction files to use `modules/**` paths and remove type documentation.

### 📊 Quick Impact

| What Changes | Before | After |
|--------------|--------|-------|
| applyTo patterns | ❌ 6+ patterns | ✅ 1-2 patterns |
| Type documentation | ❌ Present | ✅ Removed |
| Folder taxonomy | ❌ 6 folders | ✅ 3 layers |

---

## 🔧 The Spec

---

## 🎯 Intent & Scope

**Intent:** Update all instruction files for the new folder structure

**Priority:** P4  
**Difficulty:** `[KNOWN]`

**In Scope:**
- Update `applyTo` glob patterns in all 14 files
- Remove "Folders (Derived from Path)" section from context doc
- Update "Module Taxonomy" documentation
- Remove `type` field documentation

**Out of Scope:**
- Content changes beyond structure references
- New instruction files

---

## 📁 Files to Modify

### Major Changes (Content Rewrite)

| File | Changes |
|------|---------|
| `adhd_framework_context.instructions.md` | **MAJOR** — Remove "Folders" section, update "Module Taxonomy" |
| `modules.init.yaml.instructions.md` | Remove `type` from schema |
| `module_development.instructions.md` | Update paths, remove type docs |

### Pattern Updates Only (applyTo)

| File | Current Pattern | New Pattern |
|------|-----------------|-------------|
| `config_manager.instructions.md` | `project/**,managers/**,...` | `modules/**,*.py` |
| `logger_util.instructions.md` | `project/**,managers/**,...` | `modules/**,*.py` |
| `exceptions.instructions.md` | `project/**,managers/**,...` | `modules/**,**.py` |
| `cli_manager.instructions.md` | `managers/**/*_cli.py,...` | `modules/**/*_cli.py` |
| `mcp_development.instructions.md` | `mcps/**/*.py` | `modules/**/*.py` (+ mcp filter) |
| `module_instructions.instructions.md` | `managers/**,...` | `modules/**/*.instructions.md` |
| `modules_readme.instructions.md` | `cores/**/README.md,...` | `modules/**/README.md` |
| `testing_folders.instructions.md` | `tests/**,...` | No change needed |
| Plus 3 other files | Various | `modules/**` |

---

## 🔧 Implementation Details

### 1. adhd_framework_context.instructions.md (MAJOR)

**Remove Section:**
```markdown
## Folders (Derived from Path)

| Folder | Contents |
|--------|----------|
| cores/ | Infrastructure modules... |
| managers/ | Business logic... |
...
```

**Replace With:**
```markdown
## Module Organization

All modules live in the unified `modules/` directory, organized by **layer**:

| Layer | Path | Can Import From | Removal Test |
|-------|------|-----------------|---------------|
| foundation | `modules/foundation/` | Foundation only | Remove → runtime and dev break |
| runtime | `modules/runtime/` | Foundation + runtime | Remove → dev breaks |
| dev | `modules/dev/` | Anything | Remove → nothing breaks |

> **Foundation DAG Rule**: Foundation modules may depend on other foundation modules, but must form a DAG (no cycles). They NEVER import from runtime or dev.

Layer is **derived from path** for internal modules, or read from `[tool.adhd].layer` for external modules.
```

**Update Module Taxonomy:**
- Remove references to 6-folder structure
- Replace type examples with layer examples
- Update dependency direction documentation

### 2. modules.init.yaml.instructions.md

**Remove from schema:**
```yaml
# OLD
type: manager  # core|manager|plugin|util|mcp
layer: runtime

# NEW
layer: runtime  # foundation|runtime|dev (REQUIRED)
mcp: true       # (OPTIONAL) true for MCP servers
```

### 3. applyTo Pattern Updates

**Generic Update Pattern:**
```yaml
# OLD
applyTo: "cores/**/*.py,managers/**/*.py,plugins/**/*.py,utils/**/*.py,mcps/**/*.py"

# NEW
applyTo: "modules/**/*.py"
```

**For CLI-specific:**
```yaml
# OLD
applyTo: "managers/**/*_cli.py,plugins/**/*_cli.py,utils/**/*_cli.py,mcps/**/*_cli.py"

# NEW
applyTo: "modules/**/*_cli.py"
```

---

## ✅ Acceptance Criteria

- [ ] All 14 instruction files updated
- [ ] No references to legacy folder names in applyTo
- [ ] "Folders (Derived from Path)" section removed from context doc
- [ ] `type` field documentation removed
- [ ] Module Taxonomy section updated
- [ ] All instruction files still apply correctly to modules

---

## 🔗 Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| Physical migration | internal | Can do before or after | Instructions just need correct paths |

---

## 🚀 Tasks

| Task | Difficulty | Status |
|------|------------|--------|
| Update `adhd_framework_context.instructions.md` | `[KNOWN]` | ⏳ [TODO] |
| Update `modules.init.yaml.instructions.md` | `[KNOWN]` | ⏳ [TODO] |
| Update `module_development.instructions.md` | `[KNOWN]` | ⏳ [TODO] |
| Update 11 applyTo patterns | `[KNOWN]` | ⏳ [TODO] |
| Verify instructions apply correctly | `[KNOWN]` | ⏳ [TODO] |

---

## 🧪 Verification (Manual)

| What to Try | Expected Result |
|-------------|-----------------|
| Open `modules/foundation/config_manager/config_manager.py` | Config instructions applied |
| Open `modules/my_plugin/my_cli.py` | CLI instructions applied |
| Search for "cores/" in instruction files | No matches |

---

## 📋 Full File List

```
.github/instructions/
├── adhd_framework_context.instructions.md    ← MAJOR rewrite
├── agent_common_rules.instructions.md        ← No change (agent files)
├── agents_format.instructions.md             ← No change (agent files)
├── cli_manager.instructions.md               ← Update applyTo
├── config_manager.instructions.md            ← Update applyTo
├── dream_assets.instructions.md              ← No change
├── dream_blueprint.instructions.md           ← No change
├── exceptions.instructions.md                ← Update applyTo
├── instructions_format.instructions.md       ← No change
├── logger_util.instructions.md               ← Update applyTo
├── mcp_development.instructions.md           ← Update applyTo
├── module_development.instructions.md        ← Update applyTo + content
├── module_instructions.instructions.md       ← Update applyTo
├── modules.init.yaml.instructions.md         ← Remove type from schema
├── modules_readme.instructions.md            ← Update applyTo
├── prompts_format.instructions.md            ← No change
├── python_terminal_commands.instructions.md  ← No change
└── testing_folders.instructions.md           ← No change
```

---

## ✅ Migration Validation Checklist

### Completeness
- [ ] All files reviewed
- [ ] Major content changes done
- [ ] All applyTo patterns updated

### Traceability
- [ ] Implements [01_feature_new_structure.md](./01_feature_new_structure.md)

---

**← Back to:** [Index](./00_index.md) | **Prev:** [05 - adhd_mcp + CLI](./05_migration_adhd_mcp_cli.md) | **Next:** [07 - Existing Modules](./07_migration_existing_modules.md)
