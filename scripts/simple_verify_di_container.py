"""
Simple script to verify dependency injection container.

This script focuses on one thing: verifying that the dependency injection container
correctly works without circular imports.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    """Main function to verify dependency injection container."""
    print("Verifying dependency injection container...")
    
    # Step 1: Import the container module
    print("\nStep 1: Import the container module")
    try:
        import src.infrastructure.di.container
        print("✓ Successfully imported container module")
    except ImportError as e:
        print(f"✗ Failed to import container module: {e}")
        return False
    
    # Step 2: Import the Container class
    print("\nStep 2: Import the Container class")
    try:
        from src.infrastructure.di.container import Container
        print("✓ Successfully imported Container class")
    except ImportError as e:
        print(f"✗ Failed to import Container class: {e}")
        return False
    
    # Step 3: Create a container
    print("\nStep 3: Create a container")
    try:
        container = Container()
        print("✓ Successfully created Container")
    except Exception as e:
        print(f"✗ Failed to create Container: {e}")
        return False
    
    # Step 4: Test basic container operations
    print("\nStep 4: Test basic container operations")
    try:
        # Create a test service
        class TestService:
            pass
        
        # Register the service
        container.register(TestService, TestService())
        print("✓ Successfully registered a service")
        
        # Resolve the service
        resolved = container.resolve(TestService)
        if resolved is not None:
            print("✓ Successfully resolved a service")
        else:
            print("✗ Failed to resolve a service")
            return False
    except Exception as e:
        print(f"✗ Failed to test container operations: {e}")
        return False
    
    # Step 5: Try to import the config module
    print("\nStep 5: Try to import the config module")
    try:
        import src.infrastructure.di.config
        print("✓ Successfully imported config module")
    except ImportError as e:
        print(f"✗ Failed to import config module: {e}")
        print(f"Error details: {str(e)}")
        return False
    
    # Step 6: Try to import the configure_container function
    print("\nStep 6: Try to import the configure_container function")
    try:
        # Try different possible locations
        locations = [
            "src.infrastructure.di.config",
            "src.infrastructure.di"
        ]
        
        configure_container = None
        for location in locations:
            try:
                module = __import__(location, fromlist=["configure_container"])
                if hasattr(module, "configure_container"):
                    configure_container = getattr(module, "configure_container")
                    print(f"✓ Successfully imported configure_container from {location}")
                    break
            except ImportError:
                continue
        
        if configure_container is None:
            print("✗ Could not import configure_container from any expected location")
            return False
    except Exception as e:
        print(f"✗ Failed to import configure_container: {e}")
        return False
    
    # Success!
    print("\nSuccess! Dependency injection container works correctly without circular imports.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
