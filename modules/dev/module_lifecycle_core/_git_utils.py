"""Shared git utilities for module lifecycle operations.

Extracted from ``module_adder.py`` and ``module_updater.py`` to eliminate
duplicated clone logic (Non-Vibe Code — Pillar 1: Unify Before Duplicating).
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from exceptions_core import ADHDError


def clone_repo(
    repo_url: str,
    dest: Path,
    *,
    branch: Optional[str] = None,
    timeout: int = 120,
) -> Path:
    """Shallow-clone a git repository to *dest*.

    Args:
        repo_url: Git repository URL.
        dest: Destination directory for the clone.
        branch: Optional branch to clone. Defaults to the repo's HEAD.
        timeout: Timeout in seconds for the git command.

    Returns:
        The *dest* path (for chaining convenience).

    Raises:
        ADHDError: If the clone command fails.
    """
    cmd = ["git", "clone", "--depth", "1"]
    if branch:
        cmd.extend(["--branch", branch])
    cmd.extend([repo_url, str(dest)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        error_msg = result.stderr[:500] if result.stderr else "Unknown error"
        error_msg = error_msg.replace(repo_url, "<URL>")
        raise ADHDError(f"git clone failed: {error_msg}")
    return dest
