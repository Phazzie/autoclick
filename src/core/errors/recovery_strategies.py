"""Specific recovery strategies for common errors"""
import time
import logging
from typing import Dict, Any, Optional, List, Set

from src.core.errors.error_types import Error, ErrorType
from src.core.errors.recovery_strategy import RecoveryStrategy, RecoveryResult


class RefreshPageStrategy(RecoveryStrategy):
    """Recovery strategy that refreshes the page"""
    
    def __init__(
        self,
        applicable_error_types: Optional[Set[ErrorType]] = None,
        wait_after_refresh: float = 2.0
    ):
        """
        Initialize the refresh page strategy
        
        Args:
            applicable_error_types: Error types this strategy can handle (None for all)
            wait_after_refresh: Time to wait after refreshing the page (seconds)
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.applicable_error_types = applicable_error_types or {
            ErrorType.ELEMENT_STALE,
            ErrorType.ELEMENT_NOT_FOUND,
            ErrorType.JAVASCRIPT_ERROR,
            ErrorType.PAGE_LOAD_TIMEOUT
        }
        self.wait_after_refresh = wait_after_refresh
        
    def can_recover(self, error: Error) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error: Error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        return error.error_type in self.applicable_error_types
        
    def recover(self, error: Error, context: Dict[str, Any]) -> RecoveryResult:
        """
        Attempt to recover from the error by refreshing the page
        
        Args:
            error: Error to recover from
            context: Execution context
            
        Returns:
            Result of the recovery attempt
        """
        # Check if we have a browser in the context
        browser = context.get("browser")
        if not browser:
            return RecoveryResult.create_failure(
                "No browser found in context",
                {"error_type": error.error_type.name}
            )
            
        try:
            # Refresh the page
            self.logger.info("Refreshing page to recover from error")
            browser.refresh()
            
            # Wait after refresh
            if self.wait_after_refresh > 0:
                time.sleep(self.wait_after_refresh)
                
            return RecoveryResult.create_success(
                "Page refreshed successfully",
                {"wait_after_refresh": self.wait_after_refresh}
            )
        except Exception as e:
            return RecoveryResult.create_failure(
                f"Failed to refresh page: {str(e)}",
                {"exception": str(e)}
            )


class ReauthenticationStrategy(RecoveryStrategy):
    """Recovery strategy that re-authenticates the user"""
    
    def __init__(
        self,
        login_action_id: str,
        applicable_error_types: Optional[Set[ErrorType]] = None
    ):
        """
        Initialize the re-authentication strategy
        
        Args:
            login_action_id: ID of the login action to execute
            applicable_error_types: Error types this strategy can handle (None for all)
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.login_action_id = login_action_id
        self.applicable_error_types = applicable_error_types or {
            ErrorType.AUTHENTICATION_ERROR,
            ErrorType.AUTHORIZATION_ERROR
        }
        
    def can_recover(self, error: Error) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error: Error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        return error.error_type in self.applicable_error_types
        
    def recover(self, error: Error, context: Dict[str, Any]) -> RecoveryResult:
        """
        Attempt to recover from the error by re-authenticating
        
        Args:
            error: Error to recover from
            context: Execution context
            
        Returns:
            Result of the recovery attempt
        """
        # Check if we have an action factory in the context
        action_factory = context.get("action_factory")
        if not action_factory:
            return RecoveryResult.create_failure(
                "No action factory found in context",
                {"error_type": error.error_type.name}
            )
            
        try:
            # Get the login action
            login_action = action_factory.get_action_by_id(self.login_action_id)
            if not login_action:
                return RecoveryResult.create_failure(
                    f"Login action with ID '{self.login_action_id}' not found",
                    {"login_action_id": self.login_action_id}
                )
                
            # Execute the login action
            self.logger.info("Re-authenticating to recover from error")
            result = login_action.execute(context)
            
            if result.success:
                return RecoveryResult.create_success(
                    "Re-authentication successful",
                    {"login_action_id": self.login_action_id}
                )
            else:
                return RecoveryResult.create_failure(
                    f"Re-authentication failed: {result.message}",
                    {"login_action_id": self.login_action_id, "action_result": result.data}
                )
        except Exception as e:
            return RecoveryResult.create_failure(
                f"Failed to re-authenticate: {str(e)}",
                {"exception": str(e), "login_action_id": self.login_action_id}
            )


class WaitAndRetryStrategy(RecoveryStrategy):
    """Recovery strategy that waits and retries the operation"""
    
    def __init__(
        self,
        max_retries: int = 3,
        wait_seconds: float = 2.0,
        applicable_error_types: Optional[Set[ErrorType]] = None
    ):
        """
        Initialize the wait and retry strategy
        
        Args:
            max_retries: Maximum number of retry attempts
            wait_seconds: Time to wait between retries (seconds)
            applicable_error_types: Error types this strategy can handle (None for all)
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.max_retries = max_retries
        self.wait_seconds = wait_seconds
        self.applicable_error_types = applicable_error_types or {
            ErrorType.ELEMENT_NOT_FOUND,
            ErrorType.ELEMENT_NOT_VISIBLE,
            ErrorType.ELEMENT_NOT_CLICKABLE,
            ErrorType.NETWORK_ERROR,
            ErrorType.CONNECTION_ERROR
        }
        
    def can_recover(self, error: Error) -> bool:
        """
        Check if this strategy can recover from the given error
        
        Args:
            error: Error to check
            
        Returns:
            True if this strategy can recover from the error, False otherwise
        """
        return error.error_type in self.applicable_error_types
        
    def recover(self, error: Error, context: Dict[str, Any]) -> RecoveryResult:
        """
        Attempt to recover from the error by waiting and retrying
        
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
        
        # Wait before retrying
        if self.wait_seconds > 0:
            self.logger.info(f"Waiting {self.wait_seconds} seconds before retry")
            time.sleep(self.wait_seconds)
            
        return RecoveryResult.create_success(
            f"Waiting and retrying operation (attempt {retry_count + 1} of {self.max_retries})",
            {
                "retry_count": retry_count + 1,
                "max_retries": self.max_retries,
                "wait_seconds": self.wait_seconds
            }
        )
