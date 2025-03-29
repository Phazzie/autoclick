"""Error types for the automation system"""
from enum import Enum, auto
from datetime import datetime
from typing import Dict, Any, Optional


class ErrorType(Enum):
    """Types of errors that can occur in the automation system"""
    
    # Element-related errors
    ELEMENT_NOT_FOUND = auto()
    ELEMENT_NOT_VISIBLE = auto()
    ELEMENT_NOT_CLICKABLE = auto()
    ELEMENT_STALE = auto()
    
    # Navigation errors
    NAVIGATION_ERROR = auto()
    PAGE_LOAD_TIMEOUT = auto()
    REDIRECT_ERROR = auto()
    
    # Timeout errors
    TIMEOUT = auto()
    WAIT_TIMEOUT = auto()
    
    # JavaScript errors
    JAVASCRIPT_ERROR = auto()
    SCRIPT_EXECUTION_ERROR = auto()
    
    # Authentication errors
    AUTHENTICATION_ERROR = auto()
    AUTHORIZATION_ERROR = auto()
    
    # Network errors
    NETWORK_ERROR = auto()
    CONNECTION_ERROR = auto()
    REQUEST_ERROR = auto()
    
    # Data errors
    DATA_ERROR = auto()
    VALIDATION_ERROR = auto()
    PARSING_ERROR = auto()
    
    # Workflow errors
    WORKFLOW_ERROR = auto()
    ACTION_ERROR = auto()
    CONDITION_ERROR = auto()
    
    # System errors
    SYSTEM_ERROR = auto()
    RESOURCE_ERROR = auto()
    
    # Unknown error
    UNKNOWN = auto()


class ErrorSeverity(Enum):
    """Severity levels for errors"""
    
    # Informational - not an error but worth noting
    INFO = auto()
    
    # Warning - not fatal but indicates a potential issue
    WARNING = auto()
    
    # Error - operation failed but workflow can continue
    ERROR = auto()
    
    # Critical - operation failed and workflow should stop
    CRITICAL = auto()
    
    # Fatal - system-level error requiring immediate attention
    FATAL = auto()


class Error:
    """Represents an error in the automation system"""
    
    def __init__(
        self,
        error_type: ErrorType,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ):
        """
        Initialize the error
        
        Args:
            error_type: Type of the error
            message: Human-readable error message
            severity: Severity level of the error
            details: Additional details about the error
            source: Source of the error (e.g., component name)
            exception: Original exception if this error wraps an exception
        """
        self.error_type = error_type
        self.message = message
        self.severity = severity
        self.details = details or {}
        self.source = source
        self.exception = exception
        self.timestamp = datetime.now()
        
    def __str__(self) -> str:
        """String representation of the error"""
        return f"{self.error_type.name}: {self.message} ({self.severity.name})"
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error to a dictionary
        
        Returns:
            Dictionary representation of the error
        """
        return {
            "type": self.error_type.name,
            "message": self.message,
            "severity": self.severity.name,
            "details": self.details,
            "source": self.source,
            "exception": str(self.exception) if self.exception else None,
            "timestamp": self.timestamp.isoformat()
        }
        
    @classmethod
    def from_exception(
        cls,
        exception: Exception,
        error_type: ErrorType = ErrorType.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        source: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> 'Error':
        """
        Create an error from an exception
        
        Args:
            exception: Exception to convert
            error_type: Type of the error
            severity: Severity level of the error
            source: Source of the error
            details: Additional details about the error
            
        Returns:
            Error instance
        """
        return cls(
            error_type=error_type,
            message=str(exception),
            severity=severity,
            details=details or {},
            source=source,
            exception=exception
        )
