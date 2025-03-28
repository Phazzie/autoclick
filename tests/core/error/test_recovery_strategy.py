"""Tests for recovery strategies"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity
from src.core.error.recovery_strategy import (
    RecoveryResult,
    RetryStrategy,
    FallbackStrategy,
    SkipStrategy
)


class TestRecoveryResult(unittest.TestCase):
    """Test cases for RecoveryResult"""

    def test_success_result(self):
        """Test creating a successful recovery result"""
        # Create a success result
        result = RecoveryResult.success_result("Success message", "result value")
        
        # Check the properties
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Success message")
        self.assertEqual(result.result, "result value")
        self.assertIsNone(result.new_error)
        
    def test_failure_result(self):
        """Test creating a failed recovery result"""
        # Create an error context
        error = ErrorContext(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR
        )
        
        # Create a failure result
        result = RecoveryResult.failure_result("Failure message", error)
        
        # Check the properties
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Failure message")
        self.assertIsNone(result.result)
        self.assertEqual(result.new_error, error)


class TestRetryStrategy(unittest.TestCase):
    """Test cases for RetryStrategy"""

    def test_can_recover(self):
        """Test checking if the strategy can recover from an error"""
        # Create a strategy
        strategy = RetryStrategy()
        
        # Create a recoverable error
        error = ErrorContext(
            message="Network error",
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.ERROR,
            recoverable=True
        )
        
        # Check if the strategy can recover
        self.assertTrue(strategy.can_recover(error))
        
        # Create a non-recoverable error
        error = ErrorContext(
            message="Critical error",
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.CRITICAL,
            recoverable=True
        )
        
        # Check if the strategy can recover
        self.assertFalse(strategy.can_recover(error))
        
        # Create an error in a different category
        error = ErrorContext(
            message="Validation error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
            recoverable=True
        )
        
        # Check if the strategy can recover
        self.assertFalse(strategy.can_recover(error))
        
    def test_recover_success(self):
        """Test recovering from an error successfully"""
        # Create a mock operation that succeeds on the second attempt
        mock_operation = MagicMock()
        mock_operation.side_effect = [
            Exception("First attempt failed"),
            "success"
        ]
        
        # Create a strategy with a mock operation factory
        strategy = RetryStrategy(
            max_retries=3,
            delay_seconds=0.01,  # Use a small delay for testing
            operation_factory=lambda: mock_operation
        )
        
        # Create an error
        error = ErrorContext(
            message="Network error",
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.ERROR
        )
        
        # Recover from the error
        with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up the test
            result = strategy.recover(error, {"args": [], "kwargs": {}})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertEqual(result.result, "success")
        self.assertIn("succeeded after 2 attempts", result.message)
        
        # Check that the operation was called twice
        self.assertEqual(mock_operation.call_count, 2)
        
    def test_recover_failure(self):
        """Test failing to recover from an error"""
        # Create a mock operation that always fails
        mock_operation = MagicMock()
        mock_operation.side_effect = Exception("Operation failed")
        
        # Create a strategy with a mock operation factory
        strategy = RetryStrategy(
            max_retries=2,
            delay_seconds=0.01,  # Use a small delay for testing
            operation_factory=lambda: mock_operation
        )
        
        # Create an error
        error = ErrorContext(
            message="Network error",
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.ERROR
        )
        
        # Recover from the error
        with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up the test
            result = strategy.recover(error, {"args": [], "kwargs": {}})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("failed after 3 attempts", result.message)
        self.assertIsNotNone(result.new_error)
        
        # Check that the operation was called three times
        self.assertEqual(mock_operation.call_count, 3)
        
    def test_recover_no_operation_factory(self):
        """Test recovering with no operation factory"""
        # Create a strategy with no operation factory
        strategy = RetryStrategy()
        
        # Create an error
        error = ErrorContext(
            message="Network error",
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.ERROR
        )
        
        # Recover from the error
        result = strategy.recover(error, {})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("No operation factory provided", result.message)


class TestFallbackStrategy(unittest.TestCase):
    """Test cases for FallbackStrategy"""

    def test_can_recover(self):
        """Test checking if the strategy can recover from an error"""
        # Create a strategy
        strategy = FallbackStrategy(fallback_value="default")
        
        # Create an error in an applicable category
        error = ErrorContext(
            message="Element not found",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.ERROR
        )
        
        # Check if the strategy can recover
        self.assertTrue(strategy.can_recover(error))
        
        # Create an error in a different category
        error = ErrorContext(
            message="Network error",
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.ERROR
        )
        
        # Check if the strategy can recover
        self.assertFalse(strategy.can_recover(error))
        
        # Create a critical error
        error = ErrorContext(
            message="Critical error",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.CRITICAL
        )
        
        # Check if the strategy can recover
        self.assertFalse(strategy.can_recover(error))
        
    def test_recover_with_value(self):
        """Test recovering with a fallback value"""
        # Create a strategy with a fallback value
        strategy = FallbackStrategy(fallback_value="default")
        
        # Create an error
        error = ErrorContext(
            message="Element not found",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.ERROR
        )
        
        # Recover from the error
        result = strategy.recover(error, {})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertEqual(result.result, "default")
        self.assertIn("fallback value", result.message)
        
    def test_recover_with_factory(self):
        """Test recovering with a fallback factory"""
        # Create a strategy with a fallback factory
        strategy = FallbackStrategy(fallback_factory=lambda: "generated")
        
        # Create an error
        error = ErrorContext(
            message="Element not found",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.ERROR
        )
        
        # Recover from the error
        result = strategy.recover(error, {})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertEqual(result.result, "generated")
        self.assertIn("fallback value", result.message)
        
    def test_recover_factory_failure(self):
        """Test recovering with a failing fallback factory"""
        # Create a strategy with a failing fallback factory
        strategy = FallbackStrategy(fallback_factory=lambda: 1/0)  # Will raise ZeroDivisionError
        
        # Create an error
        error = ErrorContext(
            message="Element not found",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.ERROR
        )
        
        # Recover from the error
        result = strategy.recover(error, {})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("Fallback strategy failed", result.message)
        self.assertIsNotNone(result.new_error)
        
    def test_initialization_error(self):
        """Test initializing with no fallback value or factory"""
        # Try to create a strategy with no fallback value or factory
        with self.assertRaises(ValueError):
            FallbackStrategy()


class TestSkipStrategy(unittest.TestCase):
    """Test cases for SkipStrategy"""

    def test_can_recover(self):
        """Test checking if the strategy can recover from an error"""
        # Create a strategy
        strategy = SkipStrategy()
        
        # Create an error in an applicable category
        error = ErrorContext(
            message="Element not found",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.ERROR
        )
        
        # Check if the strategy can recover
        self.assertTrue(strategy.can_recover(error))
        
        # Create an error in a different category
        error = ErrorContext(
            message="Database error",
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.ERROR
        )
        
        # Check if the strategy can recover
        self.assertFalse(strategy.can_recover(error))
        
        # Create a critical error
        error = ErrorContext(
            message="Critical error",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.CRITICAL
        )
        
        # Check if the strategy can recover
        self.assertFalse(strategy.can_recover(error))
        
    def test_recover(self):
        """Test recovering by skipping"""
        # Create a strategy
        strategy = SkipStrategy(skip_message="Skipped due to error")
        
        # Create an error
        error = ErrorContext(
            message="Element not found",
            category=ErrorCategory.ELEMENT_NOT_FOUND,
            severity=ErrorSeverity.ERROR
        )
        
        # Recover from the error
        result = strategy.recover(error, {})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Skipped due to error")
        self.assertIsNone(result.result)


if __name__ == "__main__":
    unittest.main()
