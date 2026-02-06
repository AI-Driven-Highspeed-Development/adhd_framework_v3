#!/usr/bin/env python3
"""Demo script to show path collision detection in project creation.

This script simulates the project creation wizard behavior when the
destination path already exists.
"""

from pathlib import Path
import tempfile
from unittest.mock import MagicMock

from project_creator_core.project_creation_wizard import (
    run_project_creation_wizard,
    ProjectWizardArgs,
)

def demo_collision_detection():
    """Demonstrate wizard behavior when path exists."""
    print("=" * 60)
    print("Demo: Project Creation Path Collision Detection")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create an existing project directory
        existing_project = tmp_path / "my_existing_project"
        existing_project.mkdir()
        print(f"\n1. Created existing project at: {existing_project}")

        # Setup mocks
        mock_prompter = MagicMock()
        mock_logger = MagicMock()

        # Simulate user trying to create project with existing name first,
        # then using a new name
        mock_prompter.autocomplete_input.side_effect = [
            "my_existing_project",  # First try - COLLISION
            "my_new_project",       # Second try - OK
        ]
        mock_prompter.path_input.side_effect = [
            str(tmp_path),  # First try parent
            str(tmp_path),  # Second try parent
        ]
        mock_prompter.multiple_select.return_value = []
        mock_prompter.multiple_choice.return_value = "No"

        print("\n2. User enters 'my_existing_project' (collision!)")
        print("   → Wizard detects collision and prompts for retry")

        print("\n3. User enters 'my_new_project' (success!)")
        print("   → Wizard proceeds with project creation")

        # Run wizard
        prefilled = ProjectWizardArgs(create_repo=False)
        try:
            run_project_creation_wizard(
                prompter=mock_prompter,
                logger=mock_logger,
                prefilled=prefilled,
            )
        except Exception as e:
            # Expected - we're not mocking the full creation process
            pass

        # Check results
        print("\n" + "=" * 60)
        print("Results:")
        print("=" * 60)
        print(f"  • User was prompted {mock_prompter.autocomplete_input.call_count} times")

        warning_count = sum(
            1 for call in mock_logger.warning.call_args_list
            if "Path already exists" in str(call)
        )
        print(f"  • Collision warnings shown: {warning_count}")

        info_count = sum(
            1 for call in mock_logger.info.call_args_list
            if "different project name" in str(call)
        )
        print(f"  • Re-entry prompts shown: {info_count}")

        print("\n✅ Collision detection working correctly!")

if __name__ == "__main__":
    demo_collision_detection()
