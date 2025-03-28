"""Interfaces for plugins"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class PluginInterface(ABC):
    """Base interface for all plugins"""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration
        
        Args:
            config: Configuration dictionary
        """
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the plugin
        
        Returns:
            Dictionary containing plugin information
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources"""
        pass


class AutomationPluginInterface(PluginInterface):
    """Interface for automation plugins"""
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the automation
        
        Args:
            context: Execution context
            
        Returns:
            Dictionary containing the results
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of the plugin
        
        Returns:
            List of capability strings
        """
        pass


class ReporterPluginInterface(PluginInterface):
    """Interface for reporter plugins"""
    
    @abstractmethod
    def generate_report(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Generate a report from data
        
        Args:
            data: Data to include in the report
            output_path: Path to save the report
            
        Returns:
            Path to the generated report
        """
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        Get the supported report formats
        
        Returns:
            List of format strings
        """
        pass


class StoragePluginInterface(PluginInterface):
    """Interface for storage plugins"""
    
    @abstractmethod
    def save(self, key: str, data: Any) -> None:
        """
        Save data with the given key
        
        Args:
            key: Key to store the data under
            data: Data to store
        """
        pass
    
    @abstractmethod
    def load(self, key: str) -> Any:
        """
        Load data for the given key
        
        Args:
            key: Key to load data for
            
        Returns:
            Stored data, or None if not found
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete data for the given key
        
        Args:
            key: Key to delete data for
        """
        pass
    
    @abstractmethod
    def list(self) -> List[str]:
        """
        List all available keys
        
        Returns:
            List of keys
        """
        pass
