"""
Adapter for VariableStorage to provide the interface expected by the UI.
SOLID: Single responsibility - adapting variable operations.
KISS: Simple delegation to VariableStorage.
"""
from typing import List, Dict, Any, Optional

from src.core.context.variable_storage import VariableStorage, VariableScope
from src.core.models import Variable as UIVariable

class VariableAdapter:
    """Adapter for VariableStorage to provide the interface expected by the UI."""
    
    def __init__(self, variable_storage: VariableStorage):
        """Initialize the adapter with a VariableStorage instance."""
        self.variable_storage = variable_storage
    
    def get_all_variables(self) -> Dict[str, List[UIVariable]]:
        """
        Get all variables grouped by scope.
        
        Returns:
            Dictionary mapping scope names to lists of variables.
        """
        result = {}
        
        # Get variables for each scope
        for scope in VariableScope:
            scope_name = scope.name.capitalize()
            variables = []
            
            # Convert backend variables to UI variables
            for name, value in self.variable_storage._variables[scope].items():
                variables.append(UIVariable(
                    name=name,
                    value=value,
                    type=self._get_type_name(value),
                    scope=scope_name
                ))
            
            result[scope_name] = variables
        
        return result
    
    def get_variable(self, name: str) -> Optional[UIVariable]:
        """
        Get a variable by name.
        
        Args:
            name: Variable name
            
        Returns:
            Variable in the UI-expected format, or None if not found.
        """
        value = self.variable_storage.get(name)
        if value is not None:
            # Determine the scope
            scope = None
            for s in VariableScope:
                if name in self.variable_storage._variables[s]:
                    scope = s.name.capitalize()
                    break
            
            if scope:
                return UIVariable(
                    name=name,
                    value=value,
                    type=self._get_type_name(value),
                    scope=scope
                )
        
        return None
    
    def add_variable(self, name: str, value: Any, scope: str = "Workflow") -> UIVariable:
        """
        Add a new variable.
        
        Args:
            name: Variable name
            value: Variable value
            scope: Scope name (Global, Workflow, Local)
            
        Returns:
            The new variable in the UI-expected format.
        """
        # Convert scope name to enum
        scope_enum = VariableScope[scope.upper()]
        
        # Set the variable in the backend
        self.variable_storage.set(name, value, scope_enum)
        
        # Return the UI-expected format
        return UIVariable(
            name=name,
            value=value,
            type=self._get_type_name(value),
            scope=scope
        )
    
    def update_variable(self, name: str, value: Any, scope: str = "Workflow") -> UIVariable:
        """
        Update an existing variable.
        
        Args:
            name: Variable name
            value: New value
            scope: Scope name (Global, Workflow, Local)
            
        Returns:
            The updated variable in the UI-expected format.
        """
        # Convert scope name to enum
        scope_enum = VariableScope[scope.upper()]
        
        # Set the variable in the backend
        self.variable_storage.set(name, value, scope_enum)
        
        # Return the UI-expected format
        return UIVariable(
            name=name,
            value=value,
            type=self._get_type_name(value),
            scope=scope
        )
    
    def delete_variable(self, name: str, scope: str = "Workflow") -> bool:
        """
        Delete a variable.
        
        Args:
            name: Variable name
            scope: Scope name (Global, Workflow, Local)
            
        Returns:
            True if the variable was deleted, False if not found.
        """
        # Convert scope name to enum
        scope_enum = VariableScope[scope.upper()]
        
        # Check if the variable exists
        if name in self.variable_storage._variables[scope_enum]:
            # Delete the variable
            self.variable_storage.delete(name, scope_enum)
            return True
        
        return False
    
    def _get_type_name(self, value: Any) -> str:
        """
        Get the type name of a value.
        
        Args:
            value: Any value
            
        Returns:
            Type name as a string.
        """
        if value is None:
            return "None"
        elif isinstance(value, str):
            return "String"
        elif isinstance(value, int):
            return "Integer"
        elif isinstance(value, float):
            return "Float"
        elif isinstance(value, bool):
            return "Boolean"
        elif isinstance(value, list):
            return "List"
        elif isinstance(value, dict):
            return "Dictionary"
        else:
            return value.__class__.__name__
