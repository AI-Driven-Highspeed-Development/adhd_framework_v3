"""
Refresh script for config_manager.

Scans all modules for .config_template files, consolidates them into .config,
then triggers ConfigManager which auto-generates config_keys.py.

Run via: python adhd_framework.py refresh --module config-manager
"""

from __future__ import annotations

from logger_util import Logger

from .config_template import ConfigTemplate
from .config_manager import ConfigManager


def main() -> None:
    """Refresh configuration by processing templates and regenerating config_keys."""
    logger = Logger(name="config_managerRefresh")
    logger.info("Starting config_manager refresh...")

    # Step 1: Process .config_template files and consolidate into .config
    logger.info("Step 1: Processing .config_template files...")
    config_template = ConfigTemplate()
    success = config_template.generate_config(preserve_existing=True)

    if not success:
        logger.error("Failed to consolidate config templates into .config")
        return

    logger.info(f"Consolidated {len(config_template.consolidated_config)} module configurations")

    # Step 2: Instantiate ConfigManager to auto-generate config_keys.py
    logger.info("Step 2: Regenerating config_keys.py...")
    try:
        _ = ConfigManager(verbose=False)
        logger.info("config_keys.py regenerated successfully")
    except Exception as e:
        logger.error(f"Failed to regenerate config_keys.py: {e}")
        return

    logger.info("config_manager refresh complete!")


if __name__ == "__main__":
    main()