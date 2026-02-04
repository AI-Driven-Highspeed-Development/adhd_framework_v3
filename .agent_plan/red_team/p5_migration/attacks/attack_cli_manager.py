"""
HyperRed Attack Script: cli_manager

Attack vectors:
1. Handler module doesn't exist
2. Handler function doesn't exist
3. Malformed commands.json
4. Command with missing required fields
5. Short name conflicts
6. Type conversion errors
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))


def setup_cli_manager_env():
    """Set up environment for CLI manager testing."""
    from managers.cli_manager import CLIManager, ModuleRegistration, Command, CommandArg
    return CLIManager, ModuleRegistration, Command, CommandArg


def attack_nonexistent_handler_module():
    """Attack: Handler points to non-existent module"""
    print("\n=== ATTACK: Non-existent Handler Module ===")
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        
        # Create a temporary CLI manager instance
        # We need to reset singleton for testing
        CLIManager._instance = None
        
        manager = CLIManager()
        
        # Register a command with non-existent handler module
        reg = ModuleRegistration(
            module_name="test_module",
            description="Test module",
            commands=[
                Command(
                    name="test_cmd",
                    help="Test command",
                    handler="nonexistent.module:handler_fn",
                )
            ],
        )
        manager.register_module(reg)
        
        # Try to resolve the handler
        handler = manager.resolve_handler("nonexistent.module:handler_fn")
        
        if handler is None:
            print("PASS: Gracefully returned None for non-existent module")
            return "PASS"
        else:
            print("FAIL: Should not have resolved non-existent module")
            return "FAIL"
    except Exception as e:
        print(f"Result: Exception raised: {type(e).__name__}: {e}")
        # Check if it's a graceful error
        if isinstance(e, (ImportError, ModuleNotFoundError)):
            print("WARNING: ImportError not caught internally")
            return "WARNING"
        else:
            print("FAIL: Unexpected exception")
            return "FAIL"


def attack_nonexistent_handler_function():
    """Attack: Handler module exists but function doesn't"""
    print("\n=== ATTACK: Non-existent Handler Function ===")
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        CLIManager._instance = None
        
        manager = CLIManager()
        
        # Use a real module but non-existent function
        handler = manager.resolve_handler("os.path:nonexistent_function_xyz")
        
        if handler is None:
            print("PASS: Gracefully returned None for non-existent function")
            return "PASS"
        else:
            print("FAIL: Should not have resolved non-existent function")
            return "FAIL"
    except Exception as e:
        print(f"Result: Exception raised: {type(e).__name__}: {e}")
        return "WARNING"


def attack_malformed_handler_string():
    """Attack: Handler string with invalid format"""
    print("\n=== ATTACK: Malformed Handler String ===")
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        CLIManager._instance = None
        
        manager = CLIManager()
        
        # Various malformed handler strings
        malformed = [
            "no_colon",
            ":no_module",
            "module:",
            "",
            "too:many:colons",
        ]
        
        results = []
        for h in malformed:
            try:
                handler = manager.resolve_handler(h)
                results.append((h, "None" if handler is None else "resolved"))
            except Exception as e:
                results.append((h, f"exception: {type(e).__name__}"))
        
        print("Results:")
        for h, r in results:
            print(f"  '{h}': {r}")
        
        # All should either return None or raise ValueError
        all_safe = all(r in ("None", "exception: ValueError") for _, r in results)
        if all_safe:
            print("PASS: All malformed handlers handled safely")
            return "PASS"
        else:
            print("WARNING: Some malformed handlers may not be handled well")
            return "WARNING"
    except Exception as e:
        print(f"FAIL: Unexpected exception: {e}")
        return "FAIL"


def attack_short_name_conflict():
    """Attack: Two modules trying to use same short name"""
    print("\n=== ATTACK: Short Name Conflict ===")
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        CLIManager._instance = None
        
        manager = CLIManager()
        
        # Clear any existing registry
        manager._save_registry({})
        
        # Register first module with short name
        reg1 = ModuleRegistration(
            module_name="first_module",
            short_name="fm",
            description="First module",
            commands=[],
        )
        manager.register_module(reg1)
        
        # Register second module with same short name
        reg2 = ModuleRegistration(
            module_name="second_module",
            short_name="fm",  # Conflict!
            description="Second module",
            commands=[],
        )
        manager.register_module(reg2)
        
        # Check the registry
        registry = manager.get_registry()
        
        first_short = registry.get("first_module", {}).get("short_name")
        second_short = registry.get("second_module", {}).get("short_name")
        
        print(f"First module short_name: {first_short}")
        print(f"Second module short_name: {second_short}")
        
        if first_short == "fm" and second_short is None:
            print("PASS: Conflict resolved by removing second short_name")
            return "PASS"
        elif first_short == second_short == "fm":
            print("WARNING: Duplicate short_name allowed - may cause argparse issues")
            return "WARNING"
        else:
            print("INFO: Conflict handled differently than expected")
            return "INFO"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_invalid_arg_type():
    """Attack: Argument with invalid type"""
    print("\n=== ATTACK: Invalid Argument Type ===")
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        CLIManager._instance = None
        
        manager = CLIManager()
        manager._save_registry({})
        
        # Register command with invalid type
        reg = ModuleRegistration(
            module_name="type_test",
            description="Type test",
            commands=[
                Command(
                    name="test",
                    help="Test",
                    handler="os.path:join",
                    args=[
                        CommandArg(
                            name="--value",
                            help="Value",
                            type="invalid_type",  # Invalid type!
                        ),
                    ],
                )
            ],
        )
        manager.register_module(reg)
        
        # Build parser
        try:
            parser = manager.build_parser()
            print("Parser built successfully (invalid type likely defaults to str)")
            return "PASS"
        except Exception as e:
            print(f"FAIL: Parser build failed: {e}")
            return "FAIL"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_missing_command_fields():
    """Attack: Command with missing required fields"""
    print("\n=== ATTACK: Missing Command Fields ===")
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        CLIManager._instance = None
        
        manager = CLIManager()
        manager._save_registry({})
        
        # Try to register with minimal data via direct JSON manipulation
        bad_registry = {
            "bad_module": {
                "module_name": "bad_module",
                "commands": [
                    {
                        "name": "cmd1",
                        # Missing "help" and "handler"
                    }
                ],
            }
        }
        manager._save_registry(bad_registry)
        
        try:
            parser = manager.build_parser()
            print("Parser built with incomplete command data")
            return "PASS"  # Graceful handling
        except KeyError as e:
            print(f"WARNING: KeyError when building parser: {e}")
            return "WARNING"
        except Exception as e:
            print(f"FAIL: Unexpected error: {type(e).__name__}: {e}")
            return "FAIL"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_corrupt_json():
    """Attack: Corrupted commands.json file"""
    print("\n=== ATTACK: Corrupted JSON Registry ===")
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        CLIManager._instance = None
        
        manager = CLIManager()
        
        # Corrupt the JSON file
        with open(manager._registry_file, "w") as f:
            f.write("{ invalid json content")
        
        # Try to load registry
        registry = manager._load_registry()
        
        if registry == {}:
            print("PASS: Corrupted JSON returns empty dict")
            return "PASS"
        else:
            print(f"WARNING: Corrupted JSON returned: {registry}")
            return "WARNING"
    except Exception as e:
        print(f"Result: Exception: {type(e).__name__}: {e}")
        return "WARNING"


def attack_concurrent_registration():
    """Attack: Simulate concurrent registration (race condition potential)"""
    print("\n=== ATTACK: Concurrent Registration (Simulated) ===")
    import threading
    import time
    
    try:
        CLIManager, ModuleRegistration, Command, CommandArg = setup_cli_manager_env()
        CLIManager._instance = None
        
        manager = CLIManager()
        manager._save_registry({})
        
        errors = []
        
        def register_module(name):
            try:
                reg = ModuleRegistration(
                    module_name=name,
                    description=f"Module {name}",
                    commands=[],
                )
                manager.register_module(reg)
            except Exception as e:
                errors.append((name, e))
        
        # Create threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=register_module, args=(f"module_{i}",))
            threads.append(t)
        
        # Start all at once
        for t in threads:
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        if errors:
            print(f"WARNING: Errors during concurrent registration: {errors}")
            return "WARNING"
        
        registry = manager.get_registry()
        registered_count = len(registry)
        
        if registered_count == 10:
            print(f"PASS: All 10 modules registered (but file corruption possible)")
            return "INFO"  # No true test for file corruption without checking
        else:
            print(f"WARNING: Only {registered_count}/10 modules registered (race condition?)")
            return "WARNING"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def run_all_attacks():
    """Run all attack vectors."""
    print("=" * 60)
    print("HyperRed Attack Suite: cli_manager")
    print("=" * 60)
    
    attacks = [
        ("nonexistent_handler_module", attack_nonexistent_handler_module),
        ("nonexistent_handler_function", attack_nonexistent_handler_function),
        ("malformed_handler_string", attack_malformed_handler_string),
        ("short_name_conflict", attack_short_name_conflict),
        ("invalid_arg_type", attack_invalid_arg_type),
        ("missing_command_fields", attack_missing_command_fields),
        ("corrupt_json", attack_corrupt_json),
        ("concurrent_registration", attack_concurrent_registration),
    ]
    
    results = {}
    for name, attack_fn in attacks:
        try:
            result = attack_fn()
            results[name] = result
        except Exception as e:
            print(f"EXCEPTION during {name}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            results[name] = "EXCEPTION"
    
    print("\n" + "=" * 60)
    print("ATTACK SUMMARY: cli_manager")
    print("=" * 60)
    for name, result in results.items():
        print(f"  {name}: {result}")
    
    return results


if __name__ == "__main__":
    run_all_attacks()
