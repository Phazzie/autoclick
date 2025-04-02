"""
Tests for WorkflowNode serialization.

This module contains tests for the serialization of WorkflowNode models.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests workflow node serialization
"""
import unittest
from typing import Dict, Any, List
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.models import WorkflowNode
from src.core.utils.serialization import SerializableMixin


class TestWorkflowNodeSerialization(unittest.TestCase):
    """Tests for WorkflowNode serialization."""

    def setUp(self):
        """Set up test fixtures."""
        # Create nodes for testing
        self.start_node = WorkflowNode(
            id="start-node",
            type="Start",
            position=(100, 100),
            properties={},
            label="Start"
        )
        
        self.click_node = WorkflowNode(
            id="click-node",
            type="Click",
            position=(200, 100),
            properties={"selector": "#button", "timeout": 5000},
            label="Click Button"
        )
        
        self.condition_node = WorkflowNode(
            id="condition-node",
            type="Condition",
            position=(300, 100),
            properties={"condition": "element.exists('#result')", "timeout": 3000},
            label="Check Result"
        )

    def test_node_is_serializable(self):
        """Test that WorkflowNode implements SerializableMixin."""
        self.assertIsInstance(self.start_node, SerializableMixin)
        
    def test_to_dict_basic(self):
        """Test basic to_dict functionality."""
        # Convert to dictionary
        result = self.start_node.to_dict()
        
        # Verify basic properties
        self.assertEqual(result["id"], "start-node")
        self.assertEqual(result["type"], "Start")
        self.assertEqual(result["position"], (100, 100))
        self.assertEqual(result["properties"], {})
        self.assertEqual(result["label"], "Start")
        
    def test_to_dict_with_properties(self):
        """Test to_dict with properties."""
        # Convert to dictionary
        result = self.click_node.to_dict()
        
        # Verify properties
        self.assertEqual(result["properties"]["selector"], "#button")
        self.assertEqual(result["properties"]["timeout"], 5000)
        
    def test_from_dict_basic(self):
        """Test basic from_dict functionality."""
        # Create a dictionary
        data = {
            "id": "test-node",
            "type": "Test",
            "position": (150, 150),
            "properties": {"key": "value"},
            "label": "Test Node"
        }
        
        # Create a node from the dictionary
        node = WorkflowNode.from_dict(data)
        
        # Verify the node
        self.assertEqual(node.id, "test-node")
        self.assertEqual(node.type, "Test")
        self.assertEqual(node.position, (150, 150))
        self.assertEqual(node.properties, {"key": "value"})
        self.assertEqual(node.label, "Test Node")
        
    def test_from_dict_missing_required(self):
        """Test from_dict with missing required fields."""
        # Create dictionaries with missing required fields
        missing_id = {
            "type": "Test",
            "position": (150, 150)
        }
        
        missing_type = {
            "id": "test-node",
            "position": (150, 150)
        }
        
        missing_position = {
            "id": "test-node",
            "type": "Test"
        }
        
        # Verify that creating nodes raises errors
        with self.assertRaises(ValueError):
            WorkflowNode.from_dict(missing_id)
            
        with self.assertRaises(ValueError):
            WorkflowNode.from_dict(missing_type)
            
        with self.assertRaises(ValueError):
            WorkflowNode.from_dict(missing_position)
            
    def test_from_dict_default_values(self):
        """Test from_dict with default values."""
        # Create a dictionary with only required fields
        data = {
            "id": "test-node",
            "type": "Test",
            "position": (150, 150)
        }
        
        # Create a node from the dictionary
        node = WorkflowNode.from_dict(data)
        
        # Verify default values
        self.assertEqual(node.properties, {})
        self.assertEqual(node.label, "")
        
    def test_round_trip(self):
        """Test round-trip serialization (to_dict -> from_dict)."""
        # Convert to dictionary and back
        data = self.condition_node.to_dict()
        node = WorkflowNode.from_dict(data)
        
        # Verify the node
        self.assertEqual(node.id, self.condition_node.id)
        self.assertEqual(node.type, self.condition_node.type)
        self.assertEqual(node.position, self.condition_node.position)
        self.assertEqual(node.properties, self.condition_node.properties)
        self.assertEqual(node.label, self.condition_node.label)
        
    def test_properties_copy(self):
        """Test that properties are copied, not referenced."""
        # Create a node with properties
        node = WorkflowNode(
            id="test-node",
            type="Test",
            position=(150, 150),
            properties={"key": "value"}
        )
        
        # Convert to dictionary
        data = node.to_dict()
        
        # Modify the properties in the dictionary
        data["properties"]["key"] = "new-value"
        
        # Verify that the original node's properties are unchanged
        self.assertEqual(node.properties["key"], "value")
        
        # Create a new node from the dictionary
        new_node = WorkflowNode.from_dict(data)
        
        # Modify the new node's properties
        new_node.properties["key"] = "another-value"
        
        # Verify that the dictionary's properties are unchanged
        self.assertEqual(data["properties"]["key"], "new-value")


if __name__ == "__main__":
    unittest.main()
