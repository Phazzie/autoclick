"""Interface for variable access and manipulation"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, Generic, TypeVar, Type, Callable, Optional, List, Union

from src.core.context.variable_storage import VariableScope

# Type variable for generic typing
T = TypeVar('T')


class VariableType(Enum):
    """Enumeration of variable types"""
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    LIST = auto()
    DICTIONARY = auto()
    OBJECT = auto()
    ANY = auto()

    @classmethod
    def from_python_type(cls, py_type: Type) -> 'VariableType':
        """
        Convert a Python type to a VariableType

        Args:
            py_type: Python type to convert

        Returns:
            Corresponding VariableType
        """
        if py_type == str:
            return cls.STRING
        elif py_type in (int, float):
            return cls.NUMBER
        elif py_type == bool:
            return cls.BOOLEAN
        elif py_type == list:
            return cls.LIST
        elif py_type == dict:
            return cls.DICTIONARY
        elif py_type == object:
            return cls.OBJECT
        else:
            return cls.ANY


class VariableChangeEvent:
    """Event fired when a variable changes"""

    def __init__(
        self,
        variable_name: str,
        old_value: Any,
        new_value: Any,
        scope: VariableScope,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a variable change event

        Args:
            variable_name: Name of the variable that changed
            old_value: Previous value of the variable
            new_value: New value of the variable
            scope: Scope of the variable
            timestamp: Time of the change (defaults to now)
        """
        self.variable_name = variable_name
        self.old_value = old_value
        self.new_value = new_value
        self.scope = scope
        self.timestamp = timestamp or datetime.now()

    def __str__(self) -> str:
        """String representation of the event"""
        return (f"VariableChangeEvent: {self.variable_name} in {self.scope.name} "
                f"changed from {self.old_value} to {self.new_value} at {self.timestamp}")


class IValueHolder(Generic[T], ABC):
    """Interface for getting and setting values"""

    @abstractmethod
    def get_value(self) -> T:
        """
        Get the variable value

        Returns:
            Current value
        """
        pass

    @abstractmethod
    def set_value(self, new_value: T) -> None:
        """
        Set the variable value

        Args:
            new_value: New value for the variable

        Raises:
            ValueError: If the value is invalid
        """
        pass


class ITyped(ABC):
    """Interface for type information and validation"""

    @abstractmethod
    def get_type(self) -> VariableType:
        """
        Get the variable type

        Returns:
            Variable type
        """
        pass

    @abstractmethod
    def is_valid_value(self, value: Any) -> bool:
        """
        Check if a value is valid for this variable

        Args:
            value: Value to check

        Returns:
            True if the value is valid, False otherwise
        """
        pass

    @abstractmethod
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
        pass


class IObservable(ABC):
    """Interface for change notification"""

    @abstractmethod
    def add_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Add a listener for variable changes

        Args:
            listener: Callback function that will be called when the variable changes
        """
        pass

    @abstractmethod
    def remove_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Remove a listener for variable changes

        Args:
            listener: Callback function to remove
        """
        pass


class ISerializable(ABC):
    """Interface for serialization"""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert variable to dictionary for serialization

        Returns:
            Dictionary representation of the variable
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ISerializable':
        """
        Create variable from dictionary

        Args:
            data: Dictionary representation of the variable

        Returns:
            Instantiated variable

        Raises:
            ValueError: If the dictionary is invalid
        """
        pass


class IMetadata(ABC):
    """Interface for metadata operations"""

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get all metadata

        Returns:
            Dictionary of metadata
        """
        pass

    @abstractmethod
    def get_metadata_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific metadata value

        Args:
            key: Metadata key
            default: Default value if key doesn't exist

        Returns:
            Metadata value or default
        """
        pass

    @abstractmethod
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set a metadata value

        Args:
            key: Metadata key
            value: Metadata value
        """
        pass


class IVariable(IValueHolder[T], ITyped, IObservable, ISerializable, IMetadata, Generic[T], ABC):
    """Combined interface for variables"""

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the variable name

        Returns:
            Variable name
        """
        pass

    @abstractmethod
    def get_scope(self) -> VariableScope:
        """
        Get the variable scope

        Returns:
            Variable scope
        """
        pass


class VariableInterface(Generic[T], ABC):
    """Legacy interface for variable access and manipulation"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the variable name"""
        pass

    @property
    @abstractmethod
    def type(self) -> VariableType:
        """Get the variable type"""
        pass

    @property
    @abstractmethod
    def scope(self) -> VariableScope:
        """Get the variable scope"""
        pass

    @property
    @abstractmethod
    def value(self) -> T:
        """Get the variable value"""
        pass

    @value.setter
    @abstractmethod
    def value(self, new_value: T) -> None:
        """Set the variable value"""
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get variable metadata

        Returns:
            Dictionary of metadata
        """
        pass

    @abstractmethod
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set variable metadata

        Args:
            key: Metadata key
            value: Metadata value
        """
        pass

    @abstractmethod
    def add_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Add a listener for variable changes

        Args:
            listener: Callback function that will be called when the variable changes
        """
        pass

    @abstractmethod
    def remove_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Remove a listener for variable changes

        Args:
            listener: Callback function to remove
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert variable to dictionary for serialization

        Returns:
            Dictionary representation of the variable
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VariableInterface':
        """
        Create variable from dictionary

        Args:
            data: Dictionary representation of the variable

        Returns:
            Instantiated variable
        """
        pass


class TypeValidator:
    """Validates and converts variable values based on type"""

    @staticmethod
    def validate(value: Any, var_type: VariableType) -> bool:
        """
        Validate that a value matches the specified type

        Args:
            value: Value to validate
            var_type: Expected variable type

        Returns:
            True if the value matches the type, False otherwise
        """
        if var_type == VariableType.ANY:
            return True

        if var_type == VariableType.STRING:
            return isinstance(value, str)

        if var_type == VariableType.NUMBER:
            return isinstance(value, (int, float)) and not isinstance(value, bool)

        if var_type == VariableType.BOOLEAN:
            return isinstance(value, bool)

        if var_type == VariableType.LIST:
            return isinstance(value, list)

        if var_type == VariableType.DICTIONARY:
            return isinstance(value, dict)

        if var_type == VariableType.OBJECT:
            return isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict))

        return False

    @staticmethod
    def convert(value: Any, var_type: VariableType) -> Any:
        """
        Convert a value to the specified type if possible

        Args:
            value: Value to convert
            var_type: Target variable type

        Returns:
            Converted value

        Raises:
            ValueError: If the value cannot be converted to the specified type
        """
        # If the value is already the correct type, return it
        if TypeValidator.validate(value, var_type):
            return value

        # Handle conversions
        if var_type == VariableType.STRING:
            return str(value)

        if var_type == VariableType.NUMBER:
            if isinstance(value, str):
                try:
                    # Try to convert to int first, then float if that fails
                    try:
                        return int(value)
                    except ValueError:
                        return float(value)
                except ValueError:
                    raise ValueError(f"Cannot convert '{value}' to a number")
            elif isinstance(value, bool):
                return 1 if value else 0
            else:
                raise ValueError(f"Cannot convert {type(value).__name__} to a number")

        if var_type == VariableType.BOOLEAN:
            if isinstance(value, str):
                lower_value = value.lower()
                if lower_value in ('true', 'yes', '1', 'y'):
                    return True
                elif lower_value in ('false', 'no', '0', 'n'):
                    return False
                else:
                    raise ValueError(f"Cannot convert string '{value}' to a boolean")
            elif isinstance(value, (int, float)):
                return bool(value)
            else:
                raise ValueError(f"Cannot convert {type(value).__name__} to a boolean")

        if var_type == VariableType.LIST:
            if isinstance(value, str):
                # Try to interpret as JSON
                import json
                try:
                    result = json.loads(value)
                    if isinstance(result, list):
                        return result
                    else:
                        return [result]
                except json.JSONDecodeError:
                    # If not valid JSON, split by commas
                    return [item.strip() for item in value.split(',')]
            else:
                # Try to convert to a list if possible
                try:
                    return list(value)
                except:
                    raise ValueError(f"Cannot convert {type(value).__name__} to a list")

        if var_type == VariableType.DICTIONARY:
            if isinstance(value, str):
                # Try to interpret as JSON
                import json
                try:
                    result = json.loads(value)
                    if isinstance(result, dict):
                        return result
                    else:
                        raise ValueError(f"JSON does not represent a dictionary: {value}")
                except json.JSONDecodeError:
                    raise ValueError(f"Cannot convert string to a dictionary: {value}")
            else:
                raise ValueError(f"Cannot convert {type(value).__name__} to a dictionary")

        if var_type == VariableType.ANY:
            return value

        raise ValueError(f"Conversion to {var_type.name} is not supported")
