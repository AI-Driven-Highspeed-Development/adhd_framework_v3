"""Tests for pyproject_scaffolder - interactive pyproject.toml generation.

MOCKS USED IN THIS FILE:
- QuestionaryCore: Mocked in tests that need interactive prompts. Returns
  predetermined values. RISK: If prompt arguments or order change in the
  scaffolder, mock responses may not match real interactive flow.
"""

import tomllib
from pathlib import Path

import pytest


class TestScaffoldWithDefaults:
    """Test scaffolding with skip_prompt=True (all defaults)."""

    def test_scaffold_with_all_defaults(self, tmp_path):
        """skip_prompt=True should generate valid pyproject.toml with defaults.

        MOCKS: None (skip_prompt=True bypasses prompts)
        """
        from module_lifecycle_core.pyproject_scaffolder import scaffold_pyproject

        module_dir = tmp_path / "my_cool_module"
        module_dir.mkdir()

        result = scaffold_pyproject(module_dir, skip_prompt=True)

        assert result.exists()
        with result.open("rb") as f:
            data = tomllib.load(f)

        assert data["project"]["name"] == "my-cool-module"
        assert data["project"]["version"] == "0.0.1"
        assert data["tool"]["adhd"]["layer"] == "runtime"
        assert "mcp" not in data["tool"]["adhd"]

    def test_scaffold_output_is_valid_toml(self, tmp_path):
        """Generated file should be valid TOML.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_scaffolder import scaffold_pyproject

        module_dir = tmp_path / "test_module"
        module_dir.mkdir()

        result = scaffold_pyproject(module_dir, skip_prompt=True)

        with result.open("rb") as f:
            data = tomllib.load(f)

        assert "project" in data
        assert "tool" in data
        assert "adhd" in data["tool"]
        assert "build-system" in data


class TestScaffoldNameInference:
    """Test package name inference from folder names."""

    def test_kebab_case_folder(self, tmp_path):
        """my-cool-module -> my_cool_module (snake_case).

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_scaffolder import _infer_name_from_folder

        assert _infer_name_from_folder(tmp_path / "my-cool-module") == "my_cool_module"

    def test_camel_case_folder(self, tmp_path):
        """MyModule -> my_module (snake_case).

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_scaffolder import _infer_name_from_folder

        assert _infer_name_from_folder(tmp_path / "MyModule") == "my_module"

    def test_already_snake_case(self, tmp_path):
        """already_snake -> already_snake.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_scaffolder import _infer_name_from_folder

        assert _infer_name_from_folder(tmp_path / "already_snake") == "already_snake"

    def test_mixed_separators(self, tmp_path):
        """My-Cool_Module -> my_cool_module.

        MOCKS: None
        """
        from module_lifecycle_core.pyproject_scaffolder import _infer_name_from_folder

        assert _infer_name_from_folder(tmp_path / "My-Cool_Module") == "my_cool_module"
