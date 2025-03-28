"""Recovery strategies for handling errors"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable, TypeVar, Generic

from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity


# Type variable for the result of recovery
T = TypeVar('T')


class RecoveryResult(Generic[T]):
    """Result of a recovery attempt"""
    
    def __init__(
        self,
        success: bool,
        message: str,
        result: Optional[T] = None,
        new_error: Optional[ErrorContext] = None
    ):
        """
        Initialize the recovery result
        
        Args:
            success: Whether the recovery was successful
            message: Message describing the recovery result
            result: Result of the recovery, if successful
            new_error: New error that occurred during recovery, if any
        """
        self.success = success
        self.message = message
        self.result = result
        self.new_error = new_error
        
    @classmethod
    def success_result(cls, message: str, result: Optional[T] = None) -> 'RecoveryResult[T]':
        """
        Create a successful recovery result
        
        Args:
            message: Success message
            result: Result of the recovery
            
        Returns:
            A successful RecoveryResult
        """
        return cls(True, message, result)
        
    @classmethod
    def failure_result(
        cls,
        message: str,
        new_error: Optional[ErrorContext] = None
    ) -> 'RecoveryResult[T]':
        """
        Create a failed recovery result
        
        Args:
            message: Failure message
            new_error: New error that occurred during recovery, if any
            
        Returns:
            A failed RecoveryResult
        """
        return cls(False, message, None, new_error)


class RecoveryStrategy(Generic[T], ABC):
    """
    Abstract base class for recovery strategies
    
    A recovery strategy defines how to recover from a specific type of error.
    Subclasses must implement the can_recover and recover methods.
    """
    
    @abstractmethod
    def can_recover(self, error_context: ErrorContext) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error_context: The error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        pass
        
    @abstractmethod
    def recover(self, error_context: ErrorContext, context: Dict[str, Any]) -> RecoveryResult[T]:
        """
        Attempt to recover from the error
        
        Args:
            error_context: The error to recover from
            context: Additional context for recovery
            
        Returns:
            Result of the recovery attempt
        """
        pass


class RetryStrategy(RecoveryStrategy[T]):
    """
    Strategy that retries the operation that failed
    
    This strategy retries the operation a specified number of times,
    with an optional delay between retries.
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        delay_seconds: float = 1.0,
        backoff_factor: float = 2.0,
        applicable_categories: Optional[List[ErrorCategory]] = None,
        operation_factory: Optional[Callable[[], Callable[..., T]]] = None
    ):
        """
        Initialize the retry strategy
        
        Args:
            max_retries: Maximum number of retry attempts
            delay_seconds: Delay between retries in seconds
            backoff_factor: Factor to increase delay by after each retry
            applicable_categories: Categories of errors this strategy can handle
            operation_factory: Factory function to create the operation to retry
        """
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
        self.backoff_factor = backoff_factor
        self.applicable_categories = applicable_categories or [
            ErrorCategory.NETWORK,
            ErrorCategory.TIMEOUT,
            ErrorCategory.ELEMENT_NOT_FOUND,
            ErrorCategory.ELEMENT_STALE
        ]
        self.operation_factory = operation_factory
        
    def can_recover(self, error_context: ErrorContext) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error_context: The error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        # Check if the error is recoverable and in an applicable category
        return (
            error_context.recoverable and
            error_context.category in self.applicable_categories and
            error_context.severity != ErrorSeverity.CRITICAL
        )
        
    def recover(self, error_context: ErrorContext, context: Dict[str, Any]) -> RecoveryResult[T]:
        """
        Attempt to recover by retrying the operation
        
        Args:
            error_context: The error to recover from
            context: Additional context for recovery
            
        Returns:
            Result of the recovery attempt
        """
        if not self.operation_factory:
            return RecoveryResult.failure_result(
                "No operation factory provided for retry strategy"
            )
            
        # Get the operation to retry
        operation = self.operation_factory()
        if not operation:
            return RecoveryResult.failure_result(
                "Failed to create operation for retry"
            )
            
        # Get operation arguments from context
        args = context.get("args", [])
        kwargs = context.get("kwargs", {})
        
        # Try to execute the operation with retries
        import time
        
        current_delay = self.delay_seconds
        last_error = error_context
        
        for attempt in range(self.max_retries):
            try:
                # Wait before retrying
                if attempt > 0:
                    time.sleep(current_delay)
                    current_delay *= self.backoff_factor
                
                # Execute the operation
                result = operation(*args, **kwargs)
                
                # If we get here, the operation succeeded
                return RecoveryResult.success_result(
                    f"Operation succeeded after {attempt + 1} attempts",
                    result
                )
                
            except Exception as e:
                # Create a new error context for this attempt
                last_error = ErrorContext.from_exception(
                    e,
                    category=error_context.category,
                    severity=error_context.severity,
                    context={
                        **error_context.context,
                        "retry_attempt": attempt + 1
                    },
                    recoverable=attempt < self.max_retries - 1
                )
        
        # If we get here, all retries failed
        return RecoveryResult.failure_result(
            f"Operation failed after {self.max_retries} attempts",
            last_error
        )


class FallbackStrategy(RecoveryStrategy[T]):
    """
    Strategy that uses a fallback value or operation
    
    This strategy provides a fallback value or executes a fallback
    operation when the original operation fails.
    """
    
    def __init__(
        self,
        fallback_value: Optional[T] = None,
        fallback_factory: Optional[Callable[[], T]] = None,
        applicable_categories: Optional[List[ErrorCategory]] = None
    ):
        """
        Initialize the fallback strategy
        
        Args:
            fallback_value: Static fallback value to return
            fallback_factory: Factory function to create a fallback value
            applicable_categories: Categories of errors this strategy can handle
        """
        if fallback_value is None and fallback_factory is None:
            raise ValueError("Either fallback_value or fallback_factory must be provided")
            
        self.fallback_value = fallback_value
        self.fallback_factory = fallback_factory
        self.applicable_categories = applicable_categories or [
            ErrorCategory.ELEMENT_NOT_FOUND,
            ErrorCategory.VALIDATION,
            ErrorCategory.VARIABLE
        ]
        
    def can_recover(self, error_context: ErrorContext) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error_context: The error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        # Check if the error is in an applicable category
        return (
            error_context.category in self.applicable_categories and
            error_context.severity != ErrorSeverity.CRITICAL
        )
        
    def recover(self, error_context: ErrorContext, context: Dict[str, Any]) -> RecoveryResult[T]:
        """
        Attempt to recover by providing a fallback value
        
        Args:
            error_context: The error to recover from
            context: Additional context for recovery
            
        Returns:
            Result of the recovery attempt
        """
        try:
            # Use the fallback factory if provided, otherwise use the static value
            if self.fallback_factory:
                result = self.fallback_factory()
            else:
                result = self.fallback_value
                
            return RecoveryResult.success_result(
                "Recovered using fallback value",
                result
            )
            
        except Exception as e:
            # If the fallback itself fails, return a failure result
            new_error = ErrorContext.from_exception(
                e,
                category=ErrorCategory.EXECUTION,
                severity=ErrorSeverity.ERROR,
                context={
                    **error_context.context,
                    "fallback_error": str(e)
                },
                recoverable=False
            )
            
            return RecoveryResult.failure_result(
                "Fallback strategy failed",
                new_error
            )


class SkipStrategy(RecoveryStrategy[None]):
    """
    Strategy that skips the failed operation
    
    This strategy simply acknowledges the error and continues execution
    by skipping the failed operation.
    """
    
    def __init__(
        self,
        applicable_categories: Optional[List[ErrorCategory]] = None,
        skip_message: str = "Operation skipped due to error"
    ):
        """
        Initialize the skip strategy
        
        Args:
            applicable_categories: Categories of errors this strategy can handle
            skip_message: Message to return when skipping
        """
        self.applicable_categories = applicable_categories or [
            ErrorCategory.ELEMENT_NOT_FOUND,
            ErrorCategory.VALIDATION,
            ErrorCategory.TIMEOUT
        ]
        self.skip_message = skip_message
        
    def can_recover(self, error_context: ErrorContext) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error_context: The error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        # Skip strategy can handle most non-critical errors
        return (
            error_context.category in self.applicable_categories and
            error_context.severity != ErrorSeverity.CRITICAL
        )
        
    def recover(self, error_context: ErrorContext, context: Dict[str, Any]) -> RecoveryResult[None]:
        """
        Recover by skipping the operation
        
        Args:
            error_context: The error to recover from
            context: Additional context for recovery
            
        Returns:
            Result of the recovery attempt
        """
        # Simply return a success result with no value
        return RecoveryResult.success_result(self.skip_message)
