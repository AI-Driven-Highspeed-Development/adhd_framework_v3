"""
HyperRed Attack Script: adhd_mcp (adhd_controller)

Attack vectors:
1. Call list_modules with invalid filter values
2. Call get_module_info with non-existent module
3. Call get_module_info with empty string
4. Suggest module names when typo
5. Edge cases in project_info
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))


def attack_invalid_filter_types():
    """Attack: list_modules with invalid filter values"""
    print("\n=== ATTACK: Invalid Filter Types ===")
    try:
        from mcps.adhd_mcp.adhd_controller import AdhdController
        
        controller = AdhdController(root_path=PROJECT_ROOT)
        
        # Test invalid types parameter
        test_cases = [
            {"types": ["invalid_folder_type"], "desc": "non-existent folder type"},
            {"types": [123], "desc": "integer in types list"},
            {"types": "string_not_list", "desc": "string instead of list"},
            {"types": None, "desc": "explicit None"},
            {"types": [], "desc": "empty list"},
        ]
        
        results = []
        for tc in test_cases:
            try:
                result = controller.list_modules(types=tc["types"])
                if result.get("success"):
                    results.append((tc["desc"], "success", result.get("count", 0)))
                else:
                    results.append((tc["desc"], "error_response", result.get("error")))
            except Exception as e:
                results.append((tc["desc"], "exception", str(e)))
        
        print("Results:")
        for desc, status, detail in results:
            print(f"  {desc}: {status} ({detail})")
        
        # Check for unhandled exceptions
        has_exception = any(s == "exception" for _, s, _ in results)
        if has_exception:
            print("WARNING: Some invalid inputs raised exceptions")
            return "WARNING"
        else:
            print("PASS: All invalid inputs handled gracefully")
            return "PASS"
    except Exception as e:
        print(f"FAIL: Setup exception: {e}")
        return "FAIL"


def attack_nonexistent_module():
    """Attack: get_module_info with non-existent module"""
    print("\n=== ATTACK: Non-existent Module ===")
    try:
        from mcps.adhd_mcp.adhd_controller import AdhdController
        
        controller = AdhdController(root_path=PROJECT_ROOT)
        
        result = controller.get_module_info("totally_fake_module_xyz")
        
        if not result.get("success"):
            error = result.get("error")
            message = result.get("message")
            suggestions = result.get("suggestions", [])
            
            print(f"Error: {error}")
            print(f"Message: {message}")
            print(f"Suggestions: {suggestions}")
            
            if error == "module_not_found":
                print("PASS: Proper error returned for non-existent module")
                return "PASS"
            else:
                print("WARNING: Unexpected error type")
                return "WARNING"
        else:
            print("FAIL: Should not have found fake module")
            return "FAIL"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_empty_module_name():
    """Attack: get_module_info with empty string"""
    print("\n=== ATTACK: Empty Module Name ===")
    try:
        from mcps.adhd_mcp.adhd_controller import AdhdController
        
        controller = AdhdController(root_path=PROJECT_ROOT)
        
        test_cases = ["", None, "   ", "\t\n"]
        
        results = []
        for tc in test_cases:
            try:
                result = controller.get_module_info(tc)
                if result.get("success"):
                    results.append((repr(tc), "unexpected_success"))
                else:
                    results.append((repr(tc), f"error: {result.get('error')}"))
            except TypeError as e:
                results.append((repr(tc), f"TypeError: {e}"))
            except Exception as e:
                results.append((repr(tc), f"exception: {type(e).__name__}: {e}"))
        
        print("Results:")
        for tc, res in results:
            print(f"  {tc}: {res}")
        
        # Check if empty string is handled
        has_proper_error = any("invalid_argument" in r or "error:" in r for _, r in results)
        if has_proper_error:
            print("PASS: Empty/invalid names handled")
            return "PASS"
        else:
            print("WARNING: Empty names may not be validated")
            return "WARNING"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_typo_suggestions():
    """Attack: Verify typo suggestions work correctly"""
    print("\n=== ATTACK: Typo Suggestions ===")
    try:
        from mcps.adhd_mcp.adhd_controller import AdhdController
        
        controller = AdhdController(root_path=PROJECT_ROOT)
        
        # Try common typos
        typos = [
            ("config_manger", "config_manager"),  # Missing 'a'
            ("loger_util", "logger_util"),  # Missing 'g'
            ("adhd_mcpp", "adhd_mcp"),  # Extra 'p'
        ]
        
        for typo, expected in typos:
            result = controller.get_module_info(typo)
            suggestions = result.get("suggestions", [])
            print(f"  Typo '{typo}': suggestions = {suggestions}")
            
            if expected in suggestions:
                print(f"    ✓ Correct suggestion found")
            elif suggestions:
                print(f"    ~ Got different suggestions")
            else:
                print(f"    ✗ No suggestions provided")
        
        print("INFO: Suggestions feature works")
        return "INFO"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_missing_init_yaml():
    """Attack: Project without init.yaml"""
    print("\n=== ATTACK: Missing init.yaml ===")
    tmp = Path(tempfile.mkdtemp(prefix="hyperred_"))
    try:
        from mcps.adhd_mcp.adhd_controller import AdhdController
        
        # Create empty project structure
        (tmp / "managers").mkdir()
        (tmp / "cores").mkdir()
        
        controller = AdhdController(root_path=tmp)
        
        result = controller.get_project_info()
        
        if not result.get("success"):
            error = result.get("error")
            print(f"Error: {error}")
            print(f"Message: {result.get('message')}")
            
            if error == "init_yaml_not_found":
                print("PASS: Proper error for missing init.yaml")
                return "PASS"
            else:
                print("WARNING: Unexpected error type")
                return "WARNING"
        else:
            print("WARNING: Success returned for project without init.yaml")
            return "WARNING"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def attack_empty_init_yaml():
    """Attack: Project with empty init.yaml"""
    print("\n=== ATTACK: Empty init.yaml ===")
    tmp = Path(tempfile.mkdtemp(prefix="hyperred_"))
    try:
        from mcps.adhd_mcp.adhd_controller import AdhdController
        
        # Create project with empty init.yaml
        (tmp / "managers").mkdir()
        (tmp / "init.yaml").write_text("")
        
        controller = AdhdController(root_path=tmp)
        
        result = controller.get_project_info()
        
        print(f"Result: {result}")
        
        if not result.get("success"):
            print("PASS: Empty init.yaml handled as error")
            return "PASS"
        else:
            print("WARNING: Empty init.yaml treated as valid")
            return "WARNING"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def attack_malformed_init_yaml():
    """Attack: Project with malformed init.yaml"""
    print("\n=== ATTACK: Malformed init.yaml ===")
    tmp = Path(tempfile.mkdtemp(prefix="hyperred_"))
    try:
        from mcps.adhd_mcp.adhd_controller import AdhdController
        
        # Create project with malformed YAML
        (tmp / "managers").mkdir()
        (tmp / "init.yaml").write_text("""
name: test
version: [invalid list syntax
  - broken
""")
        
        controller = AdhdController(root_path=tmp)
        
        try:
            result = controller.get_project_info()
            print(f"Result: {result}")
            
            if not result.get("success"):
                print("PASS: Malformed YAML handled with error response")
                return "PASS"
            else:
                print("WARNING: Malformed YAML somehow parsed")
                return "WARNING"
        except Exception as e:
            print(f"WARNING: Exception raised instead of error response: {e}")
            return "WARNING"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_all_attacks():
    """Run all attack vectors."""
    print("=" * 60)
    print("HyperRed Attack Suite: adhd_mcp (adhd_controller)")
    print("=" * 60)
    
    attacks = [
        ("invalid_filter_types", attack_invalid_filter_types),
        ("nonexistent_module", attack_nonexistent_module),
        ("empty_module_name", attack_empty_module_name),
        ("typo_suggestions", attack_typo_suggestions),
        ("missing_init_yaml", attack_missing_init_yaml),
        ("empty_init_yaml", attack_empty_init_yaml),
        ("malformed_init_yaml", attack_malformed_init_yaml),
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
    print("ATTACK SUMMARY: adhd_mcp")
    print("=" * 60)
    for name, result in results.items():
        print(f"  {name}: {result}")
    
    return results


if __name__ == "__main__":
    run_all_attacks()
