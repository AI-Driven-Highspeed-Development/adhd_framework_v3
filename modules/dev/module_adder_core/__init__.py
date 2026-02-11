"""module_adder_core - Module lifecycle management for the ADHD Framework workspace.

Supports:
- Adding modules (git clone, monorepo subfolder, future PyPI)
- Removing modules (with reverse-dep checks and dry-run)
- Updating modules (atomic swap with rollback)
"""
# TODO: rename module_adder_core to module_lifecycle_core

from .module_adder import ModuleAdder, AddModuleResult
from .module_remover import ModuleRemover, RemoveResult
from .module_updater import ModuleUpdater, UpdateResult, BatchUpdateResult

__all__ = [
    "ModuleAdder",
    "AddModuleResult",
    "ModuleRemover",
    "RemoveResult",
    "ModuleUpdater",
    "UpdateResult",
    "BatchUpdateResult",
]
