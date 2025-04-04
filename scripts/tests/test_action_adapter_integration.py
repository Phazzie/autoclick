"""
Test if ActionAdapter correctly integrates with the UI components.

This script tests whether the ActionAdapter correctly integrates with the UI components
using clean architecture.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_action_adapter_integration():
    """Test if ActionAdapter correctly integrates with the UI components."""
    print("Testing if ActionAdapter correctly integrates with the UI components...")
    
    # Step 1: Import the domain service
    try:
        from src.domain.actions.impl.action_service import ActionService
        print("[PASS] Successfully imported ActionService")
    except ImportError as e:
        print(f"[FAIL] Could not import ActionService: {e}")
        print("  This suggests the module path is incorrect or the file doesn't exist.")
        return False
    
    # Step 2: Import the adapter
    try:
        from src.ui.adapters.impl.action_adapter import ActionAdapter
        print("[PASS] Successfully imported ActionAdapter")
    except ImportError as e:
        print(f"[FAIL] Could not import ActionAdapter: {e}")
        print("  This suggests the module path is incorrect or the file doesn't exist.")
        return False
    
    # Step 3: Create the service
    try:
        action_service = ActionService()
        print("[PASS] Successfully created ActionService")
    except Exception as e:
        print(f"[FAIL] Could not create ActionService: {e}")
        print("  This suggests there's an issue with the ActionService constructor.")
        return False
    
    # Step 4: Create the adapter with the service
    try:
        action_adapter = ActionAdapter(action_service=action_service)
        print("[PASS] Successfully created ActionAdapter with ActionService")
    except Exception as e:
        print(f"[FAIL] Could not create ActionAdapter: {e}")
        print("  This suggests there's an issue with the ActionAdapter constructor.")
        return False
    
    # Step 5: Verify the adapter is using the service
    try:
        if hasattr(action_adapter, "_provider") and action_adapter._provider is not None:
            print("[PASS] Adapter has a provider")
        else:
            print("[FAIL] Adapter does not have a provider")
            print("  This suggests there's an issue with the ActionAdapter initialization.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not verify adapter has a provider: {e}")
        print("  This suggests there's an issue with the ActionAdapter initialization.")
        return False
    
    # Step 6: Test a basic operation
    try:
        action_types = action_adapter.get_action_types()
        print(f"[PASS] Successfully got action types: {len(action_types)} types")
    except Exception as e:
        print(f"[FAIL] Could not get action types: {e}")
        print(f"  Error details: {str(e)}")
        return False
    
    print("[PASS] SUCCESS: ActionAdapter correctly integrates with the UI components")
    return True

if __name__ == "__main__":
    success = test_action_adapter_integration()
    sys.exit(0 if success else 1)
