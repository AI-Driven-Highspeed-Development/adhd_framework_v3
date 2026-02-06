"""Tests for new ModulesController APIs: require_module, sync, refresh, format methods.

MOCKS USED IN THIS FILE:
- subprocess.run: Mocked in sync/refresh tests to avoid running real uv/python commands.
  RISK: If uv behavior changes (args, exit codes), these tests won't catch it.
- shutil.which: Mocked to provide/deny uv path. RISK: None.
"""

import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from exceptions_core import ADHDError
from modules_controller_core import ModulesController, ModuleInfo
from modules_controller_core.module_types import ModuleLayer


@pytest.fixture
def project_with_modules(tmp_path: Path) -> Path:
    """Create a project with multiple modules across layers."""
    root = tmp_path / "project"
    for layer in ("foundation", "runtime", "dev"):
        for name in (f"{layer}_mod_a", f"{layer}_mod_b"):
            mod_dir = root / "modules" / layer / name
            mod_dir.mkdir(parents=True)
            (mod_dir / "pyproject.toml").write_text(f"""[project]
name = "{name.replace('_', '-')}"
version = "1.0.0"
dependencies = []

[tool.adhd]
layer = "{layer}"
""")
            (mod_dir / "__init__.py").write_text("")
    return root


class TestRequireModule:
    """Test ModulesController.require_module()."""

    def test_require_module_found(self, project_with_modules):
        """Should return ModuleInfo when module exists.

        MOCKS: None
        """
        controller = ModulesController(root_path=project_with_modules)
        module = controller.require_module("foundation_mod_a")
        assert module is not None
        assert module.name == "foundation_mod_a"

    def test_require_module_not_found_raises(self, project_with_modules):
        """Should raise ADHDError with suggestions when not found.

        MOCKS: None
        """
        controller = ModulesController(root_path=project_with_modules)
        with pytest.raises(ADHDError) as exc_info:
            controller.require_module("nonexistent_module")
        # Should mention that module wasn't found
        assert "not found" in str(exc_info.value).lower()

    def test_require_module_fuzzy_suggestion(self, project_with_modules):
        """Should suggest close matches.

        MOCKS: None
        """
        controller = ModulesController(root_path=project_with_modules)
        with pytest.raises(ADHDError) as exc_info:
            controller.require_module("foundation_mod")
        # Should suggest foundation_mod_a or foundation_mod_b
        msg = str(exc_info.value)
        assert "foundation_mod_a" in msg or "foundation_mod_b" in msg

    def test_require_module_case_insensitive(self, project_with_modules):
        """Should handle case-insensitive names.

        MOCKS: None
        """
        controller = ModulesController(root_path=project_with_modules)
        module = controller.require_module("Foundation_Mod_A")
        assert module.name == "foundation_mod_a"


class TestSync:
    """Test ModulesController.sync()."""

    def test_sync_calls_uv(self):
        """sync() should invoke uv sync.

        MOCKS: subprocess.run, shutil.which
        """
        with patch("subprocess.run") as mock_run:
            with patch("shutil.which", return_value="/usr/bin/uv"):
                mock_run.return_value = MagicMock(returncode=0)
                controller = ModulesController.__new__(ModulesController)
                controller._initialized = False
                controller.__init__()
                controller.sync()

                args = mock_run.call_args[0][0]
                assert args[0] == "/usr/bin/uv"
                assert args[1] == "sync"

    def test_sync_frozen(self):
        """sync(frozen=True) should pass --frozen flag.

        MOCKS: subprocess.run, shutil.which
        """
        with patch("subprocess.run") as mock_run:
            with patch("shutil.which", return_value="/usr/bin/uv"):
                mock_run.return_value = MagicMock(returncode=0)
                controller = ModulesController.__new__(ModulesController)
                controller._initialized = False
                controller.__init__()
                controller.sync(frozen=True)

                args = mock_run.call_args[0][0]
                assert "--frozen" in args

    def test_sync_uv_not_found_raises(self):
        """sync() should raise ADHDError when uv not found.

        MOCKS: shutil.which
        """
        with patch("shutil.which", return_value=None):
            controller = ModulesController.__new__(ModulesController)
            controller._initialized = False
            controller.__init__()
            with pytest.raises(ADHDError, match="uv"):
                controller.sync()

    def test_sync_failure_raises(self):
        """sync() should raise ADHDError on subprocess failure.

        MOCKS: subprocess.run, shutil.which
        """
        with patch("subprocess.run") as mock_run:
            with patch("shutil.which", return_value="/usr/bin/uv"):
                mock_run.side_effect = subprocess.CalledProcessError(1, "uv sync")
                controller = ModulesController.__new__(ModulesController)
                controller._initialized = False
                controller.__init__()
                with pytest.raises(ADHDError, match="sync failed"):
                    controller.sync()


class TestFormatMethods:
    """Test format_detail() and ModulesReport.format()."""

    def test_format_detail(self):
        """ModuleInfo.format_detail() should return formatted string.

        MOCKS: None
        """
        mi = ModuleInfo(
            name="test_module",
            version="1.2.3",
            layer=ModuleLayer.RUNTIME,
            path=Path("/test/modules/runtime/test_module"),
            is_mcp=True,
            repo_url="https://github.com/org/test",
            requirements=["dep1", "dep2"],
        )
        output = mi.format_detail()
        assert "test_module" in output
        assert "1.2.3" in output
        assert "runtime" in output
        assert "[MCP]" in output
        assert "dep1, dep2" in output

    def test_format_detail_no_mcp(self):
        """Non-MCP module should not show [MCP] tag.

        MOCKS: None
        """
        mi = ModuleInfo(
            name="plain_module",
            version="1.0.0",
            layer=ModuleLayer.FOUNDATION,
            path=Path("/test"),
        )
        output = mi.format_detail()
        assert "[MCP]" not in output

    def test_modules_report_format(self, project_with_modules):
        """ModulesReport.format() should list all modules.

        MOCKS: None
        """
        controller = ModulesController(root_path=project_with_modules)
        report = controller.list_all_modules()
        output = report.format()
        assert "Found" in output
        assert "foundation_mod_a" in output
        assert "runtime_mod_b" in output

    def test_modules_report_format_with_filter(self, project_with_modules):
        """ModulesReport.format() with filter should only show matching.

        MOCKS: None
        """
        from modules_controller_core.module_filter import ModuleFilter, FilterMode
        controller = ModulesController(root_path=project_with_modules)
        report = controller.list_all_modules()

        filt = ModuleFilter(mode=FilterMode.INCLUDE)
        filt.add_layer("foundation", inherit=False)

        output = report.format(filt)
        assert "foundation_mod_a" in output
        assert "dev_mod_a" not in output
