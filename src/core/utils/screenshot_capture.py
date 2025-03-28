"""Screenshot capture functionality"""
import logging
from enum import Enum, auto
from typing import Optional, Tuple, Any

try:
    from PIL import Image
    from io import BytesIO
except ImportError:
    # Provide a helpful error message if PIL is not installed
    raise ImportError(
        "The PIL package is required for screenshot functionality. "
        "Please install it using: pip install Pillow"
    )


class CaptureMode(Enum):
    """Modes for capturing screenshots"""
    FULL_SCREEN = auto()
    ELEMENT = auto()
    REGION = auto()


class ScreenshotCapture:
    """
    Captures screenshots in different modes
    
    This class is responsible only for capturing screenshots,
    not for storing or managing them.
    """
    
    def __init__(self):
        """Initialize the screenshot capture"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def capture_full_screen(self, driver: Any) -> Image.Image:
        """
        Capture a full screen screenshot
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            PIL Image object
            
        Raises:
            ValueError: If driver is None
        """
        if driver is None:
            raise ValueError("Driver cannot be None")
            
        try:
            # Take the screenshot
            png_data = driver.get_screenshot_as_png()
            
            # Open the image with PIL
            return Image.open(BytesIO(png_data))
        except Exception as e:
            self.logger.error(f"Error capturing full screen: {str(e)}")
            raise
    
    def capture_element(self, driver: Any, element: Any) -> Image.Image:
        """
        Capture a screenshot of an element
        
        Args:
            driver: Selenium WebDriver instance
            element: WebElement to capture
            
        Returns:
            PIL Image object
            
        Raises:
            ValueError: If driver or element is None
        """
        if driver is None:
            raise ValueError("Driver cannot be None")
            
        if element is None:
            raise ValueError("Element cannot be None")
            
        try:
            # Capture full screen first
            img = self.capture_full_screen(driver)
            
            # Get element location and size
            location = element.location
            size = element.size
            
            # Calculate coordinates
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            
            # Crop the image
            return img.crop((left, top, right, bottom))
        except Exception as e:
            self.logger.error(f"Error capturing element: {str(e)}")
            raise
    
    def capture_region(self, driver: Any, region: Tuple[int, int, int, int]) -> Image.Image:
        """
        Capture a screenshot of a region
        
        Args:
            driver: Selenium WebDriver instance
            region: Region to capture as (x, y, width, height)
            
        Returns:
            PIL Image object
            
        Raises:
            ValueError: If driver or region is None
        """
        if driver is None:
            raise ValueError("Driver cannot be None")
            
        if region is None:
            raise ValueError("Region cannot be None")
            
        try:
            # Capture full screen first
            img = self.capture_full_screen(driver)
            
            # Crop the image to the specified region
            return img.crop(region)
        except Exception as e:
            self.logger.error(f"Error capturing region: {str(e)}")
            raise
    
    def capture(
        self,
        driver: Any,
        mode: CaptureMode = CaptureMode.FULL_SCREEN,
        element: Optional[Any] = None,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> Image.Image:
        """
        Capture a screenshot in the specified mode
        
        Args:
            driver: Selenium WebDriver instance
            mode: Capture mode (full screen, element, region)
            element: WebElement to capture (required for ELEMENT mode)
            region: Region to capture as (x, y, width, height) (required for REGION mode)
            
        Returns:
            PIL Image object
            
        Raises:
            ValueError: If required parameters are missing for the selected mode
        """
        if mode == CaptureMode.FULL_SCREEN:
            return self.capture_full_screen(driver)
        elif mode == CaptureMode.ELEMENT:
            return self.capture_element(driver, element)
        elif mode == CaptureMode.REGION:
            return self.capture_region(driver, region)
        else:
            raise ValueError(f"Unsupported capture mode: {mode}")
