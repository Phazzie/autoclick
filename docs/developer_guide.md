# AUTOCLICK Developer Guide

## Architecture Overview

AUTOCLICK follows a Model-View-Presenter (MVP) architecture to ensure separation of concerns and maintainability. The application is organized into the following components:

### Core Components

- **Models**: Represent the data and business logic
- **Views**: Handle the UI presentation
- **Presenters**: Coordinate between models and views
- **Services**: Provide functionality to other components

### Directory Structure

```
autoclick/
├── docs/                  # Documentation
├── src/                   # Source code
│   ├── cli/               # Command-line interface
│   ├── core/              # Core functionality
│   ├── ui/                # User interface
│   │   ├── components/    # UI components
│   │   ├── interfaces/    # Interfaces for UI components
│   │   ├── models/        # Data models
│   │   ├── presenters/    # Presenters for UI components
│   │   └── services/      # Services for UI components
│   └── utils/             # Utility functions
└── tests/                 # Tests
    ├── cli/               # Tests for CLI
    ├── core/              # Tests for core functionality
    └── ui/                # Tests for UI components
```

## Design Principles

AUTOCLICK follows these design principles:

### SOLID Principles

1. **Single Responsibility Principle (SRP)**: Each class has a single responsibility
2. **Open/Closed Principle (OCP)**: Classes are open for extension but closed for modification
3. **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types
4. **Interface Segregation Principle (ISP)**: Clients should not depend on interfaces they don't use
5. **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions

### Other Principles

- **KISS (Keep It Simple, Stupid)**: Keep code simple and straightforward
- **DRY (Don't Repeat Yourself)**: Avoid code duplication
- **TDD (Test-Driven Development)**: Write tests before implementation

## Implementation Details

### Models

Models represent the data and business logic of the application. They are responsible for:

- Storing and managing data
- Implementing business rules
- Providing data access methods

Example:

```python
class WorkflowModel:
    def __init__(self) -> None:
        self._actions = []
        self._name = "New Workflow"
        self._file_path = None

    def add_action(self, action: Dict[str, Any]) -> str:
        action_id = str(uuid.uuid4())
        action_with_id = action.copy()
        action_with_id["id"] = action_id
        self._actions.append(action_with_id)
        return action_id
```

### Views

Views are responsible for displaying the UI and handling user interactions. They:

- Render the UI components
- Capture user input
- Forward user actions to presenters

Example:

```python
class WorkflowTab(BaseComponent, WorkflowViewInterface):
    def __init__(self, parent: Any, presenter: WorkflowPresenter) -> None:
        super().__init__(parent)
        self.presenter = presenter
        self.presenter.set_view(self)
        self._create_ui()

    def display_actions(self, actions: List[Dict[str, Any]]) -> None:
        # Clear existing items
        for item in self.actions_tree.get_children():
            self.actions_tree.delete(item)

        # Add actions to treeview
        for action in actions:
            self.actions_tree.insert(
                "",
                tk.END,
                values=(
                    action.get("id", ""),
                    action.get("type", ""),
                    action.get("selector", ""),
                    action.get("value", ""),
                    action.get("description", "")
                )
            )
```

### Presenters

Presenters coordinate between models and views. They:

- Handle user actions from views
- Update models based on user actions
- Update views based on model changes

Example:

```python
class WorkflowPresenter:
    def __init__(self, model: WorkflowModel, view: Optional[WorkflowViewInterface] = None) -> None:
        self.model = model
        self.view = view

    def add_action(self, action: Dict[str, Any]) -> None:
        action_id = self.model.add_action(action)
        self.refresh_view()

        if self.view:
            self.view.show_message(f"Action added: {action.get('description', 'No description')}")
```

### Services

Services provide functionality to other components. They:

- Encapsulate complex operations
- Provide reusable functionality
- Abstract external dependencies

Example:

```python
class FileService:
    def load_workflow(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise IOError(f"Failed to load workflow: {str(e)}")
```

## Adding New Features

To add a new feature to AUTOCLICK, follow these steps:

1. **Define the feature requirements**: What problem does it solve? What are the user stories?
2. **Design the feature**: How will it fit into the existing architecture? What components will it need?
3. **Write tests**: Create tests for the new feature before implementing it
4. **Implement the feature**: Follow the design principles and architecture
5. **Test the feature**: Run the tests and fix any issues
6. **Document the feature**: Update the documentation

### Example: Adding a New Action Type

1. **Define the requirements**: Users need to be able to hover over elements
2. **Design the feature**: Add a new action type "hover" to the existing action system
3. **Write tests**: Create tests for the hover action
4. **Implement the feature**:
   - Add the hover action type to the action form
   - Implement the hover action in the execution service
5. **Test the feature**: Run the tests and verify the hover action works
6. **Document the feature**: Update the documentation with the new action type

## Testing

AUTOCLICK uses unittest for testing. Tests are organized by component:

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test interactions between components
- **End-to-end tests**: Test the entire application

### Running Tests

To run all tests:

```bash
python -m unittest discover
```

To run tests for a specific module:

```bash
python -m unittest tests.ui.models.test_workflow_model
```

### Writing Tests

Follow these guidelines when writing tests:

- Test one thing per test method
- Use descriptive test method names
- Use setUp and tearDown methods for common setup and cleanup
- Use mocks for external dependencies
- Test edge cases and error conditions

Example:

```python
class TestWorkflowModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = WorkflowModel()
        self.test_action = {
            "type": "click",
            "selector": "#test-button",
            "description": "Click test button"
        }

    def test_add_action(self) -> None:
        # Act
        action_id = self.model.add_action(self.test_action)

        # Assert
        self.assertIsNotNone(action_id)
        self.assertEqual(len(self.model._actions), 1)
        self.assertEqual(self.model._actions[0]["type"], "click")
```

## Contributing

To contribute to AUTOCLICK, follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for your changes
5. Run the tests
6. Submit a pull request

### Code Style

AUTOCLICK follows these code style guidelines:

- Use type hints for all function parameters and return values
- Use docstrings for all classes and methods
- Follow PEP 8 for code formatting
- Keep functions small and focused
- Use descriptive variable and function names

### Pull Request Process

1. Ensure all tests pass
2. Update the documentation
3. Update the CHANGELOG.md file
4. Submit the pull request with a clear description of the changes

## Troubleshooting

### Common Development Issues

- **Import errors**: Check the import paths and ensure the package is installed
- **UI not updating**: Ensure the presenter is updating the view
- **Tests failing**: Check the test output for details on the failure

### Debugging Tips

- Use logging to track the flow of execution
- Use the Python debugger (pdb) to step through code
- Check the application logs for error messages
- Use print statements for quick debugging
