"""Tests for the workflow builder"""
import json
import os
import tempfile
import unittest
from typing import Dict, Any, List

from src.ui.workflow_builder import WorkflowBuilder


class TestWorkflowBuilder(unittest.TestCase):
    """Test cases for the WorkflowBuilder class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.builder = WorkflowBuilder()
        self.sample_action = {
            "type": "click",
            "selector": "#submit-button",
            "description": "Click submit button"
        }

    def test_add_action(self) -> None:
        """Test adding an action to the workflow"""
        # Add an action
        action_id = self.builder.add_action(self.sample_action)
        
        # Verify the action was added
        self.assertEqual(len(self.builder.actions), 1)
        self.assertIn(action_id, self.builder.action_ids)
        self.assertEqual(self.builder.action_ids[action_id], 0)
        
        # Verify the action data
        action = self.builder.actions[0]
        self.assertEqual(action["type"], "click")
        self.assertEqual(action["selector"], "#submit-button")
        self.assertEqual(action["description"], "Click submit button")
        self.assertEqual(action["id"], action_id)

    def test_remove_action(self) -> None:
        """Test removing an action from the workflow"""
        # Add an action
        action_id = self.builder.add_action(self.sample_action)
        
        # Remove the action
        result = self.builder.remove_action(action_id)
        
        # Verify the action was removed
        self.assertTrue(result)
        self.assertEqual(len(self.builder.actions), 0)
        self.assertNotIn(action_id, self.builder.action_ids)
        
        # Try to remove a non-existent action
        result = self.builder.remove_action("non-existent-id")
        self.assertFalse(result)

    def test_reorder_actions(self) -> None:
        """Test reordering actions in the workflow"""
        # Add multiple actions
        action1_id = self.builder.add_action({"type": "click", "selector": "#button1"})
        action2_id = self.builder.add_action({"type": "click", "selector": "#button2"})
        action3_id = self.builder.add_action({"type": "click", "selector": "#button3"})
        
        # Reorder the actions
        result = self.builder.reorder_actions([action3_id, action1_id, action2_id])
        
        # Verify the actions were reordered
        self.assertTrue(result)
        self.assertEqual(len(self.builder.actions), 3)
        self.assertEqual(self.builder.actions[0]["selector"], "#button3")
        self.assertEqual(self.builder.actions[1]["selector"], "#button1")
        self.assertEqual(self.builder.actions[2]["selector"], "#button2")
        
        # Verify the action_ids were updated
        self.assertEqual(self.builder.action_ids[action3_id], 0)
        self.assertEqual(self.builder.action_ids[action1_id], 1)
        self.assertEqual(self.builder.action_ids[action2_id], 2)
        
        # Try to reorder with an invalid ID
        result = self.builder.reorder_actions([action3_id, action1_id, "invalid-id"])
        self.assertFalse(result)
        
        # Try to reorder with missing actions
        result = self.builder.reorder_actions([action3_id, action1_id])
        self.assertFalse(result)

    def test_export_workflow(self) -> None:
        """Test exporting a workflow"""
        # Add actions
        self.builder.add_action({"type": "click", "selector": "#button1"})
        self.builder.add_action({"type": "input", "selector": "#input1", "value": "test"})
        
        # Export the workflow
        config = self.builder.export_workflow()
        
        # Verify the exported workflow
        self.assertEqual(config["name"], "Exported Workflow")
        self.assertEqual(config["version"], "1.0.0")
        self.assertEqual(len(config["actions"]), 2)
        self.assertEqual(config["actions"][0]["type"], "click")
        self.assertEqual(config["actions"][1]["type"], "input")

    def test_import_workflow(self) -> None:
        """Test importing a workflow"""
        # Create a workflow configuration
        config = {
            "name": "Test Workflow",
            "description": "Test workflow for import",
            "version": "1.0.0",
            "actions": [
                {"type": "click", "selector": "#button1", "id": "action1"},
                {"type": "input", "selector": "#input1", "value": "test", "id": "action2"}
            ]
        }
        
        # Import the workflow
        result = self.builder.import_workflow(config)
        
        # Verify the workflow was imported
        self.assertTrue(result)
        self.assertEqual(len(self.builder.actions), 2)
        self.assertEqual(self.builder.actions[0]["type"], "click")
        self.assertEqual(self.builder.actions[1]["type"], "input")
        self.assertEqual(self.builder.action_ids["action1"], 0)
        self.assertEqual(self.builder.action_ids["action2"], 1)
        
        # Test importing a workflow without IDs
        config = {
            "name": "Test Workflow",
            "description": "Test workflow for import",
            "version": "1.0.0",
            "actions": [
                {"type": "click", "selector": "#button1"},
                {"type": "input", "selector": "#input1", "value": "test"}
            ]
        }
        
        # Import the workflow
        result = self.builder.import_workflow(config)
        
        # Verify the workflow was imported and IDs were generated
        self.assertTrue(result)
        self.assertEqual(len(self.builder.actions), 2)
        self.assertEqual(len(self.builder.action_ids), 2)

    def test_save_and_load_workflow(self) -> None:
        """Test saving and loading a workflow"""
        # Add actions
        self.builder.add_action({"type": "click", "selector": "#button1"})
        self.builder.add_action({"type": "input", "selector": "#input1", "value": "test"})
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_path = temp_file.name
        
        try:
            # Save the workflow
            result = self.builder.save_workflow(temp_path)
            self.assertTrue(result)
            
            # Create a new builder
            new_builder = WorkflowBuilder()
            
            # Load the workflow
            result = new_builder.load_workflow(temp_path)
            self.assertTrue(result)
            
            # Verify the loaded workflow
            self.assertEqual(len(new_builder.actions), 2)
            self.assertEqual(new_builder.actions[0]["type"], "click")
            self.assertEqual(new_builder.actions[1]["type"], "input")
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_get_actions(self) -> None:
        """Test getting all actions"""
        # Add actions
        self.builder.add_action({"type": "click", "selector": "#button1"})
        self.builder.add_action({"type": "input", "selector": "#input1", "value": "test"})
        
        # Get all actions
        actions = self.builder.get_actions()
        
        # Verify the actions
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]["type"], "click")
        self.assertEqual(actions[1]["type"], "input")
        
        # Verify that modifying the returned list doesn't affect the original
        actions.pop(0)
        self.assertEqual(len(self.builder.actions), 2)

    def test_get_action(self) -> None:
        """Test getting an action by ID"""
        # Add an action
        action_id = self.builder.add_action(self.sample_action)
        
        # Get the action
        action = self.builder.get_action(action_id)
        
        # Verify the action
        self.assertIsNotNone(action)
        self.assertEqual(action["type"], "click")
        self.assertEqual(action["selector"], "#submit-button")
        
        # Try to get a non-existent action
        action = self.builder.get_action("non-existent-id")
        self.assertIsNone(action)

    def test_update_action(self) -> None:
        """Test updating an action"""
        # Add an action
        action_id = self.builder.add_action(self.sample_action)
        
        # Update the action
        updated_action = {
            "type": "input",
            "selector": "#email-input",
            "value": "test@example.com",
            "description": "Enter email"
        }
        result = self.builder.update_action(action_id, updated_action)
        
        # Verify the action was updated
        self.assertTrue(result)
        action = self.builder.get_action(action_id)
        self.assertEqual(action["type"], "input")
        self.assertEqual(action["selector"], "#email-input")
        self.assertEqual(action["value"], "test@example.com")
        
        # Try to update a non-existent action
        result = self.builder.update_action("non-existent-id", updated_action)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
