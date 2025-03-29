"""Factory for creating error handlers and recovery strategies"""
import logging
from typing import Dict, Any, Optional, List, Set

from src.core.errors.error_types import ErrorType
from src.core.errors.error_manager import ErrorManager
from src.core.errors.recovery_strategy import RecoveryStrategy
from src.core.errors.recovery_strategies import (
    RefreshPageStrategy,
    ReauthenticationStrategy,
    WaitAndRetryStrategy
)


class ErrorFactory:
    """
    Factory for creating error handlers and recovery strategies
    
    This class provides methods to create and configure error handling components.
    """
    
    @staticmethod
    def create_error_manager() -> ErrorManager:
        """
        Create an error manager
        
        Returns:
            Configured error manager
        """
        return ErrorManager()
        
    @staticmethod
    def create_default_recovery_strategies() -> List[RecoveryStrategy]:
        """
        Create a list of default recovery strategies
        
        Returns:
            List of recovery strategies
        """
        return [
            WaitAndRetryStrategy(max_retries=3, wait_seconds=2.0),
            RefreshPageStrategy(wait_after_refresh=2.0)
        ]
        
    @staticmethod
    def configure_error_manager_with_defaults(
        error_manager: ErrorManager,
        include_recovery_strategies: bool = True
    ) -> ErrorManager:
        """
        Configure an error manager with default settings
        
        Args:
            error_manager: Error manager to configure
            include_recovery_strategies: Whether to add default recovery strategies
            
        Returns:
            Configured error manager
        """
        # Add default recovery strategies
        if include_recovery_strategies:
            for strategy in ErrorFactory.create_default_recovery_strategies():
                error_manager.add_recovery_strategy(strategy)
                
        return error_manager
        
    @staticmethod
    def create_configured_error_manager(
        include_recovery_strategies: bool = True
    ) -> ErrorManager:
        """
        Create and configure an error manager
        
        Args:
            include_recovery_strategies: Whether to add default recovery strategies
            
        Returns:
            Configured error manager
        """
        error_manager = ErrorFactory.create_error_manager()
        return ErrorFactory.configure_error_manager_with_defaults(
            error_manager,
            include_recovery_strategies
        )
        
    @staticmethod
    def create_retry_strategy(
        max_retries: int = 3,
        wait_seconds: float = 2.0,
        applicable_error_types: Optional[Set[ErrorType]] = None
    ) -> RecoveryStrategy:
        """
        Create a wait and retry strategy
        
        Args:
            max_retries: Maximum number of retry attempts
            wait_seconds: Time to wait between retries (seconds)
            applicable_error_types: Error types this strategy can handle (None for all)
            
        Returns:
            Wait and retry strategy
        """
        return WaitAndRetryStrategy(
            max_retries=max_retries,
            wait_seconds=wait_seconds,
            applicable_error_types=applicable_error_types
        )
        
    @staticmethod
    def create_refresh_page_strategy(
        wait_after_refresh: float = 2.0,
        applicable_error_types: Optional[Set[ErrorType]] = None
    ) -> RecoveryStrategy:
        """
        Create a refresh page strategy
        
        Args:
            wait_after_refresh: Time to wait after refreshing the page (seconds)
            applicable_error_types: Error types this strategy can handle (None for all)
            
        Returns:
            Refresh page strategy
        """
        return RefreshPageStrategy(
            wait_after_refresh=wait_after_refresh,
            applicable_error_types=applicable_error_types
        )
        
    @staticmethod
    def create_reauthentication_strategy(
        login_action_id: str,
        applicable_error_types: Optional[Set[ErrorType]] = None
    ) -> RecoveryStrategy:
        """
        Create a re-authentication strategy
        
        Args:
            login_action_id: ID of the login action to execute
            applicable_error_types: Error types this strategy can handle (None for all)
            
        Returns:
            Re-authentication strategy
        """
        return ReauthenticationStrategy(
            login_action_id=login_action_id,
            applicable_error_types=applicable_error_types
        )
