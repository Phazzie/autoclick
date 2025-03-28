"""Variable storage for the execution context"""
import copy
import re
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Callable, Union, Set, Tuple


class VariableScope(Enum):
    """Enumeration of variable scopes"""
    GLOBAL = auto()    # Variables available to all contexts
    WORKFLOW = auto()  # Variables available to the current workflow
    LOCAL = auto()     # Variables available only to the current context


class VariableChangeEvent:
    """Event raised when a variable changes"""

    def __init__(self, name: str, old_value: Any, new_value: Any, scope: VariableScope):
        """
        Initialize the variable change event

        Args:
            name: Name of the variable
            old_value: Previous value (None if variable is new)
            new_value: New value
            scope: Scope of the variable
        """
        self.name = name
        self.old_value = old_value
        self.new_value = new_value
        self.scope = scope

    def __str__(self) -> str:
        """String representation of the variable change event"""
        return f"VariableChangeEvent: {self.scope.name}.{self.name} = {self.new_value}"


class VariableStorage:
    """Storage for variables with scoping"""

    def __init__(self, parent: Optional['VariableStorage'] = None):
        """
        Initialize the variable storage

        Args:
            parent: Optional parent storage for variable inheritance
        """
        self._variables: Dict[VariableScope, Dict[str, Any]] = {
            VariableScope.GLOBAL: {},
            VariableScope.WORKFLOW: {},
            VariableScope.LOCAL: {}
        }
        self._parent = parent
        self._variable_change_listeners: List[Callable[[VariableChangeEvent], None]] = []
        self._variable_name_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    def get(self, name: str, default: Any = None) -> Any:
        """
        Get a variable value

        Args:
            name: Name of the variable
            default: Default value if variable doesn't exist

        Returns:
            Variable value or default if not found
        """
        # Check local scope first
        if name in self._variables[VariableScope.LOCAL]:
            return copy.deepcopy(self._variables[VariableScope.LOCAL][name])

        # Then check workflow scope
        if name in self._variables[VariableScope.WORKFLOW]:
            return copy.deepcopy(self._variables[VariableScope.WORKFLOW][name])

        # Then check global scope
        if name in self._variables[VariableScope.GLOBAL]:
            return copy.deepcopy(self._variables[VariableScope.GLOBAL][name])

        # If we have a parent, check there
        if self._parent:
            return self._parent.get(name, default)

        # Not found, return default
        return default

    def set(self, name: str, value: Any, scope: VariableScope = VariableScope.WORKFLOW) -> None:
        """
        Set a variable value

        Args:
            name: Name of the variable
            value: Value to set
            scope: Scope of the variable

        Raises:
            ValueError: If the variable name is invalid
        """
        self._validate_variable_name(name)

        # Get the old value (if any)
        old_value = None
        if name in self._variables[scope]:
            old_value = self._variables[scope][name]

        # Set the new value (make a deep copy to prevent modification)
        self._variables[scope][name] = copy.deepcopy(value)

        # Notify listeners
        self._notify_variable_change(VariableChangeEvent(name, old_value, value, scope))

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
                old_value = self._variables[scope][name]
                del self._variables[scope][name]
                self._notify_variable_change(VariableChangeEvent(name, old_value, None, scope))
                deleted = True
        else:
            # Delete from all scopes
            for s in VariableScope:
                if name in self._variables[s]:
                    old_value = self._variables[s][name]
                    del self._variables[s][name]
                    self._notify_variable_change(VariableChangeEvent(name, old_value, None, s))
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
        for name, old_value in variables:
            self._notify_variable_change(VariableChangeEvent(name, old_value, None, scope))

    def clear_all(self) -> None:
        """Clear all variables in all scopes"""
        for scope in VariableScope:
            self.clear_scope(scope)

    def get_all(self, scope: Optional[VariableScope] = None) -> Dict[str, Any]:
        """
        Get all variables in a scope or all scopes

        Args:
            scope: Scope to get variables from (if None, get from all scopes)

        Returns:
            Dictionary of variable names and values
        """
        result: Dict[str, Any] = {}

        if scope:
            # Get from specific scope
            result.update(copy.deepcopy(self._variables[scope]))
        else:
            # Get from all scopes (local overrides workflow overrides global)
            if self._parent:
                # Start with parent variables
                result.update(self._parent.get_all())

            # Add global variables
            result.update(copy.deepcopy(self._variables[VariableScope.GLOBAL]))

            # Add workflow variables
            result.update(copy.deepcopy(self._variables[VariableScope.WORKFLOW]))

            # Add local variables
            result.update(copy.deepcopy(self._variables[VariableScope.LOCAL]))

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

    def add_variable_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Add a listener for variable change events

        Args:
            listener: Callback function that will be called when variables change
        """
        if listener not in self._variable_change_listeners:
            self._variable_change_listeners.append(listener)

    def remove_variable_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Remove a variable change listener

        Args:
            listener: Listener to remove
        """
        if listener in self._variable_change_listeners:
            self._variable_change_listeners.remove(listener)

    def _notify_variable_change(self, event: VariableChangeEvent) -> None:
        """
        Notify all listeners of a variable change

        Args:
            event: Variable change event
        """
        for listener in self._variable_change_listeners:
            try:
                listener(event)
            except Exception as e:
                # In a real application, you might want to log this error
                print(f"Error in variable change listener: {str(e)}")

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

    def clone(self) -> 'VariableStorage':
        """
        Create a clone of this variable storage

        Returns:
            New variable storage with the same variables
        """
        clone = VariableStorage(parent=self._parent)
        for scope in VariableScope:
            clone._variables[scope] = copy.deepcopy(self._variables[scope])
        return clone

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the variable storage to a dictionary

        Returns:
            Dictionary representation of the variable storage
        """
        return {
            "variables": {
                scope.name: copy.deepcopy(variables)
                for scope, variables in self._variables.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional['VariableStorage'] = None) -> 'VariableStorage':
        """
        Create a variable storage from a dictionary

        Args:
            data: Dictionary representation of the variable storage
            parent: Optional parent storage

        Returns:
            Instantiated variable storage
        """
        instance = cls(parent=parent)

        variables_data = data.get("variables", {})
        for scope_name, variables in variables_data.items():
            scope = VariableScope[scope_name]
            instance._variables[scope] = copy.deepcopy(variables)

        return instance
