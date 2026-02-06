"""module_adder_core - Add external modules to the ADHD Framework workspace.

Supports three acquisition modes:
1. Standalone repository (git clone)
2. Monorepo subfolder (git clone + extract subfolder)
3. PyPI package (future, not yet available)
"""

from .module_adder import ModuleAdder, AddModuleResult

__all__ = [
    "ModuleAdder",
    "AddModuleResult",
]
