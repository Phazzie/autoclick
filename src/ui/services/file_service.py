"""File service implementation"""
import json
from typing import Any, Dict

from src.ui.interfaces.service_interface import FileServiceInterface


class FileService(FileServiceInterface):
    """Service for file operations"""
    
    def load_workflow(self, file_path: str) -> Dict[str, Any]:
        """
        Load workflow from file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Workflow data
            
        Raises:
            IOError: If the file cannot be loaded
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise IOError(f"Failed to load workflow: {str(e)}")
    
    def save_workflow(self, workflow: Dict[str, Any], file_path: str) -> bool:
        """
        Save workflow to file
        
        Args:
            workflow: Workflow data
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            IOError: If the file cannot be saved
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(workflow, f, indent=2)
            return True
        except Exception as e:
            raise IOError(f"Failed to save workflow: {str(e)}")
