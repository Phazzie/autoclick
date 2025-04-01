"""
Tests for the workflow service implementation.

This module contains tests for the workflow service implementation.
"""
import unittest
from unittest.mock import Mock, patch

from src.core.workflow.workflow_service_new import WorkflowService
from src.core.workflow.service_exceptions import (
    WorkflowNotFoundError, WorkflowValidationError, WorkflowExecutionError,
    WorkflowRepositoryError
)


class TestWorkflowService(unittest.TestCase):
    """Tests for the WorkflowService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock dependencies
        self.repository = Mock()
        self.engine = Mock()
        self.validator = Mock()
        self.executor = Mock()
        self.context_factory = Mock()
        
        # Create the service
        self.service = WorkflowService(
            self.repository,
            self.engine,
            self.validator,
            self.executor,
            self.context_factory
        )
        
        # Create mock workflows
        self.workflow1 = Mock()
        self.workflow1.workflow_id = "workflow1"
        self.workflow1.name = "Workflow 1"
        self.workflow1.description = "Test workflow 1"
        self.workflow1.version = "1.0.0"
        self.workflow1.enabled = True
        self.workflow1.get_steps.return_value = [Mock(), Mock()]
        
        self.workflow2 = Mock()
        self.workflow2.workflow_id = "workflow2"
        self.workflow2.name = "Workflow 2"
        self.workflow2.description = "Test workflow 2"
        self.workflow2.version = "1.0.0"
        self.workflow2.enabled = False
        self.workflow2.get_steps.return_value = [Mock()]
        
        # Configure the repository
        self.repository.get_workflow.side_effect = lambda id: {
            "workflow1": self.workflow1,
            "workflow2": self.workflow2
        }.get(id)
        
        self.repository.get_workflows.return_value = [self.workflow1, self.workflow2]
        
        # Configure the engine
        self.engine.create_workflow.return_value = self.workflow1
        self.engine.create_step.return_value = Mock()
        
        # Configure the validator
        self.validator.validate_workflow.return_value = []
        
        # Configure the executor
        self.executor.execute_workflow.return_value = {"result": "success"}
        
        # Configure the context factory
        self.context_factory.create_context.return_value = Mock()
    
    def test_get_workflow(self):
        """Test getting a workflow by ID."""
        # Get existing workflow
        workflow_dto = self.service.get_workflow("workflow1")
        
        self.assertIsNotNone(workflow_dto)
        self.assertEqual(workflow_dto.workflow_id, "workflow1")
        self.assertEqual(workflow_dto.name, "Workflow 1")
        self.assertEqual(workflow_dto.description, "Test workflow 1")
        self.assertEqual(workflow_dto.version, "1.0.0")
        self.assertTrue(workflow_dto.enabled)
        self.assertEqual(workflow_dto.step_count, 2)
        
        # Get nonexistent workflow
        workflow_dto = self.service.get_workflow("nonexistent")
        
        self.assertIsNone(workflow_dto)
        
        # Test repository error
        self.repository.get_workflow.side_effect = WorkflowRepositoryError("Test error")
        
        with self.assertRaises(WorkflowRepositoryError):
            self.service.get_workflow("workflow1")
    
    def test_get_workflows(self):
        """Test getting workflows matching a query."""
        # Get all workflows
        workflow_dtos = self.service.get_workflows()
        
        self.assertEqual(len(workflow_dtos), 2)
        self.assertEqual(workflow_dtos[0].workflow_id, "workflow1")
        self.assertEqual(workflow_dtos[1].workflow_id, "workflow2")
        
        # Get workflows with query
        query = Mock()
        self.service.get_workflows(query)
        
        self.repository.get_workflows.assert_called_with(query)
        
        # Test repository error
        self.repository.get_workflows.side_effect = WorkflowRepositoryError("Test error")
        
        with self.assertRaises(WorkflowRepositoryError):
            self.service.get_workflows()
    
    def test_create_workflow(self):
        """Test creating a workflow."""
        # Create workflow data
        workflow_data = {
            "name": "New Workflow",
            "description": "Test new workflow",
            "version": "1.0.0",
            "enabled": True,
            "steps": [
                {"name": "Step 1", "step_type": "test"},
                {"name": "Step 2", "step_type": "test"}
            ]
        }
        
        # Create workflow
        workflow_dto = self.service.create_workflow(workflow_data)
        
        self.assertIsNotNone(workflow_dto)
        self.assertEqual(workflow_dto.workflow_id, "workflow1")
        self.assertEqual(workflow_dto.name, "Workflow 1")
        
        # Verify engine and repository were called
        self.engine.create_workflow.assert_called_once()
        self.engine.create_step.assert_called()
        self.repository.save_workflow.assert_called_once_with(self.workflow1)
        
        # Test validation error
        self.validator.validate_workflow.return_value = ["Error 1", "Error 2"]
        
        with self.assertRaises(WorkflowValidationError):
            self.service.create_workflow(workflow_data)
        
        # Test repository error
        self.validator.validate_workflow.return_value = []
        self.repository.save_workflow.side_effect = WorkflowRepositoryError("Test error")
        
        with self.assertRaises(WorkflowRepositoryError):
            self.service.create_workflow(workflow_data)
    
    def test_update_workflow(self):
        """Test updating a workflow."""
        # Update workflow data
        workflow_data = {
            "name": "Updated Workflow",
            "description": "Test updated workflow",
            "version": "1.1.0",
            "enabled": False,
            "steps": [
                {"name": "Step 1", "step_type": "test"}
            ]
        }
        
        # Update workflow
        workflow_dto = self.service.update_workflow("workflow1", workflow_data)
        
        self.assertIsNotNone(workflow_dto)
        self.assertEqual(workflow_dto.workflow_id, "workflow1")
        self.assertEqual(workflow_dto.name, "Workflow 1")
        
        # Verify engine and repository were called
        self.engine.create_workflow.assert_called_once()
        self.engine.create_step.assert_called_once()
        self.repository.save_workflow.assert_called_once()
        
        # Test nonexistent workflow
        self.repository.get_workflow.side_effect = lambda id: None
        
        workflow_dto = self.service.update_workflow("nonexistent", workflow_data)
        
        self.assertIsNone(workflow_dto)
        
        # Test validation error
        self.repository.get_workflow.side_effect = lambda id: self.workflow1
        self.validator.validate_workflow.return_value = ["Error 1", "Error 2"]
        
        with self.assertRaises(WorkflowValidationError):
            self.service.update_workflow("workflow1", workflow_data)
        
        # Test repository error
        self.validator.validate_workflow.return_value = []
        self.repository.save_workflow.side_effect = WorkflowRepositoryError("Test error")
        
        with self.assertRaises(WorkflowRepositoryError):
            self.service.update_workflow("workflow1", workflow_data)
    
    def test_delete_workflow(self):
        """Test deleting a workflow."""
        # Delete existing workflow
        result = self.service.delete_workflow("workflow1")
        
        self.assertTrue(result)
        self.repository.delete_workflow.assert_called_once_with("workflow1")
        
        # Delete nonexistent workflow
        self.repository.get_workflow.side_effect = lambda id: None
        
        result = self.service.delete_workflow("nonexistent")
        
        self.assertFalse(result)
        
        # Test repository error
        self.repository.get_workflow.side_effect = lambda id: self.workflow1
        self.repository.delete_workflow.side_effect = WorkflowRepositoryError("Test error")
        
        with self.assertRaises(WorkflowRepositoryError):
            self.service.delete_workflow("workflow1")
    
    def test_execute_workflow(self):
        """Test executing a workflow."""
        # Execute workflow
        result = self.service.execute_workflow("workflow1")
        
        self.assertEqual(result, {"result": "success"})
        self.executor.execute_workflow.assert_called_once_with(self.workflow1, self.context_factory.create_context.return_value)
        
        # Execute workflow with context data
        context_data = {"var1": "value1", "var2": "value2"}
        self.service.execute_workflow("workflow1", context_data)
        
        self.context_factory.create_context.assert_called_with(initial_variables=context_data)
        
        # Test nonexistent workflow
        self.repository.get_workflow.side_effect = lambda id: None
        
        with self.assertRaises(WorkflowNotFoundError):
            self.service.execute_workflow("nonexistent")
        
        # Test execution error
        self.repository.get_workflow.side_effect = lambda id: self.workflow1
        self.executor.execute_workflow.side_effect = Exception("Test error")
        
        with self.assertRaises(WorkflowExecutionError):
            self.service.execute_workflow("workflow1")
    
    def test_validate_workflow(self):
        """Test validating a workflow."""
        # Validate valid workflow
        workflow_data = {
            "name": "Test Workflow",
            "description": "Test workflow",
            "version": "1.0.0",
            "enabled": True,
            "steps": [
                {"name": "Step 1", "step_type": "test"},
                {"name": "Step 2", "step_type": "test"}
            ]
        }
        
        errors = self.service.validate_workflow(workflow_data)
        
        self.assertEqual(errors, [])
        self.validator.validate_workflow.assert_called_once_with(self.workflow1)
        
        # Validate invalid workflow
        self.validator.validate_workflow.return_value = ["Error 1", "Error 2"]
        
        errors = self.service.validate_workflow(workflow_data)
        
        self.assertEqual(errors, ["Error 1", "Error 2"])
        
        # Test engine error
        self.engine.create_workflow.side_effect = Exception("Test error")
        
        errors = self.service.validate_workflow(workflow_data)
        
        self.assertEqual(len(errors), 1)
        self.assertIn("Error validating workflow", errors[0])


if __name__ == "__main__":
    unittest.main()
