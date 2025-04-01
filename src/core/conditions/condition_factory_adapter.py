"""
Condition factory adapter.

This module provides an adapter that bridges the old and new condition factory implementations.
"""
from typing import Dict, Any, List, Optional

from .condition_factory import ConditionFactoryClass
from .interfaces import IConditionFactory
from .condition_factory_new import ConditionFactory as NewConditionFactory
from .condition_registry import ConditionRegistry
from .standard_provider import StandardConditionProvider
from .variable_provider import VariableConditionProvider


class ConditionFactoryAdapter(IConditionFactory):
    """
    Adapter for the condition factory.
    
    This class provides an adapter that implements the IConditionFactory interface
    using the new condition factory implementation, while maintaining backward
    compatibility with the original condition factory.
    """
    
    _instance: Optional['ConditionFactoryAdapter'] = None
    
    def __new__(cls) -> 'ConditionFactoryAdapter':
        """Create a new instance or return the existing one (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(ConditionFactoryAdapter, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the adapter."""
        # Create the registry
        registry = ConditionRegistry()
        
        # Register providers
        registry.register_provider(StandardConditionProvider())
        registry.register_provider(VariableConditionProvider())
        
        # Create the factory
        self._new_factory = NewConditionFactory(registry)
        
        # Get the legacy factory
        self._legacy_factory = ConditionFactoryClass.get_instance()
    
    @classmethod
    def get_instance(cls) -> 'ConditionFactoryAdapter':
        """Get the singleton instance of the adapter."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def create_condition(self, condition_type: str, config: Dict[str, Any]) -> Any:
        """
        Create a condition of the specified type.
        
        Args:
            condition_type: Type of condition to create
            config: Configuration for the condition
            
        Returns:
            Created condition
            
        Raises:
            ValueError: If the condition type is not supported
        """
        # Try to create the condition using the new factory first
        try:
            return self._new_factory.create_condition(condition_type, config)
        except Exception:
            # Fall back to the legacy implementation
            return self._legacy_factory.create_condition(condition_type, config)
    
    def get_condition_types(self) -> List[str]:
        """
        Get all supported condition types.
        
        Returns:
            List of condition types
        """
        # Combine legacy and new condition types
        legacy_types = self._legacy_factory.get_registered_condition_types()
        new_types = self._new_factory.get_condition_types()
        
        # Return unique condition types
        return list(set(legacy_types + new_types))
    
    def get_condition_schema(self, condition_type: str) -> Dict[str, Any]:
        """
        Get the schema for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Schema for the condition type
            
        Raises:
            ValueError: If the condition type is not supported
        """
        # Try to get the schema using the new factory first
        try:
            return self._new_factory.get_condition_schema(condition_type)
        except Exception:
            # Fall back to the legacy implementation
            return self._legacy_factory.get_condition_schema(condition_type)
    
    def create_condition_from_definition(self, condition_def: Dict[str, Any]) -> Any:
        """
        Create a condition from a definition.
        
        Args:
            condition_def: Condition definition
            
        Returns:
            Created condition
            
        Raises:
            ValueError: If the condition cannot be created
        """
        # Try to create the condition using the new factory first
        try:
            return self._new_factory.create_condition_from_definition(condition_def)
        except Exception:
            # Fall back to the legacy implementation
            return self._legacy_factory.create_condition_from_dict(condition_def)
