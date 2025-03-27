"""Tests for the RecordModel class"""
import unittest
from src.ui.models.record_model import RecordModel


class TestRecordModel(unittest.TestCase):
    """Test cases for the RecordModel class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = RecordModel()
        self.test_action = {
            "type": "click",
            "selector": "#test-button",
            "description": "Click test button"
        }

    def test_start_recording(self) -> None:
        """Test starting recording"""
        # Start recording
        self.model.start_recording()
        
        # Verify recording state
        self.assertTrue(self.model.is_recording)

    def test_stop_recording(self) -> None:
        """Test stopping recording"""
        # Start recording
        self.model.start_recording()
        
        # Stop recording
        self.model.stop_recording()
        
        # Verify recording state
        self.assertFalse(self.model.is_recording)

    def test_add_recorded_action(self) -> None:
        """Test adding a recorded action"""
        # Add an action
        self.model.add_recorded_action(self.test_action)
        
        # Verify the action was added
        self.assertEqual(len(self.model.recorded_actions), 1)
        self.assertEqual(self.model.recorded_actions[0], self.test_action)

    def test_clear_recorded_actions(self) -> None:
        """Test clearing recorded actions"""
        # Add actions
        self.model.add_recorded_action(self.test_action)
        self.model.add_recorded_action(self.test_action)
        
        # Clear actions
        self.model.clear_recorded_actions()
        
        # Verify actions were cleared
        self.assertEqual(len(self.model.recorded_actions), 0)

    def test_get_recorded_actions(self) -> None:
        """Test getting recorded actions"""
        # Add actions
        self.model.add_recorded_action(self.test_action)
        
        # Get actions
        actions = self.model.get_recorded_actions()
        
        # Verify actions
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0], self.test_action)
        
        # Verify that modifying the returned list doesn't affect the original
        actions.pop(0)
        self.assertEqual(len(self.model.recorded_actions), 1)

    def test_set_browser_type(self) -> None:
        """Test setting browser type"""
        # Set browser type
        self.model.set_browser_type("firefox")
        
        # Verify browser type
        self.assertEqual(self.model.browser_type, "firefox")

    def test_set_headless(self) -> None:
        """Test setting headless mode"""
        # Set headless mode
        self.model.set_headless(True)
        
        # Verify headless mode
        self.assertTrue(self.model.headless)


if __name__ == "__main__":
    unittest.main()
