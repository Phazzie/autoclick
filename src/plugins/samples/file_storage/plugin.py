"""File storage plugin implementation"""
import json
import logging
import os
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.plugins.interfaces import StoragePluginInterface


class FileStoragePlugin(StoragePluginInterface):
    """Stores data in files"""
    
    def __init__(self) -> None:
        """Initialize the file storage plugin"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        self.storage_dir: Optional[Path] = None
        self.format: str = "json"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration
        
        Args:
            config: Configuration dictionary
        """
        self.logger.info("Initializing file storage plugin")
        self.config = config
        self.storage_dir = Path(config.get("storage_dir", "storage"))
        self.format = config.get("format", "json")
        
        # Ensure the storage directory exists
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the plugin
        
        Returns:
            Dictionary containing plugin information
        """
        return {
            "name": "file_storage",
            "version": "1.0.0",
            "description": "Stores data in files",
            "author": "AUTOCLICK Team",
            "supported_formats": ["json", "pickle"],
        }
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.logger.info("Cleaning up file storage plugin")
    
    def save(self, key: str, data: Any) -> None:
        """
        Save data with the given key
        
        Args:
            key: Key to store the data under
            data: Data to store
        """
        if not self.storage_dir:
            self.logger.error("Storage directory not set")
            return
        
        self.logger.info(f"Saving data for key: {key}")
        
        # Get the file path
        file_path = self._get_file_path(key)
        
        try:
            # Save the data
            if self.format == "json":
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
            elif self.format == "pickle":
                with open(file_path, "wb") as f:
                    pickle.dump(data, f)
            else:
                self.logger.error(f"Unsupported format: {self.format}")
        except Exception as e:
            self.logger.error(f"Error saving data for key {key}: {str(e)}")
    
    def load(self, key: str) -> Any:
        """
        Load data for the given key
        
        Args:
            key: Key to load data for
            
        Returns:
            Stored data, or None if not found
        """
        if not self.storage_dir:
            self.logger.error("Storage directory not set")
            return None
        
        self.logger.info(f"Loading data for key: {key}")
        
        # Get the file path
        file_path = self._get_file_path(key)
        
        # Check if the file exists
        if not file_path.exists():
            self.logger.warning(f"No data found for key: {key}")
            return None
        
        try:
            # Load the data
            if self.format == "json":
                with open(file_path, "r") as f:
                    return json.load(f)
            elif self.format == "pickle":
                with open(file_path, "rb") as f:
                    return pickle.load(f)
            else:
                self.logger.error(f"Unsupported format: {self.format}")
                return None
        except Exception as e:
            self.logger.error(f"Error loading data for key {key}: {str(e)}")
            return None
    
    def delete(self, key: str) -> None:
        """
        Delete data for the given key
        
        Args:
            key: Key to delete data for
        """
        if not self.storage_dir:
            self.logger.error("Storage directory not set")
            return
        
        self.logger.info(f"Deleting data for key: {key}")
        
        # Get the file path
        file_path = self._get_file_path(key)
        
        # Check if the file exists
        if not file_path.exists():
            self.logger.warning(f"No data found for key: {key}")
            return
        
        try:
            # Delete the file
            file_path.unlink()
        except Exception as e:
            self.logger.error(f"Error deleting data for key {key}: {str(e)}")
    
    def list(self) -> List[str]:
        """
        List all available keys
        
        Returns:
            List of keys
        """
        if not self.storage_dir:
            self.logger.error("Storage directory not set")
            return []
        
        self.logger.info("Listing all keys")
        
        try:
            # Get all files in the storage directory
            extension = ".json" if self.format == "json" else ".pickle"
            files = list(self.storage_dir.glob(f"*{extension}"))
            
            # Extract the keys from the file names
            keys = [file.stem for file in files]
            
            return keys
        except Exception as e:
            self.logger.error(f"Error listing keys: {str(e)}")
            return []
    
    def _get_file_path(self, key: str) -> Path:
        """
        Get the file path for a key
        
        Args:
            key: Key to get the file path for
            
        Returns:
            Path to the file
        """
        if not self.storage_dir:
            raise ValueError("Storage directory not set")
        
        # Sanitize the key
        safe_key = key.replace("/", "_").replace("\\", "_")
        
        # Get the file extension
        extension = ".json" if self.format == "json" else ".pickle"
        
        # Return the file path
        return self.storage_dir / f"{safe_key}{extension}"
