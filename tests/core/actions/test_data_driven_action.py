"""Tests for the data-driven action"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.data_driven_action import DataDrivenAction
from src.core.data.sources.base import DataSource
from src.core.data.mapping.mapper import DataMapper
from src.core.data.iteration.context import DataIterationContext


# Test action for data-driven action tests
class TestAction(BaseAction):
    """Test action for data-driven action tests"""

    def __init__(
        self,
        description: str = "Test action",
        success: bool = True,
        message: str = "Test message",
        action_id: str = None
    ):
        """Initialize the test action"""
        super().__init__(description, action_id)
        self.success = success
        self.message = message
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
        
        if self.success:
            return ActionResult.create_success(self.message)
        else:
            return ActionResult.create_failure(self.message)


class TestDataDrivenAction(unittest.TestCase):
    """Test cases for the DataDrivenAction class"""
    
    def setUp(self):
        """Set up test environment"""
        # Register the DataDrivenAction with the action factory
        from src.core.actions.action_factory import ActionFactory
        factory = ActionFactory.get_instance()
        factory.register_action_type("data_driven", DataDrivenAction)
        
        # Create mock data source
        self.data_source = MagicMock(spec=DataSource)
        self.data_source.__enter__ = MagicMock(return_value=self.data_source)
        self.data_source.__exit__ = MagicMock(return_value=None)
        self.data_source.get_records = MagicMock(return_value=[
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35}
        ])
        
        # Create mock data mapper
        self.data_mapper = MagicMock(spec=DataMapper)
        self.data_mapper.map_record = MagicMock(side_effect=lambda record, context: {
            **context,
            "name": record["name"],
            "age": record["age"]
        })
        
    def test_execute_success(self):
        """Test executing with successful actions"""
        # Create actions
        action1 = TestAction(description="Action 1", success=True)
        action2 = TestAction(description="Action 2", success=True)
        
        # Create a data-driven action
        action = DataDrivenAction(
            description="Test data-driven",
            data_source=self.data_source,
            actions=[action1, action2],
            data_mapper=self.data_mapper
        )
        
        # Execute the action
        result = action.execute({})
        
        # Check the result
        self.assertTrue(result.success)
        self.assertIn("3 records: 3 succeeded, 0 failed", result.message)
        
        # Check that the actions were executed
        self.assertTrue(action1.executed)
        self.assertTrue(action2.executed)
        
    def test_execute_failure(self):
        """Test executing with failed actions"""
        # Create actions
        action1 = TestAction(description="Action 1", success=True)
        action2 = TestAction(description="Action 2", success=False, message="Action 2 failed")
        
        # Create a data-driven action
        action = DataDrivenAction(
            description="Test data-driven",
            data_source=self.data_source,
            actions=[action1, action2],
            data_mapper=self.data_mapper
        )
        
        # Execute the action
        result = action.execute({})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("3 records: 0 succeeded, 3 failed", result.message)
        
        # Check that the actions were executed
        self.assertTrue(action1.executed)
        self.assertTrue(action2.executed)
        
    def test_execute_stop_on_error(self):
        """Test stopping execution on error"""
        # Create actions
        action1 = TestAction(description="Action 1", success=True)
        action2 = TestAction(description="Action 2", success=False, message="Action 2 failed")
        
        # Create a data-driven action that stops on error
        action = DataDrivenAction(
            description="Test data-driven",
            data_source=self.data_source,
            actions=[action1, action2],
            data_mapper=self.data_mapper,
            continue_on_error=False
        )
        
        # Execute the action
        result = action.execute({})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("1 records: 0 succeeded, 1 failed", result.message)
        
    def test_execute_max_errors(self):
        """Test stopping execution after max errors"""
        # Create actions
        action1 = TestAction(description="Action 1", success=True)
        action2 = TestAction(description="Action 2", success=False, message="Action 2 failed")
        
        # Create a data-driven action with max_errors=2
        action = DataDrivenAction(
            description="Test data-driven",
            data_source=self.data_source,
            actions=[action1, action2],
            data_mapper=self.data_mapper,
            max_errors=2
        )
        
        # Execute the action
        result = action.execute({})
        
        # Check the result
        self.assertFalse(result.success)
        self.assertIn("2 records: 0 succeeded, 2 failed", result.message)
        
    def test_results_variable(self):
        """Test storing results in a variable"""
        # Create actions
        action1 = TestAction(description="Action 1", success=True)
        
        # Create a data-driven action
        action = DataDrivenAction(
            description="Test data-driven",
            data_source=self.data_source,
            actions=[action1],
            data_mapper=self.data_mapper,
            results_variable_name="test_results"
        )
        
        # Create a context
        context = {}
        
        # Execute the action
        result = action.execute(context)
        
        # Check that the results were stored in the context
        self.assertIn("test_results", context)
        self.assertIsInstance(context["test_results"], DataIterationContext)
        self.assertEqual(context["test_results"].get_summary()["total"], 3)
        
    def test_results_variable_with_variable_storage(self):
        """Test storing results in a variable with a variable storage object"""
        # Create actions
        action1 = TestAction(description="Action 1", success=True)
        
        # Create a data-driven action
        action = DataDrivenAction(
            description="Test data-driven",
            data_source=self.data_source,
            actions=[action1],
            data_mapper=self.data_mapper,
            results_variable_name="test_results"
        )
        
        # Create a mock variable storage
        variables = MagicMock()
        variables.set = MagicMock()
        
        # Create a context with the variable storage
        context = {"variables": variables}
        
        # Execute the action
        result = action.execute(context)
        
        # Check that the variables.set method was called
        variables.set.assert_called_once()
        self.assertEqual(variables.set.call_args[0][0], "test_results")
        self.assertIsInstance(variables.set.call_args[0][1], DataIterationContext)
        
    def test_serialization(self):
        """Test serializing a DataDrivenAction to dict"""
        # Create actions
        action1 = TestAction(description="Action 1", success=True)
        action2 = TestAction(description="Action 2", success=True)
        
        # Create a data-driven action
        action = DataDrivenAction(
            description="Test data-driven",
            data_source=self.data_source,
            actions=[action1, action2],
            data_mapper=self.data_mapper,
            continue_on_error=False,
            max_errors=2,
            results_variable_name="test_results",
            action_id="test-id"
        )
        
        # Serialize the action
        data = action.to_dict()
        
        # Check the serialized data
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "data_driven")
        self.assertEqual(data["description"], "Test data-driven")
        self.assertEqual(data["continue_on_error"], False)
        self.assertEqual(data["max_errors"], 2)
        self.assertEqual(data["results_variable_name"], "test_results")
        self.assertEqual(len(data["actions"]), 2)
        
    def test_deserialization(self):
        """Test deserializing a dict to DataDrivenAction"""
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
            "type": "data_driven",
            "description": "Test data-driven",
            "actions": [
                {"type": "test_action", "description": "Action 1"},
                {"type": "test_action", "description": "Action 2"}
            ],
            "continue_on_error": False,
            "max_errors": 2,
            "results_variable_name": "test_results",
            "data_source_file": "test.csv"
        }
        
        # Mock the get_instance method
        with patch('src.core.actions.action_factory.ActionFactory.get_instance',
                  return_value=action_factory):
            # Mock the DataSourceFactory
            with patch('src.core.data.sources.base.DataSourceFactory.create_csv_source',
                      return_value=self.data_source):
                # Deserialize the data
                action = DataDrivenAction.from_dict(data)
        
        # Check the deserialized action
        self.assertEqual(action.id, "test-id")
        self.assertEqual(action.description, "Test data-driven")
        self.assertEqual(action.continue_on_error, False)
        self.assertEqual(action.max_errors, 2)
        self.assertEqual(action.results_variable_name, "test_results")
        self.assertEqual(len(action.actions), 2)
        
        # Check that the action factory was called
        self.assertEqual(action_factory.create_action.call_count, 2)


if __name__ == "__main__":
    unittest.main()
