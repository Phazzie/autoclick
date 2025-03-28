"""Tests for the screenshot storage functionality"""
import os
import json
import unittest
import tempfile
from unittest.mock import MagicMock, patch
from datetime import datetime

from PIL import Image

from src.core.utils.screenshot_storage import ScreenshotStorage


class TestScreenshotStorage(unittest.TestCase):
    """Test cases for the screenshot storage"""

    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for screenshots
        self.temp_dir = tempfile.TemporaryDirectory()
        self.screenshot_dir = self.temp_dir.name

        # Create the screenshot storage
        self.storage = ScreenshotStorage(self.screenshot_dir)

        # Create a mock image
        self.mock_image = MagicMock(spec=Image.Image)
        self.mock_image.save.return_value = None

    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()

    @patch('os.path.exists')
    def test_save_image(self, mock_exists):
        """Test saving an image"""
        # Arrange
        mock_exists.return_value = True

        # Act
        result = self.storage.save_image(self.mock_image, "test_image")

        # Assert
        self.assertTrue(result.startswith(self.screenshot_dir))
        self.assertTrue(result.endswith(".png"))
        self.mock_image.save.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('json.dump')
    def test_save_image_with_metadata(self, mock_json_dump, mock_open, mock_exists):
        """Test saving an image with metadata"""
        # Arrange
        metadata = {"key": "value"}
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Act
        result = self.storage.save_image(self.mock_image, "test_image", metadata)

        # Assert
        self.assertTrue(result.startswith(self.screenshot_dir))
        self.assertTrue(result.endswith(".png"))
        self.mock_image.save.assert_called_once()
        mock_json_dump.assert_called_once()
        self.assertIn("key", mock_json_dump.call_args[0][0])
        self.assertEqual(mock_json_dump.call_args[0][0]["key"], "value")
        self.assertIn("timestamp", mock_json_dump.call_args[0][0])

    def test_get_screenshots(self):
        """Test getting all screenshots"""
        # Arrange - Create some test screenshots
        for i in range(3):
            with open(os.path.join(self.screenshot_dir, f"test_{i}.png"), 'wb') as f:
                f.write(b'test')

        # Act
        screenshots = self.storage.get_screenshots()

        # Assert
        self.assertEqual(len(screenshots), 3)
        for i in range(3):
            self.assertIn(os.path.join(self.screenshot_dir, f"test_{i}.png"), screenshots)

    def test_get_latest_screenshot(self):
        """Test getting the latest screenshot"""
        # Arrange - Create some test screenshots
        for i in range(3):
            with open(os.path.join(self.screenshot_dir, f"test_{i}.png"), 'wb') as f:
                f.write(b'test')
            # Ensure different timestamps
            import time
            time.sleep(0.01)

        # Act
        latest = self.storage.get_latest_screenshot()

        # Assert
        self.assertEqual(latest, os.path.join(self.screenshot_dir, "test_2.png"))

    def test_get_screenshot_path(self):
        """Test getting a screenshot path"""
        # Act
        path = self.storage.get_screenshot_path("test_file.png")

        # Assert
        self.assertEqual(path, os.path.join(self.screenshot_dir, "test_file.png"))

    def test_get_metadata(self):
        """Test getting metadata for a screenshot"""
        # Arrange
        screenshot_path = os.path.join(self.screenshot_dir, "test_metadata.png")
        metadata_path = screenshot_path + ".json"
        metadata = {"key": "value", "timestamp": datetime.now().isoformat()}

        # Create the screenshot file
        with open(screenshot_path, 'wb') as f:
            f.write(b'test')

        # Create the metadata file
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)

        # Act
        result = self.storage.get_metadata(screenshot_path)

        # Assert
        self.assertEqual(result["key"], "value")
        self.assertEqual(result["timestamp"], metadata["timestamp"])

    def test_get_metadata_missing(self):
        """Test getting metadata for a screenshot with no metadata"""
        # Arrange
        screenshot_path = os.path.join(self.screenshot_dir, "test_no_metadata.png")

        # Create the screenshot file
        with open(screenshot_path, 'wb') as f:
            f.write(b'test')

        # Act
        result = self.storage.get_metadata(screenshot_path)

        # Assert
        self.assertIsNone(result)

    def test_generate_filename(self):
        """Test generating a filename"""
        # Act
        filename = self.storage._generate_filename("test_name")

        # Assert
        self.assertTrue(filename.startswith("test_name_"))
        self.assertTrue(filename.endswith(".png"))
        self.assertIn(datetime.now().strftime("%Y%m%d"), filename)

    def test_generate_filename_with_invalid_chars(self):
        """Test generating a filename with invalid characters"""
        # Act
        filename = self.storage._generate_filename("test/name?with*invalid:chars")

        # Assert
        self.assertTrue(filename.startswith("test_name_with_invalid_chars"))
        self.assertTrue(filename.endswith(".png"))


if __name__ == "__main__":
    unittest.main()
