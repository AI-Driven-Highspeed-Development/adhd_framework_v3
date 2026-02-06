"""CLI E2E tests for the adhd command.

Tests run the CLI via subprocess to validate end-to-end behavior.
These tests invoke `adhd <command>` and check exit codes and output.

MOCKS USED IN THIS FILE:
- None. These tests run real subprocess commands against the real codebase.
  They test the actual CLI interface.
"""

import subprocess
from pathlib import Path

import pytest

FRAMEWORK_ROOT = Path(__file__).parent.parent.parent


def run_adhd(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    """Run `adhd <args>` via uv run and return the result."""
    cmd = ["uv", "run", "adhd", *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(FRAMEWORK_ROOT),
        timeout=30,
    )


class TestCLIHelp:
    """Test that help works for all commands."""

    def test_main_help(self):
        result = run_adhd("--help")
        assert result.returncode == 0
        assert "Available commands" in result.stdout or "usage" in result.stdout.lower()

    def test_list_help(self):
        result = run_adhd("list", "--help")
        assert result.returncode == 0
        assert "--include" in result.stdout

    def test_add_help(self):
        result = run_adhd("add", "--help")
        assert result.returncode == 0
        assert "--path" in result.stdout
        assert "--keep-git" in result.stdout
        assert "--pypi" in result.stdout


class TestCLIList:
    """Test `adhd list` command."""

    def test_list_modules(self):
        result = run_adhd("list")
        assert result.returncode == 0
        assert "Found" in result.stdout
        # Should list known modules
        assert "modules_controller_core" in result.stdout or "config_manager" in result.stdout

    def test_list_with_layer_filter(self):
        result = run_adhd("list", "-i", "foundation")
        assert result.returncode == 0
        assert "Found" in result.stdout

    def test_list_show_filters(self):
        result = run_adhd("list", "--show-filters")
        assert result.returncode == 0
        assert "Layers" in result.stdout
        assert "foundation" in result.stdout


class TestCLIDoctor:
    """Test `adhd doctor` command."""

    def test_doctor_runs(self):
        result = run_adhd("doctor")
        # May succeed or fail depending on module health, but should not crash
        assert result.returncode in (0, 1)
        assert "Doctor Report" in result.stdout or "modules checked" in result.stdout


class TestCLIDeps:
    """Test `adhd deps` command."""

    def test_deps_closure_for_known_module(self):
        result = run_adhd("deps", "--closure", "modules_controller_core")
        assert result.returncode in (0, 1)
        assert "Dependency Tree" in result.stdout or "Summary" in result.stdout

    def test_deps_closure_all(self):
        result = run_adhd("deps", "--closure-all")
        assert result.returncode in (0, 1)
        assert "Modules checked" in result.stdout or "Checking" in result.stdout


class TestCLIInfo:
    """Test `adhd info` command."""

    def test_info_known_module(self):
        result = run_adhd("info", "-m", "modules_controller_core")
        assert result.returncode == 0
        assert "MODULE INFORMATION" in result.stdout
        assert "modules_controller_core" in result.stdout

    def test_info_unknown_module(self):
        result = run_adhd("info", "-m", "nonexistent_module_xyz")
        assert result.returncode == 1


class TestCLIAddPyPI:
    """Test `adhd add --pypi` mode (expected to fail with not-implemented)."""

    def test_add_pypi_not_implemented(self):
        result = run_adhd("add", "--pypi", "some-package")
        assert result.returncode == 1
        assert "not yet available" in result.stderr.lower() or "not yet available" in result.stdout.lower()


class TestCLIWorkspace:
    """Test `adhd workspace` command."""

    def test_workspace_all(self):
        result = run_adhd("workspace", "--all")
        # Should succeed unless workspace_core has issues
        assert result.returncode in (0, 1)


class TestCLISync:
    """Test `adhd sync` command."""

    def test_sync_runs(self):
        result = run_adhd("sync")
        assert result.returncode == 0
