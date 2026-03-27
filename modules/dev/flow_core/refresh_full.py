"""Full refresh script for flow_core.

Best-effort installer for the FLOW Language VS Code extension.
Runs during `adhd refresh --full` and never raises fatal errors.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from config_manager import ConfigManager
from logger_util import Logger

DEFAULT_EXTENSION_ID = "adhd-framework.flow-language"
PATH_CLI_CANDIDATES: tuple[str, ...] = ("code", "code-insiders", "codium")


@dataclass(frozen=True)
class ExtensionInstallConfig:
    """Resolved configuration for extension installation behavior."""

    enabled: bool = True
    extension_id: str = DEFAULT_EXTENSION_ID
    vsix_path: Path | None = None
    code_cli_path: str | None = None


def _coerce_bool(value: object, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    return default


def _resolve_path(value: object) -> Path | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    candidate = Path(text).expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    return candidate


def _load_install_config(logger: Logger) -> ExtensionInstallConfig:
    """Read optional override values from flow_core config."""
    try:
        cm = ConfigManager()
        flow_core_cfg = cm.config.flow_core
        extension_cfg = flow_core_cfg.dict_get("extension_auto_install", {})

        if not isinstance(extension_cfg, dict):
            logger.warning(
                "flow_core.extension_auto_install is not a dict; using defaults."
            )
            extension_cfg = {}

        enabled = _coerce_bool(extension_cfg.get("enabled"), default=True)
        extension_id = extension_cfg.get("extension_id")
        if not isinstance(extension_id, str) or not extension_id.strip():
            extension_id = DEFAULT_EXTENSION_ID
        else:
            extension_id = extension_id.strip()

        vsix_path = _resolve_path(extension_cfg.get("vsix_path"))
        code_cli_path = extension_cfg.get("code_cli_path")
        if isinstance(code_cli_path, str):
            code_cli_path = code_cli_path.strip() or None
        else:
            code_cli_path = None

        return ExtensionInstallConfig(
            enabled=enabled,
            extension_id=extension_id,
            vsix_path=vsix_path,
            code_cli_path=code_cli_path,
        )
    except Exception as exc:
        logger.warning(
            f"Could not read flow_core config overrides; using defaults. Reason: {exc}"
        )
        return ExtensionInstallConfig()


def _iter_cli_candidates(config: ExtensionInstallConfig) -> Iterable[str]:
    seen: set[str] = set()

    if config.code_cli_path:
        explicit = config.code_cli_path.strip()
        if explicit and explicit not in seen:
            seen.add(explicit)
            yield explicit

    for candidate in PATH_CLI_CANDIDATES:
        if candidate not in seen:
            seen.add(candidate)
            yield candidate

    vscode_server_bin_root = Path.home() / ".vscode-server" / "bin"
    if vscode_server_bin_root.exists():
        for path in sorted(vscode_server_bin_root.glob("*/bin/code")):
            resolved = str(path)
            if resolved not in seen:
                seen.add(resolved)
                yield resolved


def _resolve_cli_command(candidate: str) -> str | None:
    """Resolve candidate to an executable command path."""
    if not candidate:
        return None

    has_path_separator = os.sep in candidate or (os.altsep and os.altsep in candidate)
    if has_path_separator:
        path = Path(candidate).expanduser()
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
        return None

    return shutil.which(candidate)


def _choose_code_cli(config: ExtensionInstallConfig, logger: Logger) -> str | None:
    for candidate in _iter_cli_candidates(config):
        cli = _resolve_cli_command(candidate)
        if cli:
            logger.info(f"Using VS Code CLI: {cli}")
            return cli

    logger.warning(
        "No VS Code CLI found (`code`, `code-insiders`, `codium`, or vscode-server bin path). "
        "Skipping FLOW extension install."
    )
    return None


def _is_extension_installed(cli: str, extension_id: str, logger: Logger) -> bool:
    """Check whether extension is already installed for this VS Code profile."""
    try:
        result = subprocess.run(
            [cli, "--list-extensions"],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
        if result.returncode != 0:
            logger.warning(
                "Could not list installed extensions; will attempt install anyway. "
                f"CLI exit code: {result.returncode}"
            )
            return False

        installed = {line.strip().lower() for line in result.stdout.splitlines() if line.strip()}
        return extension_id.lower() in installed
    except Exception as exc:
        logger.warning(
            f"Could not determine installed extensions; will attempt install anyway. Reason: {exc}"
        )
        return False


def _run_install_command(cli: str, args: list[str], logger: Logger) -> bool:
    cmd = [cli, *args]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
    except Exception as exc:
        logger.warning(f"Failed to execute extension install command: {exc}")
        return False

    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        details = stderr or stdout or "no CLI output"
        logger.warning(f"Extension install command failed: {details}")
        return False

    logger.info("FLOW Language extension install command completed.")
    return True


def ensure_flow_extension_installed(logger: Logger) -> None:
    """Best-effort extension installer. Never raises fatal exceptions."""
    try:
        config = _load_install_config(logger)

        if not config.enabled:
            logger.info("FLOW extension auto-install is disabled by config.")
            return

        cli = _choose_code_cli(config, logger)
        if not cli:
            return

        if _is_extension_installed(cli, config.extension_id, logger):
            logger.info(f"Extension already installed: {config.extension_id}")
            return

        if config.vsix_path and config.vsix_path.exists():
            logger.info(f"Installing FLOW extension from VSIX: {config.vsix_path}")
            _run_install_command(
                cli,
                ["--install-extension", str(config.vsix_path), "--force"],
                logger,
            )
            return

        if config.vsix_path and not config.vsix_path.exists():
            logger.warning(
                f"Configured VSIX does not exist: {config.vsix_path}. Falling back to extension ID install."
            )

        logger.info(f"Installing FLOW extension by ID: {config.extension_id}")
        _run_install_command(cli, ["--install-extension", config.extension_id], logger)
    except Exception as exc:
        logger.warning(f"FLOW extension ensure-install failed (non-fatal): {exc}")


def register_refresh() -> None:
    """Entry point used by module refresh flow during full refresh."""
    logger = Logger(name="flow_coreRefreshFull")
    logger.info("Starting flow_core full refresh...")
    ensure_flow_extension_installed(logger)
    logger.info("flow_core full refresh complete.")


def main() -> None:
    """CLI entry point for direct execution."""
    register_refresh()


if __name__ == "__main__":
    main()
