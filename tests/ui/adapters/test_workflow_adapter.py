"""Tests for the WorkflowAdapter class."""
import unittest
from unittest.mock import MagicMock, patch

from src.core.workflow.workflow_service_new import WorkflowService
from src.ui.adapters.impl.workflow_adapter import WorkflowAdapter


class TestWorkflowAdapter(unittest.TestCase):
    """Test cases for the WorkflowAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_workflow_service = MagicMock(spec=WorkflowService)
        self.adapter = WorkflowAdapter(self.mock_workflow_service)
    
    def test_get_workflow_types(self):
        """Test getting workflow types."""
        # Act
        result = self.adapter.get_workflow_types()
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "standard")
        self.assertEqual(result[0]["name"], "Standard Workflow")
    
    def test_get_all_workflows(self):
        """Test getting all workflows."""
        # Arrange
        mock_workflow1 = MagicMock()
        mock_workflow1.workflow_id = "workflow1"
        mock_workflow1.name = "Workflow 1"
        mock_workflow1.description = "Test workflow 1"
        mock_workflow1.version = "1.0.0"
        mock_workflow1.enabled = True
        mock_workflow1.steps = []
        mock_workflow1.step_count = 0
        mock_workflow1.created_at = "2023-01-01T00:00:00Z"
        mock_workflow1.updated_at = "2023-01-01T00:00:00Z"
        
        mock_workflow2 = MagicMock()
        mock_workflow2.workflow_id = "workflow2"
        mock_workflow2.name = "Workflow 2"
        mock_workflow2.description = "Test workflow 2"
        mock_workflow2.version = "1.0.0"
        mock_workflow2.enabled = True
        mock_workflow2.steps = []
        mock_workflow2.step_count = 0
        mock_workflow2.created_at = "2023-01-01T00:00:00Z"
        mock_workflow2.updated_at = "2023-01-01T00:00:00Z"
        
        self.mock_workflow_service.get_workflows.return_value = [mock_workflow1, mock_workflow2]
        
        # Act
        result = self.adapter.get_all_workflows()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "workflow1")
        self.assertEqual(result[0]["name"], "Workflow 1")
        self.assertEqual(result[1]["id"], "workflow2")
        self.assertEqual(result[1]["name"], "Workflow 2")
        
        # Verify service was called
        self.mock_workflow_service.get_workflows.assert_called_once()
    
    def test_get_workflow(self):
        """Test getting a workflow by ID."""
        # Arrange
        mock_workflow = MagicMock()
        mock_workflow.workflow_id = "workflow1"
        mock_workflow.name = "Workflow 1"
        mock_workflow.description = "Test workflow 1"
        mock_workflow.version = "1.0.0"
        mock_workflow.enabled = True
        mock_workflow.steps = []
        mock_workflow.step_count = 0
        mock_workflow.created_at = "2023-01-01T00:00:00Z"
        mock_workflow.updated_at = "2023-01-01T00:00:00Z"
        
        self.mock_workflow_service.get_workflow.return_value = mock_workflow
        
        # Act
        result = self.adapter.get_workflow("workflow1")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "workflow1")
        self.assertEqual(result["name"], "Workflow 1")
        
        # Verify service was called
        self.mock_workflow_service.get_workflow.assert_called_once_with("workflow1")
    
    def test_get_workflow_not_found(self):
        """Test getting a workflow that doesn't exist."""
        # Arrange
        self.mock_workflow_service.get_workflow.return_value = None
        
        # Act
        result = self.adapter.get_workflow("nonexistent")
        
        # Assert
        self.assertIsNone(result)
        
        # Verify service was called
        self.mock_workflow_service.get_workflow.assert_called_once_with("nonexistent")
    
    def test_create_workflow(self):
        """Test creating a workflow."""
        # Arrange
        workflow_data = {
            "name": "New Workflow",
            "description": "Test new workflow",
            "version": "1.0.0",
            "enabled": True,
            "steps": []
        }
        
        mock_workflow = MagicMock()
        mock_workflow.workflow_id = "new-workflow"
        mock_workflow.name = "New Workflow"
        mock_workflow.description = "Test new workflow"
        mock_workflow.version = "1.0.0"
        mock_workflow.enabled = True
        mock_workflow.steps = []
        mock_workflow.step_count = 0
        mock_workflow.created_at = "2023-01-01T00:00:00Z"
        mock_workflow.updated_at = "2023-01-01T00:00:00Z"
        
        self.mock_workflow_service.create_workflow.return_value = mock_workflow
        self.mock_workflow_service.validate_workflow.return_value = []
        
        # Act
        result = self.adapter.create_workflow(workflow_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "new-workflow")
        self.assertEqual(result["name"], "New Workflow")
        
        # Verify service was called
        self.mock_workflow_service.validate_workflow.assert_called_once()
        self.mock_workflow_service.create_workflow.assert_called_once()
    
    def test_create_workflow_invalid(self):
        """Test creating a workflow with invalid data."""
        # Arrange
        workflow_data = {
            "name": "",  # Invalid: empty name
            "description": "Test new workflow",
            "version": "1.0.0",
            "enabled": True,
            "steps": []
        }
        
        self.mock_workflow_service.validate_workflow.return_value = ["Name is required"]
        
        # Act/Assert
        with self.assertRaises(ValueError) as context:
            self.adapter.create_workflow(workflow_data)
        
        # Verify error message
        self.assertIn("Invalid workflow data", str(context.exception))
        
        # Verify service was called
        self.mock_workflow_service.validate_workflow.assert_called_once()
        self.mock_workflow_service.create_workflow.assert_not_called()
    
    def test_update_workflow(self):
        """Test updating a workflow."""
        # Arrange
        workflow_data = {
            "name": "Updated Workflow",
            "description": "Test updated workflow",
            "version": "1.0.1",
            "enabled": True,
            "steps": []
        }
        
        mock_workflow = MagicMock()
        mock_workflow.workflow_id = "workflow1"
        mock_workflow.name = "Updated Workflow"
        mock_workflow.description = "Test updated workflow"
        mock_workflow.version = "1.0.1"
        mock_workflow.enabled = True
        mock_workflow.steps = []
        mock_workflow.step_count = 0
        mock_workflow.created_at = "2023-01-01T00:00:00Z"
        mock_workflow.updated_at = "2023-01-02T00:00:00Z"
        
        self.mock_workflow_service.update_workflow.return_value = mock_workflow
        self.mock_workflow_service.validate_workflow.return_value = []
        
        # Act
        result = self.adapter.update_workflow("workflow1", workflow_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "workflow1")
        self.assertEqual(result["name"], "Updated Workflow")
        
        # Verify service was called
        self.mock_workflow_service.validate_workflow.assert_called_once()
        self.mock_workflow_service.update_workflow.assert_called_once_with("workflow1", self.adapter._convert_workflow_from_ui_format(workflow_data))
    
    def test_update_workflow_not_found(self):
        """Test updating a workflow that doesn't exist."""
        # Arrange
        workflow_data = {
            "name": "Updated Workflow",
            "description": "Test updated workflow",
            "version": "1.0.1",
            "enabled": True,
            "steps": []
        }
        
        self.mock_workflow_service.update_workflow.return_value = None
        self.mock_workflow_service.validate_workflow.return_value = []
        
        # Act
        result = self.adapter.update_workflow("nonexistent", workflow_data)
        
        # Assert
        self.assertIsNone(result)
        
        # Verify service was called
        self.mock_workflow_service.validate_workflow.assert_called_once()
        self.mock_workflow_service.update_workflow.assert_called_once()
    
    def test_delete_workflow(self):
        """Test deleting a workflow."""
        # Arrange
        self.mock_workflow_service.delete_workflow.return_value = True
        
        # Act
        result = self.adapter.delete_workflow("workflow1")
        
        # Assert
        self.assertTrue(result)
        
        # Verify service was called
        self.mock_workflow_service.delete_workflow.assert_called_once_with("workflow1")
    
    def test_delete_workflow_not_found(self):
        """Test deleting a workflow that doesn't exist."""
        # Arrange
        self.mock_workflow_service.delete_workflow.return_value = False
        
        # Act
        result = self.adapter.delete_workflow("nonexistent")
        
        # Assert
        self.assertFalse(result)
        
        # Verify service was called
        self.mock_workflow_service.delete_workflow.assert_called_once_with("nonexistent")
    
    def test_execute_workflow(self):
        """Test executing a workflow."""
        # Arrange
        context_data = {"variable1": "value1"}
        expected_result = {"status": "success", "data": {"output": "result"}}
        
        self.mock_workflow_service.execute_workflow.return_value = expected_result
        
        # Act
        result = self.adapter.execute_workflow("workflow1", context_data)
        
        # Assert
        self.assertEqual(result, expected_result)
        
        # Verify service was called
        self.mock_workflow_service.execute_workflow.assert_called_once_with("workflow1", context_data)
    
    def test_execute_workflow_error(self):
        """Test executing a workflow that raises an error."""
        # Arrange
        context_data = {"variable1": "value1"}
        
        self.mock_workflow_service.execute_workflow.side_effect = Exception("Test error")
        
        # Act/Assert
        with self.assertRaises(ValueError) as context:
            self.adapter.execute_workflow("workflow1", context_data)
        
        # Verify error message
        self.assertIn("Error executing workflow", str(context.exception))
        
        # Verify service was called
        self.mock_workflow_service.execute_workflow.assert_called_once_with("workflow1", context_data)
    
    def test_validate_workflow(self):
        """Test validating a workflow."""
        # Arrange
        workflow_data = {
            "name": "Test Workflow",
            "description": "Test workflow",
            "version": "1.0.0",
            "enabled": True,
            "steps": []
        }
        
        self.mock_workflow_service.validate_workflow.return_value = []
        
        # Act
        result = self.adapter.validate_workflow(workflow_data)
        
        # Assert
        self.assertEqual(result, [])
        
        # Verify service was called
        self.mock_workflow_service.validate_workflow.assert_called_once()
    
    def test_validate_workflow_invalid(self):
        """Test validating an invalid workflow."""
        # Arrange
        workflow_data = {
            "name": "",  # Invalid: empty name
            "description": "Test workflow",
            "version": "1.0.0",
            "enabled": True,
            "steps": []
        }
        
        self.mock_workflow_service.validate_workflow.return_value = ["Name is required"]
        
        # Act
        result = self.adapter.validate_workflow(workflow_data)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Name is required")
        
        # Verify service was called
        self.mock_workflow_service.validate_workflow.assert_called_once()


if __name__ == "__main__":
    unittest.main()
