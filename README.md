# AUTOCLICK - Web Automation Project

A streamlined, maintainable, and easily extensible web automation application.

## Features

- **Modern UI**: Intuitive graphical interface with keyboard shortcuts and drag-and-drop
- **Workflow Builder**: Create and edit automation workflows visually
- **Browser Recording**: Record actions in Chrome, Firefox, or Edge
- **Element Selection**: Select and inspect elements on web pages
- **Secure Credentials**: Manage website credentials securely
- **Execution Engine**: Run workflows with detailed logging
- **Extensible Architecture**: Add new features through plugins

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Chrome, Firefox, or Edge browser (for web automation)

### Setup

1. Clone the repository:

   ```
   git clone <repository-url>
   cd AUTOCLICK
   ```

2. Set up the development environment:
   ```
   python tools/setup_environment.py
   ```
   This will:
   - Install all required dependencies
   - Set up git hooks for code quality
   - Initialize the project structure

### Running the Application

1. Start the GUI:

   ```
   python -m src.cli.main gui
   ```

2. Or use the command-line interface:
   ```
   python -m src.cli.main --help
   ```

### Development Workflow

1. Make your changes following the project guidelines
2. The pre-commit hook will automatically:
   - Format your code (fix whitespace, imports, etc.)
   - Run code quality checks
3. If the checks pass, your commit will proceed
4. If the checks fail, fix the issues and try again

## Code Quality Tools

### Automatic Formatting

Run the code formatter to automatically fix common issues:

```
python tools/code_formatter.py
```

This will:

- Remove trailing whitespace
- Ensure files end with a newline
- Fix import order with isort
- Format code with black

### Quality Checks

Run the code quality checker to verify your code meets the project standards:

```
python tools/code_quality_checker.py
```

This checks:

- KISS principles (function/class sizes, complexity)
- SOLID principles (class design)
- DRY principles (code duplication)
- Type hints with mypy
- Code formatting with black

## Project Structure

- `src/` - Source code
  - `cli/` - Command-line interface
  - `core/` - Core functionality
  - `ui/` - User interface
    - `components/` - UI components
    - `interfaces/` - Interfaces for UI components
    - `models/` - Data models
    - `presenters/` - Presenters for UI components
    - `services/` - Services for UI components
  - `plugins/` - Plugin implementations
  - `utils/` - Utility functions
- `tests/` - Test suite
  - `cli/` - Tests for CLI
  - `core/` - Tests for core functionality
  - `ui/` - Tests for UI components
- `tools/` - Development tools
- `docs/` - Documentation
  - `user_guide.md` - User documentation
  - `developer_guide.md` - Developer documentation

## Plugin System

AUTOCLICK features a powerful plugin system that allows you to extend its functionality without modifying the core codebase.

### Plugin Types

The system supports several types of plugins:

- **Automation Plugins**: Extend the automation capabilities
- **Reporter Plugins**: Create custom report formats
- **Storage Plugins**: Implement different storage backends

### Using Plugins

To use plugins in your automation:

```python
from src.plugins.loader import PluginLoader

# Create a plugin loader
loader = PluginLoader()

# Load plugins from a directory
loader.load_plugins_from_directory("path/to/plugins")

# Initialize plugins with configuration
config = {
    "plugin_name": {
        "option1": "value1",
        "option2": "value2"
    }
}
loader.initialize_plugins(config)

# Get a specific plugin
plugin = loader.registry.get_plugin("plugin_name")

# Use the plugin
plugin.some_method()

# Clean up when done
loader.cleanup_plugins()
```

### Creating Plugins

To create a new plugin:

1. Create a new directory for your plugin
2. Create an `__init__.py` file
3. Create a `plugin.py` file with your plugin class
4. Implement the appropriate plugin interface

Example:

```python
from src.plugins.interfaces import ReporterPluginInterface

class MyReporterPlugin(ReporterPluginInterface):
    def initialize(self, config):
        # Initialize with configuration
        pass

    def get_info(self):
        # Return plugin information
        return {
            "name": "my_reporter",
            "version": "1.0.0",
            "description": "My custom reporter plugin"
        }

    def cleanup(self):
        # Clean up resources
        pass

    def generate_report(self, data, output_path):
        # Generate a report
        pass

    def get_supported_formats(self):
        # Return supported formats
        return ["custom"]
```

You can also use the plugin generator to create new plugins:

```
python tools/plugin_generator.py <plugin-name> <plugin-type>
```

Where `<plugin-type>` is one of:

- `reporters` - For result reporting
- `runners` - For execution strategies
- `storage` - For data storage

## Core Principles

1. **Single Responsibility (SRP)**

   - One class = one purpose
   - One function = one task
   - One file = one concern
   - Max 20 lines per function
   - Extract until you can't extract anymore

2. **Extensibility First**

   - Plugin-based architecture
   - Clear interfaces
   - Configuration-driven features
   - No hard dependencies between modules
   - Easy to add new capabilities

3. **Keep It Simple (KISS)**

   - Minimal core features
   - Clear, readable code
   - Obvious workflows
   - No premature optimization
   - Simple > clever

4. **Don't Repeat Yourself (DRY)**
   - Shared utilities
   - Common interfaces
   - Reusable components
   - Standard patterns
   - Central configuration
