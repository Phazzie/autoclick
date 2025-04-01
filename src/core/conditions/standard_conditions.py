"""
Standard condition implementations.

This module provides implementations of standard conditions.
"""
from typing import Dict, Any

from src.core.context.interfaces import IExecutionContext
from .base_condition_new import BaseCondition


class TrueCondition(BaseCondition):
    """
    Implementation of a TRUE condition.
    
    This class provides an implementation of a condition that is always met.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a TRUE condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("true", config)
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the TRUE condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            Always True
        """
        return True


class FalseCondition(BaseCondition):
    """
    Implementation of a FALSE condition.
    
    This class provides an implementation of a condition that is never met.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a FALSE condition.
        
        Args:
            config: Configuration for the condition
        """
        super().__init__("false", config)
    
    def _evaluate(self, context: IExecutionContext) -> bool:
        """
        Evaluate the FALSE condition with the given context.
        
        Args:
            context: Execution context
            
        Returns:
            Always False
        """
        return False
