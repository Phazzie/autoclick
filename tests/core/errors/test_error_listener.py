"""Tests for error listeners"""
import pytest
import logging
import os
import json
from unittest.mock import MagicMock, patch

from src.core.errors.error_types import Error, ErrorType, ErrorSeverity
from src.core.errors.error_listener import (
    ErrorEvent,
    ErrorListener,
    CallbackErrorListener,
    CompositeErrorListener
)
from src.core.errors.logging_listener import (
    LoggingErrorListener,
    FileErrorListener
)


def test_error_event_creation():
    """Test creating an error event"""
    # Create an error
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found"
    )
    
    # Create an event
    context = {"key": "value"}
    event = ErrorEvent(error, context)
    
    # Check properties
    assert event.error is error
    assert event.context is context
    assert event.timestamp is not None
    
    # Check string representation
    assert "ErrorEvent" in str(event)
    assert "ELEMENT_NOT_FOUND" in str(event)
    
    # Check dictionary conversion
    event_dict = event.to_dict()
    assert event_dict["error"]["type"] == "ELEMENT_NOT_FOUND"
    assert event_dict["context"] == {"key": "value"}
    assert "timestamp" in event_dict


def test_callback_error_listener():
    """Test callback error listener"""
    # Create a mock callback
    callback = MagicMock(return_value=True)
    
    # Create a listener
    listener = CallbackErrorListener(callback)
    
    # Create an error and event
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found"
    )
    event = ErrorEvent(error)
    
    # Call the listener
    result = listener.on_error(event)
    
    # Check results
    assert result is True
    callback.assert_called_once_with(event)


def test_composite_error_listener():
    """Test composite error listener"""
    # Create mock listeners
    listener1 = MagicMock(spec=ErrorListener)
    listener1.on_error.return_value = False
    
    listener2 = MagicMock(spec=ErrorListener)
    listener2.on_error.return_value = True
    
    listener3 = MagicMock(spec=ErrorListener)
    listener3.on_error.return_value = False
    
    # Create a composite listener
    composite = CompositeErrorListener([listener1, listener2])
    
    # Add another listener
    composite.add_listener(listener3)
    
    # Create an error and event
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found"
    )
    event = ErrorEvent(error)
    
    # Call the listener
    result = composite.on_error(event)
    
    # Check results
    assert result is True
    listener1.on_error.assert_called_once_with(event)
    listener2.on_error.assert_called_once_with(event)
    listener3.on_error.assert_called_once_with(event)
    
    # Remove a listener
    composite.remove_listener(listener2)
    
    # Reset mocks
    listener1.reset_mock()
    listener2.reset_mock()
    listener3.reset_mock()
    
    # Call the listener again
    result = composite.on_error(event)
    
    # Check results
    assert result is False
    listener1.on_error.assert_called_once_with(event)
    listener2.on_error.assert_not_called()
    listener3.on_error.assert_called_once_with(event)


@patch("logging.Logger.error")
@patch("logging.Logger.critical")
@patch("logging.Logger.warning")
@patch("logging.Logger.info")
def test_logging_error_listener(mock_info, mock_warning, mock_critical, mock_error):
    """Test logging error listener"""
    # Create a listener
    listener = LoggingErrorListener()
    
    # Create errors with different severities
    info_error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Info message",
        severity=ErrorSeverity.INFO
    )
    
    warning_error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Warning message",
        severity=ErrorSeverity.WARNING
    )
    
    error_error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Error message",
        severity=ErrorSeverity.ERROR
    )
    
    critical_error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Critical message",
        severity=ErrorSeverity.CRITICAL
    )
    
    fatal_error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Fatal message",
        severity=ErrorSeverity.FATAL
    )
    
    # Call the listener with each error
    listener.on_error(ErrorEvent(info_error))
    listener.on_error(ErrorEvent(warning_error))
    listener.on_error(ErrorEvent(error_error))
    listener.on_error(ErrorEvent(critical_error))
    listener.on_error(ErrorEvent(fatal_error))
    
    # Check that the appropriate log methods were called
    mock_info.assert_called_once()
    mock_warning.assert_called_once()
    mock_error.assert_called_once()
    assert mock_critical.call_count == 2  # Both CRITICAL and FATAL use critical()


def test_file_error_listener(tmpdir):
    """Test file error listener"""
    # Create a temporary file path
    file_path = os.path.join(tmpdir, "error_log.txt")
    
    # Create a listener
    listener = FileErrorListener(file_path)
    
    # Create an error and event
    error = Error(
        error_type=ErrorType.ELEMENT_NOT_FOUND,
        message="Element not found",
        details={"selector": "#my-element"}
    )
    event = ErrorEvent(error, {"browser": "chrome"})
    
    # Call the listener
    result = listener.on_error(event)
    
    # Check results
    assert result is False
    assert os.path.exists(file_path)
    
    # Read the file
    with open(file_path, "r") as f:
        content = f.read()
        
    # Parse the JSON
    log_entry = json.loads(content.strip())
    
    # Check the log entry
    assert log_entry["error"]["type"] == "ELEMENT_NOT_FOUND"
    assert log_entry["error"]["message"] == "Element not found"
    assert log_entry["error"]["details"]["selector"] == "#my-element"
    assert log_entry["context"]["browser"] == "chrome"
    assert "timestamp" in log_entry
    assert "log_timestamp" in log_entry
