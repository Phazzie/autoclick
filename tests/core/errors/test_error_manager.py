"""Tests for error manager"""
import pytest
from unittest.mock import MagicMock

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity
from src.core.errors.error_listener import ErrorListener, ErrorEvent
from src.core.errors.recovery_strategy import RecoveryStrategy, RecoveryResult
from src.core.errors.error_manager import ErrorManager


class MockErrorListener(ErrorListener):
    """Mock error listener for testing"""

    def __init__(self, should_handle: bool = False):
        self.events = []
        self.should_handle = should_handle

    def on_error(self, event: ErrorEvent) -> bool:
        self.events.append(event)
        return self.should_handle


class MockRecoveryStrategy(RecoveryStrategy):
    """Mock recovery strategy for testing"""

    def __init__(self, can_recover_result: bool = True, recovery_success: bool = True):
        self.errors = []
        self.contexts = []
        self.can_recover_result = can_recover_result
        self.recovery_success = recovery_success

    def can_recover(self, error: Error) -> bool:
        self.errors.append(error)
        return self.can_recover_result

    def recover(self, error: Error, context: dict) -> RecoveryResult:
        self.contexts.append(context)
        if self.recovery_success:
            return RecoveryResult.create_success("Recovery succeeded")
        else:
            return RecoveryResult.create_failure("Recovery failed")


def test_error_manager_creation():
    """Test creating an error manager"""
    manager = ErrorManager()
    assert isinstance(manager, ErrorManager)


def test_add_remove_listener():
    """Test adding and removing listeners"""
    manager = ErrorManager()
    listener = MockErrorListener()

    # Add listener
    manager.add_listener(listener)
    assert listener in manager.listeners.listeners

    # Remove listener
    manager.remove_listener(listener)
    assert listener not in manager.listeners.listeners


def test_add_remove_recovery_strategy():
    """Test adding and removing recovery strategies"""
    manager = ErrorManager()
    strategy = MockRecoveryStrategy()

    # Add strategy
    manager.add_recovery_strategy(strategy)
    assert strategy in manager.recovery_strategies.strategies

    # Remove strategy
    manager.remove_recovery_strategy(strategy)
    assert strategy not in manager.recovery_strategies.strategies


def test_handle_error_with_listener():
    """Test handling an error with a listener"""
    manager = ErrorManager()
    listener = MockErrorListener(should_handle=True)
    manager.add_listener(listener)

    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found",
        severity=ErrorSeverity.ERROR
    )

    # Handle the error
    context = {"key": "value"}
    handled, recovery_result = manager.handle_error(error, context)

    # Check results
    assert handled is True
    assert recovery_result is None
    assert len(listener.events) == 1
    assert listener.events[0].error is error
    assert listener.events[0].context is context


def test_handle_error_with_recovery():
    """Test handling an error with recovery"""
    manager = ErrorManager()
    listener = MockErrorListener(should_handle=False)
    strategy = MockRecoveryStrategy(can_recover_result=True, recovery_success=True)

    manager.add_listener(listener)
    manager.add_recovery_strategy(strategy)

    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found",
        severity=ErrorSeverity.ERROR
    )

    # Handle the error
    context = {"key": "value"}
    handled, recovery_result = manager.handle_error(error, context)

    # Check results
    assert handled is False
    assert recovery_result is not None
    assert recovery_result.success is True
    assert len(listener.events) == 1
    assert listener.events[0].error is error
    # Note: can_recover is called during both checking and actual recovery
    assert len(strategy.errors) >= 1
    assert error in strategy.errors
    assert len(strategy.contexts) == 1
    assert strategy.contexts[0] is context


def test_handle_error_with_failed_recovery():
    """Test handling an error with failed recovery"""
    manager = ErrorManager()
    strategy = MockRecoveryStrategy(can_recover_result=True, recovery_success=False)

    manager.add_recovery_strategy(strategy)

    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found",
        severity=ErrorSeverity.ERROR
    )

    # Handle the error
    context = {"key": "value"}
    handled, recovery_result = manager.handle_error(error, context)

    # Check results
    assert handled is False
    assert recovery_result is not None
    assert recovery_result.success is False
    # Note: can_recover is called during both checking and actual recovery
    assert len(strategy.errors) >= 1
    assert error in strategy.errors


def test_handle_exception():
    """Test handling an exception"""
    manager = ErrorManager()
    listener = MockErrorListener()
    manager.add_listener(listener)

    # Create an exception
    exception = ValueError("Invalid value")

    # Handle the exception
    context = {"key": "value"}
    handled, recovery_result = manager.handle_exception(
        exception=exception,
        error_type=ErrorType.VALIDATION_ERROR,
        severity=ErrorSeverity.WARNING,
        source="test_module",
        context=context
    )

    # Check results
    assert handled is False
    assert recovery_result is None
    assert len(listener.events) == 1
    assert listener.events[0].error.error_type == ErrorType.VALIDATION_ERROR
    assert listener.events[0].error.message == "Invalid value"
    assert listener.events[0].error.severity == ErrorSeverity.WARNING
    assert listener.events[0].error.source == "test_module"
    assert listener.events[0].error.exception is exception
