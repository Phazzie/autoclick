"""
Service utilities for the application.

This module provides utilities for services across the application.
Part of the service architecture refactoring to standardize service initialization.

SRP-1: Provides service utilities
"""
from typing import Dict, Any, List, Optional, TypeVar
from .logging import LoggingMixin

T = TypeVar('T')


class BaseService(LoggingMixin):
    """
    Base class for services.

    Part of the service architecture refactoring to standardize
    service initialization and dependency management.

    SRP Analysis: This base class helps services adhere to SRP by
    standardizing initialization and dependency management, allowing
    service implementations to focus on their core responsibilities.
    """

    def __init__(self, **dependencies):
        """
        Initialize the service with dependencies.

        Args:
            **dependencies: Service dependencies
        """
        # Initialize logger
        self.__init_logger__()
        self.log_info(f"Initializing {self.__class__.__name__}")

        # Store dependencies
        self._dependencies = {}
        for name, dependency in dependencies.items():
            self._dependencies[name] = dependency
            setattr(self, f"_{name}", dependency)

    def get_dependency(self, name: str) -> Any:
        """
        Get a dependency by name.

        Args:
            name: Name of the dependency

        Returns:
            The dependency or None if not found
        """
        return self._dependencies.get(name)

    def validate_dependencies(self, required_dependencies: List[str]) -> None:
        """
        Validate that required dependencies are present.

        Args:
            required_dependencies: List of required dependency names

        Raises:
            ValueError: If any required dependencies are missing
        """
        missing_dependencies = [name for name in required_dependencies if name not in self._dependencies]
        if missing_dependencies:
            raise ValueError(f"Missing required dependencies: {', '.join(missing_dependencies)}")


class ServiceRegistry:
    """
    Registry for services.

    This class provides a way to register and retrieve services.
    It helps reduce coupling between components by providing a central
    location for service lookup.

    SRP-1: Manages service registration and retrieval
    """

    def __init__(self):
        """Initialize the service registry."""
        self._services: Dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Register a service.

        Args:
            name: Name of the service
            service: Service instance
        """
        self._services[name] = service

    def get(self, name: str) -> Optional[Any]:
        """
        Get a service by name.

        Args:
            name: Name of the service

        Returns:
            Service instance or None if not found
        """
        return self._services.get(name)

    def get_all(self) -> Dict[str, Any]:
        """
        Get all registered services.

        Returns:
            Dictionary of service name to service instance
        """
        return self._services.copy()
