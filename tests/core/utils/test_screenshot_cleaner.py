"""Tests for the screenshot cleaner functionality"""
import os
import unittest
import tempfile
from unittest.mock import MagicMock, patch

from src.core.utils.screenshot_cleaner import ScreenshotCleaner


class TestScreenshotCleaner(unittest.TestCase):
    """Test cases for the screenshot cleaner"""

    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for screenshots
        self.temp_dir = tempfile.TemporaryDirectory()
        self.screenshot_dir = self.temp_dir.name
        
        # Create the screenshot cleaner
        self.cleaner = ScreenshotCleaner()
        
        # Create test screenshots
        self.screenshots = []
        for i in range(5):
            path = os.path.join(self.screenshot_dir, f"test_{i}.png")
            with open(path, 'wb') as f:
                f.write(b'test')
            self.screenshots.append(path)

    def tearDown(self):
        """Clean up after tests"""
        self.temp_dir.cleanup()

    def test_cleanup_no_excess(self):
        """Test cleaning up when there are no excess screenshots"""
        # Act
        removed = self.cleaner.cleanup(self.screenshots, max_screenshots=10)
        
        # Assert
        self.assertEqual(removed, 0)
        for screenshot in self.screenshots:
            self.assertTrue(os.path.exists(screenshot))

    def test_cleanup_with_excess(self):
        """Test cleaning up when there are excess screenshots"""
        # Act
        removed = self.cleaner.cleanup(self.screenshots, max_screenshots=3)
        
        # Assert
        self.assertEqual(removed, 2)
        
        # The first 3 screenshots should still exist
        for i in range(3):
            self.assertTrue(os.path.exists(self.screenshots[i]))
        
        # The last 2 screenshots should be removed
        for i in range(3, 5):
            self.assertFalse(os.path.exists(self.screenshots[i]))

    def test_cleanup_with_metadata(self):
        """Test cleaning up when there are metadata files"""
        # Arrange - Create metadata files
        for screenshot in self.screenshots:
            metadata_path = screenshot + ".json"
            with open(metadata_path, 'w') as f:
                f.write('{"test": "metadata"}')
        
        # Act
        removed = self.cleaner.cleanup(self.screenshots, max_screenshots=3)
        
        # Assert
        self.assertEqual(removed, 2)
        
        # The first 3 screenshots and their metadata should still exist
        for i in range(3):
            self.assertTrue(os.path.exists(self.screenshots[i]))
            self.assertTrue(os.path.exists(self.screenshots[i] + ".json"))
        
        # The last 2 screenshots and their metadata should be removed
        for i in range(3, 5):
            self.assertFalse(os.path.exists(self.screenshots[i]))
            self.assertFalse(os.path.exists(self.screenshots[i] + ".json"))

    @patch('src.core.utils.screenshot_cleaner.os.remove')
    @patch('src.core.utils.screenshot_cleaner.os.path.exists')
    def test_cleanup_with_error(self, mock_exists, mock_remove):
        """Test cleaning up when there's an error removing a file"""
        # Arrange
        mock_exists.return_value = True
        mock_remove.side_effect = [None, OSError("Test error"), None, None]
        
        # Act
        removed = self.cleaner.cleanup(self.screenshots, max_screenshots=3)
        
        # Assert
        self.assertEqual(removed, 2)  # Should still count the file that failed to remove
        self.assertEqual(mock_remove.call_count, 4)  # 2 screenshots + 2 metadata files


if __name__ == "__main__":
    unittest.main()
