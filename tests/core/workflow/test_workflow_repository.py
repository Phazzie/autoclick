"""
Tests for the workflow repository implementation.

This module contains tests for the workflow repository implementation.
"""
import unittest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

from src.core.workflow.workflow_repository import FileSystemWorkflowRepository, InMemoryWorkflowRepository
from src.core.workflow.service_exceptions import WorkflowNotFoundError


class TestInMemoryWorkflowRepository(unittest.TestCase):
    """Tests for the InMemoryWorkflowRepository class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.repository = InMemoryWorkflowRepository()
        
        # Create mock workflows
        self.workflow1 = Mock()
        self.workflow1.workflow_id = "workflow1"
        self.workflow1.name = "Workflow 1"
        self.workflow1.enabled = True
        
        self.workflow2 = Mock()
        self.workflow2.workflow_id = "workflow2"
        self.workflow2.name = "Workflow 2"
        self.workflow2.enabled = False
        
        # Add workflows to repository
        self.repository.save_workflow(self.workflow1)
        self.repository.save_workflow(self.workflow2)
        
        # Create mock query
        self.query = Mock()
        self.query.matches.side_effect = lambda w: w.enabled
    
    def test_get_workflow(self):
        """Test getting a workflow by ID."""
        # Get existing workflow
        workflow = self.repository.get_workflow("workflow1")
        
        self.assertEqual(workflow, self.workflow1)
        
        # Get nonexistent workflow
        workflow = self.repository.get_workflow("nonexistent")
        
        self.assertIsNone(workflow)
    
    def test_get_workflows(self):
        """Test getting workflows matching a query."""
        # Get all workflows
        workflows = self.repository.get_workflows()
        
        self.assertEqual(len(workflows), 2)
        self.assertIn(self.workflow1, workflows)
        self.assertIn(self.workflow2, workflows)
        
        # Get workflows matching query
        workflows = self.repository.get_workflows(self.query)
        
        self.assertEqual(len(workflows), 1)
        self.assertIn(self.workflow1, workflows)
        self.assertNotIn(self.workflow2, workflows)
    
    def test_save_workflow(self):
        """Test saving a workflow."""
        # Create a new workflow
        workflow3 = Mock()
        workflow3.workflow_id = "workflow3"
        
        # Save the workflow
        self.repository.save_workflow(workflow3)
        
        # Verify the workflow was saved
        self.assertEqual(self.repository.get_workflow("workflow3"), workflow3)
        
        # Update an existing workflow
        workflow1_updated = Mock()
        workflow1_updated.workflow_id = "workflow1"
        workflow1_updated.name = "Updated Workflow 1"
        
        # Save the updated workflow
        self.repository.save_workflow(workflow1_updated)
        
        # Verify the workflow was updated
        self.assertEqual(self.repository.get_workflow("workflow1"), workflow1_updated)
    
    def test_delete_workflow(self):
        """Test deleting a workflow."""
        # Delete an existing workflow
        self.repository.delete_workflow("workflow1")
        
        # Verify the workflow was deleted
        self.assertIsNone(self.repository.get_workflow("workflow1"))
        
        # Delete a nonexistent workflow
        with self.assertRaises(WorkflowNotFoundError):
            self.repository.delete_workflow("nonexistent")
    
    def test_count_workflows(self):
        """Test counting workflows matching a query."""
        # Count all workflows
        count = self.repository.count_workflows()
        
        self.assertEqual(count, 2)
        
        # Count workflows matching query
        count = self.repository.count_workflows(self.query)
        
        self.assertEqual(count, 1)


class TestFileSystemWorkflowRepository(unittest.TestCase):
    """Tests for the FileSystemWorkflowRepository class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a mock serializer
        self.serializer = Mock()
        
        # Create the repository
        self.repository = FileSystemWorkflowRepository(self.temp_dir, self.serializer)
        
        # Create mock workflows
        self.workflow1 = Mock()
        self.workflow1.workflow_id = "workflow1"
        self.workflow1.name = "Workflow 1"
        self.workflow1.enabled = True
        
        self.workflow2 = Mock()
        self.workflow2.workflow_id = "workflow2"
        self.workflow2.name = "Workflow 2"
        self.workflow2.enabled = False
        
        # Configure the serializer
        self.serializer.serialize_workflow.side_effect = lambda w: {
            "workflow_id": w.workflow_id,
            "name": w.name,
            "enabled": w.enabled
        }
        
        self.serializer.deserialize_workflow.side_effect = lambda d: Mock(
            workflow_id=d["workflow_id"],
            name=d["name"],
            enabled=d["enabled"]
        )
        
        # Create mock query
        self.query = Mock()
        self.query.matches.side_effect = lambda w: w.enabled
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_get_workflow(self):
        """Test saving and getting a workflow."""
        # Save the workflows
        self.repository.save_workflow(self.workflow1)
        self.repository.save_workflow(self.workflow2)
        
        # Verify the files were created
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "workflow1.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "workflow2.json")))
        
        # Get the workflows
        workflow1 = self.repository.get_workflow("workflow1")
        workflow2 = self.repository.get_workflow("workflow2")
        
        # Verify the workflows were retrieved
        self.assertEqual(workflow1.workflow_id, "workflow1")
        self.assertEqual(workflow1.name, "Workflow 1")
        self.assertTrue(workflow1.enabled)
        
        self.assertEqual(workflow2.workflow_id, "workflow2")
        self.assertEqual(workflow2.name, "Workflow 2")
        self.assertFalse(workflow2.enabled)
        
        # Get a nonexistent workflow
        workflow = self.repository.get_workflow("nonexistent")
        
        self.assertIsNone(workflow)
    
    def test_get_workflows(self):
        """Test getting workflows matching a query."""
        # Save the workflows
        self.repository.save_workflow(self.workflow1)
        self.repository.save_workflow(self.workflow2)
        
        # Get all workflows
        workflows = self.repository.get_workflows()
        
        self.assertEqual(len(workflows), 2)
        self.assertEqual(workflows[0].workflow_id, "workflow1")
        self.assertEqual(workflows[1].workflow_id, "workflow2")
        
        # Get workflows matching query
        workflows = self.repository.get_workflows(self.query)
        
        self.assertEqual(len(workflows), 1)
        self.assertEqual(workflows[0].workflow_id, "workflow1")
    
    def test_delete_workflow(self):
        """Test deleting a workflow."""
        # Save a workflow
        self.repository.save_workflow(self.workflow1)
        
        # Verify the file was created
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "workflow1.json")))
        
        # Delete the workflow
        self.repository.delete_workflow("workflow1")
        
        # Verify the file was deleted
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "workflow1.json")))
        
        # Delete a nonexistent workflow
        with self.assertRaises(WorkflowNotFoundError):
            self.repository.delete_workflow("nonexistent")
    
    def test_count_workflows(self):
        """Test counting workflows matching a query."""
        # Save the workflows
        self.repository.save_workflow(self.workflow1)
        self.repository.save_workflow(self.workflow2)
        
        # Count all workflows
        count = self.repository.count_workflows()
        
        self.assertEqual(count, 2)
        
        # Count workflows matching query
        count = self.repository.count_workflows(self.query)
        
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
