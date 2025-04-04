"""
Test for circular imports in the dependency injection modules.

This script tests one thing: whether there are circular imports in the DI modules.
"""
import sys
import os
import importlib

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_di_circular_import():
    """Test for circular imports in the dependency injection modules."""
    print("Testing for circular imports in the dependency injection modules...")

    # Step 1: Import the container module
    try:
        import src.infrastructure.di.container
        print("[PASS] Successfully imported container module")
    except ImportError as e:
        print(f"[FAIL] Could not import container module: {e}")
        print("  This suggests the module path is incorrect or the file doesn't exist.")
        return False

    # Step 2: Import the Container class
    try:
        from src.infrastructure.di.container import Container
        print("[PASS] Successfully imported Container class")
    except ImportError as e:
        print(f"[FAIL] Could not import Container class: {e}")
        print("  This suggests there's an issue with the Container class definition.")
        return False

    # Step 3: Create a container
    try:
        container = Container()
        print("[PASS] Successfully created Container")
    except Exception as e:
        print(f"[FAIL] Could not create Container: {e}")
        print("  This suggests there's an issue with the Container constructor.")
        return False

    # Step 4: Test basic container operations
    try:
        # Create a test service
        class TestService:
            pass

        # Register the service
        container.register(TestService, TestService())
        print("[PASS] Successfully registered a service")

        # Resolve the service
        resolved = container.resolve(TestService)
        if resolved is not None:
            print("[PASS] Successfully resolved a service")
        else:
            print("[FAIL] Could not resolve a service")
            print("  This suggests there's an issue with the Container's resolve method.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not test container operations: {e}")
        print("  This suggests there's an issue with the Container's register or resolve methods.")
        return False

    # Step 5: Try to import the config module
    try:
        import src.infrastructure.di.config
        print("[PASS] Successfully imported config module")
    except ImportError as e:
        print(f"[FAIL] Could not import config module: {e}")
        print(f"  Error details: {str(e)}")
        print("  This suggests there's an issue with the config module or a circular import.")
        return False

    # Step 6: Try to import the configure_container function
    try:
        # Try different possible locations
        locations = [
            "src.infrastructure.di.config",
            "src.infrastructure.di"
        ]

        configure_container = None
        for location in locations:
            try:
                module = importlib.import_module(location)
                if hasattr(module, "configure_container"):
                    configure_container = getattr(module, "configure_container")
                    print(f"[PASS] Successfully imported configure_container from {location}")
                    break
            except ImportError:
                continue

        if configure_container is None:
            print("[FAIL] Could not import configure_container from any expected location")
            print("  This suggests the function is missing or there's a circular import.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not import configure_container: {e}")
        print("  This suggests there's an issue with the configure_container function or a circular import.")
        return False

    print("[PASS] SUCCESS: No circular imports detected in the dependency injection modules")
    return True

if __name__ == "__main__":
    success = test_di_circular_import()
    sys.exit(0 if success else 1)
