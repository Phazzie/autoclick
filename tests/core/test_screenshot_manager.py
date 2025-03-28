"""Tests for the screenshot manager"""
# pylint: disable=redefined-outer-name
import os
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from src.core.screenshot_manager import ScreenshotManager


@pytest.fixture
def mock_driver():
    """Return a mock WebDriver"""
    driver = MagicMock()
    
    # Mock the get_screenshot_as_file method
    def mock_get_screenshot(filename):
        # Create an empty file to simulate taking a screenshot
        Path(filename).touch()
        return True
    
    driver.get_screenshot_as_file.side_effect = mock_get_screenshot
    
    # Mock the get_screenshot_as_png method
    driver.get_screenshot_as_png.return_value = b"mock_png_data"
    
    # Mock the get_screenshot_as_base64 method
    driver.get_screenshot_as_base64.return_value = "mock_base64_data"
    
    return driver


@pytest.fixture
def screenshot_dir(tmp_path):
    """Create a temporary directory for screenshots"""
    screenshots_dir = tmp_path / "screenshots"
    screenshots_dir.mkdir()
    return screenshots_dir


@pytest.fixture
def config(screenshot_dir):
    """Return a configuration for testing"""
    return {
        "screenshot_dir": str(screenshot_dir),
        "screenshot_format": "png",
        "screenshot_quality": 80,
        "screenshot_on_error": True,
    }


def test_screenshot_manager_initialization(config):
    """Test that ScreenshotManager initializes correctly"""
    manager = ScreenshotManager(config)
    
    assert manager.screenshot_dir == Path(config["screenshot_dir"])
    assert manager.screenshot_format == config["screenshot_format"]
    assert manager.screenshot_quality == config["screenshot_quality"]
    assert manager.screenshot_on_error == config["screenshot_on_error"]


def test_take_screenshot(mock_driver, config, screenshot_dir):
    """Test taking a screenshot"""
    manager = ScreenshotManager(config)
    
    # Take a screenshot
    screenshot_path = manager.take_screenshot(mock_driver, "test_screenshot")
    
    # Check that the screenshot file was created
    assert screenshot_path.exists()
    
    # Check that the screenshot is in the correct directory
    assert screenshot_path.parent == screenshot_dir
    
    # Check that the screenshot has the correct name format
    assert "test_screenshot" in screenshot_path.name
    assert screenshot_path.suffix == f".{config['screenshot_format']}"
    
    # Verify the driver's get_screenshot_as_file method was called
    mock_driver.get_screenshot_as_file.assert_called_once()


def test_take_screenshot_with_timestamp(mock_driver, config):
    """Test taking a screenshot with a timestamp"""
    manager = ScreenshotManager(config)
    
    # Take a screenshot with a timestamp
    screenshot_path = manager.take_screenshot(mock_driver, "test_with_timestamp", add_timestamp=True)
    
    # Check that the screenshot file was created
    assert screenshot_path.exists()
    
    # Check that the filename contains a timestamp
    # The timestamp format should be YYYYMMDD_HHMMSS
    date_format = datetime.now().strftime("%Y%m%d")
    assert date_format in screenshot_path.name


def test_take_screenshot_with_custom_directory(mock_driver, config, tmp_path):
    """Test taking a screenshot with a custom directory"""
    manager = ScreenshotManager(config)
    
    # Create a custom directory
    custom_dir = tmp_path / "custom_screenshots"
    custom_dir.mkdir()
    
    # Take a screenshot with a custom directory
    screenshot_path = manager.take_screenshot(
        mock_driver, "test_custom_dir", directory=custom_dir
    )
    
    # Check that the screenshot file was created in the custom directory
    assert screenshot_path.exists()
    assert screenshot_path.parent == custom_dir


def test_take_screenshot_on_error(mock_driver, config):
    """Test taking a screenshot on error"""
    manager = ScreenshotManager(config)
    
    # Mock an exception
    exception = Exception("Test error")
    
    # Take a screenshot on error
    screenshot_path = manager.take_screenshot_on_error(mock_driver, exception)
    
    # Check that the screenshot file was created
    assert screenshot_path.exists()
    
    # Check that the filename contains "error"
    assert "error" in screenshot_path.name.lower()
    
    # Check that the filename contains the exception type
    assert "exception" in screenshot_path.name.lower()


def test_get_screenshot_as_base64(mock_driver, config):
    """Test getting a screenshot as base64"""
    manager = ScreenshotManager(config)
    
    # Get a screenshot as base64
    base64_data = manager.get_screenshot_as_base64(mock_driver)
    
    # Check that the base64 data was returned
    assert base64_data == "mock_base64_data"
    
    # Verify the driver's get_screenshot_as_base64 method was called
    mock_driver.get_screenshot_as_base64.assert_called_once()


def test_get_screenshot_as_png(mock_driver, config):
    """Test getting a screenshot as PNG"""
    manager = ScreenshotManager(config)
    
    # Get a screenshot as PNG
    png_data = manager.get_screenshot_as_png(mock_driver)
    
    # Check that the PNG data was returned
    assert png_data == b"mock_png_data"
    
    # Verify the driver's get_screenshot_as_png method was called
    mock_driver.get_screenshot_as_png.assert_called_once()


def test_cleanup_old_screenshots(config, screenshot_dir):
    """Test cleaning up old screenshots"""
    manager = ScreenshotManager(config)
    
    # Create some old screenshot files
    for i in range(5):
        (screenshot_dir / f"old_screenshot_{i}.png").touch()
    
    # Clean up old screenshots
    manager.cleanup_old_screenshots(max_age_days=0)
    
    # Check that all screenshots were deleted
    assert len(list(screenshot_dir.glob("*.png"))) == 0
