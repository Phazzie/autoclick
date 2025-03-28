"""Tests for the screenshot action"""
import os
import unittest
import tempfile
from unittest.mock import MagicMock, patch

from src.core.actions.screenshot_action import ScreenshotAction
from src.core.utils.screenshot_capture import CaptureMode


class TestScreenshotAction(unittest.TestCase):
    """Test cases for the screenshot action"""

    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for screenshots
        self.temp_dir = tempfile.TemporaryDirectory()
        self.screenshot_dir = self.temp_dir.name

        # Create a mock driver
        self.mock_driver = MagicMock()

        # Create a mock element
        self.mock_element = MagicMock()
        self.mock_driver.find_element_by_css_selector.return_value = self.mock_element

        # Create a context with the mock driver
        self.context = {"driver": self.mock_driver}

    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()

    @patch('src.core.utils.screenshot_manager.ScreenshotManager.capture_and_save')
    def test_full_screen_screenshot(self, mock_capture_and_save):
        """Test capturing a full screen screenshot"""
        # Arrange
        mock_capture_and_save.return_value = os.path.join(self.screenshot_dir, "test_screenshot.png")
        action = ScreenshotAction(
            description="Capture full screen",
            name="test_screenshot",
            mode="full_screen",
            screenshot_dir=self.screenshot_dir
        )

        # Act
        result = action.execute(self.context)

        # Assert
        self.assertTrue(result.success)
        self.assertIn("Screenshot captured", result.message)
        mock_capture_and_save.assert_called_once()
        self.assertEqual(mock_capture_and_save.call_args[1]["mode"], CaptureMode.FULL_SCREEN)

    @patch('src.core.utils.screenshot_manager.ScreenshotManager.capture_and_save')
    def test_element_screenshot(self, mock_capture_and_save):
        """Test capturing a screenshot of an element"""
        # Arrange
        mock_capture_and_save.return_value = os.path.join(self.screenshot_dir, "test_element.png")
        action = ScreenshotAction(
            description="Capture element",
            name="test_element",
            mode="element",
            selector="#test-element",
            screenshot_dir=self.screenshot_dir
        )

        # Act
        result = action.execute(self.context)

        # Assert
        self.assertTrue(result.success)
        self.assertIn("Screenshot captured", result.message)
        self.mock_driver.find_element_by_css_selector.assert_called_once_with("#test-element")
        mock_capture_and_save.assert_called_once()
        self.assertEqual(mock_capture_and_save.call_args[1]["mode"], CaptureMode.ELEMENT)
        self.assertEqual(mock_capture_and_save.call_args[1]["element"], self.mock_element)

    @patch('src.core.utils.screenshot_manager.ScreenshotManager.capture_and_save')
    def test_region_screenshot(self, mock_capture_and_save):
        """Test capturing a screenshot of a region"""
        # Arrange
        mock_capture_and_save.return_value = os.path.join(self.screenshot_dir, "test_region.png")
        action = ScreenshotAction(
            description="Capture region",
            name="test_region",
            mode="region",
            region=(10, 20, 100, 50),
            screenshot_dir=self.screenshot_dir
        )

        # Act
        result = action.execute(self.context)

        # Assert
        self.assertTrue(result.success)
        self.assertIn("Screenshot captured", result.message)
        mock_capture_and_save.assert_called_once()
        self.assertEqual(mock_capture_and_save.call_args[1]["mode"], CaptureMode.REGION)
        self.assertEqual(mock_capture_and_save.call_args[1]["region"], (10, 20, 100, 50))

    def test_missing_driver(self):
        """Test executing with missing driver"""
        # Arrange
        action = ScreenshotAction(
            description="Capture full screen",
            name="test_screenshot",
            screenshot_dir=self.screenshot_dir
        )

        # Act
        result = action.execute({})  # Empty context

        # Assert
        self.assertFalse(result.success)
        self.assertIn("No browser driver in context", result.message)

    def test_element_not_found(self):
        """Test executing with element not found"""
        # Arrange
        self.mock_driver.find_element_by_css_selector.return_value = None
        action = ScreenshotAction(
            description="Capture element",
            name="test_element",
            mode="element",
            selector="#missing-element",
            screenshot_dir=self.screenshot_dir
        )

        # Act
        result = action.execute(self.context)

        # Assert
        self.assertFalse(result.success)
        self.assertIn("Element not found", result.message)

    def test_invalid_element_mode(self):
        """Test creating action with invalid element mode"""
        # Act & Assert
        with self.assertRaises(ValueError):
            ScreenshotAction(
                description="Invalid element mode",
                name="test_invalid",
                mode="element",
                # Missing selector
                screenshot_dir=self.screenshot_dir
            )

    def test_invalid_region_mode(self):
        """Test creating action with invalid region mode"""
        # Act & Assert
        with self.assertRaises(ValueError):
            ScreenshotAction(
                description="Invalid region mode",
                name="test_invalid",
                mode="region",
                # Missing region
                screenshot_dir=self.screenshot_dir
            )

    def test_serialization(self):
        """Test serializing the action to a dictionary"""
        # Arrange
        action = ScreenshotAction(
            description="Capture region",
            name="test_region",
            mode="region",
            region=(10, 20, 100, 50),
            screenshot_dir=self.screenshot_dir,
            action_id="test-id"
        )

        # Act
        data = action.to_dict()

        # Assert
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["type"], "screenshot")
        self.assertEqual(data["description"], "Capture region")
        self.assertEqual(data["name"], "test_region")
        self.assertEqual(data["mode"], "region")
        self.assertEqual(data["region"], (10, 20, 100, 50))
        self.assertEqual(data["screenshot_dir"], self.screenshot_dir)

    def test_deserialization(self):
        """Test deserializing the action from a dictionary"""
        # Arrange
        data = {
            "id": "test-id",
            "type": "screenshot",
            "description": "Capture region",
            "name": "test_region",
            "mode": "region",
            "region": (10, 20, 100, 50),
            "screenshot_dir": self.screenshot_dir
        }

        # Act
        action = ScreenshotAction.from_dict(data)

        # Assert
        self.assertEqual(action.id, "test-id")
        self.assertEqual(action.description, "Capture region")
        self.assertEqual(action.name, "test_region")
        self.assertEqual(action.mode_str, "region")
        self.assertEqual(action.region, (10, 20, 100, 50))
        self.assertEqual(action.screenshot_dir, self.screenshot_dir)


if __name__ == "__main__":
    unittest.main()
