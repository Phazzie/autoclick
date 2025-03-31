# AUTOCLICK User Guide

## Introduction

AUTOCLICK is an automation tool designed to perform click sequences, take screenshots, and handle credentials. This guide will help you understand how to use the application effectively.

## Getting Started

### Running the Application

To start the application:

```
python main.py
```

The application will open with a sidebar on the left containing different tabs and a main content area on the right.

## Main Components

### 1. Workflow Builder

The Workflow Builder is the main component where you create automation workflows.

#### Creating a New Workflow

1. Click on the "Workflow Builder" tab in the sidebar
2. Click the "New Workflow" button
3. Enter a name for your workflow

#### Adding Actions to Your Workflow

1. Select an action type from the toolbox on the left side of the Workflow Builder
2. Click on the canvas to place the action
3. Configure the action's properties in the properties panel on the right

#### Connecting Actions

1. Click and drag from the output port of one action to the input port of another action
2. This creates a connection that defines the flow of execution

#### Saving Your Workflow

1. Click the "Save" button to save your workflow
2. Workflows are saved in the "workflows" directory

### 2. Action Execution

The Action Execution tab allows you to run your workflows.

1. Select a workflow from the dropdown
2. Click the "Execute" button
3. View the execution results in the results area

### 3. Variable Management

The Variable Management tab allows you to create and manage variables that can be used in your workflows.

1. Click the "Add Variable" button
2. Enter a name and value for the variable
3. Variables can be referenced in action properties using `${variable_name}` syntax

### 4. Credential Management

The Credential Management tab allows you to store and manage login credentials.

1. Click the "Add Credential" button
2. Enter the required information (username, password, etc.)
3. Credentials can be used in your workflows for login actions

### 5. Condition Editor

The Condition Editor allows you to create conditional logic for your workflows.

1. Create conditions based on element properties, variable values, etc.
2. Use these conditions in If-Then-Else actions in your workflows

### 6. Loop Configuration

The Loop Configuration tab allows you to create loops for repetitive tasks.

1. Configure loop settings such as iteration count, loop variable, etc.
2. Use these loops in your workflows to repeat actions

### 7. Error Handling

The Error Handling tab allows you to configure how errors are handled in your workflows.

1. Define error recovery strategies
2. Configure retry settings, fallback actions, etc.

### 8. Reporting

The Reporting tab shows the results of workflow executions.

1. View execution statistics
2. See screenshots taken during execution
3. Analyze errors and issues

## Example Workflow: Login to a Website

Here's a step-by-step example of creating a simple login workflow:

1. Create a new workflow named "Website Login"
2. Add a "Navigate" action and set the URL to your target website
3. Add a "Click" action to click on the username field
   - Set the selector to the appropriate CSS or XPath selector
4. Add an "Input" action to enter the username
   - Set the selector to the username field
   - Set the value to `${username}` or directly enter a username
5. Add a "Click" action to click on the password field
6. Add an "Input" action to enter the password
7. Add a "Click" action to click the login button
8. Connect all actions in sequence
9. Save the workflow
10. Go to the Action Execution tab and run the workflow

## Troubleshooting

If you encounter issues:

1. Check the Error Handling tab for any logged errors
2. Verify that your selectors are correct
3. Make sure your credentials are entered correctly
4. Ensure that all actions are properly connected

## Advanced Features

### Data-Driven Automation

You can use data sources like CSV or JSON files to drive your automation:

1. Configure a data source in the Data Sources tab
2. Use a For-Each loop to iterate through the data
3. Reference data fields in your actions

### Conditional Logic

You can add conditional logic to your workflows:

1. Use If-Then-Else actions to create branches in your workflow
2. Configure conditions based on element properties, variable values, etc.

### Error Recovery

You can configure how your workflow handles errors:

1. Define error recovery strategies in the Error Handling tab
2. Configure retry settings, fallback actions, etc.

## Keyboard Shortcuts

- Ctrl+S: Save workflow
- Ctrl+N: New workflow
- Ctrl+E: Execute workflow
- Delete: Delete selected action
- Ctrl+Z: Undo
- Ctrl+Y: Redo

## Additional Resources

For more information, refer to the documentation in the "docs" directory.
