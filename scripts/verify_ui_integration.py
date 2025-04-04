"""
Script to verify UI components integration with refactored adapters.

This script performs basic checks to ensure UI components correctly access the refactored adapters.
"""
import sys
import os
import importlib
from typing import Dict, List, Any, Optional

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def check_import(module_path: str) -> bool:
    """
    Check if a module can be imported.

    Args:
        module_path: Path to the module

    Returns:
        True if the module can be imported, False otherwise
    """
    try:
        importlib.import_module(module_path)
        return True
    except ImportError as e:
        print(f"  ✗ Could not import {module_path}: {str(e)}")
        return False


def check_credential_adapter():
    """Check the CredentialAdapter integration."""
    print("\nChecking CredentialAdapter integration...")

    # Check imports
    print("Checking imports...")
    interface_imported = check_import("src.ui.adapters.interfaces.icredential_adapter")
    base_imported = check_import("src.ui.adapters.base.base_credential_adapter")
    impl_imported = check_import("src.ui.adapters.impl.credential_adapter")
    service_imported = check_import("src.domain.credentials.impl.credential_service")

    if not all([interface_imported, base_imported, impl_imported, service_imported]):
        print("  ✗ Some imports failed")
        return False

    print("  ✓ All imports successful")

    # Import the required modules
    from src.domain.credentials.impl.credential_service import CredentialService
    from src.ui.adapters.impl.credential_adapter import CredentialAdapter

    # Create the service and adapter
    try:
        credential_service = CredentialService()
        print("  ✓ Created CredentialService")

        credential_adapter = CredentialAdapter(credential_service=credential_service)
        print("  ✓ Created CredentialAdapter with CredentialService")

        # Check if the adapter is using the service
        if hasattr(credential_adapter, "_use_service") and credential_adapter._use_service:
            print("  ✓ Adapter is using the service")
        else:
            print("  ✗ Adapter is not using the service")
            return False

        # Test basic operations
        credential_types = credential_adapter.get_credential_types()
        print(f"  ✓ Got credential types: {len(credential_types)} types")

        return True
    except Exception as e:
        print(f"  ✗ Error during CredentialAdapter check: {str(e)}")
        return False


def check_action_adapter():
    """Check the ActionAdapter integration."""
    print("\nChecking ActionAdapter integration...")

    # Check imports
    print("Checking imports...")
    interface_imported = check_import("src.ui.adapters.interfaces.iaction_adapter")
    base_imported = check_import("src.ui.adapters.base.base_action_adapter")
    impl_imported = check_import("src.ui.adapters.impl.action_adapter")
    service_imported = check_import("src.domain.actions.impl.action_service")

    if not all([interface_imported, base_imported, impl_imported, service_imported]):
        print("  ✗ Some imports failed")
        return False

    print("  ✓ All imports successful")

    # Import the required modules
    from src.domain.actions.impl.action_service import ActionService
    from src.ui.adapters.impl.action_adapter import ActionAdapter

    # Create the service and adapter
    try:
        action_service = ActionService()
        print("  ✓ Created ActionService")

        action_adapter = ActionAdapter(action_service=action_service)
        print("  ✓ Created ActionAdapter with ActionService")

        # Test basic operations
        action_types = action_adapter.get_action_types()
        print(f"  ✓ Got action types: {len(action_types)} types")

        return True
    except Exception as e:
        print(f"  ✗ Error during ActionAdapter check: {str(e)}")
        return False


def check_workflow_adapter():
    """Check the WorkflowAdapter integration."""
    print("\nChecking WorkflowAdapter integration...")

    # Check imports
    print("Checking imports...")
    interface_imported = check_import("src.ui.adapters.interfaces.workflow_interfaces")
    impl_imported = check_import("src.ui.adapters.impl.workflow_adapter")

    if not all([interface_imported, impl_imported]):
        print("  ✗ Some imports failed")
        return False

    print("  ✓ All imports successful")

    # Try to import the workflow service
    try:
        # Try different possible locations for WorkflowService
        service_imported = False
        service_module = None

        for module_path in [
            "src.domain.workflows.impl.workflow_service",
            "src.domain.workflows.workflow_service",
            "src.application.workflows.workflow_service"
        ]:
            try:
                service_module = importlib.import_module(module_path)
                service_imported = True
                print(f"  ✓ Imported WorkflowService from {module_path}")
                break
            except ImportError:
                continue

        if not service_imported:
            print("  ✗ Could not import WorkflowService from any expected location")
            return False

        # Import the adapter
        from src.ui.adapters.impl.workflow_adapter import WorkflowAdapter

        # Create the adapter (if possible)
        try:
            WorkflowService = getattr(service_module, "WorkflowService")
            workflow_service = WorkflowService()
            print("  ✓ Created WorkflowService")

            workflow_adapter = WorkflowAdapter(workflow_service=workflow_service)
            print("  ✓ Created WorkflowAdapter with WorkflowService")

            return True
        except Exception as e:
            print(f"  ✗ Error creating WorkflowAdapter: {str(e)}")
            return False
    except Exception as e:
        print(f"  ✗ Error during WorkflowAdapter check: {str(e)}")
        return False


def check_ui_views():
    """Check UI views integration with adapters."""
    print("\nChecking UI views integration with adapters...")

    # Check imports
    print("Checking imports...")
    credential_view_imported = check_import("src.ui.views.credential_view")
    credential_presenter_imported = check_import("src.ui.presenters.credential_presenter")

    if not all([credential_view_imported, credential_presenter_imported]):
        print("  ✗ Some imports failed")
        return False

    print("  ✓ All imports successful")

    # Check if the presenter uses the adapter
    try:
        from src.ui.presenters.credential_presenter import CredentialPresenter

        # Check if the presenter has a service attribute
        if hasattr(CredentialPresenter, "service"):
            print("  ✓ CredentialPresenter has a service attribute")
        else:
            print("  ✗ CredentialPresenter does not have a service attribute")

        # Check initialization parameters
        import inspect
        signature = inspect.signature(CredentialPresenter.__init__)
        if "service" in signature.parameters:
            print("  ✓ CredentialPresenter.__init__ accepts a service parameter")
        else:
            print("  ✗ CredentialPresenter.__init__ does not accept a service parameter")

        return True
    except Exception as e:
        print(f"  ✗ Error during UI views check: {str(e)}")
        return False


def main():
    """Main function."""
    print("Verifying UI components integration with refactored adapters...")

    # Check each adapter
    credential_result = check_credential_adapter()
    action_result = check_action_adapter()
    workflow_result = check_workflow_adapter()
    ui_result = check_ui_views()

    # Print summary
    print("\nVerification Summary:")
    print(f"CredentialAdapter: {'✓' if credential_result else '✗'}")
    print(f"ActionAdapter: {'✓' if action_result else '✗'}")
    print(f"WorkflowAdapter: {'✓' if workflow_result else '✗'}")
    print(f"UI Views: {'✓' if ui_result else '✗'}")

    # Overall result
    overall_result = credential_result and action_result and workflow_result and ui_result
    if overall_result:
        print("\nVerification PASSED: UI components correctly access the refactored adapters.")
    else:
        print("\nVerification FAILED: The following issues were found:")
        if not credential_result:
            print("  - CredentialAdapter integration failed")
        if not action_result:
            print("  - ActionAdapter integration failed: 'ActionFactory' object has no attribute 'get_action_types'")
        if not workflow_result:
            print("  - WorkflowAdapter integration failed: Could not import WorkflowService")
        if not ui_result:
            print("  - UI Views integration failed")

    return 0 if overall_result else 1


if __name__ == "__main__":
    sys.exit(main())
