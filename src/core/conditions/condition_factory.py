"""Factory for creating conditions"""
import importlib
import inspect
from typing import Dict, Any, Type, Optional, Callable, Set

from src.core.conditions.condition_interface import ConditionInterface, ConditionFactory
from src.core.conditions.base_condition import BaseCondition


class ConditionFactoryClass:
    """Factory for creating and managing conditions"""

    _instance: Optional['ConditionFactoryClass'] = None
    _registry: Dict[str, Type[BaseCondition]] = {}

    def __new__(cls) -> 'ConditionFactoryClass':
        """Create a new instance or return the existing one (singleton pattern)"""
        if cls._instance is None:
            cls._instance = super(ConditionFactoryClass, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'ConditionFactoryClass':
        """Get the singleton instance of the factory"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_condition_type(self, condition_type: str, condition_class: Type[BaseCondition]) -> None:
        """
        Register a condition type with its implementation class

        Args:
            condition_type: String identifier for the condition type
            condition_class: Implementation class for the condition type

        Raises:
            TypeError: If condition_class is not a subclass of BaseCondition
        """
        # Validate that the condition class inherits from BaseCondition
        if not issubclass(condition_class, BaseCondition):
            raise TypeError(f"Condition class must inherit from BaseCondition: {condition_class.__name__}")

        # Register the condition type
        self._registry[condition_type] = condition_class

    def get_registered_condition_types(self) -> list[str]:
        """
        Get a list of all registered condition types

        Returns:
            List of condition type identifiers
        """
        return list(self._registry.keys())

    # Dictionary to store conditions by ID
    _condition_store: Dict[str, BaseCondition] = {}

    def get_condition_by_id(self, condition_id: str) -> Optional[BaseCondition]:
        """
        Get a condition by its ID

        Args:
            condition_id: ID of the condition to get

        Returns:
            The condition instance, or None if not found
        """
        # Return the condition from the store if it exists
        return self._condition_store.get(condition_id)

    def store_condition(self, condition: BaseCondition) -> None:
        """
        Store a condition by its ID for later retrieval

        Args:
            condition: The condition to store
        """
        self._condition_store[condition.id] = condition

    def create_condition(self, condition_data: Dict[str, Any]) -> BaseCondition:
        """
        Create a condition instance from the given data

        Args:
            condition_data: Dictionary containing condition configuration

        Returns:
            Instantiated condition

        Raises:
            ValueError: If the condition type is unknown
        """
        condition_type = condition_data.get("type")
        if not condition_type or condition_type not in self._registry:
            raise ValueError(f"Unknown condition type: {condition_type}")

        # Get the condition class and create an instance
        condition_class = self._registry[condition_type]
        condition = condition_class.from_dict(condition_data)

        # Store the condition for later retrieval
        self.store_condition(condition)

        return condition

    def get_available_condition_types(self) -> Set[str]:
        """
        Get all registered condition types

        Returns:
            Set of condition type identifiers
        """
        return set(self._registry.keys())

    def load_conditions_from_module(self, module_name: str) -> None:
        """
        Load and register all condition classes from a module

        Args:
            module_name: Name of the module to load conditions from
        """
        # Import the module
        module = importlib.import_module(module_name)

        # Get all classes defined in the module
        for name in getattr(module, "__all__", dir(module)):
            item = getattr(module, name, None)

            # Check if the item is a class that inherits from BaseCondition
            if (
                inspect.isclass(item)
                and issubclass(item, BaseCondition)
                and item is not BaseCondition
            ):
                # Register the condition type using the type property
                condition_instance = item("Temporary instance for type detection")
                condition_type = condition_instance.type
                self.register_condition_type(condition_type, item)

    @classmethod
    def register(cls, condition_type: str) -> Callable[[Type[BaseCondition]], Type[BaseCondition]]:
        """
        Decorator for registering condition classes

        Args:
            condition_type: String identifier for the condition type

        Returns:
            Decorator function that registers the condition class
        """
        def decorator(condition_class: Type[BaseCondition]) -> Type[BaseCondition]:
            # Validate that the condition class inherits from BaseCondition
            if not issubclass(condition_class, BaseCondition):
                raise TypeError(f"Condition class must inherit from BaseCondition: {condition_class.__name__}")

            # Register the condition type
            factory = cls.get_instance()
            factory.register_condition_type(condition_type, condition_class)
            return condition_class

        return decorator


# Create a singleton instance
ConditionFactory = ConditionFactoryClass.get_instance()

# Register built-in condition types
from src.core.conditions.comparison_condition import ComparisonCondition
from src.core.conditions.element_exists_condition import ElementExistsCondition
from src.core.conditions.text_contains_condition import TextContainsCondition
from src.core.conditions.composite_conditions import AndCondition, OrCondition, NotCondition

ConditionFactory.register_condition_type("comparison", ComparisonCondition)
ConditionFactory.register_condition_type("element_exists", ElementExistsCondition)
ConditionFactory.register_condition_type("text_contains", TextContainsCondition)
ConditionFactory.register_condition_type("and", AndCondition)
ConditionFactory.register_condition_type("or", OrCondition)
ConditionFactory.register_condition_type("not", NotCondition)
