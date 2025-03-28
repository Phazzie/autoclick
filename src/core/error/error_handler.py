"""Error handling system for the application"""
import logging
import datetime
from typing import Dict, Any, List, Optional, Type, TypeVar, Generic, Callable

from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity
from src.core.error.recovery_strategy import RecoveryStrategy, RecoveryResult


# Type variable for the result of recovery
T = TypeVar('T')


class ErrorHandler(Generic[T]):
    """
    Error handler for managing errors and recovery strategies
    
    This class is responsible for handling errors that occur during
    workflow execution. It maintains a list of recovery strategies
    and attempts to recover from errors using the appropriate strategy.
    """
    
    def __init__(self):
        """Initialize the error handler"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.recovery_strategies: List[RecoveryStrategy[T]] = []
        self.error_history: List[ErrorContext] = []
        self.max_history_size = 100  # Maximum number of errors to keep in history
        
    def add_strategy(self, strategy: RecoveryStrategy[T]) -> None:
        """
        Add a recovery strategy
        
        Args:
            strategy: The recovery strategy to add
        """
        self.recovery_strategies.append(strategy)
        
    def remove_strategy(self, strategy: RecoveryStrategy[T]) -> None:
        """
        Remove a recovery strategy
        
        Args:
            strategy: The recovery strategy to remove
        """
        if strategy in self.recovery_strategies:
            self.recovery_strategies.remove(strategy)
            
    def clear_strategies(self) -> None:
        """Remove all recovery strategies"""
        self.recovery_strategies.clear()
        
    def handle_error(
        self,
        error_context: ErrorContext,
        context: Dict[str, Any]
    ) -> RecoveryResult[T]:
        """
        Handle an error using the available recovery strategies
        
        Args:
            error_context: The error to handle
            context: Additional context for recovery
            
        Returns:
            Result of the recovery attempt
        """
        # Set the timestamp on the error context
        error_context.timestamp = datetime.datetime.now()
        
        # Add the error to the history
        self._add_to_history(error_context)
        
        # Log the error
        self._log_error(error_context)
        
        # If the error is not recoverable, return a failure result
        if not error_context.recoverable:
            return RecoveryResult.failure_result(
                "Error is not recoverable",
                error_context
            )
            
        # Try each recovery strategy in order
        for strategy in self.recovery_strategies:
            if strategy.can_recover(error_context):
                self.logger.debug(
                    f"Attempting recovery with strategy: {strategy.__class__.__name__}"
                )
                
                # Attempt recovery
                result = strategy.recover(error_context, context)
                
                # Log the result
                if result.success:
                    self.logger.info(
                        f"Recovery successful: {result.message}"
                    )
                else:
                    self.logger.warning(
                        f"Recovery failed: {result.message}"
                    )
                    
                    # Add the new error to the history if there is one
                    if result.new_error:
                        self._add_to_history(result.new_error)
                        
                return result
                
        # If no strategy could recover, return a failure result
        return RecoveryResult.failure_result(
            "No suitable recovery strategy found",
            error_context
        )
        
    def handle_exception(
        self,
        exception: Exception,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: Optional[Dict[str, Any]] = None,
        recovery_context: Optional[Dict[str, Any]] = None
    ) -> RecoveryResult[T]:
        """
        Handle an exception using the available recovery strategies
        
        Args:
            exception: The exception to handle
            category: Category of the error
            severity: Severity level of the error
            context: Additional context information for the error
            recovery_context: Additional context for recovery
            
        Returns:
            Result of the recovery attempt
        """
        # Create an error context from the exception
        error_context = ErrorContext.from_exception(
            exception,
            category=category,
            severity=severity,
            context=context or {}
        )
        
        # Handle the error
        return self.handle_error(error_context, recovery_context or {})
        
    def get_error_history(self) -> List[ErrorContext]:
        """
        Get the error history
        
        Returns:
            List of error contexts in chronological order (oldest first)
        """
        return self.error_history.copy()
        
    def clear_error_history(self) -> None:
        """Clear the error history"""
        self.error_history.clear()
        
    def _add_to_history(self, error_context: ErrorContext) -> None:
        """
        Add an error to the history
        
        Args:
            error_context: The error to add
        """
        self.error_history.append(error_context)
        
        # Trim the history if it exceeds the maximum size
        if len(self.error_history) > self.max_history_size:
            self.error_history = self.error_history[-self.max_history_size:]
            
    def _log_error(self, error_context: ErrorContext) -> None:
        """
        Log an error
        
        Args:
            error_context: The error to log
        """
        # Determine the log level based on the error severity
        log_level = {
            ErrorSeverity.INFO: logging.INFO,
            ErrorSeverity.WARNING: logging.WARNING,
            ErrorSeverity.ERROR: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(error_context.severity, logging.ERROR)
        
        # Log the error
        self.logger.log(
            log_level,
            f"{error_context}",
            exc_info=error_context.exception
        )


class ErrorHandlerFactory:
    """Factory for creating error handlers with predefined strategies"""
    
    @classmethod
    def create_default_handler(cls) -> ErrorHandler:
        """
        Create an error handler with default recovery strategies
        
        Returns:
            An ErrorHandler instance with default strategies
        """
        from src.core.error.recovery_strategy import RetryStrategy, FallbackStrategy, SkipStrategy
        
        handler = ErrorHandler()
        
        # Add default strategies
        handler.add_strategy(RetryStrategy(max_retries=3, delay_seconds=1.0))
        handler.add_strategy(FallbackStrategy(fallback_value=None))
        handler.add_strategy(SkipStrategy())
        
        return handler
        
    @classmethod
    def create_web_handler(cls) -> ErrorHandler:
        """
        Create an error handler optimized for web automation
        
        Returns:
            An ErrorHandler instance with web-optimized strategies
        """
        from src.core.error.recovery_strategy import RetryStrategy, FallbackStrategy, SkipStrategy
        
        handler = ErrorHandler()
        
        # Add web-specific strategies
        handler.add_strategy(RetryStrategy(
            max_retries=5,
            delay_seconds=2.0,
            applicable_categories=[
                ErrorCategory.ELEMENT_NOT_FOUND,
                ErrorCategory.ELEMENT_STALE,
                ErrorCategory.NAVIGATION,
                ErrorCategory.TIMEOUT,
                ErrorCategory.NETWORK
            ]
        ))
        
        handler.add_strategy(FallbackStrategy(
            fallback_value=None,
            applicable_categories=[
                ErrorCategory.ELEMENT_NOT_FOUND,
                ErrorCategory.VALIDATION
            ]
        ))
        
        handler.add_strategy(SkipStrategy(
            applicable_categories=[
                ErrorCategory.ELEMENT_NOT_FOUND,
                ErrorCategory.ELEMENT_STALE,
                ErrorCategory.TIMEOUT
            ]
        ))
        
        return handler
