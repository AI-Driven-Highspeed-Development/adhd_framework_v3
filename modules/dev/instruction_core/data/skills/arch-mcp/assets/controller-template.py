"""Controller implementation pattern for ADHD MCP modules.

Canonical template — adapt names and methods to your module.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from logger_util import Logger
from config_manager import ConfigManager

log = Logger(name="MyController", verbose=False)


class MyController:
    def __init__(self, workspace_root: str | Path | None = None) -> None:
        self._cm = ConfigManager(workspace_root=workspace_root)

    def my_operation(self, arg: str) -> dict[str, Any]:
        """Perform the operation."""
        log.info(f"Running operation with {arg}")
        return {"success": True, "result": "done"}


def get_my_controller() -> MyController:
    """Module-level singleton accessor."""
    global _controller
    if _controller is None:
        _controller = MyController()
    return _controller


_controller: MyController | None = None
