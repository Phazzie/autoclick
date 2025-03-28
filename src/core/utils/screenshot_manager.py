"""Screenshot management functionality"""
import logging
from typing import List, Optional, Tuple, Dict, Any

from src.core.utils.screenshot_capture import ScreenshotCapture, CaptureMode
from src.core.utils.screenshot_storage import ScreenshotStorage
from src.core.utils.screenshot_cleaner import ScreenshotCleaner


class ScreenshotManager:
    """
    Manager for capturing, storing, and cleaning up screenshots

    This class uses composition to delegate to specialized classes
    for each responsibility.
    """

    def __init__(self, screenshot_dir: str = "screenshots"):
        """
        Initialize the screenshot manager

        Args:
            screenshot_dir: Directory to store screenshots
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        # Create specialized components
        self.capture = ScreenshotCapture()
        self.storage = ScreenshotStorage(screenshot_dir)
        self.cleaner = ScreenshotCleaner()

    def capture(self, *args, **kwargs) -> str:
        """
        Capture and save a screenshot (legacy method for backward compatibility)

        This method is kept for backward compatibility.
        New code should use capture_and_save instead.
        """
        return self.capture_and_save(*args, **kwargs)

    def capture_and_save(
        self,
        driver: Any,
        name: str,
        mode: CaptureMode = CaptureMode.FULL_SCREEN,
        element: Optional[Any] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Capture and save a screenshot

        Args:
            driver: Selenium WebDriver instance
            name: Base name for the screenshot
            mode: Capture mode (full screen, element, region)
            element: WebElement to capture (required for ELEMENT mode)
            region: Region to capture as (x, y, width, height) (required for REGION mode)
            metadata: Optional metadata to associate with the screenshot

        Returns:
            Path to the saved screenshot
        """
        # Capture the screenshot
        image = self.capture.capture(driver, mode, element, region)

        # Save the image
        return self.storage.save_image(image, name, metadata)

    def get_screenshots(self) -> List[str]:
        """
        Get all screenshots

        Returns:
            List of screenshot file paths
        """
        return self.storage.get_screenshots()

    def get_latest_screenshot(self) -> Optional[str]:
        """
        Get the latest screenshot

        Returns:
            Path to the latest screenshot, or None if no screenshots exist
        """
        return self.storage.get_latest_screenshot()

    def get_screenshot_path(self, filename: str) -> str:
        """
        Get the full path to a screenshot

        Args:
            filename: Screenshot filename

        Returns:
            Full path to the screenshot
        """
        return self.storage.get_screenshot_path(filename)

    def get_metadata(self, screenshot_path: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a screenshot

        Args:
            screenshot_path: Path to the screenshot

        Returns:
            Metadata dictionary, or None if no metadata exists
        """
        return self.storage.get_metadata(screenshot_path)

    def cleanup(self, max_screenshots: int = 100) -> int:
        """
        Clean up old screenshots

        Args:
            max_screenshots: Maximum number of screenshots to keep

        Returns:
            Number of screenshots removed
        """
        screenshots = self.get_screenshots()
        return self.cleaner.cleanup(screenshots, max_screenshots)
