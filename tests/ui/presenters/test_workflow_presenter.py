"""Tests for the WorkflowPresenter class"""
import unittest
from unittest.mock import MagicMock

from src.ui.models.workflow_model import WorkflowModel
from src.ui.presenters.workflow_presenter import WorkflowPresenter


class TestWorkflowPresenter(unittest.TestCase):
    """Test cases for the WorkflowPresenter class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = WorkflowModel()
        self.view = MagicMock()
        self.presenter = WorkflowPresenter(self.model, self.view)
        self.test_action = {
            "type": "click",
            "selector": "#test-button",
            "description": "Click test button"
        }

    def test_add_action(self) -> None:
        """Test adding an action"""
        # Add an action
        self.presenter.add_action(self.test_action)
        
        # Verify the action was added to the model
        self.assertEqual(len(self.model.actions), 1)
        self.assertEqual(self.model.actions[0]["type"], "click")
        
        # Verify the view was refreshed
        self.view.display_actions.assert_called_once()
        
        # Verify a message was shown
        self.view.show_message.assert_called_once()

    def test_remove_action(self) -> None:
        """Test removing an action"""
        # Add an action
        action_id = self.model.add_action(self.test_action)
        
        # Mock the view to return the action ID
        self.view.get_selected_action_id.return_value = action_id
        
        # Remove the action
        self.presenter.remove_action()
        
        # Verify the action was removed from the model
        self.assertEqual(len(self.model.actions), 0)
        
        # Verify the view was refreshed
        self.view.display_actions.assert_called_once()
        
        # Verify a message was shown
        self.view.show_message.assert_called_once()

    def test_remove_action_no_selection(self) -> None:
        """Test removing an action with no selection"""
        # Mock the view to return None (no selection)
        self.view.get_selected_action_id.return_value = None
        
        # Remove the action
        self.presenter.remove_action()
        
        # Verify a message was shown
        self.view.show_message.assert_called_once_with("No action selected")
        
        # Verify the view was not refreshed
        self.view.display_actions.assert_not_called()

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
        self.presenter.update_action(action_id, updated_action)
        
        # Verify the action was updated in the model
        action = self.model.get_action(action_id)
        self.assertEqual(action["type"], "input")
        
        # Verify the view was refreshed
        self.view.display_actions.assert_called_once()
        
        # Verify a message was shown
        self.view.show_message.assert_called_once()

    def test_move_action_up(self) -> None:
        """Test moving an action up"""
        # Add actions
        action1_id = self.model.add_action({"type": "click", "selector": "#button1"})
        action2_id = self.model.add_action({"type": "click", "selector": "#button2"})
        
        # Mock the view to return the second action ID
        self.view.get_selected_action_id.return_value = action2_id
        
        # Move the action up
        self.presenter.move_action_up()
        
        # Verify the actions were reordered in the model
        actions = self.model.get_actions()
        self.assertEqual(actions[0]["id"], action2_id)
        self.assertEqual(actions[1]["id"], action1_id)
        
        # Verify the view was refreshed
        self.view.display_actions.assert_called_once()
        
        # Verify a message was shown
        self.view.show_message.assert_called_once_with("Action moved up")

    def test_move_action_down(self) -> None:
        """Test moving an action down"""
        # Add actions
        action1_id = self.model.add_action({"type": "click", "selector": "#button1"})
        action2_id = self.model.add_action({"type": "click", "selector": "#button2"})
        
        # Mock the view to return the first action ID
        self.view.get_selected_action_id.return_value = action1_id
        
        # Move the action down
        self.presenter.move_action_down()
        
        # Verify the actions were reordered in the model
        actions = self.model.get_actions()
        self.assertEqual(actions[0]["id"], action2_id)
        self.assertEqual(actions[1]["id"], action1_id)
        
        # Verify the view was refreshed
        self.view.display_actions.assert_called_once()
        
        # Verify a message was shown
        self.view.show_message.assert_called_once_with("Action moved down")

    def test_refresh_view(self) -> None:
        """Test refreshing the view"""
        # Add an action
        self.model.add_action(self.test_action)
        
        # Refresh the view
        self.presenter.refresh_view()
        
        # Verify the view was refreshed with the model's actions
        self.view.display_actions.assert_called_once_with(self.model.get_actions())


if __name__ == "__main__":
    unittest.main()
