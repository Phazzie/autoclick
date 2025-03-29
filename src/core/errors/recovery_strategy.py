"""Recovery strategies for handling errors"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from src.core.errors.error_types import Error, ErrorType


class RecoveryResult:
    """Result of a recovery attempt"""
    
    def __init__(
        self,
        success: bool,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize the recovery result
        
        Args:
            success: Whether the recovery was successful
            message: Message describing the recovery result
            data: Additional data about the recovery
            timestamp: Time of the recovery (defaults to now)
        """
        self.success = success
        self.message = message
        self.data = data or {}
        self.timestamp = timestamp or datetime.now()
        
    def __str__(self) -> str:
        """String representation of the recovery result"""
        status = "succeeded" if self.success else "failed"
        return f"Recovery {status}: {self.message}"
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the recovery result to a dictionary
        
        Returns:
            Dictionary representation of the recovery result
        """
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }
        
    @classmethod
    def create_success(cls, message: str, data: Optional[Dict[str, Any]] = None) -> 'RecoveryResult':
        """
        Create a successful recovery result
        
        Args:
            message: Success message
            data: Additional data about the recovery
            
        Returns:
            Successful recovery result
        """
        return cls(True, message, data)
        
    @classmethod
    def create_failure(cls, message: str, data: Optional[Dict[str, Any]] = None) -> 'RecoveryResult':
        """
        Create a failed recovery result
        
        Args:
            message: Failure message
            data: Additional data about the recovery
            
        Returns:
            Failed recovery result
        """
        return cls(False, message, data)


class RecoveryStrategy(ABC):
    """Interface for error recovery strategies"""
    
    @abstractmethod
    def can_recover(self, error: Error) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error: Error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        pass
        
    @abstractmethod
    def recover(self, error: Error, context: Dict[str, Any]) -> RecoveryResult:
        """
        Attempt to recover from the error
        
        Args:
            error: Error to recover from
            context: Execution context
            
        Returns:
            Result of the recovery attempt
        """
        pass


class RetryStrategy(RecoveryStrategy):
    """Recovery strategy that retries the operation"""
    
    def __init__(
        self,
        max_retries: int = 3,
        delay_seconds: float = 1.0,
        applicable_error_types: Optional[List[ErrorType]] = None
    ):
        """
        Initialize the retry strategy
        
        Args:
            max_retries: Maximum number of retry attempts
            delay_seconds: Delay between retries in seconds
            applicable_error_types: Error types this strategy can handle (None for all)
        """
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
        self.applicable_error_types = applicable_error_types
        
    def can_recover(self, error: Error) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error: Error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        # If no specific error types are specified, handle all errors
        if self.applicable_error_types is None:
            return True
            
        # Otherwise, check if the error type is in the list
        return error.error_type in self.applicable_error_types
        
    def recover(self, error: Error, context: Dict[str, Any]) -> RecoveryResult:
        """
        Attempt to recover from the error by retrying
        
        Args:
            error: Error to recover from
            context: Execution context
            
        Returns:
            Result of the recovery attempt
        """
        # Get the current retry count from the context
        retry_count = context.get("retry_count", 0)
        
        # Check if we've exceeded the maximum retries
        if retry_count >= self.max_retries:
            return RecoveryResult.create_failure(
                f"Maximum retry attempts ({self.max_retries}) exceeded",
                {"retry_count": retry_count, "max_retries": self.max_retries}
            )
            
        # Increment the retry count
        context["retry_count"] = retry_count + 1
        
        # Add delay information to the result
        return RecoveryResult.create_success(
            f"Retrying operation (attempt {retry_count + 1} of {self.max_retries})",
            {
                "retry_count": retry_count + 1,
                "max_retries": self.max_retries,
                "delay_seconds": self.delay_seconds
            }
        )


class CompositeRecoveryStrategy(RecoveryStrategy):
    """Recovery strategy that tries multiple strategies in sequence"""
    
    def __init__(self, strategies: Optional[List[RecoveryStrategy]] = None):
        """
        Initialize the composite recovery strategy
        
        Args:
            strategies: List of recovery strategies to try
        """
        self.strategies = strategies or []
        
    def add_strategy(self, strategy: RecoveryStrategy) -> None:
        """
        Add a recovery strategy
        
        Args:
            strategy: Recovery strategy to add
        """
        if strategy not in self.strategies:
            self.strategies.append(strategy)
            
    def remove_strategy(self, strategy: RecoveryStrategy) -> None:
        """
        Remove a recovery strategy
        
        Args:
            strategy: Recovery strategy to remove
        """
        if strategy in self.strategies:
            self.strategies.remove(strategy)
            
    def can_recover(self, error: Error) -> bool:
        """
        Check if any strategy can recover from the given error
        
        Args:
            error: Error to check
            
        Returns:
            True if any strategy can recover from the error, False otherwise
        """
        return any(strategy.can_recover(error) for strategy in self.strategies)
        
    def recover(self, error: Error, context: Dict[str, Any]) -> RecoveryResult:
        """
        Try each strategy in sequence until one succeeds
        
        Args:
            error: Error to recover from
            context: Execution context
            
        Returns:
            Result of the first successful recovery attempt, or the last failure
        """
        last_result = None
        
        for strategy in self.strategies:
            # Skip strategies that can't recover from this error
            if not strategy.can_recover(error):
                continue
                
            # Try this strategy
            result = strategy.recover(error, context)
            last_result = result
            
            # If it succeeded, return the result
            if result.success:
                return result
                
        # If we get here, all strategies failed
        if last_result:
            return last_result
            
        # If no strategies were tried, return a failure
        return RecoveryResult.create_failure(
            "No applicable recovery strategies found",
            {"error_type": error.error_type.name}
        )
