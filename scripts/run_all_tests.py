"""
Master script to run all test scripts.

This script runs all test scripts in the tests directory and provides a detailed summary.
"""
import os
import subprocess
import sys
import time

def run_test(script_path):
    """Run a test script and return success/failure with details."""
    script_name = os.path.basename(script_path)
    print(f"\n{'='*80}")
    print(f"Running {script_name}...")
    print(f"{'='*80}")

    start_time = time.time()
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    duration = time.time() - start_time

    # Print output
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")

    success = result.returncode == 0
    status = "PASSED" if success else "FAILED"
    print(f"\nTest {status} in {duration:.2f} seconds")

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
    """Run all test scripts and summarize results."""
    test_dir = os.path.join(os.path.dirname(__file__), "tests")
    test_scripts = [
        os.path.join(test_dir, f)
        for f in os.listdir(test_dir)
        if f.startswith("test_") and f.endswith(".py")
    ]

    if not test_scripts:
        print("No test scripts found in the tests directory.")
        return False

    results = []
    for script in sorted(test_scripts):
        result = run_test(script)
        results.append(result)

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"PASSED: {len(passed)}/{len(results)} ({len(passed)/len(results)*100:.1f}%)")
    for r in passed:
        print(f"  + {r['name']} - {r['reason'] or 'Test passed'} ({r['duration']:.2f}s)")

    if failed:
        print(f"\nFAILED: {len(failed)}/{len(results)} ({len(failed)/len(results)*100:.1f}%)")
        for r in failed:
            print(f"  - {r['name']} - {r['reason'] or 'Test failed'} ({r['duration']:.2f}s)")

    # Provide overall assessment
    print("\nOVERALL ASSESSMENT:")
    if not failed:
        print("[PASS] All tests passed! The system is working correctly.")
    else:
        print(f"[FAIL] {len(failed)} tests failed. The following issues need to be fixed:")
        for i, r in enumerate(failed, 1):
            print(f"  {i}. {r['name']}: {r['reason'] or 'Test failed'}")

    return len(failed) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
