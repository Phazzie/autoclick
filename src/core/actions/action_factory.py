"""Factory for creating actions"""
import importlib
import inspect
from typing import Dict, Any, Type, Optional, Callable

from src.core.actions.base_action import BaseAction


class ActionFactory:
    """Factory for creating and managing actions"""

    _instance: Optional['ActionFactory'] = None
    _registry: Dict[str, Type[BaseAction]] = {}

    def __new__(cls) -> 'ActionFactory':
        """Create a new instance or return the existing one (singleton pattern)"""
        if cls._instance is None:
            cls._instance = super(ActionFactory, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'ActionFactory':
        """Get the singleton instance of the factory"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_action_type(self, action_type: str, action_class: Type[BaseAction]) -> None:
        """
        Register an action type with its implementation class

        Args:
            action_type: String identifier for the action type
            action_class: Implementation class for the action type

        Raises:
            TypeError: If action_class is not a subclass of BaseAction
        """
        # Validate that the action class inherits from BaseAction
        if not issubclass(action_class, BaseAction):
            raise TypeError(f"Action class must inherit from BaseAction: {action_class.__name__}")

        # Register the action type
        self._registry[action_type] = action_class

    def create_action(self, action_data: Dict[str, Any]) -> BaseAction:
        """
        Create an action instance from the given data

        Args:
            action_data: Dictionary containing action configuration

        Returns:
            Instantiated action

        Raises:
            ValueError: If the action type is unknown
        """
        return self.create_from_dict(action_data)

    def create_from_dict(self, action_data: Dict[str, Any]) -> BaseAction:
        """
        Create an action from a dictionary representation

        Args:
            action_data: Dictionary containing action configuration

        Returns:
            Instantiated action

        Raises:
            ValueError: If the action type is unknown
        """
        action_type = action_data.get("type")
        if not action_type or action_type not in self._registry:
            raise ValueError(f"Unknown action type: {action_type}")

        # Get the action class and create an instance
        action_class = self._registry[action_type]
        return action_class.from_dict(action_data)

    def load_actions_from_module(self, module_name: str) -> None:
        """
        Load and register all action classes from a module

        Args:
            module_name: Name of the module to load actions from
        """
        # Import the module
        module = importlib.import_module(module_name)

        # Get all classes defined in the module
        for name in getattr(module, "__all__", dir(module)):
            item = getattr(module, name, None)

            # Check if the item is a class that inherits from BaseAction
            if (
                inspect.isclass(item)
                and issubclass(item, BaseAction)
                and item is not BaseAction
            ):
                # Register the action type using the type property
                action_instance = item("Temporary instance for type detection")
                action_type = action_instance.type
                self.register_action_type(action_type, item)

    @classmethod
    def reset_registry(cls) -> None:
        """
        Reset the action registry

        This is primarily used for testing to ensure a clean state.
        """
        cls._registry = {}
        cls._instance = None

    @classmethod
    def register(cls, action_type: str) -> Callable[[Type[BaseAction]], Type[BaseAction]]:
        """
        Decorator for registering action classes

        Args:
            action_type: String identifier for the action type

        Returns:
            Decorator function that registers the action class
        """
        def decorator(action_class: Type[BaseAction]) -> Type[BaseAction]:
            # Validate that the action class inherits from BaseAction
            if not issubclass(action_class, BaseAction):
                raise TypeError(f"Action class must inherit from BaseAction: {action_class.__name__}")

            # Register the action type
            factory = cls.get_instance()
            factory.register_action_type(action_type, action_class)
            return action_class

        return decorator
