"""Pyproject Patcher - Add packages to root pyproject.toml dependencies and uv.sources.

This module handles the string manipulation needed to add a new workspace member
to the root pyproject.toml without rewriting the entire file (preserving formatting).
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from exceptions_core import ADHDError
from logger_util import Logger

logger = Logger(name="pyproject_patcher")


def add_to_root_pyproject(package_name: str, project_root: Path) -> None:
    """Add a package to root pyproject.toml dependencies and [tool.uv.sources].

    Reads the existing pyproject.toml, adds the package to both:
    - project.dependencies list
    - [tool.uv.sources] with { workspace = true }

    Preserves formatting by using string manipulation.

    Args:
        package_name: The package name (kebab-case, e.g. 'my-module')
        project_root: Path to the project root directory

    Raises:
        ADHDError: If the file is missing, malformed, or cannot be patched.
    """
    root_pyproject = project_root / "pyproject.toml"
    if not root_pyproject.exists():
        raise ADHDError("Root pyproject.toml not found")

    original_content = root_pyproject.read_text(encoding="utf-8")

    # Parse to validate and check duplicates
    with root_pyproject.open("rb") as f:
        data = tomllib.load(f)

    # Check for duplicates
    dependencies = data.get("project", {}).get("dependencies", [])
    if package_name in dependencies:
        logger.warning(f"Package '{package_name}' already in dependencies")
        return

    sources = data.get("tool", {}).get("uv", {}).get("sources", {})
    if package_name in sources:
        logger.warning(f"Package '{package_name}' already in [tool.uv.sources]")
        return

    modified_content = original_content

    # Add to dependencies section
    modified_content = _add_to_dependencies(modified_content, package_name)

    # Add to [tool.uv.sources]
    modified_content = _add_to_uv_sources(modified_content, package_name)

    root_pyproject.write_text(modified_content, encoding="utf-8")
    logger.info(f"\u2705 Added '{package_name}' to root pyproject.toml")


def _add_to_dependencies(content: str, package_name: str) -> str:
    """Insert package into the dependencies = [...] list."""
    dep_pattern = "dependencies = ["
    dep_start = content.find(dep_pattern)
    if dep_start == -1:
        raise ADHDError("Could not find dependencies section in pyproject.toml")

    # Find the closing bracket
    bracket_depth = 0
    idx = dep_start + len(dep_pattern)
    dep_end = -1
    while idx < len(content):
        if content[idx] == "[":
            bracket_depth += 1
        elif content[idx] == "]":
            if bracket_depth == 0:
                dep_end = idx
                break
            bracket_depth -= 1
        idx += 1

    if dep_end == -1:
        raise ADHDError("Could not find end of dependencies list")

    # Determine indentation from existing entries
    lines_before = content[:dep_end].split("\n")
    indent = "    "  # Default 4 spaces
    for line in reversed(lines_before):
        stripped = line.strip()
        if stripped and stripped.startswith('"') and stripped != dep_pattern.strip():
            indent_count = len(line) - len(line.lstrip())
            indent = " " * indent_count if indent_count > 0 else "    "
            break

    new_dep = f'{indent}"{package_name}",\n'
    return content[:dep_end] + new_dep + content[dep_end:]


def _add_to_uv_sources(content: str, package_name: str) -> str:
    """Insert package into [tool.uv.sources] section."""
    sources_pattern = "[tool.uv.sources]"
    sources_start = content.find(sources_pattern)
    if sources_start == -1:
        raise ADHDError("Could not find [tool.uv.sources] section in pyproject.toml")

    # Find end of section (next [section] header or EOF)
    next_section_start = content.find("\n[", sources_start + len(sources_pattern))
    if next_section_start == -1:
        insertion_point = len(content)
    else:
        insertion_point = next_section_start

    new_source = f"{package_name} = {{ workspace = true }}\n"

    # Match indentation of existing entries
    lines_before = content[:insertion_point].split("\n")
    for line in reversed(lines_before):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and stripped != sources_pattern:
            indent_count = len(line) - len(line.lstrip())
            if indent_count > 0:
                new_source = " " * indent_count + new_source.lstrip()
            break

    return content[:insertion_point] + new_source + content[insertion_point:]
