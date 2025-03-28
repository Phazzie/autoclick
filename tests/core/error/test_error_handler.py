"""Tests for the error handler"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity
from src.core.error.error_handler import ErrorHandler, ErrorHandlerFactory
from src.core.error.recovery_strategy import RecoveryStrategy, RecoveryResult


class MockStrategy(RecoveryStrategy):
    """Mock recovery strategy for testing"""
    
    def __init__(self, can_recover_result=True, recover_result=None):
        """Initialize the mock strategy"""
        self.can_recover_result = can_recover_result
        self.recover_result = recover_result or RecoveryResult.success_result("Mock recovery")
        self.can_recover_called = False
        self.recover_called = False
        self.last_error = None
        self.last_context = None
        
    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if this strategy can recover from the given error"""
        self.can_recover_called = True
        self.last_error = error_context
        return self.can_recover_result
        
    def recover(self, error_context: ErrorContext, context: Dict[str, Any]) -> RecoveryResult:
        """Attempt to recover from the error"""
        self.recover_called = True
        self.last_error = error_context
        self.last_context = context
        return self.recover_result


class TestErrorHandler(unittest.TestCase):
    """Test cases for ErrorHandler"""

    def setUp(self):
        """Set up test environment"""
        self.handler = ErrorHandler()
        
    def test_add_strategy(self):
        """Test adding a recovery strategy"""
        # Create a mock strategy
        strategy = MockStrategy()
        
        # Add the strategy
        self.handler.add_strategy(strategy)
        
        # Check that the strategy was added
        self.assertIn(strategy, self.handler.recovery_strategies)
        
    def test_remove_strategy(self):
        """Test removing a recovery strategy"""
        # Create a mock strategy
        strategy = MockStrategy()
        
        # Add the strategy
        self.handler.add_strategy(strategy)
        
        # Remove the strategy
        self.handler.remove_strategy(strategy)
        
        # Check that the strategy was removed
        self.assertNotIn(strategy, self.handler.recovery_strategies)
        
    def test_clear_strategies(self):
        """Test clearing all recovery strategies"""
        # Add some strategies
        self.handler.add_strategy(MockStrategy())
        self.handler.add_strategy(MockStrategy())
        
        # Clear the strategies
        self.handler.clear_strategies()
        
        # Check that all strategies were removed
        self.assertEqual(len(self.handler.recovery_strategies), 0)
        
    def test_handle_error_no_strategies(self):
        """Test handling an error with no strategies"""
        # Create an error
        error = ErrorContext(
            message="Test error",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        # Handle the error
        result = self.handler.handle_error(error, {})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("No suitable recovery strategy found", result.message)
        
        # Check that the error was added to the history
        self.assertEqual(len(self.handler.error_history), 1)
        self.assertEqual(self.handler.error_history[0], error)
        
    def test_handle_error_non_recoverable(self):
        """Test handling a non-recoverable error"""
        # Create a non-recoverable error
        error = ErrorContext(
            message="Critical error",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.CRITICAL,
            recoverable=False
        )
        
        # Add a strategy that could recover
        strategy = MockStrategy()
        self.handler.add_strategy(strategy)
        
        # Handle the error
        result = self.handler.handle_error(error, {})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("Error is not recoverable", result.message)
        
        # Check that the strategy was not called
        self.assertFalse(strategy.can_recover_called)
        self.assertFalse(strategy.recover_called)
        
    def test_handle_error_with_strategy(self):
        """Test handling an error with a suitable strategy"""
        # Create an error
        error = ErrorContext(
            message="Test error",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        # Create a strategy that can recover
        strategy = MockStrategy(
            can_recover_result=True,
            recover_result=RecoveryResult.success_result("Recovered successfully")
        )
        
        # Add the strategy
        self.handler.add_strategy(strategy)
        
        # Handle the error
        context = {"test": "value"}
        result = self.handler.handle_error(error, context)
        
        # Check the result
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Recovered successfully")
        
        # Check that the strategy was called
        self.assertTrue(strategy.can_recover_called)
        self.assertTrue(strategy.recover_called)
        self.assertEqual(strategy.last_error, error)
        self.assertEqual(strategy.last_context, context)
        
    def test_handle_error_strategy_fails(self):
        """Test handling an error when the strategy fails"""
        # Create an error
        error = ErrorContext(
            message="Test error",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        # Create a strategy that fails to recover
        new_error = ErrorContext(
            message="Recovery failed",
            category=ErrorCategory.EXECUTION,
            severity=ErrorSeverity.ERROR
        )
        
        strategy = MockStrategy(
            can_recover_result=True,
            recover_result=RecoveryResult.failure_result("Recovery failed", new_error)
        )
        
        # Add the strategy
        self.handler.add_strategy(strategy)
        
        # Handle the error
        result = self.handler.handle_error(error, {})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Recovery failed")
        self.assertEqual(result.new_error, new_error)
        
        # Check that both errors were added to the history
        self.assertEqual(len(self.handler.error_history), 2)
        self.assertEqual(self.handler.error_history[0], error)
        self.assertEqual(self.handler.error_history[1], new_error)
        
    def test_handle_error_multiple_strategies(self):
        """Test handling an error with multiple strategies"""
        # Create an error
        error = ErrorContext(
            message="Test error",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        # Create strategies
        strategy1 = MockStrategy(can_recover_result=False)
        strategy2 = MockStrategy(
            can_recover_result=True,
            recover_result=RecoveryResult.success_result("Recovered with strategy 2")
        )
        strategy3 = MockStrategy(can_recover_result=True)
        
        # Add the strategies
        self.handler.add_strategy(strategy1)
        self.handler.add_strategy(strategy2)
        self.handler.add_strategy(strategy3)
        
        # Handle the error
        result = self.handler.handle_error(error, {})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Recovered with strategy 2")
        
        # Check that the strategies were called in order
        self.assertTrue(strategy1.can_recover_called)
        self.assertFalse(strategy1.recover_called)
        
        self.assertTrue(strategy2.can_recover_called)
        self.assertTrue(strategy2.recover_called)
        
        self.assertFalse(strategy3.can_recover_called)
        self.assertFalse(strategy3.recover_called)
        
    def test_handle_exception(self):
        """Test handling an exception"""
        # Create an exception
        exception = ValueError("Invalid value")
        
        # Create a strategy that can recover
        strategy = MockStrategy(
            can_recover_result=True,
            recover_result=RecoveryResult.success_result("Recovered from exception")
        )
        
        # Add the strategy
        self.handler.add_strategy(strategy)
        
        # Handle the exception
        result = self.handler.handle_exception(
            exception,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
            context={"field": "email"},
            recovery_context={"test": "value"}
        )
        
        # Check the result
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Recovered from exception")
        
        # Check that the strategy was called with the correct error context
        self.assertTrue(strategy.can_recover_called)
        self.assertTrue(strategy.recover_called)
        self.assertEqual(strategy.last_error.message, "Invalid value")
        self.assertEqual(strategy.last_error.category, ErrorCategory.VALIDATION)
        self.assertEqual(strategy.last_error.severity, ErrorSeverity.ERROR)
        self.assertEqual(strategy.last_error.context, {"field": "email"})
        self.assertEqual(strategy.last_error.exception, exception)
        self.assertEqual(strategy.last_context, {"test": "value"})
        
    def test_error_history(self):
        """Test error history management"""
        # Create some errors
        error1 = ErrorContext(
            message="Error 1",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        error2 = ErrorContext(
            message="Error 2",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        # Handle the errors
        self.handler.handle_error(error1, {})
        self.handler.handle_error(error2, {})
        
        # Check the error history
        history = self.handler.get_error_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], error1)
        self.assertEqual(history[1], error2)
        
        # Clear the error history
        self.handler.clear_error_history()
        
        # Check that the history was cleared
        self.assertEqual(len(self.handler.get_error_history()), 0)
        
    def test_error_history_limit(self):
        """Test error history size limit"""
        # Set a small history size limit
        self.handler.max_history_size = 2
        
        # Create some errors
        error1 = ErrorContext(
            message="Error 1",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        error2 = ErrorContext(
            message="Error 2",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        error3 = ErrorContext(
            message="Error 3",
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR
        )
        
        # Handle the errors
        self.handler.handle_error(error1, {})
        self.handler.handle_error(error2, {})
        self.handler.handle_error(error3, {})
        
        # Check the error history (should only contain the last 2 errors)
        history = self.handler.get_error_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], error2)
        self.assertEqual(history[1], error3)


class TestErrorHandlerFactory(unittest.TestCase):
    """Test cases for ErrorHandlerFactory"""

    def test_create_default_handler(self):
        """Test creating a default error handler"""
        # Create a default handler
        handler = ErrorHandlerFactory.create_default_handler()
        
        # Check that the handler has the expected strategies
        self.assertEqual(len(handler.recovery_strategies), 3)
        
        # Check the types of strategies
        from src.core.error.recovery_strategy import RetryStrategy, FallbackStrategy, SkipStrategy
        self.assertIsInstance(handler.recovery_strategies[0], RetryStrategy)
        self.assertIsInstance(handler.recovery_strategies[1], FallbackStrategy)
        self.assertIsInstance(handler.recovery_strategies[2], SkipStrategy)
        
    def test_create_web_handler(self):
        """Test creating a web-optimized error handler"""
        # Create a web handler
        handler = ErrorHandlerFactory.create_web_handler()
        
        # Check that the handler has the expected strategies
        self.assertEqual(len(handler.recovery_strategies), 3)
        
        # Check the types of strategies
        from src.core.error.recovery_strategy import RetryStrategy, FallbackStrategy, SkipStrategy
        self.assertIsInstance(handler.recovery_strategies[0], RetryStrategy)
        self.assertIsInstance(handler.recovery_strategies[1], FallbackStrategy)
        self.assertIsInstance(handler.recovery_strategies[2], SkipStrategy)
        
        # Check that the retry strategy has web-specific settings
        retry_strategy = handler.recovery_strategies[0]
        self.assertEqual(retry_strategy.max_retries, 5)
        self.assertEqual(retry_strategy.delay_seconds, 2.0)
        self.assertIn(ErrorCategory.ELEMENT_NOT_FOUND, retry_strategy.applicable_categories)
        self.assertIn(ErrorCategory.NAVIGATION, retry_strategy.applicable_categories)


if __name__ == "__main__":
    unittest.main()
