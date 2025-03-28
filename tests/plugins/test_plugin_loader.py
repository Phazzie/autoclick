"""Tests for plugin loader"""
# pylint: disable=redefined-outer-name
import os
from pathlib import Path
from typing import Dict, Any
from unittest.mock import MagicMock, patch
import pytest

from src.plugins.interfaces import PluginInterface


@pytest.fixture
def mock_plugin_dir(tmp_path):
    """Create a mock plugin directory for testing"""
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    
    # Create a valid plugin
    valid_plugin_dir = plugin_dir / "valid_plugin"
    valid_plugin_dir.mkdir()
    
    with open(valid_plugin_dir / "__init__.py", "w") as f:
        f.write("")
    
    with open(valid_plugin_dir / "plugin.py", "w") as f:
        f.write("""
from src.plugins.interfaces import PluginInterface

class ValidPlugin(PluginInterface):
    def initialize(self, config):
        pass
    
    def get_info(self):
        return {
            "name": "valid_plugin",
            "version": "1.0.0",
            "description": "A valid plugin for testing",
            "author": "Test Author",
        }
    
    def cleanup(self):
        pass
""")
    
    # Create an invalid plugin (missing required methods)
    invalid_plugin_dir = plugin_dir / "invalid_plugin"
    invalid_plugin_dir.mkdir()
    
    with open(invalid_plugin_dir / "__init__.py", "w") as f:
        f.write("")
    
    with open(invalid_plugin_dir / "plugin.py", "w") as f:
        f.write("""
class InvalidPlugin:
    def __init__(self):
        pass
""")
    
    return plugin_dir


def test_plugin_loader_initialization():
    """Test that PluginLoader initializes correctly"""
    # This will fail until we implement the PluginLoader class
    from src.plugins.loader import PluginLoader
    
    # Create an instance of PluginLoader
    loader = PluginLoader()
    
    # Check that the loader has a registry
    assert hasattr(loader, "registry")


@patch("importlib.import_module")
def test_plugin_loader_load_plugin(mock_import_module):
    """Test that PluginLoader can load a plugin"""
    # This will fail until we implement the PluginLoader class
    from src.plugins.loader import PluginLoader
    
    # Create a mock plugin module
    mock_plugin_class = MagicMock(spec=PluginInterface)
    mock_plugin_instance = MagicMock(spec=PluginInterface)
    mock_plugin_class.return_value = mock_plugin_instance
    
    # Configure the mock import_module
    mock_plugin_module = MagicMock()
    mock_plugin_module.ValidPlugin = mock_plugin_class
    mock_import_module.return_value = mock_plugin_module
    
    # Create an instance of PluginLoader
    loader = PluginLoader()
    
    # Load the plugin
    plugin = loader.load_plugin("valid_plugin", "ValidPlugin")
    
    # Check that the plugin was loaded
    assert plugin == mock_plugin_instance
    mock_import_module.assert_called_once_with("valid_plugin.plugin")


def test_plugin_loader_discover_plugins(mock_plugin_dir):
    """Test that PluginLoader can discover plugins"""
    # This will fail until we implement the PluginLoader class
    from src.plugins.loader import PluginLoader
    
    # Create an instance of PluginLoader
    loader = PluginLoader()
    
    # Discover plugins
    plugins = loader.discover_plugins(str(mock_plugin_dir))
    
    # Check that the valid plugin was discovered
    assert "valid_plugin" in plugins
    assert isinstance(plugins["valid_plugin"], PluginInterface)
    
    # Check that the invalid plugin was not discovered
    assert "invalid_plugin" not in plugins


def test_plugin_loader_load_plugins_from_directory(mock_plugin_dir):
    """Test that PluginLoader can load plugins from a directory"""
    # This will fail until we implement the PluginLoader class
    from src.plugins.loader import PluginLoader
    
    # Create an instance of PluginLoader
    loader = PluginLoader()
    
    # Load plugins from directory
    loader.load_plugins_from_directory(str(mock_plugin_dir))
    
    # Check that the valid plugin was loaded into the registry
    assert "valid_plugin" in loader.registry.get_plugins()
    
    # Check that the invalid plugin was not loaded
    assert "invalid_plugin" not in loader.registry.get_plugins()
