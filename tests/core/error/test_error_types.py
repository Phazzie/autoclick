"""Tests for error types"""
import unittest
from datetime import datetime

from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity


class TestErrorTypes(unittest.TestCase):
    """Test cases for error types"""

    def test_error_context_creation(self):
        """Test creating an error context"""
        # Create an error context
        context = ErrorContext(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.WARNING,
            context={"field": "email"}
        )
        
        # Check the properties
        self.assertEqual(context.message, "Test error")
        self.assertEqual(context.category, ErrorCategory.VALIDATION)
        self.assertEqual(context.severity, ErrorSeverity.WARNING)
        self.assertEqual(context.context, {"field": "email"})
        self.assertTrue(context.recoverable)
        self.assertIsNone(context.timestamp)
        
    def test_error_context_from_exception(self):
        """Test creating an error context from an exception"""
        # Create an exception
        exception = ValueError("Invalid value")
        
        # Create an error context from the exception
        context = ErrorContext.from_exception(
            exception,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR
        )
        
        # Check the properties
        self.assertEqual(context.message, "Invalid value")
        self.assertEqual(context.category, ErrorCategory.VALIDATION)
        self.assertEqual(context.severity, ErrorSeverity.ERROR)
        self.assertEqual(context.exception, exception)
        self.assertTrue(context.recoverable)
        
    def test_error_context_to_dict(self):
        """Test converting an error context to a dictionary"""
        # Create an error context
        context = ErrorContext(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.WARNING,
            context={"field": "email"}
        )
        
        # Set the timestamp
        context.timestamp = datetime.now()
        
        # Convert to a dictionary
        data = context.to_dict()
        
        # Check the dictionary
        self.assertEqual(data["message"], "Test error")
        self.assertEqual(data["category"], "VALIDATION")
        self.assertEqual(data["severity"], "WARNING")
        self.assertEqual(data["context"], {"field": "email"})
        self.assertTrue(data["recoverable"])
        self.assertIsNotNone(data["timestamp"])
        
    def test_error_context_str(self):
        """Test the string representation of an error context"""
        # Create an error context
        context = ErrorContext(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.WARNING,
            context={"field": "email"}
        )
        
        # Check the string representation
        self.assertEqual(str(context), "WARNING [VALIDATION]: Test error (Recoverable)")
        
        # Create a non-recoverable error context
        context = ErrorContext(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.WARNING,
            recoverable=False
        )
        
        # Check the string representation
        self.assertEqual(str(context), "WARNING [VALIDATION]: Test error (Non-recoverable)")


if __name__ == "__main__":
    unittest.main()
