"""
Variable adapter implementation.

This module provides a concrete implementation of the variable adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.variables.variable_storage import VariableStorage
from src.core.variables.variable_type import VariableType
from src.ui.adapters.base.base_variable_adapter import BaseVariableAdapter


class VariableAdapter(BaseVariableAdapter):
    """Concrete implementation of variable adapter."""
    
    def __init__(self, variable_storage: Optional[VariableStorage] = None):
        """
        Initialize the adapter with a VariableStorage instance.
        
        Args:
            variable_storage: Optional variable storage to use
        """
        self._variable_storage = variable_storage or VariableStorage()
    
    def get_variable_types(self) -> List[Dict[str, Any]]:
        """
        Get all available variable types.
        
        Returns:
            List of variable types with metadata
        """
        return [
            {
                "id": "string",
                "name": "String",
                "description": "Text value",
                "icon": "text"
            },
            {
                "id": "number",
                "name": "Number",
                "description": "Numeric value",
                "icon": "number"
            },
            {
                "id": "boolean",
                "name": "Boolean",
                "description": "True/False value",
                "icon": "toggle"
            },
            {
                "id": "list",
                "name": "List",
                "description": "List of values",
                "icon": "list"
            },
            {
                "id": "dictionary",
                "name": "Dictionary",
                "description": "Key-value pairs",
                "icon": "dict"
            }
        ]
    
    def get_all_variables(self) -> List[Dict[str, Any]]:
        """
        Get all variables.
        
        Returns:
            List of variables in the UI-expected format
        """
        # Get all variables from the storage
        variables = self._variable_storage.get_all_variables()
        
        # Convert to UI format
        return [self._convert_variable_to_ui_format(name, value, var_type) 
                for name, (value, var_type) in variables.items()]
    
    def get_variable(self, variable_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a variable by name.
        
        Args:
            variable_name: Variable name
            
        Returns:
            Variable in the UI-expected format, or None if not found
        """
        # Get the variable from the storage
        if not self._variable_storage.has_variable(variable_name):
            return None
        
        value = self._variable_storage.get_variable(variable_name)
        var_type = self._variable_storage.get_variable_type(variable_name)
        
        # Convert to UI format
        return self._convert_variable_to_ui_format(variable_name, value, var_type)
    
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
        # Validate the variable
        errors = self.validate_variable(variable_name, variable_value, variable_type)
        if errors:
            raise ValueError(f"Invalid variable: {', '.join(errors)}")
        
        # Determine the variable type if not specified
        if variable_type is None:
            variable_type = self._infer_variable_type(variable_value)
        
        # Convert the variable type to enum
        var_type_enum = self._get_variable_type_enum(variable_type)
        
        # Set the variable
        self._variable_storage.set_variable(variable_name, variable_value, var_type_enum)
        
        # Return the variable in UI format
        return self._convert_variable_to_ui_format(variable_name, variable_value, var_type_enum)
    
    def delete_variable(self, variable_name: str) -> bool:
        """
        Delete a variable.
        
        Args:
            variable_name: Variable name
            
        Returns:
            True if the variable was deleted, False if not found
        """
        # Check if the variable exists
        if not self._variable_storage.has_variable(variable_name):
            return False
        
        # Delete the variable
        self._variable_storage.delete_variable(variable_name)
        return True
    
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
        errors = []
        
        # Validate variable name
        if not variable_name:
            errors.append("Variable name is required")
        elif not isinstance(variable_name, str):
            errors.append("Variable name must be a string")
        elif not variable_name.isidentifier():
            errors.append("Variable name must be a valid identifier")
        
        # Determine the variable type if not specified
        if variable_type is None:
            variable_type = self._infer_variable_type(variable_value)
        
        # Validate variable value based on type
        try:
            var_type_enum = self._get_variable_type_enum(variable_type)
            self._validate_variable_value(variable_value, var_type_enum)
        except ValueError as e:
            errors.append(str(e))
        
        return errors
    
    def _convert_variable_to_ui_format(self, name: str, value: Any, var_type: VariableType) -> Dict[str, Any]:
        """
        Convert a variable to UI format.
        
        Args:
            name: Variable name
            value: Variable value
            var_type: Variable type
            
        Returns:
            Variable in UI format
        """
        return {
            "name": name,
            "value": value,
            "type": var_type.name.lower(),
            "readOnly": False
        }
    
    def _infer_variable_type(self, value: Any) -> str:
        """
        Infer the variable type from its value.
        
        Args:
            value: Variable value
            
        Returns:
            Inferred variable type
        """
        if isinstance(value, str):
            return "string"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, list):
            return "list"
        elif isinstance(value, dict):
            return "dictionary"
        else:
            return "string"
    
    def _get_variable_type_enum(self, variable_type: str) -> VariableType:
        """
        Get the VariableType enum for a variable type string.
        
        Args:
            variable_type: Variable type string
            
        Returns:
            VariableType enum
            
        Raises:
            ValueError: If the variable type is not supported
        """
        type_map = {
            "string": VariableType.STRING,
            "number": VariableType.NUMBER,
            "boolean": VariableType.BOOLEAN,
            "list": VariableType.LIST,
            "dictionary": VariableType.DICTIONARY
        }
        
        if variable_type.lower() not in type_map:
            raise ValueError(f"Unsupported variable type: {variable_type}")
        
        return type_map[variable_type.lower()]
    
    def _validate_variable_value(self, value: Any, var_type: VariableType) -> None:
        """
        Validate a variable value against a type.
        
        Args:
            value: Variable value
            var_type: Variable type
            
        Raises:
            ValueError: If the value is invalid for the type
        """
        if var_type == VariableType.STRING:
            if not isinstance(value, str):
                raise ValueError("String variable must be a string")
        elif var_type == VariableType.NUMBER:
            if not isinstance(value, (int, float)):
                raise ValueError("Number variable must be a number")
        elif var_type == VariableType.BOOLEAN:
            if not isinstance(value, bool):
                raise ValueError("Boolean variable must be a boolean")
        elif var_type == VariableType.LIST:
            if not isinstance(value, list):
                raise ValueError("List variable must be a list")
        elif var_type == VariableType.DICTIONARY:
            if not isinstance(value, dict):
                raise ValueError("Dictionary variable must be a dictionary")
