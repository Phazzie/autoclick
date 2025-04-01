"""
Tests for the workflow DTO implementation.

This module contains tests for the workflow DTO implementation.
"""
import unittest
from unittest.mock import Mock

from src.core.workflow.workflow_dto import WorkflowDTO, WorkflowStepDTO


class TestWorkflowDTO(unittest.TestCase):
    """Tests for the WorkflowDTO class."""
    
    def test_basic_properties(self):
        """Test basic DTO properties."""
        dto = WorkflowDTO(
            workflow_id="test-workflow",
            name="Test Workflow",
            description="Test workflow description",
            version="1.0.0",
            enabled=True,
            step_count=3,
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-02T00:00:00",
            metadata={"key": "value"}
        )
        
        self.assertEqual(dto.workflow_id, "test-workflow")
        self.assertEqual(dto.name, "Test Workflow")
        self.assertEqual(dto.description, "Test workflow description")
        self.assertEqual(dto.version, "1.0.0")
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.step_count, 3)
        self.assertEqual(dto.created_at, "2023-01-01T00:00:00")
        self.assertEqual(dto.updated_at, "2023-01-02T00:00:00")
        self.assertEqual(dto.metadata, {"key": "value"})
    
    def test_to_dict(self):
        """Test converting DTO to dictionary."""
        dto = WorkflowDTO(
            workflow_id="test-workflow",
            name="Test Workflow",
            description="Test workflow description",
            version="1.0.0",
            enabled=True,
            step_count=3,
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-02T00:00:00",
            metadata={"key": "value"}
        )
        
        expected = {
            "workflow_id": "test-workflow",
            "name": "Test Workflow",
            "description": "Test workflow description",
            "version": "1.0.0",
            "enabled": True,
            "step_count": 3,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "metadata": {"key": "value"}
        }
        
        self.assertEqual(dto.to_dict(), expected)
    
    def test_from_workflow(self):
        """Test creating DTO from workflow."""
        # Create a mock workflow
        workflow = Mock()
        workflow.workflow_id = "test-workflow"
        workflow.name = "Test Workflow"
        workflow.description = "Test workflow description"
        workflow.version = "1.0.0"
        workflow.enabled = True
        workflow.get_steps.return_value = [Mock(), Mock(), Mock()]
        workflow.metadata = {"key": "value"}
        
        # Create DTO from workflow
        dto = WorkflowDTO.from_workflow(workflow)
        
        self.assertEqual(dto.workflow_id, "test-workflow")
        self.assertEqual(dto.name, "Test Workflow")
        self.assertEqual(dto.description, "Test workflow description")
        self.assertEqual(dto.version, "1.0.0")
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.step_count, 3)
        self.assertEqual(dto.metadata, {"key": "value"})
    
    def test_from_dict(self):
        """Test creating DTO from dictionary."""
        data = {
            "workflow_id": "test-workflow",
            "name": "Test Workflow",
            "description": "Test workflow description",
            "version": "1.0.0",
            "enabled": True,
            "step_count": 3,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "metadata": {"key": "value"}
        }
        
        # Create DTO from dictionary
        dto = WorkflowDTO.from_dict(data)
        
        self.assertEqual(dto.workflow_id, "test-workflow")
        self.assertEqual(dto.name, "Test Workflow")
        self.assertEqual(dto.description, "Test workflow description")
        self.assertEqual(dto.version, "1.0.0")
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.step_count, 3)
        self.assertEqual(dto.created_at, "2023-01-01T00:00:00")
        self.assertEqual(dto.updated_at, "2023-01-02T00:00:00")
        self.assertEqual(dto.metadata, {"key": "value"})
    
    def test_from_dict_with_defaults(self):
        """Test creating DTO from dictionary with defaults."""
        data = {
            "name": "Test Workflow"
        }
        
        # Create DTO from dictionary
        dto = WorkflowDTO.from_dict(data)
        
        self.assertIsNotNone(dto.workflow_id)
        self.assertEqual(dto.name, "Test Workflow")
        self.assertIsNone(dto.description)
        self.assertEqual(dto.version, "1.0.0")
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.step_count, 0)
        self.assertEqual(dto.metadata, {})


class TestWorkflowStepDTO(unittest.TestCase):
    """Tests for the WorkflowStepDTO class."""
    
    def test_basic_properties(self):
        """Test basic DTO properties."""
        dto = WorkflowStepDTO(
            step_id="test-step",
            step_type="test-type",
            name="Test Step",
            description="Test step description",
            enabled=True,
            config={"param": "value"},
            metadata={"key": "value"}
        )
        
        self.assertEqual(dto.step_id, "test-step")
        self.assertEqual(dto.step_type, "test-type")
        self.assertEqual(dto.name, "Test Step")
        self.assertEqual(dto.description, "Test step description")
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.config, {"param": "value"})
        self.assertEqual(dto.metadata, {"key": "value"})
    
    def test_to_dict(self):
        """Test converting DTO to dictionary."""
        dto = WorkflowStepDTO(
            step_id="test-step",
            step_type="test-type",
            name="Test Step",
            description="Test step description",
            enabled=True,
            config={"param": "value"},
            metadata={"key": "value"}
        )
        
        expected = {
            "step_id": "test-step",
            "step_type": "test-type",
            "name": "Test Step",
            "description": "Test step description",
            "enabled": True,
            "config": {"param": "value"},
            "metadata": {"key": "value"}
        }
        
        self.assertEqual(dto.to_dict(), expected)
    
    def test_from_step(self):
        """Test creating DTO from step."""
        # Create a mock step
        step = Mock()
        step.step_id = "test-step"
        step.step_type = "test-type"
        step.name = "Test Step"
        step.description = "Test step description"
        step.enabled = True
        step.config = {"param": "value"}
        step.metadata = {"key": "value"}
        
        # Create DTO from step
        dto = WorkflowStepDTO.from_step(step)
        
        self.assertEqual(dto.step_id, "test-step")
        self.assertEqual(dto.step_type, "test-type")
        self.assertEqual(dto.name, "Test Step")
        self.assertEqual(dto.description, "Test step description")
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.config, {"param": "value"})
        self.assertEqual(dto.metadata, {"key": "value"})
    
    def test_from_dict(self):
        """Test creating DTO from dictionary."""
        data = {
            "step_id": "test-step",
            "step_type": "test-type",
            "name": "Test Step",
            "description": "Test step description",
            "enabled": True,
            "config": {"param": "value"},
            "metadata": {"key": "value"}
        }
        
        # Create DTO from dictionary
        dto = WorkflowStepDTO.from_dict(data)
        
        self.assertEqual(dto.step_id, "test-step")
        self.assertEqual(dto.step_type, "test-type")
        self.assertEqual(dto.name, "Test Step")
        self.assertEqual(dto.description, "Test step description")
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.config, {"param": "value"})
        self.assertEqual(dto.metadata, {"key": "value"})
    
    def test_from_dict_with_defaults(self):
        """Test creating DTO from dictionary with defaults."""
        data = {
            "name": "Test Step"
        }
        
        # Create DTO from dictionary
        dto = WorkflowStepDTO.from_dict(data)
        
        self.assertIsNotNone(dto.step_id)
        self.assertEqual(dto.step_type, "unknown")
        self.assertEqual(dto.name, "Test Step")
        self.assertIsNone(dto.description)
        self.assertTrue(dto.enabled)
        self.assertEqual(dto.config, {})
        self.assertEqual(dto.metadata, {})


if __name__ == "__main__":
    unittest.main()
