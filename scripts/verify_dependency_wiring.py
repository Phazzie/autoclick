"""
Script to verify the dependency wiring for all adapters.

This script verifies that all adapters are correctly wired with their dependencies
and that the UI components correctly access them.
"""
import sys
import os
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import domain services
from src.domain.credentials.impl.credential_service import CredentialService
from src.domain.actions.impl.action_service import ActionService
# WorkflowService will be imported dynamically

# Import adapters
from src.ui.adapters.impl.credential_adapter import CredentialAdapter
from src.ui.adapters.impl.action_adapter import ActionAdapter
from src.ui.adapters.impl.workflow_adapter import WorkflowAdapter


def verify_credential_adapter():
    """Verify the dependency wiring for the CredentialAdapter."""
    print("\nVerifying dependency wiring for the CredentialAdapter...")

    # Create the credential service
    credential_service = CredentialService()
    print("✓ Created CredentialService")

    # Create the adapter with the service
    credential_adapter = CredentialAdapter(credential_service=credential_service)
    print("✓ Created CredentialAdapter with CredentialService")

    # Verify that the adapter is using the service
    assert credential_adapter._use_service is True, "Adapter is not using the service"
    assert credential_adapter._service is credential_service, "Adapter is not using the correct service"
    print("✓ Adapter is correctly using the service")

    # Test some basic operations
    try:
        # Get credential types
        credential_types = credential_adapter.get_credential_types()
        print(f"✓ Got credential types: {len(credential_types)} types")

        # Create a test credential
        test_credential = {
            "username": "testuser",
            "password": "testpassword",
            "type": "username_password"
        }

        # Validate the credential
        validation_errors = credential_adapter.validate_credential("username_password", test_credential)
        if validation_errors:
            print(f"✗ Validation errors: {validation_errors}")
        else:
            print("✓ Credential validation passed")

            # Create the credential
            created_credential = credential_adapter.create_credential("username_password", test_credential)
            print(f"✓ Created credential: {created_credential['id']}")

            # Get all credentials
            all_credentials = credential_adapter.get_all_credentials()
            print(f"✓ Got all credentials: {len(all_credentials)} credentials")

            # Get the credential by ID
            credential_id = created_credential.get("id")
            if credential_id:
                credential = credential_adapter.get_credential(credential_id)
                print(f"✓ Got credential by ID: {credential['id']}")

                # Test the credential
                test_result = credential_adapter.test_credential(credential_id)
                print(f"✓ Tested credential: {test_result['success']}")

                # Delete the credential
                delete_result = credential_adapter.delete_credential(credential_id)
                print(f"✓ Deleted credential: {delete_result}")
            else:
                print("✗ Created credential has no ID")
    except Exception as e:
        print(f"✗ Error during operations: {str(e)}")
        return False

    return True


def verify_action_adapter():
    """Verify the dependency wiring for the ActionAdapter."""
    print("\nVerifying dependency wiring for the ActionAdapter...")

    try:
        # Create the action service
        action_service = ActionService()
        print("✓ Created ActionService")

        # Create the adapter with the service
        action_adapter = ActionAdapter(action_service=action_service)
        print("✓ Created ActionAdapter with ActionService")

        # Verify that the adapter is using the service
        assert hasattr(action_adapter, "_service"), "Adapter does not have _service attribute"
        assert action_adapter._service is action_service, "Adapter is not using the correct service"
        print("✓ Adapter is correctly using the service")

        # Test some basic operations
        # Get action types
        action_types = action_adapter.get_action_types()
        print(f"✓ Got action types: {len(action_types)} types")

        # Get action schema
        if action_types:
            action_type = action_types[0]['id']
            schema = action_adapter.get_action_schema(action_type)
            print(f"✓ Got action schema for {action_type}")

        return True
    except Exception as e:
        print(f"✗ Error during operations: {str(e)}")
        return False


def verify_workflow_adapter():
    """Verify the dependency wiring for the WorkflowAdapter."""
    print("\nVerifying dependency wiring for the WorkflowAdapter...")

    try:
        # Try to import the workflow service
        try:
            from src.domain.workflows.workflow_service import WorkflowService
        except ImportError:
            print("✗ Could not import WorkflowService from domain layer")
            return False

        # Create the workflow service
        workflow_service = WorkflowService()
        print("✓ Created WorkflowService")

        # Create the adapter with the service
        workflow_adapter = WorkflowAdapter(workflow_service=workflow_service)
        print("✓ Created WorkflowAdapter with WorkflowService")

        # Test some basic operations if possible
        if hasattr(workflow_adapter, "get_workflow_types"):
            workflow_types = workflow_adapter.get_workflow_types()
            print(f"✓ Got workflow types: {len(workflow_types) if workflow_types else 0} types")

        return True
    except Exception as e:
        print(f"✗ Error during operations: {str(e)}")
        return False


def verify_dependency_wiring() -> bool:
    """Verify the dependency wiring for all adapters."""
    print("Verifying dependency wiring for all adapters...")

    # Verify each adapter
    credential_result = verify_credential_adapter()
    action_result = verify_action_adapter()
    workflow_result = verify_workflow_adapter()

    # Print summary
    print("\nDependency wiring verification summary:")
    print(f"CredentialAdapter: {'✓' if credential_result else '✗'}")
    print(f"ActionAdapter: {'✓' if action_result else '✗'}")
    print(f"WorkflowAdapter: {'✓' if workflow_result else '✗'}")

    # Overall result
    overall_result = credential_result and action_result and workflow_result
    if overall_result:
        print("\nDependency wiring verification complete. All adapters are correctly wired.")
    else:
        print("\nDependency wiring verification failed. Some adapters are not correctly wired.")

    return overall_result


if __name__ == "__main__":
    verify_dependency_wiring()
