"""Tests for the WorkflowPresenter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List

from src.core.models import Workflow, WorkflowNode, WorkflowConnection
from src.ui.presenters.workflow_presenter import WorkflowPresenter
from src.ui.adapters.workflow_adapter import WorkflowAdapter

class TestWorkflowPresenter(unittest.TestCase):
    """Test cases for the WorkflowPresenter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=WorkflowAdapter)
        
        # Create the presenter
        self.presenter = WorkflowPresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service
        )
        
        # Set up mock data
        self.test_workflow = Workflow(
            id="test_workflow",
            name="Test Workflow",
            nodes={
                "node1": WorkflowNode(
                    id="node1",
                    type="Start",
                    position=(100, 100),
                    properties={},
                    label="Start"
                ),
                "node2": WorkflowNode(
                    id="node2",
                    type="Click",
                    position=(300, 100),
                    properties={"selector": "#button"},
                    label="Click Button"
                ),
                "node3": WorkflowNode(
                    id="node3",
                    type="End",
                    position=(500, 100),
                    properties={},
                    label="End"
                )
            },
            connections={
                "conn1": WorkflowConnection(
                    id="conn1",
                    source_node_id="node1",
                    source_port="output",
                    target_node_id="node2",
                    target_port="input"
                ),
                "conn2": WorkflowConnection(
                    id="conn2",
                    source_node_id="node2",
                    source_port="output",
                    target_node_id="node3",
                    target_port="input"
                )
            }
        )
        
        # Configure mock service
        self.mock_service.get_all_workflows.return_value = [self.test_workflow]
        self.mock_service.get_workflow.return_value = self.test_workflow
        self.mock_service.get_node_types.return_value = [
            {"type": "Start", "name": "Start", "description": "Start of workflow"},
            {"type": "Click", "name": "Click", "description": "Click on element"},
            {"type": "Type", "name": "Type", "description": "Type text"},
            {"type": "Wait", "name": "Wait", "description": "Wait for time or element"},
            {"type": "Condition", "name": "Condition", "description": "Branch based on condition"},
            {"type": "Loop", "name": "Loop", "description": "Repeat actions"},
            {"type": "End", "name": "End", "description": "End of workflow"}
        ]
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the service was called
        self.mock_service.get_node_types.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.initialize_canvas.assert_called_once()
        self.mock_view.initialize_toolbox.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_load_workflow(self):
        """Test loading a workflow."""
        # Call the method
        self.presenter.load_workflow("test_workflow")
        
        # Verify the service was called
        self.mock_service.get_workflow.assert_called_once_with("test_workflow")
        
        # Verify the view was updated
        self.mock_view.clear_canvas.assert_called_once()
        self.mock_view.redraw_workflow.assert_called_once_with(self.test_workflow)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_create_new_workflow(self):
        """Test creating a new workflow."""
        # Call the method
        self.presenter.create_new_workflow("New Workflow")
        
        # Verify the service was called
        self.mock_service.create_workflow.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.clear_canvas.assert_called_once()
        self.mock_view.redraw_workflow.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_workflow(self):
        """Test saving a workflow."""
        # Set up mock view
        self.mock_view.get_workflow_name.return_value = "Updated Workflow"
        
        # Call the method
        self.presenter.save_workflow()
        
        # Verify the service was called
        self.mock_service.update_workflow.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_add_node(self):
        """Test adding a node."""
        # Call the method
        self.presenter.add_node("Click", (200, 200))
        
        # Verify the current workflow was updated
        self.assertIsNotNone(self.presenter.current_workflow)
        
        # Verify the view was updated
        self.mock_view.draw_node.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_select_node(self):
        """Test selecting a node."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        
        # Call the method
        self.presenter.select_node("node2")
        
        # Verify the view was updated
        self.mock_view.select_node_visual.assert_called_once_with("node2")
        self.mock_view.display_properties_for_node.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_update_node_properties(self):
        """Test updating node properties."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        self.presenter.selected_node_id = "node2"
        
        # Set up mock view
        self.mock_view.get_properties_data.return_value = {"selector": "#new-button", "label": "New Label"}
        
        # Call the method
        self.presenter.update_node_properties()
        
        # Verify the node was updated
        self.assertEqual(self.presenter.current_workflow.nodes["node2"].properties["selector"], "#new-button")
        self.assertEqual(self.presenter.current_workflow.nodes["node2"].label, "New Label")
        
        # Verify the view was updated
        self.mock_view.redraw_workflow.assert_called_once_with(self.presenter.current_workflow)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_node(self):
        """Test deleting a node."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        self.presenter.selected_node_id = "node2"
        
        # Call the method
        self.presenter.delete_node()
        
        # Verify the node was deleted
        self.assertNotIn("node2", self.presenter.current_workflow.nodes)
        
        # Verify connections were deleted
        self.assertNotIn("conn1", self.presenter.current_workflow.connections)
        self.assertNotIn("conn2", self.presenter.current_workflow.connections)
        
        # Verify the view was updated
        self.mock_view.redraw_workflow.assert_called_once_with(self.presenter.current_workflow)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_add_connection(self):
        """Test adding a connection."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        
        # Call the method
        self.presenter.add_connection("node1", "output", "node3", "input")
        
        # Verify a connection was added
        self.assertEqual(len(self.presenter.current_workflow.connections), 3)
        
        # Find the new connection
        new_conn = None
        for conn_id, conn in self.presenter.current_workflow.connections.items():
            if conn.source_node_id == "node1" and conn.target_node_id == "node3":
                new_conn = conn
                break
        
        # Verify the connection properties
        self.assertIsNotNone(new_conn)
        self.assertEqual(new_conn.source_port, "output")
        self.assertEqual(new_conn.target_port, "input")
        
        # Verify the view was updated
        self.mock_view.draw_connection.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_connection(self):
        """Test deleting a connection."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        
        # Call the method
        self.presenter.delete_connection("conn1")
        
        # Verify the connection was deleted
        self.assertNotIn("conn1", self.presenter.current_workflow.connections)
        
        # Verify the view was updated
        self.mock_view.redraw_workflow.assert_called_once_with(self.presenter.current_workflow)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_execute_workflow(self):
        """Test executing a workflow."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        
        # Set up mock service
        self.mock_service.execute_workflow.return_value = {
            "workflow_id": "test_workflow",
            "success": True,
            "message": "Workflow executed successfully",
            "results": [],
            "completed": True
        }
        
        # Call the method
        result = self.presenter.execute_workflow()
        
        # Verify the service was called
        self.mock_service.execute_workflow.assert_called_once_with(self.test_workflow)
        
        # Verify the result
        self.assertTrue(result["success"])
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_validate_workflow(self):
        """Test validating a workflow."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        
        # Call the method
        result = self.presenter.validate_workflow()
        
        # Verify the result
        self.assertTrue(result["valid"])
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_validate_workflow_invalid(self):
        """Test validating an invalid workflow."""
        # Set up the presenter with an invalid workflow (no end node)
        invalid_workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            nodes={
                "node1": WorkflowNode(
                    id="node1",
                    type="Start",
                    position=(100, 100),
                    properties={},
                    label="Start"
                ),
                "node2": WorkflowNode(
                    id="node2",
                    type="Click",
                    position=(300, 100),
                    properties={"selector": "#button"},
                    label="Click Button"
                )
            },
            connections={
                "conn1": WorkflowConnection(
                    id="conn1",
                    source_node_id="node1",
                    source_port="output",
                    target_node_id="node2",
                    target_port="input"
                )
            }
        )
        
        self.presenter.current_workflow = invalid_workflow
        
        # Call the method
        result = self.presenter.validate_workflow()
        
        # Verify the result
        self.assertFalse(result["valid"])
        self.assertIn("No End node found", result["errors"])
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()

if __name__ == "__main__":
    unittest.main()
