"""Type-specific variable implementations"""
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic, Type, cast

from src.core.context.variable_storage import VariableScope
from src.core.variables.variable_interface import VariableType
from src.core.variables.variable import Variable

# Type variables for generic typing
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class StringVariable(Variable[str]):
    """Variable that holds a string value"""

    def __init__(
        self,
        name: str,
        value: Union[str, Any] = "",
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a string variable

        Args:
            name: Variable name
            value: Initial value (will be converted to string if not already)
            scope: Variable scope
            metadata: Optional metadata dictionary
        """
        super().__init__(name, str(value), VariableType.STRING, scope, metadata)

    def is_empty(self) -> bool:
        """
        Check if the string is empty

        Returns:
            True if the string is empty, False otherwise
        """
        return len(self.get_value()) == 0

    def contains(self, substring: str, case_sensitive: bool = True) -> bool:
        """
        Check if the string contains a substring

        Args:
            substring: Substring to check for
            case_sensitive: Whether the check should be case-sensitive

        Returns:
            True if the string contains the substring, False otherwise
        """
        if case_sensitive:
            return substring in self.get_value()
        else:
            return substring.lower() in self.get_value().lower()

    def to_lower(self) -> str:
        """
        Get lowercase version of the string

        Returns:
            Lowercase string
        """
        return self.get_value().lower()

    def to_upper(self) -> str:
        """
        Get uppercase version of the string

        Returns:
            Uppercase string
        """
        return self.get_value().upper()


class NumberVariable(Variable[Union[int, float]]):
    """Variable that holds a numeric value (int or float)"""

    def __init__(
        self,
        name: str,
        value: Union[int, float, str] = 0,
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a number variable

        Args:
            name: Variable name
            value: Initial value (will be converted to number if possible)
            scope: Variable scope
            metadata: Optional metadata dictionary

        Raises:
            ValueError: If the value cannot be converted to a number
        """
        super().__init__(name, value, VariableType.NUMBER, scope, metadata)

    def increment(self, amount: Union[int, float] = 1) -> Union[int, float]:
        """
        Increment the value

        Args:
            amount: Amount to increment by

        Returns:
            New value
        """
        current_value = self.get_value()
        self.set_value(cast(Union[int, float], current_value + amount))
        return self.get_value()

    def decrement(self, amount: Union[int, float] = 1) -> Union[int, float]:
        """
        Decrement the value

        Args:
            amount: Amount to decrement by

        Returns:
            New value
        """
        current_value = self.get_value()
        self.set_value(cast(Union[int, float], current_value - amount))
        return self.get_value()

    def is_integer(self) -> bool:
        """
        Check if the value is an integer

        Returns:
            True if the value is an integer, False if it's a float
        """
        return isinstance(self.get_value(), int)

    def to_int(self) -> int:
        """
        Convert the value to an integer

        Returns:
            Integer value
        """
        return int(self.get_value())

    def to_float(self) -> float:
        """
        Convert the value to a float

        Returns:
            Float value
        """
        return float(self.get_value())


class BooleanVariable(Variable[bool]):
    """Variable that holds a boolean value"""

    def __init__(
        self,
        name: str,
        value: Union[bool, str, int] = False,
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a boolean variable

        Args:
            name: Variable name
            value: Initial value (will be converted to boolean if possible)
            scope: Variable scope
            metadata: Optional metadata dictionary

        Raises:
            ValueError: If the value cannot be converted to a boolean
        """
        super().__init__(name, value, VariableType.BOOLEAN, scope, metadata)

    def toggle(self) -> bool:
        """
        Toggle the boolean value

        Returns:
            New value
        """
        current_value = self.get_value()
        self.set_value(not current_value)
        return self.get_value()


class ListVariable(Variable[List[Any]], Generic[T]):
    """Variable that holds a list of values"""

    def __init__(
        self,
        name: str,
        value: Union[List[T], str] = None,
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None,
        item_type: Optional[Type[T]] = None
    ):
        """
        Initialize a list variable

        Args:
            name: Variable name
            value: Initial value (will be converted to list if possible)
            scope: Variable scope
            metadata: Optional metadata dictionary
            item_type: Optional type for list items (for type checking)

        Raises:
            ValueError: If the value cannot be converted to a list
            TypeError: If any item in the list doesn't match item_type
        """
        # Handle default value
        if value is None:
            value = []

        # Convert to list if needed
        if not isinstance(value, list):
            value = self.convert_value(value)

        # Validate item types if item_type is specified
        if item_type is not None and value:
            for i, item in enumerate(value):
                if not isinstance(item, item_type):
                    try:
                        # Try to convert the item to the correct type
                        value[i] = item_type(item)
                    except (ValueError, TypeError) as e:
                        raise TypeError(f"Item at index {i} is not of type {item_type.__name__}: {str(e)}")

        # Store item_type in metadata
        if metadata is None:
            metadata = {}
        if item_type is not None:
            metadata["item_type"] = item_type.__name__

        super().__init__(name, value, VariableType.LIST, scope, metadata)

    def append(self, item: T) -> None:
        """
        Append an item to the list

        Args:
            item: Item to append

        Raises:
            TypeError: If the item doesn't match the item_type
        """
        # Check if we have an item_type specified in metadata
        item_type_name = self.get_metadata_value("item_type")
        if item_type_name:
            # Get the actual type object
            item_type = globals().get(item_type_name) or __builtins__.get(item_type_name)
            if item_type and not isinstance(item, item_type):
                try:
                    # Try to convert the item to the correct type
                    item = item_type(item)
                except (ValueError, TypeError) as e:
                    raise TypeError(f"Item is not of type {item_type_name}: {str(e)}")

        new_list = self.get_value()
        new_list.append(item)
        self.set_value(new_list)

    def extend(self, items: List[T]) -> None:
        """
        Extend the list with another list

        Args:
            items: Items to add
        """
        new_list = self.get_value()
        new_list.extend(items)
        self.set_value(new_list)

    def remove(self, item: T) -> None:
        """
        Remove an item from the list

        Args:
            item: Item to remove

        Raises:
            ValueError: If the item is not in the list
        """
        new_list = self.get_value()
        new_list.remove(item)
        self.set_value(new_list)

    def clear(self) -> None:
        """Clear the list"""
        self.set_value([])

    def get(self, index: int) -> T:
        """
        Get an item by index

        Args:
            index: Index of the item

        Returns:
            Item at the specified index

        Raises:
            IndexError: If the index is out of range
        """
        return self.get_value()[index]

    def set(self, index: int, item: T) -> None:
        """
        Set an item by index

        Args:
            index: Index of the item
            item: New value for the item

        Raises:
            IndexError: If the index is out of range
        """
        new_list = self.get_value()
        new_list[index] = item
        self.set_value(new_list)

    def length(self) -> int:
        """
        Get the length of the list

        Returns:
            Number of items in the list
        """
        return len(self.get_value())

    def is_empty(self) -> bool:
        """
        Check if the list is empty

        Returns:
            True if the list is empty, False otherwise
        """
        return len(self.get_value()) == 0

    def contains(self, item: T) -> bool:
        """
        Check if the list contains an item

        Args:
            item: Item to check for

        Returns:
            True if the list contains the item, False otherwise
        """
        return item in self.get_value()


class DictionaryVariable(Variable[Dict[K, V]], Generic[K, V]):
    """Variable that holds a dictionary of key-value pairs"""

    def __init__(
        self,
        name: str,
        value: Union[Dict[K, V], str] = None,
        scope: VariableScope = VariableScope.WORKFLOW,
        metadata: Optional[Dict[str, Any]] = None,
        key_type: Optional[Type[K]] = None,
        value_type: Optional[Type[V]] = None
    ):
        """
        Initialize a dictionary variable

        Args:
            name: Variable name
            value: Initial value (will be converted to dictionary if possible)
            scope: Variable scope
            metadata: Optional metadata dictionary
            key_type: Optional type for dictionary keys (for type checking)
            value_type: Optional type for dictionary values (for type checking)

        Raises:
            ValueError: If the value cannot be converted to a dictionary
            TypeError: If any key or value doesn't match the specified types
        """
        # Handle default value
        if value is None:
            value = {}

        # Convert to dictionary if needed
        if not isinstance(value, dict):
            value = self.convert_value(value)

        # Validate key and value types if specified
        if (key_type is not None or value_type is not None) and value:
            validated_dict = {}
            for k, v in value.items():
                # Validate and convert key if needed
                if key_type is not None and not isinstance(k, key_type):
                    try:
                        k = key_type(k)
                    except (ValueError, TypeError) as e:
                        raise TypeError(f"Key '{k}' is not of type {key_type.__name__}: {str(e)}")

                # Validate and convert value if needed
                if value_type is not None and not isinstance(v, value_type):
                    try:
                        v = value_type(v)
                    except (ValueError, TypeError) as e:
                        raise TypeError(f"Value for key '{k}' is not of type {value_type.__name__}: {str(e)}")

                validated_dict[k] = v

            value = validated_dict

        # Store type information in metadata
        if metadata is None:
            metadata = {}
        if key_type is not None:
            metadata["key_type"] = key_type.__name__
        if value_type is not None:
            metadata["value_type"] = value_type.__name__

        super().__init__(name, value, VariableType.DICTIONARY, scope, metadata)

    def get(self, key: K, default: V = None) -> V:
        """
        Get a value by key

        Args:
            key: Dictionary key
            default: Default value if key doesn't exist

        Returns:
            Value for the key or default if not found
        """
        return self.get_value().get(key, default)

    def set(self, key: K, value: V) -> None:
        """
        Set a value by key

        Args:
            key: Dictionary key
            value: Value to set

        Raises:
            TypeError: If the key or value doesn't match the specified types
        """
        # Check if we have type information in metadata
        key_type_name = self.get_metadata_value("key_type")
        value_type_name = self.get_metadata_value("value_type")

        # Validate and convert key if needed
        if key_type_name:
            key_type = globals().get(key_type_name) or __builtins__.get(key_type_name)
            if key_type and not isinstance(key, key_type):
                try:
                    key = key_type(key)
                except (ValueError, TypeError) as e:
                    raise TypeError(f"Key is not of type {key_type_name}: {str(e)}")

        # Validate and convert value if needed
        if value_type_name:
            value_type = globals().get(value_type_name) or __builtins__.get(value_type_name)
            if value_type and not isinstance(value, value_type):
                try:
                    value = value_type(value)
                except (ValueError, TypeError) as e:
                    raise TypeError(f"Value is not of type {value_type_name}: {str(e)}")

        new_dict = self.get_value()
        new_dict[key] = value
        self.set_value(new_dict)

    def remove(self, key: K) -> None:
        """
        Remove a key-value pair

        Args:
            key: Key to remove

        Raises:
            KeyError: If the key doesn't exist
        """
        new_dict = self.get_value()
        del new_dict[key]
        self.set_value(new_dict)

    def clear(self) -> None:
        """Clear the dictionary"""
        self.set_value({})

    def has_key(self, key: K) -> bool:
        """
        Check if the dictionary has a key

        Args:
            key: Key to check for

        Returns:
            True if the key exists, False otherwise
        """
        return key in self.get_value()

    def keys(self) -> List[K]:
        """
        Get all keys

        Returns:
            List of keys
        """
        return list(self.get_value().keys())

    def values(self) -> List[V]:
        """
        Get all values

        Returns:
            List of values
        """
        return list(self.get_value().values())

    def items(self) -> List[tuple[K, V]]:
        """
        Get all key-value pairs

        Returns:
            List of (key, value) tuples
        """
        return list(self.get_value().items())

    def length(self) -> int:
        """
        Get the number of key-value pairs

        Returns:
            Number of items in the dictionary
        """
        return len(self.get_value())

    def is_empty(self) -> bool:
        """
        Check if the dictionary is empty

        Returns:
            True if the dictionary is empty, False otherwise
        """
        return len(self.get_value()) == 0
