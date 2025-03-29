"""Tests for specific recovery strategies"""
import pytest
from unittest.mock import MagicMock, patch

from src.core.errors.error_types import Error, ErrorType
from src.core.errors.recovery_strategies import (
    RefreshPageStrategy,
    ReauthenticationStrategy,
    WaitAndRetryStrategy
)


@patch("time.sleep")
def test_refresh_page_strategy(mock_sleep):
    """Test refresh page strategy"""
    # Create a strategy
    strategy = RefreshPageStrategy(wait_after_refresh=2.0)
    
    # Create errors of different types
    stale_error = Error(error_type=ErrorType.ELEMENT_STALE, message="Element is stale")
    not_found_error = Error(error_type=ErrorType.ELEMENT_NOT_FOUND, message="Element not found")
    timeout_error = Error(error_type=ErrorType.TIMEOUT, message="Operation timed out")
    
    # Check which errors it can recover from
    assert strategy.can_recover(stale_error) is True
    assert strategy.can_recover(not_found_error) is True
    assert strategy.can_recover(timeout_error) is False
    
    # Create a mock browser
    browser = MagicMock()
    context = {"browser": browser}
    
    # Test recovery
    result = strategy.recover(stale_error, context)
    
    # Check results
    assert result.success is True
    assert "Page refreshed successfully" in result.message
    browser.refresh.assert_called_once()
    mock_sleep.assert_called_once_with(2.0)
    
    # Test recovery without browser
    result = strategy.recover(stale_error, {})
    
    assert result.success is False
    assert "No browser found" in result.message


def test_reauthentication_strategy():
    """Test reauthentication strategy"""
    # Create a strategy
    strategy = ReauthenticationStrategy(login_action_id="login_action_123")
    
    # Create errors of different types
    auth_error = Error(error_type=ErrorType.AUTHENTICATION_ERROR, message="Authentication failed")
    not_found_error = Error(error_type=ErrorType.ELEMENT_NOT_FOUND, message="Element not found")
    
    # Check which errors it can recover from
    assert strategy.can_recover(auth_error) is True
    assert strategy.can_recover(not_found_error) is False
    
    # Create a mock action factory and login action
    login_action = MagicMock()
    login_action.execute.return_value = MagicMock(success=True)
    
    action_factory = MagicMock()
    action_factory.get_action_by_id.return_value = login_action
    
    context = {"action_factory": action_factory}
    
    # Test recovery
    result = strategy.recover(auth_error, context)
    
    # Check results
    assert result.success is True
    assert "Re-authentication successful" in result.message
    action_factory.get_action_by_id.assert_called_once_with("login_action_123")
    login_action.execute.assert_called_once_with(context)
    
    # Test recovery with failed login
    login_action.execute.return_value = MagicMock(success=False, message="Login failed")
    result = strategy.recover(auth_error, context)
    
    assert result.success is False
    assert "Re-authentication failed" in result.message
    
    # Test recovery without action factory
    result = strategy.recover(auth_error, {})
    
    assert result.success is False
    assert "No action factory found" in result.message
    
    # Test recovery with missing login action
    action_factory.get_action_by_id.return_value = None
    result = strategy.recover(auth_error, context)
    
    assert result.success is False
    assert "Login action with ID" in result.message


@patch("time.sleep")
def test_wait_and_retry_strategy(mock_sleep):
    """Test wait and retry strategy"""
    # Create a strategy
    strategy = WaitAndRetryStrategy(max_retries=3, wait_seconds=2.0)
    
    # Create errors of different types
    not_found_error = Error(error_type=ErrorType.ELEMENT_NOT_FOUND, message="Element not found")
    not_visible_error = Error(error_type=ErrorType.ELEMENT_NOT_VISIBLE, message="Element not visible")
    timeout_error = Error(error_type=ErrorType.TIMEOUT, message="Operation timed out")
    
    # Check which errors it can recover from
    assert strategy.can_recover(not_found_error) is True
    assert strategy.can_recover(not_visible_error) is True
    assert strategy.can_recover(timeout_error) is False
    
    # Test recovery
    context = {}
    result = strategy.recover(not_found_error, context)
    
    # Check results
    assert result.success is True
    assert "Waiting and retrying" in result.message
    assert context["retry_count"] == 1
    assert result.data["retry_count"] == 1
    assert result.data["max_retries"] == 3
    assert result.data["wait_seconds"] == 2.0
    mock_sleep.assert_called_once_with(2.0)
    
    # Test recovery with existing retry count
    context = {"retry_count": 2}
    result = strategy.recover(not_found_error, context)
    
    assert result.success is True
    assert context["retry_count"] == 3
    assert result.data["retry_count"] == 3
    
    # Test recovery with max retries exceeded
    context = {"retry_count": 3}
    result = strategy.recover(not_found_error, context)
    
    assert result.success is False
    assert "Maximum retry attempts" in result.message
