"""Pyproject Scaffolder - Interactive pyproject.toml generation for modules without one.

When a module is added from git (Mode 1 or 2) and lacks a pyproject.toml,
this scaffolder prompts the user (or uses defaults) to create a minimal one.
"""

from __future__ import annotations

import re
from pathlib import Path

from logger_util import Logger

logger = Logger(name="pyproject_scaffolder")


def _infer_name_from_folder(folder_path: Path) -> str:
    """Infer a snake_case package name from a folder name.

    Examples:
        my-cool-module -> my_cool_module
        MyModule -> my_module
    """
    name = folder_path.name
    # Insert underscores before uppercase letters (CamelCase)
    name = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name)
    # Replace non-alphanumeric with underscore
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    # Collapse multiple underscores
    name = re.sub(r"_+", "_", name).strip("_")
    return name.lower() or "unnamed_module"


def scaffold_pyproject(
    module_dir: Path,
    *,
    skip_prompt: bool = False,
) -> Path:
    """Create a minimal pyproject.toml for a module directory.

    Args:
        module_dir: Path to the module directory.
        skip_prompt: If True, use all defaults without asking.

    Returns:
        Path to the created pyproject.toml.
    """
    pyproject_path = module_dir / "pyproject.toml"

    if skip_prompt:
        name = _infer_name_from_folder(module_dir)
        version = "0.0.1"
        description = ""
        layer = "runtime"
        is_mcp = False
        python_requires = ">=3.11"
    else:
        from creator_common_core import QuestionaryCore
        prompter = QuestionaryCore()

        default_name = _infer_name_from_folder(module_dir)

        logger.info(
            f"\n\U0001f4e6 Module at {module_dir.name} has no pyproject.toml. Creating one interactively.\n"
        )

        name = prompter.text_input("Package name?", default=default_name)
        version = prompter.text_input("Version?", default="0.0.1")
        description = prompter.text_input("One-line description?", default="")
        layer = prompter.multiple_choice(
            "Layer?",
            choices=["foundation", "runtime", "dev"],
            default="runtime",
        )
        is_mcp = prompter.confirm("Is this an MCP server module?", default=False)
        python_requires = prompter.text_input("Python version requirement?", default=">=3.11")

    # Normalize name to kebab-case for [project] name
    package_name = name.lower().replace("_", "-")

    mcp_line = "mcp = true\n" if is_mcp else ""
    desc_line = f'description = "{description}"\n' if description else ""

    content = f"""[project]
name = "{package_name}"
version = "{version}"
{desc_line}requires-python = "{python_requires}"
dependencies = []

[tool.adhd]
layer = "{layer}"
{mcp_line}
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

    pyproject_path.write_text(content, encoding="utf-8")
    logger.info(f"\u2705 Created pyproject.toml for {name}")

    return pyproject_path
