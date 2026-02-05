import sys
from pathlib import Path

from .instruction_controller import InstructionController
from logger_util import Logger

__all__ = ["InstructionController"]

if __name__ == "__main__":
    # This block is executed when the file is run as a script,
    # e.g. by ProjectInit during project initialization.
    logger = Logger(name="InstructionCoreInit")
    logger.info("Running instruction core initialization...")
    try:
        controller = InstructionController(root_path=Path.cwd(), logger=logger)
        controller.run()
        logger.info("Instruction core initialization completed.")
    except Exception as e:
        logger.error(f"Instruction core initialization failed: {e}")
        sys.exit(1)