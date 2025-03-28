"""Tests for the WorkflowModel class"""
import unittest
from src.ui.models.workflow_model import WorkflowModel


class TestWorkflowModel(unittest.TestCase):
    """Test cases for the WorkflowModel class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = WorkflowModel()
        self.test_action = {
            "type": "click",
            "selector": "#test-button",
            "description": "Click test button"
        }

    def test_add_action(self) -> None:
        """Test adding an action to the workflow"""
        # Add an action
        action_id = self.model.add_action(self.test_action)
        
        # Verify the action was added
        self.assertEqual(len(self.model.actions), 1)
        self.assertEqual(self.model.actions[0]["type"], "click")
        self.assertEqual(self.model.actions[0]["selector"], "#test-button")
        self.assertEqual(self.model.actions[0]["description"], "Click test button")
        self.assertEqual(self.model.actions[0]["id"], action_id)

    def test_remove_action(self) -> None:
        """Test removing an action from the workflow"""
        # Add an action
        action_id = self.model.add_action(self.test_action)
        
        # Remove the action
        result = self.model.remove_action(action_id)
        
        # Verify the action was removed
        self.assertTrue(result)
        self.assertEqual(len(self.model.actions), 0)
        
        # Try to remove a non-existent action
        result = self.model.remove_action("non-existent-id")
        self.assertFalse(result)

    def test_get_actions(self) -> None:
        """Test getting all actions"""
        # Add actions
        self.model.add_action({"type": "click", "selector": "#button1"})
        self.model.add_action({"type": "input", "selector": "#input1", "value": "test"})
        
        # Get all actions
        actions = self.model.get_actions()
        
        # Verify the actions
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]["type"], "click")
        self.assertEqual(actions[1]["type"], "input")
        
        # Verify that modifying the returned list doesn't affect the original
        actions.pop(0)
        self.assertEqual(len(self.model.actions), 2)

    def test_get_action(self) -> None:
        """Test getting an action by ID"""
        # Add an action
        action_id = self.model.add_action(self.test_action)
        
        # Get the action
        action = self.model.get_action(action_id)
        
        # Verify the action
        self.assertIsNotNone(action)
        self.assertEqual(action["type"], "click")
        self.assertEqual(action["selector"], "#test-button")
        
        # Try to get a non-existent action
        action = self.model.get_action("non-existent-id")
        self.assertIsNone(action)

    def test_update_action(self) -> None:
        """Test updating an action"""
        # Add an action
        action_id = self.model.add_action(self.test_action)
        
        # Update the action
        updated_action = {
            "type": "input",
            "selector": "#test-input",
            "value": "test value",
            "description": "Enter test value"
        }
        result = self.model.update_action(action_id, updated_action)
        
        # Verify the action was updated
        self.assertTrue(result)
        action = self.model.get_action(action_id)
        self.assertEqual(action["type"], "input")
        self.assertEqual(action["selector"], "#test-input")
        self.assertEqual(action["value"], "test value")
        self.assertEqual(action["description"], "Enter test value")
        
        # Try to update a non-existent action
        result = self.model.update_action("non-existent-id", updated_action)
        self.assertFalse(result)

    def test_reorder_actions(self) -> None:
        """Test reordering actions"""
        # Add actions
        action1_id = self.model.add_action({"type": "click", "selector": "#button1"})
        action2_id = self.model.add_action({"type": "click", "selector": "#button2"})
        action3_id = self.model.add_action({"type": "click", "selector": "#button3"})
        
        # Reorder actions
        result = self.model.reorder_actions([action3_id, action1_id, action2_id])
        
        # Verify the actions were reordered
        self.assertTrue(result)
        actions = self.model.get_actions()
        self.assertEqual(actions[0]["id"], action3_id)
        self.assertEqual(actions[1]["id"], action1_id)
        self.assertEqual(actions[2]["id"], action2_id)
        
        # Try to reorder with an invalid ID
        result = self.model.reorder_actions([action3_id, action1_id, "non-existent-id"])
        self.assertFalse(result)
        
        # Try to reorder with a different number of actions
        result = self.model.reorder_actions([action3_id, action1_id])
        self.assertFalse(result)

    def test_clear(self) -> None:
        """Test clearing the workflow"""
        # Add actions
        self.model.add_action(self.test_action)
        self.model.file_path = "/path/to/workflow.json"
        
        # Clear the workflow
        self.model.clear()
        
        # Verify the workflow was cleared
        self.assertEqual(len(self.model.actions), 0)
        self.assertEqual(self.model.name, "New Workflow")
        self.assertIsNone(self.model.file_path)

    def test_to_dict(self) -> None:
        """Test converting the workflow to a dictionary"""
        # Add actions
        self.model.add_action(self.test_action)
        self.model.name = "Test Workflow"
        
        # Convert to dictionary
        workflow_dict = self.model.to_dict()
        
        # Verify the dictionary
        self.assertEqual(workflow_dict["name"], "Test Workflow")
        self.assertEqual(len(workflow_dict["actions"]), 1)
        self.assertEqual(workflow_dict["actions"][0]["type"], "click")

    def test_from_dict(self) -> None:
        """Test loading the workflow from a dictionary"""
        # Create a workflow dictionary
        workflow_dict = {
            "name": "Imported Workflow",
            "actions": [
                {"type": "click", "selector": "#button1"},
                {"type": "input", "selector": "#input1", "value": "test"}
            ]
        }
        
        # Load from dictionary
        result = self.model.from_dict(workflow_dict)
        
        # Verify the workflow was loaded
        self.assertTrue(result)
        self.assertEqual(self.model.name, "Imported Workflow")
        self.assertEqual(len(self.model.actions), 2)
        self.assertEqual(self.model.actions[0]["type"], "click")
        self.assertEqual(self.model.actions[1]["type"], "input")
        
        # Verify that IDs were added
        self.assertIn("id", self.model.actions[0])
        self.assertIn("id", self.model.actions[1])


if __name__ == "__main__":
    unittest.main()
