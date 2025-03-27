# AUTOCLICK User Guide

## Introduction

AUTOCLICK is a powerful web automation tool that allows you to automate repetitive tasks in web browsers. With its intuitive graphical user interface, you can record browser actions, select elements, build workflows, and execute automations without writing code.

## Getting Started

### Installation

To install AUTOCLICK, follow these steps:

1. Ensure you have Python 3.8 or later installed
2. Clone the repository: `git clone https://github.com/Phazzie/autoclick.git`
3. Navigate to the project directory: `cd autoclick`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python -m src.cli.main gui`

### Main Interface

The AUTOCLICK interface consists of five main tabs:

1. **Record**: Record browser actions in real-time
2. **Element Selector**: Select and inspect elements on web pages
3. **Workflow Builder**: Create and edit automation workflows
4. **Execution**: Run automation workflows
5. **Credentials**: Manage stored credentials for websites

## Recording Browser Actions

The Record tab allows you to record actions in a web browser:

1. Select a browser (Chrome, Firefox, or Edge)
2. Toggle headless mode if needed
3. Click "Start Recording" to launch the browser
4. Perform actions in the browser (clicks, inputs, etc.)
5. Click "Stop Recording" when finished
6. Review recorded actions in the list
7. Click "Add to Workflow" to add selected actions to the workflow builder

## Selecting Elements

The Element Selector tab helps you identify and select elements on web pages:

1. Enter a URL in the address bar
2. Select a browser (Chrome, Firefox, or Edge)
3. Toggle headless mode if needed
4. Click "Select Element" to launch the browser
5. Click on elements in the page to select them
6. View element properties in the properties panel
7. Click "Add to Workflow" to create an action for the selected element

## Building Workflows

The Workflow Builder tab allows you to create and edit automation workflows:

1. Use "Add Action" to add a new action manually
2. Use "Remove Action" to delete the selected action
3. Use "Move Up" and "Move Down" to reorder actions
4. Double-click an action to edit its properties
5. Drag and drop actions to reorder them

### Action Types

- **Click**: Click on an element
- **Input**: Enter text into an input field
- **Select**: Select an option from a dropdown
- **Wait**: Wait for a specified time or condition
- **Navigate**: Navigate to a URL

## Executing Workflows

The Execution tab allows you to run your automation workflows:

1. Select a browser (Chrome, Firefox, or Edge)
2. Toggle headless mode if needed
3. Set timeout and other execution options
4. Click "Run Workflow" to execute the current workflow
5. View execution progress in the log
6. Click "Stop Execution" to halt the workflow if needed

## Managing Credentials

The Credentials tab allows you to securely store and manage website credentials:

1. Select a site from the list to view its credentials
2. Enter site name, username, and password
3. Click "Save" to store the credentials
4. Click "Remove" to delete the credentials
5. Click "Clear" to clear the form

## Keyboard Shortcuts

AUTOCLICK provides keyboard shortcuts for common actions:

- **Ctrl+N**: New workflow
- **Ctrl+O**: Open workflow
- **Ctrl+S**: Save workflow
- **Ctrl+Shift+S**: Save workflow as
- **Ctrl+Q**: Exit application
- **Ctrl+1**: Switch to Record tab
- **Ctrl+2**: Switch to Element Selector tab
- **Ctrl+3**: Switch to Workflow Builder tab
- **Ctrl+4**: Switch to Execution tab
- **Ctrl+5**: Switch to Credentials tab
- **F1**: Show keyboard shortcuts

### Workflow Builder Shortcuts

- **Ctrl+N**: Add action
- **Delete**: Remove selected action
- **Ctrl+Up**: Move selected action up
- **Ctrl+Down**: Move selected action down

## Tips and Tricks

- Use headless mode for faster execution when visual feedback isn't needed
- Create small, focused workflows for better maintainability
- Use descriptive names for your workflows and actions
- Test workflows with different browsers to ensure compatibility
- Use the Element Selector to find the most reliable selectors for elements

## Troubleshooting

### Common Issues

- **Browser doesn't launch**: Ensure the selected browser is installed on your system
- **Element not found**: Try using a different selector or wait for the element to appear
- **Action fails**: Check if the website structure has changed
- **Workflow stops unexpectedly**: Check the execution log for error messages

### Getting Help

If you encounter issues not covered in this guide, please:

1. Check the [GitHub repository](https://github.com/Phazzie/autoclick) for known issues
2. Submit a new issue with detailed information about the problem
3. Include steps to reproduce, expected behavior, and actual behavior
