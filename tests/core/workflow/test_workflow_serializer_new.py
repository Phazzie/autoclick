"""
Tests for the workflow serializer implementation.

This module contains tests for the workflow serializer implementation.
"""
import unittest
import json
from unittest.mock import Mock, patch

from src.core.workflow.workflow_serializer_new import WorkflowSerializer
from src.core.workflow.service_exceptions import WorkflowSerializationError, WorkflowDeserializationError


class TestWorkflowSerializer(unittest.TestCase):
    """Tests for the WorkflowSerializer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock workflow engine
        self.engine = Mock()
        
        # Create the serializer
        self.serializer = WorkflowSerializer(self.engine)
        
        # Create mock workflows and steps
        self.workflow = Mock()
        self.workflow.workflow_id = "test-workflow"
        self.workflow.name = "Test Workflow"
        self.workflow.description = "Test workflow description"
        self.workflow.version = "1.0.0"
        self.workflow.enabled = True
        self.workflow.metadata = {"key": "value"}
        
        self.step1 = Mock()
        self.step1.step_id = "step1"
        self.step1.step_type = "test"
        self.step1.name = "Step 1"
        self.step1.description = "Test step 1"
        self.step1.enabled = True
        self.step1.config = {"param1": "value1"}
        self.step1.metadata = {"key1": "value1"}
        
        self.step2 = Mock()
        self.step2.step_id = "step2"
        self.step2.step_type = "test"
        self.step2.name = "Step 2"
        self.step2.description = "Test step 2"
        self.step2.enabled = True
        self.step2.config = {"param2": "value2"}
        self.step2.metadata = {"key2": "value2"}
        
        # Configure the workflow
        self.workflow.get_steps.return_value = [self.step1, self.step2]
        
        # Configure the engine
        self.engine.create_workflow.return_value = self.workflow
        self.engine.create_step.side_effect = lambda data: {
            "step1": self.step1,
            "step2": self.step2
        }.get(data.get("step_id"))
    
    def test_serialize_workflow(self):
        """Test serializing a workflow."""
        # Serialize the workflow
        data = self.serializer.serialize_workflow(self.workflow)
        
        # Verify the serialized data
        self.assertEqual(data["workflow_id"], "test-workflow")
        self.assertEqual(data["name"], "Test Workflow")
        self.assertEqual(data["description"], "Test workflow description")
        self.assertEqual(data["version"], "1.0.0")
        self.assertTrue(data["enabled"])
        self.assertEqual(data["metadata"], {"key": "value"})
        self.assertEqual(len(data["steps"]), 2)
        
        # Verify the serialized steps
        self.assertEqual(data["steps"][0]["step_id"], "step1")
        self.assertEqual(data["steps"][0]["step_type"], "test")
        self.assertEqual(data["steps"][0]["name"], "Step 1")
        self.assertEqual(data["steps"][0]["description"], "Test step 1")
        self.assertTrue(data["steps"][0]["enabled"])
        self.assertEqual(data["steps"][0]["config"], {"param1": "value1"})
        self.assertEqual(data["steps"][0]["metadata"], {"key1": "value1"})
        
        self.assertEqual(data["steps"][1]["step_id"], "step2")
        self.assertEqual(data["steps"][1]["step_type"], "test")
        self.assertEqual(data["steps"][1]["name"], "Step 2")
        self.assertEqual(data["steps"][1]["description"], "Test step 2")
        self.assertTrue(data["steps"][1]["enabled"])
        self.assertEqual(data["steps"][1]["config"], {"param2": "value2"})
        self.assertEqual(data["steps"][1]["metadata"], {"key2": "value2"})
        
        # Test serialization error
        self.workflow.get_steps.side_effect = Exception("Test error")
        
        with self.assertRaises(WorkflowSerializationError):
            self.serializer.serialize_workflow(self.workflow)
    
    def test_deserialize_workflow(self):
        """Test deserializing a workflow."""
        # Create serialized data
        data = {
            "workflow_id": "test-workflow",
            "name": "Test Workflow",
            "description": "Test workflow description",
            "version": "1.0.0",
            "enabled": True,
            "metadata": {"key": "value"},
            "steps": [
                {
                    "step_id": "step1",
                    "step_type": "test",
                    "name": "Step 1",
                    "description": "Test step 1",
                    "enabled": True,
                    "config": {"param1": "value1"},
                    "metadata": {"key1": "value1"}
                },
                {
                    "step_id": "step2",
                    "step_type": "test",
                    "name": "Step 2",
                    "description": "Test step 2",
                    "enabled": True,
                    "config": {"param2": "value2"},
                    "metadata": {"key2": "value2"}
                }
            ]
        }
        
        # Deserialize the workflow
        workflow = self.serializer.deserialize_workflow(data)
        
        # Verify the engine was called
        self.engine.create_workflow.assert_called_once()
        self.assertEqual(self.engine.create_step.call_count, 2)
        
        # Verify the workflow was returned
        self.assertEqual(workflow, self.workflow)
        
        # Test deserialization error
        self.engine.create_workflow.side_effect = Exception("Test error")
        
        with self.assertRaises(WorkflowDeserializationError):
            self.serializer.deserialize_workflow(data)
    
    def test_serialize_step(self):
        """Test serializing a workflow step."""
        # Serialize the step
        data = self.serializer.serialize_step(self.step1)
        
        # Verify the serialized data
        self.assertEqual(data["step_id"], "step1")
        self.assertEqual(data["step_type"], "test")
        self.assertEqual(data["name"], "Step 1")
        self.assertEqual(data["description"], "Test step 1")
        self.assertTrue(data["enabled"])
        self.assertEqual(data["config"], {"param1": "value1"})
        self.assertEqual(data["metadata"], {"key1": "value1"})
        
        # Test serialization error
        with patch.object(self.step1, "step_id", side_effect=Exception("Test error")):
            with self.assertRaises(WorkflowSerializationError):
                self.serializer.serialize_step(self.step1)
    
    def test_deserialize_step(self):
        """Test deserializing a workflow step."""
        # Create serialized data
        data = {
            "step_id": "step1",
            "step_type": "test",
            "name": "Step 1",
            "description": "Test step 1",
            "enabled": True,
            "config": {"param1": "value1"},
            "metadata": {"key1": "value1"}
        }
        
        # Deserialize the step
        step = self.serializer.deserialize_step(data)
        
        # Verify the engine was called
        self.engine.create_step.assert_called_with(data)
        
        # Verify the step was returned
        self.assertEqual(step, self.step1)
        
        # Test deserialization error
        self.engine.create_step.side_effect = Exception("Test error")
        
        with self.assertRaises(WorkflowDeserializationError):
            self.serializer.deserialize_step(data)
    
    def test_serialize_to_json(self):
        """Test serializing a workflow to JSON."""
        # Serialize the workflow to JSON
        json_str = self.serializer.serialize_to_json(self.workflow)
        
        # Verify the JSON string
        data = json.loads(json_str)
        
        self.assertEqual(data["workflow_id"], "test-workflow")
        self.assertEqual(data["name"], "Test Workflow")
        self.assertEqual(len(data["steps"]), 2)
        
        # Test serialization error
        self.workflow.get_steps.side_effect = Exception("Test error")
        
        with self.assertRaises(WorkflowSerializationError):
            self.serializer.serialize_to_json(self.workflow)
    
    def test_deserialize_from_json(self):
        """Test deserializing a workflow from JSON."""
        # Create JSON string
        json_str = json.dumps({
            "workflow_id": "test-workflow",
            "name": "Test Workflow",
            "description": "Test workflow description",
            "version": "1.0.0",
            "enabled": True,
            "metadata": {"key": "value"},
            "steps": [
                {
                    "step_id": "step1",
                    "step_type": "test",
                    "name": "Step 1",
                    "description": "Test step 1",
                    "enabled": True,
                    "config": {"param1": "value1"},
                    "metadata": {"key1": "value1"}
                },
                {
                    "step_id": "step2",
                    "step_type": "test",
                    "name": "Step 2",
                    "description": "Test step 2",
                    "enabled": True,
                    "config": {"param2": "value2"},
                    "metadata": {"key2": "value2"}
                }
            ]
        })
        
        # Deserialize the workflow from JSON
        workflow = self.serializer.deserialize_from_json(json_str)
        
        # Verify the engine was called
        self.engine.create_workflow.assert_called_once()
        self.assertEqual(self.engine.create_step.call_count, 2)
        
        # Verify the workflow was returned
        self.assertEqual(workflow, self.workflow)
        
        # Test deserialization error with invalid JSON
        with self.assertRaises(WorkflowDeserializationError):
            self.serializer.deserialize_from_json("invalid json")
        
        # Test deserialization error with engine error
        self.engine.create_workflow.side_effect = Exception("Test error")
        
        with self.assertRaises(WorkflowDeserializationError):
            self.serializer.deserialize_from_json(json_str)


if __name__ == "__main__":
    unittest.main()
