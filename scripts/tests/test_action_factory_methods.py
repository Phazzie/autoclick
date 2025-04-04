"""
Test if ActionFactory has the required methods.

This script tests one thing: whether ActionFactory has a get_action_types method.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_action_factory_has_get_action_types():
    """Test if ActionFactory has get_action_types method."""
    print("Testing if ActionFactory has get_action_types method...")

    # Step 1: Import ActionFactory
    try:
        from src.core.actions.action_factory import ActionFactory
        print("[PASS] Successfully imported ActionFactory")
    except ImportError as e:
        print(f"[FAIL] Could not import ActionFactory: {e}")
        print("  This suggests the module path is incorrect or the file doesn't exist.")
        return False

    # Step 2: Get ActionFactory instance
    try:
        factory = ActionFactory.get_instance()
        print("[PASS] Successfully got ActionFactory instance")
    except Exception as e:
        print(f"[FAIL] Could not get ActionFactory instance: {e}")
        print("  This suggests there's an issue with the singleton implementation.")
        return False

    # Step 3: Check if get_action_types method exists
    if hasattr(factory, "get_action_types"):
        print("[PASS] SUCCESS: ActionFactory has get_action_types method")

        # Step 4: Verify the method works as expected
        try:
            action_types = factory.get_action_types()
            if isinstance(action_types, list):
                print(f"[PASS] Method returns a list with {len(action_types)} items")
            else:
                print(f"[FAIL] Method returns {type(action_types)} instead of a list")
                return False
        except Exception as e:
            print(f"[FAIL] Method exists but raises an exception when called: {e}")
            return False

        return True
    else:
        print("[FAIL] ActionFactory does not have get_action_types method")

        # Provide helpful diagnostic information
        available_methods = [m for m in dir(factory) if not m.startswith("_") and callable(getattr(factory, m))]
        print(f"  Available methods: {', '.join(available_methods)}")
        print("  This suggests the method needs to be added to the ActionFactory class.")

        # Check if there's a similar method that might serve the same purpose
        similar_methods = [m for m in available_methods if "type" in m.lower() or "get" in m.lower()]
        if similar_methods:
            print(f"  Similar methods that might serve the same purpose: {', '.join(similar_methods)}")

        return False

if __name__ == "__main__":
    success = test_action_factory_has_get_action_types()
    sys.exit(0 if success else 1)
