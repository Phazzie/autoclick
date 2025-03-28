"""Interfaces for services"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class DialogServiceInterface(ABC):
    """Interface for dialog operations"""
    
    @abstractmethod
    def show_info(self, title: str, message: str) -> None:
        """
        Show information dialog
        
        Args:
            title: Dialog title
            message: Dialog message
        """
        pass
    
    @abstractmethod
    def show_error(self, title: str, message: str) -> None:
        """
        Show error dialog
        
        Args:
            title: Dialog title
            message: Dialog message
        """
        pass
    
    @abstractmethod
    def show_confirmation(self, title: str, message: str) -> bool:
        """
        Show confirmation dialog
        
        Args:
            title: Dialog title
            message: Dialog message
            
        Returns:
            True if confirmed, False otherwise
        """
        pass
    
    @abstractmethod
    def open_file(self, file_types: List[Tuple[str, str]]) -> Optional[str]:
        """
        Open file dialog
        
        Args:
            file_types: List of file type tuples (description, extension)
            
        Returns:
            Selected file path, or None if cancelled
        """
        pass
    
    @abstractmethod
    def save_file(self, file_types: List[Tuple[str, str]], default_extension: str) -> Optional[str]:
        """
        Save file dialog
        
        Args:
            file_types: List of file type tuples (description, extension)
            default_extension: Default file extension
            
        Returns:
            Selected file path, or None if cancelled
        """
        pass


class FileServiceInterface(ABC):
    """Interface for file operations"""
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass


class ThemeServiceInterface(ABC):
    """Interface for theme management"""
    
    @abstractmethod
    def set_theme(self, theme: str) -> None:
        """
        Set the application theme
        
        Args:
            theme: Theme name
        """
        pass
    
    @abstractmethod
    def get_theme(self) -> str:
        """
        Get the current theme
        
        Returns:
            Current theme name
        """
        pass
