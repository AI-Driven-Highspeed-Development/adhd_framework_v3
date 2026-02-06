"""Tests for project creation wizard path collision detection."""
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from project_creator_core.project_creation_wizard import (
    run_project_creation_wizard,
    ProjectWizardArgs,
)


class TestProjectPathCollisionDetection:
    """Test that wizard prompts user to re-enter when path already exists."""

    def test_existing_path_prompts_retry(self, tmp_path):
        """When destination path exists, wizard should prompt user to re-enter."""
        # Create an existing project directory
        existing_project = tmp_path / "existing_project"
        existing_project.mkdir()

        # Mock prompter and logger
        mock_prompter = MagicMock()
        mock_logger = MagicMock()

        # First attempt: return existing project name
        # Second attempt: return non-existing project name
        mock_prompter.autocomplete_input.side_effect = [
            "existing_project",  # First try - exists
            "new_project",       # Second try - doesn't exist
        ]
        mock_prompter.path_input.side_effect = [
            str(tmp_path),  # First try parent dir
            str(tmp_path),  # Second try parent dir
        ]
        mock_prompter.multiple_select.return_value = []  # No optional modules
        mock_prompter.multiple_choice.return_value = "No"  # No GitHub repo

        # Run wizard (will fail at project creation since we're not mocking everything,
        # but we only care about the path collision detection logic)
        prefilled = ProjectWizardArgs(
            create_repo=False,  # Skip GitHub repo creation prompts
        )

        try:
            run_project_creation_wizard(
                prompter=mock_prompter,
                logger=mock_logger,
                prefilled=prefilled,
            )
        except Exception:
            # Expected to fail at creation since we're not fully mocking
            pass

        # Verify that autocomplete_input was called twice (once for each attempt)
        assert mock_prompter.autocomplete_input.call_count == 2
        # Verify warning was logged about existing path
        warning_calls = [
            call for call in mock_logger.warning.call_args_list
            if "Path already exists" in str(call)
        ]
        assert len(warning_calls) == 1

    def test_prefilled_collision_clears_and_prompts(self, tmp_path):
        """When prefilled args point to existing path, wizard should clear them and prompt."""
        # Create an existing project directory
        existing_project = tmp_path / "prefilled_project"
        existing_project.mkdir()

        # Mock prompter and logger
        mock_prompter = MagicMock()
        mock_logger = MagicMock()

        # User prompted to enter a new name after collision
        mock_prompter.autocomplete_input.return_value = "new_project"
        mock_prompter.path_input.return_value = str(tmp_path)
        mock_prompter.multiple_select.return_value = []  # No optional modules
        mock_prompter.multiple_choice.return_value = "No"  # No GitHub repo

        # Prefilled args that point to existing directory
        prefilled = ProjectWizardArgs(
            name="prefilled_project",
            parent_dir=str(tmp_path),
            create_repo=False,
        )

        try:
            run_project_creation_wizard(
                prompter=mock_prompter,
                logger=mock_logger,
                prefilled=prefilled,
            )
        except Exception:
            # Expected to fail at creation since we're not fully mocking
            pass

        # Verify that warning was logged
        warning_calls = [
            call for call in mock_logger.warning.call_args_list
            if "Path already exists" in str(call)
        ]
        assert len(warning_calls) == 1

        # Verify user was prompted for new input (since prefilled was cleared)
        assert mock_prompter.autocomplete_input.call_count == 1

    def test_non_existing_path_no_retry(self, tmp_path):
        """When destination path doesn't exist, wizard should proceed without retry."""
        # Mock prompter and logger
        mock_prompter = MagicMock()
        mock_logger = MagicMock()

        # Return a project name that doesn't exist
        mock_prompter.autocomplete_input.return_value = "brand_new_project"
        mock_prompter.path_input.return_value = str(tmp_path)
        mock_prompter.multiple_select.return_value = []  # No optional modules
        mock_prompter.multiple_choice.return_value = "No"  # No GitHub repo

        prefilled = ProjectWizardArgs(create_repo=False)

        try:
            run_project_creation_wizard(
                prompter=mock_prompter,
                logger=mock_logger,
                prefilled=prefilled,
            )
        except Exception:
            # Expected to fail at creation since we're not fully mocking
            pass

        # Verify that autocomplete_input was called only once (no retry)
        assert mock_prompter.autocomplete_input.call_count == 1
        # Verify no warning was logged
        warning_calls = [
            call for call in mock_logger.warning.call_args_list
            if "Path already exists" in str(call)
        ]
        assert len(warning_calls) == 0
