"""
Test if WorkflowValidationError can be imported.

This script tests one thing: whether WorkflowValidationError can be imported from any expected location.
"""
import sys
import os
import importlib

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_workflow_validation_error_import():
    """Test if WorkflowValidationError can be imported."""
    print("Testing if WorkflowValidationError can be imported...")

    # Try different possible locations
    locations = [
        "src.domain.workflows.exceptions",
        "src.domain.workflows.workflow_service",
        "src.core.workflow.workflow_service",
        "src.core.workflow.exceptions"
    ]

    workflow_validation_error = None
    successful_location = None

    for location in locations:
        try:
            module = importlib.import_module(location)
            if hasattr(module, "WorkflowValidationError"):
                workflow_validation_error = getattr(module, "WorkflowValidationError")
                successful_location = location
                print(f"[PASS] Successfully imported WorkflowValidationError from {location}")
                break
        except ImportError as e:
            print(f"  Could not import from {location}: {e}")

    if workflow_validation_error is None:
        print("[FAIL] Could not import WorkflowValidationError from any expected location")
        print("  This suggests the class is missing or in a different location.")

        # Try to find any module with "workflow" and "error" or "exception" in the name
        error_modules = []
        for root, _, files in os.walk("src"):
            for file in files:
                if "workflow" in file.lower() and ("error" in file.lower() or "exception" in file.lower()) and file.endswith(".py"):
                    module_path = os.path.join(root, file).replace("\\", "/").replace("/", ".").replace(".py", "")
                    error_modules.append(module_path)

        if error_modules:
            print("  Possible workflow-related error modules:")
            for module in error_modules:
                print(f"    - {module}")

        return False

    # Verify it's an exception class
    try:
        if issubclass(workflow_validation_error, Exception):
            print("[PASS] WorkflowValidationError is an Exception subclass")
        else:
            print("[FAIL] WorkflowValidationError is not an Exception subclass")
            print("  This suggests it's not properly defined as an exception.")
            return False
    except TypeError as e:
        print(f"[FAIL] Could not check if WorkflowValidationError is an Exception subclass: {e}")
        print("  This suggests it's not a class.")
        return False

    print(f"[PASS] SUCCESS: WorkflowValidationError can be imported from {successful_location}")
    return True

if __name__ == "__main__":
    success = test_workflow_validation_error_import()
    sys.exit(0 if success else 1)
