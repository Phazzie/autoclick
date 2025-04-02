"""
Tests for WorkflowConnection serialization.

This module contains tests for the serialization of WorkflowConnection models.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests workflow connection serialization
"""
import unittest
from typing import Dict, Any
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.models import WorkflowConnection
from src.core.utils.serialization import SerializableMixin


class TestWorkflowConnectionSerialization(unittest.TestCase):
    """Tests for WorkflowConnection serialization."""

    def setUp(self):
        """Set up test fixtures."""
        # Create connections for testing
        self.standard_connection = WorkflowConnection(
            id="standard-connection",
            source_node_id="source-node",
            source_port="output",
            target_node_id="target-node",
            target_port="input"
        )
        
        self.conditional_connection = WorkflowConnection(
            id="conditional-connection",
            source_node_id="condition-node",
            source_port="true_branch",
            target_node_id="success-node",
            target_port="input"
        )
        
        self.loop_connection = WorkflowConnection(
            id="loop-connection",
            source_node_id="loop-node",
            source_port="loop_body",
            target_node_id="loop-body-node",
            target_port="input"
        )

    def test_connection_is_serializable(self):
        """Test that WorkflowConnection implements SerializableMixin."""
        self.assertIsInstance(self.standard_connection, SerializableMixin)
        
    def test_to_dict_basic(self):
        """Test basic to_dict functionality."""
        # Convert to dictionary
        result = self.standard_connection.to_dict()
        
        # Verify basic properties
        self.assertEqual(result["id"], "standard-connection")
        self.assertEqual(result["source_node_id"], "source-node")
        self.assertEqual(result["source_port"], "output")
        self.assertEqual(result["target_node_id"], "target-node")
        self.assertEqual(result["target_port"], "input")
        
    def test_to_dict_conditional(self):
        """Test to_dict with conditional connection."""
        # Convert to dictionary
        result = self.conditional_connection.to_dict()
        
        # Verify properties
        self.assertEqual(result["source_port"], "true_branch")
        
    def test_to_dict_loop(self):
        """Test to_dict with loop connection."""
        # Convert to dictionary
        result = self.loop_connection.to_dict()
        
        # Verify properties
        self.assertEqual(result["source_port"], "loop_body")
        
    def test_from_dict_basic(self):
        """Test basic from_dict functionality."""
        # Create a dictionary
        data = {
            "id": "test-connection",
            "source_node_id": "test-source",
            "source_port": "test-output",
            "target_node_id": "test-target",
            "target_port": "test-input"
        }
        
        # Create a connection from the dictionary
        connection = WorkflowConnection.from_dict(data)
        
        # Verify the connection
        self.assertEqual(connection.id, "test-connection")
        self.assertEqual(connection.source_node_id, "test-source")
        self.assertEqual(connection.source_port, "test-output")
        self.assertEqual(connection.target_node_id, "test-target")
        self.assertEqual(connection.target_port, "test-input")
        
    def test_from_dict_missing_required(self):
        """Test from_dict with missing required fields."""
        # Create dictionaries with missing required fields
        missing_id = {
            "source_node_id": "test-source",
            "source_port": "test-output",
            "target_node_id": "test-target",
            "target_port": "test-input"
        }
        
        missing_source_node_id = {
            "id": "test-connection",
            "source_port": "test-output",
            "target_node_id": "test-target",
            "target_port": "test-input"
        }
        
        missing_source_port = {
            "id": "test-connection",
            "source_node_id": "test-source",
            "target_node_id": "test-target",
            "target_port": "test-input"
        }
        
        missing_target_node_id = {
            "id": "test-connection",
            "source_node_id": "test-source",
            "source_port": "test-output",
            "target_port": "test-input"
        }
        
        missing_target_port = {
            "id": "test-connection",
            "source_node_id": "test-source",
            "source_port": "test-output",
            "target_node_id": "test-target"
        }
        
        # Verify that creating connections raises errors
        with self.assertRaises(ValueError):
            WorkflowConnection.from_dict(missing_id)
            
        with self.assertRaises(ValueError):
            WorkflowConnection.from_dict(missing_source_node_id)
            
        with self.assertRaises(ValueError):
            WorkflowConnection.from_dict(missing_source_port)
            
        with self.assertRaises(ValueError):
            WorkflowConnection.from_dict(missing_target_node_id)
            
        with self.assertRaises(ValueError):
            WorkflowConnection.from_dict(missing_target_port)
            
    def test_round_trip(self):
        """Test round-trip serialization (to_dict -> from_dict)."""
        # Convert to dictionary and back
        data = self.conditional_connection.to_dict()
        connection = WorkflowConnection.from_dict(data)
        
        # Verify the connection
        self.assertEqual(connection.id, self.conditional_connection.id)
        self.assertEqual(connection.source_node_id, self.conditional_connection.source_node_id)
        self.assertEqual(connection.source_port, self.conditional_connection.source_port)
        self.assertEqual(connection.target_node_id, self.conditional_connection.target_node_id)
        self.assertEqual(connection.target_port, self.conditional_connection.target_port)


if __name__ == "__main__":
    unittest.main()
