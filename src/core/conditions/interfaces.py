"""
Interfaces for condition components.

This module defines the interfaces for condition components,
following the Interface Segregation Principle to ensure clients only
depend on the methods they actually use.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Set, TypeVar, Generic, Type

from src.core.context.interfaces import IExecutionContext

# Type variables for generic interfaces
T = TypeVar('T')


class ICondition(ABC):
    """Interface for conditions."""
    
    @property
    @abstractmethod
    def condition_id(self) -> str:
        """Get the condition ID."""
        pass
    
    @property
    @abstractmethod
    def condition_type(self) -> str:
        """Get the condition type."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the condition name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        """Get the condition description."""
        pass
    
    @abstractmethod
    def evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if the condition is met, False otherwise
        """
        pass
    
    @abstractmethod
    def validate(self) -> List[str]:
        """
        Validate the condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        pass


class ICompoundCondition(ICondition):
    """Interface for compound conditions."""
    
    @abstractmethod
    def add_condition(self, condition: ICondition) -> None:
        """
        Add a condition to this compound condition.
        
        Args:
            condition: Condition to add
        """
        pass
    
    @abstractmethod
    def remove_condition(self, condition_id: str) -> None:
        """
        Remove a condition from this compound condition.
        
        Args:
            condition_id: ID of the condition to remove
        """
        pass
    
    @abstractmethod
    def get_conditions(self) -> List[ICondition]:
        """
        Get all conditions in this compound condition.
        
        Returns:
            List of conditions
        """
        pass
    
    @abstractmethod
    def get_condition(self, condition_id: str) -> Optional[ICondition]:
        """
        Get a condition by ID.
        
        Args:
            condition_id: Condition ID
            
        Returns:
            Condition or None if not found
        """
        pass


class IConditionFactory(ABC):
    """Interface for condition factories."""
    
    @abstractmethod
    def create_condition(self, condition_type: str, config: Dict[str, Any]) -> ICondition:
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
        pass
    
    @abstractmethod
    def get_condition_types(self) -> List[str]:
        """
        Get all supported condition types.
        
        Returns:
            List of condition types
        """
        pass
    
    @abstractmethod
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
        pass


class IConditionProvider(ABC):
    """Interface for condition providers."""
    
    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Get the provider ID."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the provider name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get the provider description."""
        pass
    
    @abstractmethod
    def get_condition_types(self) -> List[str]:
        """
        Get all condition types supported by this provider.
        
        Returns:
            List of condition types
        """
        pass
    
    @abstractmethod
    def get_condition_schema(self, condition_type: str) -> Dict[str, Any]:
        """
        Get the schema for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Schema for the condition type
            
        Raises:
            ValueError: If the condition type is not supported by this provider
        """
        pass
    
    @abstractmethod
    def create_condition(self, condition_type: str, config: Dict[str, Any]) -> ICondition:
        """
        Create a condition of the specified type.
        
        Args:
            condition_type: Type of condition to create
            config: Configuration for the condition
            
        Returns:
            Created condition
            
        Raises:
            ValueError: If the condition type is not supported by this provider
        """
        pass


class IConditionRegistry(ABC):
    """Interface for condition registries."""
    
    @abstractmethod
    def register_provider(self, provider: IConditionProvider) -> None:
        """
        Register a condition provider.
        
        Args:
            provider: Condition provider to register
        """
        pass
    
    @abstractmethod
    def unregister_provider(self, provider_id: str) -> None:
        """
        Unregister a condition provider.
        
        Args:
            provider_id: ID of the provider to unregister
        """
        pass
    
    @abstractmethod
    def get_provider(self, provider_id: str) -> Optional[IConditionProvider]:
        """
        Get a provider by ID.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            Provider or None if not found
        """
        pass
    
    @abstractmethod
    def get_providers(self) -> List[IConditionProvider]:
        """
        Get all registered providers.
        
        Returns:
            List of providers
        """
        pass
    
    @abstractmethod
    def get_condition_types(self) -> List[str]:
        """
        Get all condition types from all providers.
        
        Returns:
            List of condition types
        """
        pass
    
    @abstractmethod
    def get_provider_for_condition_type(self, condition_type: str) -> Optional[IConditionProvider]:
        """
        Get the provider for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Provider or None if not found
        """
        pass


class IConditionResolver(ABC):
    """Interface for condition resolvers."""
    
    @abstractmethod
    def resolve_condition(self, condition_def: Dict[str, Any]) -> ICondition:
        """
        Resolve a condition from a definition.
        
        Args:
            condition_def: Condition definition
            
        Returns:
            Resolved condition
            
        Raises:
            ValueError: If the condition cannot be resolved
        """
        pass
    
    @abstractmethod
    def resolve_compound_condition(self, condition_def: Dict[str, Any]) -> ICompoundCondition:
        """
        Resolve a compound condition from a definition.
        
        Args:
            condition_def: Compound condition definition
            
        Returns:
            Resolved compound condition
            
        Raises:
            ValueError: If the compound condition cannot be resolved
        """
        pass
