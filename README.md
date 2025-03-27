# AUTOCLICK - Web Automation Project

A streamlined, maintainable, and easily extensible web automation application.

## Features

- Manages user credentials securely
- Allows users to build and execute web automation workflows
- Provides basic reporting/analytics on results
- Supports parallel execution of workflows
- Enables easy addition of new features through plugins

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git

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
  - `core/` - Core functionality
  - `plugins/` - Plugin implementations
  - `utils/` - Utility functions
- `tests/` - Test suite
- `tools/` - Development tools
- `docs/` - Documentation

## Creating Plugins

Use the plugin generator to create new plugins:

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
