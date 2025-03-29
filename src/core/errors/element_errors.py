"""Element-related errors for the automation system"""
from typing import Dict, Any, Optional

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity


class ElementNotFoundError(Error):
    """Error raised when an element is not found"""
    
    def __init__(
        self,
        selector: str,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the element not found error
        
        Args:
            selector: Selector used to find the element
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Create default message if none provided
        if message is None:
            message = f"Element not found with selector: {selector}"
            
        # Add selector to details
        details = details or {}
        details["selector"] = selector
        
        super().__init__(
            error_type=ErrorType.ELEMENT_NOT_FOUND,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )


class ElementNotVisibleError(Error):
    """Error raised when an element is found but not visible"""
    
    def __init__(
        self,
        selector: str,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the element not visible error
        
        Args:
            selector: Selector used to find the element
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Create default message if none provided
        if message is None:
            message = f"Element found but not visible with selector: {selector}"
            
        # Add selector to details
        details = details or {}
        details["selector"] = selector
        
        super().__init__(
            error_type=ErrorType.ELEMENT_NOT_VISIBLE,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )


class ElementNotClickableError(Error):
    """Error raised when an element is found but not clickable"""
    
    def __init__(
        self,
        selector: str,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the element not clickable error
        
        Args:
            selector: Selector used to find the element
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Create default message if none provided
        if message is None:
            message = f"Element found but not clickable with selector: {selector}"
            
        # Add selector to details
        details = details or {}
        details["selector"] = selector
        
        super().__init__(
            error_type=ErrorType.ELEMENT_NOT_CLICKABLE,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )


class ElementStaleError(Error):
    """Error raised when an element reference is stale"""
    
    def __init__(
        self,
        selector: str,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the element stale error
        
        Args:
            selector: Selector used to find the element
            message: Human-readable error message
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
        """
        # Create default message if none provided
        if message is None:
            message = f"Element reference is stale for selector: {selector}"
            
        # Add selector to details
        details = details or {}
        details["selector"] = selector
        
        super().__init__(
            error_type=ErrorType.ELEMENT_STALE,
            message=message,
            severity=ErrorSeverity.ERROR,
            details=details,
            source=source,
            exception=exception
        )
