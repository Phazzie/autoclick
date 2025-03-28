"""Screenshot utilities for capturing browser screenshots"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union

from PIL import Image
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def take_screenshot(
    driver: WebDriver,
    output_path: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    prefix: str = "screenshot",
    use_timestamp: bool = False,
    save_metadata: bool = False,
) -> Union[bool, Tuple[bool, Path]]:
    """
    Take a screenshot of the current browser window
    
    Args:
        driver: WebDriver instance
        output_path: Path to save the screenshot (if None, a path will be generated)
        output_dir: Directory to save the screenshot (used if output_path is None)
        prefix: Prefix for the filename (used if output_path is None)
        use_timestamp: Whether to include a timestamp in the filename
        save_metadata: Whether to save metadata about the screenshot
        
    Returns:
        If output_path is provided: True if successful, False otherwise
        If output_path is None: Tuple of (success, output_path)
    """
    logger = logging.getLogger(__name__)
    
    # Generate output path if not provided
    if output_path is None:
        if output_dir is None:
            output_dir = Path.cwd() / "screenshots"
        else:
            output_dir = Path(output_dir)
        
        # Create the output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp if requested
        if use_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prefix}_{timestamp}.png"
        else:
            filename = f"{prefix}.png"
        
        output_path = output_dir / filename
    else:
        output_path = Path(output_path)
        
        # Create the output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Take the screenshot
        logger.info(f"Taking screenshot: {output_path}")
        success = driver.get_screenshot_as_file(str(output_path))
        
        if not success:
            logger.error("Failed to take screenshot")
            return False
        
        # Save metadata if requested
        if save_metadata:
            metadata = {
                "url": driver.current_url,
                "timestamp": datetime.now().isoformat(),
                "browser": driver.name if hasattr(driver, "name") else "unknown",
                "title": driver.title,
                "window_size": driver.get_window_size(),
            }
            
            metadata_path = output_path.with_suffix(".json")
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Saved screenshot metadata: {metadata_path}")
        
        if output_path is None:
            return True, output_path
        return True
    except Exception as e:
        logger.error(f"Error taking screenshot: {str(e)}")
        if output_path is None:
            return False, output_path
        return False


def take_element_screenshot(
    driver: WebDriver,
    element: WebElement,
    output_path: Union[str, Path],
    save_metadata: bool = False,
) -> bool:
    """
    Take a screenshot of a specific element
    
    Args:
        driver: WebDriver instance
        element: WebElement to capture
        output_path: Path to save the screenshot
        save_metadata: Whether to save metadata about the screenshot
        
    Returns:
        True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    output_path = Path(output_path)
    
    # Create the output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Take a screenshot of the entire page
        temp_path = output_path.with_name(f"temp_{output_path.name}")
        success = driver.get_screenshot_as_file(str(temp_path))
        
        if not success:
            logger.error("Failed to take screenshot")
            return False
        
        try:
            # Get the element's location and size
            location = element.location
            size = element.size
            
            # Open the screenshot
            img = Image.open(temp_path)
            
            # Calculate the element's coordinates
            left = location["x"]
            top = location["y"]
            right = location["x"] + size["width"]
            bottom = location["y"] + size["height"]
            
            # Crop the image to the element
            img = img.crop((left, top, right, bottom))
            
            # Save the cropped image
            img.save(str(output_path))
            
            # Save metadata if requested
            if save_metadata:
                metadata = {
                    "url": driver.current_url,
                    "timestamp": datetime.now().isoformat(),
                    "browser": driver.name if hasattr(driver, "name") else "unknown",
                    "title": driver.title,
                    "element_location": location,
                    "element_size": size,
                }
                
                metadata_path = output_path.with_suffix(".json")
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f, indent=2)
                
                logger.info(f"Saved element screenshot metadata: {metadata_path}")
            
            logger.info(f"Saved element screenshot: {output_path}")
            return True
        finally:
            # Clean up the temporary file
            if temp_path.exists():
                temp_path.unlink()
    except Exception as e:
        logger.error(f"Error taking element screenshot: {str(e)}")
        return False
