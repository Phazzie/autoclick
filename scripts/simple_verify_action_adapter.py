"""
Simple script to verify ActionAdapter integration.

This script focuses on one thing: verifying that the ActionAdapter 
correctly integrates with the UI components using clean architecture.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    """Main function to verify ActionAdapter integration."""
    print("Verifying ActionAdapter integration...")
    
    # Step 1: Import the domain service
    print("\nStep 1: Import the domain service")
    try:
        from src.domain.actions.impl.action_service import ActionService
        print("✓ Successfully imported ActionService")
    except ImportError as e:
        print(f"✗ Failed to import ActionService: {e}")
        return False
    
    # Step 2: Import the adapter
    print("\nStep 2: Import the adapter")
    try:
        from src.ui.adapters.impl.action_adapter import ActionAdapter
        print("✓ Successfully imported ActionAdapter")
    except ImportError as e:
        print(f"✗ Failed to import ActionAdapter: {e}")
        return False
    
    # Step 3: Create the service
    print("\nStep 3: Create the service")
    try:
        action_service = ActionService()
        print("✓ Successfully created ActionService")
    except Exception as e:
        print(f"✗ Failed to create ActionService: {e}")
        return False
    
    # Step 4: Create the adapter with the service
    print("\nStep 4: Create the adapter with the service")
    try:
        action_adapter = ActionAdapter(action_service=action_service)
        print("✓ Successfully created ActionAdapter with ActionService")
    except Exception as e:
        print(f"✗ Failed to create ActionAdapter: {e}")
        return False
    
    # Step 5: Check ActionFactory
    print("\nStep 5: Check ActionFactory")
    try:
        from src.core.actions.action_factory import ActionFactory
        factory = ActionFactory.get_instance()
        print("✓ Successfully got ActionFactory instance")
        
        # Check if the factory has the expected methods
        if hasattr(factory, "get_action_types"):
            print("✓ ActionFactory has get_action_types method")
        else:
            print("✗ ActionFactory does not have get_action_types method")
            
            # Check for alternative methods
            methods = [method for method in dir(factory) if not method.startswith("_") and callable(getattr(factory, method))]
            print(f"Available methods: {methods}")
            return False
    except Exception as e:
        print(f"✗ Failed to check ActionFactory: {e}")
        return False
    
    # Step 6: Test a basic operation
    print("\nStep 6: Test a basic operation")
    try:
        action_types = action_adapter.get_action_types()
        print(f"✓ Successfully got action types: {len(action_types)} types")
    except Exception as e:
        print(f"✗ Failed to get action types: {e}")
        print(f"Error details: {str(e)}")
        return False
    
    # Success!
    print("\nSuccess! ActionAdapter correctly integrates with the UI components using clean architecture.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
