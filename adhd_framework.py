#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import difflib
import os
import shutil
import sys
import subprocess
import argparse
from pathlib import Path

try:
    import argcomplete
except ImportError:
    argcomplete = None


class UVNotFoundError(Exception):
    """Raised when the 'uv' command is not found in PATH."""
    pass


def _require_uv() -> str:
    """Ensure uv is available and return its path.
    
    Raises:
        UVNotFoundError: If uv is not found in PATH.
    """
    uv_path = shutil.which("uv")
    if not uv_path:
        raise UVNotFoundError(
            "'uv' command not found. Please install uv: https://docs.astral.sh/uv/getting-started/installation/"
        )
    return uv_path


def _run_uv_sync() -> None:
    """Run 'uv sync' to synchronize project dependencies.
    
    Raises:
        UVNotFoundError: If uv is not found.
        subprocess.CalledProcessError: If uv sync fails.
    """
    uv_path = _require_uv()
    subprocess.run([uv_path, "sync"], check=True)


class ADHDFramework:
    """Main ADHD Framework CLI class"""

    def __init__(self):
        from config_manager import ConfigManager
        from logger_util import Logger
        from github_api_core import GithubApi
        from questionary_core import QuestionaryCore

        self.logger = Logger(__class__.__name__)
        self.prompter = QuestionaryCore()

        try:
            self._gh_path = GithubApi.require_gh()
        except RuntimeError as e:
            self.logger.error(f"GitHub CLI setup not complete: {e}")
            sys.exit(1)

    def run(self, args):
        command_map = {
            'create-project': self.create_project_proc,
            'cp': self.create_project_proc,
            'create-module': self.create_module_proc,
            'cm': self.create_module_proc,
            'init': self.init_project,  # Alias for sync (backward compat)
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
        }

        handler = command_map.get(args.command)
        if handler:
            handler(args)

    def create_project_proc(self, args) -> None:
        from project_creator_core.project_creation_wizard import run_project_creation_wizard
        run_project_creation_wizard(
            prompter=self.prompter,
            logger=self.logger,
        )

    def create_module_proc(self, args) -> None:
        """Enter the interactive module creation flow with templates."""
        from module_creator_core.module_creation_wizard import run_module_creation_wizard
        run_module_creation_wizard(
            prompter=self.prompter,
            logger=self.logger,
        )

    def init_project(self, args) -> None:
        """Initialize project by running uv sync.
        
        Note: This is an alias for 'sync' command for backward compatibility.
        """
        self.logger.info("Initializing project with uv sync...")
        self.logger.info("💡 Tip: 'adhd init' is now 'adhd sync' (keeping 'init' for compatibility)")
        try:
            _run_uv_sync()
            self.logger.info("✅ Project initialization completed successfully!")
        except UVNotFoundError as e:
            self.logger.error(f"❌ {e}")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ uv sync failed: {e}")
            sys.exit(1)

    def sync_project(self, args) -> None:
        """Synchronize project dependencies using uv."""
        self.logger.info("Synchronizing project dependencies...")
        try:
            uv_path = _require_uv()
            cmd = [uv_path, "sync"]
            if getattr(args, 'frozen', False):
                cmd.append("--frozen")
            subprocess.run(cmd, check=True)
            self.logger.info("✅ Project sync completed successfully!")
        except UVNotFoundError as e:
            self.logger.error(f"❌ {e}")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ uv sync failed: {e}")
            sys.exit(1)

    def migrate_modules(self, args) -> None:
        """Migrate modules from init.yaml to pyproject.toml."""
        from modules_controller_core import ModulesController
        
        controller = ModulesController()
        dry_run = getattr(args, 'dry_run', False)
        keep = getattr(args, 'keep', False)
        module_name = getattr(args, 'module', None)
        
        if dry_run:
            self.logger.info("🔍 Dry run mode - no changes will be made")
        
        if module_name:
            # Migrate specific module
            module = controller.get_module_by_name(module_name)
            if not module:
                report = controller.list_all_modules()
                all_names = [m.name for m in report.modules]
                suggestions = difflib.get_close_matches(module_name, all_names, n=3, cutoff=0.4)
                if suggestions:
                    self.logger.error(f"❌ Module '{module_name}' not found. Did you mean: {', '.join(suggestions)}?")
                else:
                    self.logger.error(f"❌ Module '{module_name}' not found. Use 'adhd list' to see available modules.")
                sys.exit(1)
            
            result = controller.migrate_module(module.path, dry_run=dry_run, keep_init_yaml=keep)
            status = "✅" if result.success else "❌"
            print(f"  {status} {result.module_name}: {result.message}")
            
            if not result.success:
                sys.exit(1)
        else:
            # Migrate all modules
            results = controller.migrate_all_modules(dry_run=dry_run, keep_init_yaml=keep)
            
            if not results:
                self.logger.info("✅ No modules need migration")
                return
            
            success_count = sum(1 for r in results if r.success)
            fail_count = len(results) - success_count
            
            print(f"\n📦 Migration {'preview' if dry_run else 'results'}:")
            for result in results:
                status = "✅" if result.success else "❌"
                print(f"  {status} {result.module_name}: {result.message}")
            
            print(f"\n{'Would migrate' if dry_run else 'Migrated'}: {success_count} modules")
            if fail_count > 0:
                print(f"Failed: {fail_count} modules")
                # Exit code 2 if ALL modules failed, code 1 if partial failure
                sys.exit(2 if success_count == 0 else 1)

    def doctor_check(self, args) -> None:
        """Check module health and report issues."""
        from modules_controller_core import ModulesController, DoctorIssueSeverity
        
        controller = ModulesController()
        report = controller.doctor_check()
        
        # Group issues by severity
        errors = [i for i in report.issues if i.severity == DoctorIssueSeverity.ERROR]
        warnings = [i for i in report.issues if i.severity == DoctorIssueSeverity.WARNING]
        infos = [i for i in report.issues if i.severity == DoctorIssueSeverity.INFO]
        
        print(f"\n🩺 Doctor Report: {report.modules_checked} modules checked\n")
        
        if report.is_healthy and not warnings:
            print("✅ All modules are healthy!\n")
            return
        
        if errors:
            print("❌ Errors (must fix):")
            for issue in errors:
                print(f"  • {issue.message}")
                if issue.suggestion:
                    print(f"    💡 {issue.suggestion}")
            print()
        
        if warnings:
            print("⚠️  Warnings (should fix):")
            for issue in warnings:
                print(f"  • {issue.message}")
                if issue.suggestion:
                    print(f"    💡 {issue.suggestion}")
            print()
        
        if infos:
            print("ℹ️  Info:")
            for issue in infos:
                print(f"  • {issue.message}")
            print()
        
        # Summary
        print(f"Summary: {report.error_count} errors, {report.warning_count} warnings, {report.info_count} info")
        
        if report.error_count > 0:
            sys.exit(1)

    def deps_check(self, args) -> None:
        """Check dependency closure and detect layer violations."""
        from modules_controller_core import (
            ModulesController,
            DependencyWalker,
            ViolationType,
            format_dependency_tree,
        )
        
        controller = ModulesController()
        
        module_name = getattr(args, 'closure', None) or getattr(args, 'module', None)
        if not module_name:
            self.logger.error("Please specify a module with --closure <module_name>")
            sys.exit(1)
        
        # Handle 'type/name' format
        if "/" in module_name:
            module_name = module_name.split("/")[-1]
        
        # Check if module exists
        module = controller.get_module_by_name(module_name)
        if not module:
            report = controller.list_all_modules()
            all_names = [m.name for m in report.modules]
            suggestions = difflib.get_close_matches(module_name, all_names, n=3, cutoff=0.4)
            if suggestions:
                self.logger.error(f"❌ Module '{module_name}' not found. Did you mean: {', '.join(suggestions)}?")
            else:
                self.logger.error(f"❌ Module '{module_name}' not found. Use 'adhd list' to see available modules.")
            sys.exit(1)
        
        walker = DependencyWalker(controller)
        closure = walker.walk_dependencies(module_name)
        
        # Print dependency tree
        print(f"\n🌳 Dependency Tree for {module_name}:\n")
        print(format_dependency_tree(closure.tree))
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"  • ADHD modules: {len(closure.adhd_deps)}")
        print(f"  • External packages: {len(closure.external_deps)}")
        print(f"  • Total dependencies: {len(closure.all_deps)}")
        
        # Print violations if any
        if closure.has_violations:
            print(f"\n❌ Layer Violations Found ({len(closure.violations)}):\n")
            for violation in closure.violations:
                if violation.violation_type == ViolationType.CROSS_LAYER:
                    print(f"  • {violation.message}")
                else:
                    print(f"  • {violation.message}")
            
            print("\n💡 Tip: Layer hierarchy is foundation < runtime < dev")
            print("   A module can only depend on modules at the same or lower layer.")
            sys.exit(1)
        else:
            print("\n✅ No layer violations found!")

    def refresh_project(self, args) -> None:
        """Refresh project modules."""
        from modules_controller_core import ModulesController
        
        # Handle --sync flag: run uv sync first
        if getattr(args, 'sync', False):
            self.logger.info("Running uv sync before refresh...")
            try:
                _run_uv_sync()
                self.logger.info("✅ uv sync completed")
            except UVNotFoundError as e:
                self.logger.error(f"❌ {e}")
                sys.exit(1)
            except subprocess.CalledProcessError as e:
                self.logger.error(f"❌ uv sync failed: {e}")
                sys.exit(1)
        
        controller = ModulesController()
        if args.module:
            self.logger.info(f"Refreshing module: {args.module}")
            module = controller.get_module_by_name(args.module)
            if module:
                controller.run_module_refresh_script(module)
                self.logger.info(f"✅ Module {args.module} refreshed!")
            else:
                # Suggest similar module names
                report = controller.list_all_modules()
                all_names = [m.name for m in report.modules]
                suggestions = difflib.get_close_matches(args.module, all_names, n=3, cutoff=0.4)
                if suggestions:
                    self.logger.error(f"❌ Module '{args.module}' not found. Did you mean: {', '.join(suggestions)}?")
                else:
                    self.logger.error(f"❌ Module '{args.module}' not found. Use 'adhd list' to see available modules.")
                sys.exit(1)
        else:
            self.logger.info("Refreshing all modules...")
            report = controller.list_all_modules()
            for module in report.modules:
                if module.has_refresh_script():
                    controller.run_module_refresh_script(module)
            self.logger.info("✅ Project refresh completed!")

    def list_modules(self, args) -> None:
        """List all modules with optional filtering."""
        from modules_controller_core import (
            ModulesController,
            ModuleFilter,
            FilterMode,
            FilterInfo,
        )
        
        # Handle --show-filters flag
        if getattr(args, 'show_filters', False):
            print(FilterInfo.get_available().format())
            return
        
        controller = ModulesController()
        report = controller.list_all_modules()
        modules = report.modules
        
        # Build filter from args
        filter_obj = None
        if getattr(args, 'include', None):
            filter_obj = ModuleFilter(mode=FilterMode.INCLUDE)
            for val in args.include:
                filter_obj = self._add_filter_value(filter_obj, val)
        elif getattr(args, 'require', None):
            filter_obj = ModuleFilter(mode=FilterMode.REQUIRE)
            for val in args.require:
                filter_obj = self._add_filter_value(filter_obj, val)
        elif getattr(args, 'exclude', None):
            filter_obj = ModuleFilter(mode=FilterMode.EXCLUDE)
            for val in args.exclude:
                filter_obj = self._add_filter_value(filter_obj, val)
        
        # Apply filter
        if filter_obj and filter_obj.has_filters:
            modules = filter_obj.filter_modules(modules)
        
        print(f"\n📦 Found {len(modules)} modules:")
        for module in modules:
            status = "⚠️ " if module.issues else "✅"
            layer_str = module.layer.value if module.layer else "?"
            print(f"  {status} {module.name} ({module.module_type.name}) [{layer_str}] - v{module.version}")
            if module.issues:
                for issue in module.issues:
                    print(f"     - {issue.message}")
    
    def _add_filter_value(self, filter_obj: "ModuleFilter", value: str) -> "ModuleFilter":
        """Add a filter value, auto-detecting the dimension."""
        from modules_controller_core import ModuleLayer, ModuleTypeEnum, GitState
        
        value_lower = value.lower()
        
        # Try layer first
        if ModuleLayer.validate(value_lower):
            return filter_obj.add_layer(value_lower)
        
        # Try type
        try:
            ModuleTypeEnum(value_lower)
            return filter_obj.add_type(value_lower)
        except ValueError:
            pass
        
        # Try git state
        try:
            GitState(value_lower)
            return filter_obj.add_state(value_lower)
        except ValueError:
            pass
        
        self.logger.warning(f"Unknown filter value: {value}")
        return filter_obj

    def show_module_info(self, args) -> None:
        """Show module info."""
        from modules_controller_core import ModulesController
        controller = ModulesController()
        module = controller.get_module_by_name(args.module)
        
        if not module:
            # Suggest similar module names
            report = controller.list_all_modules()
            all_names = [m.name for m in report.modules]
            suggestions = difflib.get_close_matches(args.module, all_names, n=3, cutoff=0.4)
            if suggestions:
                self.logger.error(f"❌ Module '{args.module}' not found. Did you mean: {', '.join(suggestions)}?")
            else:
                self.logger.error(f"❌ Module '{args.module}' not found. Use 'adhd list' to see available modules.")
            sys.exit(1)

        print(f"\n📦 MODULE INFORMATION: {module.name}")
        print(f"  📁 Path: {module.path}")
        print(f"  📂 Type: {module.module_type.name}")
        print(f"  🏷️  Version: {module.version}")
        layer_display = module.layer.value if module.layer else "N/A"
        print(f"  📊 Layer: {layer_display}")
        print(f"  🔗 Repo URL: {module.repo_url or 'N/A'}")
        
        reqs = ", ".join(module.requirements) if module.requirements else "None"
        print(f"  🧱 Requirements: {reqs}")
        
        print(f"  🔄 Has Refresh Script: {'Yes' if module.has_refresh_script() else 'No'}")
        print(f"  🚀 Has Initializer: {'Yes' if module.has_initializer() else 'No'}")
        
        if module.issues:
            print("  ⚠️  Issues:")
            for issue in module.issues:
                print(f"    - {issue.message}")

    def update_workspace(self, args) -> None:
        """Update VS Code workspace file."""
        from modules_controller_core import (
            ModulesController,
            WorkspaceGenerationMode,
            ModuleFilter,
            FilterMode,
        )
        
        controller = ModulesController()
        overrides = {}
        
        mode = WorkspaceGenerationMode.DEFAULT
        if args.all:
            mode = WorkspaceGenerationMode.INCLUDE_ALL
        elif args.ignore_overrides:
            mode = WorkspaceGenerationMode.IGNORE_OVERRIDES
        
        # Build filter from args (same pattern as list_modules)
        filter_obj = None
        if getattr(args, 'include', None):
            filter_obj = ModuleFilter(mode=FilterMode.INCLUDE)
            for val in args.include:
                filter_obj = self._add_filter_value(filter_obj, val)
        elif getattr(args, 'require', None):
            filter_obj = ModuleFilter(mode=FilterMode.REQUIRE)
            for val in args.require:
                filter_obj = self._add_filter_value(filter_obj, val)
        elif getattr(args, 'exclude', None):
            filter_obj = ModuleFilter(mode=FilterMode.EXCLUDE)
            for val in args.exclude:
                filter_obj = self._add_filter_value(filter_obj, val)

        if args.module:
            module = controller.get_module_by_name(args.module)
            if not module:
                # Suggest similar module names
                report = controller.list_all_modules()
                all_names = [m.name for m in report.modules]
                suggestions = difflib.get_close_matches(args.module, all_names, n=3, cutoff=0.4)
                if suggestions:
                    self.logger.error(f"❌ Module '{args.module}' not found. Did you mean: {', '.join(suggestions)}?")
                else:
                    self.logger.error(f"❌ Module '{args.module}' not found. Use 'adhd list' to see available modules.")
                sys.exit(1)
            
            # Determine current visibility based on mode to toggle it
            current_visibility = False
            if mode == WorkspaceGenerationMode.INCLUDE_ALL:
                current_visibility = True
            elif mode == WorkspaceGenerationMode.IGNORE_OVERRIDES:
                current_visibility = module.module_type.shows_in_workspace
            else:
                current_visibility = module.shows_in_workspace
                if current_visibility is None:
                    current_visibility = module.module_type.shows_in_workspace
            
            new_visibility = not current_visibility
            overrides[module.name] = new_visibility
            self.logger.info(f"Temporarily toggling workspace visibility for {module.name} to {new_visibility}")

        path = controller.generate_workspace_file(mode=mode, overrides=overrides, module_filter=filter_obj)
        
        # Show filter info if applied
        if filter_obj and filter_obj.has_filters:
            self.logger.info(f"📋 Filter applied: {filter_obj.mode.value} mode")
        
        self.logger.info(f"✅ Workspace file updated at: {path}")


def module_completer(prefix, parsed_args, **kwargs):
    """Autocomplete module names with type grouping."""
    # Suppress logging to prevent corrupting shell completion output
    os.environ["ADHD_LOG_LEVEL"] = "CRITICAL"
    try:
        from modules_controller_core import ModulesController
        controller = ModulesController()
        report = controller.list_all_modules()
        
        # Return modules in 'type/name' format for better organization
        # e.g. 'managers/config_manager', 'cores/project_init_core'
        options = []
        for m in report.modules:
            # Use plural name for grouping (e.g. 'managers', 'cores')
            type_name = m.module_type.plural_name.lower()
            option = f"{type_name}/{m.name}"
            options.append(option)
            
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
    refresh_parser.add_argument('--sync', '-s', action='store_true', help='Run uv sync before refreshing')
    refresh_arg = refresh_parser.add_argument('--module', '-m', help='Refresh specific module by name')
    if argcomplete:
        refresh_arg.completer = module_completer

    # List command with filters
    list_parser = subparsers.add_parser('list', aliases=['ls'], help='List all discovered modules')
    list_parser.add_argument('--show-filters', action='store_true', help='Show available filter values')
    # Filter mode group (mutually exclusive)
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
    # Filter flags (same as list command)
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
    doctor_parser = subparsers.add_parser('doctor', aliases=['doc'], help='Check module health and report issues')
    doctor_parser.add_argument('--fix', '-f', action='store_true', help='Attempt to fix simple issues (placeholder)')
    doctor_parser.add_argument('--json', '-j', action='store_true', help='Output in JSON format (placeholder)')

    # Deps command - dependency closure and violation detection
    deps_parser = subparsers.add_parser('deps', aliases=['dp'], help='Analyze module dependencies')
    deps_closure_arg = deps_parser.add_argument('--closure', '-c', metavar='MODULE',
                                                 help='Show dependency tree for a module with layer labels')
    if argcomplete:
        deps_closure_arg.completer = module_completer

    if argcomplete:
        argcomplete.autocomplete(parser)
        
    return parser


def main() -> None:
    """Main entry point for the ADHD Framework CLI.
    
    This function is called when running the CLI via the 'adhd' command
    (configured as a console script entry point in pyproject.toml).
    """
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
    else:
        framework = ADHDFramework()
        framework.run(args)


if __name__ == "__main__":
    main()
