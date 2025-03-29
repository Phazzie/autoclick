"""Timeout-related errors for the automation system"""
from typing import Dict, Any, Optional

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity


class TimeoutError(Error):
    """Error raised when an operation times out"""
    
    def __init__(
        self,
        operation: str,
        timeout_seconds: float,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the timeout error
        
        Args:
            operation: Description of the operation that timed out
            timeout_seconds: Timeout duration in seconds
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Create default message if none provided
        if message is None:
            message = f"Operation '{operation}' timed out after {timeout_seconds} seconds"
            
        # Add operation and timeout to details
        details = details or {}
        details["operation"] = operation
        details["timeout_seconds"] = timeout_seconds
        
        super().__init__(
            error_type=ErrorType.TIMEOUT,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )


class WaitTimeoutError(Error):
    """Error raised when waiting for a condition times out"""
    
    def __init__(
        self,
        condition: str,
        timeout_seconds: float,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the wait timeout error
        
        Args:
            condition: Description of the condition being waited for
            timeout_seconds: Timeout duration in seconds
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Create default message if none provided
        if message is None:
            message = f"Waiting for condition '{condition}' timed out after {timeout_seconds} seconds"
            
        # Add condition and timeout to details
        details = details or {}
        details["condition"] = condition
        details["timeout_seconds"] = timeout_seconds
        
        super().__init__(
            error_type=ErrorType.WAIT_TIMEOUT,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )


class PageLoadTimeoutError(Error):
    """Error raised when a page load times out"""
    
    def __init__(
        self,
        url: str,
        timeout_seconds: float,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the page load timeout error
        
        Args:
            url: URL of the page being loaded
            timeout_seconds: Timeout duration in seconds
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Create default message if none provided
        if message is None:
            message = f"Page load for URL '{url}' timed out after {timeout_seconds} seconds"
            
        # Add URL and timeout to details
        details = details or {}
        details["url"] = url
        details["timeout_seconds"] = timeout_seconds
        
        super().__init__(
            error_type=ErrorType.PAGE_LOAD_TIMEOUT,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )
