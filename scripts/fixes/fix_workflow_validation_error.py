"""
Fix the WorkflowValidationError import issue.

This script fixes the issue with importing WorkflowValidationError in the workflow_presenter.py file.
"""
import sys
import os
import re

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def fix_workflow_validation_error():
    """Fix the WorkflowValidationError import issue."""
    print("Fixing WorkflowValidationError import issue...")

    # Step 1: Locate the workflow_adapter.py file
    adapter_path = os.path.join("src", "ui", "adapters", "workflow_adapter.py")
    if not os.path.exists(adapter_path):
        print(f"[FAIL] Could not find {adapter_path}")
        return False

    print(f"[PASS] Found {adapter_path}")

    # Step 2: Read the file
    try:
        with open(adapter_path, "r") as f:
            content = f.read()
        print("[PASS] Successfully read the file")
    except Exception as e:
        print(f"[FAIL] Could not read the file: {e}")
        return False

    # Step 3: Find the problematic import
    if "from src.core.workflow.workflow_service import WorkflowService, WorkflowValidationError" in content:
        print("[PASS] Found problematic import")

        # Step 4: Replace the import
        new_content = content.replace(
            "from src.core.workflow.workflow_service import WorkflowService, WorkflowValidationError",
            "from src.core.workflow.workflow_service import WorkflowService\nfrom src.core.workflow.exceptions import WorkflowValidationError"
        )

        # Step 5: Write the file
        try:
            with open(adapter_path, "w") as f:
                f.write(new_content)
            print("[PASS] Successfully updated the file")
        except Exception as e:
            print(f"[FAIL] Could not write the file: {e}")
            return False
    else:
        print("[FAIL] Could not find problematic import")

        # Try to find any import of WorkflowValidationError
        imports = re.findall(r"from\s+.*\s+import\s+.*WorkflowValidationError.*", content)
        if imports:
            print(f"  Found these imports instead: {imports}")
        else:
            print("  No import of WorkflowValidationError found")

        return False

    print("[PASS] SUCCESS: Fixed WorkflowValidationError import issue")
    return True

if __name__ == "__main__":
    success = fix_workflow_validation_error()
    sys.exit(0 if success else 1)
