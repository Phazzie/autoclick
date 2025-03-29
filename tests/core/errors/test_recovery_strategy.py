"""Tests for recovery strategies"""
import pytest
from unittest.mock import MagicMock, patch

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity
from src.core.errors.recovery_strategy import (
    RecoveryResult,
    RecoveryStrategy,
    RetryStrategy,
    CompositeRecoveryStrategy
)
from src.core.errors.recovery_strategies import (
    RefreshPageStrategy,
    ReauthenticationStrategy,
    WaitAndRetryStrategy
)


def test_recovery_result_creation():
    """Test creating recovery results"""
    # Create a success result
    success_result = RecoveryResult.create_success(
        "Recovery succeeded",
        {"attempt": 1}
    )
    
    assert success_result.success is True
    assert success_result.message == "Recovery succeeded"
    assert success_result.data == {"attempt": 1}
    
    # Create a failure result
    failure_result = RecoveryResult.create_failure(
        "Recovery failed",
        {"reason": "timeout"}
    )
    
    assert failure_result.success is False
    assert failure_result.message == "Recovery failed"
    assert failure_result.data == {"reason": "timeout"}


def test_retry_strategy():
    """Test retry strategy"""
    # Create a retry strategy
    strategy = RetryStrategy(max_retries=3, delay_seconds=1.0)
    
    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found"
    )
    
    # Check if it can recover
    assert strategy.can_recover(error) is True
    
    # Test recovery
    context = {}
    result = strategy.recover(error, context)
    
    assert result.success is True
    assert "Retrying operation" in result.message
    assert context["retry_count"] == 1
    assert result.data["retry_count"] == 1
    assert result.data["max_retries"] == 3
    
    # Test recovery with existing retry count
    context = {"retry_count": 2}
    result = strategy.recover(error, context)
    
    assert result.success is True
    assert context["retry_count"] == 3
    assert result.data["retry_count"] == 3
    
    # Test recovery with max retries exceeded
    context = {"retry_count": 3}
    result = strategy.recover(error, context)
    
    assert result.success is False
    assert "Maximum retry attempts" in result.message


def test_composite_recovery_strategy():
    """Test composite recovery strategy"""
    # Create mock strategies
    strategy1 = MagicMock(spec=RecoveryStrategy)
    strategy1.can_recover.return_value = False
    
    strategy2 = MagicMock(spec=RecoveryStrategy)
    strategy2.can_recover.return_value = True
    strategy2.recover.return_value = RecoveryResult.create_success("Strategy 2 succeeded")
    
    strategy3 = MagicMock(spec=RecoveryStrategy)
    strategy3.can_recover.return_value = True
    strategy3.recover.return_value = RecoveryResult.create_failure("Strategy 3 failed")
    
    # Create composite strategy
    composite = CompositeRecoveryStrategy([strategy1, strategy2, strategy3])
    
    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found"
    )
    
    # Check if it can recover
    assert composite.can_recover(error) is True
    
    # Test recovery
    context = {}
    result = composite.recover(error, context)
    
    assert result.success is True
    assert result.message == "Strategy 2 succeeded"
    
    # Strategy 1 should be skipped because it can't recover
    strategy1.recover.assert_not_called()
    
    # Strategy 2 should be called and succeed
    strategy2.recover.assert_called_once_with(error, context)
    
    # Strategy 3 should not be called because strategy 2 succeeded
    strategy3.recover.assert_not_called()


@patch("time.sleep")
def test_wait_and_retry_strategy(mock_sleep):
    """Test wait and retry strategy"""
    # Create a wait and retry strategy
    strategy = WaitAndRetryStrategy(max_retries=2, wait_seconds=1.5)
    
    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found"
    )
    
    # Check if it can recover
    assert strategy.can_recover(error) is True
    
    # Test recovery
    context = {}
    result = strategy.recover(error, context)
    
    assert result.success is True
    assert "Waiting and retrying" in result.message
    assert context["retry_count"] == 1
    assert result.data["wait_seconds"] == 1.5
    
    # Sleep should be called with the wait time
    mock_sleep.assert_called_once_with(1.5)


@patch("time.sleep")
def test_refresh_page_strategy(mock_sleep):
    """Test refresh page strategy"""
    # Create a refresh page strategy
    strategy = RefreshPageStrategy(wait_after_refresh=1.0)
    
    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_STALE,
        message="Element is stale"
    )
    
    # Check if it can recover
    assert strategy.can_recover(error) is True
    
    # Create a mock browser
    browser = MagicMock()
    context = {"browser": browser}
    
    # Test recovery
    result = strategy.recover(error, context)
    
    assert result.success is True
    assert "Page refreshed successfully" in result.message
    
    # Browser refresh should be called
    browser.refresh.assert_called_once()
    
    # Sleep should be called with the wait time
    mock_sleep.assert_called_once_with(1.0)
    
    # Test recovery without browser
    context = {}
    result = strategy.recover(error, context)
    
    assert result.success is False
    assert "No browser found" in result.message
