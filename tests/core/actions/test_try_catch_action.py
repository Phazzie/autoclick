"""Tests for the try-catch action"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.try_catch_action import TryCatchAction
from src.core.error.error_types import ErrorContext, ErrorCategory, ErrorSeverity


# Test action for try-catch action tests
class TestAction(BaseAction):
    """Test action for try-catch action tests"""

    def __init__(
        self,
        description: str = "Test action",
        success: bool = True,
        message: str = "Test message",
        exception: bool = False,
        action_id: str = None
    ):
        """Initialize the test action"""
        super().__init__(description, action_id)
        self.success = success
        self.message = message
        self.exception = exception
        self.executed = False
        self.last_context = None

    @property
    def type(self) -> str:
        """Get the action type"""
        return "test_action"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        self.executed = True
        self.last_context = context.copy() if isinstance(context, dict) else None
        
        if self.exception:
            raise Exception(self.message)
            
        if self.success:
            return ActionResult.create_success(self.message)
        else:
            return ActionResult.create_failure(self.message)


class TestTryCatchAction(unittest.TestCase):
    """Test cases for the TryCatchAction class"""
    
    def setUp(self):
        """Set up test environment"""
        # Register the TryCatchAction with the action factory
        from src.core.actions.action_factory import ActionFactory
        factory = ActionFactory.get_instance()
        factory.register_action_type("try_catch", TryCatchAction)
        
    def test_try_success(self):
        """Test executing the try block successfully"""
        # Create actions
        try_action1 = TestAction(description="Try action 1", success=True)
        try_action2 = TestAction(description="Try action 2", success=True)
        catch_action = TestAction(description="Catch action")
        finally_action = TestAction(description="Finally action")
        
        # Create the try-catch action
        action = TryCatchAction(
            description="Test try-catch",
            try_actions=[try_action1, try_action2],
            catch_actions=[catch_action],
            finally_actions=[finally_action]
        )
        
        # Execute the action
        result = action.execute({})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertIn("Try block executed successfully", result.message)
        
        # Check that the try actions were executed
        self.assertTrue(try_action1.executed)
        self.assertTrue(try_action2.executed)
        
        # Check that the catch action was not executed
        self.assertFalse(catch_action.executed)
        
        # Check that the finally action was executed
        self.assertTrue(finally_action.executed)
        
    def test_try_failure(self):
        """Test executing the try block with a failure"""
        # Create actions
        try_action1 = TestAction(description="Try action 1", success=True)
        try_action2 = TestAction(description="Try action 2", success=False, message="Action failed")
        try_action3 = TestAction(description="Try action 3", success=True)
        catch_action = TestAction(description="Catch action")
        finally_action = TestAction(description="Finally action")
        
        # Create the try-catch action
        action = TryCatchAction(
            description="Test try-catch",
            try_actions=[try_action1, try_action2, try_action3],
            catch_actions=[catch_action],
            finally_actions=[finally_action],
            error_variable_name="error"
        )
        
        # Create a context
        context = {}
        
        # Execute the action
        result = action.execute(context)
        
        # Check the result
        self.assertTrue(result.success)
        self.assertIn("Error occurred but was handled successfully", result.message)
        
        # Check that the try actions were executed correctly
        self.assertTrue(try_action1.executed)
        self.assertTrue(try_action2.executed)
        self.assertFalse(try_action3.executed)  # Should not be executed after failure
        
        # Check that the catch action was executed
        self.assertTrue(catch_action.executed)
        
        # Check that the finally action was executed
        self.assertTrue(finally_action.executed)
        
        # Check that the error was stored in the context
        self.assertIn("error", context)
        self.assertEqual(context["error"]["message"], "Action failed")
        self.assertEqual(context["error"]["category"], "EXECUTION")
        
    def test_try_exception(self):
        """Test executing the try block with an exception"""
        # Create actions
        try_action1 = TestAction(description="Try action 1", success=True)
        try_action2 = TestAction(
            description="Try action 2",
            exception=True,
            message="Test exception"
        )
        try_action3 = TestAction(description="Try action 3", success=True)
        catch_action = TestAction(description="Catch action")
        finally_action = TestAction(description="Finally action")
        
        # Create the try-catch action
        action = TryCatchAction(
            description="Test try-catch",
            try_actions=[try_action1, try_action2, try_action3],
            catch_actions=[catch_action],
            finally_actions=[finally_action],
            error_variable_name="error"
        )
        
        # Create a context
        context = {}
        
        # Execute the action
        result = action.execute(context)
        
        # Check the result
        self.assertTrue(result.success)
        self.assertIn("Error occurred but was handled successfully", result.message)
        
        # Check that the try actions were executed correctly
        self.assertTrue(try_action1.executed)
        self.assertTrue(try_action2.executed)
        self.assertFalse(try_action3.executed)  # Should not be executed after exception
        
        # Check that the catch action was executed
        self.assertTrue(catch_action.executed)
        
        # Check that the finally action was executed
        self.assertTrue(finally_action.executed)
        
        # Check that the error was stored in the context
        self.assertIn("error", context)
        self.assertEqual(context["error"]["message"], "Test exception")
        self.assertEqual(context["error"]["category"], "EXECUTION")
        
    def test_catch_failure(self):
        """Test executing the catch block with a failure"""
        # Create actions
        try_action = TestAction(description="Try action", success=False, message="Try failed")
        catch_action1 = TestAction(description="Catch action 1", success=True)
        catch_action2 = TestAction(description="Catch action 2", success=False, message="Catch failed")
        finally_action = TestAction(description="Finally action")
        
        # Create the try-catch action
        action = TryCatchAction(
            description="Test try-catch",
            try_actions=[try_action],
            catch_actions=[catch_action1, catch_action2],
            finally_actions=[finally_action]
        )
        
        # Execute the action
        result = action.execute({})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("Error occurred and catch actions failed", result.message)
        
        # Check that the try action was executed
        self.assertTrue(try_action.executed)
        
        # Check that the catch actions were executed
        self.assertTrue(catch_action1.executed)
        self.assertTrue(catch_action2.executed)
        
        # Check that the finally action was executed
        self.assertTrue(finally_action.executed)
        
    def test_finally_failure(self):
        """Test executing the finally block with a failure"""
        # Create actions
        try_action = TestAction(description="Try action", success=True)
        catch_action = TestAction(description="Catch action")
        finally_action = TestAction(description="Finally action", success=False, message="Finally failed")
        
        # Create the try-catch action
        action = TryCatchAction(
            description="Test try-catch",
            try_actions=[try_action],
            catch_actions=[catch_action],
            finally_actions=[finally_action]
        )
        
        # Execute the action
        result = action.execute({})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertIn("Try block executed successfully", result.message)
        
        # Check that the try action was executed
        self.assertTrue(try_action.executed)
        
        # Check that the catch action was not executed
        self.assertFalse(catch_action.executed)
        
        # Check that the finally action was executed
        self.assertTrue(finally_action.executed)
        
    def test_variables_context(self):
        """Test using a variables object in the context"""
        # Create a mock variables object
        variables = MagicMock()
        variables.set = MagicMock()
        
        # Create actions
        try_action = TestAction(description="Try action", success=False, message="Try failed")
        catch_action = TestAction(description="Catch action")
        
        # Create the try-catch action
        action = TryCatchAction(
            description="Test try-catch",
            try_actions=[try_action],
            catch_actions=[catch_action],
            error_variable_name="error"
        )
        
        # Create a context with the variables object
        context = {"variables": variables}
        
        # Execute the action
        result = action.execute(context)
        
        # Check that the variables.set method was called
        variables.set.assert_called_once()
        self.assertEqual(variables.set.call_args[0][0], "error")
        
    def test_serialization(self):
        """Test serializing a TryCatchAction to dict"""
        # Create actions
        try_action = TestAction(description="Try action")
        catch_action = TestAction(description="Catch action")
        finally_action = TestAction(description="Finally action")
        
        # Create the try-catch action
        action = TryCatchAction(
            description="Test try-catch",
            try_actions=[try_action],
            catch_actions=[catch_action],
            finally_actions=[finally_action],
            error_variable_name="error",
            action_id="test-id"
        )
        
        # Serialize the action
        data = action.to_dict()
        
        # Check the serialized data
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "try_catch")
        self.assertEqual(data["description"], "Test try-catch")
        self.assertEqual(data["error_variable_name"], "error")
        self.assertEqual(len(data["try_actions"]), 1)
        self.assertEqual(len(data["catch_actions"]), 1)
        self.assertEqual(len(data["finally_actions"]), 1)
        
    def test_deserialization(self):
        """Test deserializing a dict to TryCatchAction"""
        # Create a mock action factory
        action_factory = MagicMock()
        
        # Mock the create_action method
        action_factory.create_action.side_effect = lambda data: TestAction(
            description=data.get("description", ""),
            action_id=data.get("id")
        )
        
        # Create serialized data
        data = {
            "id": "test-id",
            "type": "try_catch",
            "description": "Test try-catch",
            "try_actions": [
                {"type": "test_action", "description": "Try action"}
            ],
            "catch_actions": [
                {"type": "test_action", "description": "Catch action"}
            ],
            "finally_actions": [
                {"type": "test_action", "description": "Finally action"}
            ],
            "error_variable_name": "error"
        }
        
        # Mock the get_instance method
        with patch('src.core.actions.action_factory.ActionFactory.get_instance',
                  return_value=action_factory):
            # Deserialize the data
            action = TryCatchAction.from_dict(data)
        
        # Check the deserialized action
        self.assertEqual(action.id, "test-id")
        self.assertEqual(action.description, "Test try-catch")
        self.assertEqual(action.error_variable_name, "error")
        self.assertEqual(len(action.try_actions), 1)
        self.assertEqual(len(action.catch_actions), 1)
        self.assertEqual(len(action.finally_actions), 1)


if __name__ == "__main__":
    unittest.main()
