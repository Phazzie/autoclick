"""Tests for the retry action"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.retry_action_impl import RetryAction


# Test action for retry action tests
class TestAction(BaseAction):
    """Test action for retry action tests"""

    def __init__(
        self,
        description: str = "Test action",
        success_pattern: list = None,
        action_id: str = None
    ):
        """
        Initialize the test action
        
        Args:
            description: Description of the action
            success_pattern: List of booleans indicating success/failure pattern
                             for successive executions
            action_id: Optional action ID
        """
        super().__init__(description, action_id)
        self.success_pattern = success_pattern or [True]
        self.execution_count = 0
        self.last_context = None

    @property
    def type(self) -> str:
        """Get the action type"""
        return "test_action"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        self.last_context = context.copy() if isinstance(context, dict) else None
        
        # Get the success value for this execution
        success = self.success_pattern[min(self.execution_count, len(self.success_pattern) - 1)]
        self.execution_count += 1
        
        if success:
            return ActionResult.create_success(
                f"Execution {self.execution_count} succeeded",
                {"execution_count": self.execution_count}
            )
        else:
            return ActionResult.create_failure(
                f"Execution {self.execution_count} failed",
                {"execution_count": self.execution_count}
            )


class TestRetryAction(unittest.TestCase):
    """Test cases for the RetryAction class"""
    
    def setUp(self):
        """Set up test environment"""
        # Register the RetryAction with the action factory
        from src.core.actions.action_factory import ActionFactory
        factory = ActionFactory.get_instance()
        factory.register_action_type("retry", RetryAction)
        
    def test_success_first_attempt(self):
        """Test executing an action that succeeds on the first attempt"""
        # Create an action that succeeds
        action = TestAction(success_pattern=[True])
        
        # Create a retry action
        retry_action = RetryAction(
            description="Test retry",
            action=action,
            max_retries=3
        )
        
        # Execute the retry action
        result = retry_action.execute({})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertIn("succeeded after 1 attempts", result.message)
        
        # Check that the action was executed once
        self.assertEqual(action.execution_count, 1)
        
    def test_success_after_retries(self):
        """Test executing an action that succeeds after some retries"""
        # Create an action that fails twice then succeeds
        action = TestAction(success_pattern=[False, False, True])
        
        # Create a retry action
        retry_action = RetryAction(
            description="Test retry",
            action=action,
            max_retries=3,
            delay_seconds=0.01  # Use a small delay for testing
        )
        
        # Execute the retry action
        with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up the test
            result = retry_action.execute({})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertIn("succeeded after 3 attempts", result.message)
        
        # Check that the action was executed three times
        self.assertEqual(action.execution_count, 3)
        
        # Check that sleep was called twice (once after each failure)
        self.assertEqual(mock_sleep.call_count, 2)
        
    def test_failure_all_attempts(self):
        """Test executing an action that fails on all attempts"""
        # Create an action that always fails
        action = TestAction(success_pattern=[False])
        
        # Create a retry action
        retry_action = RetryAction(
            description="Test retry",
            action=action,
            max_retries=2,
            delay_seconds=0.01  # Use a small delay for testing
        )
        
        # Execute the retry action
        with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up the test
            result = retry_action.execute({})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("failed after 3 attempts", result.message)
        
        # Check that the action was executed three times (initial + 2 retries)
        self.assertEqual(action.execution_count, 3)
        
        # Check that sleep was called twice (once after each failure)
        self.assertEqual(mock_sleep.call_count, 2)
        
    def test_backoff(self):
        """Test that the delay increases with each retry"""
        # Create an action that always fails
        action = TestAction(success_pattern=[False])
        
        # Create a retry action with backoff
        retry_action = RetryAction(
            description="Test retry",
            action=action,
            max_retries=2,
            delay_seconds=1.0,
            backoff_factor=2.0
        )
        
        # Execute the retry action
        with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up the test
            result = retry_action.execute({})
        
        # Check that sleep was called with increasing delays
        mock_sleep.assert_any_call(1.0)  # First retry
        mock_sleep.assert_any_call(2.0)  # Second retry (1.0 * 2.0)
        
    def test_variables(self):
        """Test that variables are updated correctly"""
        # Create an action that fails then succeeds
        action = TestAction(success_pattern=[False, True])
        
        # Create a retry action with variables
        retry_action = RetryAction(
            description="Test retry",
            action=action,
            max_retries=3,
            delay_seconds=0.01,
            success_variable_name="success",
            attempts_variable_name="attempts"
        )
        
        # Create a context
        context = {}
        
        # Execute the retry action
        with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up the test
            result = retry_action.execute(context)
        
        # Check the result
        self.assertTrue(result.success)
        
        # Check that the variables were updated
        self.assertIn("success", context)
        self.assertIn("attempts", context)
        self.assertTrue(context["success"])
        self.assertEqual(context["attempts"], 2)
        
    def test_variables_with_variable_storage(self):
        """Test that variables are updated correctly when using a variable storage object"""
        # Create an action that fails then succeeds
        action = TestAction(success_pattern=[False, True])
        
        # Create a mock variable storage
        variables = MagicMock()
        variables.set = MagicMock()
        
        # Create a retry action with variables
        retry_action = RetryAction(
            description="Test retry",
            action=action,
            max_retries=3,
            delay_seconds=0.01,
            success_variable_name="success",
            attempts_variable_name="attempts"
        )
        
        # Create a context with the variable storage
        context = {"variables": variables}
        
        # Execute the retry action
        with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up the test
            result = retry_action.execute(context)
        
        # Check that the variables were updated
        variables.set.assert_any_call("success", True)
        variables.set.assert_any_call("attempts", 2)
        
    def test_serialization(self):
        """Test serializing a RetryAction to dict"""
        # Create an action
        action = TestAction()
        
        # Create a retry action
        retry_action = RetryAction(
            description="Test retry",
            action=action,
            max_retries=3,
            delay_seconds=1.5,
            backoff_factor=2.0,
            success_variable_name="success",
            attempts_variable_name="attempts",
            action_id="test-id"
        )
        
        # Serialize the action
        data = retry_action.to_dict()
        
        # Check the serialized data
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "retry")
        self.assertEqual(data["description"], "Test retry")
        self.assertEqual(data["max_retries"], 3)
        self.assertEqual(data["delay_seconds"], 1.5)
        self.assertEqual(data["backoff_factor"], 2.0)
        self.assertEqual(data["success_variable_name"], "success")
        self.assertEqual(data["attempts_variable_name"], "attempts")
        self.assertEqual(data["action"]["type"], "test_action")
        
    def test_deserialization(self):
        """Test deserializing a dict to RetryAction"""
        # Create a mock action factory
        action_factory = MagicMock()
        
        # Mock the create_action method
        action_factory.create_action.return_value = TestAction(
            description="Deserialized action"
        )
        
        # Create serialized data
        data = {
            "id": "test-id",
            "type": "retry",
            "description": "Test retry",
            "action": {"type": "test_action", "description": "Test action"},
            "max_retries": 3,
            "delay_seconds": 1.5,
            "backoff_factor": 2.0,
            "success_variable_name": "success",
            "attempts_variable_name": "attempts"
        }
        
        # Mock the get_instance method
        with patch('src.core.actions.action_factory.ActionFactory.get_instance',
                  return_value=action_factory):
            # Deserialize the data
            action = RetryAction.from_dict(data)
        
        # Check the deserialized action
        self.assertEqual(action.id, "test-id")
        self.assertEqual(action.description, "Test retry")
        self.assertEqual(action.max_retries, 3)
        self.assertEqual(action.delay_seconds, 1.5)
        self.assertEqual(action.backoff_factor, 2.0)
        self.assertEqual(action.success_variable_name, "success")
        self.assertEqual(action.attempts_variable_name, "attempts")
        
        # Check that the action factory was called
        action_factory.create_action.assert_called_once_with(data["action"])


if __name__ == "__main__":
    unittest.main()
