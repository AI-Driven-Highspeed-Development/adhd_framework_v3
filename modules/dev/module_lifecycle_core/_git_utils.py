"""Shared git utilities for module lifecycle operations.

Extracted from ``module_adder.py`` and ``module_updater.py`` to eliminate
duplicated clone logic (Non-Vibe Code — Pillar 1: Unify Before Duplicating).
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from exceptions_core import ADHDError


@dataclass
class ParsedGitSource:
    """Components extracted from a GitHub URL.

    Attributes:
        clone_url: Git-cloneable URL (e.g., ``https://github.com/org/repo.git``).
        branch: Optional branch parsed from ``/tree/<branch>/...`` path segment.
        subfolder: Optional subfolder path parsed from the URL
            (e.g., ``modules/dev/adhd_mcp``).
    """

    clone_url: str
    branch: Optional[str] = None
    subfolder: Optional[str] = None


# Match: https://github.com/{owner}/{repo}[.git][/tree/{branch}[/{subfolder}]]
_GITHUB_BROWSER_RE = re.compile(
    r"^https?://github\.com/"
    r"(?P<owner>[^/]+)/"
    r"(?P<repo>[^/.]+)"
    r"(?:\.git)?"
    r"(?:/tree/(?P<branch>[^/]+)(?:/(?P<subfolder>.+))?)?"
    r"/?$"
)


def parse_github_url(url: str) -> ParsedGitSource:
    """Parse a GitHub URL into clone-ready components.

    Supported formats:
        - Browser URL with subfolder:
          ``https://github.com/org/repo/tree/branch/path/to/subfolder``
        - Clone URL: ``https://github.com/org/repo.git``
        - Bare URL: ``https://github.com/org/repo``
        - SSH URL: ``git@github.com:org/repo.git`` — passed through as-is
        - Non-GitHub URL — passed through as-is (no parsing attempted)

    Note:
        Cannot disambiguate branch names containing ``/`` from subfolder paths.
        For example, ``/tree/feature/fix/path`` is parsed as
        ``branch="feature", subfolder="fix/path"``.  This matches typical ADHD
        module URLs which use simple branch names (``main``, ``dev``, etc.).

    Args:
        url: Any git-related URL.

    Returns:
        ParsedGitSource with clone_url, optional branch, optional subfolder.
    """
    # SSH URLs — pass through unchanged
    if url.startswith("git@"):
        return ParsedGitSource(clone_url=url)

    m = _GITHUB_BROWSER_RE.match(url)
    if not m:
        # Non-GitHub HTTPS URL — pass through unchanged
        return ParsedGitSource(clone_url=url)

    owner = m.group("owner")
    repo = m.group("repo")
    branch = m.group("branch")
    subfolder = m.group("subfolder")

    if subfolder:
        subfolder = subfolder.rstrip("/")

    clone_url = f"https://github.com/{owner}/{repo}.git"

    return ParsedGitSource(
        clone_url=clone_url,
        branch=branch,
        subfolder=subfolder,
    )


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
