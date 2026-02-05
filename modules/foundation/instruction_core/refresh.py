from __future__ import annotations
import sys
from pathlib import Path

from .instruction_controller import InstructionController
from logger_util import Logger

def main() -> None:
    """
    Refresh script for instruction_core.
    Syncs instructions and agents to .github/ folder.
    """
    logger = Logger(name="InstructionCoreRefresh")
    logger.info("Starting instruction core refresh...")
    
    try:
        # Initialize controller with current working directory as root
        # When run via adhd_cli refresh, cwd is set to project root
        controller = InstructionController(root_path=Path.cwd(), logger=logger)
        controller.run()
        logger.info("Instruction core refresh completed successfully.")
    except Exception as e:
        logger.error(f"Instruction core refresh failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
