"""
Frontmatter Parser — YAML frontmatter extraction from Markdown files.

Parses the YAML frontmatter block (delimited by ``---``) from plan
and module spec Markdown files in the DREAM planning system.
"""
# JUSTIFY: separate from instruction_core's inline parsing — different module domain, avoids cross-module dependency
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from logger_util import Logger

_logger = Logger(name="dream_mcp.frontmatter_parser")

# Matches YAML frontmatter: opening ---, content, closing --- on own lines.
# Handles optional leading whitespace, CRLF/LF, and EOF after closing ---.
_FRONTMATTER_RE = re.compile(
    r"\A\s*---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)",
    re.DOTALL,
)


def parse_frontmatter(text: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter from a markdown text string.

    Frontmatter is expected as the first block in the file, delimited
    by triple dashes (``---``) on their own lines.

    Args:
        text: Full markdown text content.

    Returns:
        Parsed YAML dict, or None if no valid frontmatter found.
    """
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None

    yaml_block = match.group(1).strip()
    if not yaml_block:
        return None

    try:
        parsed = yaml.safe_load(yaml_block)
        if isinstance(parsed, dict):
            return parsed
        return None
    except yaml.YAMLError as exc:
        _logger.debug(f"YAML parse error in frontmatter: {exc}")
        return None


def parse_frontmatter_file(path: Path) -> dict[str, Any] | None:
    """Parse YAML frontmatter from a markdown file.

    Args:
        path: Path to the markdown file.

    Returns:
        Parsed YAML dict, or None if file doesn't exist or has no frontmatter.
    """
    if not path.is_file():
        return None

    try:
        text = path.read_text(encoding="utf-8")
        return parse_frontmatter(text)
    except OSError as exc:
        _logger.debug(f"Could not read {path}: {exc}")
        return None
