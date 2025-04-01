"""
Condition resolver implementation.

This module provides an implementation of the IConditionResolver interface,
for resolving conditions from definitions.
"""
from typing import Dict, Any, List, Optional

from .interfaces import IConditionResolver, ICondition, ICompoundCondition, IConditionRegistry
from .exceptions import ConditionResolverError, ConditionTypeNotFoundError
from .compound_condition import AndCondition, OrCondition, NotCondition


class ConditionResolver(IConditionResolver):
    """
    Implementation of a condition resolver.
    
    This class provides an implementation of the IConditionResolver interface,
    for resolving conditions from definitions.
    """
    
    def __init__(self, registry: IConditionRegistry):
        """
        Initialize a condition resolver.
        
        Args:
            registry: Condition registry to use for resolving conditions
        """
        self._registry = registry
    
    def resolve_condition(self, condition_def: Dict[str, Any]) -> ICondition:
        """
        Resolve a condition from a definition.
        
        Args:
            condition_def: Condition definition
            
        Returns:
            Resolved condition
            
        Raises:
            ConditionResolverError: If the condition cannot be resolved
        """
        try:
            # Get the condition type
            condition_type = condition_def.get("condition_type")
            if not condition_type:
                raise ConditionResolverError("Condition type is required")
            
            # Handle compound conditions
            if condition_type == "and":
                return self.resolve_compound_condition(condition_def)
            elif condition_type == "or":
                return self.resolve_compound_condition(condition_def)
            elif condition_type == "not":
                # Create a NOT condition
                not_condition = NotCondition(condition_def)
                
                # Resolve the child condition
                child_def = condition_def.get("condition")
                if not child_def:
                    raise ConditionResolverError("Child condition is required for NOT condition")
                
                child_condition = self.resolve_condition(child_def)
                not_condition.condition = child_condition
                
                return not_condition
            
            # Get the provider for the condition type
            provider = self._registry.get_provider_for_condition_type(condition_type)
            if not provider:
                raise ConditionTypeNotFoundError(condition_type)
            
            # Create the condition
            return provider.create_condition(condition_type, condition_def)
        except ConditionTypeNotFoundError as e:
            raise ConditionResolverError(f"Condition type '{e.condition_type}' not found")
        except Exception as e:
            if isinstance(e, ConditionResolverError):
                raise
            raise ConditionResolverError(f"Error resolving condition: {str(e)}", e)
    
    def resolve_compound_condition(self, condition_def: Dict[str, Any]) -> ICompoundCondition:
        """
        Resolve a compound condition from a definition.
        
        Args:
            condition_def: Compound condition definition
            
        Returns:
            Resolved compound condition
            
        Raises:
            ConditionResolverError: If the compound condition cannot be resolved
        """
        try:
            # Get the condition type
            condition_type = condition_def.get("condition_type")
            if not condition_type:
                raise ConditionResolverError("Condition type is required")
            
            # Create the compound condition
            if condition_type == "and":
                compound_condition = AndCondition(condition_def)
            elif condition_type == "or":
                compound_condition = OrCondition(condition_def)
            else:
                raise ConditionResolverError(f"Condition type '{condition_type}' is not a compound condition type")
            
            # Resolve child conditions
            child_defs = condition_def.get("conditions", [])
            for child_def in child_defs:
                child_condition = self.resolve_condition(child_def)
                compound_condition.add_condition(child_condition)
            
            return compound_condition
        except Exception as e:
            if isinstance(e, ConditionResolverError):
                raise
            raise ConditionResolverError(f"Error resolving compound condition: {str(e)}", e)
