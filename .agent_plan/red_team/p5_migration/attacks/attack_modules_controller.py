"""
HyperRed Attack Script: modules_controller_core

Attack vectors:
1. Symlinked module folders
2. Module with missing pyproject.toml (but has __init__.py)
3. Malformed TOML (syntax errors)
4. Module without [tool.adhd] section
5. Empty module folder (no __init__.py)
6. Unicode in module names
7. Very long module names
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

from cores.modules_controller_core import ModulesController, ModuleInfo
from cores.modules_controller_core.modules_controller import ModulesReport

def setup_test_workspace() -> Path:
    """Create a temporary workspace with edge case modules."""
    tmp = Path(tempfile.mkdtemp(prefix="hyperred_"))
    
    # Create standard folder structure
    (tmp / "managers").mkdir()
    (tmp / "cores").mkdir()
    (tmp / "utils").mkdir()
    (tmp / "plugins").mkdir()
    (tmp / "mcps").mkdir()
    
    return tmp

def cleanup_test_workspace(tmp: Path) -> None:
    """Clean up the temporary workspace."""
    shutil.rmtree(tmp, ignore_errors=True)

def create_valid_module(tmp: Path, folder: str, name: str) -> Path:
    """Create a valid module for comparison."""
    module_path = tmp / folder / name
    module_path.mkdir(parents=True, exist_ok=True)
    
    # Create pyproject.toml with [tool.adhd]
    pyproject = module_path / "pyproject.toml"
    pyproject.write_text(f'''[project]
name = "{name}"
version = "1.0.0"

[tool.adhd]
layer = "foundation"
''')
    
    # Create __init__.py
    init_file = module_path / "__init__.py"
    init_file.write_text("")
    
    return module_path


def attack_missing_pyproject():
    """Attack: Directory exists but no pyproject.toml"""
    print("\n=== ATTACK: Missing pyproject.toml ===")
    tmp = setup_test_workspace()
    try:
        # Create a folder without pyproject.toml
        module_path = tmp / "managers" / "orphan_module"
        module_path.mkdir(parents=True)
        (module_path / "__init__.py").write_text("")
        
        controller = ModulesController(root_path=tmp)
        report = controller.scan_all_modules()
        
        # Should NOT discover this as a module
        found_orphan = any(m.name == "orphan_module" for m in report.modules)
        if found_orphan:
            print("FAIL: Orphan module without pyproject.toml was discovered!")
            return "FAIL"
        else:
            print("PASS: Orphan module correctly ignored")
            return "PASS"
    finally:
        cleanup_test_workspace(tmp)


def attack_malformed_toml():
    """Attack: pyproject.toml with syntax errors"""
    print("\n=== ATTACK: Malformed TOML ===")
    tmp = setup_test_workspace()
    try:
        module_path = tmp / "managers" / "bad_toml"
        module_path.mkdir(parents=True)
        
        # Write malformed TOML
        pyproject = module_path / "pyproject.toml"
        pyproject.write_text('''
[project
name = "bad_toml"
version = "1.0.0"
# Missing closing bracket!
''')
        
        controller = ModulesController(root_path=tmp)
        try:
            report = controller.scan_all_modules()
            # Should handle gracefully - either skip or log warning
            found_bad = [m for m in report.modules if m.name == "bad_toml"]
            if found_bad:
                print(f"Module found with issues: {found_bad[0].issues}")
                return "PASS" if found_bad[0].issues else "WARNING"
            else:
                print("PASS: Malformed TOML module skipped gracefully")
                return "PASS"
        except Exception as e:
            print(f"FAIL: Unhandled exception: {type(e).__name__}: {e}")
            return "FAIL"
    finally:
        cleanup_test_workspace(tmp)


def attack_missing_tool_adhd():
    """Attack: pyproject.toml without [tool.adhd] section"""
    print("\n=== ATTACK: Missing [tool.adhd] Section ===")
    tmp = setup_test_workspace()
    try:
        module_path = tmp / "managers" / "no_adhd_section"
        module_path.mkdir(parents=True)
        
        # Write valid TOML but without [tool.adhd]
        pyproject = module_path / "pyproject.toml"
        pyproject.write_text('''[project]
name = "no_adhd_section"
version = "1.0.0"

[tool.black]
line-length = 100
''')
        
        controller = ModulesController(root_path=tmp)
        try:
            report = controller.scan_all_modules()
            found = [m for m in report.modules if m.name == "no_adhd_section"]
            if found:
                print(f"Module found with issues: {found[0].issues}")
                # Should have issues flagged
                return "WARNING" if found[0].issues else "FAIL"
            else:
                print("PASS: Module without [tool.adhd] skipped")
                return "PASS"
        except Exception as e:
            print(f"FAIL: Unhandled exception: {type(e).__name__}: {e}")
            return "FAIL"
    finally:
        cleanup_test_workspace(tmp)


def attack_symlinked_module():
    """Attack: Symlinked module folder"""
    print("\n=== ATTACK: Symlinked Module Folder ===")
    tmp = setup_test_workspace()
    try:
        # Create a real module
        real_module = create_valid_module(tmp, "managers", "real_module")
        
        # Create symlink to it
        symlink_path = tmp / "managers" / "symlink_module"
        try:
            os.symlink(real_module, symlink_path)
        except OSError as e:
            print(f"SKIP: Cannot create symlink: {e}")
            return "SKIP"
        
        controller = ModulesController(root_path=tmp)
        report = controller.scan_all_modules()
        
        # Count how many times the module appears
        module_names = [m.name for m in report.modules]
        print(f"Discovered modules: {module_names}")
        
        # Both should be discovered as separate modules
        if "real_module" in module_names and "symlink_module" in module_names:
            print("INFO: Both real and symlinked module discovered")
            return "INFO"
        elif "symlink_module" not in module_names:
            print("INFO: Symlinked module not discovered (may be intentional)")
            return "INFO"
        else:
            print("PASS: Symlinks handled")
            return "PASS"
    finally:
        cleanup_test_workspace(tmp)


def attack_empty_module():
    """Attack: Module folder with pyproject.toml but no __init__.py"""
    print("\n=== ATTACK: Empty Module (no __init__.py) ===")
    tmp = setup_test_workspace()
    try:
        module_path = tmp / "managers" / "empty_module"
        module_path.mkdir(parents=True)
        
        # Create pyproject.toml but NO __init__.py
        pyproject = module_path / "pyproject.toml"
        pyproject.write_text('''[project]
name = "empty_module"
version = "1.0.0"

[tool.adhd]
layer = "foundation"
''')
        
        controller = ModulesController(root_path=tmp)
        report = controller.scan_all_modules()
        
        found = [m for m in report.modules if m.name == "empty_module"]
        if found:
            print(f"Module found: {found[0].name}, has_initializer={found[0].has_initializer()}")
            # Check if has_initializer() correctly returns False
            if not found[0].has_initializer():
                print("PASS: Module discovered, has_initializer() correctly returns False")
                return "PASS"
            else:
                print("FAIL: has_initializer() returned True for missing __init__.py")
                return "FAIL"
        else:
            print("INFO: Module without __init__.py not discovered")
            return "INFO"
    finally:
        cleanup_test_workspace(tmp)


def attack_unicode_module_name():
    """Attack: Module with unicode characters in name"""
    print("\n=== ATTACK: Unicode Module Name ===")
    tmp = setup_test_workspace()
    try:
        # Try various unicode names
        unicode_names = ["café_module", "模块_manager", "emoji_🎉_mod"]
        
        results = []
        for name in unicode_names:
            try:
                module_path = tmp / "managers" / name
                module_path.mkdir(parents=True, exist_ok=True)
                
                pyproject = module_path / "pyproject.toml"
                pyproject.write_text(f'''[project]
name = "{name}"
version = "1.0.0"

[tool.adhd]
layer = "foundation"
''')
                results.append((name, "created"))
            except Exception as e:
                results.append((name, f"error: {e}"))
        
        controller = ModulesController(root_path=tmp)
        report = controller.scan_all_modules()
        
        for name, status in results:
            if status == "created":
                found = any(m.name == name for m in report.modules)
                print(f"  {name}: {'discovered' if found else 'NOT discovered'}")
        
        print("INFO: Unicode handling varies by filesystem")
        return "INFO"
    finally:
        cleanup_test_workspace(tmp)


def attack_very_long_path():
    """Attack: Very long module path"""
    print("\n=== ATTACK: Very Long Module Name ===")
    tmp = setup_test_workspace()
    try:
        # Create a very long module name (filesystem limit is usually 255 chars)
        long_name = "a" * 200  # Very long but under most filesystem limits
        
        try:
            module_path = tmp / "managers" / long_name
            module_path.mkdir(parents=True)
            
            pyproject = module_path / "pyproject.toml"
            pyproject.write_text(f'''[project]
name = "{long_name}"
version = "1.0.0"

[tool.adhd]
layer = "foundation"
''')
            
            controller = ModulesController(root_path=tmp)
            report = controller.scan_all_modules()
            
            found = any(m.name == long_name for m in report.modules)
            if found:
                print(f"PASS: Long module name ({len(long_name)} chars) discovered")
                return "PASS"
            else:
                print(f"WARNING: Long module name not discovered")
                return "WARNING"
        except OSError as e:
            print(f"SKIP: Filesystem doesn't support long name: {e}")
            return "SKIP"
    finally:
        cleanup_test_workspace(tmp)


def attack_hidden_folder():
    """Attack: Module starting with . (hidden folder)"""
    print("\n=== ATTACK: Hidden Folder Module ===")
    tmp = setup_test_workspace()
    try:
        module_path = tmp / "managers" / ".hidden_module"
        module_path.mkdir(parents=True)
        
        pyproject = module_path / "pyproject.toml"
        pyproject.write_text('''[project]
name = ".hidden_module"
version = "1.0.0"

[tool.adhd]
layer = "foundation"
''')
        
        controller = ModulesController(root_path=tmp)
        report = controller.scan_all_modules()
        
        found = any(m.name == ".hidden_module" for m in report.modules)
        if found:
            print("WARNING: Hidden folder module was discovered (may expose internal files)")
            return "WARNING"
        else:
            print("PASS: Hidden folder correctly ignored")
            return "PASS"
    finally:
        cleanup_test_workspace(tmp)


def attack_dunder_folder():
    """Attack: Module starting with __ (dunder folder)"""
    print("\n=== ATTACK: Dunder Folder Module ===")
    tmp = setup_test_workspace()
    try:
        module_path = tmp / "managers" / "__special__"
        module_path.mkdir(parents=True)
        
        pyproject = module_path / "pyproject.toml"
        pyproject.write_text('''[project]
name = "__special__"
version = "1.0.0"

[tool.adhd]
layer = "foundation"
''')
        
        controller = ModulesController(root_path=tmp)
        report = controller.scan_all_modules()
        
        found = any(m.name == "__special__" for m in report.modules)
        if found:
            print("WARNING: Dunder folder module was discovered")
            return "WARNING"
        else:
            print("PASS: Dunder folder correctly ignored")
            return "PASS"
    finally:
        cleanup_test_workspace(tmp)


def attack_duplicate_module_name():
    """Attack: Same module name in different folders"""
    print("\n=== ATTACK: Duplicate Module Name ===")
    tmp = setup_test_workspace()
    try:
        # Create same-named module in different folders
        create_valid_module(tmp, "managers", "shared_name")
        create_valid_module(tmp, "utils", "shared_name")
        
        controller = ModulesController(root_path=tmp)
        report = controller.scan_all_modules()
        
        # Count occurrences
        matches = [m for m in report.modules if m.name == "shared_name"]
        print(f"Found {len(matches)} modules named 'shared_name'")
        for m in matches:
            print(f"  - {m.folder}/{m.name}")
        
        if len(matches) == 2:
            print("INFO: Both modules discovered (namespace collision possible)")
            return "INFO"
        elif len(matches) == 1:
            print("WARNING: Only one of the duplicate modules discovered")
            return "WARNING"
        else:
            print("FAIL: No duplicate modules found")
            return "FAIL"
    finally:
        cleanup_test_workspace(tmp)


def run_all_attacks():
    """Run all attack vectors."""
    print("=" * 60)
    print("HyperRed Attack Suite: modules_controller_core")
    print("=" * 60)
    
    attacks = [
        ("missing_pyproject", attack_missing_pyproject),
        ("malformed_toml", attack_malformed_toml),
        ("missing_tool_adhd", attack_missing_tool_adhd),
        ("symlinked_module", attack_symlinked_module),
        ("empty_module", attack_empty_module),
        ("unicode_module_name", attack_unicode_module_name),
        ("very_long_path", attack_very_long_path),
        ("hidden_folder", attack_hidden_folder),
        ("dunder_folder", attack_dunder_folder),
        ("duplicate_module_name", attack_duplicate_module_name),
    ]
    
    results = {}
    for name, attack_fn in attacks:
        try:
            result = attack_fn()
            results[name] = result
        except Exception as e:
            print(f"EXCEPTION during {name}: {type(e).__name__}: {e}")
            results[name] = "EXCEPTION"
    
    print("\n" + "=" * 60)
    print("ATTACK SUMMARY: modules_controller_core")
    print("=" * 60)
    for name, result in results.items():
        print(f"  {name}: {result}")
    
    return results


if __name__ == "__main__":
    run_all_attacks()
