"""
Condition factory implementation.

This module provides an implementation of the IConditionFactory interface,
for creating conditions.
"""
from typing import Dict, Any, List, Optional

from .interfaces import IConditionFactory, ICondition, IConditionRegistry
from .exceptions import ConditionFactoryError, ConditionTypeNotFoundError
from .condition_resolver import ConditionResolver


class ConditionFactory(IConditionFactory):
    """
    Implementation of a condition factory.
    
    This class provides an implementation of the IConditionFactory interface,
    for creating conditions.
    """
    
    def __init__(self, registry: IConditionRegistry):
        """
        Initialize a condition factory.
        
        Args:
            registry: Condition registry to use for creating conditions
        """
        self._registry = registry
        self._resolver = ConditionResolver(registry)
    
    def create_condition(self, condition_type: str, config: Dict[str, Any]) -> ICondition:
        """
        Create a condition of the specified type.
        
        Args:
            condition_type: Type of condition to create
            config: Configuration for the condition
            
        Returns:
            Created condition
            
        Raises:
            ConditionFactoryError: If the condition cannot be created
        """
        try:
            # Get the provider for the condition type
            provider = self._registry.get_provider_for_condition_type(condition_type)
            if not provider:
                raise ConditionTypeNotFoundError(condition_type)
            
            # Create the condition
            return provider.create_condition(condition_type, config)
        except ConditionTypeNotFoundError as e:
            raise ConditionFactoryError(condition_type, f"Condition type '{e.condition_type}' not found")
        except Exception as e:
            if isinstance(e, ConditionFactoryError):
                raise
            raise ConditionFactoryError(condition_type, f"Error creating condition: {str(e)}", e)
    
    def get_condition_types(self) -> List[str]:
        """
        Get all supported condition types.
        
        Returns:
            List of condition types
        """
        return self._registry.get_condition_types()
    
    def get_condition_schema(self, condition_type: str) -> Dict[str, Any]:
        """
        Get the schema for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Schema for the condition type
            
        Raises:
            ConditionFactoryError: If the condition type is not supported
        """
        try:
            # Get the provider for the condition type
            provider = self._registry.get_provider_for_condition_type(condition_type)
            if not provider:
                raise ConditionTypeNotFoundError(condition_type)
            
            # Get the schema
            return provider.get_condition_schema(condition_type)
        except ConditionTypeNotFoundError as e:
            raise ConditionFactoryError(condition_type, f"Condition type '{e.condition_type}' not found")
        except Exception as e:
            if isinstance(e, ConditionFactoryError):
                raise
            raise ConditionFactoryError(condition_type, f"Error getting condition schema: {str(e)}", e)
    
    def create_condition_from_definition(self, condition_def: Dict[str, Any]) -> ICondition:
        """
        Create a condition from a definition.
        
        Args:
            condition_def: Condition definition
            
        Returns:
            Created condition
            
        Raises:
            ConditionFactoryError: If the condition cannot be created
        """
        try:
            return self._resolver.resolve_condition(condition_def)
        except Exception as e:
            condition_type = condition_def.get("condition_type", "unknown")
            if isinstance(e, ConditionFactoryError):
                raise
            raise ConditionFactoryError(condition_type, f"Error creating condition from definition: {str(e)}", e)
