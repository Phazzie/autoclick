"""Tests for the screenshot manager"""
import os
import unittest
import tempfile
from unittest.mock import MagicMock
from PIL import Image

from src.core.utils.screenshot_manager import ScreenshotManager
from src.core.utils.screenshot_capture import CaptureMode, ScreenshotCapture
from src.core.utils.screenshot_storage import ScreenshotStorage
from src.core.utils.screenshot_cleaner import ScreenshotCleaner


class TestScreenshotManager(unittest.TestCase):
    """Test cases for the screenshot manager"""

    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for screenshots
        self.temp_dir = tempfile.TemporaryDirectory()
        self.screenshot_dir = self.temp_dir.name

        # Create mock components
        self.mock_capture = MagicMock(spec=ScreenshotCapture)
        self.mock_storage = MagicMock(spec=ScreenshotStorage)
        self.mock_cleaner = MagicMock(spec=ScreenshotCleaner)

        # Create the screenshot manager with mock components
        self.manager = ScreenshotManager(self.screenshot_dir)
        self.manager.capture = self.mock_capture
        self.manager.storage = self.mock_storage
        self.manager.cleaner = self.mock_cleaner

        # Mock driver for testing
        self.mock_driver = MagicMock()

        # Mock element for testing
        self.mock_element = MagicMock()
        self.mock_element.location = {'x': 10, 'y': 20}
        self.mock_element.size = {'width': 100, 'height': 50}

        # Mock PIL Image for testing
        self.mock_image = MagicMock(spec=Image.Image)
        self.mock_image.crop.return_value = self.mock_image

        # Set up mock capture to return mock image
        self.mock_capture.capture.return_value = self.mock_image

        # Set up mock storage to return a file path
        self.mock_storage.save_image.return_value = os.path.join(self.screenshot_dir, "test_screenshot.png")

    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()

    def test_capture_and_save_full_screen(self):
        """Test capturing and saving a full screen screenshot"""
        # Act
        result = self.manager.capture_and_save(
            self.mock_driver,
            "test_full_screen",
            mode=CaptureMode.FULL_SCREEN
        )

        # Assert
        self.mock_capture.capture.assert_called_once_with(
            self.mock_driver, CaptureMode.FULL_SCREEN, None, None
        )
        self.mock_storage.save_image.assert_called_once_with(
            self.mock_image, "test_full_screen", None
        )
        self.assertEqual(result, os.path.join(self.screenshot_dir, "test_screenshot.png"))

    def test_capture_and_save_element(self):
        """Test capturing and saving a screenshot of an element"""
        # Act
        result = self.manager.capture_and_save(
            self.mock_driver,
            "test_element",
            mode=CaptureMode.ELEMENT,
            element=self.mock_element
        )

        # Assert
        self.mock_capture.capture.assert_called_once_with(
            self.mock_driver, CaptureMode.ELEMENT, self.mock_element, None
        )
        self.mock_storage.save_image.assert_called_once_with(
            self.mock_image, "test_element", None
        )
        self.assertEqual(result, os.path.join(self.screenshot_dir, "test_screenshot.png"))

    def test_capture_and_save_region(self):
        """Test capturing and saving a screenshot of a region"""
        # Arrange
        region = (10, 20, 100, 50)

        # Act
        result = self.manager.capture_and_save(
            self.mock_driver,
            "test_region",
            mode=CaptureMode.REGION,
            region=region
        )

        # Assert
        self.mock_capture.capture.assert_called_once_with(
            self.mock_driver, CaptureMode.REGION, None, region
        )
        self.mock_storage.save_image.assert_called_once_with(
            self.mock_image, "test_region", None
        )
        self.assertEqual(result, os.path.join(self.screenshot_dir, "test_screenshot.png"))

    def test_capture_and_save_with_metadata(self):
        """Test capturing and saving a screenshot with metadata"""
        # Arrange
        metadata = {"key": "value"}

        # Act
        result = self.manager.capture_and_save(
            self.mock_driver,
            "test_metadata",
            mode=CaptureMode.FULL_SCREEN,
            metadata=metadata
        )

        # Assert
        self.mock_capture.capture.assert_called_once_with(
            self.mock_driver, CaptureMode.FULL_SCREEN, None, None
        )
        self.mock_storage.save_image.assert_called_once_with(
            self.mock_image, "test_metadata", metadata
        )
        self.assertEqual(result, os.path.join(self.screenshot_dir, "test_screenshot.png"))

    def test_get_screenshots(self):
        """Test getting all screenshots"""
        # Arrange
        expected_screenshots = ["screenshot1.png", "screenshot2.png"]
        self.mock_storage.get_screenshots.return_value = expected_screenshots

        # Act
        result = self.manager.get_screenshots()

        # Assert
        self.assertEqual(result, expected_screenshots)
        self.mock_storage.get_screenshots.assert_called_once()

    def test_get_latest_screenshot(self):
        """Test getting the latest screenshot"""
        # Arrange
        expected_screenshot = "latest_screenshot.png"
        self.mock_storage.get_latest_screenshot.return_value = expected_screenshot

        # Act
        result = self.manager.get_latest_screenshot()

        # Assert
        self.assertEqual(result, expected_screenshot)
        self.mock_storage.get_latest_screenshot.assert_called_once()

    def test_get_screenshot_path(self):
        """Test getting a screenshot path"""
        # Arrange
        filename = "test_file.png"
        expected_path = os.path.join(self.screenshot_dir, filename)
        self.mock_storage.get_screenshot_path.return_value = expected_path

        # Act
        result = self.manager.get_screenshot_path(filename)

        # Assert
        self.assertEqual(result, expected_path)
        self.mock_storage.get_screenshot_path.assert_called_once_with(filename)

    def test_get_metadata(self):
        """Test getting metadata for a screenshot"""
        # Arrange
        screenshot_path = "test_screenshot.png"
        expected_metadata = {"key": "value"}
        self.mock_storage.get_metadata.return_value = expected_metadata

        # Act
        result = self.manager.get_metadata(screenshot_path)

        # Assert
        self.assertEqual(result, expected_metadata)
        self.mock_storage.get_metadata.assert_called_once_with(screenshot_path)

    def test_cleanup(self):
        """Test cleaning up old screenshots"""
        # Arrange
        screenshots = [f"screenshot_{i}.png" for i in range(5)]
        max_screenshots = 3
        expected_removed = 2
        self.mock_storage.get_screenshots.return_value = screenshots
        self.mock_cleaner.cleanup.return_value = expected_removed

        # Act
        result = self.manager.cleanup(max_screenshots)

        # Assert
        self.assertEqual(result, expected_removed)
        self.mock_storage.get_screenshots.assert_called_once()
        self.mock_cleaner.cleanup.assert_called_once_with(screenshots, max_screenshots)


if __name__ == "__main__":
    unittest.main()
