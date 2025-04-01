"""
Base condition implementation.

This module provides a base implementation of the ICondition interface,
with common functionality for all condition types.
"""
import uuid
from typing import Dict, Any, List, Optional

from src.core.context.interfaces import IExecutionContext
from .interfaces import ICondition
from .exceptions import ConditionEvaluationError


class BaseCondition(ICondition):
    """
    Base implementation of a condition.
    
    This class provides a base implementation of the ICondition interface,
    with common functionality for all condition types.
    """
    
    def __init__(self, condition_type: str, config: Dict[str, Any]):
        """
        Initialize a base condition.
        
        Args:
            condition_type: Type of condition
            config: Configuration for the condition
        """
        self._condition_id = config.get("condition_id", str(uuid.uuid4()))
        self._condition_type = condition_type
        self._name = config.get("name", f"{condition_type.capitalize()} Condition")
        self._description = config.get("description")
        self._config = config.copy()
        
        # Remove standard properties from config
        for key in ["condition_id", "condition_type", "name", "description"]:
            if key in self._config:
                del self._config[key]
    
    @property
    def condition_id(self) -> str:
        """Get the condition ID."""
        return self._condition_id
    
    @property
    def condition_type(self) -> str:
        """Get the condition type."""
        return self._condition_type
    
    @property
    def name(self) -> str:
        """Get the condition name."""
        return self._name
    
    @property
    def description(self) -> Optional[str]:
        """Get the condition description."""
        return self._description
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the condition configuration."""
        return self._config.copy()
    
    def evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if the condition is met, False otherwise
            
        Raises:
            ConditionEvaluationError: If there is an error evaluating the condition
        """
        try:
            return self._evaluate(context)
        except ConditionEvaluationError:
            raise
        except Exception as e:
            raise ConditionEvaluationError(self._condition_id, str(e), e)
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the condition with the given context.
        
        This method should be overridden by subclasses to implement the actual evaluation logic.
        
        Args:
            context: Execution context
            
        Returns:
            True if the condition is met, False otherwise
            
        Raises:
            NotImplementedError: If the method is not overridden by a subclass
        """
        raise NotImplementedError("Subclasses must implement _evaluate")
    
    def validate(self) -> List[str]:
        """
        Validate the condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate standard properties
        if not self._condition_id:
            errors.append("Condition ID is required")
        
        if not self._condition_type:
            errors.append("Condition type is required")
        
        if not self._name:
            errors.append("Condition name is required")
        
        # Call subclass validation
        subclass_errors = self._validate()
        if subclass_errors:
            errors.extend(subclass_errors)
        
        return errors
    
    def _validate(self) -> List[str]:
        """
        Validate the condition configuration.
        
        This method should be overridden by subclasses to implement the actual validation logic.
        
        Returns:
            List of validation errors, empty if valid
        """
        return []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the condition to a dictionary.
        
        Returns:
            Dictionary representation of the condition
        """
        result = {
            "condition_id": self._condition_id,
            "condition_type": self._condition_type,
            "name": self._name,
            "description": self._description,
            **self._config
        }
        
        # Remove None values
        return {k: v for k, v in result.items() if v is not None}
    
    def __str__(self) -> str:
        """
        Get a string representation of the condition.
        
        Returns:
            String representation
        """
        return f"{self._name} ({self._condition_type})"
    
    def __repr__(self) -> str:
        """
        Get a detailed string representation of the condition.
        
        Returns:
            Detailed string representation
        """
        return f"{self.__class__.__name__}(condition_id='{self._condition_id}', condition_type='{self._condition_type}', name='{self._name}')"
