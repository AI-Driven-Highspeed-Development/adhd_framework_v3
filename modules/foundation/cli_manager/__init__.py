"""cli_manager - Centralized CLI command registration and admin CLI generation."""

from cli_manager.cli_manager import (
    CLIManager,
    Command,
    CommandArg,
    CommandGroup,
    ModuleRegistration,
)

__all__ = [
    "CLIManager",
    "Command",
    "CommandArg",
    "CommandGroup",
    "ModuleRegistration",
]
