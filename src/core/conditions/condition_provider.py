"""
Condition provider implementation.

This module provides a base implementation of the IConditionProvider interface,
for providing condition types.
"""
from typing import Dict, Any, List, Optional, Type, Callable
import inspect

from .interfaces import IConditionProvider, ICondition
from .exceptions import ConditionProviderError, ConditionTypeNotFoundError


class BaseConditionProvider(IConditionProvider):
    """
    Base implementation of a condition provider.
    
    This class provides a base implementation of the IConditionProvider interface,
    for providing condition types.
    """
    
    def __init__(self, provider_id: str, name: str, description: str = ""):
        """
        Initialize a base condition provider.
        
        Args:
            provider_id: Provider ID
            name: Provider name
            description: Provider description
        """
        self._provider_id = provider_id
        self._name = name
        self._description = description
        self._condition_types: Dict[str, Type[ICondition]] = {}
        self._condition_schemas: Dict[str, Dict[str, Any]] = {}
        self._condition_factories: Dict[str, Callable[[Dict[str, Any]], ICondition]] = {}
    
    @property
    def provider_id(self) -> str:
        """Get the provider ID."""
        return self._provider_id
    
    @property
    def name(self) -> str:
        """Get the provider name."""
        return self._name
    
    @property
    def description(self) -> str:
        """Get the provider description."""
        return self._description
    
    def register_condition_type(self, condition_type: str, condition_class: Type[ICondition],
                               schema: Dict[str, Any]) -> None:
        """
        Register a condition type.
        
        Args:
            condition_type: Condition type
            condition_class: Condition class
            schema: Schema for the condition type
        """
        self._condition_types[condition_type] = condition_class
        self._condition_schemas[condition_type] = schema
        self._condition_factories[condition_type] = lambda config: condition_class(config)
    
    def register_condition_factory(self, condition_type: str, factory: Callable[[Dict[str, Any]], ICondition],
                                  schema: Dict[str, Any]) -> None:
        """
        Register a condition factory.
        
        Args:
            condition_type: Condition type
            factory: Factory function for creating conditions of this type
            schema: Schema for the condition type
        """
        self._condition_factories[condition_type] = factory
        self._condition_schemas[condition_type] = schema
    
    def get_condition_types(self) -> List[str]:
        """
        Get all condition types supported by this provider.
        
        Returns:
            List of condition types
        """
        return list(self._condition_factories.keys())
    
    def get_condition_schema(self, condition_type: str) -> Dict[str, Any]:
        """
        Get the schema for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Schema for the condition type
            
        Raises:
            ConditionTypeNotFoundError: If the condition type is not supported by this provider
        """
        if condition_type not in self._condition_schemas:
            raise ConditionTypeNotFoundError(condition_type)
        
        return self._condition_schemas[condition_type]
    
    def create_condition(self, condition_type: str, config: Dict[str, Any]) -> ICondition:
        """
        Create a condition of the specified type.
        
        Args:
            condition_type: Type of condition to create
            config: Configuration for the condition
            
        Returns:
            Created condition
            
        Raises:
            ConditionTypeNotFoundError: If the condition type is not supported by this provider
            ConditionProviderError: If there is an error creating the condition
        """
        if condition_type not in self._condition_factories:
            raise ConditionTypeNotFoundError(condition_type)
        
        try:
            # Create a copy of the config with the condition type
            config_with_type = config.copy()
            config_with_type["condition_type"] = condition_type
            
            # Create the condition
            return self._condition_factories[condition_type](config_with_type)
        except ConditionTypeNotFoundError:
            raise
        except Exception as e:
            raise ConditionProviderError(self._provider_id, f"Error creating condition of type '{condition_type}'", e)
