"""
Error handling utilities for the application.

This module provides utilities for handling errors across the application.
Part of the error handling refactoring to standardize error handling.

SRP-1: Provides error handling utilities
"""
from typing import Optional, Callable, TypeVar, Type, cast
import traceback
from .logging import LoggingMixin

T = TypeVar('T')


class ApplicationError(Exception):
    """Base class for application-specific errors."""

    def __init__(self, message: str, cause: Optional[Exception] = None):
        """
        Initialize the error.

        Args:
            message: Error message
            cause: Optional cause of the error
        """
        super().__init__(message)
        self.cause = cause
        self.traceback = traceback.format_exc() if cause else None


class OperationError(ApplicationError):
    """Error that occurs during an operation."""
    pass


class ValidationError(ApplicationError):
    """Error that occurs during validation."""
    pass


class StorageError(ApplicationError):
    """Error that occurs during storage operations."""
    pass


class ErrorHandlingMixin(LoggingMixin):
    """
    Mixin for standardized error handling.

    Part of the error handling refactoring to standardize
    error handling across the application.

    SRP Analysis: This mixin adds error handling responsibility to classes,
    but since error handling is a cross-cutting concern, it doesn't violate SRP.
    It standardizes how errors are handled without adding business logic.
    """

    def _handle_generic(self, operation_type: str, operation_name: str,
                       error_class: Type[ApplicationError], operation: Callable[..., T],
                       *args, **kwargs) -> T:
        """
        Generic method to handle operations with standardized error handling.

        Args:
            operation_type: Type of operation (e.g., 'operation', 'validation', 'storage')
            operation_name: Name of the operation for error reporting
            error_class: Error class to raise if the operation fails
            operation: Callable to execute
            *args: Arguments to pass to the operation
            **kwargs: Keyword arguments to pass to the operation

        Returns:
            Result of the operation

        Raises:
            ApplicationError: If the operation fails (specific subclass determined by error_class)
        """
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            error_context = f"{operation_type} {operation_name}" if operation_type else operation_name
            self.log_error(f"Error during {error_context}", e)
            raise error_class(f"Error during {error_context}: {str(e)}", e)

    def handle_operation(self, operation_name: str, operation: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute an operation with standardized error handling.

        Args:
            operation_name: Name of the operation for error reporting
            operation: Callable to execute
            *args: Arguments to pass to the operation
            **kwargs: Keyword arguments to pass to the operation

        Returns:
            Result of the operation

        Raises:
            OperationError: If the operation fails
        """
        return self._handle_generic('', operation_name, OperationError, operation, *args, **kwargs)

    def handle_validation(self, validation_name: str, validation: Callable[..., bool], *args, **kwargs) -> bool:
        """
        Execute a validation with standardized error handling.

        Args:
            validation_name: Name of the validation for error reporting
            validation: Callable to execute
            *args: Arguments to pass to the validation
            **kwargs: Keyword arguments to pass to the validation

        Returns:
            Result of the validation

        Raises:
            ValidationError: If the validation fails with an exception
        """
        return cast(bool, self._handle_generic('validation', validation_name, ValidationError, validation, *args, **kwargs))

    def handle_storage(self, storage_name: str, storage_operation: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute a storage operation with standardized error handling.

        Args:
            storage_name: Name of the storage operation for error reporting
            storage_operation: Callable to execute
            *args: Arguments to pass to the storage operation
            **kwargs: Keyword arguments to pass to the storage operation

        Returns:
            Result of the storage operation

        Raises:
            StorageError: If the storage operation fails
        """
        return self._handle_generic('storage operation', storage_name, StorageError, storage_operation, *args, **kwargs)
