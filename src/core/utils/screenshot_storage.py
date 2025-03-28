"""Screenshot storage functionality"""
import os
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from PIL import Image


class ScreenshotStorage:
    """
    Stores and manages screenshot files
    
    This class is responsible only for storing and retrieving screenshots,
    not for capturing them.
    """
    
    def __init__(self, screenshot_dir: str = "screenshots"):
        """
        Initialize the screenshot storage
        
        Args:
            screenshot_dir: Directory to store screenshots
        """
        self.screenshot_dir = screenshot_dir
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create the screenshot directory if it doesn't exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def save_image(self, image: Image.Image, name: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save an image to the screenshot directory
        
        Args:
            image: PIL Image to save
            name: Base name for the screenshot
            metadata: Optional metadata to associate with the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        # Generate a filename
        filename = self._generate_filename(name)
        file_path = os.path.join(self.screenshot_dir, filename)
        
        try:
            # Save the image
            image.save(file_path)
            self.logger.info(f"Screenshot saved to {file_path}")
            
            # Save metadata if provided
            if metadata:
                self._save_metadata(file_path, metadata)
            
            return file_path
        except Exception as e:
            self.logger.error(f"Error saving screenshot: {str(e)}")
            raise
    
    def get_screenshots(self) -> List[str]:
        """
        Get all screenshots in the screenshot directory
        
        Returns:
            List of screenshot file paths
        """
        # Get all PNG files in the screenshot directory
        screenshots = []
        for filename in os.listdir(self.screenshot_dir):
            if filename.lower().endswith(".png"):
                screenshots.append(os.path.join(self.screenshot_dir, filename))
        
        # Sort by modification time (newest first)
        screenshots.sort(key=os.path.getmtime, reverse=True)
        
        return screenshots
    
    def get_latest_screenshot(self) -> Optional[str]:
        """
        Get the latest screenshot
        
        Returns:
            Path to the latest screenshot, or None if no screenshots exist
        """
        screenshots = self.get_screenshots()
        return screenshots[0] if screenshots else None
    
    def get_screenshot_path(self, filename: str) -> str:
        """
        Get the full path to a screenshot
        
        Args:
            filename: Screenshot filename
            
        Returns:
            Full path to the screenshot
        """
        return os.path.join(self.screenshot_dir, filename)
    
    def get_metadata(self, screenshot_path: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a screenshot
        
        Args:
            screenshot_path: Path to the screenshot
            
        Returns:
            Metadata dictionary, or None if no metadata exists
        """
        # Create metadata file path
        metadata_path = screenshot_path + ".json"
        
        # Load metadata if it exists
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading metadata: {str(e)}")
        
        return None
    
    def _generate_filename(self, name: str) -> str:
        """
        Generate a filename for a screenshot
        
        Args:
            name: Base name for the screenshot
            
        Returns:
            Generated filename
        """
        # Clean the name (remove invalid characters)
        name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        
        return f"{name}_{timestamp}.png"
    
    def _save_metadata(self, screenshot_path: str, metadata: Dict[str, Any]) -> None:
        """
        Save metadata for a screenshot
        
        Args:
            screenshot_path: Path to the screenshot
            metadata: Metadata to save
        """
        # Create metadata file path
        metadata_path = screenshot_path + ".json"
        
        # Add timestamp to metadata
        metadata["timestamp"] = datetime.now().isoformat()
        
        # Save metadata
        try:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving metadata: {str(e)}")
