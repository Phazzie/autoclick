"""Loader for discovering and loading plugins"""
import importlib
import inspect
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from src.plugins.interfaces import PluginInterface
from src.plugins.registry import PluginRegistry


class PluginLoader:
    """Discovers and loads plugins"""
    
    def __init__(self) -> None:
        """Initialize the plugin loader"""
        self.logger = logging.getLogger(__name__)
        self.registry = PluginRegistry()
    
    def load_plugin(self, module_name: str, class_name: str) -> Optional[PluginInterface]:
        """
        Load a plugin from a module
        
        Args:
            module_name: Name of the module containing the plugin
            class_name: Name of the plugin class
            
        Returns:
            Plugin instance, or None if loading failed
        """
        try:
            # Import the module
            module = importlib.import_module(f"{module_name}.plugin")
            
            # Get the plugin class
            plugin_class = getattr(module, class_name)
            
            # Check if the class implements PluginInterface
            if not issubclass(plugin_class, PluginInterface):
                self.logger.warning(
                    f"Class {class_name} in module {module_name} "
                    f"does not implement PluginInterface"
                )
                return None
            
            # Create an instance of the plugin
            plugin = plugin_class()
            
            return plugin
        except ImportError as e:
            self.logger.error(f"Error importing module {module_name}: {str(e)}")
        except AttributeError as e:
            self.logger.error(
                f"Class {class_name} not found in module {module_name}: {str(e)}"
            )
        except Exception as e:
            self.logger.error(f"Error loading plugin {module_name}.{class_name}: {str(e)}")
        
        return None
    
    def discover_plugins(self, directory: str) -> Dict[str, PluginInterface]:
        """
        Discover plugins in a directory
        
        Args:
            directory: Directory to search for plugins
            
        Returns:
            Dictionary of plugin names to plugin instances
        """
        self.logger.info(f"Discovering plugins in {directory}")
        plugins = {}
        
        # Ensure the directory exists
        if not os.path.isdir(directory):
            self.logger.warning(f"Plugin directory {directory} does not exist")
            return plugins
        
        # Add the directory to the Python path
        sys.path.insert(0, directory)
        
        try:
            # Iterate over subdirectories
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                
                # Check if it's a directory and contains a plugin.py file
                if (os.path.isdir(item_path) and 
                    os.path.isfile(os.path.join(item_path, "__init__.py")) and
                    os.path.isfile(os.path.join(item_path, "plugin.py"))):
                    
                    # Try to find plugin classes in the module
                    try:
                        # Import the module
                        module = importlib.import_module(f"{item}.plugin")
                        
                        # Find classes that implement PluginInterface
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if (issubclass(obj, PluginInterface) and 
                                obj is not PluginInterface and
                                not name.startswith("_")):
                                
                                # Create an instance of the plugin
                                plugin = obj()
                                plugins[item] = plugin
                                self.logger.info(f"Discovered plugin: {item} ({name})")
                    except Exception as e:
                        self.logger.error(f"Error discovering plugin in {item}: {str(e)}")
        finally:
            # Remove the directory from the Python path
            if directory in sys.path:
                sys.path.remove(directory)
        
        return plugins
    
    def load_plugins_from_directory(self, directory: str) -> None:
        """
        Load plugins from a directory and register them
        
        Args:
            directory: Directory to search for plugins
        """
        self.logger.info(f"Loading plugins from {directory}")
        
        # Discover plugins
        plugins = self.discover_plugins(directory)
        
        # Register plugins
        for name, plugin in plugins.items():
            self.registry.register_plugin(name, plugin)
    
    def initialize_plugins(self, config: Dict[str, Any]) -> None:
        """
        Initialize all registered plugins
        
        Args:
            config: Configuration dictionary
        """
        self.registry.initialize_plugins(config)
    
    def cleanup_plugins(self) -> None:
        """Clean up all registered plugins"""
        self.registry.cleanup_plugins()
