# ADHDFramework Logic Extraction Blueprint

> **Goal:** `ADHDFramework` class becomes a thin dispatcher — zero business logic, zero presentation formatting.
> All domain logic moves to the modules that own it.

---

## Current State (adhd_framework.py — 966 LOC)

The `ADHDFramework` class currently mixes three concerns:

1. **CLI dispatch** — routing `args.command` to handlers (correct role)
2. **Business logic** — fuzzy-matching module names, building filters, walking dependency trees, parsing pyproject.toml, cloning repos (wrong place)
3. **Presentation** — emoji-formatted print statements, severity grouping, tree rendering (wrong place)

### Method-by-Method Audit

| Method | LOC | Logic Leak | Correct Owner |
|---|---|---|---|
| `__init__` | 12 | Instantiates QuestionaryCore, calls GithubApi.require_gh | OK (bootstrap) |
| `run` | 10 | Pure dispatch map | OK |
| `create_project_proc` | 4 | Thin delegate | OK |
| `create_module_proc` | 4 | Thin delegate | OK |
| `init_project` | 12 | uv sync + error handling + emoji output | **modules_controller_core** |
| `sync_project` | 14 | uv sync --frozen + error handling + emoji output | **modules_controller_core** |
| `migrate_modules` | 52 | Fuzzy match, single/bulk migration, result formatting | **modules_controller_core** |
| `doctor_check` | 48 | Severity grouping, formatted report rendering | **modules_controller_core** |
| `deps_check` | 50 | Module lookup, walker orchestration, tree printing | **modules_controller_core** |
| `_deps_check_all` | 52 | Full-scan violation aggregation + report | **modules_controller_core** |
| `refresh_project` | 36 | uv sync + per-module refresh + fuzzy match | **modules_controller_core** |
| `list_modules` | 32 | Filter building + formatted list output | **modules_controller_core** |
| `_add_filter_value` | 18 | Filter dimension detection | **module_filter (already exists)** |
| `show_module_info` | 30 | Module lookup + formatted info card | **modules_controller_core** |
| `update_workspace` | 52 | Visibility toggling + filter building + generation | **modules_controller_core** |
| `add_module` | 130 | Clone, validate pyproject, collision check, move, uv sync, prompt | **new: module_adder_core** |
| `_add_to_root_pyproject` | 80 | TOML string surgery to inject dependency + source | **new: module_adder_core** |

**Total logic that doesn't belong: ~600 LOC out of ~838 method LOC (72%)**

---

## Target State

```
adhd_framework.py                   # ~120 LOC: parser + thin handlers that call module APIs
  |
  +-- modules_controller_core       # gains: sync, migrate, doctor, deps, refresh, list, info, workspace CLI-facing APIs
  |     +-- module_filter            # gains: from_args() auto-detection (already partially there)
  |     +-- dependency_walker        # unchanged (already isolated)
  |
  +-- module_adder_core (NEW, dev)   # 3 acquisition modes + pyproject scaffolding + root pyproject patching
  |
  +-- creator_common_core            # QuestionaryCore extracted to its own file (questionary_prompter.py)
  +-- github_api_core                # unchanged (already owns require_gh)
```

---

## Extraction Plan

### Phase 1 — Relocate Presentation (Low Risk)

Every handler currently does its own `print(f"emoji ...")` formatting. Extract these into **formatter functions** that live next to the data they format, inside the owning module.

| Current Location | Target | New Function |
|---|---|---|
| `doctor_check` print block | `modules_controller_core/module_doctor.py` | `DoctorReport.format() -> str` |
| `deps_check` tree + violation print | `modules_controller_core/deferred/dependency_walker.py` | `DependencyClosure.format() -> str` |
| `_deps_check_all` aggregated print | same file | `format_all_violations(results) -> str` |
| `list_modules` module listing | `modules_controller_core/modules_controller.py` | `ModulesReport.format(filter) -> str` |
| `show_module_info` info card | `modules_controller_core/modules_controller.py` | `ModuleInfo.format_detail() -> str` |
| `migrate_modules` result table | `modules_controller_core/modules_controller.py` | `format_migration_results(results) -> str` |

After this phase, each handler in `ADHDFramework` becomes:
```python
def doctor_check(self, args):
    report = controller.doctor_check()
    print(report.format())
    if report.error_count > 0:
        sys.exit(1)
```

### Phase 2 — Relocate Business Logic (Medium Risk)

#### 2a. Fuzzy module lookup (repeated 5 times)

The pattern `get_module_by_name -> if not -> difflib.get_close_matches -> sys.exit` appears in:
`migrate_modules`, `refresh_project`, `show_module_info`, `update_workspace`, `deps_check`

Move to `ModulesController`:
```python
def require_module(self, name: str) -> ModuleInfo:
    """Get module or raise ADHDError with fuzzy suggestions."""
```

Callers become one-liners that catch `ADHDError`.

#### 2b. Filter building (`_add_filter_value` + 3 call sites)

`_add_filter_value` auto-detects filter dimension (layer vs. git-state). This logic belongs in `ModuleFilter`:
```python
@classmethod
def from_args(cls, mode, values) -> ModuleFilter:
    """Build filter from raw CLI string values, auto-detecting dimensions."""
```

The three call-sites in `list_modules`, `update_workspace`, and any future command collapse to:
```python
filter_obj = ModuleFilter.from_args(FilterMode.INCLUDE, args.include)
```

**Bug fix:** L472 references `normalized` which is undefined — fix during this extraction.

#### 2c. Sync / Init

`init_project` and `sync_project` both wrap `_run_uv_sync()` with error handling.
Move to `ModulesController`:
```python
def sync(self, frozen=False) -> None:
    """Run uv sync. Raises ADHDError on failure."""
```

The `_require_uv` / `_run_uv_sync` free functions and `UVNotFoundError` class at module top-level move with it (or to a small `uv_runner` utility inside modules_controller_core).

#### 2d. Refresh orchestration

`refresh_project` combines uv-sync + per-module refresh. This is pure `ModulesController` territory:
```python
def refresh(self, module_name=None, skip_sync=False) -> None:
```

#### 2e. Workspace visibility toggling

`update_workspace` contains toggle-logic that reads current visibility and flips it. This belongs in `ModulesController.generate_workspace_file` or a dedicated method:
```python
def toggle_workspace_visibility(self, module_name, mode) -> Path:
```

### Phase 3 — Extract `module_adder_core` (Higher Risk, Expanded Scope)

This is a **new dev-layer module** that replaces the current `add_module` / `_add_to_root_pyproject` methods and extends them with three acquisition modes.

See **Phase 3 Detail** section below.

### Phase 4 — QuestionaryCore file split in creator_common_core

`QuestionaryCore` is currently embedded in `creator_common_core.py` alongside git/template helpers. Since `module_adder_core` also needs it, and it has no dependency on the git/template code around it:

- Extract `QuestionaryCore` class into `creator_common_core/questionary_prompter.py`
- Keep the import in `creator_common_core/__init__.py` so existing callers are unaffected
- No new module — just a file split within `creator_common_core`

This makes `module_adder_core` depend on `creator_common_core` (both dev layer, valid) without pulling in all the template/clone functions.

---

## Phase 3 Detail — `module_adder_core`

### Rationale

`module_adder_core` lives in the **dev layer** because:
- It depends on git clone + network I/O + interactive prompts — all dev-layer concerns
- `modules_controller_core` is foundation layer and must stay network-free
- The TOML surgery in `_add_to_root_pyproject` is gnarly and deserves its own tests

### Three Acquisition Modes

The new module supports three ways to add a module:

#### Mode 1: Standalone Repository

```
adhd add https://github.com/org/some_module
```

- Clone the entire repo (shallow `--depth 1`)
- Expect `pyproject.toml` at repo root
- If `pyproject.toml` is missing: enter interactive pyproject scaffolding (see below)
- If `pyproject.toml` exists but has no `[tool.adhd]` section: prompt user for layer, inject it
- Strip `.git/` directory (and `.github/`, any CI config) but **preserve `.gitignore`**
- Move to `modules/<layer>/<module_name>/`

#### Mode 2: Monorepo Sub-folder

```
adhd add https://github.com/org/big_repo --path packages/some_module
```

New `--path` flag specifies a subfolder within the cloned repo.

- Clone the entire repo (shallow `--depth 1`)
- Extract only the specified subfolder
- Expect `pyproject.toml` at `<subfolder>/pyproject.toml`
- If `pyproject.toml` is missing at subfolder root: enter interactive pyproject scaffolding
- Same `.git` stripping rules as Mode 1
- The subfolder's own `.gitignore` is preserved if present
- Move extracted subfolder to `modules/<layer>/<module_name>/`

#### Mode 3: PyPI Package (future, blocked)

```
adhd add --pypi some-package
```

- `pip download --no-deps --no-binary :all:` or `uv pip download` the sdist
- Unpack, read `pyproject.toml`
- **Strict validation:** Must have `[tool.adhd]` section with valid `layer`. If missing, **reject** — do not prompt. Print error: "Package is not an ADHD-compatible module. [tool.adhd] section required."
- If valid: install to `modules/<layer>/<module_name>/`

> **Status: DO NOT IMPLEMENT YET.** No ADHD-compatible packages exist on PyPI. The CLI flag should be accepted but print "PyPI mode is not yet available" and exit.

### Interactive pyproject.toml Scaffolding

When Mode 1 or Mode 2 encounters a directory without `pyproject.toml`, instead of failing, prompt the user:

```
Module at <path> has no pyproject.toml. Create one interactively?
```

If yes, use `QuestionaryCore` (from `creator_common_core/questionary_prompter.py`) to collect:

| Field | Prompt | Default |
|---|---|---|
| `name` | Package name? | Inferred from folder name (snake_case) |
| `version` | Version? | `0.0.1` |
| `description` | One-line description? | (empty) |
| `layer` | Layer? (foundation/runtime/dev) | `runtime` — select prompt |
| `mcp` | Is this an MCP server module? | No — confirm prompt |
| `python_requires` | Python version? | `>=3.11` |

Then generate a minimal `pyproject.toml`:

```toml
[project]
name = "<name>"
version = "<version>"
description = "<description>"
requires-python = "<python_requires>"
dependencies = []

[tool.adhd]
layer = "<layer>"
# mcp = true  (only if user said yes)

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

This reuses the same template patterns from `module_creator_core` but is deliberately simpler — we're adopting an existing codebase, not scaffolding a new one from templates.

### Git Info Stripping Rules

When importing from git (Modes 1 & 2), the default behavior is to **sever the module from its source**:

| Item | Default | With `--keep-git` |
|---|---|---|
| `.git/` directory | **Remove** | Preserve |
| `.github/` directory | **Remove** | Preserve |
| `.gitignore` | **Preserve** | Preserve |
| `.gitmodules` | **Remove** | Preserve |
| `.gitattributes` | **Preserve** | Preserve |

**Why preserve `.gitignore`?** The project-level git reads `.gitignore` files in subdirectories. A module's `.gitignore` will correctly cause the project git to ignore that module's build artifacts, `__pycache__/`, etc. This is beneficial.

**Why preserve `.gitattributes`?** Same cascading behavior — line-ending rules, diff drivers, etc.

**The `--keep-git` flag:** For cases where the user wants to maintain the submodule's git history (e.g., contributing back upstream). When `--keep-git` is passed, nothing git-related is removed. Note: a `.git/` inside `modules/` creates a nested repo which git handles as a submodule-like entity — the user should understand this.

### Root pyproject.toml Patching

The `_add_to_root_pyproject` logic moves here with improvements:

1. Read root `pyproject.toml` with `tomllib`
2. Check for duplicates in both `dependencies` and `[tool.uv.sources]`
3. Add package to `dependencies` list
4. Add `package_name = { workspace = true }` to `[tool.uv.sources]`
5. Preserve file formatting (string manipulation, not TOML rewrite)

This is only triggered when the user confirms (via `QuestionaryCore.confirm()`) or passes `--add-to-root`.

### Module File Structure

```
modules/dev/module_adder_core/
  __init__.py                  # exports: ModuleAdder, AddModuleResult
  module_adder.py              # main class: ModuleAdder
  pyproject_patcher.py         # _add_to_root_pyproject logic
  pyproject_scaffolder.py      # interactive pyproject.toml creation
  pyproject.toml               # module metadata (layer=dev)
  tests/
    test_module_adder.py       # unit tests (mocked git, mocked filesystem)
    test_pyproject_patcher.py  # tests for root pyproject.toml surgery
    test_pyproject_scaffolder.py
```

### Public API

```python
class AddModuleResult:
    """Result of an add operation."""
    success: bool
    module_name: str
    target_path: Path
    layer: str
    message: str

class ModuleAdder:
    """Adds external modules to the ADHD workspace."""

    def __init__(self, project_root: Path | None = None):
        ...

    def add_from_repo(
        self,
        repo_url: str,
        subfolder: str | None = None,   # None = Mode 1, str = Mode 2
        *,
        keep_git: bool = False,
        add_to_root: bool | None = None, # None = ask, True/False = skip prompt
        skip_prompt: bool = False,        # skip all prompts (use defaults)
    ) -> AddModuleResult:
        """Clone a repo (or subfolder of a repo) and install as workspace module."""
        ...

    def add_from_pypi(self, package_name: str) -> AddModuleResult:
        """Future: install from PyPI. Currently raises NotImplementedError."""
        raise NotImplementedError("PyPI mode is not yet available.")
```

### CLI Interface Changes

Current:
```
adhd add <repo_url> [--skip-prompt/-y]
```

New:
```
adhd add <source> [--path <subfolder>] [--keep-git] [--add-to-root] [--skip-prompt/-y] [--pypi]
```

| Flag | Description |
|---|---|
| `<source>` | Git repository URL (or package name with `--pypi`) |
| `--path <subfolder>` | Extract subfolder from monorepo (Mode 2) |
| `--keep-git` | Preserve `.git/` directory instead of stripping it |
| `--add-to-root` | Add to root pyproject.toml without prompting |
| `--skip-prompt` / `-y` | Skip all interactive prompts, use defaults |
| `--pypi` | Treat `<source>` as a PyPI package name (not yet available) |

---

## Resulting ADHDFramework Shape

After all phases, `adhd_framework.py` should look like:

```python
class ADHDFramework:
    def __init__(self):
        self.logger = Logger(__class__.__name__)
        # no more QuestionaryCore or GithubApi here

    def run(self, args): ...  # dispatch map unchanged

    # --- Every handler below is <=10 lines ---

    def create_project_proc(self, args):
        run_project_creation_wizard(logger=self.logger)  # wizard owns prompt creation

    def create_module_proc(self, args):
        run_module_creation_wizard(logger=self.logger)

    def sync_project(self, args):
        ModulesController().sync(frozen=getattr(args, 'frozen', False))

    def init_project(self, args):
        self.sync_project(args)  # true alias

    def refresh_project(self, args):
        ModulesController().refresh(
            module_name=getattr(args, 'module', None),
            skip_sync=getattr(args, 'no_sync', False),
        )

    def list_modules(self, args):
        controller = ModulesController()
        filt = ModuleFilter.from_args(...)
        print(controller.list_all_modules().format(filt))

    def show_module_info(self, args):
        module = ModulesController().require_module(args.module)
        print(module.format_detail())

    def migrate_modules(self, args):
        results = ModulesController().migrate(module_name=..., dry_run=..., keep=...)
        print(format_migration_results(results))

    def doctor_check(self, args):
        report = ModulesController().doctor_check()
        print(report.format())
        if report.error_count > 0: sys.exit(1)

    def deps_check(self, args):
        # one-liner delegate to controller ...

    def update_workspace(self, args):
        # one-liner delegate to controller ...

    def add_module(self, args):
        from module_adder_core import ModuleAdder
        adder = ModuleAdder()
        if getattr(args, 'pypi', False):
            result = adder.add_from_pypi(args.source)
        else:
            result = adder.add_from_repo(
                args.source,
                subfolder=getattr(args, 'path', None),
                keep_git=getattr(args, 'keep_git', False),
                add_to_root=getattr(args, 'add_to_root', None),
                skip_prompt=getattr(args, 'skip_prompt', False),
            )
        if not result.success:
            self.logger.error(f"Failed: {result.message}")
            sys.exit(1)
        self.logger.info(result.message)
```

---

## Migration Safety

| Risk | Mitigation |
|---|---|
| Breaking existing `adhd` CLI behavior | No CLI interface changes for existing flags — same commands, same output. New flags are additive only. |
| Output format changes break scripts | Keep emoji format identical; formatter functions reproduce current output exactly |
| New module `module_adder_core` needs wiring | Add to `pyproject.toml` workspace members, `uv sync` |
| `_add_filter_value` has a bug (`normalized` undefined on L472) | Fix during extraction — this is a latent bug regardless |
| `QuestionaryCore` instantiated in `__init__` but only used by 2 wizard commands | Move instantiation into the wizards/adder that need it |
| `GithubApi.require_gh()` called unconditionally at startup | Move to commands that actually need GitHub (create-project). `module_adder_core` uses raw `git` CLI, not `gh`. |
| `.gitignore` in modules cascades to project git | This is **beneficial** — module build artifacts get ignored automatically. Tested in CI pipeline (see test plan). |
| `--keep-git` creates nested repo | Document this as advanced usage. Git handles nested repos gracefully (shows as untracked directory). |

---

## Sequence

```
Phase 1 (Presentation)  ->  Phase 2a-2e (Logic)  ->  Phase 4 (QCore split)  ->  Phase 3 (module_adder_core)
         |                           |                        |                           |
    zero behavior change      API additions to         file split only,          new module with
    just move print logic     existing modules         no behavior change        3 acquisition modes
```

Each phase is independently shippable. Phase 1 alone cuts `adhd_framework.py` by ~200 LOC with zero behavior change.

---

## Open Questions (Resolved)

1. ~~`module_adder_core` vs extending `modules_controller_core`?~~ **Resolved: new module.** Foundation layer must stay network-free.
2. **Should `setup_parser()` stay in `adhd_framework.py` or move to `cli_manager`?** — Parser definition is tightly coupled to the command set. If CLIManager adopts the `adhd` commands (not just admin_cli), the parser could be auto-built. This is a bigger refactor and out of scope here.
3. ~~`GithubApi.require_gh()` at startup~~ **Resolved:** Make it lazy, only called by commands that need `gh`.
