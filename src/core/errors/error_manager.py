"""Error manager for coordinating error handling"""
import logging
from typing import Dict, Any, Optional, List, Callable, Type

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity
from src.core.errors.error_listener import ErrorListener, ErrorEvent, CompositeErrorListener
from src.core.errors.recovery_strategy import RecoveryStrategy, RecoveryResult, CompositeRecoveryStrategy


class ErrorManager:
    """
    Manages error handling for the automation system
    
    This class coordinates error listeners and recovery strategies to provide
    a unified interface for error handling.
    """
    
    def __init__(self):
        """Initialize the error manager"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.listeners = CompositeErrorListener()
        self.recovery_strategies = CompositeRecoveryStrategy()
        
    def add_listener(self, listener: ErrorListener) -> None:
        """
        Add an error listener
        
        Args:
            listener: Error listener to add
        """
        self.listeners.add_listener(listener)
        
    def remove_listener(self, listener: ErrorListener) -> None:
        """
        Remove an error listener
        
        Args:
            listener: Error listener to remove
        """
        self.listeners.remove_listener(listener)
        
    def add_recovery_strategy(self, strategy: RecoveryStrategy) -> None:
        """
        Add a recovery strategy
        
        Args:
            strategy: Recovery strategy to add
        """
        self.recovery_strategies.add_strategy(strategy)
        
    def remove_recovery_strategy(self, strategy: RecoveryStrategy) -> None:
        """
        Remove a recovery strategy
        
        Args:
            strategy: Recovery strategy to remove
        """
        self.recovery_strategies.remove_strategy(strategy)
        
    def handle_error(
        self,
        error: Error,
        context: Optional[Dict[str, Any]] = None,
        attempt_recovery: bool = True
    ) -> Tuple[bool, Optional[RecoveryResult]]:
        """
        Handle an error
        
        Args:
            error: Error to handle
            context: Execution context
            attempt_recovery: Whether to attempt recovery
            
        Returns:
            Tuple of (handled, recovery_result)
            - handled: True if the error was handled by a listener
            - recovery_result: Result of recovery attempt, or None if no recovery was attempted
        """
        # Create the error event
        event = ErrorEvent(error, context)
        
        # Log the error
        self.logger.error(f"Error occurred: {error}")
        
        # Notify listeners
        handled = self.listeners.on_error(event)
        
        # Attempt recovery if requested and not already handled
        recovery_result = None
        if attempt_recovery and not handled and self.recovery_strategies.can_recover(error):
            recovery_result = self.recovery_strategies.recover(error, context or {})
            
            # Log the recovery result
            if recovery_result.success:
                self.logger.info(f"Recovery succeeded: {recovery_result.message}")
            else:
                self.logger.warning(f"Recovery failed: {recovery_result.message}")
                
        return handled, recovery_result
        
    def handle_exception(
        self,
        exception: Exception,
        error_type: ErrorType = ErrorType.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        source: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        attempt_recovery: bool = True
    ) -> Tuple[bool, Optional[RecoveryResult]]:
        """
        Handle an exception
        
        Args:
            exception: Exception to handle
            error_type: Type of the error
            severity: Severity level of the error
            source: Source of the error
            context: Execution context
            attempt_recovery: Whether to attempt recovery
            
        Returns:
            Tuple of (handled, recovery_result)
            - handled: True if the error was handled by a listener
            - recovery_result: Result of recovery attempt, or None if no recovery was attempted
        """
        # Convert the exception to an error
        error = Error.from_exception(
            exception=exception,
            error_type=error_type,
            severity=severity,
            source=source
        )
        
        # Handle the error
        return self.handle_error(error, context, attempt_recovery)
        
    def create_error_callback(
        self,
        callback: Callable[[ErrorEvent], bool]
    ) -> ErrorListener:
        """
        Create an error listener from a callback function
        
        Args:
            callback: Function to call when an error occurs
            
        Returns:
            Error listener that calls the callback function
        """
        from src.core.errors.error_listener import CallbackErrorListener
        listener = CallbackErrorListener(callback)
        self.add_listener(listener)
        return listener
        
    def create_error(
        self,
        error_type: ErrorType,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        exception: Optional[Exception] = None
    ) -> Error:
        """
        Create an error
        
        Args:
            error_type: Type of the error
            message: Human-readable error message
            severity: Severity level of the error
            details: Additional details about the error
            source: Source of the error
            exception: Original exception if this error wraps an exception
            
        Returns:
            Error instance
        """
        return Error(
            error_type=error_type,
            message=message,
            severity=severity,
            details=details,
            source=source,
            exception=exception
        )
