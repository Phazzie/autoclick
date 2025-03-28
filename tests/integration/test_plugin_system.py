"""Integration tests for the plugin system"""
# pylint: disable=redefined-outer-name
import os
from pathlib import Path
import shutil
import pytest

from src.plugins.loader import PluginLoader
from src.plugins.interfaces import (
    PluginInterface,
    ReporterPluginInterface,
    StoragePluginInterface
)


@pytest.fixture
def plugin_dir(tmp_path) -> Path:
    """Create a temporary plugin directory with sample plugins"""
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    
    # Copy the sample plugins to the temporary directory
    sample_plugins_dir = Path(__file__).parent.parent.parent / "src" / "plugins" / "samples"
    if sample_plugins_dir.exists():
        for item in sample_plugins_dir.iterdir():
            if item.is_dir():
                shutil.copytree(item, plugin_dir / item.name)
    
    return plugin_dir


@pytest.fixture
def plugin_loader() -> PluginLoader:
    """Return a plugin loader instance"""
    return PluginLoader()


def test_plugin_discovery(plugin_loader, plugin_dir):
    """Test that plugins can be discovered"""
    # Discover plugins
    plugins = plugin_loader.discover_plugins(str(plugin_dir))
    
    # Check that plugins were discovered
    assert len(plugins) > 0
    
    # Check that the HTML reporter plugin was discovered
    assert "html_reporter" in plugins
    assert isinstance(plugins["html_reporter"], ReporterPluginInterface)
    
    # Check that the file storage plugin was discovered
    assert "file_storage" in plugins
    assert isinstance(plugins["file_storage"], StoragePluginInterface)


def test_plugin_loading_and_registration(plugin_loader, plugin_dir):
    """Test that plugins can be loaded and registered"""
    # Load plugins from the directory
    plugin_loader.load_plugins_from_directory(str(plugin_dir))
    
    # Check that plugins were registered
    plugins = plugin_loader.registry.get_plugins()
    assert len(plugins) > 0
    
    # Check that the HTML reporter plugin was registered
    assert "html_reporter" in plugins
    assert isinstance(plugins["html_reporter"], ReporterPluginInterface)
    
    # Check that the file storage plugin was registered
    assert "file_storage" in plugins
    assert isinstance(plugins["file_storage"], StoragePluginInterface)


def test_plugin_initialization_and_cleanup(plugin_loader, plugin_dir):
    """Test that plugins can be initialized and cleaned up"""
    # Load plugins from the directory
    plugin_loader.load_plugins_from_directory(str(plugin_dir))
    
    # Initialize plugins with configuration
    config = {
        "html_reporter": {
            "template_path": "templates/report.html"
        },
        "file_storage": {
            "storage_dir": "data/storage",
            "format": "json"
        }
    }
    plugin_loader.initialize_plugins(config)
    
    # Check that the HTML reporter plugin was initialized
    html_reporter = plugin_loader.registry.get_plugin("html_reporter")
    assert html_reporter.config == config["html_reporter"]
    
    # Check that the file storage plugin was initialized
    file_storage = plugin_loader.registry.get_plugin("file_storage")
    assert file_storage.config == config["file_storage"]
    
    # Clean up plugins
    plugin_loader.cleanup_plugins()


def test_plugin_functionality(plugin_loader, plugin_dir, tmp_path):
    """Test that plugins can be used"""
    # Load plugins from the directory
    plugin_loader.load_plugins_from_directory(str(plugin_dir))
    
    # Initialize plugins with configuration
    storage_dir = tmp_path / "storage"
    report_dir = tmp_path / "reports"
    
    config = {
        "html_reporter": {
            "template_path": "templates/report.html"
        },
        "file_storage": {
            "storage_dir": str(storage_dir),
            "format": "json"
        }
    }
    plugin_loader.initialize_plugins(config)
    
    # Use the HTML reporter plugin
    html_reporter = plugin_loader.registry.get_plugin("html_reporter")
    if html_reporter and isinstance(html_reporter, ReporterPluginInterface):
        # Create some sample data
        data = {
            "results": [
                {
                    "script": "script1.py",
                    "status": "success",
                    "duration": 1.5,
                    "message": ""
                },
                {
                    "script": "script2.py",
                    "status": "error",
                    "duration": 0.5,
                    "message": "Element not found"
                }
            ]
        }
        
        # Generate a report
        report_dir.mkdir(exist_ok=True)
        output_path = str(report_dir / "report.html")
        html_reporter.generate_report(data, output_path)
        
        # Check that the report was generated
        assert Path(output_path).exists()
    
    # Use the file storage plugin
    file_storage = plugin_loader.registry.get_plugin("file_storage")
    if file_storage and isinstance(file_storage, StoragePluginInterface):
        # Save some data
        test_data = {"name": "Test", "value": 42}
        file_storage.save("test_data", test_data)
        
        # Check that the storage directory was created
        assert storage_dir.exists()
        
        # Load the data
        loaded_data = file_storage.load("test_data")
        
        # Check that the data was loaded correctly
        assert loaded_data == test_data
        
        # List all keys
        keys = file_storage.list()
        
        # Check that the key is in the list
        assert "test_data" in keys
        
        # Delete the data
        file_storage.delete("test_data")
        
        # Check that the key was deleted
        keys = file_storage.list()
        assert "test_data" not in keys
    
    # Clean up plugins
    plugin_loader.cleanup_plugins()
