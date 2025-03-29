"""Tests for error types"""
import pytest
from datetime import datetime

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity


def test_error_creation():
    """Test creating an error"""
    # Create a basic error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found",
        severity=ErrorSeverity.ERROR,
        details={"selector": "#my-element"},
        source="test_module"
    )
    
    # Check properties
    assert error.error_type == ErrorType.ELEMENT_NOT_FOUND
    assert error.message == "Element not found"
    assert error.severity == ErrorSeverity.ERROR
    assert error.details == {"selector": "#my-element"}
    assert error.source == "test_module"
    assert error.exception is None
    assert isinstance(error.timestamp, datetime)
    
    # Check string representation
    assert str(error) == "ELEMENT_NOT_FOUND: Element not found (ERROR)"


def test_error_from_exception():
    """Test creating an error from an exception"""
    # Create an exception
    exception = ValueError("Invalid value")
    
    # Create an error from the exception
    error = Error.from_exception(
        exception=exception,
        error_type=ErrorType.VALIDATION_ERROR,
        severity=ErrorSeverity.WARNING,
        source="test_module",
        details={"field": "username"}
    )
    
    # Check properties
    assert error.error_type == ErrorType.VALIDATION_ERROR
    assert error.message == "Invalid value"
    assert error.severity == ErrorSeverity.WARNING
    assert error.details == {"field": "username"}
    assert error.source == "test_module"
    assert error.exception is exception
    assert isinstance(error.timestamp, datetime)


def test_error_to_dict():
    """Test converting an error to a dictionary"""
    # Create an error
    error = Error(
        error_type=ErrorType.NETWORK_ERROR,
        message="Connection failed",
        severity=ErrorSeverity.CRITICAL,
        details={"url": "https://example.com"},
        source="test_module"
    )
    
    # Convert to dictionary
    error_dict = error.to_dict()
    
    # Check dictionary contents
    assert error_dict["type"] == "NETWORK_ERROR"
    assert error_dict["message"] == "Connection failed"
    assert error_dict["severity"] == "CRITICAL"
    assert error_dict["details"] == {"url": "https://example.com"}
    assert error_dict["source"] == "test_module"
    assert error_dict["exception"] is None
    assert isinstance(error_dict["timestamp"], str)
