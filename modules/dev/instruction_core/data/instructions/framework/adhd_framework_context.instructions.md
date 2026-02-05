# ADHD Framework Context

## Why This Framework Exists
AI agents hit a **Context Wall** as complexity grows. This framework solves it via:
- **Fractal Modularity**: Small, single-responsibility modules. Agents load only what they need.
- **Deterministic Lifecycle**: Init bootstraps, Refresh self-heals.
- **AI-Native Context**: `.instructions.md` files teach agents the "how" alongside code.

## Core Philosophy
1. **Read Before Write**: NEVER guess. Read docs/source first.
2. **Reuse, Don't Reinvent**: Check existing modules before implementing.
3. **Consistency**: MIMIC existing style exactly.
4. **Single Responsibility**: One module = one job.
5. **Understand the Why**: Know *why* patterns exist.

## Project Structure
- **Directories**:
  - `project/`: App code. `project/data/`: App data (use Config-Manager paths).
  - `modules/foundation/`: Bootstrap-time modules (no ADHD deps).
  - `modules/runtime/`: Normal operational modules (most modules).
  - `modules/dev/`: Development/testing tools only.
  - `tests/`: Project-level integration tests. `tests/integration/` for cross-module tests.
  - `playground/`: Project-level exploration, demos, prototypes.
  - `.temp_agent_work/`: Agent workspace, MUST clean up after. Never commit.
  - `.agent_plan/`: Agent planning artifacts. `day_dream/` for visions, `red_team/` for HyperRed.
- **Entry Points**: `adhd_framework.py` (framework CLI), `<app_name>.py` (app).
- **Module Assets** (`modules/<layer>/<name>/`):
  - `__init__.py`, `pyproject.toml`, `.config_template`, `data/`, `refresh.py`
  - `<name>.instructions.md`, `requirements.txt` (PyPI only)
  - `tests/` (optional), `playground/` (optional)

## Module Taxonomy

### Layers (Required)
Every module declares a `layer` in `pyproject.toml` indicating when it loads:

| Layer | Purpose | When to Use |
|:---|:---|:---|
| **foundation** | Core infrastructure, no ADHD deps | Bootstrap-time modules |
| **runtime** | Normal operational modules | Most modules (default choice) |
| **dev** | Development/testing tools only | Build tools, test utilities |

### Folders (Derived from Path)
Folder location determines module category - no explicit `type` field needed:

| Folder | Purpose | When |
|:---|:---|:---|
| `cores/` | Framework internals | NEVER create unless extending framework |
| `managers/` | Stateful singletons, coordination | Needs state/lifecycle |
| `utils/` | Stateless pure functions | No state |
| `plugins/` | Project-specific extensions | Only for THIS project |
| `mcps/` | AI tool integrations | Extending agent capabilities |

### MCP Flag (Optional)
MCP servers add `mcp = true` in `[tool.adhd]` to enable special handling.

**Decision**: State? → `managers/`. Stateless? → `utils/`. Reusable? → `managers/`. Project-only? → `plugins/`.

## Module Naming
- **Suffix matches folder**: `*_manager`, `*_util`, `*_plugin`, `*_core`, `*_mcp`
- **Snake_case**, specific, descriptive
- ✅ `oauth2_auth_manager` ❌ `auth`

## Reusable vs Project-Specific Modules

Modules fall into two categories based on **reusability across projects**:

### Reusable (Generic) Modules
**No project-specific knowledge**, can copy to other ADHD projects:

| Pattern | Examples |
|:---|:---|
| Generic terms | `auth_manager`, `session_manager`, `rss_monitor_plugin` |
| Technology-specific | `torrent_client_plugin`, `external_media_manager` |
| Common patterns | `notification_plugin`, `cache_manager` |

### Project-Specific Modules
**Domain logic unique to this project**, name indicates context:

| Pattern | Examples |
|:---|:---|
| Domain prefix | `anime_download_manager`, `video_stream_manager` |
| Project prefix | `animenest_webui_plugin`, `animenest_cli_plugin` |
| Feature-specific | `anime_library_scanner_plugin`, `syoboi_api_plugin` |

### The Reusability Test
*"In a list of 50 modules from different projects, do I know what it does AND which project it belongs to?"*
- **Reusable**: Generic name → reuse anywhere
- **Project-Specific**: Includes domain/project context

### Abstraction Pattern
Extract generic layers from project-specific features, e.g.:
```
Generic module: external_media_manager (scanning, indexing)
Used by --> anime_library_scanner  or  photo_library_scanner (Project: domain parsing)
```

## AI-Native Context System
`instruction_core` syncs to `.github/` for VS Code Copilot:
- **Source**: `cores/instruction_core/data/`, `<module>/<name>.instructions.md`
- **Dest**: `.github/instructions/`, `.github/agents/`, `.github/prompts/`
- **Trigger**: `./adhd_framework.py refresh`
