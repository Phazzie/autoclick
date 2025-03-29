"""Improved implementation of the Variable interface"""
import copy
import logging
from typing import Any, Dict, Generic, TypeVar, Callable, Optional, List, Type, ClassVar

from src.core.context.variable_storage import VariableScope
from src.core.variables.variable_interface import (
    IVariable, VariableType, VariableChangeEvent, TypeValidator
)

# Type variable for generic typing
T = TypeVar('T')


class Variable(IVariable[T], Generic[T]):
    """
    Implementation of the Variable interface using composition
    
    This class implements the Variable interface using composition rather than inheritance,
    separating the concerns of value storage, type validation, change notification, and
    serialization into distinct components.
    """
    
    def __init__(
        self,
        name: str,
        value: T,
        var_type: VariableType,
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a variable
        
        Args:
            name: Variable name
            value: Initial value
            var_type: Variable type
            scope: Variable scope
            metadata: Optional metadata dictionary
            
        Raises:
            ValueError: If the value doesn't match the specified type
        """
        self._name = name
        self._type = var_type
        self._scope = scope
        self._metadata = metadata or {}
        self._change_listeners: List[Callable[[VariableChangeEvent], None]] = []
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        
        # Validate and set the initial value
        if not self.is_valid_value(value):
            try:
                # Try to convert the value to the correct type
                self._value = self.convert_value(value)
            except ValueError as e:
                raise ValueError(f"Invalid value for variable '{name}' of type {var_type.name}: {str(e)}")
        else:
            self._value = value
    
    def get_name(self) -> str:
        """Get the variable name"""
        return self._name
        
    def get_type(self) -> VariableType:
        """Get the variable type"""
        return self._type
        
    def get_scope(self) -> VariableScope:
        """Get the variable scope"""
        return self._scope
        
    def get_value(self) -> T:
        """Get the variable value"""
        return copy.deepcopy(self._value)
        
    def set_value(self, new_value: T) -> None:
        """
        Set the variable value
        
        Args:
            new_value: New value for the variable
            
        Raises:
            ValueError: If the value doesn't match the variable type
        """
        # Validate the new value
        if not self.is_valid_value(new_value):
            try:
                # Try to convert the value to the correct type
                converted_value = self.convert_value(new_value)
            except ValueError as e:
                raise ValueError(f"Invalid value for variable '{self._name}' of type {self._type.name}: {str(e)}")
        else:
            converted_value = new_value
            
        # If the value hasn't changed, do nothing
        if self._value == converted_value:
            return
            
        # Save the old value
        old_value = self._value
        
        # Update the value
        self._value = converted_value
        
        # Notify listeners
        self._notify_change(old_value, converted_value)
    
    def is_valid_value(self, value: Any) -> bool:
        """
        Check if a value is valid for this variable
        
        Args:
            value: Value to check
            
        Returns:
            True if the value is valid, False otherwise
        """
        return TypeValidator.validate(value, self._type)
        
    def convert_value(self, value: Any) -> Any:
        """
        Convert a value to the correct type if possible
        
        Args:
            value: Value to convert
            
        Returns:
            Converted value
            
        Raises:
            ValueError: If the value cannot be converted
        """
        return TypeValidator.convert(value, self._type)
        
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get all metadata
        
        Returns:
            Dictionary of metadata
        """
        return copy.deepcopy(self._metadata)
        
    def get_metadata_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific metadata value
        
        Args:
            key: Metadata key
            default: Default value if key doesn't exist
            
        Returns:
            Metadata value or default
        """
        return self._metadata.get(key, default)
        
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set a metadata value
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self._metadata[key] = value
        
    def add_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Add a listener for variable changes
        
        Args:
            listener: Callback function that will be called when the variable changes
        """
        if listener not in self._change_listeners:
            self._change_listeners.append(listener)
        
    def remove_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Remove a listener for variable changes
        
        Args:
            listener: Callback function to remove
        """
        if listener in self._change_listeners:
            self._change_listeners.remove(listener)
    
    def _notify_change(self, old_value: Any, new_value: Any) -> None:
        """
        Notify listeners of a value change
        
        Args:
            old_value: Previous value
            new_value: New value
        """
        event = VariableChangeEvent(
            variable_name=self._name,
            old_value=old_value,
            new_value=new_value,
            scope=self._scope
        )
        
        # Log the change
        self.logger.debug(f"Variable '{self._name}' changed: {old_value} -> {new_value}")
        
        # Notify listeners
        for listener in self._change_listeners:
            try:
                listener(event)
            except Exception as e:
                self.logger.error(f"Error in variable change listener: {str(e)}")
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert variable to dictionary for serialization
        
        Returns:
            Dictionary representation of the variable
        """
        return {
            "name": self._name,
            "type": self._type.name,
            "scope": self._scope.name,
            "value": self._value,
            "metadata": self._metadata
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Variable':
        """
        Create variable from dictionary
        
        Args:
            data: Dictionary representation of the variable
            
        Returns:
            Instantiated variable
            
        Raises:
            ValueError: If the dictionary is invalid
        """
        # Validate required fields
        required_fields = ["name", "type", "value"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
                
        # Parse the type and scope
        try:
            var_type = VariableType[data["type"]]
        except KeyError:
            raise ValueError(f"Invalid variable type: {data['type']}")
            
        scope = VariableScope.WORKFLOW
        if "scope" in data:
            try:
                scope = VariableScope[data["scope"]]
            except KeyError:
                raise ValueError(f"Invalid variable scope: {data['scope']}")
                
        # Create the variable
        return cls(
            name=data["name"],
            value=data["value"],
            var_type=var_type,
            scope=scope,
            metadata=data.get("metadata", {})
        )
        
    def __str__(self) -> str:
        """String representation of the variable"""
        return f"{self._name} ({self._type.name}) = {self._value}"
        
    def __repr__(self) -> str:
        """Detailed string representation of the variable"""
        return f"Variable(name='{self._name}', type={self._type.name}, scope={self._scope.name}, value={self._value})"
