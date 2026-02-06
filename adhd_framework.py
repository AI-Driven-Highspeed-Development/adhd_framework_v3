#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""ADHD Framework CLI - Thin dispatcher.

All business logic lives in the modules that own it. This file contains:
- Argument parser setup
- Command dispatch map
- Thin handler methods (each <=10 lines) that delegate to module APIs
"""

import os
import sys
import argparse
from exceptions_core import ADHDError

try:
    import argcomplete
except ImportError:
    argcomplete = None


class ADHDFramework:
    """Main ADHD Framework CLI class — thin dispatcher only."""

    def __init__(self):
        from logger_util import Logger
        self.logger = Logger(__class__.__name__)

    def run(self, args):
        command_map = {
            'create-project': self.create_project_proc,
            'cp': self.create_project_proc,
            'create-module': self.create_module_proc,
            'cm': self.create_module_proc,
            'init': self.init_project,
            'i': self.init_project,
            'sync': self.sync_project,
            's': self.sync_project,
            'refresh': self.refresh_project,
            'r': self.refresh_project,
            'list': self.list_modules,
            'ls': self.list_modules,
            'info': self.show_module_info,
            'in': self.show_module_info,
            'workspace': self.update_workspace,
            'ws': self.update_workspace,
            'migrate': self.migrate_modules,
            'mg': self.migrate_modules,
            'doctor': self.doctor_check,
            'doc': self.doctor_check,
            'deps': self.deps_check,
            'dp': self.deps_check,
            'add': self.add_module,
            'a': self.add_module,
        }

        handler = command_map.get(args.command)
        if handler:
            handler(args)

    # ------------------------------------------------------------------
    # Wizard commands (already thin)
    # ------------------------------------------------------------------

    def create_project_proc(self, args) -> None:
        from creator_common_core import QuestionaryCore
        from project_creator_core.project_creation_wizard import run_project_creation_wizard
        run_project_creation_wizard(
            prompter=QuestionaryCore(),
            logger=self.logger,
        )

    def create_module_proc(self, args) -> None:
        from creator_common_core import QuestionaryCore
        from module_creator_core.module_creation_wizard import run_module_creation_wizard
        run_module_creation_wizard(
            prompter=QuestionaryCore(),
            logger=self.logger,
        )

    # ------------------------------------------------------------------
    # Sync / Init / Refresh
    # ------------------------------------------------------------------

    def init_project(self, args) -> None:
        self.logger.info("Initializing project with uv sync...")
        self.logger.info("\U0001f4a1 Tip: 'adhd init' is now 'adhd sync' (keeping 'init' for compatibility)")
        self._do_sync(args)

    def sync_project(self, args) -> None:
        self.logger.info("Synchronizing project dependencies...")
        self._do_sync(args)

    def _do_sync(self, args) -> None:
        from modules_controller_core import ModulesController
        try:
            ModulesController().sync(frozen=getattr(args, 'frozen', False))
            self.logger.info("\u2705 Project sync completed successfully!")
        except ADHDError as e:
            self.logger.error(f"\u274c {e}")
            sys.exit(1)

    def refresh_project(self, args) -> None:
        from modules_controller_core import ModulesController
        try:
            ModulesController().refresh(
                module_name=getattr(args, 'module', None),
                skip_sync=getattr(args, 'no_sync', False),
                full=getattr(args, 'full', False),
            )
        except ADHDError as e:
            self.logger.error(f"\u274c {e}")
            sys.exit(1)

    # ------------------------------------------------------------------
    # List / Info
    # ------------------------------------------------------------------

    def list_modules(self, args) -> None:
        from modules_controller_core import (
            ModulesController,
            FilterInfo,
        )

        if getattr(args, 'show_filters', False):
            print(FilterInfo.get_available().format())
            return

        controller = ModulesController()
        report = controller.list_all_modules()

        filter_obj = self._build_filter(args)
        print(report.format(filter_obj))

    def show_module_info(self, args) -> None:
        from modules_controller_core import ModulesController
        try:
            module = ModulesController().require_module(args.module)
            print(module.format_detail())
        except ADHDError as e:
            self.logger.error(f"\u274c {e}")
            sys.exit(1)

    # ------------------------------------------------------------------
    # Migrate
    # ------------------------------------------------------------------

    def migrate_modules(self, args) -> None:
        from modules_controller_core import ModulesController

        controller = ModulesController()
        dry_run = getattr(args, 'dry_run', False)
        keep = getattr(args, 'keep', False)
        module_name = getattr(args, 'module', None)

        if dry_run:
            self.logger.info("\U0001f50d Dry run mode - no changes will be made")

        if module_name:
            try:
                module = controller.require_module(module_name)
            except ADHDError as e:
                self.logger.error(f"\u274c {e}")
                sys.exit(1)

            result = controller.migrate_module(module.path, dry_run=dry_run, keep_init_yaml=keep)
            status = "\u2705" if result.success else "\u274c"
            print(f"  {status} {result.module_name}: {result.message}")
            if not result.success:
                sys.exit(1)
        else:
            results = controller.migrate_all_modules(dry_run=dry_run, keep_init_yaml=keep)
            if not results:
                self.logger.info("\u2705 No modules need migration")
                return

            success_count = sum(1 for r in results if r.success)
            fail_count = len(results) - success_count

            print(f"\n\U0001f4e6 Migration {'preview' if dry_run else 'results'}:")
            for result in results:
                status = "\u2705" if result.success else "\u274c"
                print(f"  {status} {result.module_name}: {result.message}")

            print(f"\n{'Would migrate' if dry_run else 'Migrated'}: {success_count} modules")
            if fail_count > 0:
                print(f"Failed: {fail_count} modules")
                sys.exit(2 if success_count == 0 else 1)

    # ------------------------------------------------------------------
    # Doctor
    # ------------------------------------------------------------------

    def doctor_check(self, args) -> None:
        from modules_controller_core import ModulesController
        controller = ModulesController()
        report = controller.doctor_check()
        print(report.format())
        if report.error_count > 0:
            sys.exit(1)

    # ------------------------------------------------------------------
    # Deps
    # ------------------------------------------------------------------

    def deps_check(self, args) -> None:
        from modules_controller_core import ModulesController, DependencyWalker

        controller = ModulesController()

        if getattr(args, 'closure_all', False):
            self._deps_check_all(controller)
            return

        module_name = getattr(args, 'closure', None) or getattr(args, 'module', None)
        if not module_name:
            self.logger.error("Please specify a module with --closure <module_name> or use --closure-all")
            sys.exit(1)

        if "/" in module_name:
            module_name = module_name.split("/")[-1]

        try:
            controller.require_module(module_name)
        except ADHDError as e:
            self.logger.error(f"\u274c {e}")
            sys.exit(1)

        walker = DependencyWalker(controller)
        closure = walker.walk_dependencies(module_name)
        print(closure.format())
        if closure.has_violations:
            sys.exit(1)

    def _deps_check_all(self, controller) -> None:
        from modules_controller_core import DependencyWalker, format_all_violations

        report = controller.list_all_modules()
        walker = DependencyWalker(controller)

        print(f"\n\U0001f50d Checking layer violations across {len(report.modules)} modules...\n")

        results = []
        for module in report.modules:
            try:
                closure = walker.walk_dependencies(module.name)
                results.append((module.name, closure))
            except Exception as e:
                self.logger.warning(f"\u26a0\ufe0f  Could not check {module.name}: {e}")

        print(format_all_violations(results, len(report.modules)))

        has_violations = any(c.has_violations for _, c in results)
        if has_violations:
            sys.exit(1)

    # ------------------------------------------------------------------
    # Workspace
    # ------------------------------------------------------------------

    def update_workspace(self, args) -> None:
        from modules_controller_core import ModulesController, WorkspaceGenerationMode

        controller = ModulesController()
        overrides = {}

        mode = WorkspaceGenerationMode.DEFAULT
        if args.all:
            mode = WorkspaceGenerationMode.INCLUDE_ALL
        elif args.ignore_overrides:
            mode = WorkspaceGenerationMode.IGNORE_OVERRIDES

        filter_obj = self._build_filter(args)

        if args.module:
            try:
                module = controller.require_module(args.module)
            except ADHDError as e:
                self.logger.error(f"\u274c {e}")
                sys.exit(1)

            current_visibility = module.shows_in_workspace
            if current_visibility is None:
                current_visibility = module.default_shows_in_workspace()

            overrides[module.name] = not current_visibility
            self.logger.info(
                f"Temporarily toggling workspace visibility for {module.name} to {not current_visibility}"
            )

        path = controller.generate_workspace_file(mode=mode, overrides=overrides, module_filter=filter_obj)

        if filter_obj and filter_obj.has_filters:
            self.logger.info(f"\U0001f4cb Filter applied: {filter_obj.mode.value} mode")

        self.logger.info(f"\u2705 Workspace file updated at: {path}")

    # ------------------------------------------------------------------
    # Add Module
    # ------------------------------------------------------------------

    def add_module(self, args) -> None:
        from module_adder_core import ModuleAdder

        if getattr(args, 'pypi', False):
            try:
                ModuleAdder().add_from_pypi(args.source)
            except NotImplementedError as e:
                self.logger.error(f"\u274c {e}")
                sys.exit(1)
            return

        adder = ModuleAdder()
        result = adder.add_from_repo(
            args.source,
            subfolder=getattr(args, 'path', None),
            keep_git=getattr(args, 'keep_git', False),
            add_to_root=getattr(args, 'add_to_root', None),
            skip_prompt=getattr(args, 'skip_prompt', False),
        )
        if not result.success:
            self.logger.error(f"\u274c {result.message}")
            sys.exit(1)
        self.logger.info(f"\u2705 {result.message}")

    # ------------------------------------------------------------------
    # Helper: build filter from args
    # ------------------------------------------------------------------

    def _build_filter(self, args):
        """Build a ModuleFilter from CLI args, or return None."""
        from modules_controller_core import ModuleFilter, FilterMode

        if getattr(args, 'include', None):
            return ModuleFilter.from_args(FilterMode.INCLUDE, args.include)
        elif getattr(args, 'require', None):
            return ModuleFilter.from_args(FilterMode.REQUIRE, args.require)
        elif getattr(args, 'exclude', None):
            return ModuleFilter.from_args(FilterMode.EXCLUDE, args.exclude)
        return None


def module_completer(prefix, parsed_args, **kwargs):
    """Autocomplete module names with type grouping."""
    os.environ["ADHD_LOG_LEVEL"] = "CRITICAL"
    try:
        from modules_controller_core import ModulesController
        controller = ModulesController()
        report = controller.list_all_modules()
        options = [f"{m.folder}/{m.name}" for m in report.modules]
        return [o for o in options if o.startswith(prefix)]
    except Exception:
        return []


def setup_parser() -> argparse.ArgumentParser:
    """Configure and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="ADHD Framework CLI - AI-Driven High-speed Development Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    subparsers.add_parser('create-project', aliases=['cp'], help='Create a new ADHD project')
    subparsers.add_parser('create-module', aliases=['cm'], help='Create a new module')

    # Sync command (primary) and init (alias for backward compat)
    sync_parser = subparsers.add_parser('sync', aliases=['s'], help='Synchronize project dependencies using uv')
    sync_parser.add_argument('--frozen', action='store_true', help="Don't update lockfile (pass to uv sync --frozen)")
    subparsers.add_parser('init', aliases=['i'], help='Initialize project (alias for sync)')

    refresh_parser = subparsers.add_parser('refresh', aliases=['r'], help='Refresh project modules')
    refresh_parser.add_argument('--no-sync', '-n', action='store_true', help='Skip running uv sync before refreshing')
    refresh_parser.add_argument('--full', '-f', action='store_true', help='Also run refresh_full.py scripts (heavy operations)')
    refresh_arg = refresh_parser.add_argument('--module', '-m', help='Refresh specific module by name')
    if argcomplete:
        refresh_arg.completer = module_completer

    # List command with filters
    list_parser = subparsers.add_parser('list', aliases=['ls'], help='List all discovered modules')
    list_parser.add_argument('--show-filters', action='store_true', help='Show available filter values')
    filter_group = list_parser.add_mutually_exclusive_group()
    filter_group.add_argument('-i', '--include', nargs='+', metavar='FILTER',
                              help='Include only matching modules (layer/type/state)')
    filter_group.add_argument('-r', '--require', nargs='+', metavar='FILTER',
                              help='Require all filters to match (AND logic)')
    filter_group.add_argument('-x', '--exclude', nargs='+', metavar='FILTER',
                              help='Exclude matching modules')

    info_parser = subparsers.add_parser('info', aliases=['in'], help='Show detailed module information')
    info_arg = info_parser.add_argument('--module', '-m', required=True, help='Module name to show information for')
    if argcomplete:
        info_arg.completer = module_completer

    workspace_parser = subparsers.add_parser('workspace', aliases=['ws'], help='Update VS Code workspace file')
    workspace_parser.add_argument('--all', action='store_true', help='Include all modules regardless of settings')
    workspace_parser.add_argument('--ignore-overrides', action='store_true', help='Ignore module-level overrides')
    workspace_arg = workspace_parser.add_argument('--module', '-m', help='Toggle workspace visibility for a specific module')
    workspace_filter_group = workspace_parser.add_mutually_exclusive_group()
    workspace_filter_group.add_argument('-i', '--include', nargs='+', metavar='FILTER',
                                        help='Include only matching modules (layer/type/state)')
    workspace_filter_group.add_argument('-r', '--require', nargs='+', metavar='FILTER',
                                        help='Require all filters to match (AND logic)')
    workspace_filter_group.add_argument('-x', '--exclude', nargs='+', metavar='FILTER',
                                        help='Exclude matching modules')
    if argcomplete:
        workspace_arg.completer = module_completer

    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', aliases=['mg'], help='Migrate init.yaml to pyproject.toml')
    migrate_parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would be migrated without making changes')
    migrate_parser.add_argument('--keep', '-k', action='store_true', help='Keep init.yaml after migration (for backup)')
    migrate_arg = migrate_parser.add_argument('--module', '-m', help='Migrate specific module only (default: all)')
    if argcomplete:
        migrate_arg.completer = module_completer

    # Doctor command
    subparsers.add_parser('doctor', aliases=['doc'], help='Check module health and report issues')

    # Deps command
    deps_parser = subparsers.add_parser('deps', aliases=['dp'], help='Analyze module dependencies')
    deps_closure_arg = deps_parser.add_argument('--closure', '-c', metavar='MODULE',
                                                 help='Show dependency tree for a module with layer labels')
    deps_parser.add_argument('--closure-all', action='store_true',
                             help='Check layer violations across ALL modules (for CI)')
    if argcomplete:
        deps_closure_arg.completer = module_completer

    # Add command - supports repo, monorepo subfolder, and (future) PyPI
    add_parser = subparsers.add_parser('add', aliases=['a'], help='Add a module to the workspace')
    add_parser.add_argument('source', help='Git repository URL (or package name with --pypi)')
    add_parser.add_argument('--path', help='Subfolder within repo to extract (monorepo mode)')
    add_parser.add_argument('--keep-git', action='store_true', help='Preserve .git/ directory')
    add_parser.add_argument('--add-to-root', action='store_true', default=None,
                           help='Add to root pyproject.toml without prompting')
    add_parser.add_argument('--skip-prompt', '-y', action='store_true',
                           help='Skip all interactive prompts, use defaults')
    add_parser.add_argument('--pypi', action='store_true',
                           help='Treat source as a PyPI package name (not yet available)')

    if argcomplete:
        argcomplete.autocomplete(parser)

    return parser


def main() -> None:
    """Main entry point for the ADHD Framework CLI."""
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
    else:
        framework = ADHDFramework()
        framework.run(args)


if __name__ == "__main__":
    main()
