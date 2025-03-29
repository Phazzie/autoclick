"""Tests for error factory"""
import pytest

from src.core.errors.error_factory import ErrorFactory
from src.core.errors.error_manager import ErrorManager
from src.core.errors.recovery_strategy import RecoveryStrategy
from src.core.errors.recovery_strategies import (
    RefreshPageStrategy,
    ReauthenticationStrategy,
    WaitAndRetryStrategy
)


def test_create_error_manager():
    """Test creating an error manager"""
    manager = ErrorFactory.create_error_manager()
    assert isinstance(manager, ErrorManager)


def test_create_default_recovery_strategies():
    """Test creating default recovery strategies"""
    strategies = ErrorFactory.create_default_recovery_strategies()
    
    assert len(strategies) > 0
    assert any(isinstance(s, WaitAndRetryStrategy) for s in strategies)
    assert any(isinstance(s, RefreshPageStrategy) for s in strategies)


def test_configure_error_manager_with_defaults():
    """Test configuring an error manager with defaults"""
    manager = ErrorManager()
    
    # Configure with defaults
    configured_manager = ErrorFactory.configure_error_manager_with_defaults(manager)
    
    assert configured_manager is manager
    assert len(manager.recovery_strategies.strategies) > 0
    
    # Configure without recovery strategies
    manager = ErrorManager()
    configured_manager = ErrorFactory.configure_error_manager_with_defaults(
        manager,
        include_recovery_strategies=False
    )
    
    assert configured_manager is manager
    assert len(manager.recovery_strategies.strategies) == 0


def test_create_configured_error_manager():
    """Test creating and configuring an error manager"""
    manager = ErrorFactory.create_configured_error_manager()
    
    assert isinstance(manager, ErrorManager)
    assert len(manager.recovery_strategies.strategies) > 0
    
    # Create without recovery strategies
    manager = ErrorFactory.create_configured_error_manager(include_recovery_strategies=False)
    
    assert isinstance(manager, ErrorManager)
    assert len(manager.recovery_strategies.strategies) == 0


def test_create_retry_strategy():
    """Test creating a retry strategy"""
    strategy = ErrorFactory.create_retry_strategy(
        max_retries=5,
        wait_seconds=3.0
    )
    
    assert isinstance(strategy, WaitAndRetryStrategy)
    assert strategy.max_retries == 5
    assert strategy.wait_seconds == 3.0


def test_create_refresh_page_strategy():
    """Test creating a refresh page strategy"""
    strategy = ErrorFactory.create_refresh_page_strategy(
        wait_after_refresh=2.5
    )
    
    assert isinstance(strategy, RefreshPageStrategy)
    assert strategy.wait_after_refresh == 2.5


def test_create_reauthentication_strategy():
    """Test creating a reauthentication strategy"""
    strategy = ErrorFactory.create_reauthentication_strategy(
        login_action_id="login_action_123"
    )
    
    assert isinstance(strategy, ReauthenticationStrategy)
    assert strategy.login_action_id == "login_action_123"
