"""Tests for the ActionExecutionPresenter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, List, Any

from src.core.models import Workflow, WorkflowNode, WorkflowConnection
from src.ui.presenters.action_execution_presenter import ActionExecutionPresenter
from src.ui.adapters.workflow_adapter import WorkflowAdapter

class TestActionExecutionPresenter(unittest.TestCase):
    """Test cases for the ActionExecutionPresenter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=WorkflowAdapter)
        
        # Create the presenter
        self.presenter = ActionExecutionPresenter(
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
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the service was called
        self.mock_service.get_all_workflows.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_workflow_list.assert_called_once_with([self.test_workflow])
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_load_workflows(self):
        """Test loading workflows."""
        # Call the method
        self.presenter.load_workflows()
        
        # Verify the service was called
        self.mock_service.get_all_workflows.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_workflow_list.assert_called_once_with([self.test_workflow])
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_select_workflow(self):
        """Test selecting a workflow."""
        # Call the method
        self.presenter.select_workflow("test_workflow")
        
        # Verify the service was called
        self.mock_service.get_workflow.assert_called_once_with("test_workflow")
        
        # Verify the view was updated
        self.mock_view.display_workflow_details.assert_called_once_with(self.test_workflow)
        self.mock_view.set_execution_controls_state.assert_called_once_with(True)
        
        # Verify the current workflow was set
        self.assertEqual(self.presenter.current_workflow, self.test_workflow)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_select_workflow_not_found(self):
        """Test selecting a workflow that doesn't exist."""
        # Configure mock service
        self.mock_service.get_workflow.return_value = None
        
        # Call the method
        self.presenter.select_workflow("nonexistent")
        
        # Verify the service was called
        self.mock_service.get_workflow.assert_called_once_with("nonexistent")
        
        # Verify the view was not updated
        self.mock_view.display_workflow_details.assert_not_called()
        self.mock_view.set_execution_controls_state.assert_not_called()
        
        # Verify the current workflow was not set
        self.assertIsNone(self.presenter.current_workflow)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_execute_workflow(self):
        """Test executing a workflow."""
        # Set up the presenter
        self.presenter.current_workflow = self.test_workflow
        
        # Mock the _execute_workflow_thread method
        self.presenter._execute_workflow_thread = MagicMock()
        
        # Call the method
        self.presenter.execute_workflow()
        
        # Verify the view was updated
        self.mock_view.reset_execution_display.assert_called_once()
        self.mock_view.update_progress.assert_called_once_with(0, 3)  # 3 nodes
        self.mock_view.set_execution_controls_state.assert_called_once_with(False)
        self.mock_view.set_pause_resume_button_state.assert_called_once_with(True, "Pause")
        self.mock_view.set_stop_button_state.assert_called_once_with(True)
        
        # Verify the execution state was set
        self.assertTrue(self.presenter.is_executing)
        self.assertFalse(self.presenter.execution_paused)
        self.assertEqual(self.presenter.current_step, 0)
        self.assertEqual(self.presenter.total_steps, 3)  # 3 nodes
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_execute_workflow_no_workflow(self):
        """Test executing a workflow when no workflow is selected."""
        # Set up the presenter
        self.presenter.current_workflow = None
        
        # Call the method
        self.presenter.execute_workflow()
        
        # Verify the view was not updated
        self.mock_view.reset_execution_display.assert_not_called()
        self.mock_view.update_progress.assert_not_called()
        self.mock_view.set_execution_controls_state.assert_not_called()
        
        # Verify the execution state was not set
        self.assertFalse(self.presenter.is_executing)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_pause_resume_execution(self):
        """Test pausing and resuming workflow execution."""
        # Set up the presenter
        self.presenter.is_executing = True
        self.presenter.execution_paused = False
        
        # Call the method to pause
        self.presenter.pause_resume_execution()
        
        # Verify the execution state was set
        self.assertTrue(self.presenter.execution_paused)
        
        # Verify the view was updated
        self.mock_view.set_pause_resume_button_state.assert_called_once_with(True, "Resume")
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
        
        # Reset mocks
        self.mock_view.reset_mock()
        self.mock_app.reset_mock()
        
        # Call the method to resume
        self.presenter.pause_resume_execution()
        
        # Verify the execution state was set
        self.assertFalse(self.presenter.execution_paused)
        
        # Verify the view was updated
        self.mock_view.set_pause_resume_button_state.assert_called_once_with(True, "Pause")
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_stop_execution(self):
        """Test stopping workflow execution."""
        # Set up the presenter
        self.presenter.is_executing = True
        self.presenter.execution_paused = True
        
        # Call the method
        self.presenter.stop_execution()
        
        # Verify the execution state was set
        self.assertFalse(self.presenter.is_executing)
        self.assertFalse(self.presenter.execution_paused)
        
        # Verify the view was updated
        self.mock_view.set_execution_controls_state.assert_called_once_with(True)
        self.mock_view.set_pause_resume_button_state.assert_called_once_with(False, "Pause")
        self.mock_view.set_stop_button_state.assert_called_once_with(False)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_execution_results(self):
        """Test saving execution results."""
        # Set up the presenter
        self.presenter.execution_results = [
            {
                "node_id": "node1",
                "node_type": "Start",
                "node_label": "Start",
                "success": True,
                "message": "Executed Start node: Start",
                "timestamp": 1234567890
            }
        ]
        
        # Call the method
        self.presenter.save_execution_results("results.json")
        
        # Verify the view was called
        self.mock_view.save_results_to_file.assert_called_once_with(
            self.presenter.execution_results, "results.json"
        )
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_execution_results_no_results(self):
        """Test saving execution results when there are no results."""
        # Set up the presenter
        self.presenter.execution_results = []
        
        # Call the method
        self.presenter.save_execution_results("results.json")
        
        # Verify the view was not called
        self.mock_view.save_results_to_file.assert_not_called()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()

if __name__ == "__main__":
    unittest.main()
