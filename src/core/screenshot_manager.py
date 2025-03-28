"""Screenshot management for browser automation"""
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union

from src.utils.debug_utils import debug_trace, exception_handler
from src.utils.selenium_utils import require_selenium


class ScreenshotManager:
    """Manages screenshots for browser automation"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the screenshot manager
        
        Args:
            config: Configuration dictionary with screenshot settings
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Get screenshot settings from config
        self.screenshot_dir = Path(config.get("screenshot_dir", "screenshots"))
        self.screenshot_format = config.get("screenshot_format", "png")
        self.screenshot_quality = config.get("screenshot_quality", 80)
        self.screenshot_on_error = config.get("screenshot_on_error", True)
        
        # Ensure the screenshot directory exists
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    @debug_trace
    def take_screenshot(
        self,
        driver: Any,
        name: str,
        add_timestamp: bool = False,
        directory: Optional[Union[str, Path]] = None,
    ) -> Path:
        """
        Take a screenshot of the current browser window
        
        Args:
            driver: WebDriver instance
            name: Base name for the screenshot
            add_timestamp: Whether to add a timestamp to the filename
            directory: Custom directory to save the screenshot in
            
        Returns:
            Path to the saved screenshot
        """
        # Ensure Selenium is available
        require_selenium()
        
        # Sanitize the name (remove invalid characters)
        name = "".join(c if c.isalnum() or c in "._- " else "_" for c in name)
        
        # Add timestamp if requested
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.{self.screenshot_format}"
        else:
            filename = f"{name}.{self.screenshot_format}"
        
        # Determine the directory to save in
        if directory:
            save_dir = Path(directory)
        else:
            save_dir = self.screenshot_dir
        
        # Ensure the directory exists
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Create the full path
        screenshot_path = save_dir / filename
        
        # Take the screenshot
        self.logger.info(f"Taking screenshot: {screenshot_path}")
        driver.get_screenshot_as_file(str(screenshot_path))
        
        return screenshot_path
    
    @debug_trace
    def take_screenshot_on_error(self, driver: Any, exception: Exception) -> Path:
        """
        Take a screenshot when an error occurs
        
        Args:
            driver: WebDriver instance
            exception: The exception that occurred
            
        Returns:
            Path to the saved screenshot
        """
        # Create a name based on the exception
        exception_type = type(exception).__name__
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"error_{exception_type}_{timestamp}"
        
        # Take the screenshot
        return self.take_screenshot(driver, name)
    
    @debug_trace
    def get_screenshot_as_base64(self, driver: Any) -> str:
        """
        Get a screenshot as a base64-encoded string
        
        Args:
            driver: WebDriver instance
            
        Returns:
            Base64-encoded screenshot
        """
        # Ensure Selenium is available
        require_selenium()
        
        self.logger.info("Getting screenshot as base64")
        return driver.get_screenshot_as_base64()
    
    @debug_trace
    def get_screenshot_as_png(self, driver: Any) -> bytes:
        """
        Get a screenshot as PNG binary data
        
        Args:
            driver: WebDriver instance
            
        Returns:
            PNG binary data
        """
        # Ensure Selenium is available
        require_selenium()
        
        self.logger.info("Getting screenshot as PNG")
        return driver.get_screenshot_as_png()
    
    @debug_trace
    @exception_handler
    def cleanup_old_screenshots(self, max_age_days: int = 7) -> int:
        """
        Delete screenshots older than the specified age
        
        Args:
            max_age_days: Maximum age in days
            
        Returns:
            Number of screenshots deleted
        """
        self.logger.info(f"Cleaning up screenshots older than {max_age_days} days")
        
        # Calculate the cutoff date
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        # Find and delete old screenshots
        count = 0
        for screenshot_file in self.screenshot_dir.glob(f"*.{self.screenshot_format}"):
            # Get the file's modification time
            mod_time = datetime.fromtimestamp(screenshot_file.stat().st_mtime)
            
            # Delete if older than the cutoff
            if mod_time < cutoff_date:
                self.logger.debug(f"Deleting old screenshot: {screenshot_file}")
                screenshot_file.unlink()
                count += 1
        
        self.logger.info(f"Deleted {count} old screenshots")
        return count
