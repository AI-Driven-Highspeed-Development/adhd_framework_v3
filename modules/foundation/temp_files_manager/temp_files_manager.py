from __future__ import annotations

import os
import shutil
import uuid
from typing import Optional

from config_manager import ConfigManager
from logger_util import Logger


class TempFilesManager:
    """Manage temporary directories with tracking and safe cleanup.

    Preference order for base temp directory (when base_dir is not provided):
    1) Config for the specified module_key (e.g. github_api_core.path.unix_temp/windows_temp)
    2) OS temp dir via tempfile.gettempdir() joined with module_key
    """

    def __init__(
        self,
        base_dir: Optional[str] = None
    ) -> None:
        self.logger = Logger(name=__class__.__name__)
        self.cm = ConfigManager()
        self.config = self.cm.config.temp_files_manager
        
        self._pool: list[str] = []
        self.base_dir = base_dir or self._resolve_os_base_dir()
        os.makedirs(self.base_dir, exist_ok=True)

    # ---------------- Public API ----------------
    def make_dir(self, prefix: str = "tmp") -> str:
        """Create a unique temporary directory under base_dir and track it."""
        name = f"{prefix}_{uuid.uuid4().hex[:16]}"
        path = os.path.join(self.base_dir, name)
        os.makedirs(path, exist_ok=True)
        self._pool.append(path)
        self.logger.debug(f"Created temp dir: {path}")
        return path

    def cleanup(self, path: str) -> None:
        """Remove a tracked temporary directory recursively."""
        try:
            if path in self._pool:
                self._pool.remove(path)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
                self.logger.debug(f"Cleaned temp dir: {path}")
        except Exception as e:
            self.logger.error(f"Error cleaning temp dir {path}: {e}")

    def cleanup_all(self) -> None:
        """Remove all tracked temporary directories."""
        for p in list(self._pool):
            self.cleanup(p)
        self._pool.clear()

    # ---------------- Internal helpers ----------------
    def _resolve_os_base_dir(self) -> Optional[str]:
        if os.name == "nt":
            return self.config.path.windows_temp
        if os.name != "nt":
            return self.config.path.unix_temp
        return None
