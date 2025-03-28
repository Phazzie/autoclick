"""Tests for the screenshot capture functionality"""
import unittest
from unittest.mock import MagicMock, patch

from src.core.utils.screenshot_capture import ScreenshotCapture, CaptureMode


class TestScreenshotCapture(unittest.TestCase):
    """Test cases for the screenshot capture"""

    def setUp(self):
        """Set up test environment"""
        # Create the screenshot capture
        self.capture = ScreenshotCapture()
        
        # Mock driver for testing
        self.mock_driver = MagicMock()
        
        # Mock element for testing
        self.mock_element = MagicMock()
        self.mock_element.location = {'x': 10, 'y': 20}
        self.mock_element.size = {'width': 100, 'height': 50}
        
        # Mock PIL Image for testing
        self.mock_image = MagicMock()
        self.mock_image.crop.return_value = self.mock_image

    @patch('src.core.utils.screenshot_capture.Image')
    def test_capture_full_screen(self, mock_image_module):
        """Test capturing a full screen screenshot"""
        # Arrange
        self.mock_driver.get_screenshot_as_png.return_value = b'fake_png_data'
        mock_image_module.open.return_value = self.mock_image
        
        # Act
        result = self.capture.capture_full_screen(self.mock_driver)
        
        # Assert
        self.assertEqual(result, self.mock_image)
        self.mock_driver.get_screenshot_as_png.assert_called_once()
        mock_image_module.open.assert_called_once()

    @patch('src.core.utils.screenshot_capture.Image')
    def test_capture_element(self, mock_image_module):
        """Test capturing a screenshot of an element"""
        # Arrange
        self.mock_driver.get_screenshot_as_png.return_value = b'fake_png_data'
        mock_image_module.open.return_value = self.mock_image
        
        # Act
        result = self.capture.capture_element(self.mock_driver, self.mock_element)
        
        # Assert
        self.assertEqual(result, self.mock_image)
        self.mock_driver.get_screenshot_as_png.assert_called_once()
        mock_image_module.open.assert_called_once()
        self.mock_image.crop.assert_called_once()

    @patch('src.core.utils.screenshot_capture.Image')
    def test_capture_region(self, mock_image_module):
        """Test capturing a screenshot of a region"""
        # Arrange
        self.mock_driver.get_screenshot_as_png.return_value = b'fake_png_data'
        mock_image_module.open.return_value = self.mock_image
        
        # Act
        result = self.capture.capture_region(self.mock_driver, (10, 20, 100, 50))
        
        # Assert
        self.assertEqual(result, self.mock_image)
        self.mock_driver.get_screenshot_as_png.assert_called_once()
        mock_image_module.open.assert_called_once()
        self.mock_image.crop.assert_called_once()

    def test_capture_missing_driver(self):
        """Test capturing with missing driver"""
        # Act & Assert
        with self.assertRaises(ValueError):
            self.capture.capture_full_screen(None)

    def test_capture_missing_element(self):
        """Test capturing with missing element"""
        # Act & Assert
        with self.assertRaises(ValueError):
            self.capture.capture_element(self.mock_driver, None)

    def test_capture_missing_region(self):
        """Test capturing with missing region"""
        # Act & Assert
        with self.assertRaises(ValueError):
            self.capture.capture_region(self.mock_driver, None)

    @patch('src.core.utils.screenshot_capture.Image')
    def test_capture_with_mode(self, mock_image_module):
        """Test capturing with different modes"""
        # Arrange
        self.mock_driver.get_screenshot_as_png.return_value = b'fake_png_data'
        mock_image_module.open.return_value = self.mock_image
        
        # Act - Full screen
        result1 = self.capture.capture(self.mock_driver, CaptureMode.FULL_SCREEN)
        
        # Act - Element
        result2 = self.capture.capture(
            self.mock_driver, 
            CaptureMode.ELEMENT, 
            self.mock_element
        )
        
        # Act - Region
        result3 = self.capture.capture(
            self.mock_driver, 
            CaptureMode.REGION, 
            region=(10, 20, 100, 50)
        )
        
        # Assert
        self.assertEqual(result1, self.mock_image)
        self.assertEqual(result2, self.mock_image)
        self.assertEqual(result3, self.mock_image)
        self.assertEqual(self.mock_driver.get_screenshot_as_png.call_count, 3)
        self.assertEqual(mock_image_module.open.call_count, 3)
        self.assertEqual(self.mock_image.crop.call_count, 2)


if __name__ == "__main__":
    unittest.main()
