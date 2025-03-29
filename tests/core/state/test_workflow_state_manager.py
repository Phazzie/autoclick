"""Tests for the workflow state manager"""
import unittest
from typing import Dict, Any, List, Optional, Tuple
from unittest.mock import MagicMock, patch

from src.core.context.execution_context import ExecutionContext
from src.core.state.workflow_state_manager_interface import WorkflowStateManagerInterface
from src.core.state.workflow_state_manager import WorkflowStateManager
from src.core.state.state_persistence_interface import StatePersistenceInterface
from src.core.state.checkpoint_manager_interface import CheckpointManagerInterface


class TestWorkflowStateManager(unittest.TestCase):
    """Test cases for the workflow state manager"""

    def setUp(self):
        """Set up test environment"""
        # Create mock dependencies
        self.mock_state_persistence = MagicMock(spec=StatePersistenceInterface)
        self.mock_checkpoint_manager = MagicMock(spec=CheckpointManagerInterface)
        
        # Create the workflow state manager
        self.manager = WorkflowStateManager(
            state_persistence=self.mock_state_persistence,
            checkpoint_manager=self.mock_checkpoint_manager
        )
        
        # Create test data
        self.workflow_id = "test-workflow-123"
        self.context = ExecutionContext()
        self.state_file = "/path/to/state.json"
        self.checkpoint_id = "test-checkpoint-456"
        self.checkpoint_name = "test-checkpoint"
        self.checkpoint_data = {"key": "value"}

    def test_implements_interface(self):
        """Test that WorkflowStateManager implements WorkflowStateManagerInterface"""
        self.assertIsInstance(self.manager, WorkflowStateManagerInterface)

    def test_save_workflow_state(self):
        """Test saving workflow state"""
        # Arrange
        self.mock_state_persistence.save_state.return_value = self.state_file
        
        # Act
        result = self.manager.save_workflow_state(self.workflow_id, self.context)
        
        # Assert
        self.assertEqual(result, self.state_file)
        self.mock_state_persistence.save_state.assert_called_once_with(
            self.workflow_id, self.context
        )

    def test_save_workflow_state_error(self):
        """Test saving workflow state with error"""
        # Arrange
        self.mock_state_persistence.save_state.side_effect = Exception("Test error")
        
        # Act & Assert
        with self.assertRaises(IOError):
            self.manager.save_workflow_state(self.workflow_id, self.context)

    def test_load_workflow_state(self):
        """Test loading workflow state"""
        # Arrange
        self.mock_state_persistence.load_state.return_value = self.context
        
        # Act
        result = self.manager.load_workflow_state(self.state_file)
        
        # Assert
        self.assertEqual(result, self.context)
        self.mock_state_persistence.load_state.assert_called_once_with(self.state_file)

    def test_load_workflow_state_error(self):
        """Test loading workflow state with error"""
        # Arrange
        self.mock_state_persistence.load_state.side_effect = FileNotFoundError("Test error")
        
        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            self.manager.load_workflow_state(self.state_file)

    def test_get_latest_state(self):
        """Test getting the latest state"""
        # Arrange
        self.mock_state_persistence.get_latest_state_file.return_value = self.state_file
        
        # Act
        result = self.manager.get_latest_state(self.workflow_id)
        
        # Assert
        self.assertEqual(result, self.state_file)
        self.mock_state_persistence.get_latest_state_file.assert_called_once_with(
            self.workflow_id
        )

    def test_create_checkpoint(self):
        """Test creating a checkpoint"""
        # Arrange
        self.mock_checkpoint_manager.create_checkpoint.return_value = self.checkpoint_id
        
        # Act
        result = self.manager.create_checkpoint(
            self.workflow_id, self.context, self.checkpoint_data, self.checkpoint_name
        )
        
        # Assert
        self.assertEqual(result, self.checkpoint_id)
        self.mock_checkpoint_manager.create_checkpoint.assert_called_once_with(
            self.workflow_id, self.context, self.checkpoint_data, self.checkpoint_name
        )

    def test_create_checkpoint_error(self):
        """Test creating a checkpoint with error"""
        # Arrange
        self.mock_checkpoint_manager.create_checkpoint.side_effect = Exception("Test error")
        
        # Act & Assert
        with self.assertRaises(IOError):
            self.manager.create_checkpoint(
                self.workflow_id, self.context, self.checkpoint_data, self.checkpoint_name
            )

    def test_restore_from_checkpoint(self):
        """Test restoring from a checkpoint"""
        # Arrange
        expected_result = (self.context, self.checkpoint_data)
        self.mock_checkpoint_manager.restore_from_checkpoint.return_value = expected_result
        
        # Act
        result = self.manager.restore_from_checkpoint(self.checkpoint_id)
        
        # Assert
        self.assertEqual(result, expected_result)
        self.mock_checkpoint_manager.restore_from_checkpoint.assert_called_once_with(
            self.checkpoint_id
        )

    def test_restore_from_checkpoint_error(self):
        """Test restoring from a checkpoint with error"""
        # Arrange
        self.mock_checkpoint_manager.restore_from_checkpoint.side_effect = FileNotFoundError("Test error")
        
        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            self.manager.restore_from_checkpoint(self.checkpoint_id)

    def test_get_checkpoints(self):
        """Test getting checkpoints"""
        # Arrange
        expected_checkpoints = [{"id": "1"}, {"id": "2"}]
        self.mock_checkpoint_manager.get_checkpoints_for_workflow.return_value = expected_checkpoints
        
        # Act
        result = self.manager.get_checkpoints(self.workflow_id)
        
        # Assert
        self.assertEqual(result, expected_checkpoints)
        self.mock_checkpoint_manager.get_checkpoints_for_workflow.assert_called_once_with(
            self.workflow_id
        )

    def test_get_checkpoints_error(self):
        """Test getting checkpoints with error"""
        # Arrange
        self.mock_checkpoint_manager.get_checkpoints_for_workflow.side_effect = Exception("Test error")
        
        # Act
        result = self.manager.get_checkpoints(self.workflow_id)
        
        # Assert
        self.assertEqual(result, [])

    def test_get_checkpoint_by_name(self):
        """Test getting a checkpoint by name"""
        # Arrange
        expected_checkpoint = {"id": self.checkpoint_id}
        self.mock_checkpoint_manager.get_checkpoint_by_name.return_value = expected_checkpoint
        
        # Act
        result = self.manager.get_checkpoint_by_name(self.workflow_id, self.checkpoint_name)
        
        # Assert
        self.assertEqual(result, expected_checkpoint)
        self.mock_checkpoint_manager.get_checkpoint_by_name.assert_called_once_with(
            self.workflow_id, self.checkpoint_name
        )

    def test_get_checkpoint_by_name_error(self):
        """Test getting a checkpoint by name with error"""
        # Arrange
        self.mock_checkpoint_manager.get_checkpoint_by_name.side_effect = Exception("Test error")
        
        # Act
        result = self.manager.get_checkpoint_by_name(self.workflow_id, self.checkpoint_name)
        
        # Assert
        self.assertIsNone(result)

    def test_delete_checkpoint(self):
        """Test deleting a checkpoint"""
        # Arrange
        self.mock_checkpoint_manager.delete_checkpoint.return_value = True
        
        # Act
        result = self.manager.delete_checkpoint(self.checkpoint_id)
        
        # Assert
        self.assertTrue(result)
        self.mock_checkpoint_manager.delete_checkpoint.assert_called_once_with(
            self.checkpoint_id
        )

    def test_delete_checkpoint_error(self):
        """Test deleting a checkpoint with error"""
        # Arrange
        self.mock_checkpoint_manager.delete_checkpoint.side_effect = Exception("Test error")
        
        # Act
        result = self.manager.delete_checkpoint(self.checkpoint_id)
        
        # Assert
        self.assertFalse(result)

    def test_cleanup_old_states(self):
        """Test cleaning up old states"""
        # Arrange
        self.mock_state_persistence.cleanup_old_states.return_value = 5
        
        # Act
        result = self.manager.cleanup_old_states(self.workflow_id, 10)
        
        # Assert
        self.assertEqual(result, 5)
        self.mock_state_persistence.cleanup_old_states.assert_called_once_with(
            self.workflow_id, 10
        )

    def test_cleanup_old_states_error(self):
        """Test cleaning up old states with error"""
        # Arrange
        self.mock_state_persistence.cleanup_old_states.side_effect = Exception("Test error")
        
        # Act
        result = self.manager.cleanup_old_states(self.workflow_id, 10)
        
        # Assert
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
