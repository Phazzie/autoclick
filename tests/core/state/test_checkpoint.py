"""Tests for the checkpoint functionality"""
import unittest
from datetime import datetime
from typing import Dict, Any
from unittest.mock import MagicMock

from src.core.context.execution_context import ExecutionContext
from src.core.state.checkpoint_interface import CheckpointInterface
from src.core.state.checkpoint import Checkpoint


class TestCheckpoint(unittest.TestCase):
    """Test cases for the checkpoint functionality"""

    def setUp(self):
        """Set up test environment"""
        # Create a test execution context
        self.context = ExecutionContext()
        
        # Create test data
        self.checkpoint_id = "test-checkpoint-123"
        self.workflow_id = "test-workflow-456"
        self.timestamp = datetime.now().isoformat()
        self.name = "test-checkpoint"
        self.data = {"key": "value", "number": 42}
        
        # Create a checkpoint
        self.checkpoint = Checkpoint(
            checkpoint_id=self.checkpoint_id,
            workflow_id=self.workflow_id,
            timestamp=self.timestamp,
            name=self.name,
            data=self.data,
            context=self.context
        )

    def test_implements_interface(self):
        """Test that Checkpoint implements CheckpointInterface"""
        self.assertIsInstance(self.checkpoint, CheckpointInterface)

    def test_get_id(self):
        """Test getting the checkpoint ID"""
        self.assertEqual(self.checkpoint.get_id(), self.checkpoint_id)

    def test_get_workflow_id(self):
        """Test getting the workflow ID"""
        self.assertEqual(self.checkpoint.get_workflow_id(), self.workflow_id)

    def test_get_timestamp(self):
        """Test getting the timestamp"""
        self.assertEqual(self.checkpoint.get_timestamp(), self.timestamp)

    def test_get_name(self):
        """Test getting the name"""
        self.assertEqual(self.checkpoint.get_name(), self.name)

    def test_get_name_none(self):
        """Test getting the name when it's None"""
        # Arrange
        checkpoint = Checkpoint(
            checkpoint_id=self.checkpoint_id,
            workflow_id=self.workflow_id,
            timestamp=self.timestamp,
            name=None,
            data=self.data,
            context=self.context
        )
        
        # Act & Assert
        self.assertIsNone(checkpoint.get_name())

    def test_get_data(self):
        """Test getting the data"""
        # Act
        data = self.checkpoint.get_data()
        
        # Assert
        self.assertEqual(data, self.data)
        self.assertEqual(data["key"], "value")
        self.assertEqual(data["number"], 42)

    def test_get_context(self):
        """Test getting the context"""
        self.assertEqual(self.checkpoint.get_context(), self.context)

    def test_to_dict(self):
        """Test converting to a dictionary"""
        # Act
        result = self.checkpoint.to_dict()
        
        # Assert
        self.assertEqual(result["id"], self.checkpoint_id)
        self.assertEqual(result["workflow_id"], self.workflow_id)
        self.assertEqual(result["timestamp"], self.timestamp)
        self.assertEqual(result["name"], self.name)
        self.assertEqual(result["data"], self.data)

    def test_from_dict(self):
        """Test creating from a dictionary"""
        # Arrange
        data = {
            "id": self.checkpoint_id,
            "workflow_id": self.workflow_id,
            "timestamp": self.timestamp,
            "name": self.name,
            "data": self.data
        }
        
        # Act
        checkpoint = Checkpoint.from_dict(data, self.context)
        
        # Assert
        self.assertEqual(checkpoint.get_id(), self.checkpoint_id)
        self.assertEqual(checkpoint.get_workflow_id(), self.workflow_id)
        self.assertEqual(checkpoint.get_timestamp(), self.timestamp)
        self.assertEqual(checkpoint.get_name(), self.name)
        self.assertEqual(checkpoint.get_data(), self.data)
        self.assertEqual(checkpoint.get_context(), self.context)

    def test_from_dict_missing_id(self):
        """Test creating from a dictionary with missing ID"""
        # Arrange
        data = {
            "workflow_id": self.workflow_id,
            "timestamp": self.timestamp,
            "name": self.name,
            "data": self.data
        }
        
        # Act & Assert
        with self.assertRaises(ValueError):
            Checkpoint.from_dict(data, self.context)

    def test_from_dict_missing_workflow_id(self):
        """Test creating from a dictionary with missing workflow ID"""
        # Arrange
        data = {
            "id": self.checkpoint_id,
            "timestamp": self.timestamp,
            "name": self.name,
            "data": self.data
        }
        
        # Act & Assert
        with self.assertRaises(ValueError):
            Checkpoint.from_dict(data, self.context)


if __name__ == "__main__":
    unittest.main()
