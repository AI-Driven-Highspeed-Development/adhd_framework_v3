"""
Refresh script for flow_core module.

This script is called during framework refresh to perform any
necessary setup or synchronization for the Flow Core module.
"""

from __future__ import annotations

from logger_util import Logger
from .flow_cli import register_cli


def main() -> None:
    """
    Refresh script for flow_core.
    
    Registers CLI commands with the centralized CLIManager.
    """
    logger = Logger(name="FlowCoreRefresh")
    
    try:
        register_cli()
        logger.info("Flow core refresh: CLI commands registered.")
    except Exception as e:
        logger.warning(f"Flow core refresh: Could not register CLI commands: {e}")


if __name__ == "__main__":
    main()
