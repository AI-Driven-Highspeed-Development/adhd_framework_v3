# Modules Controller Core

Central registry that discovers, validates, and manages all ADHD Framework modules.

## Overview
- Discovers modules in `modules/{foundation,runtime,dev}/` layer structure
- Reads module metadata from `pyproject.toml` with `[tool.adhd]` configuration
- Provides cached `ModulesReport` objects for fast reuse by CLIs and other automation
- Includes dependency walking, health checks, filtering, and refresh ordering

## Features
- **Single scan, cached results** – `list_all_modules()` returns the previous scan; call `scan_all_modules()` to rescan
- **Rich module info** – `ModuleInfo` stores name, version, layer, path, MCP flag, repo URL, requirements, and issues
- **Module filtering** – `ModuleFilter` selects modules by layer, MCP flag, or git state with include/exclude/require modes
- **Dependency walker** – `DependencyWalker` builds transitive closure sets and detects cross-layer violations
- **Health checks** – `DoctorReport` validates module structure, pyproject.toml, and workspace membership
- **Refresh ordering** – `sort_modules_for_refresh` topologically sorts modules so dependencies refresh first
- **Issue catalog** – `ModuleIssueCode` enumerates missing metadata (version, layer, pyproject.toml)
- **Module lookup** – `get_module_by_name` with fuzzy suggestions via `require_module`

## Quickstart

```python
from modules_controller_core import ModulesController, DependencyWalker, ModuleFilter, FilterMode

controller = ModulesController()
report = controller.list_all_modules()

print(f"Total modules: {len(report.modules)}")
for module in report.issued_modules:
    codes = ", ".join(i.code.value for i in module.issues)
    print(f"{module.name} ({module.layer.value}) -> {codes}")

# Find a specific module
mod = controller.get_module_by_name("logger_util")

# Walk dependencies
walker = DependencyWalker(controller)
closure = walker.walk_dependencies("adhd_mcp")
print(closure.format())

# Filter to foundation modules only
f = ModuleFilter(mode=FilterMode.INCLUDE)
f.add_layer("foundation")
filtered = f.filter_modules(report.modules)
```

## API

```python
@dataclass
class ModuleInfo:
    name: str
    version: str
    layer: ModuleLayer
    path: Path
    is_mcp: bool = False
    repo_url: str | None = None
    requirements: list[str] = field(default_factory=list)
    issues: list[ModuleIssue] = field(default_factory=list)
    shows_in_workspace: bool | None = None
    def has_refresh_script(self) -> bool: ...
    def has_refresh_full_script(self) -> bool: ...
    def has_initializer(self) -> bool: ...
    def has_instructions(self) -> bool: ...

class ModulesController:
    def __init__(self, root_path: Path | None = None): ...
    def list_all_modules(self) -> ModulesReport: ...
    def scan_all_modules(self) -> ModulesReport: ...
    def get_module_by_name(self, module_name: str) -> ModuleInfo | None: ...
    def require_module(self, module_name: str) -> ModuleInfo: ...  # raises ADHDError
    def run_module_refresh_script(self, module: ModuleInfo, ...) -> None: ...
    def run_module_refresh_full_script(self, module: ModuleInfo, ...) -> None: ...
    def generate_workspace_file(self, mode, overrides, module_filter) -> Path: ...
    def refresh(self, module_name=None, *, skip_sync=False, full=False) -> None: ...
    def sync(self, *, frozen: bool = False) -> None: ...
    def doctor_check(self) -> DoctorReport: ...

class DependencyWalker:
    def __init__(self, controller: ModulesController): ...
    def walk_dependencies(self, module_name: str, max_depth: int = 50) -> DependencyClosure: ...
    def get_reverse_deps(self, module_name: str) -> set[str]: ...

@dataclass
class DependencyClosure:
    root_module: str
    tree: DependencyNode
    all_deps: set[str]
    adhd_deps: set[str]
    external_deps: set[str]
    violations: list[DependencyViolation]

class ModuleFilter:
    mode: FilterMode  # INCLUDE | REQUIRE | EXCLUDE
    def add_layer(self, layer: str) -> ModuleFilter: ...
    def add_mcp(self) -> ModuleFilter: ...
    def add_state(self, state: str) -> ModuleFilter: ...
    def filter_modules(self, modules: list[ModuleInfo]) -> list[ModuleInfo]: ...
    @classmethod
    def from_args(cls, mode: FilterMode, values: list[str]) -> ModuleFilter: ...

@dataclass
class DoctorReport:
    issues: list[DoctorIssue]
    modules_checked: int
    def is_healthy(self) -> bool: ...

class ModuleLayer(str, Enum):      # FOUNDATION | RUNTIME | DEV
class FilterMode(str, Enum):       # INCLUDE | REQUIRE | EXCLUDE
class FilterDimension(str, Enum):  # LAYER | FOLDER | MCP | STATE
class GitState(str, Enum):         # DIRTY | UNPUSHED | CLEAN
class ViolationType(str, Enum):    # CROSS_LAYER | MISSING_DEP
class ModuleIssueCode(str, Enum):  # see module_issues.py
class DoctorIssueSeverity(str, Enum):  # ERROR | WARNING | INFO

def sort_modules_for_refresh(modules: list[ModuleInfo]) -> list[ModuleInfo]: ...
def format_dependency_tree(node: DependencyNode) -> str: ...
def format_all_violations(violations: list[DependencyViolation]) -> str: ...
```

## Notes
- `ModulesController` is a singleton per root path; repeated instantiations reuse the cached instance.
- `ModuleInfo.layer` comes from `[tool.adhd].layer` in pyproject.toml.
- `DependencyWalker` resolves kebab-case package names to snake_case module names automatically.
- Layer hierarchy is `foundation < runtime < dev`; a module can only depend on its own layer or lower.

## Requirements & prerequisites
- `logger-util`
- `exceptions-core`

## Troubleshooting
- **Module missing from report** – ensure its directory is directly under `modules/{foundation,runtime,dev}/` and not prefixed with `_` or `.`.
- **Missing layer warning** – ensure `[tool.adhd].layer` is set to `foundation`, `runtime`, or `dev` in pyproject.toml.
- **Circular dependency error during refresh** – check `pyproject.toml` dependencies for cycles; `sort_modules_for_refresh` will raise `ADHDError`.
- **Module not found with suggestions** – `require_module` uses fuzzy matching; check the spelling against `adhd list` output.

## Module structure

```
modules_controller_core/
├─ __init__.py              # exports (30+ symbols)
├─ modules_controller.py    # ModulesController, ModuleInfo, ModulesReport
├─ dependency_walker.py     # DependencyWalker, DependencyClosure, violations
├─ module_doctor.py         # DoctorReport, DoctorIssue, DoctorIssueSeverity
├─ module_filter.py         # ModuleFilter, FilterMode, FilterDimension, GitState
├─ module_issues.py         # ModuleIssue, ModuleIssueCode
├─ module_types.py          # ModuleLayer, layer constants, path utilities
├─ refresh_order.py         # sort_modules_for_refresh (topological sort)
├─ pyproject.toml           # module metadata
├─ README.md                # this file
└─ tests/                   # unit tests
```

## See also
- Logger Util – logging used throughout this module
- Exceptions Core – `ADHDError` base exception
- Module Creator Core – scaffolds new modules with compliant metadata
- Workspace Core – generates VS Code workspace files from module data