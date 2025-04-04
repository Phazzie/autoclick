"""
Tests for service utilities.

This module contains tests for the service utilities.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests service utilities
"""
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict, List, Optional

# Import the module to be tested (will be implemented after tests)
# from src.core.utils.service import BaseService, ServiceRegistry


class TestBaseService(unittest.TestCase):
    """Tests for the BaseService class."""

    def test_init(self):
        """Test that BaseService initializes correctly."""
        # This test will pass once we implement the BaseService
        # with the expected behavior
        try:
            from src.core.utils.service import BaseService

            # Create a service with dependencies
            service = BaseService(
                dependency1="value1",
                dependency2="value2"
            )

            # Verify that the dependencies were stored
            self.assertEqual(service._dependencies, {
                "dependency1": "value1",
                "dependency2": "value2"
            })

            # Verify that the dependencies were set as attributes
            self.assertEqual(service._dependency1, "value1")
            self.assertEqual(service._dependency2, "value2")
        except ImportError:
            self.skipTest("BaseService not implemented yet")

    def test_get_dependency(self):
        """Test that get_dependency returns the correct dependency."""
        # This test will pass once we implement the BaseService
        # with the expected behavior
        try:
            from src.core.utils.service import BaseService

            # Create a service with dependencies
            service = BaseService(
                dependency1="value1",
                dependency2="value2"
            )

            # Verify that get_dependency returns the correct dependency
            self.assertEqual(service.get_dependency("dependency1"), "value1")
            self.assertEqual(service.get_dependency("dependency2"), "value2")

            # Verify that get_dependency returns None for non-existent dependencies
            self.assertIsNone(service.get_dependency("dependency3"))
        except ImportError:
            self.skipTest("BaseService not implemented yet")

    def test_validate_dependencies(self):
        """Test that validate_dependencies raises ValueError for missing dependencies."""
        # This test will pass once we implement the BaseService
        # with the expected behavior
        try:
            from src.core.utils.service import BaseService

            # Create a service with dependencies
            service = BaseService(
                dependency1="value1",
                dependency2="value2"
            )

            # Verify that validate_dependencies does not raise for dependencies that are present
            service.validate_dependencies(["dependency1", "dependency2"])

            # Verify that validate_dependencies raises for dependencies that are missing
            with self.assertRaises(ValueError):
                service.validate_dependencies(["dependency1", "dependency3"])

            with self.assertRaises(ValueError):
                service.validate_dependencies(["dependency3"])
        except ImportError:
            self.skipTest("BaseService not implemented yet")

    def test_logging(self):
        """Test that BaseService initializes the logger correctly."""
        # This test will pass once we implement the BaseService
        # with the expected behavior
        try:
            from src.core.utils.service import BaseService

            # Mock the log_info method
            with patch.object(BaseService, 'log_info') as mock_log_info:
                # Create a service
                service = BaseService()

                # Verify that log_info was called with the initialization message
                mock_log_info.assert_called_once()
                self.assertIn("Initializing", mock_log_info.call_args[0][0])
        except ImportError:
            self.skipTest("BaseService not implemented yet")


class TestServiceRegistry(unittest.TestCase):
    """Tests for the ServiceRegistry class."""

    def test_init(self):
        """Test that ServiceRegistry initializes correctly."""
        # This test will pass once we implement the ServiceRegistry
        # with the expected behavior
        try:
            from src.core.utils.service import ServiceRegistry

            # Create a registry
            registry = ServiceRegistry()

            # Verify that the registry is empty
            self.assertEqual(registry._services, {})
        except ImportError:
            self.skipTest("ServiceRegistry not implemented yet")

    def test_register(self):
        """Test that register adds a service to the registry."""
        # This test will pass once we implement the ServiceRegistry
        # with the expected behavior
        try:
            from src.core.utils.service import ServiceRegistry

            # Create a registry
            registry = ServiceRegistry()

            # Register a service
            service = object()
            registry.register("service1", service)

            # Verify that the service was added to the registry
            self.assertEqual(registry._services, {"service1": service})

            # Register another service
            service2 = object()
            registry.register("service2", service2)

            # Verify that both services are in the registry
            self.assertEqual(registry._services, {
                "service1": service,
                "service2": service2
            })

            # Register a service with an existing name
            service3 = object()
            registry.register("service1", service3)

            # Verify that the service was replaced
            self.assertEqual(registry._services, {
                "service1": service3,
                "service2": service2
            })
        except ImportError:
            self.skipTest("ServiceRegistry not implemented yet")

    def test_get(self):
        """Test that get returns the correct service."""
        # This test will pass once we implement the ServiceRegistry
        # with the expected behavior
        try:
            from src.core.utils.service import ServiceRegistry

            # Create a registry
            registry = ServiceRegistry()

            # Register services
            service1 = object()
            service2 = object()
            registry.register("service1", service1)
            registry.register("service2", service2)

            # Verify that get returns the correct service
            self.assertEqual(registry.get("service1"), service1)
            self.assertEqual(registry.get("service2"), service2)

            # Verify that get returns None for non-existent services
            self.assertIsNone(registry.get("service3"))
        except ImportError:
            self.skipTest("ServiceRegistry not implemented yet")

    def test_get_all(self):
        """Test that get_all returns all services."""
        # This test will pass once we implement the ServiceRegistry
        # with the expected behavior
        try:
            from src.core.utils.service import ServiceRegistry

            # Create a registry
            registry = ServiceRegistry()

            # Register services
            service1 = object()
            service2 = object()
            registry.register("service1", service1)
            registry.register("service2", service2)

            # Verify that get_all returns all services
            self.assertEqual(registry.get_all(), {
                "service1": service1,
                "service2": service2
            })

            # Verify that get_all returns a copy of the services
            services = registry.get_all()
            services["service3"] = object()

            # Verify that the registry was not modified
            self.assertEqual(registry._services, {
                "service1": service1,
                "service2": service2
            })
        except ImportError:
            self.skipTest("ServiceRegistry not implemented yet")


if __name__ == "__main__":
    unittest.main()
