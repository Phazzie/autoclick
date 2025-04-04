"""
Script to verify dependency wiring and configuration.

This script checks the dependency injection configuration to ensure proper wiring.
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


def check_container():
    """Check the dependency injection container."""
    print("\nChecking dependency injection container...")

    # Check imports
    print("Checking imports...")
    container_imported = check_import("src.infrastructure.di.container")
    config_imported = check_import("src.infrastructure.di.config")

    if not all([container_imported, config_imported]):
        print("  ✗ Some imports failed")
        return False

    print("  ✓ All imports successful")

    # Import the container
    try:
        from src.infrastructure.di.container import Container

        # Create a container
        container = Container()
        print("  ✓ Created Container")

        # Check if the container has the expected methods
        if hasattr(container, "register") and hasattr(container, "resolve"):
            print("  ✓ Container has register and resolve methods")
        else:
            print("  ✗ Container is missing expected methods")
            return False

        # Try to register and resolve a simple service
        class TestService:
            pass

        container.register(TestService, TestService())
        resolved = container.resolve(TestService)

        if resolved is not None:
            print("  ✓ Container can register and resolve services")
        else:
            print("  ✗ Container failed to resolve a registered service")
            return False

        return True
    except Exception as e:
        print(f"  ✗ Error during container check: {str(e)}")
        return False


def check_adapter_factory():
    """Check the adapter factory."""
    print("\nChecking adapter factory...")

    # Check imports
    print("Checking imports...")
    factory_imported = check_import("src.ui.adapters.factory.adapter_factory_new")

    if not factory_imported:
        print("  ✗ Factory import failed")
        return False

    print("  ✓ Factory import successful")

    # Import the factory
    try:
        from src.ui.adapters.factory.adapter_factory_new import AdapterFactoryNew

        # Create a factory
        factory = AdapterFactoryNew()
        print("  ✓ Created AdapterFactoryNew")

        # Check if the factory has the expected methods
        expected_methods = [
            "get_workflow_adapter",
            "get_workflow_query_adapter",
            "get_workflow_command_adapter",
            "get_workflow_execution_adapter",
            "get_workflow_validation_adapter",
            "get_workflow_type_adapter"
        ]

        missing_methods = [method for method in expected_methods if not hasattr(factory, method)]

        if not missing_methods:
            print("  ✓ Factory has all expected methods")
        else:
            print(f"  ✗ Factory is missing methods: {', '.join(missing_methods)}")
            return False

        # Check if the factory has a container
        if hasattr(factory, "_container"):
            print("  ✓ Factory has a container")
        else:
            print("  ✗ Factory does not have a container")
            return False

        return True
    except Exception as e:
        print(f"  ✗ Error during factory check: {str(e)}")
        return False


def check_app_initialization():
    """Check the application initialization."""
    print("\nChecking application initialization...")

    # Check imports
    print("Checking imports...")
    app_imported = check_import("app")

    if not app_imported:
        print("  ✗ App import failed")
        return False

    print("  ✓ App import successful")

    # Check if the app initializes the adapters
    try:
        from app import AutoClickApp

        # Check if the app has an _init_services method
        if hasattr(AutoClickApp, "_init_services"):
            print("  ✓ App has _init_services method")
        else:
            print("  ✗ App does not have _init_services method")
            return False

        # Check the method implementation
        import inspect
        source = inspect.getsource(AutoClickApp._init_services)

        # Check for adapter initialization
        adapters = [
            "credential_service",
            "variable_service",
            "workflow_service",
            "error_service",
            "condition_service",
            "loop_service",
            "datasource_service",
            "reporting_service"
        ]

        missing_adapters = [adapter for adapter in adapters if adapter not in source]

        if not missing_adapters:
            print("  ✓ App initializes all expected adapters")
        else:
            print(f"  ✗ App is missing adapter initialization: {', '.join(missing_adapters)}")
            return False

        return True
    except Exception as e:
        print(f"  ✗ Error during app initialization check: {str(e)}")
        return False


def main():
    """Main function."""
    print("Verifying dependency wiring and configuration...")

    # Check each component
    container_result = check_container()
    factory_result = check_adapter_factory()
    app_result = check_app_initialization()

    # Print summary
    print("\nVerification Summary:")
    print(f"Dependency Injection Container: {'✓' if container_result else '✗'}")
    print(f"Adapter Factory: {'✓' if factory_result else '✗'}")
    print(f"Application Initialization: {'✓' if app_result else '✗'}")

    # Overall result
    overall_result = container_result and factory_result and app_result
    if overall_result:
        print("\nVerification PASSED: Dependency wiring and configuration are correct.")
    else:
        print("\nVerification FAILED: The following issues were found:")
        if not container_result:
            print("  - Dependency Injection Container issues: Could not properly register or resolve services")
        if not factory_result:
            print("  - Adapter Factory issues: Missing expected methods or container")
        if not app_result:
            print("  - Application Initialization issues: Missing adapter initialization in _init_services method")

    return 0 if overall_result else 1


if __name__ == "__main__":
    sys.exit(main())
