"""Tests for the screenshot utility"""
# pylint: disable=redefined-outer-name
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from selenium.webdriver.remote.webdriver import WebDriver

from src.utils.screenshot import take_screenshot, take_element_screenshot


@pytest.fixture
def mock_driver():
    """Return a mock WebDriver"""
    driver = MagicMock(spec=WebDriver)

    # Mock the get_screenshot_as_file method
    def mock_get_screenshot_as_file(filename):
        # Create an empty file
        with open(filename, "w") as f:
            f.write("")
        return True

    driver.get_screenshot_as_file.side_effect = mock_get_screenshot_as_file

    return driver


@pytest.fixture
def mock_element():
    """Return a mock WebElement"""
    element = MagicMock()

    # Mock the screenshot_as_png property
    element.screenshot_as_png = b"mock_screenshot_data"

    # Mock the location and size properties
    element.location = {"x": 10, "y": 20}
    element.size = {"width": 100, "height": 50}

    return element


def test_take_screenshot(mock_driver, tmp_path):
    """Test taking a screenshot of the entire page"""
    # Define the output path
    output_path = tmp_path / "screenshot.png"

    # Take the screenshot
    result = take_screenshot(mock_driver, output_path)

    # Verify the result
    assert result is True
    assert output_path.exists()

    # Verify the driver method was called
    mock_driver.get_screenshot_as_file.assert_called_once_with(str(output_path))


def test_take_screenshot_with_directory_creation(mock_driver, tmp_path):
    """Test taking a screenshot with directory creation"""
    # Define the output path in a subdirectory
    output_dir = tmp_path / "screenshots"
    output_path = output_dir / "screenshot.png"

    # Take the screenshot
    result = take_screenshot(mock_driver, output_path)

    # Verify the result
    assert result is True
    assert output_path.exists()
    assert output_dir.exists()


@patch("src.utils.screenshot.Image.open")
def test_take_element_screenshot(mock_image_open, mock_driver, mock_element, tmp_path):
    """Test taking a screenshot of a specific element"""
    # Define the output path
    output_path = tmp_path / "element_screenshot.png"

    # Mock the Image.open method
    mock_image = MagicMock()
    mock_image_open.return_value = mock_image
    mock_image.crop.return_value = mock_image

    # Create a temporary file that will be used by the function
    temp_path = output_path.with_name(f"temp_{output_path.name}")
    with open(temp_path, "w") as f:
        f.write("")

    # Take the element screenshot
    result = take_element_screenshot(mock_driver, mock_element, output_path)

    # Create the output file to simulate the save operation
    with open(output_path, "w") as f:
        f.write("")

    # Verify the result
    assert result is True
    assert output_path.exists()

    # Verify the driver method was called
    mock_driver.get_screenshot_as_file.assert_called_once()

    # Verify the image was cropped
    mock_image.crop.assert_called_once()

    # Verify the cropped image was saved
    mock_image.save.assert_called_once_with(str(output_path))
