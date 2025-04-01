"""
Compound condition implementations.

This module provides implementations of compound conditions,
such as AND, OR, and NOT conditions.
"""
from typing import Dict, Any, List, Optional

from src.core.context.interfaces import IExecutionContext
from .interfaces import ICondition
from .compound_condition_base import CompoundCondition
from .base_condition_new import BaseCondition
from .exceptions import ConditionEvaluationError


class AndCondition(CompoundCondition):
    """
    Implementation of an AND condition.
    
    This class provides an implementation of a condition that is met
    when all of its child conditions are met.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize an AND condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("and", config)
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the AND condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if all child conditions are met, False otherwise
        """
        # If there are no conditions, return True
        if not self._conditions:
            return True
        
        # Evaluate all conditions
        for condition in self._conditions.values():
            if not condition.evaluate(context):
                return False
        
        return True
    
    def _validate(self) -> List[str]:
        """
        Validate the AND condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = super()._validate()
        
        # No additional validation needed
        
        return errors


class OrCondition(CompoundCondition):
    """
    Implementation of an OR condition.
    
    This class provides an implementation of a condition that is met
    when at least one of its child conditions is met.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize an OR condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("or", config)
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the OR condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if at least one child condition is met, False otherwise
        """
        # If there are no conditions, return False
        if not self._conditions:
            return False
        
        # Evaluate all conditions
        for condition in self._conditions.values():
            if condition.evaluate(context):
                return True
        
        return False
    
    def _validate(self) -> List[str]:
        """
        Validate the OR condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = super()._validate()
        
        # No additional validation needed
        
        return errors


class NotCondition(BaseCondition):
    """
    Implementation of a NOT condition.
    
    This class provides an implementation of a condition that is met
    when its child condition is not met.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a NOT condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("not", config)
        self._condition: Optional[ICondition] = None
    
    @property
    def condition(self) -> Optional[ICondition]:
        """Get the child condition."""
        return self._condition
    
    @condition.setter
    def condition(self, condition: ICondition) -> None:
        """Set the child condition."""
        self._condition = condition
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the NOT condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if the child condition is not met, False otherwise
            
        Raises:
            ConditionEvaluationError: If the child condition is not set
        """
        if self._condition is None:
            raise ConditionEvaluationError(self._condition_id, "Child condition is not set")
        
        return not self._condition.evaluate(context)
    
    def _validate(self) -> List[str]:
        """
        Validate the NOT condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate child condition
        if self._condition is None:
            errors.append("Child condition is required")
        else:
            condition_errors = self._condition.validate()
            if condition_errors:
                errors.append("Errors in child condition:")
                for error in condition_errors:
                    errors.append(f"  - {error}")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the NOT condition to a dictionary.
        
        Returns:
            Dictionary representation of the NOT condition
        """
        result = super().to_dict()
        
        # Add child condition
        if self._condition is not None:
            result["condition"] = self._condition.to_dict()
        
        return result
