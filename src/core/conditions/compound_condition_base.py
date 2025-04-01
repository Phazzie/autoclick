"""
Base compound condition implementation.

This module provides a base implementation of the ICompoundCondition interface.
"""
from typing import Dict, Any, List, Optional

from .interfaces import ICondition, ICompoundCondition
from .base_condition_new import BaseCondition
from .exceptions import ConditionNotFoundError


class CompoundCondition(BaseCondition, ICompoundCondition):
    """
    Base implementation of a compound condition.
    
    This class provides a base implementation of the ICompoundCondition interface,
    for conditions that combine other conditions.
    """
    
    def __init__(self, condition_type: str, config: Dict[str, Any]):
        """
        Initialize a compound condition.
        
        Args:
            condition_type: Type of condition
            config: Configuration for the condition
        """
        super().__init__(condition_type, config)
        self._conditions: Dict[str, ICondition] = {}
    
    def add_condition(self, condition: ICondition) -> None:
        """
        Add a condition to this compound condition.
        
        Args:
            condition: Condition to add
        """
        self._conditions[condition.condition_id] = condition
    
    def remove_condition(self, condition_id: str) -> None:
        """
        Remove a condition from this compound condition.
        
        Args:
            condition_id: ID of the condition to remove
            
        Raises:
            ConditionNotFoundError: If the condition is not found
        """
        if condition_id not in self._conditions:
            raise ConditionNotFoundError(condition_id)
        
        del self._conditions[condition_id]
    
    def get_conditions(self) -> List[ICondition]:
        """
        Get all conditions in this compound condition.
        
        Returns:
            List of conditions
        """
        return list(self._conditions.values())
    
    def get_condition(self, condition_id: str) -> Optional[ICondition]:
        """
        Get a condition by ID.
        
        Args:
            condition_id: Condition ID
            
        Returns:
            Condition or None if not found
        """
        return self._conditions.get(condition_id)
    
    def _validate(self) -> List[str]:
        """
        Validate the compound condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate child conditions
        for condition in self._conditions.values():
            condition_errors = condition.validate()
            if condition_errors:
                errors.append(f"Errors in condition '{condition.condition_id}':")
                for error in condition_errors:
                    errors.append(f"  - {error}")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the compound condition to a dictionary.
        
        Returns:
            Dictionary representation of the compound condition
        """
        result = super().to_dict()
        
        # Add conditions
        result["conditions"] = [condition.to_dict() for condition in self._conditions.values()]
        
        return result
