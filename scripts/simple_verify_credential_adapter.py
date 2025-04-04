"""
Simple script to verify CredentialAdapter integration.

This script focuses on one thing: verifying that the CredentialAdapter 
correctly integrates with the UI components using clean architecture.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    """Main function to verify CredentialAdapter integration."""
    print("Verifying CredentialAdapter integration...")
    
    # Step 1: Import the domain service
    print("\nStep 1: Import the domain service")
    try:
        from src.domain.credentials.impl.credential_service import CredentialService
        print("✓ Successfully imported CredentialService")
    except ImportError as e:
        print(f"✗ Failed to import CredentialService: {e}")
        return False
    
    # Step 2: Import the adapter
    print("\nStep 2: Import the adapter")
    try:
        from src.ui.adapters.impl.credential_adapter import CredentialAdapter
        print("✓ Successfully imported CredentialAdapter")
    except ImportError as e:
        print(f"✗ Failed to import CredentialAdapter: {e}")
        return False
    
    # Step 3: Create the service
    print("\nStep 3: Create the service")
    try:
        credential_service = CredentialService()
        print("✓ Successfully created CredentialService")
    except Exception as e:
        print(f"✗ Failed to create CredentialService: {e}")
        return False
    
    # Step 4: Create the adapter with the service
    print("\nStep 4: Create the adapter with the service")
    try:
        credential_adapter = CredentialAdapter(credential_service=credential_service)
        print("✓ Successfully created CredentialAdapter with CredentialService")
    except Exception as e:
        print(f"✗ Failed to create CredentialAdapter: {e}")
        return False
    
    # Step 5: Verify the adapter is using the service
    print("\nStep 5: Verify the adapter is using the service")
    try:
        if hasattr(credential_adapter, "_use_service") and credential_adapter._use_service:
            print("✓ Adapter is using the service")
        else:
            print("✗ Adapter is not using the service")
            return False
    except Exception as e:
        print(f"✗ Failed to verify adapter is using service: {e}")
        return False
    
    # Step 6: Test a basic operation
    print("\nStep 6: Test a basic operation")
    try:
        credential_types = credential_adapter.get_credential_types()
        print(f"✓ Successfully got credential types: {len(credential_types)} types")
    except Exception as e:
        print(f"✗ Failed to get credential types: {e}")
        return False
    
    # Step 7: Import the presenter
    print("\nStep 7: Import the presenter")
    try:
        from src.ui.presenters.credential_presenter import CredentialPresenter
        print("✓ Successfully imported CredentialPresenter")
    except ImportError as e:
        print(f"✗ Failed to import CredentialPresenter: {e}")
        return False
    
    # Step 8: Check if the presenter accepts the adapter
    print("\nStep 8: Check if the presenter accepts the adapter")
    try:
        import inspect
        signature = inspect.signature(CredentialPresenter.__init__)
        if "service" in signature.parameters:
            print("✓ CredentialPresenter.__init__ accepts a service parameter")
        else:
            print("✗ CredentialPresenter.__init__ does not accept a service parameter")
            return False
    except Exception as e:
        print(f"✗ Failed to check presenter signature: {e}")
        return False
    
    # Success!
    print("\nSuccess! CredentialAdapter correctly integrates with the UI components using clean architecture.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
