"""Tests for the workflow serializer"""
import os
import unittest
import tempfile
import json
from typing import Dict, Any, List

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.workflow.workflow_serializer import WorkflowSerializer


# Create a simple test action for serialization testing
class TestAction(BaseAction):
    """Test action for serialization tests"""

    def __init__(self, description: str, value: str = "", action_id: str = None):
        """Initialize the test action"""
        super().__init__(description, action_id)
        self.value = value

    @property
    def type(self) -> str:
        """Get the action type"""
        return "test_action"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        return ActionResult.create_success(f"Executed: {self.description}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data["value"] = self.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestAction':
        """Create an action from a dictionary"""
        return cls(
            description=data.get("description", ""),
            value=data.get("value", ""),
            action_id=data.get("id")
        )


class TestWorkflowSerializer(unittest.TestCase):
    """Test cases for the workflow serializer"""

    def setUp(self):
        """Set up test environment"""
        self.serializer = WorkflowSerializer()
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a simple workflow for testing
        self.test_workflow = [
            TestAction("Action 1", "value1", "id1"),
            TestAction("Action 2", "value2", "id2"),
            TestAction("Action 3", "value3", "id3")
        ]

        self.test_metadata = {
            "name": "Test Workflow",
            "description": "A test workflow",
            "author": "Test Author",
            "version": "1.0.0"
        }

    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()

    def test_serialize_workflow(self):
        """Test serializing a workflow to a dictionary"""
        # Act
        result = self.serializer.serialize_workflow(self.test_workflow, self.test_metadata)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(result["metadata"]["name"], "Test Workflow")
        self.assertEqual(len(result["actions"]), 3)
        self.assertEqual(result["actions"][0]["id"], "id1")
        self.assertEqual(result["actions"][1]["value"], "value2")
        self.assertEqual(result["schema_version"], "1.0")

    def test_deserialize_workflow(self):
        """Test deserializing a workflow from a dictionary"""
        # Arrange
        serialized = self.serializer.serialize_workflow(self.test_workflow, self.test_metadata)

        # Act
        actions, metadata = self.serializer.deserialize_workflow(serialized)

        # Assert
        self.assertEqual(len(actions), 3)
        # Check that the action is an instance of TestAction
        self.assertEqual(actions[0].__class__.__name__, "TestAction")
        self.assertEqual(actions[0].id, "id1")
        self.assertEqual(actions[1].value, "value2")
        self.assertEqual(metadata["name"], "Test Workflow")

    def test_save_workflow_to_file(self):
        """Test saving a workflow to a file"""
        # Arrange
        file_path = os.path.join(self.temp_dir.name, "test_workflow.json")

        # Act
        self.serializer.save_workflow_to_file(file_path, self.test_workflow, self.test_metadata)

        # Assert
        self.assertTrue(os.path.exists(file_path))

        # Verify file contents
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["metadata"]["name"], "Test Workflow")
            self.assertEqual(len(data["actions"]), 3)

    def test_load_workflow_from_file(self):
        """Test loading a workflow from a file"""
        # Arrange
        file_path = os.path.join(self.temp_dir.name, "test_workflow.json")
        self.serializer.save_workflow_to_file(file_path, self.test_workflow, self.test_metadata)

        # Act
        result = self.serializer.load_workflow_from_file(file_path)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(result["metadata"]["name"], "Test Workflow")
        self.assertEqual(len(result["actions"]), 3)

        # Verify actions were properly loaded
        actions, metadata = self.serializer.deserialize_workflow(result)
        self.assertEqual(len(actions), 3)
        # Check that the action is an instance of TestAction
        self.assertEqual(actions[0].__class__.__name__, "TestAction")
        self.assertEqual(actions[0].id, "id1")

    def test_serialize_complex_workflow(self):
        """Test serializing a workflow with nested actions"""
        # Arrange - create a more complex workflow with nested structure
        from src.core.actions.action_factory import ActionFactory

        # Register the test action with the factory
        ActionFactory.register("test_action")(TestAction)

        # Act
        result = self.serializer.serialize_workflow(self.test_workflow, self.test_metadata)

        # Deserialize using the action factory
        actions, metadata = self.serializer.deserialize_workflow(result, use_factory=True)

        # Assert
        self.assertEqual(len(actions), 3)
        self.assertIsInstance(actions[0], TestAction)
        self.assertEqual(actions[0].id, "id1")
        self.assertEqual(actions[1].value, "value2")

    def test_version_compatibility(self):
        """Test handling different schema versions"""
        # Arrange
        serialized = self.serializer.serialize_workflow(self.test_workflow, self.test_metadata)

        # Modify the schema version
        serialized["schema_version"] = "0.9"

        # Act & Assert
        with self.assertRaises(ValueError):
            self.serializer.deserialize_workflow(serialized, strict_version=True)

        # Should not raise with strict_version=False
        actions, metadata = self.serializer.deserialize_workflow(serialized, strict_version=False)
        self.assertEqual(len(actions), 3)

    def test_invalid_data(self):
        """Test handling invalid data"""
        # Arrange
        invalid_data = {"not_a_workflow": True}

        # Act & Assert
        with self.assertRaises(ValueError):
            self.serializer.deserialize_workflow(invalid_data)

        # Test with missing actions
        invalid_data = {"metadata": {}, "schema_version": "1.0"}
        with self.assertRaises(ValueError):
            self.serializer.deserialize_workflow(invalid_data)


if __name__ == "__main__":
    unittest.main()
