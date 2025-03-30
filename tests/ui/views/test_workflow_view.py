"""Tests for the WorkflowView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk

from src.ui.views.workflow_view import WorkflowView
from src.core.models import Workflow, WorkflowNode, WorkflowConnection

class TestWorkflowView(unittest.TestCase):
    """Test cases for the WorkflowView class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by all tests."""
        # Initialize the root window
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the window
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Destroy the root window
        cls.root.destroy()
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock presenter
        self.mock_presenter = MagicMock()
        
        # Create the view
        self.view = WorkflowView(self.root)
        self.view.set_presenter(self.mock_presenter)
        
        # Build the UI
        self.view.build_ui()
        
        # Set up test data
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
        
        self.node_types = [
            {"type": "Start", "name": "Start", "description": "Start of workflow"},
            {"type": "Click", "name": "Click", "description": "Click on element"},
            {"type": "Type", "name": "Type", "description": "Type text"},
            {"type": "Wait", "name": "Wait", "description": "Wait for time or element"},
            {"type": "Condition", "name": "Condition", "description": "Branch based on condition"},
            {"type": "Loop", "name": "Loop", "description": "Repeat actions"},
            {"type": "End", "name": "End", "description": "End of workflow"}
        ]
    
    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.toolbar_frame)
        self.assertIsNotNone(self.view.toolbox_frame)
        self.assertIsNotNone(self.view.canvas_frame)
        self.assertIsNotNone(self.view.properties_frame)
        self.assertIsNotNone(self.view.canvas)
        self.assertIsNotNone(self.view.new_button)
        self.assertIsNotNone(self.view.open_button)
        self.assertIsNotNone(self.view.save_button)
        self.assertIsNotNone(self.view.execute_button)
        self.assertIsNotNone(self.view.validate_button)
    
    def test_initialize_canvas(self):
        """Test initializing the canvas."""
        # Call the method
        self.view.initialize_canvas()
        
        # Verify the canvas was initialized
        self.assertEqual(self.view.canvas.cget("width"), 800)
        self.assertEqual(self.view.canvas.cget("height"), 600)
        self.assertEqual(self.view.canvas_scale, 1.0)
        self.assertEqual(self.view.canvas_offset, (0, 0))
    
    def test_initialize_toolbox(self):
        """Test initializing the toolbox."""
        # Call the method
        self.view.initialize_toolbox(self.node_types)
        
        # Verify the toolbox was initialized
        self.assertEqual(len(self.view.node_buttons), len(self.node_types))
    
    def test_clear_canvas(self):
        """Test clearing the canvas."""
        # Add some items to the canvas
        self.view.canvas.create_rectangle(10, 10, 50, 50, tags=("node", "node1"))
        self.view.canvas.create_line(50, 30, 100, 30, tags=("connection", "conn1"))
        
        # Call the method
        self.view.clear_canvas()
        
        # Verify the canvas was cleared
        self.assertEqual(len(self.view.canvas.find_all()), 0)
        self.assertEqual(self.view.node_elements, {})
        self.assertEqual(self.view.connection_elements, {})
    
    def test_redraw_workflow(self):
        """Test redrawing a workflow."""
        # Mock the draw methods
        self.view.draw_node = MagicMock()
        self.view.draw_connection = MagicMock()
        
        # Call the method
        self.view.redraw_workflow(self.test_workflow)
        
        # Verify the draw methods were called
        self.assertEqual(self.view.draw_node.call_count, 3)  # 3 nodes
        self.assertEqual(self.view.draw_connection.call_count, 2)  # 2 connections
    
    def test_draw_node(self):
        """Test drawing a node."""
        # Call the method
        node = self.test_workflow.nodes["node1"]
        self.view.draw_node(node)
        
        # Verify the node was drawn
        self.assertIn(node.id, self.view.node_elements)
        
        # Verify the canvas has the node
        node_items = self.view.canvas.find_withtag(f"node_{node.id}")
        self.assertGreater(len(node_items), 0)
    
    def test_draw_connection(self):
        """Test drawing a connection."""
        # First draw the nodes
        self.view.draw_node(self.test_workflow.nodes["node1"])
        self.view.draw_node(self.test_workflow.nodes["node2"])
        
        # Call the method
        connection = self.test_workflow.connections["conn1"]
        self.view.draw_connection(connection)
        
        # Verify the connection was drawn
        self.assertIn(connection.id, self.view.connection_elements)
        
        # Verify the canvas has the connection
        connection_items = self.view.canvas.find_withtag(f"connection_{connection.id}")
        self.assertGreater(len(connection_items), 0)
    
    def test_select_node_visual(self):
        """Test selecting a node visually."""
        # First draw a node
        node = self.test_workflow.nodes["node1"]
        self.view.draw_node(node)
        
        # Call the method
        self.view.select_node_visual(node.id)
        
        # Verify the node was selected
        self.assertEqual(self.view.selected_node_id, node.id)
    
    def test_display_properties_for_node(self):
        """Test displaying properties for a node."""
        # Call the method
        node = self.test_workflow.nodes["node2"]
        self.view.display_properties_for_node(node)
        
        # Verify the properties were displayed
        self.assertIsNotNone(self.view.properties_editors)
        self.assertGreater(len(self.view.properties_editors), 0)
    
    def test_get_properties_data(self):
        """Test getting properties data."""
        # Set up the view
        node = self.test_workflow.nodes["node2"]
        self.view.display_properties_for_node(node)
        
        # Mock the property editors
        for prop_name, editor in self.view.properties_editors.items():
            editor.get = MagicMock(return_value=node.properties.get(prop_name, ""))
        
        # Call the method
        data = self.view.get_properties_data()
        
        # Verify the data
        self.assertEqual(data["selector"], "#button")
    
    def test_get_workflow_name(self):
        """Test getting the workflow name."""
        # Set up the view
        self.view.workflow_name_var.set("Test Workflow")
        
        # Call the method
        name = self.view.get_workflow_name()
        
        # Verify the name
        self.assertEqual(name, "Test Workflow")
    
    def test_on_new_clicked(self):
        """Test the new button click event handler."""
        # Mock the dialog
        with patch("tkinter.simpledialog.askstring", return_value="New Workflow"):
            # Call the method
            self.view._on_new_clicked()
            
            # Verify the presenter was called
            self.mock_presenter.create_new_workflow.assert_called_once_with("New Workflow")
    
    def test_on_open_clicked(self):
        """Test the open button click event handler."""
        # Mock the dialog
        with patch("tkinter.filedialog.askopenfilename", return_value="workflow.json"):
            # Call the method
            self.view._on_open_clicked()
            
            # Verify the presenter was called
            self.mock_presenter.load_workflow.assert_called_once_with("workflow.json")
    
    def test_on_save_clicked(self):
        """Test the save button click event handler."""
        # Call the method
        self.view._on_save_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.save_workflow.assert_called_once()
    
    def test_on_execute_clicked(self):
        """Test the execute button click event handler."""
        # Call the method
        self.view._on_execute_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.execute_workflow.assert_called_once()
    
    def test_on_validate_clicked(self):
        """Test the validate button click event handler."""
        # Set up mock presenter
        self.mock_presenter.validate_workflow.return_value = {
            "valid": True,
            "errors": []
        }
        
        # Call the method
        self.view._on_validate_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.validate_workflow.assert_called_once()
    
    def test_on_canvas_click(self):
        """Test the canvas click event handler."""
        # Set up the view
        self.view.selected_node_type = "Click"
        
        # Create a mock event
        event = MagicMock()
        event.x = 200
        event.y = 200
        
        # Call the method
        self.view._on_canvas_click(event)
        
        # Verify the presenter was called
        self.mock_presenter.add_node.assert_called_once_with("Click", (200, 200))
    
    def test_on_node_click(self):
        """Test the node click event handler."""
        # First draw a node
        node = self.test_workflow.nodes["node1"]
        self.view.draw_node(node)
        
        # Create a mock event
        event = MagicMock()
        event.widget = self.view.canvas
        
        # Mock the find_closest method
        self.view.canvas.find_closest = MagicMock(return_value=[self.view.node_elements[node.id]["body"]])
        self.view.canvas.gettags = MagicMock(return_value=(f"node_{node.id}", "body"))
        
        # Call the method
        self.view._on_node_click(event)
        
        # Verify the presenter was called
        self.mock_presenter.select_node.assert_called_once_with(node.id)
    
    def test_on_connection_click(self):
        """Test the connection click event handler."""
        # First draw a connection
        self.view.draw_node(self.test_workflow.nodes["node1"])
        self.view.draw_node(self.test_workflow.nodes["node2"])
        connection = self.test_workflow.connections["conn1"]
        self.view.draw_connection(connection)
        
        # Create a mock event
        event = MagicMock()
        event.widget = self.view.canvas
        
        # Mock the find_closest method
        self.view.canvas.find_closest = MagicMock(return_value=[self.view.connection_elements[connection.id]])
        self.view.canvas.gettags = MagicMock(return_value=(f"connection_{connection.id}",))
        
        # Call the method
        self.view._on_connection_click(event)
        
        # Verify the presenter was called
        self.mock_presenter.delete_connection.assert_called_once_with(connection.id)
    
    def test_on_node_type_selected(self):
        """Test the node type selected event handler."""
        # Call the method
        self.view._on_node_type_selected("Click")
        
        # Verify the selected node type was updated
        self.assertEqual(self.view.selected_node_type, "Click")
    
    def test_on_properties_save(self):
        """Test the properties save event handler."""
        # Call the method
        self.view._on_properties_save()
        
        # Verify the presenter was called
        self.mock_presenter.update_node_properties.assert_called_once()
    
    def test_on_node_delete(self):
        """Test the node delete event handler."""
        # Call the method
        self.view._on_node_delete()
        
        # Verify the presenter was called
        self.mock_presenter.delete_node.assert_called_once()

if __name__ == "__main__":
    unittest.main()
