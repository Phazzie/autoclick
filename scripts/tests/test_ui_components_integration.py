"""
Test if UI components correctly access the refactored adapters.

This script tests whether the UI components correctly access the refactored adapters.
"""
import sys
import os
import inspect

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_credential_presenter():
    """Test if CredentialPresenter correctly accesses the CredentialAdapter."""
    print("Testing if CredentialPresenter correctly accesses the CredentialAdapter...")

    # Step 1: Import the presenter
    try:
        from src.ui.presenters.credential_presenter import CredentialPresenter
        print("[PASS] Successfully imported CredentialPresenter")
    except ImportError as e:
        print(f"[FAIL] Could not import CredentialPresenter: {e}")
        print("  This suggests the module path is incorrect or the file doesn't exist.")
        return False

    # Step 2: Check if the presenter has a service attribute
    try:
        if hasattr(CredentialPresenter, "service"):
            print("[PASS] CredentialPresenter has a service attribute")
        else:
            print("[FAIL] CredentialPresenter does not have a service attribute")
            print("  This suggests the presenter is not designed to use an adapter.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not check if CredentialPresenter has a service attribute: {e}")
        return False

    # Step 3: Check if the presenter's constructor accepts a service parameter
    try:
        signature = inspect.signature(CredentialPresenter.__init__)
        if "service" in signature.parameters:
            print("[PASS] CredentialPresenter.__init__ accepts a service parameter")
        else:
            print("[FAIL] CredentialPresenter.__init__ does not accept a service parameter")
            print("  This suggests the presenter is not designed to use an adapter.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not check CredentialPresenter.__init__ signature: {e}")
        return False

    print("[PASS] SUCCESS: CredentialPresenter correctly accesses the CredentialAdapter")
    return True

def test_action_execution_presenter():
    """Test if ActionExecutionPresenter correctly accesses the ActionAdapter."""
    print("\nTesting if ActionExecutionPresenter correctly accesses the ActionAdapter...")

    # Step 1: Import the presenter
    try:
        from src.ui.presenters.action_execution_presenter import ActionExecutionPresenter
        print("[PASS] Successfully imported ActionExecutionPresenter")
    except ImportError as e:
        print(f"[FAIL] Could not import ActionExecutionPresenter: {e}")
        print("  This suggests the module path is incorrect or the file doesn't exist.")
        return False

    # Step 2: Check if the presenter has a service attribute
    try:
        if hasattr(ActionExecutionPresenter, "service"):
            print("[PASS] ActionExecutionPresenter has a service attribute")
        else:
            print("[FAIL] ActionExecutionPresenter does not have a service attribute")
            print("  This suggests the presenter is not designed to use an adapter.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not check if ActionExecutionPresenter has a service attribute: {e}")
        return False

    # Step 3: Check if the presenter's constructor accepts a service parameter
    try:
        signature = inspect.signature(ActionExecutionPresenter.__init__)
        if "service" in signature.parameters:
            print("[PASS] ActionExecutionPresenter.__init__ accepts a service parameter")
        else:
            print("[FAIL] ActionExecutionPresenter.__init__ does not accept a service parameter")
            print("  This suggests the presenter is not designed to use an adapter.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not check ActionExecutionPresenter.__init__ signature: {e}")
        return False

    print("[PASS] SUCCESS: ActionExecutionPresenter correctly accesses the ActionAdapter")
    return True

def test_workflow_presenter():
    """Test if WorkflowPresenter correctly accesses the WorkflowAdapter."""
    print("\nTesting if WorkflowPresenter correctly accesses the WorkflowAdapter...")

    # Step 1: Import the presenter
    try:
        from src.ui.presenters.workflow_presenter import WorkflowPresenter
        print("[PASS] Successfully imported WorkflowPresenter")
    except ImportError as e:
        print(f"[FAIL] Could not import WorkflowPresenter: {e}")
        print("  This suggests the module path is incorrect or the file doesn't exist.")
        return False

    # Step 2: Check if the presenter has a service attribute
    try:
        if hasattr(WorkflowPresenter, "service"):
            print("[PASS] WorkflowPresenter has a service attribute")
        else:
            print("[FAIL] WorkflowPresenter does not have a service attribute")
            print("  This suggests the presenter is not designed to use an adapter.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not check if WorkflowPresenter has a service attribute: {e}")
        return False

    # Step 3: Check if the presenter's constructor accepts a service parameter
    try:
        signature = inspect.signature(WorkflowPresenter.__init__)
        if "service" in signature.parameters:
            print("[PASS] WorkflowPresenter.__init__ accepts a service parameter")
        else:
            print("[FAIL] WorkflowPresenter.__init__ does not accept a service parameter")
            print("  This suggests the presenter is not designed to use an adapter.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not check WorkflowPresenter.__init__ signature: {e}")
        return False

    print("[PASS] SUCCESS: WorkflowPresenter correctly accesses the WorkflowAdapter")
    return True

def main():
    """Run all tests."""
    credential_result = test_credential_presenter()
    action_result = test_action_execution_presenter()
    workflow_result = test_workflow_presenter()

    # Print summary
    print("\nSUMMARY:")
    print(f"CredentialPresenter: {'PASS' if credential_result else 'FAIL'}")
    print(f"ActionExecutionPresenter: {'PASS' if action_result else 'FAIL'}")
    print(f"WorkflowPresenter: {'PASS' if workflow_result else 'FAIL'}")

    # Overall result
    overall_result = credential_result and action_result and workflow_result
    if overall_result:
        print("\n[PASS] SUCCESS: All UI components correctly access the refactored adapters")
    else:
        print("\n[FAIL] Some UI components do not correctly access the refactored adapters")

    return overall_result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
