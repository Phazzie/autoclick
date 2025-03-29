"""Enhanced variable storage using the Variable interface"""
import copy
import re
import logging
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Callable, Union, Set, Tuple, Type, TypeVar, Generic, cast

from src.core.context.variable_storage import VariableScope, VariableChangeEvent as LegacyVariableChangeEvent
from src.core.variables.variable_interface import VariableType
from src.core.variables.variable import Variable
from src.core.variables.variable_factory import VariableFactory
from src.core.variables.typed_variables import (
    StringVariable, NumberVariable, BooleanVariable, ListVariable, DictionaryVariable
)

# Type variable for generic typing
T = TypeVar('T')


class VariableStorageV2:
    """Enhanced storage for variables with scoping using the Variable interface"""

    def __init__(self, parent: Optional['VariableStorageV2'] = None):
        """
        Initialize the variable storage
        
        Args:
            parent: Optional parent storage for variable inheritance
        """
        self._variables: Dict[VariableScope, Dict[str, Variable]] = {
            VariableScope.GLOBAL: {},
            VariableScope.WORKFLOW: {},
            VariableScope.LOCAL: {}
        }
        self._parent = parent
        self._variable_change_listeners: List[Callable[[LegacyVariableChangeEvent], None]] = []
        self._variable_name_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
        self._variable_factory = VariableFactory()
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def get(self, name: str, default: Any = None) -> Any:
        """
        Get a variable value (legacy method for backward compatibility)
        
        Args:
            name: Name of the variable
            default: Default value if variable doesn't exist
            
        Returns:
            Variable value or default if not found
        """
        variable = self.get_variable(name)
        if variable:
            return variable.get_value()
        return default
        
    def get_variable(self, name: str) -> Optional[Variable]:
        """
        Get a variable object
        
        Args:
            name: Name of the variable
            
        Returns:
            Variable object or None if not found
        """
        # Check local scope first
        if name in self._variables[VariableScope.LOCAL]:
            return self._variables[VariableScope.LOCAL][name]
            
        # Then check workflow scope
        if name in self._variables[VariableScope.WORKFLOW]:
            return self._variables[VariableScope.WORKFLOW][name]
            
        # Then check global scope
        if name in self._variables[VariableScope.GLOBAL]:
            return self._variables[VariableScope.GLOBAL][name]
            
        # If we have a parent, check there
        if self._parent:
            return self._parent.get_variable(name)
            
        # Not found
        return None
        
    def get_typed_variable(self, name: str, var_type: VariableType) -> Optional[Variable]:
        """
        Get a variable object with type checking
        
        Args:
            name: Name of the variable
            var_type: Expected variable type
            
        Returns:
            Variable object or None if not found or wrong type
            
        Raises:
            TypeError: If the variable exists but is not of the expected type
        """
        variable = self.get_variable(name)
        if not variable:
            return None
            
        if variable.get_type() != var_type:
            raise TypeError(f"Variable '{name}' is of type {variable.get_type().name}, not {var_type.name}")
            
        return variable
        
    def get_string(self, name: str) -> Optional[str]:
        """
        Get a string variable value
        
        Args:
            name: Name of the variable
            
        Returns:
            String value or None if not found
            
        Raises:
            TypeError: If the variable exists but is not a string
        """
        variable = self.get_typed_variable(name, VariableType.STRING)
        if variable:
            return cast(str, variable.get_value())
        return None
        
    def get_number(self, name: str) -> Optional[Union[int, float]]:
        """
        Get a number variable value
        
        Args:
            name: Name of the variable
            
        Returns:
            Number value or None if not found
            
        Raises:
            TypeError: If the variable exists but is not a number
        """
        variable = self.get_typed_variable(name, VariableType.NUMBER)
        if variable:
            return cast(Union[int, float], variable.get_value())
        return None
        
    def get_boolean(self, name: str) -> Optional[bool]:
        """
        Get a boolean variable value
        
        Args:
            name: Name of the variable
            
        Returns:
            Boolean value or None if not found
            
        Raises:
            TypeError: If the variable exists but is not a boolean
        """
        variable = self.get_typed_variable(name, VariableType.BOOLEAN)
        if variable:
            return cast(bool, variable.get_value())
        return None
        
    def get_list(self, name: str) -> Optional[List[Any]]:
        """
        Get a list variable value
        
        Args:
            name: Name of the variable
            
        Returns:
            List value or None if not found
            
        Raises:
            TypeError: If the variable exists but is not a list
        """
        variable = self.get_typed_variable(name, VariableType.LIST)
        if variable:
            return cast(List[Any], variable.get_value())
        return None
        
    def get_dictionary(self, name: str) -> Optional[Dict[Any, Any]]:
        """
        Get a dictionary variable value
        
        Args:
            name: Name of the variable
            
        Returns:
            Dictionary value or None if not found
            
        Raises:
            TypeError: If the variable exists but is not a dictionary
        """
        variable = self.get_typed_variable(name, VariableType.DICTIONARY)
        if variable:
            return cast(Dict[Any, Any], variable.get_value())
        return None
        
    def set(self, name: str, value: Any, scope: VariableScope = VariableScope.WORKFLOW) -> None:
        """
        Set a variable value (legacy method for backward compatibility)
        
        Args:
            name: Name of the variable
            value: Value to set
            scope: Scope of the variable
            
        Raises:
            ValueError: If the variable name is invalid
        """
        self._validate_variable_name(name)
        
        # Infer the variable type from the value
        var_type = self._infer_type(value)
        
        # Check if the variable already exists
        existing_variable = self.get_variable(name)
        if existing_variable and existing_variable.get_scope() == scope:
            # Update the existing variable
            existing_variable.set_value(value)
        else:
            # Create a new variable
            variable = self._variable_factory.create_variable(name, value, var_type, scope)
            
            # Store the variable
            self._variables[scope][name] = variable
            
            # Add a change listener to the variable
            variable.add_change_listener(self._on_variable_change)
            
            # Notify listeners about the new variable
            old_value = None
            if existing_variable:
                old_value = existing_variable.get_value()
                
            self._notify_variable_change(LegacyVariableChangeEvent(name, old_value, value, scope))
            
    def set_variable(self, variable: Variable) -> None:
        """
        Set a variable object
        
        Args:
            variable: Variable object to set
            
        Raises:
            ValueError: If the variable name is invalid
        """
        name = variable.get_name()
        scope = variable.get_scope()
        value = variable.get_value()
        
        self._validate_variable_name(name)
        
        # Check if the variable already exists
        existing_variable = self.get_variable(name)
        old_value = None
        if existing_variable:
            old_value = existing_variable.get_value()
            
        # Store the variable
        self._variables[scope][name] = variable
        
        # Add a change listener to the variable
        variable.add_change_listener(self._on_variable_change)
        
        # Notify listeners
        self._notify_variable_change(LegacyVariableChangeEvent(name, old_value, value, scope))
        
    def create_variable(
        self,
        name: str,
        value: Any,
        var_type: Optional[VariableType] = None,
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Variable:
        """
        Create and store a new variable
        
        Args:
            name: Name of the variable
            value: Initial value
            var_type: Variable type (inferred from value if not specified)
            scope: Variable scope
            metadata: Optional metadata dictionary
            
        Returns:
            Created variable
            
        Raises:
            ValueError: If the variable name is invalid
        """
        self._validate_variable_name(name)
        
        # Create the variable
        variable = self._variable_factory.create_variable(name, value, var_type, scope, metadata)
        
        # Store the variable
        self.set_variable(variable)
        
        return variable
        
    def delete(self, name: str, scope: Optional[VariableScope] = None) -> bool:
        """
        Delete a variable
        
        Args:
            name: Name of the variable
            scope: Scope of the variable (if None, delete from all scopes)
            
        Returns:
            True if the variable was deleted, False if not found
        """
        deleted = False
        
        if scope:
            # Delete from specific scope
            if name in self._variables[scope]:
                variable = self._variables[scope][name]
                old_value = variable.get_value()
                del self._variables[scope][name]
                self._notify_variable_change(LegacyVariableChangeEvent(name, old_value, None, scope))
                deleted = True
        else:
            # Delete from all scopes
            for s in VariableScope:
                if name in self._variables[s]:
                    variable = self._variables[s][name]
                    old_value = variable.get_value()
                    del self._variables[s][name]
                    self._notify_variable_change(LegacyVariableChangeEvent(name, old_value, None, s))
                    deleted = True
                    
        return deleted
        
    def clear_scope(self, scope: VariableScope) -> None:
        """
        Clear all variables in a scope
        
        Args:
            scope: Scope to clear
        """
        # Create a copy of the variables to notify about
        variables = list(self._variables[scope].items())
        
        # Clear the scope
        self._variables[scope].clear()
        
        # Notify listeners
        for name, variable in variables:
            self._notify_variable_change(LegacyVariableChangeEvent(name, variable.get_value(), None, scope))
            
    def clear_all(self) -> None:
        """Clear all variables in all scopes"""
        for scope in VariableScope:
            self.clear_scope(scope)
            
    def get_all(self, scope: Optional[VariableScope] = None) -> Dict[str, Any]:
        """
        Get all variable values in a scope or all scopes
        
        Args:
            scope: Scope to get variables from (if None, get from all scopes)
            
        Returns:
            Dictionary of variable names and values
        """
        result: Dict[str, Any] = {}
        
        if scope:
            # Get from specific scope
            for name, variable in self._variables[scope].items():
                result[name] = variable.get_value()
        else:
            # Get from all scopes (local overrides workflow overrides global)
            if self._parent:
                # Start with parent variables
                result.update(self._parent.get_all())
                
            # Add global variables
            for name, variable in self._variables[VariableScope.GLOBAL].items():
                result[name] = variable.get_value()
                
            # Add workflow variables
            for name, variable in self._variables[VariableScope.WORKFLOW].items():
                result[name] = variable.get_value()
                
            # Add local variables
            for name, variable in self._variables[VariableScope.LOCAL].items():
                result[name] = variable.get_value()
                
        return result
        
    def get_all_variables(self, scope: Optional[VariableScope] = None) -> Dict[str, Variable]:
        """
        Get all variable objects in a scope or all scopes
        
        Args:
            scope: Scope to get variables from (if None, get from all scopes)
            
        Returns:
            Dictionary of variable names and objects
        """
        result: Dict[str, Variable] = {}
        
        if scope:
            # Get from specific scope
            result.update(self._variables[scope])
        else:
            # Get from all scopes (local overrides workflow overrides global)
            if self._parent:
                # Start with parent variables
                result.update(self._parent.get_all_variables())
                
            # Add global variables
            result.update(self._variables[VariableScope.GLOBAL])
                
            # Add workflow variables
            result.update(self._variables[VariableScope.WORKFLOW])
                
            # Add local variables
            result.update(self._variables[VariableScope.LOCAL])
                
        return result
        
    def get_names(self, scope: Optional[VariableScope] = None) -> Set[str]:
        """
        Get all variable names in a scope or all scopes
        
        Args:
            scope: Scope to get variable names from (if None, get from all scopes)
            
        Returns:
            Set of variable names
        """
        if scope:
            # Get from specific scope
            return set(self._variables[scope].keys())
        else:
            # Get from all scopes
            names = set()
            if self._parent:
                names.update(self._parent.get_names())
            for s in VariableScope:
                names.update(self._variables[s].keys())
            return names
            
    def has(self, name: str, scope: Optional[VariableScope] = None) -> bool:
        """
        Check if a variable exists
        
        Args:
            name: Name of the variable
            scope: Scope to check (if None, check all scopes)
            
        Returns:
            True if the variable exists, False otherwise
        """
        if scope:
            # Check specific scope
            return name in self._variables[scope]
        else:
            # Check all scopes
            for s in VariableScope:
                if name in self._variables[s]:
                    return True
            # Check parent if we have one
            if self._parent:
                return self._parent.has(name)
            return False
            
    def get_scope(self, name: str) -> Optional[VariableScope]:
        """
        Get the scope of a variable
        
        Args:
            name: Name of the variable
            
        Returns:
            Scope of the variable or None if not found
        """
        # Check local scope first
        if name in self._variables[VariableScope.LOCAL]:
            return VariableScope.LOCAL
            
        # Then check workflow scope
        if name in self._variables[VariableScope.WORKFLOW]:
            return VariableScope.WORKFLOW
            
        # Then check global scope
        if name in self._variables[VariableScope.GLOBAL]:
            return VariableScope.GLOBAL
            
        # If we have a parent, check there
        if self._parent:
            return self._parent.get_scope(name)
            
        # Not found
        return None
        
    def add_variable_change_listener(self, listener: Callable[[LegacyVariableChangeEvent], None]) -> None:
        """
        Add a listener for variable change events
        
        Args:
            listener: Callback function that will be called when variables change
        """
        if listener not in self._variable_change_listeners:
            self._variable_change_listeners.append(listener)
            
    def remove_variable_change_listener(self, listener: Callable[[LegacyVariableChangeEvent], None]) -> None:
        """
        Remove a variable change listener
        
        Args:
            listener: Listener to remove
        """
        if listener in self._variable_change_listeners:
            self._variable_change_listeners.remove(listener)
            
    def _notify_variable_change(self, event: LegacyVariableChangeEvent) -> None:
        """
        Notify all listeners of a variable change
        
        Args:
            event: Variable change event
        """
        for listener in self._variable_change_listeners:
            try:
                listener(event)
            except Exception as e:
                self.logger.error(f"Error in variable change listener: {str(e)}")
                
    def _on_variable_change(self, event: 'src.core.variables.variable_interface.VariableChangeEvent') -> None:
        """
        Handle variable change events from Variable objects
        
        Args:
            event: Variable change event
        """
        # Convert to legacy event format and notify listeners
        legacy_event = LegacyVariableChangeEvent(
            name=event.variable_name,
            old_value=event.old_value,
            new_value=event.new_value,
            scope=event.scope
        )
        self._notify_variable_change(legacy_event)
                
    def _validate_variable_name(self, name: str) -> None:
        """
        Validate a variable name
        
        Args:
            name: Name to validate
            
        Raises:
            ValueError: If the name is invalid
        """
        if not name:
            raise ValueError("Variable name cannot be empty")
            
        if not self._variable_name_pattern.match(name):
            raise ValueError(
                f"Invalid variable name: {name}. "
                "Variable names must start with a letter or underscore "
                "and contain only letters, numbers, and underscores."
            )
            
    def clone(self) -> 'VariableStorageV2':
        """
        Create a clone of this variable storage
        
        Returns:
            New variable storage with the same variables
        """
        clone = VariableStorageV2(parent=self._parent)
        for scope in VariableScope:
            for name, variable in self._variables[scope].items():
                clone._variables[scope][name] = self._variable_factory.create_from_dict(variable.to_dict())
                clone._variables[scope][name].add_change_listener(clone._on_variable_change)
        return clone
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the variable storage to a dictionary
        
        Returns:
            Dictionary representation of the variable storage
        """
        return {
            "variables": {
                scope.name: {
                    name: variable.to_dict()
                    for name, variable in variables.items()
                }
                for scope, variables in self._variables.items()
            }
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional['VariableStorageV2'] = None) -> 'VariableStorageV2':
        """
        Create a variable storage from a dictionary
        
        Args:
            data: Dictionary representation of the variable storage
            parent: Optional parent storage
            
        Returns:
            Instantiated variable storage
        """
        instance = cls(parent=parent)
        factory = VariableFactory()
        
        variables_data = data.get("variables", {})
        for scope_name, variables in variables_data.items():
            scope = VariableScope[scope_name]
            for name, variable_data in variables.items():
                variable = factory.create_from_dict(variable_data)
                instance._variables[scope][name] = variable
                variable.add_change_listener(instance._on_variable_change)
                
        return instance
        
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
