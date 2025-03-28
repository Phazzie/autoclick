"""Utilities for serialization and deserialization"""
import json
from typing import Dict, Any, List, Optional, Union, Type, TypeVar, Generic, Callable
import logging
from datetime import datetime, date
import uuid
import re

T = TypeVar('T')


class SerializationUtils:
    """Utility functions for serialization and deserialization"""

    @staticmethod
    def serialize_datetime(dt: datetime) -> str:
        """
        Serialize a datetime object to ISO format string

        Args:
            dt: Datetime object to serialize

        Returns:
            ISO format string
        """
        return dt.isoformat()

    @staticmethod
    def deserialize_datetime(dt_str: str) -> datetime:
        """
        Deserialize an ISO format string to a datetime object

        Args:
            dt_str: ISO format string to deserialize

        Returns:
            Datetime object

        Raises:
            ValueError: If the string is not a valid ISO format
        """
        return datetime.fromisoformat(dt_str)

    @staticmethod
    def serialize_date(d: date) -> str:
        """
        Serialize a date object to ISO format string

        Args:
            d: Date object to serialize

        Returns:
            ISO format string
        """
        return d.isoformat()

    @staticmethod
    def deserialize_date(d_str: str) -> date:
        """
        Deserialize an ISO format string to a date object

        Args:
            d_str: ISO format string to deserialize

        Returns:
            Date object

        Raises:
            ValueError: If the string is not a valid ISO format
        """
        return date.fromisoformat(d_str)

    @staticmethod
    def is_valid_uuid(uuid_str: str) -> bool:
        """
        Check if a string is a valid UUID

        Args:
            uuid_str: String to check

        Returns:
            True if the string is a valid UUID, False otherwise
        """
        try:
            uuid_obj = uuid.UUID(uuid_str)
            return str(uuid_obj) == uuid_str
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def is_valid_iso_datetime(dt_str: str) -> bool:
        """
        Check if a string is a valid ISO datetime format

        Args:
            dt_str: String to check

        Returns:
            True if the string is a valid ISO datetime, False otherwise
        """
        try:
            datetime.fromisoformat(dt_str)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_iso_date(d_str: str) -> bool:
        """
        Check if a string is a valid ISO date format

        Args:
            d_str: String to check

        Returns:
            True if the string is a valid ISO date, False otherwise
        """
        try:
            date.fromisoformat(d_str)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_serialized_object(
        obj: Dict[str, Any],
        required_fields: List[str],
        optional_fields: Optional[List[str]] = None
    ) -> bool:
        """
        Validate a serialized object against required and optional fields

        Args:
            obj: Object to validate
            required_fields: List of required field names
            optional_fields: Optional list of optional field names

        Returns:
            True if the object is valid, False otherwise
        """
        if not isinstance(obj, dict):
            return False

        # Check required fields
        for field in required_fields:
            if field not in obj:
                return False

        # Check that all fields are either required or optional
        if optional_fields:
            allowed_fields = set(required_fields + optional_fields)
            for field in obj:
                if field not in allowed_fields:
                    return False

        return True


class VersionedSerializer(Generic[T]):
    """
    Base class for versioned serializers

    This class provides a framework for serializing and deserializing objects
    with version compatibility.
    """

    def __init__(self) -> None:
        """Initialize the versioned serializer"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._serializers: Dict[str, Callable[[T], Dict[str, Any]]] = {}
        self._deserializers: Dict[str, Callable[[Dict[str, Any]], T]] = {}
        self._current_version = "1.0.0"

    def register_serializer(
        self,
        version: str,
        serializer: Callable[[T], Dict[str, Any]]
    ) -> None:
        """
        Register a serializer for a specific version

        Args:
            version: Version string
            serializer: Function that converts an object to a dictionary
        """
        self._serializers[version] = serializer

    def register_deserializer(
        self,
        version: str,
        deserializer: Callable[[Dict[str, Any]], T]
    ) -> None:
        """
        Register a deserializer for a specific version

        Args:
            version: Version string
            deserializer: Function that converts a dictionary to an object
        """
        self._deserializers[version] = deserializer

    def set_current_version(self, version: str) -> None:
        """
        Set the current version

        Args:
            version: Version string
        """
        if version not in self._serializers:
            raise ValueError(f"No serializer registered for version {version}")
        if version not in self._deserializers:
            raise ValueError(f"No deserializer registered for version {version}")
        self._current_version = version

    def serialize(self, obj: T, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Serialize an object to a dictionary

        Args:
            obj: Object to serialize
            version: Optional version to use (defaults to current version)

        Returns:
            Dictionary representation of the object

        Raises:
            ValueError: If no serializer is registered for the version
        """
        version = version or self._current_version
        if version not in self._serializers:
            raise ValueError(f"No serializer registered for version {version}")

        serializer = self._serializers[version]
        result = serializer(obj)
        result["_version"] = version
        return result

    def deserialize(self, data: Dict[str, Any]) -> T:
        """
        Deserialize a dictionary to an object

        Args:
            data: Dictionary to deserialize

        Returns:
            Deserialized object

        Raises:
            ValueError: If no deserializer is registered for the version
        """
        version = data.get("_version", self._current_version)
        if version not in self._deserializers:
            raise ValueError(f"No deserializer registered for version {version}")

        deserializer = self._deserializers[version]
        return deserializer(data)
