from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from creator_common_core import (
    RepoCreationOptions,
    to_snake_case,
    QuestionaryCore,
)
from .project_creator import ProjectCreator, ProjectParams
from .preload_sets import parse_preload_sets, PreloadSet, ModuleSource
from exceptions_core import ADHDError
from logger_util import Logger
from .yaml_utils import YamlReader


@dataclass
class ProjectWizardArgs:
    """Pre-filled arguments for project creation wizard."""
    name: Optional[str] = None
    parent_dir: Optional[str] = None
    description: Optional[str] = None  # Project description
    preload_sets: Optional[List[str]] = None  # Selected optional module sets (e.g., ["HyperPM"])
    create_repo: Optional[bool] = None  # None = ask, True = yes, False = no
    owner: Optional[str] = None
    visibility: Optional[str] = None  # "public" or "private"


def run_project_creation_wizard(
    *,
    prompter: QuestionaryCore,
    logger: Logger,
    prefilled: Optional[ProjectWizardArgs] = None,
) -> None:
    """Guide the user through the interactive project scaffolding workflow.
    
    Creates a new project using embedded templates (no external cloning).
    
    Args:
        prompter: QuestionaryCore instance for interactive prompts
        logger: Logger instance
        prefilled: Pre-filled arguments to skip corresponding prompts
    """
    if prefilled is None:
        prefilled = ProjectWizardArgs()

    try:
        # Loop until we get a valid (non-existing) project path
        while True:
            # Project name
            if prefilled.name:
                project_name = to_snake_case(prefilled.name)
                if project_name != prefilled.name:
                    logger.info(f"Project name normalized to '{project_name}'")
            else:
                raw_project_name = prompter.autocomplete_input(
                    "Project name",
                    choices=[],
                    default="my_project",
                )
                project_name = to_snake_case(raw_project_name)
                if project_name != raw_project_name:
                    logger.info(f"Project name normalized to '{project_name}'")

            # Parent directory
            if prefilled.parent_dir:
                parent_dir = prefilled.parent_dir
            else:
                parent_dir = prompter.path_input(
                    "Destination parent directory",
                    default=".",
                    only_directories=True,
                )

            dest_path_obj = Path(parent_dir) / project_name
            dest_path = str(dest_path_obj)

            # Check if the destination path already exists
            if dest_path_obj.exists():
                logger.warning(f"⚠️  Path already exists: {dest_path}")
                logger.info("Please enter a different project name or parent directory.")
                # Clear prefilled values so user is prompted again
                prefilled.name = None
                prefilled.parent_dir = None
                continue

            # Valid path found, break out of loop
            break

        # Optional description
        description = prefilled.description or ""

    except KeyboardInterrupt:
        logger.info("Input cancelled. Exiting.")
        return

    # Load preload sets
    module_sources = _load_and_select_preload_sets(prompter, logger, prefilled)

    # GitHub repository creation
    try:
        repo_options = _prompt_repo_creation(prompter, logger, prefilled)
    except KeyboardInterrupt:
        logger.info("Repository creation cancelled. Exiting.")
        return

    # Create the project using embedded templates
    params = ProjectParams(
        repo_path=dest_path,
        module_sources=module_sources,
        project_name=project_name,
        description=description,
        repo_options=repo_options,
    )
    creator = ProjectCreator(params)
    try:
        dest = creator.create()
    except ADHDError as exc:  # pragma: no cover - CLI flow
        logger.error(f"❌ Failed to create project: {exc}")
        return

    logger.info(f"✅ Project created at: {dest}")
    logger.info("")
    logger.info("Next steps:")
    logger.info(f"  cd {dest}")
    logger.info(f"  source .venv/bin/activate  # activate the venv")
    logger.info("")
    logger.info("Then you can use the adhd command directly:")
    logger.info("  adhd --help")
    logger.info("  adhd new-module  # to add modules")
    logger.info("")
    logger.info("Or use 'uv run' without activating:")
    logger.info("  uv run adhd --help")


# Path to preload sets YAML file
PRELOAD_SETS_PATH = Path(__file__).parent / "data" / "module_preload_sets.yaml"


def _load_and_select_preload_sets(
    prompter: QuestionaryCore,
    logger: Logger,
    prefilled: ProjectWizardArgs,
) -> List[ModuleSource]:
    """Load preload sets and prompt user to select optional module bundles.
    
    Returns:
        List of ModuleSource for all modules to install (always + selected options)
    """
    # Load the preload sets YAML
    if not PRELOAD_SETS_PATH.exists():
        logger.warning(f"Preload sets file not found: {PRELOAD_SETS_PATH}")
        return []
    
    try:
        yf = YamlReader.read_yaml(PRELOAD_SETS_PATH)
        always_modules, optional_sets = parse_preload_sets(yf)
    except Exception as exc:
        logger.warning(f"Failed to load preload sets: {exc}")
        return []
    
    # Start with the "always" modules (core dependencies)
    module_sources = list(always_modules)
    logger.info(f"📦 Including {len(always_modules)} core modules automatically:")
    for src in always_modules:
        logger.info(f"   • {src.display_name}")
    
    # If no optional sets available, return just the always modules
    if not optional_sets:
        return module_sources
    
    # Handle optional set selection
    selected_set_names: List[str] = []
    
    if prefilled.preload_sets is not None:
        # Use pre-filled selection
        selected_set_names = prefilled.preload_sets
    else:
        # Prompt user to select optional module bundles
        set_choices = [f"{s.name} - {s.description}" for s in optional_sets]
        
        try:
            logger.info("")  # Blank line for visual separation
            logger.info("🎯 Optional module bundles available:")
            selected_labels = prompter.multiple_select(
                "Select additional bundles (↑↓ to move, SPACE to toggle, ENTER to confirm)",
                choices=set_choices,
            )
            # Extract set names from the labels
            selected_set_names = [label.split(" - ")[0] for label in selected_labels]
        except KeyboardInterrupt:
            logger.info("Module selection cancelled. Using only core modules.")
            return module_sources
    
    # Add modules from selected optional sets
    if selected_set_names:
        logger.info("")  # Blank line for visual separation
        logger.info(f"📦 Adding {len(selected_set_names)} optional bundle(s):")
    for opt_set in optional_sets:
        if opt_set.name in selected_set_names:
            module_sources.extend(opt_set.modules)
            logger.info(f"   • {opt_set.name} ({len(opt_set.modules)} module(s))")
    
    # Final summary
    logger.info("")
    logger.info(f"✅ Total modules to install: {len(module_sources)}")
    
    return module_sources


def _prompt_repo_creation(
    prompter: QuestionaryCore,
    logger: Logger,
    prefilled: ProjectWizardArgs,
) -> Optional[RepoCreationOptions]:
    from github_api_core import GithubApi
    
    # Check if repo creation is pre-determined
    if prefilled.create_repo is False:
        return None
    
    if prefilled.create_repo is None:
        try:
            create_choice = prompter.multiple_choice(
                "Create a GitHub repository for this project?",
                ["Yes", "No"],
                default="Yes",
            )
        except KeyboardInterrupt:
            logger.info("Repository creation choice cancelled. Exiting.")
            raise

        if create_choice != "Yes":
            return None

    try:
        api = GithubApi()
        user_login = api.get_authenticated_user_login()
    except ADHDError as exc:
        logger.error(f"Failed to initialize GitHub CLI: {exc}")
        return None

    try:
        orgs = api.get_user_orgs()
    except ADHDError as exc:
        logger.error(f"Failed to fetch organizations: {exc}")
        orgs = []

    owner_lookup: dict[str, str] = {}
    if user_login:
        owner_lookup[f"{user_login} (personal)"] = user_login

    for org in orgs:
        login = org.get("login")
        if login and login not in owner_lookup.values():
            owner_lookup[f"{login} (org)"] = login

    if not owner_lookup:
        logger.error("No eligible GitHub owners found; skipping repository creation.")
        return None

    # Owner selection
    if prefilled.owner:
        # Validate the prefilled owner
        if prefilled.owner in owner_lookup.values():
            owner = prefilled.owner
        else:
            logger.error(f"Owner '{prefilled.owner}' not found. Available: {', '.join(owner_lookup.values())}")
            return None
    else:
        owner_labels = list(owner_lookup.keys())
        options_preview = "\n".join(f" - {label}" for label in owner_labels)
        logger.info(f"Available repository owners:\n{options_preview}")

        try:
            owner_label = prompter.multiple_choice(
                "Select repository owner",
                owner_labels
            )
        except KeyboardInterrupt:
            logger.info("Repository owner selection cancelled. Exiting.")
            raise
        owner = owner_lookup[owner_label]

    # Visibility selection
    if prefilled.visibility:
        if prefilled.visibility not in ["public", "private"]:
            logger.error(f"Invalid visibility '{prefilled.visibility}'. Must be 'public' or 'private'.")
            return None
        visibility = prefilled.visibility
    else:
        try:
            visibility_choice = prompter.multiple_choice(
                "Repository visibility",
                ["Public", "Private"],
                default="Private",
            )
        except KeyboardInterrupt:
            logger.info("Repository visibility selection cancelled. Exiting.")
            raise
        visibility = "private" if visibility_choice == "Private" else "public"
    
    return RepoCreationOptions(owner=owner, visibility=visibility)


__all__ = ["run_project_creation_wizard", "ProjectWizardArgs"]
