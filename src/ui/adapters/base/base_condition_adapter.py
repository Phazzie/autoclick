"""
Base condition adapter implementation.

This module provides a base implementation of the condition adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.ui.adapters.interfaces.icondition_adapter import IConditionAdapter


class BaseConditionAdapter(IConditionAdapter):
    """Base implementation of condition adapter."""
    
    def get_condition_types(self) -> List[Dict[str, Any]]:
        """
        Get all available condition types.
        
        Returns:
            List of condition types with metadata
        """
        raise NotImplementedError("Subclasses must implement get_condition_types")
    
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
        raise NotImplementedError("Subclasses must implement get_condition_schema")
    
    def create_condition(self, condition_type: str, condition_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a condition.
        
        Args:
            condition_type: Condition type
            condition_data: Condition data
            
        Returns:
            Created condition in the UI-expected format
            
        Raises:
            ValueError: If the condition data is invalid
        """
        raise NotImplementedError("Subclasses must implement create_condition")
    
    def validate_condition(self, condition_type: str, condition_data: Dict[str, Any]) -> List[str]:
        """
        Validate a condition.
        
        Args:
            condition_type: Condition type
            condition_data: Condition data
            
        Returns:
            List of validation errors, empty if valid
        """
        raise NotImplementedError("Subclasses must implement validate_condition")
