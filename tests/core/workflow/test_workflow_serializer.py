"""Tests for the workflow serializer"""
import unittest
import os
import tempfile
import json
from typing import Dict, Any, List
from unittest.mock import MagicMock, patch

from src.core.actions.base_action import BaseAction
from src.core.actions.click_action import ClickAction
from src.core.actions.action_factory import ActionFactory
from src.core.context.execution_context import ExecutionContext
from src.core.workflow.workflow_serializer import WorkflowSerializer


class TestWorkflowSerializer(unittest.TestCase):
    """Test cases for the workflow serializer"""

    @classmethod
    def setUpClass(cls):
        """Set up the test class"""
        # Reset the action factory registry
        ActionFactory.reset_registry()
        # Register the ClickAction
        factory = ActionFactory.get_instance()
        factory.register_action_type("click", ClickAction)

    def setUp(self):
        """Set up test environment"""
        self.serializer = WorkflowSerializer()
        self.test_actions = [
            ClickAction(description="Click button 1", selector="#button1", action_id="action1"),
            ClickAction(description="Click button 2", selector="#button2", action_id="action2")
        ]
        self.test_context = ExecutionContext(context_id="test-context")
        self.test_metadata = {
            "name": "Test Workflow",
            "description": "A test workflow",
            "author": "Test User"
        }

    def test_serialize_workflow(self):
        """Test serializing a workflow to a dictionary"""
        # Act
        result = self.serializer.serialize_workflow(
            self.test_actions,
            self.test_context,
            self.test_metadata
        )

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("metadata", result)
        self.assertIn("actions", result)
        self.assertIn("context", result)

        # Check metadata
        self.assertEqual(result["metadata"]["name"], "Test Workflow")
        self.assertEqual(result["metadata"]["description"], "A test workflow")
        self.assertEqual(result["metadata"]["author"], "Test User")
        self.assertEqual(result["metadata"]["action_count"], 2)
        self.assertIn("version", result["metadata"])
        self.assertIn("created_at", result["metadata"])

        # Check actions
        self.assertEqual(len(result["actions"]), 2)
        self.assertEqual(result["actions"][0]["id"], "action1")
        self.assertEqual(result["actions"][0]["type"], "click")
        self.assertEqual(result["actions"][0]["selector"], "#button1")
        self.assertEqual(result["actions"][1]["id"], "action2")
        self.assertEqual(result["actions"][1]["type"], "click")
        self.assertEqual(result["actions"][1]["selector"], "#button2")

        # Check context
        self.assertEqual(result["context"]["id"], "test-context")

    def test_serialize_workflow_without_context(self):
        """Test serializing a workflow without a context"""
        # Act
        result = self.serializer.serialize_workflow(
            self.test_actions,
            metadata=self.test_metadata
        )

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("metadata", result)
        self.assertIn("actions", result)
        self.assertNotIn("context", result)

    def test_serialize_workflow_without_metadata(self):
        """Test serializing a workflow without metadata"""
        # Act
        result = self.serializer.serialize_workflow(
            self.test_actions,
            self.test_context
        )

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("metadata", result)
        self.assertIn("actions", result)
        self.assertIn("context", result)

        # Check default metadata
        self.assertIn("version", result["metadata"])
        self.assertIn("created_at", result["metadata"])
        self.assertEqual(result["metadata"]["action_count"], 2)

    @patch('src.core.actions.action_factory.ActionFactory')
    def test_deserialize_workflow(self, mock_factory_class):
        """Test deserializing a workflow from a dictionary"""
        # Arrange
        mock_factory = MagicMock()
        mock_factory_class.get_instance.return_value = mock_factory

        # Mock the create_action method to return the actions
        mock_factory.create_action.side_effect = lambda data: ClickAction(
            description=data.get("description", ""),
            selector=data.get("selector", ""),
            action_id=data.get("id")
        )

        # Create a workflow dictionary
        workflow_dict = {
            "metadata": {
                "name": "Test Workflow",
                "description": "A test workflow",
                "author": "Test User",
                "version": "1.0.0",
                "created_at": "2023-01-01T00:00:00",
                "action_count": 2
            },
            "actions": [
                {
                    "id": "action1",
                    "type": "click",
                    "description": "Click button 1",
                    "selector": "#button1"
                },
                {
                    "id": "action2",
                    "type": "click",
                    "description": "Click button 2",
                    "selector": "#button2"
                }
            ],
            "context": self.test_context.to_dict()
        }

        # Act
        result = self.serializer.deserialize_workflow(workflow_dict)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("actions", result)
        self.assertIn("context", result)
        self.assertIn("metadata", result)

        # Check actions
        self.assertEqual(len(result["actions"]), 2)
        self.assertEqual(result["actions"][0].id, "action1")
        self.assertEqual(result["actions"][0].type, "click")
        self.assertEqual(result["actions"][0].description, "Click button 1")
        self.assertEqual(result["actions"][1].id, "action2")
        self.assertEqual(result["actions"][1].type, "click")
        self.assertEqual(result["actions"][1].description, "Click button 2")

        # Check context
        self.assertEqual(result["context"].id, "test-context")

        # Check metadata
        self.assertEqual(result["metadata"]["name"], "Test Workflow")
        self.assertEqual(result["metadata"]["description"], "A test workflow")
        self.assertEqual(result["metadata"]["author"], "Test User")

    def test_deserialize_workflow_invalid_input(self):
        """Test deserializing an invalid workflow"""
        # Test with non-dictionary input
        with self.assertRaises(ValueError):
            self.serializer.deserialize_workflow("not a dictionary")

        # Test with missing actions key
        with self.assertRaises(ValueError):
            self.serializer.deserialize_workflow({"metadata": {}})

        # Test with non-list actions
        with self.assertRaises(ValueError):
            self.serializer.deserialize_workflow({"actions": "not a list"})

    def test_save_and_load_workflow(self):
        """Test saving and loading a workflow to/from a file"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_path = temp_file.name

        try:
            # Save the workflow
            self.serializer.save_workflow_to_file(
                temp_path,
                self.test_actions,
                self.test_context,
                self.test_metadata
            )

            # Check that the file exists and contains valid JSON
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, 'r') as f:
                file_content = f.read()
                json_content = json.loads(file_content)
                self.assertIsInstance(json_content, dict)
                self.assertIn("metadata", json_content)
                self.assertIn("actions", json_content)
                self.assertIn("context", json_content)

            # Mock the deserialize_workflow method to return a known result
            expected_result = {
                "actions": self.test_actions,
                "context": self.test_context,
                "metadata": self.test_metadata
            }

            with patch.object(self.serializer, 'deserialize_workflow', return_value=expected_result):
                # Load the workflow
                result = self.serializer.load_workflow_from_file(temp_path)

                # Assert
                self.assertEqual(result, expected_result)

        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @patch('builtins.open')
    def test_save_workflow_file_error(self, mock_open):
        """Test error handling when saving a workflow to a file"""
        # Make open raise an IOError
        mock_open.side_effect = IOError("Test file error")

        # Try to save the workflow
        with self.assertRaises(IOError):
            self.serializer.save_workflow_to_file(
                "test_workflow.json",
                self.test_actions
            )

    def test_load_workflow_file_error(self):
        """Test error handling when loading a workflow from a file"""
        # Try to load from a non-existent file
        with self.assertRaises(IOError):
            self.serializer.load_workflow_from_file("/non/existent/workflow.json")


if __name__ == "__main__":
    unittest.main()
