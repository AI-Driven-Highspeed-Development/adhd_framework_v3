"""
HyperRed Attack Script: adhd refresh command

Attack vectors:
1. Run when `uv` is not in PATH (simulated)
2. Test with --dry-run vs actual execution
3. Run with invalid module name
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))


def attack_uv_not_available():
    """Attack: Run refresh when uv is not available"""
    print("\n=== ATTACK: UV Not Available ===")
    
    # Check if uv is actually available
    result = subprocess.run(["which", "uv"], capture_output=True, text=True)
    if result.returncode != 0:
        print("SKIP: uv is actually not installed, cannot simulate")
        return "SKIP"
    
    # We can't easily test this without modifying PATH and that would
    # affect our test runner. Document as INFO.
    print("INFO: Would require PATH manipulation to test")
    print("      Recommendation: adhd refresh should check for uv availability")
    return "INFO"


def attack_invalid_module_refresh():
    """Attack: Run refresh on non-existent module"""
    print("\n=== ATTACK: Refresh Non-existent Module ===")
    
    try:
        # Run adhd refresh with invalid module
        result = subprocess.run(
            ["uv", "run", "python", "-m", "adhd_framework", "refresh", "--module", "fake_module_xyz"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=30,
        )
        
        print(f"Exit code: {result.returncode}")
        print(f"Stdout: {result.stdout[:500] if result.stdout else '(empty)'}")
        print(f"Stderr: {result.stderr[:500] if result.stderr else '(empty)'}")
        
        if result.returncode != 0:
            print("PASS: Non-existent module rejected")
            return "PASS"
        else:
            print("WARNING: Command succeeded for non-existent module")
            return "WARNING"
    except subprocess.TimeoutExpired:
        print("WARNING: Command timed out")
        return "WARNING"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_refresh_dry_run():
    """Attack: Test dry-run flag behavior"""
    print("\n=== ATTACK: Refresh Dry Run ===")
    
    try:
        # Check if dry-run flag exists and works
        result = subprocess.run(
            ["uv", "run", "python", "-m", "adhd_framework", "refresh", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=30,
        )
        
        print(f"Help output (first 800 chars):")
        print(result.stdout[:800] if result.stdout else "(no stdout)")
        
        has_dry_run = "--dry-run" in result.stdout or "--dry_run" in result.stdout
        print(f"\nDry run flag available: {has_dry_run}")
        
        if has_dry_run:
            print("INFO: Dry run available for safe testing")
            return "INFO"
        else:
            print("INFO: No dry run flag (commands may execute directly)")
            return "INFO"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_refresh_module_with_no_refresh_script():
    """Attack: Run module refresh on module without refresh.py"""
    print("\n=== ATTACK: Refresh Module Without refresh.py ===")
    
    try:
        # Find a module without refresh.py
        from cores.modules_controller_core import ModulesController
        
        controller = ModulesController(root_path=PROJECT_ROOT)
        report = controller.scan_all_modules()
        
        modules_without_refresh = [
            m for m in report.modules if not m.has_refresh_script()
        ]
        
        if not modules_without_refresh:
            print("SKIP: All modules have refresh.py")
            return "SKIP"
        
        target = modules_without_refresh[0]
        print(f"Target module without refresh.py: {target.name} ({target.folder})")
        
        # Try to refresh this module
        result = subprocess.run(
            ["uv", "run", "python", "-m", "adhd_framework", "refresh", "--module", target.name],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=30,
        )
        
        print(f"Exit code: {result.returncode}")
        print(f"Stdout: {result.stdout[:300] if result.stdout else '(empty)'}")
        
        # Should handle gracefully
        print("INFO: Refresh on module without refresh.py tested")
        return "INFO"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def attack_refresh_all_default():
    """Attack: Test default refresh behavior (uv sync)"""
    print("\n=== ATTACK: Default Refresh (uv sync) ===")
    
    try:
        # Run refresh with dry-run if available, otherwise just check help
        result = subprocess.run(
            ["uv", "run", "python", "-m", "adhd_framework", "refresh", "--dry-run"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=60,
        )
        
        print(f"Exit code: {result.returncode}")
        output = result.stdout + result.stderr
        print(f"Combined output (first 500 chars):\n{output[:500]}")
        
        # Check if uv sync is mentioned
        if "uv sync" in output.lower() or "syncing" in output.lower():
            print("INFO: Default refresh runs uv sync")
        else:
            print("INFO: Default refresh behavior tested")
        
        return "INFO"
    except Exception as e:
        print(f"FAIL: Exception: {e}")
        return "FAIL"


def run_all_attacks():
    """Run all attack vectors."""
    print("=" * 60)
    print("HyperRed Attack Suite: adhd refresh")
    print("=" * 60)
    
    attacks = [
        ("uv_not_available", attack_uv_not_available),
        ("invalid_module_refresh", attack_invalid_module_refresh),
        ("refresh_dry_run", attack_refresh_dry_run),
        ("refresh_module_without_script", attack_refresh_module_with_no_refresh_script),
        ("refresh_all_default", attack_refresh_all_default),
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
    print("ATTACK SUMMARY: adhd refresh")
    print("=" * 60)
    for name, result in results.items():
        print(f"  {name}: {result}")
    
    return results


if __name__ == "__main__":
    run_all_attacks()
