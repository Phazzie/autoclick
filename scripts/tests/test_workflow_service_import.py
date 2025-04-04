"""
Test if WorkflowService can be imported.

This script tests one thing: whether WorkflowService can be imported from any expected location.
"""
import sys
import os
import importlib

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_workflow_service_import():
    """Test if WorkflowService can be imported."""
    print("Testing if WorkflowService can be imported...")

    # Try different possible locations
    locations = [
        "src.domain.workflows.impl.workflow_service",
        "src.domain.workflows.workflow_service",
        "src.application.workflows.workflow_service",
        "src.core.workflow.workflow_service"
    ]

    workflow_service = None
    successful_location = None

    for location in locations:
        try:
            module = importlib.import_module(location)
            if hasattr(module, "WorkflowService"):
                workflow_service = getattr(module, "WorkflowService")
                successful_location = location
                print(f"[PASS] Successfully imported WorkflowService from {location}")
                break
        except ImportError as e:
            print(f"  Could not import from {location}: {e}")

    if workflow_service is None:
        print("[FAIL] Could not import WorkflowService from any expected location")
        print("  This suggests the class is missing or in a different location.")

        # Try to find any module with "workflow" in the name
        workflow_modules = []
        for root, _, files in os.walk("src"):
            for file in files:
                if "workflow" in file.lower() and file.endswith(".py"):
                    module_path = os.path.join(root, file).replace("\\", "/").replace("/", ".").replace(".py", "")
                    workflow_modules.append(module_path)

        if workflow_modules:
            print("  Possible workflow-related modules:")
            for module in workflow_modules[:10]:  # Limit to 10 to avoid overwhelming output
                print(f"    - {module}")

        return False

    # Try to create an instance
    try:
        instance = workflow_service()
        print("[PASS] Successfully created WorkflowService instance")
    except Exception as e:
        print(f"[FAIL] Could not create WorkflowService instance: {e}")
        print("  This suggests there's an issue with the WorkflowService constructor.")
        return False

    print(f"[PASS] SUCCESS: WorkflowService can be imported from {successful_location}")
    return True

if __name__ == "__main__":
    success = test_workflow_service_import()
    sys.exit(0 if success else 1)
