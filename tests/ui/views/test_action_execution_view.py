"""Tests for the ActionExecutionView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk
import json
import os
import tempfile

from src.ui.views.action_execution_view import ActionExecutionView
from src.core.models import Workflow, WorkflowNode, WorkflowConnection

class TestActionExecutionView(unittest.TestCase):
    """Test cases for the ActionExecutionView class."""
    
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
        self.view = ActionExecutionView(self.root)
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
    
    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.workflow_frame)
        self.assertIsNotNone(self.view.execution_frame)
        self.assertIsNotNone(self.view.details_frame)
        self.assertIsNotNone(self.view.controls_frame)
        self.assertIsNotNone(self.view.progress_frame)
        self.assertIsNotNone(self.view.results_frame)
        self.assertIsNotNone(self.view.workflow_list_frame)
        self.assertIsNotNone(self.view.results_text)
        self.assertIsNotNone(self.view.progress_bar)
        self.assertIsNotNone(self.view.execute_button)
        self.assertIsNotNone(self.view.pause_resume_button)
        self.assertIsNotNone(self.view.stop_button)
        self.assertIsNotNone(self.view.save_button)
    
    def test_update_workflow_list(self):
        """Test updating the workflow list."""
        # Call the method
        self.view.update_workflow_list([self.test_workflow])
        
        # Verify the workflow buttons were created
        self.assertIn(self.test_workflow.id, self.view.workflow_buttons)
        self.assertEqual(len(self.view.workflow_buttons), 1)
    
    def test_display_workflow_details(self):
        """Test displaying workflow details."""
        # Call the method
        self.view.display_workflow_details(self.test_workflow)
        
        # Verify the details were updated
        self.assertEqual(self.view.name_value.cget("text"), self.test_workflow.name)
        self.assertEqual(self.view.id_value.cget("text"), self.test_workflow.id)
        self.assertEqual(self.view.nodes_value.cget("text"), str(len(self.test_workflow.nodes)))
        
        # Verify the selected workflow ID was set
        self.assertEqual(self.view.selected_workflow_id, self.test_workflow.id)
    
    def test_set_execution_controls_state(self):
        """Test setting the execution controls state."""
        # Call the method to enable
        self.view.set_execution_controls_state(True)
        
        # Verify the controls were enabled
        self.assertEqual(self.view.execute_button.cget("state"), "normal")
        self.assertEqual(self.view.save_button.cget("state"), "normal")
        
        # Call the method to disable
        self.view.set_execution_controls_state(False)
        
        # Verify the controls were disabled
        self.assertEqual(self.view.execute_button.cget("state"), "disabled")
        self.assertEqual(self.view.save_button.cget("state"), "disabled")
    
    def test_set_pause_resume_button_state(self):
        """Test setting the pause/resume button state."""
        # Call the method to enable with "Pause" text
        self.view.set_pause_resume_button_state(True, "Pause")
        
        # Verify the button was enabled with "Pause" text
        self.assertEqual(self.view.pause_resume_button.cget("state"), "normal")
        self.assertEqual(self.view.pause_resume_button.cget("text"), "Pause")
        
        # Call the method to enable with "Resume" text
        self.view.set_pause_resume_button_state(True, "Resume")
        
        # Verify the button was enabled with "Resume" text
        self.assertEqual(self.view.pause_resume_button.cget("state"), "normal")
        self.assertEqual(self.view.pause_resume_button.cget("text"), "Resume")
        
        # Call the method to disable
        self.view.set_pause_resume_button_state(False)
        
        # Verify the button was disabled
        self.assertEqual(self.view.pause_resume_button.cget("state"), "disabled")
    
    def test_set_stop_button_state(self):
        """Test setting the stop button state."""
        # Call the method to enable
        self.view.set_stop_button_state(True)
        
        # Verify the button was enabled
        self.assertEqual(self.view.stop_button.cget("state"), "normal")
        
        # Call the method to disable
        self.view.set_stop_button_state(False)
        
        # Verify the button was disabled
        self.assertEqual(self.view.stop_button.cget("state"), "disabled")
    
    def test_update_progress(self):
        """Test updating the progress bar."""
        # Call the method
        self.view.update_progress(2, 5)
        
        # Verify the progress label was updated
        self.assertEqual(self.view.progress_label.cget("text"), "Progress: 2/5")
        
        # Verify the progress bar was updated
        self.assertEqual(self.view.progress_bar.get(), 0.4)  # 2/5 = 0.4
    
    def test_reset_execution_display(self):
        """Test resetting the execution display."""
        # Set up the view with some results
        self.view.results_text.configure(state="normal")
        self.view.results_text.insert("1.0", "Test results")
        self.view.results_text.configure(state="disabled")
        self.view.execution_results = [{"test": "result"}]
        
        # Call the method
        self.view.reset_execution_display()
        
        # Verify the results text was cleared
        self.assertEqual(self.view.results_text.get("1.0", "end-1c"), "")
        
        # Verify the execution results were cleared
        self.assertEqual(self.view.execution_results, [])
    
    def test_add_execution_result(self):
        """Test adding an execution result."""
        # Set up test result
        result = {
            "node_id": "node1",
            "node_type": "Start",
            "node_label": "Start",
            "success": True,
            "message": "Executed Start node: Start",
            "timestamp": 1234567890
        }
        
        # Call the method
        self.view.add_execution_result(result)
        
        # Verify the result was added to the results text
        self.assertIn("Start: Executed Start node: Start", self.view.results_text.get("1.0", "end-1c"))
        
        # Verify the result was added to the execution results
        self.assertEqual(self.view.execution_results, [result])
    
    def test_display_execution_results(self):
        """Test displaying execution results."""
        # Set up test results
        results = {
            "workflow_id": "test_workflow",
            "success": True,
            "message": "Workflow executed successfully",
            "results": [],
            "completed": True
        }
        
        # Set up the view
        self.view.name_value.configure(text="Test Workflow")
        
        # Call the method
        self.view.display_execution_results(results)
        
        # Verify the results were displayed
        result_text = self.view.results_text.get("1.0", "end-1c")
        self.assertIn("Execution Summary", result_text)
        self.assertIn("Workflow: Test Workflow", result_text)
        self.assertIn("Status: Success", result_text)
        self.assertIn("Message: Workflow executed successfully", result_text)
        
        # Verify the save button was enabled
        self.assertEqual(self.view.save_button.cget("state"), "normal")
    
    def test_save_results_to_file_json(self):
        """Test saving results to a JSON file."""
        # Set up test results
        results = [
            {
                "node_id": "node1",
                "node_type": "Start",
                "node_label": "Start",
                "success": True,
                "message": "Executed Start node: Start",
                "timestamp": 1234567890
            }
        ]
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
            file_path = temp_file.name
        
        try:
            # Call the method
            self.view.save_results_to_file(results, file_path)
            
            # Verify the file was created
            self.assertTrue(os.path.exists(file_path))
            
            # Verify the file contains the results
            with open(file_path, "r") as f:
                saved_results = json.load(f)
                self.assertEqual(saved_results, results)
        finally:
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def test_on_workflow_selected(self):
        """Test the workflow selected event handler."""
        # Set up the view
        self.view.workflow_buttons = {
            "test_workflow": MagicMock(),
            "other_workflow": MagicMock()
        }
        
        # Call the method
        self.view._on_workflow_selected("test_workflow")
        
        # Verify the presenter was called
        self.mock_presenter.select_workflow.assert_called_once_with("test_workflow")
        
        # Verify the buttons were updated
        self.view.workflow_buttons["test_workflow"].configure.assert_called_once()
        self.view.workflow_buttons["other_workflow"].configure.assert_called_once()
    
    def test_on_refresh_clicked(self):
        """Test the refresh button click event handler."""
        # Call the method
        self.view._on_refresh_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.load_workflows.assert_called_once()
    
    def test_on_execute_clicked(self):
        """Test the execute button click event handler."""
        # Call the method
        self.view._on_execute_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.execute_workflow.assert_called_once()
    
    def test_on_pause_resume_clicked(self):
        """Test the pause/resume button click event handler."""
        # Call the method
        self.view._on_pause_resume_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.pause_resume_execution.assert_called_once()
    
    def test_on_stop_clicked(self):
        """Test the stop button click event handler."""
        # Call the method
        self.view._on_stop_clicked()
        
        # Verify the presenter was called
        self.mock_presenter.stop_execution.assert_called_once()
    
    def test_on_save_clicked_no_results(self):
        """Test the save button click event handler with no results."""
        # Set up the view
        self.view.execution_results = []
        
        # Mock the messagebox.showinfo method
        with patch("tkinter.messagebox.showinfo") as mock_showinfo:
            # Call the method
            self.view._on_save_clicked()
            
            # Verify the messagebox was shown
            mock_showinfo.assert_called_once()
            
            # Verify the presenter was not called
            self.mock_presenter.save_execution_results.assert_not_called()

if __name__ == "__main__":
    unittest.main()
