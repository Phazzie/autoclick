"""
Variable condition implementations.

This module provides implementations of variable-related conditions.
"""
from typing import Dict, Any, List, Optional
import re
import operator

from src.core.context.interfaces import IExecutionContext
from .base_condition_new import BaseCondition
from .exceptions import ConditionEvaluationError


class VariableCompareCondition(BaseCondition):
    """
    Implementation of a variable comparison condition.
    
    This class provides an implementation of a condition that compares a variable value
    with a specified value using a comparison operator.
    """
    
    # Supported operators
    OPERATORS = {
        'eq': operator.eq,
        'ne': operator.ne,
        'lt': operator.lt,
        'le': operator.le,
        'gt': operator.gt,
        'ge': operator.ge,
        'contains': lambda x, y: y in x if isinstance(x, (str, list, tuple, set, dict)) else False,
        'not_contains': lambda x, y: y not in x if isinstance(x, (str, list, tuple, set, dict)) else True,
        'starts_with': lambda x, y: x.startswith(y) if isinstance(x, str) else False,
        'ends_with': lambda x, y: x.endswith(y) if isinstance(x, str) else False,
        'matches': lambda x, y: bool(re.search(y, x)) if isinstance(x, str) else False
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a variable comparison condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("variable_compare", config)
        self._variable = config.get("variable")
        self._operator_name = config.get("operator")
        self._value = config.get("value")
        
        # Get the operator function
        self._operator_func = self.OPERATORS.get(self._operator_name)
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the variable comparison condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if the condition is met, False otherwise
            
        Raises:
            ConditionEvaluationError: If the variable does not exist or the operator is not supported
        """
        # Check if the variable exists
        if not context.has_variable(self._variable):
            return False
        
        # Get the variable value
        variable_value = context.get_variable(self._variable)
        
        # Check if the operator is supported
        if not self._operator_func:
            raise ConditionEvaluationError(self._condition_id, f"Unsupported operator: {self._operator_name}")
        
        try:
            # Compare the values
            return self._operator_func(variable_value, self._value)
        except Exception as e:
            # If the comparison fails (e.g., type mismatch), return False
            return False
    
    def _validate(self) -> List[str]:
        """
        Validate the variable comparison condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate variable
        if not self._variable:
            errors.append("Variable is required")
        
        # Validate operator
        if not self._operator_name:
            errors.append("Operator is required")
        elif self._operator_name not in self.OPERATORS:
            errors.append(f"Unsupported operator: {self._operator_name}")
        
        # Validate value
        if self._value is None:
            errors.append("Value is required")
        
        return errors


class VariableExistsCondition(BaseCondition):
    """
    Implementation of a variable exists condition.
    
    This class provides an implementation of a condition that checks if a variable exists.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a variable exists condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("variable_exists", config)
        self._variable = config.get("variable")
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the variable exists condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if the variable exists, False otherwise
        """
        return context.has_variable(self._variable)
    
    def _validate(self) -> List[str]:
        """
        Validate the variable exists condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate variable
        if not self._variable:
            errors.append("Variable is required")
        
        return errors


class VariableEmptyCondition(BaseCondition):
    """
    Implementation of a variable empty condition.
    
    This class provides an implementation of a condition that checks if a variable is empty.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a variable empty condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("variable_empty", config)
        self._variable = config.get("variable")
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the variable empty condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if the variable is empty, False otherwise
        """
        # Check if the variable exists
        if not context.has_variable(self._variable):
            return True
        
        # Get the variable value
        value = context.get_variable(self._variable)
        
        # Check if the value is empty
        if value is None:
            return True
        
        if isinstance(value, (str, list, tuple, set, dict)):
            return len(value) == 0
        
        return False
    
    def _validate(self) -> List[str]:
        """
        Validate the variable empty condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate variable
        if not self._variable:
            errors.append("Variable is required")
        
        return errors


class VariableTypeCondition(BaseCondition):
    """
    Implementation of a variable type condition.
    
    This class provides an implementation of a condition that checks the type of a variable.
    """
    
    # Supported types
    TYPE_CHECKS = {
        'string': lambda x: isinstance(x, str),
        'number': lambda x: isinstance(x, (int, float)),
        'boolean': lambda x: isinstance(x, bool),
        'list': lambda x: isinstance(x, list),
        'dict': lambda x: isinstance(x, dict),
        'null': lambda x: x is None
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a variable type condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("variable_type", config)
        self._variable = config.get("variable")
        self._type = config.get("type")
        
        # Get the type check function
        self._type_check = self.TYPE_CHECKS.get(self._type)
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the variable type condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            True if the variable is of the specified type, False otherwise
            
        Raises:
            ConditionEvaluationError: If the type is not supported
        """
        # Check if the variable exists
        if not context.has_variable(self._variable):
            return False
        
        # Get the variable value
        value = context.get_variable(self._variable)
        
        # Check if the type is supported
        if not self._type_check:
            raise ConditionEvaluationError(self._condition_id, f"Unsupported type: {self._type}")
        
        # Check the type
        return self._type_check(value)
    
    def _validate(self) -> List[str]:
        """
        Validate the variable type condition configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate variable
        if not self._variable:
            errors.append("Variable is required")
        
        # Validate type
        if not self._type:
            errors.append("Type is required")
        elif self._type not in self.TYPE_CHECKS:
            errors.append(f"Unsupported type: {self._type}")
        
        return errors
