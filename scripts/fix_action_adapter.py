"""
Script to fix the ActionAdapter issue.

This script examines the ActionAdapter and ActionFactory to identify and fix the issue
with the get_action_types method.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    """Main function to fix the ActionAdapter issue."""
    print("Fixing ActionAdapter issue...")
    
    # Step 1: Examine the ActionAdapter
    print("\nStep 1: Examine the ActionAdapter")
    try:
        from src.ui.adapters.impl.action_adapter import ActionAdapter
        
        # Check if the adapter has a _provider attribute
        if hasattr(ActionAdapter, "_provider"):
            print("✓ ActionAdapter has a _provider attribute")
        else:
            print("✗ ActionAdapter does not have a _provider attribute")
        
        # Check the get_action_types method
        import inspect
        source = inspect.getsource(ActionAdapter.get_action_types)
        print(f"get_action_types method source:\n{source}")
    except Exception as e:
        print(f"✗ Failed to examine ActionAdapter: {e}")
        return False
    
    # Step 2: Examine the ActionFactory
    print("\nStep 2: Examine the ActionFactory")
    try:
        from src.core.actions.action_factory import ActionFactory
        factory = ActionFactory.get_instance()
        
        # Check available methods
        methods = [method for method in dir(factory) if not method.startswith("_") and callable(getattr(factory, method))]
        print(f"Available methods: {methods}")
        
        # Check if there's a method that might return action types
        if "register_action_type" in methods:
            print("✓ ActionFactory has register_action_type method")
            
            # Check if there's a way to get registered action types
            if hasattr(factory, "_registry"):
                print("✓ ActionFactory has _registry attribute")
                registry = getattr(factory, "_registry")
                print(f"Registry type: {type(registry)}")
                if isinstance(registry, dict):
                    print(f"Registry keys: {list(registry.keys())}")
            else:
                print("✗ ActionFactory does not have _registry attribute")
    except Exception as e:
        print(f"✗ Failed to examine ActionFactory: {e}")
        return False
    
    # Step 3: Propose a fix
    print("\nStep 3: Propose a fix")
    print("Based on the examination, here's a proposed fix:")
    print("1. Add a get_action_types method to ActionFactory that returns the keys of the _registry dictionary")
    print("2. Update the ActionAdapter to use this method")
    
    # Step 4: Implement the fix for ActionFactory
    print("\nStep 4: Implement the fix for ActionFactory")
    try:
        from src.core.actions.action_factory import ActionFactory
        
        # Add the get_action_types method to ActionFactory
        def get_action_types(self):
            """
            Get all registered action types.
            
            Returns:
                List of action type names
            """
            return list(self._registry.keys())
        
        # Add the method to the class
        ActionFactory.get_action_types = get_action_types
        
        # Test the method
        factory = ActionFactory.get_instance()
        action_types = factory.get_action_types()
        print(f"✓ Successfully added get_action_types method to ActionFactory")
        print(f"✓ Method returns: {action_types}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to implement fix: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
