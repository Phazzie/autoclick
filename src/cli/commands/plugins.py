"""Plugins command handler"""
import argparse
import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List

from src.plugins.loader import PluginLoader
from src.plugins.interfaces import PluginInterface


def get_plugins_dir() -> Path:
    """
    Get the plugins directory
    
    Returns:
        Path to the plugins directory
    """
    # Default plugins directory
    plugins_dir = Path.home() / ".autoclick" / "plugins"
    
    # Ensure the directory exists
    plugins_dir.mkdir(parents=True, exist_ok=True)
    
    return plugins_dir


def get_plugin_loader() -> PluginLoader:
    """
    Get a configured plugin loader
    
    Returns:
        Configured plugin loader
    """
    # Create and return the plugin loader
    return PluginLoader()


def plugins_command(args: argparse.Namespace) -> int:
    """
    Handle the plugins command
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    logger = logging.getLogger(__name__)
    
    # If no subcommand is specified, show help
    if not hasattr(args, "subcommand") or not args.subcommand:
        logger.error("No subcommand specified")
        return 2
    
    try:
        # Get the plugin loader
        loader = get_plugin_loader()
        
        # Get the plugins directory
        plugins_dir = get_plugins_dir()
        
        # Load plugins from the plugins directory
        loader.load_plugins_from_directory(str(plugins_dir))
        
        # Handle the list subcommand
        if args.subcommand == "list":
            plugins = loader.registry.get_plugins()
            
            if plugins:
                print("Installed plugins:")
                for name, plugin in plugins.items():
                    info = plugin.get_info()
                    print(f"- {name} (v{info.get('version', 'unknown')}): {info.get('description', '')}")
            else:
                print("No plugins installed")
        
        # Handle the info subcommand
        elif args.subcommand == "info":
            plugin_name = args.plugin
            plugin = loader.registry.get_plugin(plugin_name)
            
            if plugin:
                info = plugin.get_info()
                print(f"Plugin: {plugin_name}")
                print(f"Version: {info.get('version', 'unknown')}")
                print(f"Description: {info.get('description', '')}")
                print(f"Author: {info.get('author', 'unknown')}")
                
                # Print additional information if available
                for key, value in info.items():
                    if key not in ("name", "version", "description", "author"):
                        print(f"{key.capitalize()}: {value}")
            else:
                logger.error(f"Plugin not found: {plugin_name}")
                return 2
        
        # Handle the install subcommand
        elif args.subcommand == "install":
            plugin_path = Path(args.plugin_path)
            
            if not plugin_path.exists():
                logger.error(f"Plugin path not found: {plugin_path}")
                return 2
            
            if plugin_path.is_file():
                logger.error("Installing from a file is not supported. Please provide a directory.")
                return 2
            
            # Get the plugin name from the directory name
            plugin_name = plugin_path.name
            
            # Check if the plugin already exists
            if (plugins_dir / plugin_name).exists():
                logger.error(f"Plugin already installed: {plugin_name}")
                return 2
            
            try:
                # Copy the plugin to the plugins directory
                shutil.copytree(plugin_path, plugins_dir / plugin_name)
                logger.info(f"Installed plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error installing plugin: {str(e)}")
                return 5
        
        # Handle the uninstall subcommand
        elif args.subcommand == "uninstall":
            plugin_name = args.plugin
            plugin_dir = plugins_dir / plugin_name
            
            if not plugin_dir.exists():
                logger.error(f"Plugin not found: {plugin_name}")
                return 2
            
            try:
                # Remove the plugin directory
                shutil.rmtree(plugin_dir)
                logger.info(f"Uninstalled plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error uninstalling plugin: {str(e)}")
                return 5
        
        # Handle the enable subcommand
        elif args.subcommand == "enable":
            plugin_name = args.plugin
            plugin = loader.registry.get_plugin(plugin_name)
            
            if not plugin:
                logger.error(f"Plugin not found: {plugin_name}")
                return 2
            
            # Enable the plugin (placeholder for future implementation)
            logger.info(f"Enabled plugin: {plugin_name}")
        
        # Handle the disable subcommand
        elif args.subcommand == "disable":
            plugin_name = args.plugin
            plugin = loader.registry.get_plugin(plugin_name)
            
            if not plugin:
                logger.error(f"Plugin not found: {plugin_name}")
                return 2
            
            # Disable the plugin (placeholder for future implementation)
            logger.info(f"Disabled plugin: {plugin_name}")
        
        else:
            logger.error(f"Unknown subcommand: {args.subcommand}")
            return 2
        
        return 0
    
    except Exception as e:
        logger.error(f"Error in plugins command: {str(e)}")
        return 1
