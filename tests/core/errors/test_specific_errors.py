"""Tests for specific error types"""
import pytest

from src.core.errors.error_types import ErrorType, ErrorSeverity
from src.core.errors.element_errors import (
    ElementNotFoundError,
    ElementNotVisibleError,
    ElementNotClickableError,
    ElementStaleError
)
from src.core.errors.timeout_errors import (
    TimeoutError,
    WaitTimeoutError,
    PageLoadTimeoutError
)
from src.core.errors.workflow_errors import (
    WorkflowError,
    ActionError,
    ConditionError
)


def test_element_not_found_error():
    """Test element not found error"""
    # Create an error with default message
    error = ElementNotFoundError(selector="#my-element")
    
    # Check properties
    assert error.error_type == ErrorType.ELEMENT_NOT_FOUND
    assert "Element not found" in error.message
    assert "#my-element" in error.message
    assert error.details["selector"] == "#my-element"
    
    # Create an error with custom message
    error = ElementNotFoundError(
        selector="#my-element",
        message="Custom error message",
        details={"page": "login"},
        source="test_module"
    )
    
    # Check properties
    assert error.error_type == ErrorType.ELEMENT_NOT_FOUND
    assert error.message == "Custom error message"
    assert error.details["selector"] == "#my-element"
    assert error.details["page"] == "login"
    assert error.source == "test_module"


def test_element_not_visible_error():
    """Test element not visible error"""
    # Create an error with default message
    error = ElementNotVisibleError(selector="#my-element")
    
    # Check properties
    assert error.error_type == ErrorType.ELEMENT_NOT_VISIBLE
    assert "not visible" in error.message
    assert "#my-element" in error.message
    assert error.details["selector"] == "#my-element"


def test_element_not_clickable_error():
    """Test element not clickable error"""
    # Create an error with default message
    error = ElementNotClickableError(selector="#my-element")
    
    # Check properties
    assert error.error_type == ErrorType.ELEMENT_NOT_CLICKABLE
    assert "not clickable" in error.message
    assert "#my-element" in error.message
    assert error.details["selector"] == "#my-element"


def test_element_stale_error():
    """Test element stale error"""
    # Create an error with default message
    error = ElementStaleError(selector="#my-element")
    
    # Check properties
    assert error.error_type == ErrorType.ELEMENT_STALE
    assert "stale" in error.message
    assert "#my-element" in error.message
    assert error.details["selector"] == "#my-element"


def test_timeout_error():
    """Test timeout error"""
    # Create an error with default message
    error = TimeoutError(operation="click", timeout_seconds=10)
    
    # Check properties
    assert error.error_type == ErrorType.TIMEOUT
    assert "timed out" in error.message
    assert "10 seconds" in error.message
    assert error.details["operation"] == "click"
    assert error.details["timeout_seconds"] == 10


def test_wait_timeout_error():
    """Test wait timeout error"""
    # Create an error with default message
    error = WaitTimeoutError(condition="element to be visible", timeout_seconds=5)
    
    # Check properties
    assert error.error_type == ErrorType.WAIT_TIMEOUT
    assert "timed out" in error.message
    assert "5 seconds" in error.message
    assert error.details["condition"] == "element to be visible"
    assert error.details["timeout_seconds"] == 5


def test_page_load_timeout_error():
    """Test page load timeout error"""
    # Create an error with default message
    error = PageLoadTimeoutError(url="https://example.com", timeout_seconds=30)
    
    # Check properties
    assert error.error_type == ErrorType.PAGE_LOAD_TIMEOUT
    assert "timed out" in error.message
    assert "30 seconds" in error.message
    assert error.details["url"] == "https://example.com"
    assert error.details["timeout_seconds"] == 30


def test_workflow_error():
    """Test workflow error"""
    # Create an error
    error = WorkflowError(
        workflow_id="workflow_123",
        message="Workflow execution failed",
        details={"step": "login"},
        source="test_module"
    )
    
    # Check properties
    assert error.error_type == ErrorType.WORKFLOW_ERROR
    assert error.message == "Workflow execution failed"
    assert error.details["workflow_id"] == "workflow_123"
    assert error.details["step"] == "login"
    assert error.source == "test_module"


def test_action_error():
    """Test action error"""
    # Create an error
    error = ActionError(
        action_id="action_123",
        action_type="click",
        message="Action execution failed",
        details={"selector": "#my-element"},
        source="test_module"
    )
    
    # Check properties
    assert error.error_type == ErrorType.ACTION_ERROR
    assert error.message == "Action execution failed"
    assert error.details["action_id"] == "action_123"
    assert error.details["action_type"] == "click"
    assert error.details["selector"] == "#my-element"
    assert error.source == "test_module"


def test_condition_error():
    """Test condition error"""
    # Create an error
    error = ConditionError(
        condition_id="condition_123",
        condition_type="element_exists",
        message="Condition evaluation failed",
        details={"selector": "#my-element"},
        source="test_module"
    )
    
    # Check properties
    assert error.error_type == ErrorType.CONDITION_ERROR
    assert error.message == "Condition evaluation failed"
    assert error.details["condition_id"] == "condition_123"
    assert error.details["condition_type"] == "element_exists"
    assert error.details["selector"] == "#my-element"
    assert error.source == "test_module"
