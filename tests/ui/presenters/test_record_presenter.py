"""Tests for the RecordPresenter class"""
import unittest
from unittest.mock import MagicMock

from src.ui.models.record_model import RecordModel
from src.ui.presenters.record_presenter import RecordPresenter


class TestRecordPresenter(unittest.TestCase):
    """Test cases for the RecordPresenter class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = RecordModel()
        self.view = MagicMock()
        self.presenter = RecordPresenter(self.model, self.view)
        self.test_action = {
            "type": "click",
            "selector": "#test-button",
            "description": "Click test button"
        }

    def test_start_recording(self) -> None:
        """Test starting recording"""
        # Start recording
        self.presenter.start_recording()
        
        # Verify the model was updated
        self.assertTrue(self.model.is_recording)
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Recording started")

    def test_stop_recording(self) -> None:
        """Test stopping recording"""
        # Start recording
        self.model.start_recording()
        
        # Stop recording
        self.presenter.stop_recording()
        
        # Verify the model was updated
        self.assertFalse(self.model.is_recording)
        
        # Verify the view was updated
        self.view.display_recorded_actions.assert_called_once()
        self.view.show_message.assert_called_once()

    def test_add_recorded_action(self) -> None:
        """Test adding a recorded action"""
        # Add an action
        self.presenter.add_recorded_action(self.test_action)
        
        # Verify the model was updated
        self.assertEqual(len(self.model.recorded_actions), 1)
        self.assertEqual(self.model.recorded_actions[0], self.test_action)
        
        # Verify the view was updated
        self.view.display_recorded_actions.assert_called_once_with(self.model.get_recorded_actions())
        self.view.show_message.assert_called_once()

    def test_clear_recorded_actions(self) -> None:
        """Test clearing recorded actions"""
        # Add actions
        self.model.add_recorded_action(self.test_action)
        
        # Clear actions
        self.presenter.clear_recorded_actions()
        
        # Verify the model was updated
        self.assertEqual(len(self.model.recorded_actions), 0)
        
        # Verify the view was updated
        self.view.display_recorded_actions.assert_called_once_with([])
        self.view.show_message.assert_called_once_with("Recorded actions cleared")

    def test_set_browser_type(self) -> None:
        """Test setting browser type"""
        # Set browser type
        self.presenter.set_browser_type("firefox")
        
        # Verify the model was updated
        self.assertEqual(self.model.browser_type, "firefox")
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Browser type set to firefox")

    def test_set_headless(self) -> None:
        """Test setting headless mode"""
        # Set headless mode
        self.presenter.set_headless(True)
        
        # Verify the model was updated
        self.assertTrue(self.model.headless)
        
        # Verify the view was updated
        self.view.show_message.assert_called_once_with("Headless mode enabled")

    def test_refresh_view(self) -> None:
        """Test refreshing the view"""
        # Add an action
        self.model.add_recorded_action(self.test_action)
        
        # Refresh the view
        self.presenter.refresh_view()
        
        # Verify the view was updated
        self.view.display_recorded_actions.assert_called_once_with(self.model.get_recorded_actions())


if __name__ == "__main__":
    unittest.main()
