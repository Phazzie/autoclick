"""
Serialization utilities for the application.

This module provides utilities for serializing and deserializing objects.
Part of the model serialization refactoring to standardize data persistence.

SRP-1: Provides serialization utilities
"""
from typing import Dict, List, Any, TypeVar, Type, Generic, Protocol, runtime_checkable

T = TypeVar('T')


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate that required fields are present in the data.

    Args:
        data: Dictionary to validate
        required_fields: List of required field names

    Raises:
        ValueError: If any required fields are missing
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")


@runtime_checkable
class Serializable(Protocol):
    """Protocol defining serializable objects."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary."""
        ...

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serializable':
        """Create object from dictionary."""
        ...

class SerializableMixin:
    """
    Mixin for serializable objects.

    Part of the model serialization refactoring to standardize
    data persistence across the application.

    SRP Analysis: This mixin adds serialization responsibility to model classes,
    temporarily increasing SRP violations. In future refactoring phases, this
    responsibility will be extracted to dedicated serializer classes.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the object to a dictionary.

        Returns:
            Dictionary representation of the object
        """
        # Implementation specific to each class
        raise NotImplementedError("Subclasses must implement to_dict()")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SerializableMixin':
        """
        Create an object from a dictionary.

        Args:
            data: Dictionary representation of the object

        Returns:
            New instance of the class

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Implementation specific to each class
        raise NotImplementedError("Subclasses must implement from_dict()")

    @classmethod
    def validate_required_fields(cls, data: Dict[str, Any], required_fields: List[str]) -> None:
        """
        Validate that required fields are present in the data.

        Args:
            data: Dictionary to validate
            required_fields: List of required field names

        Raises:
            ValueError: If any required fields are missing
        """
        validate_required_fields(data, required_fields)


class Serializer(Generic[T]):
    """
    Generic serializer for objects.

    This class provides a way to serialize and deserialize objects
    without modifying the objects themselves. This is the target pattern
    for future refactoring to extract serialization responsibility from model classes.
    """

    def __init__(self, cls: Type[T]):
        """
        Initialize the serializer.

        Args:
            cls: The class this serializer handles
        """
        self.cls = cls

    def to_dict(self, obj: T) -> Dict[str, Any]:
        """
        Convert an object to a dictionary.

        Args:
            obj: Object to convert

        Returns:
            Dictionary representation of the object
        """
        # Implementation specific to each serializer
        raise NotImplementedError("Subclasses must implement to_dict()")

    def from_dict(self, data: Dict[str, Any]) -> T:
        """
        Create an object from a dictionary.

        Args:
            data: Dictionary representation of the object

        Returns:
            New instance of the class

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Implementation specific to each serializer
        raise NotImplementedError("Subclasses must implement from_dict()")

    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> None:
        """
        Validate that required fields are present in the data.

        Args:
            data: Dictionary to validate
            required_fields: List of required field names

        Raises:
            ValueError: If any required fields are missing
        """
        validate_required_fields(data, required_fields)