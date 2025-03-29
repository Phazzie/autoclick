"""Registry for managing plugins"""
import logging
from typing import Any, Dict, List, Optional

from src.plugins.interfaces import PluginInterface


class PluginRegistry:
    """Registry for managing plugins"""
    
    def __init__(self) -> None:
        """Initialize the plugin registry"""
        self.logger = logging.getLogger(__name__)
        self.plugins: Dict[str, PluginInterface] = {}
    
    def register_plugin(self, name: str, plugin: PluginInterface) -> None:
        """
        Register a plugin
        
        Args:
            name: Name of the plugin
            plugin: Plugin instance
        """
        self.logger.info(f"Registering plugin: {name}")
        self.plugins[name] = plugin
    
    def unregister_plugin(self, name: str) -> None:
        """
        Unregister a plugin
        
        Args:
            name: Name of the plugin
        """
        if name in self.plugins:
            self.logger.info(f"Unregistering plugin: {name}")
            del self.plugins[name]
    
    def get_plugin(self, name: str) -> Optional[PluginInterface]:
        """
        Get a plugin by name
        
        Args:
            name: Name of the plugin
            
        Returns:
            Plugin instance, or None if not found
        """
        return self.plugins.get(name)
    
    def get_plugins(self) -> Dict[str, PluginInterface]:
        """
        Get all registered plugins
        
        Returns:
            Dictionary of plugin names to plugin instances
        """
        return self.plugins.copy()
    
    def initialize_plugins(self, config: Dict[str, Any]) -> None:
        """
        Initialize all registered plugins
        
        Args:
            config: Configuration dictionary
        """
        self.logger.info("Initializing plugins")
        for name, plugin in self.plugins.items():
            try:
                plugin_config = config.get(name, {})
                plugin.initialize(plugin_config)
                self.logger.info(f"Initialized plugin: {name}")
            except Exception as e:
                self.logger.error(f"Error initializing plugin {name}: {str(e)}")
    
    def cleanup_plugins(self) -> None:
        """Clean up all registered plugins"""
        self.logger.info("Cleaning up plugins")
        for name, plugin in self.plugins.items():
            try:
                plugin.cleanup()
                self.logger.info(f"Cleaned up plugin: {name}")
            except Exception as e:
                self.logger.error(f"Error cleaning up plugin {name}: {str(e)}")
    
    def get_plugin_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a plugin
        
        Args:
            name: Name of the plugin
            
        Returns:
            Dictionary containing plugin information, or None if not found
        """
        plugin = self.get_plugin(name)
        if plugin:
            try:
                return plugin.get_info()
            except Exception as e:
                self.logger.error(f"Error getting info for plugin {name}: {str(e)}")
        return None
    
    def get_all_plugin_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all registered plugins
        
        Returns:
            Dictionary of plugin names to plugin information
        """
        info = {}
        for name, plugin in self.plugins.items():
            plugin_info = self.get_plugin_info(name)
            if plugin_info:
                info[name] = plugin_info
        return info
