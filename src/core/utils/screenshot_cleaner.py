"""Screenshot cleanup functionality"""
import os
import logging
from typing import List


class ScreenshotCleaner:
    """
    Cleans up old screenshots
    
    This class is responsible only for cleaning up screenshots,
    not for capturing or storing them.
    """
    
    def __init__(self):
        """Initialize the screenshot cleaner"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def cleanup(self, screenshots: List[str], max_screenshots: int = 100) -> int:
        """
        Clean up old screenshots
        
        Args:
            screenshots: List of screenshot paths
            max_screenshots: Maximum number of screenshots to keep
            
        Returns:
            Number of screenshots removed
        """
        # If we have more screenshots than the maximum, remove the oldest ones
        if len(screenshots) > max_screenshots:
            # Get the screenshots to remove (oldest first)
            to_remove = screenshots[max_screenshots:]
            
            # Remove the screenshots
            for screenshot in to_remove:
                try:
                    os.remove(screenshot)
                    # Also remove metadata file if it exists
                    metadata_file = screenshot + ".json"
                    if os.path.exists(metadata_file):
                        os.remove(metadata_file)
                except Exception as e:
                    self.logger.error(f"Error removing screenshot {screenshot}: {str(e)}")
            
            self.logger.info(f"Removed {len(to_remove)} old screenshots")
            return len(to_remove)
        
        return 0
