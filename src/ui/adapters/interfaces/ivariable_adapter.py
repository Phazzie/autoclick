"""
Variable adapter interface.

This module defines the interface for variable adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IVariableAdapter(ABC):
    """Interface for variable adapters."""
    
    @abstractmethod
    def get_variable_types(self) -> List[Dict[str, Any]]:
        """
        Get all available variable types.
        
        Returns:
            List of variable types with metadata
        """
        pass
    
    @abstractmethod
    def get_all_variables(self) -> List[Dict[str, Any]]:
        """
        Get all variables.
        
        Returns:
            List of variables in the UI-expected format
        """
        pass
    
    @abstractmethod
    def get_variable(self, variable_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a variable by name.
        
        Args:
            variable_name: Variable name
            
        Returns:
            Variable in the UI-expected format, or None if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_variable(self, variable_name: str) -> bool:
        """
        Delete a variable.
        
        Args:
            variable_name: Variable name
            
        Returns:
            True if the variable was deleted, False if not found
        """
        pass
    
    @abstractmethod
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
        pass
