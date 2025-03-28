"""Tests for plugin registry"""
# pylint: disable=redefined-outer-name
from typing import Dict, Any
from unittest.mock import MagicMock, patch
import pytest

from src.plugins.interfaces import PluginInterface


class MockPlugin(PluginInterface):
    """Mock plugin for testing"""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.initialized = False
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin"""
        self.initialized = True
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the plugin"""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Mock plugin for testing",
            "author": "Test Author",
        }
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.initialized = False


@pytest.fixture
def mock_plugins():
    """Return mock plugins for testing"""
    return {
        "plugin1": MockPlugin("plugin1", "1.0.0"),
        "plugin2": MockPlugin("plugin2", "2.0.0"),
    }


def test_plugin_registry_initialization():
    """Test that PluginRegistry initializes correctly"""
    # This will fail until we implement the PluginRegistry class
    from src.plugins.registry import PluginRegistry
    
    # Create an instance of PluginRegistry
    registry = PluginRegistry()
    
    # Check that the registry is empty
    assert len(registry.get_plugins()) == 0


def test_plugin_registry_register_plugin(mock_plugins):
    """Test that PluginRegistry can register plugins"""
    # This will fail until we implement the PluginRegistry class
    from src.plugins.registry import PluginRegistry
    
    # Create an instance of PluginRegistry
    registry = PluginRegistry()
    
    # Register plugins
    for name, plugin in mock_plugins.items():
        registry.register_plugin(name, plugin)
    
    # Check that the plugins were registered
    assert len(registry.get_plugins()) == len(mock_plugins)
    
    # Check that the plugins can be retrieved
    for name, plugin in mock_plugins.items():
        assert registry.get_plugin(name) == plugin


def test_plugin_registry_unregister_plugin(mock_plugins):
    """Test that PluginRegistry can unregister plugins"""
    # This will fail until we implement the PluginRegistry class
    from src.plugins.registry import PluginRegistry
    
    # Create an instance of PluginRegistry
    registry = PluginRegistry()
    
    # Register plugins
    for name, plugin in mock_plugins.items():
        registry.register_plugin(name, plugin)
    
    # Unregister a plugin
    plugin_to_remove = list(mock_plugins.keys())[0]
    registry.unregister_plugin(plugin_to_remove)
    
    # Check that the plugin was unregistered
    assert len(registry.get_plugins()) == len(mock_plugins) - 1
    assert registry.get_plugin(plugin_to_remove) is None


def test_plugin_registry_initialize_plugins(mock_plugins):
    """Test that PluginRegistry can initialize plugins"""
    # This will fail until we implement the PluginRegistry class
    from src.plugins.registry import PluginRegistry
    
    # Create an instance of PluginRegistry
    registry = PluginRegistry()
    
    # Register plugins
    for name, plugin in mock_plugins.items():
        registry.register_plugin(name, plugin)
    
    # Initialize plugins
    config = {"test": "config"}
    registry.initialize_plugins(config)
    
    # Check that the plugins were initialized
    for plugin in mock_plugins.values():
        assert plugin.initialized


def test_plugin_registry_cleanup_plugins(mock_plugins):
    """Test that PluginRegistry can clean up plugins"""
    # This will fail until we implement the PluginRegistry class
    from src.plugins.registry import PluginRegistry
    
    # Create an instance of PluginRegistry
    registry = PluginRegistry()
    
    # Register plugins
    for name, plugin in mock_plugins.items():
        registry.register_plugin(name, plugin)
    
    # Initialize plugins
    config = {"test": "config"}
    registry.initialize_plugins(config)
    
    # Clean up plugins
    registry.cleanup_plugins()
    
    # Check that the plugins were cleaned up
    for plugin in mock_plugins.values():
        assert not plugin.initialized
