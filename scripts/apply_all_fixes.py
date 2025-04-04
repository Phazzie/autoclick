"""
Master script to apply all fix scripts.

This script applies all fix scripts in the fixes directory and provides a detailed summary.
"""
import os
import subprocess
import sys
import time

def apply_fix(script_path):
    """Apply a fix script and return success/failure with details."""
    script_name = os.path.basename(script_path)
    print(f"\n{'='*80}")
    print(f"Applying {script_name}...")
    print(f"{'='*80}")

    start_time = time.time()
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    duration = time.time() - start_time

    # Print output
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")

    success = result.returncode == 0
    status = "SUCCEEDED" if success else "FAILED"
    print(f"\nFix {status} in {duration:.2f} seconds")

    # Extract reason for failure/success from the last line of output
    lines = result.stdout.strip().split('\n')
    reason = ""
    for line in reversed(lines):
        if line.startswith("[PASS] SUCCESS:") or line.startswith("[FAIL]"):
            reason = line
            break

    return {
        "name": script_name,
        "success": success,
        "duration": duration,
        "reason": reason,
        "output": result.stdout
    }

def main():
    """Apply all fix scripts and summarize results."""
    fix_dir = os.path.join(os.path.dirname(__file__), "fixes")
    fix_scripts = [
        os.path.join(fix_dir, f)
        for f in os.listdir(fix_dir)
        if f.startswith("fix_") and f.endswith(".py")
    ]

    if not fix_scripts:
        print("No fix scripts found in the fixes directory.")
        return False

    results = []
    for script in sorted(fix_scripts):
        result = apply_fix(script)
        results.append(result)

    # Print summary
    print("\n" + "="*80)
    print("FIX SUMMARY")
    print("="*80)

    succeeded = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"SUCCEEDED: {len(succeeded)}/{len(results)} ({len(succeeded)/len(results)*100:.1f}%)")
    for r in succeeded:
        print(f"  + {r['name']} - {r['reason'] or 'Fix succeeded'} ({r['duration']:.2f}s)")

    if failed:
        print(f"\nFAILED: {len(failed)}/{len(results)} ({len(failed)/len(results)*100:.1f}%)")
        for r in failed:
            print(f"  - {r['name']} - {r['reason'] or 'Fix failed'} ({r['duration']:.2f}s)")

    # Provide overall assessment
    print("\nOVERALL ASSESSMENT:")
    if not failed:
        print("[PASS] All fixes succeeded! The system should now be working correctly.")
        print("  Run the tests again to verify.")
    else:
        print(f"[FAIL] {len(failed)} fixes failed. The following issues still need to be addressed:")
        for i, r in enumerate(failed, 1):
            print(f"  {i}. {r['name']}: {r['reason'] or 'Fix failed'}")

    return len(failed) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
