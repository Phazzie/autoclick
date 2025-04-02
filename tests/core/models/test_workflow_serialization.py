"""
Tests for Workflow serialization.

This module contains tests for the serialization of Workflow models.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests workflow serialization
"""
import unittest
from typing import Dict, Any, List
import sys
import os
import uuid

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.core.models import Workflow, WorkflowNode, WorkflowConnection
from src.core.utils.serialization import SerializableMixin


class TestWorkflowSerialization(unittest.TestCase):
    """Tests for Workflow serialization."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a simple workflow for testing
        self.workflow = Workflow(
            id="test-workflow",
            name="Test Workflow",
            metadata={
                "description": "A test workflow",
                "version": "1.0.0"
            }
        )

        # Add some nodes
        start_node = WorkflowNode(
            id="start-node",
            type="Start",
            position=(100, 100),
            properties={},
            label="Start"
        )

        click_node = WorkflowNode(
            id="click-node",
            type="Click",
            position=(200, 100),
            properties={"selector": "#button", "timeout": 5000},
            label="Click Button"
        )

        end_node = WorkflowNode(
            id="end-node",
            type="End",
            position=(300, 100),
            properties={},
            label="End"
        )

        # Add nodes to workflow
        self.workflow.add_node(start_node)
        self.workflow.add_node(click_node)
        self.workflow.add_node(end_node)

        # Add connections
        start_to_click = WorkflowConnection(
            id="start-to-click",
            source_node_id="start-node",
            source_port="output",
            target_node_id="click-node",
            target_port="input"
        )

        click_to_end = WorkflowConnection(
            id="click-to-end",
            source_node_id="click-node",
            source_port="output",
            target_node_id="end-node",
            target_port="input"
        )

        # Add connections to workflow
        self.workflow.add_connection(start_to_click)
        self.workflow.add_connection(click_to_end)

    def test_workflow_is_serializable(self):
        """Test that Workflow implements SerializableMixin."""
        self.assertIsInstance(self.workflow, SerializableMixin)

    def test_to_dict_basic(self):
        """Test basic to_dict functionality."""
        # Convert to dictionary
        result = self.workflow.to_dict()

        # Verify basic properties
        self.assertEqual(result["id"], "test-workflow")
        self.assertEqual(result["name"], "Test Workflow")
        self.assertEqual(result["metadata"]["description"], "A test workflow")
        self.assertEqual(result["metadata"]["version"], "1.0.0")

        # Verify nodes and connections
        self.assertIn("nodes", result)
        self.assertIn("connections", result)
        self.assertEqual(len(result["nodes"]), 3)
        self.assertEqual(len(result["connections"]), 2)

    def test_to_dict_nodes(self):
        """Test that nodes are properly serialized."""
        # Convert to dictionary
        result = self.workflow.to_dict()

        # Get nodes
        nodes = result["nodes"]

        # Verify that each node has the expected properties
        for node in nodes:
            self.assertIn("id", node)
            self.assertIn("type", node)
            self.assertIn("position", node)
            self.assertIn("properties", node)
            self.assertIn("label", node)

        # Verify specific node properties
        click_node = next(node for node in nodes if node["id"] == "click-node")
        self.assertEqual(click_node["type"], "Click")
        self.assertEqual(click_node["position"], (200, 100))
        self.assertEqual(click_node["properties"]["selector"], "#button")
        self.assertEqual(click_node["properties"]["timeout"], 5000)
        self.assertEqual(click_node["label"], "Click Button")

    def test_to_dict_connections(self):
        """Test that connections are properly serialized."""
        # Convert to dictionary
        result = self.workflow.to_dict()

        # Get connections
        connections = result["connections"]

        # Verify that each connection has the expected properties
        for connection in connections:
            self.assertIn("id", connection)
            self.assertIn("source_node_id", connection)
            self.assertIn("source_port", connection)
            self.assertIn("target_node_id", connection)
            self.assertIn("target_port", connection)

        # Verify specific connection properties
        start_to_click = next(conn for conn in connections if conn["id"] == "start-to-click")
        self.assertEqual(start_to_click["source_node_id"], "start-node")
        self.assertEqual(start_to_click["source_port"], "output")
        self.assertEqual(start_to_click["target_node_id"], "click-node")
        self.assertEqual(start_to_click["target_port"], "input")

    def test_from_dict_basic(self):
        """Test basic from_dict functionality."""
        # Convert to dictionary and back
        data = self.workflow.to_dict()
        result = Workflow.from_dict(data)

        # Verify basic properties
        self.assertEqual(result.id, "test-workflow")
        self.assertEqual(result.name, "Test Workflow")
        self.assertEqual(result.metadata["description"], "A test workflow")
        self.assertEqual(result.metadata["version"], "1.0.0")

        # Verify nodes and connections
        self.assertEqual(len(result.nodes), 3)
        self.assertEqual(len(result.connections), 2)

    def test_from_dict_nodes(self):
        """Test that nodes are properly deserialized."""
        # Convert to dictionary and back
        data = self.workflow.to_dict()
        result = Workflow.from_dict(data)

        # Verify that each node has the expected properties
        for node_id, node in result.nodes.items():
            self.assertEqual(node.id, node_id)
            self.assertIn("type", dir(node))
            self.assertIn("position", dir(node))
            self.assertIn("properties", dir(node))
            self.assertIn("label", dir(node))

        # Verify specific node properties
        click_node = result.nodes["click-node"]
        self.assertEqual(click_node.type, "Click")
        self.assertEqual(click_node.position, (200, 100))
        self.assertEqual(click_node.properties["selector"], "#button")
        self.assertEqual(click_node.properties["timeout"], 5000)
        self.assertEqual(click_node.label, "Click Button")

    def test_from_dict_connections(self):
        """Test that connections are properly deserialized."""
        # Convert to dictionary and back
        data = self.workflow.to_dict()
        result = Workflow.from_dict(data)

        # Verify that each connection has the expected properties
        for conn_id, conn in result.connections.items():
            self.assertEqual(conn.id, conn_id)
            self.assertIn("source_node_id", dir(conn))
            self.assertIn("source_port", dir(conn))
            self.assertIn("target_node_id", dir(conn))
            self.assertIn("target_port", dir(conn))

        # Verify specific connection properties
        start_to_click = result.connections["start-to-click"]
        self.assertEqual(start_to_click.source_node_id, "start-node")
        self.assertEqual(start_to_click.source_port, "output")
        self.assertEqual(start_to_click.target_node_id, "click-node")
        self.assertEqual(start_to_click.target_port, "input")

    def test_from_dict_missing_required(self):
        """Test from_dict with missing required fields."""
        # Create a dictionary with missing required fields
        data = {
            "name": "Test Workflow",
            "description": "A test workflow",
            "version": "1.0.0"
        }

        # Verify that creating a workflow raises an error
        with self.assertRaises(ValueError):
            Workflow.from_dict(data)

    def test_round_trip(self):
        """Test round-trip serialization (to_dict -> from_dict)."""
        # Convert to dictionary and back
        data = self.workflow.to_dict()
        result = Workflow.from_dict(data)

        # Convert back to dictionary
        result_data = result.to_dict()

        # Verify that the dictionaries are equal
        self.assertEqual(data["id"], result_data["id"])
        self.assertEqual(data["name"], result_data["name"])
        self.assertEqual(data["metadata"]["description"], result_data["metadata"]["description"])
        self.assertEqual(data["metadata"]["version"], result_data["metadata"]["version"])

        # Verify that the nodes are equal
        self.assertEqual(len(data["nodes"]), len(result_data["nodes"]))
        for node1 in data["nodes"]:
            node2 = next(n for n in result_data["nodes"] if n["id"] == node1["id"])
            self.assertEqual(node1["type"], node2["type"])
            self.assertEqual(node1["position"], node2["position"])
            self.assertEqual(node1["properties"], node2["properties"])
            self.assertEqual(node1["label"], node2["label"])

        # Verify that the connections are equal
        self.assertEqual(len(data["connections"]), len(result_data["connections"]))
        for conn1 in data["connections"]:
            conn2 = next(c for c in result_data["connections"] if c["id"] == conn1["id"])
            self.assertEqual(conn1["source_node_id"], conn2["source_node_id"])
            self.assertEqual(conn1["source_port"], conn2["source_port"])
            self.assertEqual(conn1["target_node_id"], conn2["target_node_id"])
            self.assertEqual(conn1["target_port"], conn2["target_port"])


if __name__ == "__main__":
    unittest.main()
