"""Tests for the state persistence functionality"""
import os
import unittest
import tempfile
import json
from typing import Dict, Any, List
from datetime import datetime

from src.core.context.execution_context import ExecutionContext
from src.core.context.execution_state import ExecutionStateEnum
from src.core.context.variable_storage import VariableScope
from src.core.state.state_persistence import StatePersistence


class TestStatePersistence(unittest.TestCase):
    """Test cases for the state persistence functionality"""

    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for state files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_dir = self.temp_dir.name

        # Create a state persistence instance
        self.persistence = StatePersistence(self.state_dir)

        # Create a test execution context
        self.context = ExecutionContext()

        # Set up some test state
        self.context.state.transition_to(ExecutionStateEnum.RUNNING)
        self.context.variables.set("test_var", "test_value", VariableScope.WORKFLOW)
        self.context.variables.set("test_num", 42, VariableScope.GLOBAL)

        # Create a unique workflow ID for testing
        self.workflow_id = "test-workflow-123"

    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()

    def test_save_state(self):
        """Test saving state to a file"""
        # Act
        file_path = self.persistence.save_state(self.workflow_id, self.context)

        # Assert
        self.assertTrue(os.path.exists(file_path))

        # Verify file contents
        with open(file_path, 'r') as f:
            data = json.load(f)

        self.assertEqual(data["workflow_id"], self.workflow_id)
        self.assertEqual(data["context"]["state"]["current_state"], "RUNNING")
        self.assertEqual(data["context"]["variables"]["workflow"]["test_var"], "test_value")
        self.assertEqual(data["context"]["variables"]["global"]["test_num"], 42)
        self.assertIn("timestamp", data)

    def test_load_state(self):
        """Test loading state from a file"""
        # Arrange
        file_path = self.persistence.save_state(self.workflow_id, self.context)

        # Act
        loaded_context = self.persistence.load_state(file_path)

        # Assert
        self.assertEqual(loaded_context.state.current_state, ExecutionStateEnum.RUNNING)
        self.assertEqual(loaded_context.variables.get("test_var"), "test_value")
        self.assertEqual(loaded_context.variables.get("test_num"), 42)

    def test_get_latest_state(self):
        """Test getting the latest state for a workflow"""
        # Arrange - Save multiple states with different timestamps
        for i in range(3):
            self.persistence.save_state(self.workflow_id, self.context)
            # Ensure different timestamps
            import time
            time.sleep(0.01)

        # Act
        latest_file = self.persistence.get_latest_state_file(self.workflow_id)

        # Assert
        self.assertIsNotNone(latest_file)
        self.assertTrue(os.path.exists(latest_file))

        # Verify it's the latest one
        all_files = self.persistence.get_state_files(self.workflow_id)
        self.assertEqual(latest_file, all_files[0])  # First file should be the latest

    def test_get_state_files(self):
        """Test getting all state files for a workflow"""
        # Arrange - Save multiple states
        for i in range(3):
            self.persistence.save_state(self.workflow_id, self.context)

        # Act
        files = self.persistence.get_state_files(self.workflow_id)

        # Assert
        # We should have at least one file
        self.assertGreaterEqual(len(files), 1)
        for file in files:
            self.assertTrue(os.path.exists(file))
            self.assertIn(self.workflow_id, file)

    def test_cleanup_old_states(self):
        """Test cleaning up old state files"""
        # Arrange - Save multiple states
        for i in range(5):
            self.persistence.save_state(self.workflow_id, self.context)

        # Act
        removed = self.persistence.cleanup_old_states(self.workflow_id, max_states=3)

        # Assert
        # Get the remaining files
        files = self.persistence.get_state_files(self.workflow_id)
        # We should have at most max_states files left
        self.assertLessEqual(len(files), 3)


if __name__ == "__main__":
    unittest.main()
