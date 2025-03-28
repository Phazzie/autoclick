"""Error type definitions for the application"""
from enum import Enum, auto
from typing import Dict, Any, Optional


class ErrorSeverity(Enum):
    """Severity levels for errors"""
    INFO = auto()       # Informational, not an error but worth noting
    WARNING = auto()    # Warning, operation can continue but with caution
    ERROR = auto()      # Error, operation failed but system can continue
    CRITICAL = auto()   # Critical, system may need to shut down or restart


class ErrorCategory(Enum):
    """Categories of errors that can occur in the application"""
    # Input/Output errors
    FILE_IO = auto()           # File read/write errors
    NETWORK = auto()           # Network connectivity issues
    DATABASE = auto()          # Database access errors
    
    # UI/Browser errors
    ELEMENT_NOT_FOUND = auto() # Element not found in the DOM
    ELEMENT_STALE = auto()     # Element reference is stale
    NAVIGATION = auto()        # Navigation errors
    TIMEOUT = auto()           # Operation timed out
    
    # Workflow errors
    VALIDATION = auto()        # Input validation errors
    EXECUTION = auto()         # Workflow execution errors
    CONDITION = auto()         # Condition evaluation errors
    VARIABLE = auto()          # Variable access or manipulation errors
    
    # System errors
    CONFIGURATION = auto()     # Configuration errors
    RESOURCE = auto()          # Resource allocation/access errors
    PERMISSION = auto()        # Permission/authorization errors
    
    # Other
    UNKNOWN = auto()           # Unknown or unclassified errors


class ErrorContext:
    """
    Context information for an error
    
    This class holds detailed information about an error, including
    the error message, category, severity, and any additional context
    that might be useful for debugging or recovery.
    """
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        exception: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
        recoverable: bool = True
    ):
        """
        Initialize the error context
        
        Args:
            message: Human-readable error message
            category: Category of the error
            severity: Severity level of the error
            exception: Original exception that caused this error, if any
            context: Additional context information as key-value pairs
            recoverable: Whether this error is potentially recoverable
        """
        self.message = message
        self.category = category
        self.severity = severity
        self.exception = exception
        self.context = context or {}
        self.recoverable = recoverable
        self.timestamp = None  # Will be set when the error occurs
        
    def __str__(self) -> str:
        """String representation of the error context"""
        return (
            f"{self.severity.name} [{self.category.name}]: {self.message}"
            f"{' (Recoverable)' if self.recoverable else ' (Non-recoverable)'}"
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the error context to a dictionary"""
        return {
            "message": self.message,
            "category": self.category.name,
            "severity": self.severity.name,
            "exception": str(self.exception) if self.exception else None,
            "context": self.context,
            "recoverable": self.recoverable,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
        
    @classmethod
    def from_exception(
        cls,
        exception: Exception,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: Optional[Dict[str, Any]] = None,
        recoverable: bool = True
    ) -> 'ErrorContext':
        """
        Create an error context from an exception
        
        Args:
            exception: The exception to create the context from
            category: Category of the error
            severity: Severity level of the error
            context: Additional context information
            recoverable: Whether this error is potentially recoverable
            
        Returns:
            An ErrorContext instance
        """
        return cls(
            message=str(exception),
            category=category,
            severity=severity,
            exception=exception,
            context=context,
            recoverable=recoverable
        )
