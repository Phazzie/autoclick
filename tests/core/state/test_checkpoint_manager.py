"""Tests for the checkpoint manager functionality"""
import os
import unittest
import tempfile
from typing import Dict, Any, List
from datetime import datetime

from src.core.context.execution_context import ExecutionContext
from src.core.context.execution_state import ExecutionStateEnum
from src.core.context.variable_storage import VariableScope
from src.core.state.checkpoint_manager import CheckpointManager


class TestCheckpointManager(unittest.TestCase):
    """Test cases for the checkpoint manager functionality"""

    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for checkpoint files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.checkpoint_dir = self.temp_dir.name
        
        # Create a checkpoint manager instance
        self.manager = CheckpointManager(self.checkpoint_dir)
        
        # Create a test execution context
        self.context = ExecutionContext()
        
        # Set up some test state
        self.context.state.transition_to(ExecutionStateEnum.RUNNING)
        self.context.variables.set("test_var", "test_value", VariableScope.WORKFLOW)
        self.context.variables.set("test_num", 42, VariableScope.GLOBAL)
        
        # Create a unique workflow ID for testing
        self.workflow_id = "test-workflow-123"
        
        # Create test checkpoint data
        self.checkpoint_data = {
            "action_index": 5,
            "custom_data": {"key": "value"}
        }

    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()

    def test_create_checkpoint(self):
        """Test creating a checkpoint"""
        # Act
        checkpoint_id = self.manager.create_checkpoint(
            self.workflow_id, 
            self.context, 
            self.checkpoint_data
        )
        
        # Assert
        self.assertIsNotNone(checkpoint_id)
        checkpoint_file = self.manager.get_checkpoint_file(checkpoint_id)
        self.assertTrue(os.path.exists(checkpoint_file))

    def test_restore_from_checkpoint(self):
        """Test restoring from a checkpoint"""
        # Arrange
        checkpoint_id = self.manager.create_checkpoint(
            self.workflow_id, 
            self.context, 
            self.checkpoint_data
        )
        
        # Modify the context to ensure restoration works
        self.context.variables.set("test_var", "modified_value")
        self.context.variables.set("new_var", "new_value")
        
        # Act
        restored_context, restored_data = self.manager.restore_from_checkpoint(checkpoint_id)
        
        # Assert
        self.assertEqual(restored_context.state.current_state, ExecutionStateEnum.RUNNING)
        self.assertEqual(restored_context.variables.get("test_var"), "test_value")
        self.assertEqual(restored_context.variables.get("test_num"), 42)
        self.assertIsNone(restored_context.variables.get("new_var"))
        self.assertEqual(restored_data["action_index"], 5)
        self.assertEqual(restored_data["custom_data"]["key"], "value")

    def test_get_checkpoints_for_workflow(self):
        """Test getting all checkpoints for a workflow"""
        # Arrange - Create multiple checkpoints
        checkpoint_ids = []
        for i in range(3):
            data = self.checkpoint_data.copy()
            data["action_index"] = i
            checkpoint_id = self.manager.create_checkpoint(
                self.workflow_id, 
                self.context, 
                data
            )
            checkpoint_ids.append(checkpoint_id)
        
        # Act
        checkpoints = self.manager.get_checkpoints_for_workflow(self.workflow_id)
        
        # Assert
        self.assertEqual(len(checkpoints), 3)
        for checkpoint in checkpoints:
            self.assertIn(checkpoint["id"], checkpoint_ids)
            self.assertEqual(checkpoint["workflow_id"], self.workflow_id)
            self.assertIn("timestamp", checkpoint)
            self.assertIn("data", checkpoint)

    def test_delete_checkpoint(self):
        """Test deleting a checkpoint"""
        # Arrange
        checkpoint_id = self.manager.create_checkpoint(
            self.workflow_id, 
            self.context, 
            self.checkpoint_data
        )
        
        # Act
        result = self.manager.delete_checkpoint(checkpoint_id)
        
        # Assert
        self.assertTrue(result)
        checkpoint_file = self.manager.get_checkpoint_file(checkpoint_id)
        self.assertFalse(os.path.exists(checkpoint_file))

    def test_create_named_checkpoint(self):
        """Test creating a named checkpoint"""
        # Arrange
        checkpoint_name = "important-state"
        
        # Act
        checkpoint_id = self.manager.create_checkpoint(
            self.workflow_id, 
            self.context, 
            self.checkpoint_data,
            name=checkpoint_name
        )
        
        # Assert
        checkpoints = self.manager.get_checkpoints_for_workflow(self.workflow_id)
        self.assertEqual(len(checkpoints), 1)
        self.assertEqual(checkpoints[0]["name"], checkpoint_name)

    def test_get_checkpoint_by_name(self):
        """Test getting a checkpoint by name"""
        # Arrange
        checkpoint_name = "important-state"
        self.manager.create_checkpoint(
            self.workflow_id, 
            self.context, 
            self.checkpoint_data,
            name=checkpoint_name
        )
        
        # Act
        checkpoint = self.manager.get_checkpoint_by_name(self.workflow_id, checkpoint_name)
        
        # Assert
        self.assertIsNotNone(checkpoint)
        self.assertEqual(checkpoint["name"], checkpoint_name)
        self.assertEqual(checkpoint["workflow_id"], self.workflow_id)


if __name__ == "__main__":
    unittest.main()
