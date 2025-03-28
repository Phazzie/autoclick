"""Demonstration of the plugin system"""
import logging
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.plugins.loader import PluginLoader
from src.plugins.interfaces import ReporterPluginInterface, StoragePluginInterface


def main():
    """Main entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create a plugin loader
    loader = PluginLoader()
    
    # Get the path to the sample plugins
    plugin_dir = Path(__file__).parent.parent / "src" / "plugins" / "samples"
    
    # Load plugins from the directory
    loader.load_plugins_from_directory(str(plugin_dir))
    
    # Get all registered plugins
    plugins = loader.registry.get_plugins()
    print(f"Loaded {len(plugins)} plugins:")
    for name, plugin in plugins.items():
        info = plugin.get_info()
        print(f"  - {name} (v{info.get('version', 'unknown')}): {info.get('description', '')}")
    
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
    loader.initialize_plugins(config)
    
    # Use the HTML reporter plugin
    html_reporter = loader.registry.get_plugin("html_reporter")
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
                },
                {
                    "script": "script3.py",
                    "status": "success",
                    "duration": 2.0,
                    "message": ""
                }
            ]
        }
        
        # Generate a report
        output_path = "examples/report.html"
        html_reporter.generate_report(data, output_path)
        print(f"Generated HTML report: {output_path}")
    
    # Use the file storage plugin
    file_storage = loader.registry.get_plugin("file_storage")
    if file_storage and isinstance(file_storage, StoragePluginInterface):
        # Save some data
        file_storage.save("test_data", {"name": "Test", "value": 42})
        print("Saved test data")
        
        # Load the data
        data = file_storage.load("test_data")
        print(f"Loaded test data: {data}")
        
        # List all keys
        keys = file_storage.list()
        print(f"Available keys: {keys}")
    
    # Clean up plugins
    loader.cleanup_plugins()


if __name__ == "__main__":
    main()
