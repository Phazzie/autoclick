"""
Condition registry implementation.

This module provides an implementation of the IConditionRegistry interface,
for registering and retrieving condition providers.
"""
from typing import Dict, Any, List, Optional

from .interfaces import IConditionRegistry, IConditionProvider
from .exceptions import ConditionRegistryError, ConditionTypeNotFoundError


class ConditionRegistry(IConditionRegistry):
    """
    Implementation of a condition registry.
    
    This class provides an implementation of the IConditionRegistry interface,
    for registering and retrieving condition providers.
    """
    
    def __init__(self):
        """Initialize a condition registry."""
        self._providers: Dict[str, IConditionProvider] = {}
        self._condition_type_providers: Dict[str, IConditionProvider] = {}
    
    def register_provider(self, provider: IConditionProvider) -> None:
        """
        Register a condition provider.
        
        Args:
            provider: Condition provider to register
            
        Raises:
            ConditionRegistryError: If a provider with the same ID is already registered
        """
        if provider.provider_id in self._providers:
            raise ConditionRegistryError(f"Provider '{provider.provider_id}' is already registered")
        
        # Register the provider
        self._providers[provider.provider_id] = provider
        
        # Register condition types
        for condition_type in provider.get_condition_types():
            if condition_type in self._condition_type_providers:
                existing_provider = self._condition_type_providers[condition_type]
                raise ConditionRegistryError(
                    f"Condition type '{condition_type}' is already registered by provider '{existing_provider.provider_id}'"
                )
            
            self._condition_type_providers[condition_type] = provider
    
    def unregister_provider(self, provider_id: str) -> None:
        """
        Unregister a condition provider.
        
        Args:
            provider_id: ID of the provider to unregister
        """
        if provider_id not in self._providers:
            return
        
        # Get the provider
        provider = self._providers[provider_id]
        
        # Unregister condition types
        for condition_type in provider.get_condition_types():
            if condition_type in self._condition_type_providers:
                del self._condition_type_providers[condition_type]
        
        # Unregister the provider
        del self._providers[provider_id]
    
    def get_provider(self, provider_id: str) -> Optional[IConditionProvider]:
        """
        Get a provider by ID.
        
        Args:
            provider_id: Provider ID
            
        Returns:
            Provider or None if not found
        """
        return self._providers.get(provider_id)
    
    def get_providers(self) -> List[IConditionProvider]:
        """
        Get all registered providers.
        
        Returns:
            List of providers
        """
        return list(self._providers.values())
    
    def get_condition_types(self) -> List[str]:
        """
        Get all condition types from all providers.
        
        Returns:
            List of condition types
        """
        return list(self._condition_type_providers.keys())
    
    def get_provider_for_condition_type(self, condition_type: str) -> Optional[IConditionProvider]:
        """
        Get the provider for a condition type.
        
        Args:
            condition_type: Condition type
            
        Returns:
            Provider or None if not found
        """
        return self._condition_type_providers.get(condition_type)
