"""Factory for creating variables"""
import logging
from typing import Any, Dict, Type, Optional, Dict, Union, List, TypeVar, Generic

from src.core.context.variable_storage import VariableScope
from src.core.variables.variable_interface import VariableType
from src.core.variables.variable import Variable
from src.core.variables.typed_variables import (
    StringVariable, NumberVariable, BooleanVariable, ListVariable, DictionaryVariable
)

# Type variable for generic typing
T = TypeVar('T')


class VariableFactory:
    """Factory for creating variables of different types"""
    
    def __init__(self):
        """Initialize the variable factory"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._variable_classes: Dict[VariableType, Type[Variable]] = {
            VariableType.STRING: StringVariable,
            VariableType.NUMBER: NumberVariable,
            VariableType.BOOLEAN: BooleanVariable,
            VariableType.LIST: ListVariable,
            VariableType.DICTIONARY: DictionaryVariable,
            VariableType.ANY: Variable
        }
    
    def create_variable(
        self,
        name: str,
        value: Any,
        var_type: Optional[VariableType] = None,
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Variable:
        """
        Create a variable of the specified type
        
        Args:
            name: Variable name
            value: Initial value
            var_type: Variable type (inferred from value if not specified)
            scope: Variable scope
            metadata: Optional metadata dictionary
            
        Returns:
            Created variable
            
        Raises:
            ValueError: If the value cannot be converted to the specified type
            TypeError: If the variable type is not supported
        """
        # Infer type from value if not specified
        if var_type is None:
            var_type = self._infer_type(value)
            
        # Get the variable class for the type
        variable_class = self._get_variable_class(var_type)
        
        # Create and return the variable
        return variable_class(name, value, scope, metadata)
    
    def create_from_dict(self, data: Dict[str, Any]) -> Variable:
        """
        Create a variable from a dictionary
        
        Args:
            data: Dictionary representation of the variable
            
        Returns:
            Created variable
            
        Raises:
            ValueError: If the dictionary is invalid
            TypeError: If the variable type is not supported
        """
        # Validate required fields
        required_fields = ["name", "type", "value"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
                
        # Parse the type
        try:
            var_type = VariableType[data["type"]]
        except KeyError:
            raise ValueError(f"Invalid variable type: {data['type']}")
            
        # Parse the scope
        scope = VariableScope.WORKFLOW
        if "scope" in data:
            try:
                scope = VariableScope[data["scope"]]
            except KeyError:
                raise ValueError(f"Invalid variable scope: {data['scope']}")
                
        # Get the variable class for the type
        variable_class = self._get_variable_class(var_type)
        
        # Create and return the variable
        return variable_class(
            name=data["name"],
            value=data["value"],
            scope=scope,
            metadata=data.get("metadata", {})
        )
    
    def register_variable_class(self, var_type: VariableType, variable_class: Type[Variable]) -> None:
        """
        Register a variable class for a type
        
        Args:
            var_type: Variable type
            variable_class: Variable class to register
            
        Raises:
            TypeError: If the variable class doesn't inherit from Variable
        """
        if not issubclass(variable_class, Variable):
            raise TypeError(f"Variable class must inherit from Variable: {variable_class.__name__}")
            
        self._variable_classes[var_type] = variable_class
        self.logger.info(f"Registered variable class {variable_class.__name__} for type {var_type.name}")
    
    def _get_variable_class(self, var_type: VariableType) -> Type[Variable]:
        """
        Get the variable class for a type
        
        Args:
            var_type: Variable type
            
        Returns:
            Variable class
            
        Raises:
            TypeError: If the variable type is not supported
        """
        if var_type not in self._variable_classes:
            raise TypeError(f"Unsupported variable type: {var_type.name}")
            
        return self._variable_classes[var_type]
    
    def _infer_type(self, value: Any) -> VariableType:
        """
        Infer the variable type from a value
        
        Args:
            value: Value to infer type from
            
        Returns:
            Inferred variable type
        """
        if isinstance(value, str):
            return VariableType.STRING
        elif isinstance(value, bool):
            return VariableType.BOOLEAN
        elif isinstance(value, (int, float)):
            return VariableType.NUMBER
        elif isinstance(value, list):
            return VariableType.LIST
        elif isinstance(value, dict):
            return VariableType.DICTIONARY
        else:
            return VariableType.OBJECT
