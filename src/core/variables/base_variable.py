"""Base implementation of the VariableInterface"""
import copy
import logging
from typing import Any, Dict, Generic, TypeVar, Callable, Optional, List, Type, ClassVar

from src.core.context.variable_storage import VariableScope
from src.core.variables.variable_interface import (
    VariableInterface, VariableType, VariableChangeEvent, TypeValidator
)

# Type variable for generic typing
T = TypeVar('T')


class BaseVariable(VariableInterface[T], Generic[T]):
    """Base implementation of the VariableInterface"""
    
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
        if not TypeValidator.validate(value, var_type):
            try:
                # Try to convert the value to the correct type
                self._value = TypeValidator.convert(value, var_type)
            except ValueError as e:
                raise ValueError(f"Invalid value for variable '{name}' of type {var_type.name}: {str(e)}")
        else:
            self._value = value
    
    @property
    def name(self) -> str:
        """Get the variable name"""
        return self._name
        
    @property
    def type(self) -> VariableType:
        """Get the variable type"""
        return self._type
        
    @property
    def scope(self) -> VariableScope:
        """Get the variable scope"""
        return self._scope
        
    @property
    def value(self) -> T:
        """Get the variable value"""
        return copy.deepcopy(self._value)
        
    @value.setter
    def value(self, new_value: T) -> None:
        """
        Set the variable value
        
        Args:
            new_value: New value for the variable
            
        Raises:
            ValueError: If the value doesn't match the variable type
        """
        # Validate the new value
        if not TypeValidator.validate(new_value, self._type):
            try:
                # Try to convert the value to the correct type
                converted_value = TypeValidator.convert(new_value, self._type)
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
        
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get variable metadata
        
        Returns:
            Dictionary of metadata
        """
        return copy.deepcopy(self._metadata)
        
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set variable metadata
        
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
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseVariable':
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
        required_fields = ["name", "type", "scope", "value"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
                
        # Parse the type and scope
        try:
            var_type = VariableType[data["type"]]
        except KeyError:
            raise ValueError(f"Invalid variable type: {data['type']}")
            
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
        return f"BaseVariable(name='{self._name}', type={self._type.name}, scope={self._scope.name}, value={self._value})"
