"""
Base variable adapter implementation.

This module provides a base implementation of the variable adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.ui.adapters.interfaces.ivariable_adapter import IVariableAdapter


class BaseVariableAdapter(IVariableAdapter):
    """Base implementation of variable adapter."""
    
    def get_variable_types(self) -> List[Dict[str, Any]]:
        """
        Get all available variable types.
        
        Returns:
            List of variable types with metadata
        """
        raise NotImplementedError("Subclasses must implement get_variable_types")
    
    def get_all_variables(self) -> List[Dict[str, Any]]:
        """
        Get all variables.
        
        Returns:
            List of variables in the UI-expected format
        """
        raise NotImplementedError("Subclasses must implement get_all_variables")
    
    def get_variable(self, variable_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a variable by name.
        
        Args:
            variable_name: Variable name
            
        Returns:
            Variable in the UI-expected format, or None if not found
        """
        raise NotImplementedError("Subclasses must implement get_variable")
    
    def set_variable(self, variable_name: str, variable_value: Any, variable_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Set a variable value.
        
        Args:
            variable_name: Variable name
            variable_value: Variable value
            variable_type: Optional variable type
            
        Returns:
            Variable in the UI-expected format
            
        Raises:
            ValueError: If the variable value is invalid for the specified type
        """
        raise NotImplementedError("Subclasses must implement set_variable")
    
    def delete_variable(self, variable_name: str) -> bool:
        """
        Delete a variable.
        
        Args:
            variable_name: Variable name
            
        Returns:
            True if the variable was deleted, False if not found
        """
        raise NotImplementedError("Subclasses must implement delete_variable")
    
    def validate_variable(self, variable_name: str, variable_value: Any, variable_type: Optional[str] = None) -> List[str]:
        """
        Validate a variable value.
        
        Args:
            variable_name: Variable name
            variable_value: Variable value
            variable_type: Optional variable type
            
        Returns:
            List of validation errors, empty if valid
        """
        raise NotImplementedError("Subclasses must implement validate_variable")
