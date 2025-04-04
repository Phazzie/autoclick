"""
Script to verify that all tests pass and code coverage is adequate.

This script runs all tests and generates a coverage report.
"""
import sys
import os
import subprocess
import json
from typing import Dict, Any, List, Tuple

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_tests() -> bool:
    """
    Run all tests.
    
    Returns:
        True if all tests pass, False otherwise
    """
    print("Running tests...")
    result = subprocess.run(
        ["python", "-m", "unittest", "discover", "-s", "tests"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    return result.returncode == 0


def run_coverage() -> Tuple[bool, Dict[str, Any]]:
    """
    Run coverage analysis.
    
    Returns:
        Tuple of (success, coverage_data)
    """
    print("Running coverage analysis...")
    
    # Run coverage
    result = subprocess.run(
        ["coverage", "run", "--source=src", "-m", "unittest", "discover", "-s", "tests"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Coverage run failed: {result.stderr}")
        return False, {}
    
    # Generate coverage report
    result = subprocess.run(
        ["coverage", "json"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Coverage report generation failed: {result.stderr}")
        return False, {}
    
    # Load coverage data
    try:
        with open("coverage.json", "r") as f:
            coverage_data = json.load(f)
        return True, coverage_data
    except Exception as e:
        print(f"Error loading coverage data: {str(e)}")
        return False, {}


def analyze_coverage(coverage_data: Dict[str, Any]) -> bool:
    """
    Analyze coverage data.
    
    Args:
        coverage_data: Coverage data
        
    Returns:
        True if coverage is adequate, False otherwise
    """
    print("Analyzing coverage...")
    
    # Get total coverage
    total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
    print(f"Total coverage: {total_coverage:.2f}%")
    
    # Check if coverage is adequate
    if total_coverage < 80:
        print("Coverage is below 80%, which is not adequate.")
        return False
    
    # Get coverage by file
    files = coverage_data.get("files", {})
    low_coverage_files = []
    
    for file_path, file_data in files.items():
        file_coverage = file_data.get("summary", {}).get("percent_covered", 0)
        if file_coverage < 70:
            low_coverage_files.append((file_path, file_coverage))
    
    if low_coverage_files:
        print("The following files have low coverage:")
        for file_path, file_coverage in low_coverage_files:
            print(f"  {file_path}: {file_coverage:.2f}%")
        return False
    
    print("Coverage is adequate.")
    return True


def verify_tests_and_coverage() -> bool:
    """
    Verify that all tests pass and code coverage is adequate.
    
    Returns:
        True if verification passes, False otherwise
    """
    print("Verifying tests and code coverage...")
    
    # Run tests
    tests_pass = run_tests()
    if not tests_pass:
        print("Tests failed.")
        return False
    
    print("All tests pass.")
    
    # Run coverage analysis
    coverage_success, coverage_data = run_coverage()
    if not coverage_success:
        print("Coverage analysis failed.")
        return False
    
    # Analyze coverage
    coverage_adequate = analyze_coverage(coverage_data)
    if not coverage_adequate:
        print("Coverage is not adequate.")
        return False
    
    print("Verification passed: All tests pass and code coverage is adequate.")
    return True


if __name__ == "__main__":
    success = verify_tests_and_coverage()
    sys.exit(0 if success else 1)
