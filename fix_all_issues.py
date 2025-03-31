#!/usr/bin/env python
"""
Master Script to Fix All Issues in AUTOCLICK

This script runs all the individual fix scripts to resolve various issues in the codebase:
1. Merge conflicts
2. BOM (Byte Order Mark) issues
3. Encoding issues
4. Null bytes

Usage:
    python fix_all_issues.py
"""
import os
import sys
import subprocess

def run_script(script_name):
    """Run a Python script and return its exit code."""
    print(f"\nRunning {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors from {script_name}:")
        print(result.stderr)
    return result.returncode

def main():
    """Main function to run all fix scripts."""
    print("\n" + "=" * 80)
    print("AUTOCLICK Master Fix Script".center(80))
    print("=" * 80 + "\n")
    
    # List of fix scripts to run
    fix_scripts = [
        "fix_encoding_issues.py",  # Fix encoding first
        "fix_bom_issues.py",       # Then fix BOM
        "fix_null_bytes.py",       # Then fix null bytes
        "fix_merge_conflicts.py",  # Finally fix merge conflicts
    ]
    
    # Run each fix script
    success_count = 0
    for script in fix_scripts:
        if os.path.exists(script):
            exit_code = run_script(script)
            if exit_code == 0:
                success_count += 1
            else:
                print(f"WARNING: {script} exited with code {exit_code}")
        else:
            print(f"ERROR: Script {script} not found")
    
    print("\n" + "=" * 80)
    print("Summary".center(80))
    print("=" * 80 + "\n")
    
    print(f"Successfully ran {success_count} out of {len(fix_scripts)} fix scripts")
    
    if success_count == len(fix_scripts):
        print("\nAll issues should now be fixed. Try running your application again.")
    else:
        print("\nSome issues may still remain. Check the output above for details.")
    
    return 0 if success_count == len(fix_scripts) else 1

if __name__ == "__main__":
    sys.exit(main())
