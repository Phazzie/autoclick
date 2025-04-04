# INSTRUCTIONS FOR AI ASSISTANT

## Task Overview

I need you to analyze and fix the problematic components in the AUTOCLICK project. This document contains the code for components that need to be fixed or replaced, along with descriptions of their issues and reference implementations of working components.

## Requested  Format

Please provide your response in the following format:

1. **Analysis Summary**: A high-level overview of the issues you've identified and your approach to fixing them

2. **For Each Problematic Component**:

    - Brief analysis of specific issues (beyond what I've already identified)
    - Complete implementation of the fixed component as a code block
    - Unit tests for the component as a separate code block
    - Explanation of how your implementation addresses the issues and follows SOLID/KISS/DRY principles

3. **Integration Guide**: Instructions on how to integrate your fixed components with the existing architecture

4. **Testing Strategy**: Approach for testing the integrated components

Please ensure all implementations:

-   Follow SOLID, KISS, and DRY principles (93%+ compliance)
-   Use proper dependency injection
-   Have clear separation of concerns
-   Include comprehensive unit tests
-   Are compatible with the existing architecture

---

# AUTOCLICK Project Analysis

This document provides a comprehensive analysis of the AUTOCLICK project, focusing on problematic components that need to be fixed or replaced.

## Project Overview

AUTOCLICK is an application that loads credentials from a file, performs click sequences, takes screenshots, logs out, and repeats with the next set of credentials. The project is implementing clean architecture with domain, application, infrastructure, and UI layers.

### Project Structure

The project follows a clean architecture approach with these main directories:

```
src/
├── core/               # Core business logic and domain models
│   ├── actions/        # Action implementations (click, screenshot, etc.)
│   ├── conditions/     # Condition implementations for decision making
│   ├── context/        # Execution context and variable storage
│   ├── credentials/    # Credential management
│   ├── data/           # Data sources and mapping
│   ├── errors/         # Error handling and recovery
│   ├── events/         # Event system for communication
│   ├── models.py       # Core domain models
│   ├── utils/          # Utility functions
│   ├── variables/      # Variable handling
│   └── workflow/       # Workflow engine and services
│       ├── engine/     # New engine implementation
│       └── service/    # New service implementation
├── domain/             # Domain layer (clean architecture)
│   ├── actions/        # Domain interfaces for actions
│   ├── credentials/    # Domain interfaces for credentials
│   └── workflows/      # Domain interfaces for workflows
├── application/        # Application layer (clean architecture)
│   └── workflows/      # Application services for workflows
├── infrastructure/     # Infrastructure layer (clean architecture)
│   ├── adapters/       # Adapters for external services
│   ├── repositories/   # Data repositories
│   └── serialization/  # Serialization services
└── ui/                 # User interface layer
    ├── adapters/       # UI adapters for domain services
    ├── components/     # UI components
    ├── presenters/     # Presenters for UI logic
    └── views/          # Views for UI rendering
```

### Component Dependencies

Here are the key component dependencies in the system:

1. **UI Layer Dependencies**:

    - Views depend on Presenters
    - Presenters depend on UI Adapters
    - UI Adapters depend on Domain Services

2. **Workflow Engine Dependencies**:

    - WorkflowEngine depends on WorkflowValidator, WorkflowExecutor, EventBus
    - WorkflowValidator validates WorkflowDefinition objects
    - WorkflowExecutor executes WorkflowDefinition objects
    - WorkflowService depends on WorkflowEngine and WorkflowStorageService

3. **Action System Dependencies**:

    - Actions depend on ExecutionContext
    - ExecutionContext depends on VariableStorage
    - ActionFactory creates and manages Actions

4. **Data Flow**:
    - UI → Presenters → Adapters → Domain Services → Core Services → Infrastructure

### Key Requirements

-   Strict adherence to SOLID, KISS, DRY principles
-   Test-Driven Development (TDD) mandatory
-   Single Responsibility Principle (SRP) focus
-   Proper dependency injection
-   Clean separation of concerns

### Test Example

Here's an example of a test for the WorkflowEngine component that follows the project's testing approach:

```python
"""Tests for the refactored workflow engine."""
import unittest
from unittest.mock import Mock, MagicMock, patch

from src.core.workflow.interfaces import WorkflowDefinition
from src.core.workflow.workflow_engine_new import WorkflowEngine
from src.core.workflow.execution_result import ExecutionResult
from src.core.workflow.exceptions import WorkflowValidationError, WorkflowError


class TestWorkflowEngine(unittest.TestCase):
    """Tests for the WorkflowEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = Mock()
        self.executor = Mock()
        self.event_bus = Mock()
        self.action_resolver = Mock()

        self.engine = WorkflowEngine(
            validator=self.validator,
            executor=self.executor,
            event_bus=self.event_bus,
            action_resolver=self.action_resolver
        )

        # Create a sample workflow definition
        self.workflow = WorkflowDefinition(
            workflow_id="test-workflow",
            name="Test Workflow",
            description="A test workflow",
            actions=[
                {"id": "action1", "type": "test_action", "params": {"param1": "value1"}},
                {"id": "action2", "type": "test_action", "params": {"param2": "value2"}}
            ],
            connections=[
                {"source": "action1", "target": "action2"}
            ]
        )

        # Create a sample context
        self.context = {"var1": "value1", "var2": "value2"}

    def test_validate_workflow(self):
        """Test validating a workflow."""
        # Set up mock
        self.validator.validate.return_value = []

        # Call the method
        result = self.engine.validate_workflow(self.workflow)

        # Verify the result
        self.assertEqual(result, [])
        self.validator.validate.assert_called_once_with(self.workflow)
```

## Problematic Components

The following components have significant issues and need to be fixed or replaced. For each component, specific requirements are provided to guide the implementation.

### src/core/workflow/workflow_engine.py

**Created:** 2025-04-02 02:20:12
**Modified:** 2025-04-02 02:20:12
**Size:** 17167 bytes

**Issues:**

-   Missing implementation of abstract methods
-   Overly rigid validation rules
-   Doesn't handle different workflow structures
-   Caused the application to fail

**Specific Requirements:**

1. Implement all abstract methods from the interface
2. Make validation rules more flexible to handle different workflow structures
3. Properly handle error cases and provide meaningful error messages
4. Use dependency injection for all dependencies
5. Follow the pattern established in workflow_engine_new.py
6. Ensure all methods have proper unit tests

**Code:**

```python
"""Implementation of the workflow execution engine"""
import uuid
import logging
import threading
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Callable, Union, Set

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.context.execution_context import ExecutionContext
from src.core.context.execution_state import ExecutionStateEnum
from src.core.workflow.workflow_engine_interface import WorkflowEngineInterface
from src.core.workflow.workflow_event import (
    WorkflowEvent, WorkflowEventType, WorkflowStateEvent, ActionEvent, EventDispatcher
)
from src.core.workflow.workflow_statistics import WorkflowStatistics


class WorkflowStatus(Enum):
    """Status of a workflow"""
    PENDING = auto()    # Workflow is created but not started
    RUNNING = auto()    # Workflow is currently running
    PAUSED = auto()     # Workflow is paused
    COMPLETED = auto()  # Workflow completed successfully
    FAILED = auto()     # Workflow failed with an error
    ABORTED = auto()    # Workflow was manually aborted


class WorkflowEngine(WorkflowEngineInterface):
    """Engine for executing workflows"""

    def __init__(self):
        """Initialize the workflow engine"""
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._event_dispatcher = EventDispatcher()
        self._workflows: Dict[str, Dict[str, Any]] = {}
        self._running_workflows: Set[str] = set()
        self._paused_workflows: Set[str] = set()
        self._workflow_locks: Dict[str, threading.Lock] = {}
        self._statistics: Dict[str, WorkflowStatistics] = {}

    def execute_action(
        self,
        action: BaseAction,
        context: Union[ExecutionContext, Dict[str, Any]]
    ) -> ActionResult:
        """
        Execute a single action

        Args:
            action: Action to execute
            context: Execution context or context dictionary

        Returns:
            Result of the action execution
        """
        # Convert dictionary context to ExecutionContext if needed
        if isinstance(context, dict):
            execution_context = ExecutionContext()
            for key, value in context.items():
                execution_context.variables.set(key, value)
        else:
            execution_context = context

        # Create a context dictionary for the action
        action_context = execution_context.variables.get_all()

        # Execute the action
        self.logger.info(f"Executing action: {action.description}")
        result = action.execute(action_context)

        # Update the context with any new variables from the result
        if result.success and result.data:
            for key, value in result.data.items():
                execution_context.variables.set(key, value)

        return result

    def execute_workflow(
        self,
        actions: List[BaseAction],
        context: Optional[Union[ExecutionContext, Dict[str, Any]]] = None,
        workflow_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a sequence of actions as a workflow

        Args:
            actions: List of actions to execute
            context: Execution context or context dictionary (created if not provided)
            workflow_id: Optional workflow identifier (generated if not provided)

        Returns:
            Dictionary containing workflow execution results
        """
        # Generate workflow ID if not provided
        workflow_id = workflow_id or str(uuid.uuid4())

        # Create a lock for this workflow
        self._workflow_locks[workflow_id] = threading.Lock()

        # Create execution context if not provided
        if context is None:
            execution_context = ExecutionContext()
        elif isinstance(context, dict):
            execution_context = ExecutionContext()
            for key, value in context.items():
                execution_context.variables.set(key, value)
        else:
            execution_context = context

        # Initialize workflow state
        self._workflows[workflow_id] = {
            "id": workflow_id,
            "actions": actions,
            "context": execution_context,
            "current_index": 0,
            "status": WorkflowStatus.PENDING,
            "results": []
        }

        # Create statistics collector
        self._statistics[workflow_id] = WorkflowStatistics()

        # Start the workflow
        return self._run_workflow(workflow_id)

    def _run_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Run a workflow with the given ID

        Args:
            workflow_id: ID of the workflow to run

        Returns:
            Dictionary containing workflow execution results
        """
        if workflow_id not in self._workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")

        workflow = self._workflows[workflow_id]
        actions = workflow["actions"]
        context = workflow["context"]
        results = []

        # Mark workflow as running
        with self._workflow_locks[workflow_id]:
            workflow["status"] = WorkflowStatus.RUNNING
            self._running_workflows.add(workflow_id)

        # Transition context to running state
        context.state.transition_to(ExecutionStateEnum.RUNNING)

        # Dispatch workflow started event
        self._dispatch_workflow_event(
            WorkflowEventType.WORKFLOW_STARTED,
            workflow_id,
            {"total_actions": len(actions)}
        )

        # Execute each action in sequence
        success = True
        error_message = None

        for i, action in enumerate(actions):
            # Check if workflow should be paused or aborted
            with self._workflow_locks[workflow_id]:
                if workflow_id in self._paused_workflows:
                    # Workflow is paused, save current index and return
                    workflow["current_index"] = i
                    workflow["status"] = WorkflowStatus.PAUSED
                    return {
                        "workflow_id": workflow_id,
                        "success": None,
                        "message": "Workflow paused",
                        "results": results,
                        "completed": False
                    }

                if workflow_id not in self._running_workflows:
                    # Workflow was aborted
                    workflow["status"] = WorkflowStatus.ABORTED
                    context.state.transition_to(ExecutionStateEnum.ABORTED)
                    self._dispatch_workflow_event(
                        WorkflowEventType.WORKFLOW_ABORTED,
                        workflow_id
                    )
                    return {
                        "workflow_id": workflow_id,
                        "success": False,
                        "message": "Workflow aborted",
                        "results": results,
                        "completed": False
                    }

                # Update current index
                workflow["current_index"] = i

            # Dispatch action started event
            self._dispatch_action_event(
                WorkflowEventType.ACTION_STARTED,
                workflow_id,
                action,
                i
            )

            # Execute the action
            try:
                result = self.execute_action(action, context)
                results.append(result)

                if result.success:
                    # Dispatch action completed event
                    self._dispatch_action_event(
                        WorkflowEventType.ACTION_COMPLETED,
                        workflow_id,
                        action,
                        i,
                        result
                    )
                else:
                    # Action failed
                    success = False
                    error_message = f"Action failed: {result.message}"

                    # Dispatch action failed event
                    self._dispatch_action_event(
                        WorkflowEventType.ACTION_FAILED,
                        workflow_id,
                        action,
                        i,
                        result
                    )

                    # Stop execution on first failure
                    break
            except Exception as e:
                # Handle unexpected exceptions
                self.logger.error(f"Error executing action: {str(e)}", exc_info=True)
                success = False
                error_message = f"Error executing action: {str(e)}"

                # Create failure result
                failure_result = ActionResult.create_failure(str(e))
                results.append(failure_result)

                # Dispatch action failed event
                self._dispatch_action_event(
                    WorkflowEventType.ACTION_FAILED,
                    workflow_id,
                    action,
                    i,
                    failure_result
                )

                # Stop execution on exception
                break

        # Update workflow status and context state
        with self._workflow_locks[workflow_id]:
            if success:
                workflow["status"] = WorkflowStatus.COMPLETED
                context.state.transition_to(ExecutionStateEnum.COMPLETED)
                self._dispatch_workflow_event(
                    WorkflowEventType.WORKFLOW_COMPLETED,
                    workflow_id
                )
            else:
                workflow["status"] = WorkflowStatus.FAILED
                context.state.transition_to(ExecutionStateEnum.FAILED)
                self._dispatch_workflow_event(
                    WorkflowEventType.WORKFLOW_FAILED,
                    workflow_id,
                    {"error": error_message}
                )

            # Store results
            workflow["results"] = results

            # Remove from running workflows
            if workflow_id in self._running_workflows:
                self._running_workflows.remove(workflow_id)

        # Return workflow results
        return {
            "workflow_id": workflow_id,
            "success": success,
            "message": "Workflow completed successfully" if success else error_message,
            "results": results,
            "completed": True
        }

    def pause_workflow(self, workflow_id: str) -> bool:
        """
        Pause a running workflow

        Args:
            workflow_id: ID of the workflow to pause

        Returns:
            True if the workflow was paused, False otherwise
        """
        if workflow_id not in self._workflows:
            return False

        with self._workflow_locks[workflow_id]:
            if workflow_id not in self._running_workflows:
                return False

            self._paused_workflows.add(workflow_id)
            self._dispatch_workflow_event(
                WorkflowEventType.WORKFLOW_PAUSED,
                workflow_id
            )
            return True

    def resume_workflow(self, workflow_id: str) -> bool:
        """
        Resume a paused workflow

        Args:
            workflow_id: ID of the workflow to resume

        Returns:
            True if the workflow was resumed, False otherwise
        """
        if workflow_id not in self._workflows:
            return False

        with self._workflow_locks[workflow_id]:
            if workflow_id not in self._paused_workflows:
                return False

            self._paused_workflows.remove(workflow_id)
            self._running_workflows.add(workflow_id)
            self._dispatch_workflow_event(
                WorkflowEventType.WORKFLOW_RESUMED,
                workflow_id
            )

        # Continue execution in a new thread
        threading.Thread(
            target=self._run_workflow,
            args=(workflow_id,),
            daemon=True
        ).start()

        return True

    def abort_workflow(self, workflow_id: str) -> bool:
        """
        Abort a running or paused workflow

        Args:
            workflow_id: ID of the workflow to abort

        Returns:
            True if the workflow was aborted, False otherwise
        """
        if workflow_id not in self._workflows:
            return False

        with self._workflow_locks[workflow_id]:
            if (
                workflow_id not in self._running_workflows
                and workflow_id not in self._paused_workflows
            ):
                return False

            # Remove from running and paused workflows
            if workflow_id in self._running_workflows:
                self._running_workflows.remove(workflow_id)
            if workflow_id in self._paused_workflows:
                self._paused_workflows.remove(workflow_id)

            # Update workflow status
            workflow = self._workflows[workflow_id]
            workflow["status"] = WorkflowStatus.ABORTED

            # Update context state
            context = workflow["context"]
            context.state.transition_to(ExecutionStateEnum.ABORTED)

            # Dispatch workflow aborted event
            self._dispatch_workflow_event(
                WorkflowEventType.WORKFLOW_ABORTED,
                workflow_id
            )

            return True

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            Dictionary containing workflow status or None if not found
        """
        if workflow_id not in self._workflows:
            return None

        workflow = self._workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "status": workflow["status"].name,
            "current_index": workflow["current_index"],
            "total_actions": len(workflow["actions"]),
            "completed_actions": min(workflow["current_index"], len(workflow["actions"])),
            "context_state": workflow["context"].state.current_state.name
        }

    def get_workflow_statistics(self, workflow_id: str) -> Optional[WorkflowStatistics]:
        """
        Get statistics for a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            WorkflowStatistics object or None if not found
        """
        return self._statistics.get(workflow_id)

    def add_event_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """
        Add a listener for workflow events

        Args:
            event_type: Type of event to listen for, or None for all events
            listener: Callback function that will be called when events occur
        """
        self._event_dispatcher.add_listener(event_type, listener)

    def remove_event_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """
        Remove an event listener

        Args:
            event_type: Type of event the listener was registered for, or None for all events
            listener: Listener to remove
        """
        self._event_dispatcher.remove_listener(event_type, listener)

    def _dispatch_workflow_event(
        self,
        event_type: WorkflowEventType,
        workflow_id: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Dispatch a workflow state event

        Args:
            event_type: Type of the event
            workflow_id: ID of the workflow
            data: Additional event data
        """
        event = WorkflowStateEvent(event_type, workflow_id, data=data)
        self._event_dispatcher.dispatch(event)

        # Record event in statistics
        if workflow_id in self._statistics:
            self._statistics[workflow_id].record_event(event)

    def _dispatch_action_event(
        self,
        event_type: WorkflowEventType,
        workflow_id: str,
        action: BaseAction,
        action_index: int,
        result: Optional[ActionResult] = None
    ) -> None:
        """
        Dispatch an action event

        Args:
            event_type: Type of the event
            workflow_id: ID of the workflow
            action: The action that was executed
            action_index: Index of the action in the workflow
            result: Result of the action execution (for completed/failed events)
        """
        event = ActionEvent(event_type, workflow_id, action, action_index, result)
        self._event_dispatcher.dispatch(event)

        # Record event in statistics
        if workflow_id in self._statistics:
            self._statistics[workflow_id].record_event(event)

```

### src/core/workflow/engine/workflow_validator.py

**Created:** 2025-04-02 19:43:52
**Modified:** 2025-04-02 20:21:18
**Size:** 3738 bytes

**Issues:**

-   Too strict validation rules (requiring End nodes)
-   Doesn't handle different workflow structures
-   Not flexible enough for real-world use
-   Creates poor user experience

**Code:**

```python
"""
Workflow validator implementation.

This module contains the implementation of the workflow validator.

SRP-1: Provides workflow validator implementation
"""
from typing import Dict, Any, List, Optional, Set

from src.core.utils.logging import LoggingMixin
from src.core.utils.error_handling import ErrorHandlingMixin
from src.core.workflow.interfaces import IWorkflowValidator, WorkflowDefinition


class WorkflowValidator(ErrorHandlingMixin, IWorkflowValidator):
    """Implementation of the workflow validator."""

    def __init__(self):
        """Initialize the workflow validator."""
        # Initialize logger
        self.__init_logger__()

        # Log initialization
        self.log_info(f"Initialized {self.__class__.__name__}")

    def validate(self, workflow: WorkflowDefinition) -> List[str]:
        """
        Validate a workflow.

        Args:
            workflow: Workflow to validate

        Returns:
            List of validation errors, empty if valid
        """
        errors = []

        # Validate workflow ID
        if not workflow.workflow_id:
            errors.append("Workflow ID is required")

        # Validate workflow name
        if not workflow.name:
            errors.append("Workflow name is required")

        # Validate nodes
        if not workflow.nodes:
            errors.append("Workflow must have at least one node")
        else:
            # Validate start node
            if not any(node.type == "Start" for node in workflow.nodes.values()):
                errors.append("Workflow must have a start node")

            # Validate end node
            if not any(node.type == "End" for node in workflow.nodes.values()):
                errors.append("Workflow must have an end node")

            # Validate node connections
            errors.extend(self._validate_connections(workflow))

        return errors

    def _validate_connections(self, workflow: WorkflowDefinition) -> List[str]:
        """
        Validate workflow connections.

        Args:
            workflow: Workflow to validate

        Returns:
            List of validation errors, empty if valid
        """
        errors = []

        # Get all node IDs
        node_ids = set(workflow.nodes.keys())

        # Get all connected node IDs
        connected_nodes = set()

        # Validate connections
        for connection_id, connection in workflow.connections.items():
            # Validate source node
            if connection.source_node_id not in node_ids:
                errors.append(f"Connection {connection_id} references non-existent source node {connection.source_node_id}")
            else:
                connected_nodes.add(connection.source_node_id)

            # Validate target node
            if connection.target_node_id not in node_ids:
                errors.append(f"Connection {connection_id} references non-existent target node {connection.target_node_id}")
            else:
                connected_nodes.add(connection.target_node_id)

        # Check for disconnected nodes
        disconnected_nodes = node_ids - connected_nodes

        # Exclude start nodes from disconnected nodes check
        disconnected_nodes = {node_id for node_id in disconnected_nodes
                             if workflow.nodes[node_id].type != "Start"}

        # Exclude end nodes from disconnected nodes check
        disconnected_nodes = {node_id for node_id in disconnected_nodes
                             if workflow.nodes[node_id].type != "End"}

        # Add errors for disconnected nodes
        if disconnected_nodes:
            for node_id in disconnected_nodes:
                errors.append(f"Node {node_id} is disconnected")

        return errors

```

### src/core/workflow/workflow_engine_interface.py

**Created:** 2025-03-28 06:38:08
**Modified:** 2025-03-28 06:38:08
**Size:** 4119 bytes

**Issues:**

-   Too complex with too many responsibilities
-   Violates Interface Segregation Principle
-   Has methods that aren't needed in all implementations
-   Led to implementation difficulties

**Code:**

```python
"""Interface for workflow execution engines"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable, Union

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.context.execution_context import ExecutionContext
from src.core.workflow.workflow_event import WorkflowEvent, WorkflowEventType
from src.core.workflow.workflow_statistics import WorkflowStatistics


class WorkflowEngineInterface(ABC):
    """Interface for workflow execution engines"""

    @abstractmethod
    def execute_action(
        self,
        action: BaseAction,
        context: Union[ExecutionContext, Dict[str, Any]]
    ) -> ActionResult:
        """
        Execute a single action

        Args:
            action: Action to execute
            context: Execution context or context dictionary

        Returns:
            Result of the action execution
        """
        pass

    @abstractmethod
    def execute_workflow(
        self,
        actions: List[BaseAction],
        context: Optional[Union[ExecutionContext, Dict[str, Any]]] = None,
        workflow_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a sequence of actions as a workflow

        Args:
            actions: List of actions to execute
            context: Execution context or context dictionary (created if not provided)
            workflow_id: Optional workflow identifier (generated if not provided)

        Returns:
            Dictionary containing workflow execution results
        """
        pass

    @abstractmethod
    def pause_workflow(self, workflow_id: str) -> bool:
        """
        Pause a running workflow

        Args:
            workflow_id: ID of the workflow to pause

        Returns:
            True if the workflow was paused, False otherwise
        """
        pass

    @abstractmethod
    def resume_workflow(self, workflow_id: str) -> bool:
        """
        Resume a paused workflow

        Args:
            workflow_id: ID of the workflow to resume

        Returns:
            True if the workflow was resumed, False otherwise
        """
        pass

    @abstractmethod
    def abort_workflow(self, workflow_id: str) -> bool:
        """
        Abort a running or paused workflow

        Args:
            workflow_id: ID of the workflow to abort

        Returns:
            True if the workflow was aborted, False otherwise
        """
        pass

    @abstractmethod
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            Dictionary containing workflow status or None if not found
        """
        pass

    @abstractmethod
    def get_workflow_statistics(self, workflow_id: str) -> Optional[WorkflowStatistics]:
        """
        Get statistics for a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            WorkflowStatistics object or None if not found
        """
        pass

    @abstractmethod
    def add_event_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """
        Add a listener for workflow events

        Args:
            event_type: Type of event to listen for, or None for all events
            listener: Callback function that will be called when events occur
        """
        pass

    @abstractmethod
    def remove_event_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """
        Remove an event listener

        Args:
            event_type: Type of event the listener was registered for, or None for all events
            listener: Listener to remove
        """
        pass

```

### src/core/workflow/workflow_validation_service.py

**Created:** 2025-04-01 05:32:52
**Modified:** 2025-04-03 15:35:45
**Size:** 6132 bytes

**Issues:**

-   Duplicates functionality already in the validator
-   Not properly integrated with the architecture
-   Creates confusion about where validation logic should live
-   Adds complexity without clear benefits

**Code:**

```python
"""
Workflow validation service.
SOLID: Single responsibility - workflow validation logic.
KISS: Simple validation methods.
"""
from typing import List, Dict, Set
from src.core.models import Workflow, WorkflowNode, WorkflowConnection

class WorkflowValidationError(Exception):
    """Exception raised when a workflow fails validation."""
    pass

class WorkflowValidationService:
    """Service for validating workflows."""

    def validate_workflow(self, workflow: Workflow) -> None:
        """
        Validate a workflow.

        Args:
            workflow: Workflow to validate

        Raises:
            WorkflowValidationError: If the workflow is invalid
        """
        errors = []

        # Check for required fields
        if not workflow.id:
            errors.append("Workflow ID is required")
        if not workflow.name:
            errors.append("Workflow name is required")

        # Check for start and end nodes
        start_nodes = [node for node in workflow.nodes.values() if node.type == "Start"]
        if not start_nodes:
            errors.append("Workflow must have at least one Start node")
        elif len(start_nodes) > 1:
            errors.append("Workflow must have only one Start node")

        # End node check is now a warning, not an error
        end_nodes = [node for node in workflow.nodes.values() if node.type == "End"]
        if not end_nodes:
            # Only warn about missing End node if there are more than just a Start node
            # This allows new workflows with just a Start node to be created
            if len(workflow.nodes) > 1:
                errors.append("Warning: Workflow should have at least one End node for proper execution")

        # Check for cycles
        try:
            self._detect_cycles(workflow)
        except WorkflowValidationError as e:
            errors.append(str(e))

        # Check for disconnected nodes
        disconnected = self._find_disconnected_nodes(workflow)
        if disconnected:
            node_names = ", ".join([f"{node.type} ({node.id})" for node in disconnected])
            errors.append(f"Workflow contains disconnected nodes: {node_names}")

        # Check for invalid connections
        for conn_id, conn in workflow.connections.items():
            # Check that source and target nodes exist
            if conn.source_node_id not in workflow.nodes:
                errors.append(f"Connection {conn_id} references non-existent source node {conn.source_node_id}")
            if conn.target_node_id not in workflow.nodes:
                errors.append(f"Connection {conn_id} references non-existent target node {conn.target_node_id}")

        # If there are any errors, raise an exception
        if errors:
            raise WorkflowValidationError("Workflow validation failed: " + "; ".join(errors))


    def _detect_cycles(self, workflow: Workflow) -> None:
        """
        Detect cycles in a workflow.

        Args:
            workflow: Workflow to check

        Raises:
            WorkflowValidationError: If a cycle is detected
        """
        # Build adjacency list
        adjacency: Dict[str, List[str]] = {node_id: [] for node_id in workflow.nodes}
        for conn in workflow.connections.values():
            if conn.source_node_id in adjacency:
                adjacency[conn.source_node_id].append(conn.target_node_id)

        # Track visited and recursion stack
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node_id: str) -> bool:
            """Depth-first search to detect cycles."""
            visited.add(node_id)

            rec_stack.add(node_id)

            for neighbor in adjacency.get(node_id, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node_id)
            return False
        # Check each node
        for node_id in workflow.nodes:
            if node_id not in visited:
                if dfs(node_id):
                    raise WorkflowValidationError("Workflow contains a cycle")


    def _find_disconnected_nodes(self, workflow: Workflow) -> List[WorkflowNode]:
        """
        Find nodes that are not reachable from any Start node.

        Args:
            workflow: Workflow to check

        Returns:
            List of disconnected nodes
        """
        if not workflow.nodes:
            return []

        start_nodes = [node.id for node in workflow.nodes.values() if node.type == "Start"]
        if not start_nodes:
            # If no start node, consider all nodes disconnected (though validation should catch this earlier)
            return list(workflow.nodes.values())

        # Build adjacency list (source -> list of targets)
        adjacency: Dict[str, List[str]] = {node_id: [] for node_id in workflow.nodes}
        for conn in workflow.connections.values():
            if conn.source_node_id in adjacency:
                adjacency[conn.source_node_id].append(conn.target_node_id)

        # Perform BFS from all start nodes to find reachable nodes
        reachable: Set[str] = set()
        queue: List[str] = start_nodes[:] # Start queue with all start nodes

        for start_node_id in start_nodes:
             reachable.add(start_node_id) # Start nodes are reachable

        head = 0
        while head < len(queue):
            current_node_id = queue[head]
            head += 1

            for neighbor_id in adjacency.get(current_node_id, []):
                if neighbor_id not in reachable:
                    reachable.add(neighbor_id)
                    queue.append(neighbor_id)

        # Return nodes that are not in the reachable set
        disconnected_nodes = [
            node for node_id, node in workflow.nodes.items() if node_id not in reachable
        ]
        return disconnected_nodes
```

### src/ui/views/workflow_view.py

**Created:** 2025-04-02 02:20:12
**Modified:** 2025-04-02 02:20:12
**Size:** 51582 bytes

**Issues:**

-   Direct dependencies on workflow service implementation
-   Mixes presentation and business logic
-   Complex event handling that's difficult to test
-   Tightly coupled to specific UI framework

**Code:**

```python
﻿"""

Workflow Builder View for creating and editing workflows.

SOLID: Single responsibility - UI for workflow building.

KISS: Simple canvas-based interface with intuitive interactions.

"""

print("DEBUG: workflow_view.py is being loaded!")

import customtkinter as ctk

import tkinter as tk

from tkinter import simpledialog, filedialog, messagebox

from typing import Dict, List, Any, Optional, TYPE_CHECKING, Tuple, Set, Callable



from ..views.base_view import BaseView

from ..utils.constants import (

    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,

    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER

)

from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

from ..components.context_menu import ContextMenu



if TYPE_CHECKING:

    from ..presenters.workflow_presenter import WorkflowPresenter



class WorkflowView(BaseView):

    """View for building and editing workflows."""



    # Type hint for the presenter

    presenter: 'WorkflowPresenter'



    def __init__(self, master, **kwargs):

        """Initialize the workflow view."""

        super().__init__(master, **kwargs)

        self.selected_node_id = None  # Currently selected node

        self.selected_node_type = None  # Currently selected node type for adding

        self.node_elements = {}  # Dictionary of node canvas elements

        self.connection_elements = {}  # Dictionary of connection canvas elements

        self.properties_editors = {}  # Dictionary of property editors

        self.canvas_scale = 1.0  # Canvas zoom level

        self.canvas_offset = (0, 0)  # Canvas pan offset

        self.workflow_name_var = tk.StringVar(value="Untitled Workflow")

        self.is_connecting = False  # Flag for connection creation mode

        self.connection_start = None  # Starting node/port for connection



        # Drag and drop variables

        self.is_dragging = False  # Flag for node dragging from toolbox

        self.drag_data = {"x": 0, "y": 0, "node_type": None}  # Data for dragging

        self.drag_icon = None  # Visual representation of dragged node





        # Context menus

        self.node_context_menu = None

        self.connection_context_menu = None

        self.canvas_context_menu = None







    def _create_widgets(self):

        """Create the UI widgets."""

        # Main layout - split into toolbar, toolbox, canvas, and properties

        self.grid_columnconfigure(0, weight=0)  # Toolbox
        self.grid_columnconfigure(1, weight=1)  # Canvas
        self.grid_columnconfigure(2, weight=0)  # Properties
        self.grid_rowconfigure(0, weight=0)  # Toolbar
        self.grid_rowconfigure(1, weight=1)  # Main content

        # Debug grid configuration
        print("DEBUG: WorkflowView grid configured")
        print(f"DEBUG: Grid rowconfigure: {self.grid_size()[1]} rows")
        print(f"DEBUG: Grid columnconfigure: {self.grid_size()[0]} columns")



        # === Toolbar ===

        self.toolbar_frame = ctk.CTkFrame(self)

        self.toolbar_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.toolbar_frame.grid_columnconfigure(0, weight=0)

        self.toolbar_frame.grid_columnconfigure(1, weight=1)

        self.toolbar_frame.grid_columnconfigure(2, weight=0)



        # Workflow name

        self.name_label = ctk.CTkLabel(self.toolbar_frame, text="Workflow Name:", font=get_default_font())

        self.name_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.name_entry = ctk.CTkEntry(self.toolbar_frame, textvariable=self.workflow_name_var, width=200)

        self.name_entry.grid(row=0, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        # Toolbar buttons

        self.toolbar_buttons_frame = ctk.CTkFrame(self.toolbar_frame)

        self.toolbar_buttons_frame.grid(row=0, column=2, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.new_button = ctk.CTkButton(

            self.toolbar_buttons_frame, text="New", width=80, command=self._on_new_clicked

        )

        self.new_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.open_button = ctk.CTkButton(

            self.toolbar_buttons_frame, text="Open", width=80, command=self._on_open_clicked

        )

        self.open_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.save_button = ctk.CTkButton(

            self.toolbar_buttons_frame, text="Save", width=80, command=self._on_save_clicked

        )

        self.save_button.grid(row=0, column=2, padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.execute_button = ctk.CTkButton(

            self.toolbar_buttons_frame, text="Execute", width=80, command=self._on_execute_clicked

        )

        self.execute_button.grid(row=0, column=3, padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.validate_button = ctk.CTkButton(

            self.toolbar_buttons_frame, text="Validate", width=80, command=self._on_validate_clicked

        )

        self.validate_button.grid(row=0, column=4, padx=PAD_X_INNER, pady=PAD_Y_INNER)



        # === Toolbox ===

        self.toolbox_frame = ctk.CTkFrame(self)

        self.toolbox_frame.grid(row=1, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.toolbox_label = ctk.CTkLabel(

            self.toolbox_frame, text="Node Types", font=get_header_font()

        )

        self.toolbox_label.grid(row=0, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.node_buttons_frame = ctk.CTkScrollableFrame(self.toolbox_frame, width=150, height=500)

        self.node_buttons_frame.grid(row=1, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.node_buttons = {}  # Will be populated in initialize_toolbox



        # === Canvas ===
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=1, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)

        # Debug canvas frame
        print("DEBUG: Canvas frame created")
        print(f"DEBUG: Canvas frame grid position: row=1, column=1")
        print(f"DEBUG: Canvas frame visible: {self.canvas_frame.winfo_viewable()}")

        # Force update to ensure frame is drawn
        self.canvas_frame.update()



        self.canvas = tk.Canvas(
            self.canvas_frame, bg="#2B2B2B", width=800, height=600,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Debug canvas creation
        print("DEBUG: Canvas created")
        print(f"DEBUG: Canvas dimensions: {self.canvas.winfo_width()}x{self.canvas.winfo_height()}")
        print(f"DEBUG: Canvas grid position: row=0, column=0")
        print(f"DEBUG: Canvas visible: {self.canvas.winfo_viewable()}")

        # Force update to ensure canvas is drawn
        self.canvas.update()



        # Canvas scrollbars

        self.canvas_x_scrollbar = ctk.CTkScrollbar(

            self.canvas_frame, orientation="horizontal", command=self.canvas.xview

        )

        self.canvas_x_scrollbar.grid(row=1, column=0, sticky="ew")



        self.canvas_y_scrollbar = ctk.CTkScrollbar(

            self.canvas_frame, orientation="vertical", command=self.canvas.yview

        )

        self.canvas_y_scrollbar.grid(row=0, column=1, sticky="ns")



        self.canvas.configure(

            xscrollcommand=self.canvas_x_scrollbar.set,

            yscrollcommand=self.canvas_y_scrollbar.set,

            scrollregion=(0, 0, 1500, 1000)

        )



        # Canvas event bindings
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)

        # Bind middle mouse button for panning
        self.canvas.bind("<Button-2>", self._on_canvas_middle_click)
        self.canvas.bind("<B2-Motion>", self._on_canvas_middle_drag)
        self.canvas.bind("<ButtonRelease-2>", self._on_canvas_middle_release)

        # Bind mousewheel for zooming
        self.canvas.bind("<MouseWheel>", self._on_canvas_scroll)  # Windows/macOS
        self.canvas.bind("<Button-4>", self._on_canvas_scroll)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_canvas_scroll)  # Linux scroll down



        # === Properties Panel ===

        self.properties_frame = ctk.CTkFrame(self)

        self.properties_frame.grid(row=1, column=2, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.properties_label = ctk.CTkLabel(

            self.properties_frame, text="Properties", font=get_header_font()

        )

        self.properties_label.grid(row=0, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.properties_scroll_frame = ctk.CTkScrollableFrame(self.properties_frame, width=250, height=500)

        self.properties_scroll_frame.grid(row=1, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        # Properties buttons

        self.properties_buttons_frame = ctk.CTkFrame(self.properties_frame)

        self.properties_buttons_frame.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.properties_save_button = ctk.CTkButton(

            self.properties_buttons_frame, text="Apply", command=self._on_properties_save

        )

        self.properties_save_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)



        self.node_delete_button = ctk.CTkButton(

            self.properties_buttons_frame, text="Delete Node", command=self._on_node_delete

        )

        self.node_delete_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)



    def _setup_layout(self):

        """Set up the layout grid."""

        # Main layout already set up in _create_widgets
        print("DEBUG: WorkflowView._setup_layout() called")

        # Note: Context menus are created in build_ui to avoid duplication
        print("DEBUG: WorkflowView._setup_layout() completed")



    def build_ui(self):

        """Override build_ui to also create context menus."""

        print("DEBUG: WorkflowView.build_ui() called")
        # Call the parent class's build_ui method

        super().build_ui()
        print("DEBUG: WorkflowView.build_ui() - super().build_ui() completed")


        # Create context menus
        print("DEBUG: WorkflowView.build_ui() - creating context menus")

        self._create_context_menus()
        print("DEBUG: WorkflowView.build_ui() - context menus created")


        print("DEBUG: WorkflowView.build_ui() completed")

        # Force update to ensure view is drawn
        self.update()
        print(f"DEBUG: WorkflowView dimensions after build: {self.winfo_width()}x{self.winfo_height()}")
        print(f"DEBUG: WorkflowView visible after build: {self.winfo_viewable()}")





    def initialize_canvas(self):

        """Initialize the canvas for workflow editing."""
        print("DEBUG: Initializing canvas")

        # Set up canvas properties

        self.canvas.config(width=800, height=600)

        self.canvas_scale = 1.0

        self.canvas_offset = (0, 0)

        # Draw grid lines
        print("DEBUG: Drawing grid")

        self._draw_grid()
        print("DEBUG: Grid drawn")

        # Debug canvas state
        print(f"DEBUG: Canvas dimensions: {self.canvas.winfo_width()}x{self.canvas.winfo_height()}")
        print(f"DEBUG: Canvas visible: {self.canvas.winfo_viewable()}")
        print(f"DEBUG: Canvas frame dimensions: {self.canvas_frame.winfo_width()}x{self.canvas_frame.winfo_height()}")
        print(f"DEBUG: Canvas frame visible: {self.canvas_frame.winfo_viewable()}")
        print("DEBUG: Canvas initialization complete")



    def initialize_toolbox(self, node_types: List[Dict[str, Any]]):

        """

        Initialize the toolbox with node types.



        Args:

            node_types: List of node types with metadata

        """

        # Clear existing buttons

        for widget in self.node_buttons_frame.winfo_children():

            widget.destroy()



        self.node_buttons = {}



        # Create buttons for each node type

        for i, node_type in enumerate(node_types):

            button = ctk.CTkButton(

                self.node_buttons_frame,

                text=node_type["name"],

                command=lambda t=node_type["type"]: self._on_node_type_selected(t)

            )

            button.grid(row=i*2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)



            # Add tooltip

            tooltip = ctk.CTkLabel(

                self.node_buttons_frame,

                text=node_type["description"],

                font=get_small_font(),

                text_color="gray",

                wraplength=140

            )

            tooltip.grid(row=i*2+1, column=0, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))



            # Store node type data with the button for drag and drop

            button.node_type = node_type["type"]

            button.node_name = node_type["name"]



            # Add drag and drop event bindings

            button.bind("<Button-1>", self._on_toolbox_button_press)

            button.bind("<B1-Motion>", self._on_toolbox_button_drag)

            button.bind("<ButtonRelease-1>", self._on_toolbox_button_release)



            self.node_buttons[node_type["type"]] = button



    def clear_canvas(self):

        """Clear the canvas."""

        # Delete all canvas items

        self.canvas.delete("all")



        # Reset node and connection elements

        self.node_elements = {}

        self.connection_elements = {}



        # Draw grid lines

        self._draw_grid()



    def redraw_workflow(self, workflow: Optional[Any]):

        """

        Redraw the entire workflow.



        Args:

            workflow: Workflow to draw

        """
        print("DEBUG: WorkflowView.redraw_workflow() called")

        if not workflow:
            print("DEBUG: No workflow provided to redraw_workflow()")
            return

        print(f"DEBUG: Redrawing workflow with {len(workflow.nodes)} nodes and {len(workflow.connections)} connections")

        # Clear the canvas
        print("DEBUG: Clearing canvas...")
        self.clear_canvas()
        print("DEBUG: Canvas cleared")


        # Draw all nodes
        print("DEBUG: Drawing nodes...")
        for node_id, node in workflow.nodes.items():
            print(f"DEBUG: Drawing node {node_id} of type {node.type} at position {node.position}")
            self.draw_node(node)
        print("DEBUG: All nodes drawn")


        # Draw all connections
        print("DEBUG: Drawing connections...")
        for conn_id, conn in workflow.connections.items():
            print(f"DEBUG: Drawing connection {conn_id} from {conn.source_node_id} to {conn.target_node_id}")
            self.draw_connection(conn)
        print("DEBUG: All connections drawn")

        # Debug canvas state after redraw
        print(f"DEBUG: Canvas dimensions after redraw: {self.canvas.winfo_width()}x{self.canvas.winfo_height()}")
        print(f"DEBUG: Canvas visible after redraw: {self.canvas.winfo_viewable()}")
        print(f"DEBUG: Canvas frame dimensions after redraw: {self.canvas_frame.winfo_width()}x{self.canvas_frame.winfo_height()}")
        print(f"DEBUG: Canvas frame visible after redraw: {self.canvas_frame.winfo_viewable()}")

        # Force update to ensure canvas is drawn
        self.canvas.update()
        self.canvas_frame.update()
        self.update()

        print("DEBUG: WorkflowView.redraw_workflow() completed")



    def draw_node(self, node: Any):

        """

        Draw a node on the canvas.



        Args:

            node: Node to draw

        """
        print(f"DEBUG: Drawing node {node.id} of type {node.type}")

        # Node dimensions
        width = 120
        height = 60

        # Get node position in world coordinates
        world_x, world_y = node.position
        print(f"DEBUG: Node world position: ({world_x}, {world_y})")

        # Convert to screen coordinates
        x, y = self.world_to_screen(world_x, world_y)
        print(f"DEBUG: Node screen position: ({x}, {y})")


        # Node colors based on type

        colors = {

            "Start": "#4CAF50",  # Green

            "End": "#F44336",    # Red

            "Click": "#2196F3",  # Blue

            "Type": "#9C27B0",   # Purple

            "Wait": "#FF9800",   # Orange

            "Condition": "#FFEB3B",  # Yellow

            "Loop": "#795548"    # Brown

        }



        color = colors.get(node.type, "#607D8B")  # Default to gray
        print(f"DEBUG: Node color: {color}")


        # Draw node body
        print("DEBUG: Drawing node body...")
        body = self.canvas.create_rectangle(

            x - width/2, y - height/2, x + width/2, y + height/2,

            fill=color, outline="#FFFFFF", width=2,

            tags=(f"node_{node.id}", "body")

        )
        print(f"DEBUG: Node body created with ID: {body}")


        # Draw node label
        print("DEBUG: Drawing node label...")
        label = self.canvas.create_text(

            x, y, text=node.label or node.type,

            fill="#FFFFFF", font=("Arial", 12, "bold"),

            tags=(f"node_{node.id}", "label")

        )
        print(f"DEBUG: Node label created with ID: {label}")


        # Draw input port
        print("DEBUG: Drawing input port...")
        input_port = self.canvas.create_oval(

            x - 5, y - height/2 - 5, x + 5, y - height/2 + 5,

            fill="#FFFFFF", outline="#000000",

            tags=(f"node_{node.id}", "input_port")

        )
        print(f"DEBUG: Input port created with ID: {input_port}")


        # Draw output port
        print("DEBUG: Drawing output port...")
        output_port = self.canvas.create_oval(

            x - 5, y + height/2 - 5, x + 5, y + height/2 + 5,

            fill="#FFFFFF", outline="#000000",

            tags=(f"node_{node.id}", "output_port")

        )
        print(f"DEBUG: Output port created with ID: {output_port}")


        # Store node elements
        print("DEBUG: Storing node elements...")
        self.node_elements[node.id] = {

            "body": body,

            "label": label,

            "input_port": input_port,

            "output_port": output_port,

            "world_position": (world_x, world_y),  # Store world position
            "screen_position": (x, y),  # Store screen position

            "width": width,

            "height": height

        }
        print(f"DEBUG: Node elements stored for node {node.id}")


        # Add event bindings
        print("DEBUG: Adding event bindings...")
        self.canvas.tag_bind(f"node_{node.id}", "<Button-1>", self._on_node_click)

        self.canvas.tag_bind(f"node_{node.id}", "<B1-Motion>", self._on_node_drag)

        self.canvas.tag_bind(f"node_{node.id}", "<ButtonRelease-1>", self._on_node_release)
        print("DEBUG: Event bindings added")

        print(f"DEBUG: Node {node.id} drawing completed")



    def draw_connection(self, connection: Any):

        """

        Draw a connection on the canvas.



        Args:

            connection: Connection to draw

        """

        # Get source and target nodes

        if connection.source_node_id not in self.node_elements or connection.target_node_id not in self.node_elements:

            return



        source_node = self.node_elements[connection.source_node_id]

        target_node = self.node_elements[connection.target_node_id]



        # Get port positions
        if connection.source_port == "output":
            source_x, source_y = source_node["screen_position"][0], source_node["screen_position"][1] + source_node["height"]/2
        else:
            source_x, source_y = source_node["screen_position"]

        if connection.target_port == "input":
            target_x, target_y = target_node["screen_position"][0], target_node["screen_position"][1] - target_node["height"]/2
        else:
            target_x, target_y = target_node["screen_position"]



        # Calculate control points for bezier curve

        control1_x, control1_y = source_x, source_y + 50

        control2_x, control2_y = target_x, target_y - 50



        # Draw connection line

        line = self.canvas.create_line(

            source_x, source_y, control1_x, control1_y, control2_x, control2_y, target_x, target_y,

            fill="#FFFFFF", width=2, smooth=True, splinesteps=20,

            tags=(f"connection_{connection.id}",)

        )



        # Draw arrow

        arrow_size = 8

        arrow = self.canvas.create_polygon(

            target_x - arrow_size, target_y - arrow_size,

            target_x, target_y,

            target_x - arrow_size, target_y + arrow_size,

            fill="#FFFFFF", outline="#FFFFFF",

            tags=(f"connection_{connection.id}", "arrow")

        )



        # Store connection elements

        self.connection_elements[connection.id] = line



        # Add event bindings

        self.canvas.tag_bind(f"connection_{connection.id}", "<Button-1>", self._on_connection_click)



    def select_node_visual(self, node_id: Optional[str]):

        """

        Visually select a node on the canvas.



        Args:

            node_id: ID of the node to select, or None to deselect

        """

        # Reset all node highlights

        for nid, elements in self.node_elements.items():

            self.canvas.itemconfig(elements["body"], width=2)



        # Highlight the selected node

        if node_id and node_id in self.node_elements:

            self.canvas.itemconfig(self.node_elements[node_id]["body"], width=4)

            self.selected_node_id = node_id

        else:

            self.selected_node_id = None



    def display_properties_for_node(self, node_data: Optional[Any]):

        """

        Display properties for a node in the properties panel.



        Args:

            node_data: Node data to display

        """

        # Clear existing property editors

        for widget in self.properties_scroll_frame.winfo_children():

            widget.destroy()



        self.properties_editors = {}



        if not node_data:

            return



        # Display node type

        type_label = ctk.CTkLabel(

            self.properties_scroll_frame, text=f"Type: {node_data.type}",

            font=get_default_font()

        )

        type_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        # Display node ID

        id_label = ctk.CTkLabel(

            self.properties_scroll_frame, text=f"ID: {node_data.id}",

            font=get_small_font(), text_color="gray"

        )

        id_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))



        # Display node label editor

        label_label = ctk.CTkLabel(

            self.properties_scroll_frame, text="Label:",

            font=get_default_font()

        )

        label_label.grid(row=2, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)



        label_entry = ctk.CTkEntry(self.properties_scroll_frame)

        label_entry.grid(row=2, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        label_entry.insert(0, node_data.label or "")

        self.properties_editors["label"] = label_entry



        # Display node properties

        row = 3

        for prop_name, prop_value in node_data.properties.items():

            prop_label = ctk.CTkLabel(

                self.properties_scroll_frame, text=f"{prop_name.replace('_', ' ').title()}:",

                font=get_default_font()

            )

            prop_label.grid(row=row, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)



            prop_entry = ctk.CTkEntry(self.properties_scroll_frame)

            prop_entry.grid(row=row, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

            prop_entry.insert(0, str(prop_value))

            self.properties_editors[prop_name] = prop_entry



            row += 1



        # Add property button

        add_prop_button = ctk.CTkButton(

            self.properties_scroll_frame, text="Add Property",

            command=self._on_add_property

        )

        add_prop_button.grid(row=row, column=0, columnspan=2, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)



    def get_properties_data(self) -> Optional[Dict]:

        """

        Get the data from the properties panel.



        Returns:

            Dictionary containing the property data

        """

        if not self.properties_editors:

            return None



        data = {}



        for prop_name, editor in self.properties_editors.items():

            data[prop_name] = editor.get()



        return data



    def get_workflow_name(self) -> str:

        """

        Get the workflow name.



        Returns:

            Workflow name

        """

        return self.workflow_name_var.get()



    # === Event Handlers ===



    def _on_new_clicked(self):

        """Handle new button click."""

        name = simpledialog.askstring("New Workflow", "Enter workflow name:")

        if name:

            if self.presenter:

                self.presenter.create_new_workflow(name)



    def _on_open_clicked(self):

        """Handle open button click."""

        workflow_id = filedialog.askopenfilename(

            title="Open Workflow",

            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]

        )

        if workflow_id and self.presenter:

            self.presenter.load_workflow(workflow_id)



    def _on_save_clicked(self):

        """Handle save button click."""

        if self.presenter:

            self.presenter.save_workflow()



    def _on_execute_clicked(self):

        """Handle execute button click."""

        if self.presenter:

            result = self.presenter.execute_workflow()



            if result["success"]:

                messagebox.showinfo("Execution Result", "Workflow executed successfully!")

            else:

                messagebox.showerror("Execution Error", f"Workflow execution failed: {result['message']}")



    def _on_validate_clicked(self):

        """Handle validate button click."""

        if self.presenter:

            result = self.presenter.validate_workflow()



            if result["valid"]:

                messagebox.showinfo("Validation Result", "Workflow is valid!")

            else:

                messagebox.showerror("Validation Error", f"Workflow validation failed:\n{chr(10).join(result['errors'])}")



    def _on_canvas_click(self, event):

        """Handle canvas click."""

        if self.selected_node_type and not self.is_dragging:

            # Add a new node

            if self.presenter:

                # Convert screen coordinates to world coordinates
                world_x, world_y = self.screen_to_world(event.x, event.y)
                self.presenter.add_node(self.selected_node_type, (world_x, world_y))

                self.selected_node_type = None  # Reset selection



                # Reset node type buttons

                for button in self.node_buttons.values():

                    button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Default color



    def _on_canvas_right_click(self, event):

        """Handle canvas right click."""



        # Check if we clicked on a node

        node_id = self._find_node_at_position(event.x, event.y)

        if node_id:

            self.selected_node_id = node_id

            self._highlight_selected_node()

            self.node_context_menu.show(event.x_root, event.y_root)

            return



        # Check if we clicked on a connection

        connection_id = self._find_connection_at_position(event.x, event.y)

        if connection_id:

            self.selected_connection_id = connection_id

            self._highlight_selected_connection()

            self.connection_context_menu.show(event.x_root, event.y_root)

            return



        # Otherwise, show the canvas context menu

        self.canvas_context_menu.show(event.x_root, event.y_root)



        # Show context menu

        pass





    def _on_canvas_drag(self, event):

        """Handle canvas drag."""

        # If dragging a node from toolbox, update the drag icon position

        if self.is_dragging and self.drag_icon:

            # Calculate the distance moved

            dx = event.x - self.drag_data["x"]

            dy = event.y - self.drag_data["y"]



            # Move the drag icon

            self.canvas.move(self.drag_icon, dx, dy)



            # Update the drag data

            self.drag_data["x"] = event.x

            self.drag_data["y"] = event.y



    def _on_canvas_release(self, event):

        """Handle canvas release."""

        # If dropping a node from toolbox, create a new node

        if self.is_dragging and self.drag_data["node_type"]:

            # Add a new node at the drop position

            if self.presenter:

                # Convert screen coordinates to world coordinates
                world_x, world_y = self.screen_to_world(event.x, event.y)
                self.presenter.add_node(self.drag_data["node_type"], (world_x, world_y))



            # Clean up drag and drop

            self._end_drag()



        # End pan or connection creation

        if self.is_connecting and self.temp_connection:

            # End connection creation

            self.canvas.delete(self.temp_connection)

            self.temp_connection = None

            self.is_connecting = False

            self.connection_start = None



    def _on_canvas_scroll(self, event):
        """Handle canvas scroll."""
        print("DEBUG: WorkflowView._on_canvas_scroll() called")

        # Determine the direction of the scroll
        if event.num == 4 or event.delta > 0:
            # Scroll up - zoom in
            self._zoom_canvas(1.1, event.x, event.y)
            print("DEBUG: Zooming in")
        elif event.num == 5 or event.delta < 0:
            # Scroll down - zoom out
            self._zoom_canvas(0.9, event.x, event.y)
            print("DEBUG: Zooming out")





    def _zoom_canvas(self, factor: float, center_x: int = None, center_y: int = None):
        """
        Zoom the canvas by the given factor.

        Args:
            factor: Zoom factor (>1 to zoom in, <1 to zoom out)
            center_x: X coordinate of zoom center (defaults to canvas center)
            center_y: Y coordinate of zoom center (defaults to canvas center)
        """
        print(f"DEBUG: WorkflowView._zoom_canvas({factor}, {center_x}, {center_y}) called")

        # Default to canvas center if no center point provided
        if center_x is None or center_y is None:
            center_x = self.canvas.winfo_width() / 2
            center_y = self.canvas.winfo_height() / 2

        # Calculate new scale, clamping to reasonable limits
        new_scale = max(0.1, min(3.0, self.canvas_scale * factor))

        # If scale didn't change, no need to zoom
        if new_scale == self.canvas_scale:
            return

        # Calculate zoom center in world coordinates
        world_center_x = (center_x - self.canvas_offset[0]) / self.canvas_scale
        world_center_y = (center_y - self.canvas_offset[1]) / self.canvas_scale

        # Calculate new offset to keep zoom center fixed
        new_offset_x = center_x - world_center_x * new_scale
        new_offset_y = center_y - world_center_y * new_scale

        # Update scale and offset
        scale_change = new_scale / self.canvas_scale
        self.canvas_scale = new_scale
        self.canvas_offset = (new_offset_x, new_offset_y)

        # Scale all objects on canvas
        self.canvas.scale("all", center_x, center_y, scale_change, scale_change)

        # Redraw grid
        self._draw_grid()

        print(f"DEBUG: Canvas zoomed to scale {self.canvas_scale}")

        print(f"DEBUG: Canvas zoomed to scale {self.canvas_scale}")

    def _on_node_click(self, event):

        """Handle node click."""

        # Get the clicked node

        item = self.canvas.find_closest(event.x, event.y)[0]

        tags = self.canvas.gettags(item)



        for tag in tags:

            if tag.startswith("node_"):

                node_id = tag[5:]  # Remove "node_" prefix

                if self.presenter:

                    self.presenter.select_node(node_id)

                break



    def _on_node_drag(self, event):

        """Handle node drag."""

        # Move the selected node

        if not self.selected_node_id:

            return



        # Get node elements

        elements = self.node_elements.get(self.selected_node_id)

        if not elements:

            return



        # Calculate movement in screen coordinates
        old_screen_x, old_screen_y = elements["screen_position"]
        dx = event.x - old_screen_x
        dy = event.y - old_screen_y



        # Move all node elements

        for key, item_id in elements.items():

            if key not in ["world_position", "screen_position", "width", "height"]:

                self.canvas.move(item_id, dx, dy)



        # Update node screen position
        elements["screen_position"] = (event.x, event.y)

        # Update node world position
        world_x, world_y = self.screen_to_world(event.x, event.y)
        elements["world_position"] = (world_x, world_y)

        # Update the node in the workflow model
        if self.presenter and self.presenter.current_workflow:
            node = self.presenter.current_workflow.nodes.get(self.selected_node_id)
            if node:
                node.position = (world_x, world_y)



        # Update connections

        for conn_id, conn in self.presenter.current_workflow.connections.items():

            if conn.source_node_id == self.selected_node_id or conn.target_node_id == self.selected_node_id:

                self.draw_connection(conn)



    def _on_node_release(self, event):

        """Handle node release."""

        # End node drag

        if self.selected_node_id:

            # Update the node position in the workflow

            if self.presenter and self.presenter.current_workflow:

                node = self.presenter.current_workflow.nodes.get(self.selected_node_id)

                if node:

                    elements = self.node_elements.get(self.selected_node_id)

                    if elements:

                        node.position = elements["position"]



    def _on_connection_click(self, event):

        """Handle connection click."""

        # Get the clicked connection

        item = self.canvas.find_closest(event.x, event.y)[0]

        tags = self.canvas.gettags(item)



        for tag in tags:

            if tag.startswith("connection_"):

                conn_id = tag[11:]  # Remove "connection_" prefix



                # Ask for confirmation

                if messagebox.askyesno("Delete Connection", "Delete this connection?"):

                    if self.presenter:

                        self.presenter.delete_connection(conn_id)

                break



    def _on_node_type_selected(self, node_type: str):

        """Handle node type selection."""

        self.selected_node_type = node_type



        # Highlight the selected button

        for type_name, button in self.node_buttons.items():

            if type_name == node_type:

                button.configure(fg_color=("#2E7D32", "#2E7D32"))  # Green

            else:

                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Default color



    def _on_properties_save(self):

        """Handle properties save button click."""

        if self.presenter:

            self.presenter.update_node_properties()



    def _on_node_delete(self):

        """Handle node delete button click."""

        if self.selected_node_id and messagebox.askyesno("Delete Node", "Delete this node?"):

            if self.presenter:

                self.presenter.delete_node()



    # === Drag and Drop Methods ===



    def _on_toolbox_button_press(self, event):

        """Handle toolbox button press for drag and drop."""

        # Get the button that was clicked

        button = event.widget



        # Store the node type for dragging

        self.drag_data["node_type"] = button.node_type

        self.drag_data["node_name"] = button.node_name



        # Convert button coordinates to canvas coordinates

        button_x = button.winfo_rootx() - self.canvas.winfo_rootx()

        button_y = button.winfo_rooty() - self.canvas.winfo_rooty()



        # Store the initial position

        self.drag_data["x"] = button_x

        self.drag_data["y"] = button_y



        # Highlight the button

        button.configure(fg_color=("#2E7D32", "#2E7D32"))  # Green



    def _on_toolbox_button_drag(self, event):

        """Handle toolbox button drag."""

        # If we haven't started dragging yet, create a drag icon

        if not self.is_dragging and self.drag_data["node_type"]:

            self.is_dragging = True



            # Convert to canvas coordinates

            canvas_x = event.widget.winfo_rootx() - self.canvas.winfo_rootx() + event.x

            canvas_y = event.widget.winfo_rooty() - self.canvas.winfo_rooty() + event.y



            # Create a drag icon on the canvas

            self._create_drag_icon(canvas_x, canvas_y)



            # Update the drag position

            self.drag_data["x"] = canvas_x

            self.drag_data["y"] = canvas_y



    def _on_toolbox_button_release(self, event):

        """Handle toolbox button release."""

        # Reset button appearance

        event.widget.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Default color



        # If we're not dragging, handle as a normal click

        if not self.is_dragging:

            self._on_node_type_selected(event.widget.node_type)

            return



        # If we're dragging but not over the canvas, cancel the drag

        canvas_x = event.widget.winfo_rootx() - self.canvas.winfo_rootx() + event.x

        canvas_y = event.widget.winfo_rooty() - self.canvas.winfo_rooty() + event.y



        canvas_width = self.canvas.winfo_width()

        canvas_height = self.canvas.winfo_height()



        if canvas_x < 0 or canvas_x > canvas_width or canvas_y < 0 or canvas_y > canvas_height:

            # Outside canvas, cancel drag

            self._end_drag()

            return



        # Otherwise, the canvas release handler will handle the drop



    def _create_drag_icon(self, x, y):

        """Create a visual representation of the node being dragged."""

        # Node dimensions

        width = 120

        height = 60



        # Create a simple rectangle as the drag icon

        self.drag_icon = self.canvas.create_rectangle(

            x - width/2, y - height/2,

            x + width/2, y + height/2,

            fill="#3B8ED0", outline="#FFFFFF", width=2,

            dash=(4, 4),  # Dashed outline to indicate dragging

            tags=("drag_icon",)

        )



        # Add the node type name

        self.drag_text = self.canvas.create_text(

            x, y,

            text=self.drag_data["node_name"],

            fill="#FFFFFF",

            font=get_default_font(),

            tags=("drag_icon",)

        )



    def _end_drag(self):

        """End the drag and drop operation."""

        # Delete the drag icon

        if self.drag_icon:

            self.canvas.delete("drag_icon")

            self.drag_icon = None

            self.drag_text = None



        # Reset drag state

        self.is_dragging = False

        self.drag_data["node_type"] = None

        self.drag_data["node_name"] = None





    # === Context Menu Methods ===



    def _create_context_menus(self):

        """Create context menus for the workflow view."""

        # Node context menu

        self.node_context_menu = ContextMenu(self.canvas)

        self.node_context_menu.add_command("Edit Properties", self._on_node_click)

        self.node_context_menu.add_command("Delete Node", self._on_node_delete)

        self.node_context_menu.add_separator()

        self.node_context_menu.add_command("Copy Node", self._on_node_copy)

        self.node_context_menu.add_command("Duplicate Node", self._on_node_duplicate)



        # Connection context menu

        self.connection_context_menu = ContextMenu(self.canvas)

        self.connection_context_menu.add_command("Delete Connection", self._on_connection_delete)



        # Canvas context menu

        self.canvas_context_menu = ContextMenu(self.canvas)

        self.canvas_context_menu.add_command("Add Node", self._on_canvas_add_node)

        self.canvas_context_menu.add_command("Paste Node", self._on_canvas_paste_node, enabled=False)

        self.canvas_context_menu.add_separator()

        self.canvas_context_menu.add_command("Reset View", self._on_canvas_reset_view)



    def _on_canvas_right_click(self, event):

        """Handle canvas right-click for context menu."""

        # Check if we clicked on a node

        node_id = self._find_node_at_position(event.x, event.y)

        if node_id:

            self.selected_node_id = node_id

            self._highlight_selected_node()

            self.node_context_menu.show(event.x_root, event.y_root)

            return



        # Check if we clicked on a connection

        connection_id = self._find_connection_at_position(event.x, event.y)

        if connection_id:

            self.selected_connection_id = connection_id

            self._highlight_selected_connection()

            self.connection_context_menu.show(event.x_root, event.y_root)

            return



        # Otherwise, show the canvas context menu

        self.canvas_context_menu.show(event.x_root, event.y_root)



    def _find_node_at_position(self, x, y):

        """Find a node at the given position."""

        # Check if the position is within any node

        for node_id, elements in self.node_elements.items():

            # Get the node screen position and dimensions
            node_x, node_y = elements["screen_position"]

            node_width = 120  # Standard node width

            node_height = 60  # Standard node height



            # Check if the position is within the node

            if (node_x - node_width/2 <= x <= node_x + node_width/2 and

                node_y - node_height/2 <= y <= node_y + node_height/2):

                return node_id



        return None



    def _find_connection_at_position(self, x, y):

        """Find a connection at the given position."""

        # Check if the position is near any connection line

        for connection_id, elements in self.connection_elements.items():

            # Get the connection line

            line_id = elements["line"]



            # Get the coordinates of the line

            coords = self.canvas.coords(line_id)



            # For bezier curves, check if the point is near the curve

            # This is a simplified check - just check if the point is near the bounding box

            x_coords = [coords[i] for i in range(0, len(coords), 2)]

            y_coords = [coords[i] for i in range(1, len(coords), 2)]



            min_x = min(x_coords) - 5

            max_x = max(x_coords) + 5

            min_y = min(y_coords) - 5

            max_y = max(y_coords) + 5



            if min_x <= x <= max_x and min_y <= y <= max_y:

                # More precise check - calculate distance to the line segments

                for i in range(len(x_coords) - 1):

                    x1, y1 = x_coords[i], y_coords[i]

                    x2, y2 = x_coords[i+1], y_coords[i+1]



                    # Calculate distance from point to line segment

                    distance = self._point_to_line_distance(x, y, x1, y1, x2, y2)



                    if distance <= 5:  # 5 pixels tolerance

                        return connection_id



        return None



    def _point_to_line_distance(self, x, y, x1, y1, x2, y2):

        """Calculate the distance from a point to a line segment."""

        # Calculate the length of the line segment

        line_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5



        if line_length == 0:

            # The line segment is actually a point

            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5



        # Calculate the projection of the point onto the line

        t = max(0, min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (line_length ** 2)))



        # Calculate the closest point on the line segment

        closest_x = x1 + t * (x2 - x1)

        closest_y = y1 + t * (y2 - y1)



        # Calculate the distance from the point to the closest point on the line segment

        return ((x - closest_x) ** 2 + (y - closest_y) ** 2) ** 0.5



    def _on_node_copy(self):

        """Handle node copy."""

        if self.selected_node_id and self.presenter:

            self.presenter.copy_node(self.selected_node_id)



    def _on_node_duplicate(self):

        """Handle node duplicate."""

        if self.selected_node_id and self.presenter:

            self.presenter.duplicate_node(self.selected_node_id)



    def _on_connection_delete(self):

        """Handle connection delete."""

        if self.selected_connection_id and self.presenter:

            self.presenter.delete_connection(self.selected_connection_id)



    def _on_canvas_add_node(self):

        """Handle adding a node from the canvas context menu."""

        # Show a dialog to select the node type

        if self.presenter:

            self.presenter.show_add_node_dialog()



    def _on_canvas_paste_node(self):

        """Handle pasting a node from the canvas context menu."""

        if self.presenter:

            self.presenter.paste_node()



    def _on_canvas_reset_view(self):

        """Handle resetting the canvas view."""

        # Reset the canvas scale and offset

        self.canvas_scale = 1.0

        self.canvas_offset = (0, 0)



        # Redraw the canvas

        self._redraw_canvas()







    def _on_add_property(self):

        """Handle add property button click."""

        prop_name = simpledialog.askstring("Add Property", "Enter property name:")

        if prop_name:

            # Add a new property editor

            row = len(self.properties_editors) + 3  # Offset for type, ID, and label



            prop_label = ctk.CTkLabel(

                self.properties_scroll_frame, text=f"{prop_name.replace('_', ' ').title()}:",

                font=get_default_font()

            )

            prop_label.grid(row=row, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)



            prop_entry = ctk.CTkEntry(self.properties_scroll_frame)

            prop_entry.grid(row=row, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

            self.properties_editors[prop_name] = prop_entry



    # === Helper Methods ===



    def _on_canvas_middle_click(self, event):
        """
        Handle middle mouse button click for panning.

        Args:
            event: Mouse click event
        """
        print("DEBUG: WorkflowView._on_canvas_middle_click() called")

        # Store the starting position for panning
        self.drag_start_x = event.x
        self.drag_start_y = event.y

        # Change cursor to indicate panning mode
        self.canvas.config(cursor="fleur")

    def _on_canvas_middle_drag(self, event):
        """
        Handle middle mouse button drag for panning.

        Args:
            event: Mouse drag event
        """
        print("DEBUG: WorkflowView._on_canvas_middle_drag() called")

        # Calculate the distance moved
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        # Update the drag start position
        self.drag_start_x = event.x
        self.drag_start_y = event.y

        # Pan the canvas
        self._pan_canvas(dx, dy)

    def _on_canvas_middle_release(self, event):
        """
        Handle middle mouse button release after panning.

        Args:
            event: Mouse release event
        """
        print("DEBUG: WorkflowView._on_canvas_middle_release() called")

        # Reset cursor
        self.canvas.config(cursor="")

    def _pan_canvas(self, dx: int, dy: int):
        """
        Pan the canvas by the given amount.

        Args:
            dx: Change in x direction
            dy: Change in y direction
        """
        print(f"DEBUG: WorkflowView._pan_canvas({dx}, {dy}) called")

        # Update offset
        self.canvas_offset = (
            self.canvas_offset[0] + dx,
            self.canvas_offset[1] + dy
        )

        # Move all objects
        self.canvas.move("all", dx, dy)

        # Redraw grid
        self._draw_grid()

        print(f"DEBUG: Canvas panned to offset {self.canvas_offset}")

    def _draw_grid(self):
        """Draw grid lines on the canvas."""
        print("DEBUG: WorkflowView._draw_grid() called")

        # Clear existing grid
        self.canvas.delete("grid")

        # Get canvas dimensions
        width = int(self.canvas.cget("width"))
        height = int(self.canvas.cget("height"))

        if width <= 1 or height <= 1:  # Canvas not yet properly sized
            return

        # Calculate grid spacing based on zoom level
        spacing = int(20 * self.canvas_scale)
        if spacing < 5:  # Minimum grid spacing
            spacing = 5

        # Calculate grid offset based on pan offset
        offset_x = int(self.canvas_offset[0] % spacing)
        offset_y = int(self.canvas_offset[1] % spacing)

        # Draw vertical lines
        for x in range(offset_x, width + 1, spacing):
            self.canvas.create_line(x, 0, x, height, fill="#444444", tags="grid")

        # Draw horizontal lines
        for y in range(offset_y, height + 1, spacing):
            self.canvas.create_line(0, y, width, y, fill="#444444", tags="grid")

    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[float, float]:
        """
        Convert screen coordinates to world coordinates.

        Args:
            screen_x: X coordinate in screen space
            screen_y: Y coordinate in screen space

        Returns:
            Tuple of (x, y) in world space
        """
        world_x = (screen_x - self.canvas_offset[0]) / self.canvas_scale
        world_y = (screen_y - self.canvas_offset[1]) / self.canvas_scale
        return (world_x, world_y)

    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[int, int]:
        """
        Convert world coordinates to screen coordinates.

        Args:
            world_x: X coordinate in world space
            world_y: Y coordinate in world space

        Returns:
            Tuple of (x, y) in screen space
        """
        screen_x = int(world_x * self.canvas_scale + self.canvas_offset[0])
        screen_y = int(world_y * self.canvas_scale + self.canvas_offset[1])
        return (screen_x, screen_y)


```

### src/ui/presenters/workflow_presenter.py

**Created:** 2025-04-02 02:20:12
**Modified:** 2025-04-02 02:20:12
**Size:** 15696 bytes

**Issues:**

-   Directly references backend services
-   Doesn't use proper dependency injection
-   Handles too many responsibilities
-   Difficult to test in isolation

**Code:**

```python
"""
Workflow Builder Presenter for managing workflow creation and editing.
SOLID: Single responsibility - business logic for workflow building.
KISS: Simple operations with clear error handling.
"""
import uuid
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.workflow_adapter import WorkflowAdapter
from src.core.models import Workflow, WorkflowNode, WorkflowConnection

if TYPE_CHECKING:
    from ..views.workflow_view import WorkflowView
    from app import AutoClickApp

class WorkflowPresenter(BasePresenter[WorkflowAdapter]):
    """Presenter for the Workflow Builder view."""

    # Type hints for view and app
    view: 'WorkflowView'
    app: 'AutoClickApp'

    def __init__(self, view: 'WorkflowView', app: 'AutoClickApp', service: WorkflowAdapter):
        """
        Initialize the workflow presenter.

        Args:
            view: The workflow view
            app: The main application
            service: The workflow adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.current_workflow: Optional[Workflow] = None
        self.selected_node_id: Optional[str] = None
        self.node_types: List[Dict[str, Any]] = []

    def initialize_view(self):
        """Initialize the view with data."""
        try:
            print("DEBUG: WorkflowPresenter.initialize_view() called")
            # Get node types from the service
            self.node_types = self.service.get_node_types()
            print(f"DEBUG: Got {len(self.node_types)} node types")

            # Initialize the canvas and toolbox
            print("DEBUG: Initializing canvas...")
            self.view.initialize_canvas()
            print("DEBUG: Canvas initialized")

            print("DEBUG: Initializing toolbox...")
            self.view.initialize_toolbox(self.node_types)
            print("DEBUG: Toolbox initialized")

            # Create a new empty workflow
            print("DEBUG: Creating new workflow...")
            self.create_new_workflow("Untitled Workflow")
            print("DEBUG: New workflow created")

            self.update_app_status("Workflow builder initialized")
            print("DEBUG: WorkflowPresenter.initialize_view() completed")
        except Exception as e:
            print(f"ERROR: Failed to initialize workflow builder: {str(e)}")
            self._handle_error("initializing workflow builder", e)

    def load_workflow(self, workflow_id: str):
        """
        Load a workflow from the service.

        Args:
            workflow_id: ID of the workflow to load
        """
        try:
            # Get the workflow from the service
            workflow = self.service.get_workflow(workflow_id)

            if workflow:
                # Set the current workflow
                self.current_workflow = workflow

                # Clear the canvas and redraw the workflow
                self.view.clear_canvas()
                self.view.redraw_workflow(workflow)

                # Update the workflow name
                self.view.workflow_name_var.set(workflow.name)

                self.update_app_status(f"Loaded workflow: {workflow.name}")
            else:
                self.update_app_status(f"Workflow not found: {workflow_id}")
        except Exception as e:
            self._handle_error(f"loading workflow {workflow_id}", e)

    def create_new_workflow(self, name: str):
        """
        Create a new workflow.

        Args:
            name: Name of the new workflow
        """
        try:
            print(f"DEBUG: Creating new workflow: {name}")
            # Create a new workflow
            workflow_id = str(uuid.uuid4())
            workflow = Workflow(
                id=workflow_id,
                name=name,
                nodes={},
                connections={}
            )
            print(f"DEBUG: Created workflow object with ID: {workflow_id}")

            # Add a start node
            start_node_id = str(uuid.uuid4())
            start_node = WorkflowNode(
                id=start_node_id,
                type="Start",
                position=(100, 100),
                properties={},
                label="Start"
            )
            workflow.nodes[start_node_id] = start_node
            print(f"DEBUG: Added start node with ID: {start_node_id}")

            # Set the current workflow
            self.current_workflow = workflow
            print("DEBUG: Set current workflow")

            # Save the workflow to the service
            self.service.create_workflow(workflow)
            print("DEBUG: Saved workflow to service")

            # Clear the canvas and redraw the workflow
            print("DEBUG: Clearing canvas...")
            self.view.clear_canvas()
            print("DEBUG: Canvas cleared")

            print("DEBUG: Redrawing workflow...")
            self.view.redraw_workflow(workflow)
            print("DEBUG: Workflow redrawn")

            # Update the workflow name
            self.view.workflow_name_var.set(name)
            print("DEBUG: Updated workflow name")

            self.update_app_status(f"Created new workflow: {name}")
            print(f"DEBUG: create_new_workflow({name}) completed")
        except Exception as e:
            print(f"ERROR: Failed to create new workflow: {str(e)}")
            self._handle_error(f"creating new workflow {name}", e)

    def save_workflow(self):
        """Save the current workflow."""
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to save")
                return

            # Update the workflow name
            self.current_workflow.name = self.view.get_workflow_name()

            # Save the workflow to the service
            self.service.update_workflow(self.current_workflow)

            self.update_app_status(f"Saved workflow: {self.current_workflow.name}")
        except Exception as e:
            self._handle_error("saving workflow", e)

    def add_node(self, node_type: str, position: Tuple[int, int]):
        """
        Add a node to the current workflow.

        Args:
            node_type: Type of node to add
            position: Position (x, y) to place the node
        """
        try:
            if not self.current_workflow:
                self.create_new_workflow("Untitled Workflow")

            # Create a new node
            node_id = str(uuid.uuid4())
            node = WorkflowNode(
                id=node_id,
                type=node_type,
                position=position,
                properties={},
                label=node_type
            )

            # Add the node to the workflow
            self.current_workflow.nodes[node_id] = node

            # Draw the node on the canvas
            self.view.draw_node(node)

            self.update_app_status(f"Added {node_type} node")

            return node_id
        except Exception as e:
            self._handle_error(f"adding {node_type} node", e)
            return None

    def select_node(self, node_id: str):
        """
        Select a node in the workflow.

        Args:
            node_id: ID of the node to select
        """
        try:
            if not self.current_workflow or node_id not in self.current_workflow.nodes:
                self.update_app_status(f"Node not found: {node_id}")
                return

            # Set the selected node
            self.selected_node_id = node_id

            # Update the view
            self.view.select_node_visual(node_id)
            self.view.display_properties_for_node(self.current_workflow.nodes[node_id])

            self.update_app_status(f"Selected {self.current_workflow.nodes[node_id].type} node")
        except Exception as e:
            self._handle_error(f"selecting node {node_id}", e)

    def update_node_properties(self):
        """Update the properties of the selected node."""
        try:
            if not self.current_workflow or not self.selected_node_id:
                self.update_app_status("No node selected")
                return

            # Get the properties from the view
            properties = self.view.get_properties_data()

            if not properties:
                self.update_app_status("No properties to update")
                return

            # Update the node properties
            node = self.current_workflow.nodes[self.selected_node_id]
            node.properties.update(properties)

            # Update the node label if provided
            if "label" in properties:
                node.label = properties["label"]

            # Redraw the workflow
            self.view.redraw_workflow(self.current_workflow)

            self.update_app_status(f"Updated {node.type} node properties")
        except Exception as e:
            self._handle_error("updating node properties", e)

    def delete_node(self):
        """Delete the selected node."""
        try:
            if not self.current_workflow or not self.selected_node_id:
                self.update_app_status("No node selected")
                return

            # Get the node
            node = self.current_workflow.nodes[self.selected_node_id]

            # Find connections to/from this node
            connections_to_delete = []
            for conn_id, conn in self.current_workflow.connections.items():
                if conn.source_node_id == self.selected_node_id or conn.target_node_id == self.selected_node_id:
                    connections_to_delete.append(conn_id)

            # Delete the connections
            for conn_id in connections_to_delete:
                del self.current_workflow.connections[conn_id]

            # Delete the node
            del self.current_workflow.nodes[self.selected_node_id]

            # Clear the selection
            self.selected_node_id = None

            # Redraw the workflow
            self.view.redraw_workflow(self.current_workflow)

            self.update_app_status(f"Deleted {node.type} node")
        except Exception as e:
            self._handle_error("deleting node", e)

    def add_connection(self, source_node_id: str, source_port: str, target_node_id: str, target_port: str):
        """
        Add a connection between nodes.

        Args:
            source_node_id: ID of the source node
            source_port: Port on the source node
            target_node_id: ID of the target node
            target_port: Port on the target node
        """
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to add connection to")
                return

            # Check if the nodes exist
            if source_node_id not in self.current_workflow.nodes:
                self.update_app_status(f"Source node not found: {source_node_id}")
                return

            if target_node_id not in self.current_workflow.nodes:
                self.update_app_status(f"Target node not found: {target_node_id}")
                return

            # Create a new connection
            conn_id = str(uuid.uuid4())
            connection = WorkflowConnection(
                id=conn_id,
                source_node_id=source_node_id,
                source_port=source_port,
                target_node_id=target_node_id,
                target_port=target_port
            )

            # Add the connection to the workflow
            self.current_workflow.connections[conn_id] = connection

            # Draw the connection on the canvas
            self.view.draw_connection(connection)

            self.update_app_status("Added connection")

            return conn_id
        except Exception as e:
            self._handle_error("adding connection", e)
            return None

    def delete_connection(self, connection_id: str):
        """
        Delete a connection.

        Args:
            connection_id: ID of the connection to delete
        """
        try:
            if not self.current_workflow or connection_id not in self.current_workflow.connections:
                self.update_app_status(f"Connection not found: {connection_id}")
                return

            # Delete the connection
            del self.current_workflow.connections[connection_id]

            # Redraw the workflow
            self.view.redraw_workflow(self.current_workflow)

            self.update_app_status("Deleted connection")
        except Exception as e:
            self._handle_error(f"deleting connection {connection_id}", e)

    def execute_workflow(self):
        """
        Execute the current workflow.

        Returns:
            Dictionary containing execution results
        """
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to execute")
                return {"success": False, "message": "No workflow to execute"}

            # Save the workflow first
            self.save_workflow()

            # Execute the workflow
            result = self.service.execute_workflow(self.current_workflow)

            if result["success"]:
                self.update_app_status("Workflow executed successfully")
            else:
                self.update_app_status(f"Workflow execution failed: {result['message']}")

            return result
        except Exception as e:
            self._handle_error("executing workflow", e)
            return {"success": False, "message": str(e)}

    def validate_workflow(self):
        """
        Validate the current workflow.

        Returns:
            Dictionary containing validation results
        """
        try:
            if not self.current_workflow:
                self.update_app_status("No workflow to validate")
                return {"valid": False, "errors": ["No workflow to validate"]}

            # Initialize validation results
            result = {"valid": True, "errors": []}

            # Check if there's a Start node
            has_start = False
            for node in self.current_workflow.nodes.values():
                if node.type == "Start":
                    has_start = True
                    break

            if not has_start:
                result["valid"] = False
                result["errors"].append("No Start node found")

            # Check if there's an End node
            has_end = False
            for node in self.current_workflow.nodes.values():
                if node.type == "End":
                    has_end = True
                    break

            if not has_end:
                result["valid"] = False
                result["errors"].append("No End node found")

            # Check if all nodes are connected
            connected_nodes = set()
            for conn in self.current_workflow.connections.values():
                connected_nodes.add(conn.source_node_id)
                connected_nodes.add(conn.target_node_id)

            for node_id in self.current_workflow.nodes:
                if node_id not in connected_nodes and len(self.current_workflow.nodes) > 1:
                    result["valid"] = False
                    result["errors"].append(f"Node {node_id} is not connected")

            # Update status
            if result["valid"]:
                self.update_app_status("Workflow is valid")
            else:
                self.update_app_status(f"Workflow validation failed: {', '.join(result['errors'])}")

            return result
        except Exception as e:
            self._handle_error("validating workflow", e)
            return {"valid": False, "errors": [str(e)]}

```

### src/core/workflow/workflow_serializer.py

**Created:** 2025-03-30 12:08:15
**Modified:** 2025-03-30 12:08:15
**Size:** 8104 bytes

**Issues:**

-   Overly complex serialization/deserialization
-   Different formats for storage vs. memory
-   Multiple conversion steps
-   Potential for bugs and inconsistencies

**Code:**

```python
"""Serialization for workflows"""
import os
import json
import logging
from typing import Dict, Any, List, Tuple, Optional, Union

from src.core.actions.base_action import BaseAction
from src.core.actions.action_factory import ActionFactory
from src.core.conditions.condition_factory import ConditionFactoryClass


class WorkflowSerializer:
    """
    Serializer for workflows

    This class provides methods to serialize workflows to JSON and deserialize
    them back into executable workflows. It handles saving and loading workflows
    to/from files, and provides version compatibility checks.
    """

    # Current schema version
    SCHEMA_VERSION = "1.0"

    def __init__(self):
        """Initialize the workflow serializer"""
        self.logger = logging.getLogger(self.__class__.__name__)

    def serialize_workflow(
        self,
        actions: List[BaseAction],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Serialize a workflow to a dictionary

        Args:
            actions: List of actions in the workflow
            metadata: Optional metadata for the workflow

        Returns:
            Dictionary representation of the workflow
        """
        # Create the basic structure
        result = {
            "schema_version": self.SCHEMA_VERSION,
            "metadata": metadata or {},
            "actions": [action.to_dict() for action in actions]
        }

        return result

    def deserialize_workflow(
        self,
        data: Dict[str, Any],
        use_factory: bool = False,
        strict_version: bool = False
    ) -> Tuple[List[BaseAction], Dict[str, Any]]:
        """
        Deserialize a workflow from a dictionary

        Args:
            data: Dictionary representation of the workflow
            use_factory: Whether to use the ActionFactory to create actions
            strict_version: Whether to enforce schema version compatibility

        Returns:
            Tuple of (actions, metadata)

        Raises:
            ValueError: If the data is invalid or incompatible
        """
        # Validate the data
        if not isinstance(data, dict):
            raise ValueError("Invalid workflow data: must be a dictionary")

        if "actions" not in data:
            raise ValueError("Invalid workflow data: missing 'actions' key")

        # Check schema version
        schema_version = data.get("schema_version", "1.0")
        if strict_version and schema_version != self.SCHEMA_VERSION:
            raise ValueError(
                f"Schema version mismatch: expected {self.SCHEMA_VERSION}, got {schema_version}"
            )

        # Get metadata
        metadata = data.get("metadata", {})

        # Deserialize actions
        actions = []
        action_data_list = data.get("actions", [])

        for action_data in action_data_list:
            if use_factory:
                # Use the action factory to create the action
                action_type = action_data.get("type")
                if not action_type:
                    self.logger.warning(f"Action data missing 'type': {action_data}")
                    continue

                try:
                    # Handle IfThenElseAction specially to process its condition
                    if action_type == "if_then_else":
                        # Process the condition
                        condition_data = action_data.get("condition", {})
                        condition_type = condition_data.get("type")

                        if condition_type:
                            try:
                                # Create the condition using the ConditionFactory
                                condition = ConditionFactoryClass.get_instance().create_condition(condition_data)

                                # Update the action data with the condition
                                action_data["_condition"] = condition
                            except Exception as e:
                                self.logger.error(f"Error creating condition of type {condition_type}: {str(e)}")

                    # Create the action using the ActionFactory
                    action = ActionFactory.get_instance().create_from_dict(action_data)
                    actions.append(action)
                except Exception as e:
                    self.logger.error(f"Error creating action of type {action_type}: {str(e)}")
                    continue
            else:
                # Use the TestAction class for testing
                from tests.core.workflow.test_workflow_serializer import TestAction
                action = TestAction.from_dict(action_data)
                actions.append(action)

        return actions, metadata

    def save_workflow_to_file(
        self,
        file_path: str,
        actions: List[BaseAction],
        metadata: Optional[Dict[str, Any]] = None,
        indent: int = 2
    ) -> None:
        """
        Save a workflow to a file

        Args:
            file_path: Path to save the workflow to
            actions: List of actions in the workflow
            metadata: Optional metadata for the workflow
            indent: JSON indentation level

        Raises:
            IOError: If the file cannot be written
        """
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        # Serialize the workflow
        data = self.serialize_workflow(actions, metadata)

        # Write to file
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=indent)

            self.logger.info(f"Saved workflow to {file_path}")
        except IOError as e:
            self.logger.error(f"Error saving workflow to {file_path}: {str(e)}")
            raise

    def load_workflow_from_file(
        self,
        file_path: str,
        use_factory: bool = False,
        strict_version: bool = False
    ) -> Dict[str, Any]:
        """
        Load a workflow from a file

        Args:
            file_path: Path to load the workflow from
            use_factory: Whether to use the ActionFactory to create actions
            strict_version: Whether to enforce schema version compatibility

        Returns:
            Dictionary representation of the workflow

        Raises:
            IOError: If the file cannot be read
            ValueError: If the file contains invalid data
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            self.logger.info(f"Loaded workflow from {file_path}")
            return data
        except IOError as e:
            self.logger.error(f"Error loading workflow from {file_path}: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing workflow file {file_path}: {str(e)}")
            raise ValueError(f"Invalid JSON in workflow file: {str(e)}")

    def load_and_deserialize_workflow(
        self,
        file_path: str,
        use_factory: bool = True,
        strict_version: bool = False
    ) -> Tuple[List[BaseAction], Dict[str, Any]]:
        """
        Load and deserialize a workflow from a file

        Args:
            file_path: Path to load the workflow from
            use_factory: Whether to use the ActionFactory to create actions
            strict_version: Whether to enforce schema version compatibility

        Returns:
            Tuple of (actions, metadata)

        Raises:
            IOError: If the file cannot be read
            ValueError: If the file contains invalid data
        """
        # Load the workflow data
        data = self.load_workflow_from_file(file_path)

        # Deserialize the workflow
        return self.deserialize_workflow(data, use_factory, strict_version)

```

## Components for Discussion

The following components have both strengths and weaknesses and require further analysis.

### src/core/workflow/workflow_storage_service.py

**Created:** 2025-04-01 06:53:38
**Modified:** 2025-04-02 01:57:14
**Size:** 4379 bytes

**Code:**

```python
"""
Workflow storage service.
SOLID: Single responsibility - workflow persistence logic.
KISS: Simple methods for loading and saving workflows.
"""
import json
import os
import logging
from typing import Dict, Any

from src.core.models import Workflow


class WorkflowStorageService:
    """Service for managing workflow storage (loading and saving)."""

    def __init__(self, storage_dir: str = "workflows"):
        """
        Initialize the workflow storage service.

        Args:
            storage_dir: Directory for storing workflow files
        """
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.storage_dir = storage_dir
        self.workflows: Dict[str, Workflow] = {}

        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)

        # Load existing workflows
        self._load_workflows()

    def _load_workflows(self) -> None:
        """Load all workflows from the storage directory."""
        if not os.path.exists(self.storage_dir):
            self.logger.warning(f"Storage directory does not exist: {self.storage_dir}")
            return

        workflow_files = [f for f in os.listdir(self.storage_dir) if f.endswith(".json")]
        if not workflow_files:
            self.logger.info(f"No workflow files found in {self.storage_dir}")
            return

        for filename in workflow_files:
            workflow_path = os.path.join(self.storage_dir, filename)
            try:
                # Check if file is empty
                if os.path.getsize(workflow_path) == 0:
                    self.logger.warning(f"Skipping empty workflow file: {filename}")
                    continue

                # Try to load and parse the file
                with open(workflow_path, "r") as f:
                    try:
                        workflow_data = json.load(f)
                    except json.JSONDecodeError as je:
                        self.logger.error(f"Invalid JSON in workflow file {filename}: {str(je)}")
                        continue

                    # Validate workflow data
                    if not isinstance(workflow_data, dict):
                        self.logger.error(f"Invalid workflow data in {filename}: not a dictionary")
                        continue

                    # Deserialize workflow
                    try:
                        workflow = self._deserialize_workflow(workflow_data)
                        self.workflows[workflow.id] = workflow
                        self.logger.info(f"Loaded workflow: {workflow.name} ({workflow.id})")
                    except Exception as e:
                        self.logger.error(f"Error deserializing workflow from {filename}: {str(e)}")
            except Exception as e:
                self.logger.error(f"Error loading workflow from {filename}: {str(e)}")

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow file from disk.

        Args:
            workflow_id: ID of the workflow to delete

        Returns:
            True if the workflow file was deleted, False if it wasn't found.
        """
        workflow_path = os.path.join(self.storage_dir, f"{workflow_id}.json")
        if os.path.exists(workflow_path):
            os.remove(workflow_path)
            return True
        return False

    def _save_workflow(self, workflow: Workflow) -> None:
        """
        Save a workflow to disk.

        Args:
            workflow: Workflow to save
        """
        workflow_path = os.path.join(self.storage_dir, f"{workflow.id}.json")
        with open(workflow_path, "w") as f:
            json.dump(self._serialize_workflow(workflow), f, indent=2)

    def _serialize_workflow(self, workflow: Workflow) -> Dict[str, Any]:
        """
        Serialize a workflow to a dictionary.

        Args:
            workflow: Workflow to serialize

        Returns:
            Dictionary representation of the workflow
        """
        return workflow.to_dict()

    def _deserialize_workflow(self, data: Dict[str, Any]) -> Workflow:
        """
        Deserialize a workflow from a dictionary.
        """
        return Workflow.from_dict(data)

```

### src/core/credentials/credential_manager.py

**Created:** 2025-03-30 12:08:15
**Modified:** 2025-03-30 12:08:15
**Size:** 22556 bytes

**Code:**

```python
"""Credential management for tracking and filtering credentials"""
import csv
import json
import logging
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set


class CredentialStatus(Enum):
    """Status of a credential"""

    UNUSED = auto()  # Credential has not been used yet
    SUCCESS = auto()  # Credential was used successfully
    FAILURE = auto()  # Credential failed to authenticate
    LOCKED = auto()  # Account is locked or requires additional verification
    EXPIRED = auto()  # Credential has expired
    INVALID = auto()  # Credential format is invalid
    BLACKLISTED = auto()  # Credential has been blacklisted


class CredentialRecord:
    """
    Record of a credential and its usage history

    This class tracks a credential and its usage history, including
    success/failure status, timestamps, and additional metadata.
    """

    def __init__(
        self,
        username: str,
        password: str,
        status: CredentialStatus = CredentialStatus.UNUSED,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the credential record

        Args:
            username: Username or identifier
            password: Password or secret
            status: Initial status of the credential
            metadata: Additional metadata for the credential
        """
        self.username = username
        self.password = password
        self.status = status
        self.metadata = metadata or {}
        self.attempts = 0
        self.last_used = None
        self.last_result = None
        self.history = []

    def record_attempt(
        self,
        success: bool,
        message: str,
        status: Optional[CredentialStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record an authentication attempt

        Args:
            success: Whether the attempt was successful
            message: Result message
            status: New status for the credential (if None, will be set based on success)
            metadata: Additional metadata for the attempt
        """
        # Increment attempt counter
        self.attempts += 1

        # Set timestamp
        timestamp = datetime.now()
        self.last_used = timestamp

        # Set result
        self.last_result = {
            "success": success,
            "message": message,
            "timestamp": timestamp,
            "metadata": metadata or {},
        }

        # Add to history
        self.history.append(self.last_result)

        # Update status
        if status:
            self.status = status
        elif success:
            self.status = CredentialStatus.SUCCESS
        else:
            self.status = CredentialStatus.FAILURE

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the credential record to a dictionary

        Returns:
            Dictionary representation of the credential record
        """
        return {
            "username": self.username,
            "password": self.password,
            "status": self.status.name,
            "attempts": self.attempts,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "last_result": self.last_result,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CredentialRecord":
        """
        Create a credential record from a dictionary

        Args:
            data: Dictionary representation of the credential record

        Returns:
            Credential record
        """
        # Create the record
        record = cls(
            username=data["username"],
            password=data["password"],
            status=CredentialStatus[data["status"]]
            if "status" in data
            else CredentialStatus.UNUSED,
            metadata=data.get("metadata", {}),
        )

        # Set additional properties
        record.attempts = data.get("attempts", 0)

        if "last_used" in data and data["last_used"]:
            record.last_used = datetime.fromisoformat(data["last_used"])

        record.last_result = data.get("last_result")
        record.history = data.get("history", [])

        return record


class CredentialManager:
    """
    Manager for tracking and filtering credentials

    This class manages a set of credentials, tracks their usage,
    and provides methods for filtering and exporting them.
    """

    def __init__(self):
        """Initialize the credential manager"""
        self.credentials: Dict[str, CredentialRecord] = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_credential(
        self,
        username: str,
        password: str,
        status: CredentialStatus = CredentialStatus.UNUSED,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CredentialRecord:
        """
        Add a credential to the manager

        Args:
            username: Username or identifier
            password: Password or secret
            status: Initial status of the credential
            metadata: Additional metadata for the credential

        Returns:
            The credential record
        """
        # Create the credential record
        record = CredentialRecord(username, password, status, metadata)

        # Add to the credentials dictionary
        self.credentials[username] = record

        return record

    def get_credential(self, username: str) -> Optional[CredentialRecord]:
        """
        Get a credential by username

        Args:
            username: Username to look up

        Returns:
            Credential record, or None if not found
        """
        return self.credentials.get(username)

    def record_attempt(
        self,
        username: str,
        success: bool,
        message: str,
        status: Optional[CredentialStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record an authentication attempt for a credential

        Args:
            username: Username of the credential
            success: Whether the attempt was successful
            message: Result message
            status: New status for the credential
            metadata: Additional metadata for the attempt

        Raises:
            KeyError: If the credential is not found
        """
        # Get the credential record
        record = self.get_credential(username)

        if not record:
            raise KeyError(f"Credential not found: {username}")

        # Record the attempt
        record.record_attempt(success, message, status, metadata)

    def get_credentials_by_status(
        self, status: CredentialStatus
    ) -> List[CredentialRecord]:
        """
        Get credentials by status

        Args:
            status: Status to filter by

        Returns:
            List of credential records with the specified status
        """
        return [
            record for record in self.credentials.values() if record.status == status
        ]

    def get_failed_credentials(self) -> List[CredentialRecord]:
        """
        Get credentials that have failed authentication

        Returns:
            List of credential records with failure status
        """
        return self.get_credentials_by_status(CredentialStatus.FAILURE)

    def get_successful_credentials(self) -> List[CredentialRecord]:
        """
        Get credentials that have successfully authenticated

        Returns:
            List of credential records with success status
        """
        return self.get_credentials_by_status(CredentialStatus.SUCCESS)

    def get_unused_credentials(self) -> List[CredentialRecord]:
        """
        Get credentials that have not been used

        Returns:
            List of credential records with unused status
        """
        return self.get_credentials_by_status(CredentialStatus.UNUSED)

    def remove_credential(self, username: str) -> bool:
        """
        Remove a credential from the manager

        Args:
            username: Username of the credential to remove

        Returns:
            True if the credential was removed, False if not found
        """
        if username in self.credentials:
            del self.credentials[username]
            return True
        return False

    def remove_credentials_by_status(self, status: CredentialStatus) -> int:
        """
        Remove credentials with a specific status

        Args:
            status: Status to filter by

        Returns:
            Number of credentials removed
        """
        # Get usernames to remove
        usernames = [
            record.username
            for record in self.credentials.values()
            if record.status == status
        ]

        # Remove the credentials
        for username in usernames:
            self.remove_credential(username)

        return len(usernames)

    def remove_failed_credentials(self) -> int:
        """
        Remove credentials that have failed authentication

        Returns:
            Number of credentials removed
        """
        return self.remove_credentials_by_status(CredentialStatus.FAILURE)

    def update_credential_status(self, username: str, status: CredentialStatus) -> bool:
        """
        Update the status of a credential

        Args:
            username: Username of the credential to update
            status: New status for the credential

        Returns:
            True if the credential was updated, False if not found
        """
        record = self.get_credential(username)
        if record:
            record.status = status
            return True
        return False

    def update_credentials_status(
        self, from_status: CredentialStatus, to_status: CredentialStatus
    ) -> int:
        """
        Update the status of all credentials with a specific status

        Args:
            from_status: Current status to match
            to_status: New status to set

        Returns:
            Number of credentials updated
        """
        # Get credentials with the specified status
        records = self.get_credentials_by_status(from_status)

        # Update their status
        for record in records:
            record.status = to_status

        return len(records)

    def load_from_csv(
        self,
        file_path: str,
        username_field: str = "username",
        password_field: str = "password",
        delimiter: str = ",",
    ) -> int:
        """
        Load credentials from a CSV file

        Args:
            file_path: Path to the CSV file
            username_field: Name of the username field
            password_field: Name of the password field
            delimiter: Field delimiter

        Returns:
            Number of credentials loaded

        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If the file cannot be read
        """
        try:
            # Open the CSV file
            with open(file_path, "r", newline="") as file:
                # Create a CSV reader
                reader = csv.DictReader(file, delimiter=delimiter)

                # Check that the required fields are present
                if (
                    username_field not in reader.fieldnames
                    or password_field not in reader.fieldnames
                ):
                    raise ValueError(
                        f"CSV file must contain {username_field} and {password_field} fields"
                    )

                # Load the credentials
                count = 0
                for row in reader:
                    username = row[username_field]
                    password = row[password_field]

                    # Create metadata from other fields
                    metadata = {
                        key: value
                        for key, value in row.items()
                        if key not in [username_field, password_field]
                    }

                    # Add the credential
                    self.add_credential(username, password, metadata=metadata)
                    count += 1

                self.logger.info(f"Loaded {count} credentials from {file_path}")
                return count

        except (FileNotFoundError, IOError) as e:
            self.logger.error(f"Failed to load credentials from {file_path}: {str(e)}")
            raise

    def save_to_csv(
        self,
        file_path: str,
        username_field: str = "username",
        password_field: str = "password",
        include_status: bool = True,
        include_metadata: bool = True,
        delimiter: str = ",",
        filter_status: Optional[Set[CredentialStatus]] = None,
    ) -> int:
        """
        Save credentials to a CSV file

        Args:
            file_path: Path to the CSV file
            username_field: Name of the username field
            password_field: Name of the password field
            include_status: Whether to include the status field
            include_metadata: Whether to include metadata fields
            delimiter: Field delimiter
            filter_status: Set of statuses to include (None for all)

        Returns:
            Number of credentials saved

        Raises:
            IOError: If the file cannot be written
        """
        try:
            # Get the credentials to save
            if filter_status:
                credentials = [
                    record
                    for record in self.credentials.values()
                    if record.status in filter_status
                ]
            else:
                credentials = list(self.credentials.values())

            # If there are no credentials, don't create the file
            if not credentials:
                self.logger.warning(f"No credentials to save to {file_path}")
                return 0

            # Determine the fieldnames
            fieldnames = [username_field, password_field]

            if include_status:
                fieldnames.append("status")

            if include_metadata:
                # Get all metadata keys
                metadata_keys = set()
                for record in credentials:
                    metadata_keys.update(record.metadata.keys())

                # Add metadata fields
                fieldnames.extend(sorted(metadata_keys))

            # Open the CSV file
            with open(file_path, "w", newline="") as file:
                # Create a CSV writer
                writer = csv.DictWriter(
                    file, fieldnames=fieldnames, delimiter=delimiter
                )

                # Write the header
                writer.writeheader()

                # Write the credentials
                for record in credentials:
                    row = {
                        username_field: record.username,
                        password_field: record.password,
                    }

                    if include_status:
                        row["status"] = record.status.name

                    if include_metadata:
                        for key, value in record.metadata.items():
                            row[key] = value

                    writer.writerow(row)

                self.logger.info(f"Saved {len(credentials)} credentials to {file_path}")
                return len(credentials)

        except IOError as e:
            self.logger.error(f"Failed to save credentials to {file_path}: {str(e)}")
            raise

    def load_from_json(self, file_path: str) -> int:
        """
        Load credentials from a JSON file

        Args:
            file_path: Path to the JSON file

        Returns:
            Number of credentials loaded

        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If the file cannot be read
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            # Open the JSON file
            with open(file_path, "r") as file:
                # Load the JSON data
                data = json.load(file)

                # Check that the data is a list
                if not isinstance(data, list):
                    raise ValueError("JSON file must contain a list of credentials")

                # Load the credentials
                count = 0
                for item in data:
                    # Check that the item is a dictionary
                    if not isinstance(item, dict):
                        continue

                    # Check that the required fields are present
                    if "username" not in item or "password" not in item:
                        continue

                    # Create the credential record
                    record = CredentialRecord.from_dict(item)

                    # Add to the credentials dictionary
                    self.credentials[record.username] = record
                    count += 1

                self.logger.info(f"Loaded {count} credentials from {file_path}")
                return count

        except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load credentials from {file_path}: {str(e)}")
            raise

    def save_to_json(
        self,
        file_path: str,
        include_history: bool = False,
        filter_status: Optional[Set[CredentialStatus]] = None,
    ) -> int:
        """
        Save credentials to a JSON file

        Args:
            file_path: Path to the JSON file
            include_history: Whether to include the attempt history
            filter_status: Set of statuses to include (None for all)

        Returns:
            Number of credentials saved

        Raises:
            IOError: If the file cannot be written
        """
        try:
            # Get the credentials to save
            if filter_status:
                credentials = [
                    record
                    for record in self.credentials.values()
                    if record.status in filter_status
                ]
            else:
                credentials = list(self.credentials.values())

            # If there are no credentials, don't create the file
            if not credentials:
                self.logger.warning(f"No credentials to save to {file_path}")
                return 0

            # Convert the credentials to dictionaries
            data = []
            for record in credentials:
                item = record.to_dict()

                if include_history:
                    item["history"] = record.history

                data.append(item)

            # Open the JSON file
            with open(file_path, "w") as file:
                # Write the JSON data
                json.dump(data, file, indent=2)

                self.logger.info(f"Saved {len(credentials)} credentials to {file_path}")
                return len(credentials)

        except IOError as e:
            self.logger.error(f"Failed to save credentials to {file_path}: {str(e)}")
            raise

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the credentials

        Returns:
            Dictionary of statistics including:
            - total: Total number of credentials
            - active: Number of active credentials (not blacklisted, locked, or expired)
            - inactive: Number of inactive credentials (blacklisted, locked, or expired)
            - status_counts: Count of credentials by status
            - total_attempts: Total number of login attempts
            - successful_attempts: Number of successful login attempts
            - failed_attempts: Number of failed login attempts
            - success_rate: Ratio of successful attempts to total attempts
            - average_attempts: Average number of attempts per credential
        """
        # Count credentials by status
        status_counts = {}
        for status in CredentialStatus:
            status_counts[status.name] = len(self.get_credentials_by_status(status))

        # Calculate active and inactive counts
        inactive_statuses = [
            CredentialStatus.BLACKLISTED,
            CredentialStatus.LOCKED,
            CredentialStatus.EXPIRED,
            CredentialStatus.INVALID
        ]
        inactive_count = sum(status_counts[status.name] for status in inactive_statuses)
        active_count = len(self.credentials) - inactive_count

        # Calculate attempt statistics
        total_attempts = 0
        successful_attempts = 0
        failed_attempts = 0

        for record in self.credentials.values():
            total_attempts += record.attempts
            for attempt in record.history:
                if attempt.get("success", False):
                    successful_attempts += 1
                else:
                    failed_attempts += 1

        # Calculate success rate
        success_rate = (
            successful_attempts / total_attempts
            if total_attempts > 0
            else 0
        )

        # Calculate average attempts per credential
        average_attempts = (
            total_attempts / len(self.credentials)
            if len(self.credentials) > 0
            else 0
        )

        return {
            "total": len(self.credentials),
            "active": active_count,
            "inactive": inactive_count,
            "status_counts": status_counts,
            "total_attempts": total_attempts,
            "successful_attempts": successful_attempts,
            "failed_attempts": failed_attempts,
            "success_rate": success_rate,
            "average_attempts": average_attempts,
        }

```

### src/core/context/variable_storage.py

**Created:** 2025-03-28 06:38:08
**Modified:** 2025-03-28 06:38:08
**Size:** 12370 bytes

**Code:**

```python
"""Variable storage for the execution context"""
import copy
import re
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Callable, Union, Set, Tuple


class VariableScope(Enum):
    """Enumeration of variable scopes"""
    GLOBAL = auto()    # Variables available to all contexts
    WORKFLOW = auto()  # Variables available to the current workflow
    LOCAL = auto()     # Variables available only to the current context


class VariableChangeEvent:
    """Event raised when a variable changes"""

    def __init__(self, name: str, old_value: Any, new_value: Any, scope: VariableScope):
        """
        Initialize the variable change event

        Args:
            name: Name of the variable
            old_value: Previous value (None if variable is new)
            new_value: New value
            scope: Scope of the variable
        """
        self.name = name
        self.old_value = old_value
        self.new_value = new_value
        self.scope = scope

    def __str__(self) -> str:
        """String representation of the variable change event"""
        return f"VariableChangeEvent: {self.scope.name}.{self.name} = {self.new_value}"


class VariableStorage:
    """Storage for variables with scoping"""

    def __init__(self, parent: Optional['VariableStorage'] = None):
        """
        Initialize the variable storage

        Args:
            parent: Optional parent storage for variable inheritance
        """
        self._variables: Dict[VariableScope, Dict[str, Any]] = {
            VariableScope.GLOBAL: {},
            VariableScope.WORKFLOW: {},
            VariableScope.LOCAL: {}
        }
        self._parent = parent
        self._variable_change_listeners: List[Callable[[VariableChangeEvent], None]] = []
        self._variable_name_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    def get(self, name: str, default: Any = None) -> Any:
        """
        Get a variable value

        Args:
            name: Name of the variable
            default: Default value if variable doesn't exist

        Returns:
            Variable value or default if not found
        """
        # Check local scope first
        if name in self._variables[VariableScope.LOCAL]:
            return copy.deepcopy(self._variables[VariableScope.LOCAL][name])

        # Then check workflow scope
        if name in self._variables[VariableScope.WORKFLOW]:
            return copy.deepcopy(self._variables[VariableScope.WORKFLOW][name])

        # Then check global scope
        if name in self._variables[VariableScope.GLOBAL]:
            return copy.deepcopy(self._variables[VariableScope.GLOBAL][name])

        # If we have a parent, check there
        if self._parent:
            return self._parent.get(name, default)

        # Not found, return default
        return default

    def set(self, name: str, value: Any, scope: VariableScope = VariableScope.WORKFLOW) -> None:
        """
        Set a variable value

        Args:
            name: Name of the variable
            value: Value to set
            scope: Scope of the variable

        Raises:
            ValueError: If the variable name is invalid
        """
        self._validate_variable_name(name)

        # Get the old value (if any)
        old_value = None
        if name in self._variables[scope]:
            old_value = self._variables[scope][name]

        # Set the new value (make a deep copy to prevent modification)
        self._variables[scope][name] = copy.deepcopy(value)

        # Notify listeners
        self._notify_variable_change(VariableChangeEvent(name, old_value, value, scope))

    def delete(self, name: str, scope: Optional[VariableScope] = None) -> bool:
        """
        Delete a variable

        Args:
            name: Name of the variable
            scope: Scope of the variable (if None, delete from all scopes)

        Returns:
            True if the variable was deleted, False if not found
        """
        deleted = False

        if scope:
            # Delete from specific scope
            if name in self._variables[scope]:
                old_value = self._variables[scope][name]
                del self._variables[scope][name]
                self._notify_variable_change(VariableChangeEvent(name, old_value, None, scope))
                deleted = True
        else:
            # Delete from all scopes
            for s in VariableScope:
                if name in self._variables[s]:
                    old_value = self._variables[s][name]
                    del self._variables[s][name]
                    self._notify_variable_change(VariableChangeEvent(name, old_value, None, s))
                    deleted = True

        return deleted

    def clear_scope(self, scope: VariableScope) -> None:
        """
        Clear all variables in a scope

        Args:
            scope: Scope to clear
        """
        # Create a copy of the variables to notify about
        variables = list(self._variables[scope].items())

        # Clear the scope
        self._variables[scope].clear()

        # Notify listeners
        for name, old_value in variables:
            self._notify_variable_change(VariableChangeEvent(name, old_value, None, scope))

    def clear_all(self) -> None:
        """Clear all variables in all scopes"""
        for scope in VariableScope:
            self.clear_scope(scope)

    def get_all(self, scope: Optional[VariableScope] = None) -> Dict[str, Any]:
        """
        Get all variables in a scope or all scopes

        Args:
            scope: Scope to get variables from (if None, get from all scopes)

        Returns:
            Dictionary of variable names and values
        """
        result: Dict[str, Any] = {}

        if scope:
            # Get from specific scope
            result.update(copy.deepcopy(self._variables[scope]))
        else:
            # Get from all scopes (local overrides workflow overrides global)
            if self._parent:
                # Start with parent variables
                result.update(self._parent.get_all())

            # Add global variables
            result.update(copy.deepcopy(self._variables[VariableScope.GLOBAL]))

            # Add workflow variables
            result.update(copy.deepcopy(self._variables[VariableScope.WORKFLOW]))

            # Add local variables
            result.update(copy.deepcopy(self._variables[VariableScope.LOCAL]))

        return result

    def get_names(self, scope: Optional[VariableScope] = None) -> Set[str]:
        """
        Get all variable names in a scope or all scopes

        Args:
            scope: Scope to get variable names from (if None, get from all scopes)

        Returns:
            Set of variable names
        """
        if scope:
            # Get from specific scope
            return set(self._variables[scope].keys())
        else:
            # Get from all scopes
            names = set()
            if self._parent:
                names.update(self._parent.get_names())
            for s in VariableScope:
                names.update(self._variables[s].keys())
            return names

    def has(self, name: str, scope: Optional[VariableScope] = None) -> bool:
        """
        Check if a variable exists

        Args:
            name: Name of the variable
            scope: Scope to check (if None, check all scopes)

        Returns:
            True if the variable exists, False otherwise
        """
        if scope:
            # Check specific scope
            return name in self._variables[scope]
        else:
            # Check all scopes
            for s in VariableScope:
                if name in self._variables[s]:
                    return True
            # Check parent if we have one
            if self._parent:
                return self._parent.has(name)
            return False

    def get_scope(self, name: str) -> Optional[VariableScope]:
        """
        Get the scope of a variable

        Args:
            name: Name of the variable

        Returns:
            Scope of the variable or None if not found
        """
        # Check local scope first
        if name in self._variables[VariableScope.LOCAL]:
            return VariableScope.LOCAL

        # Then check workflow scope
        if name in self._variables[VariableScope.WORKFLOW]:
            return VariableScope.WORKFLOW

        # Then check global scope
        if name in self._variables[VariableScope.GLOBAL]:
            return VariableScope.GLOBAL

        # If we have a parent, check there
        if self._parent:
            return self._parent.get_scope(name)

        # Not found
        return None

    def add_variable_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Add a listener for variable change events

        Args:
            listener: Callback function that will be called when variables change
        """
        if listener not in self._variable_change_listeners:
            self._variable_change_listeners.append(listener)

    def remove_variable_change_listener(self, listener: Callable[[VariableChangeEvent], None]) -> None:
        """
        Remove a variable change listener

        Args:
            listener: Listener to remove
        """
        if listener in self._variable_change_listeners:
            self._variable_change_listeners.remove(listener)

    def _notify_variable_change(self, event: VariableChangeEvent) -> None:
        """
        Notify all listeners of a variable change

        Args:
            event: Variable change event
        """
        for listener in self._variable_change_listeners:
            try:
                listener(event)
            except Exception as e:
                # In a real application, you might want to log this error
                print(f"Error in variable change listener: {str(e)}")

    def _validate_variable_name(self, name: str) -> None:
        """
        Validate a variable name

        Args:
            name: Name to validate

        Raises:
            ValueError: If the name is invalid
        """
        if not name:
            raise ValueError("Variable name cannot be empty")

        if not self._variable_name_pattern.match(name):
            raise ValueError(
                f"Invalid variable name: {name}. "
                "Variable names must start with a letter or underscore "
                "and contain only letters, numbers, and underscores."
            )

    def clone(self) -> 'VariableStorage':
        """
        Create a clone of this variable storage

        Returns:
            New variable storage with the same variables
        """
        clone = VariableStorage(parent=self._parent)
        for scope in VariableScope:
            clone._variables[scope] = copy.deepcopy(self._variables[scope])
        return clone

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the variable storage to a dictionary

        Returns:
            Dictionary representation of the variable storage
        """
        return {
            "variables": {
                scope.name: copy.deepcopy(variables)
                for scope, variables in self._variables.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional['VariableStorage'] = None) -> 'VariableStorage':
        """
        Create a variable storage from a dictionary

        Args:
            data: Dictionary representation of the variable storage
            parent: Optional parent storage

        Returns:
            Instantiated variable storage
        """
        instance = cls(parent=parent)

        variables_data = data.get("variables", {})
        for scope_name, variables in variables_data.items():
            scope = VariableScope[scope_name]
            instance._variables[scope] = copy.deepcopy(variables)

        return instance

```

### src/core/actions/action_factory.py

**Created:** 2025-03-30 12:08:15
**Modified:** 2025-04-03 14:22:19
**Size:** 5048 bytes

**Code:**

```python
"""Factory for creating actions"""
import importlib
import inspect
from typing import Dict, Any, Type, Optional, Callable

from src.core.actions.base_action import BaseAction


class ActionFactory:
    """Factory for creating and managing actions"""

    _instance: Optional['ActionFactory'] = None
    _registry: Dict[str, Type[BaseAction]] = {}

    def __new__(cls) -> 'ActionFactory':
        """Create a new instance or return the existing one (singleton pattern)"""
        if cls._instance is None:
            cls._instance = super(ActionFactory, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'ActionFactory':
        """Get the singleton instance of the factory"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_action_types(self) -> list:
        """
        Get all registered action types.

        Returns:
            List of action type names
        """
        return list(self._registry.keys())

    def register_action_type(self, action_type: str, action_class: Type[BaseAction]) -> None:
        """
        Register an action type with its implementation class

        Args:
            action_type: String identifier for the action type
            action_class: Implementation class for the action type

        Raises:
            TypeError: If action_class is not a subclass of BaseAction
        """
        # Validate that the action class inherits from BaseAction
        if not issubclass(action_class, BaseAction):
            raise TypeError(f"Action class must inherit from BaseAction: {action_class.__name__}")

        # Register the action type
        self._registry[action_type] = action_class

    def create_action(self, action_data: Dict[str, Any]) -> BaseAction:
        """
        Create an action instance from the given data

        Args:
            action_data: Dictionary containing action configuration

        Returns:
            Instantiated action

        Raises:
            ValueError: If the action type is unknown
        """
        return self.create_from_dict(action_data)

    def create_from_dict(self, action_data: Dict[str, Any]) -> BaseAction:
        """
        Create an action from a dictionary representation

        Args:
            action_data: Dictionary containing action configuration

        Returns:
            Instantiated action

        Raises:
            ValueError: If the action type is unknown
        """
        action_type = action_data.get("type")
        if not action_type or action_type not in self._registry:
            raise ValueError(f"Unknown action type: {action_type}")

        # Get the action class and create an instance
        action_class = self._registry[action_type]
        return action_class.from_dict(action_data)

    def load_actions_from_module(self, module_name: str) -> None:
        """
        Load and register all action classes from a module

        Args:
            module_name: Name of the module to load actions from
        """
        # Import the module
        module = importlib.import_module(module_name)

        # Get all classes defined in the module
        for name in getattr(module, "__all__", dir(module)):
            item = getattr(module, name, None)

            # Check if the item is a class that inherits from BaseAction
            if (
                inspect.isclass(item)
                and issubclass(item, BaseAction)
                and item is not BaseAction
            ):
                # Register the action type using the type property
                action_instance = item("Temporary instance for type detection")
                action_type = action_instance.type
                self.register_action_type(action_type, item)

    @classmethod
    def reset_registry(cls) -> None:
        """
        Reset the action registry

        This is primarily used for testing to ensure a clean state.
        """
        cls._registry = {}
        cls._instance = None

    @classmethod
    def register(cls, action_type: str) -> Callable[[Type[BaseAction]], Type[BaseAction]]:
        """
        Decorator for registering action classes

        Args:
            action_type: String identifier for the action type

        Returns:
            Decorator function that registers the action class
        """
        def decorator(action_class: Type[BaseAction]) -> Type[BaseAction]:
            # Validate that the action class inherits from BaseAction
            if not issubclass(action_class, BaseAction):
                raise TypeError(f"Action class must inherit from BaseAction: {action_class.__name__}")

            # Register the action type
            factory = cls.get_instance()
            factory.register_action_type(action_type, action_class)
            return action_class

        return decorator

```

### src/core/workflow/workflow_service.py

**Created:** 2025-03-31 15:37:48
**Modified:** 2025-04-03 15:25:31
**Size:** 10086 bytes

**Code:**

```python
from src.core.workflow.workflow_validation_service import WorkflowValidationService
from src.core.workflow.workflow_storage_service import WorkflowStorageService
"""
Workflow service for managing workflows.

This service acts as an intermediary between the UI and the workflow engine,
providing methods for workflow CRUD operations, validation, persistence, and execution.

SOLID: Single responsibility - manages workflow operations.
KISS: Simple interface for workflow management.
"""
import json
import os
import uuid
import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime

from src.core.models import Workflow, WorkflowNode, WorkflowConnection
from src.core.workflow.workflow_engine_new import WorkflowEngine
from src.core.workflow.workflow_event import WorkflowEventType
from src.core.actions.base_action import BaseAction
from src.core.context.execution_context import ExecutionContext


class WorkflowService:
    """Service for managing workflows."""

    def __init__(self, storage_dir: str = "workflows"):
        """
        Initialize the workflow service.

        Args:
            storage_dir: Directory for storing workflow files
        """
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.info("Initializing OLD WorkflowService implementation")
        self.storage_dir = storage_dir
        self.workflows: Dict[str, Workflow] = {}
        self.workflow_storage_service = WorkflowStorageService(storage_dir=self.storage_dir) # Instantiate storage service
        self.workflow_engine = WorkflowEngine()

        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)

        # Load existing workflows
        self._load_workflows() # Load workflows via storage service

    def _load_workflows(self) -> None:
        """Load all workflows from the storage directory."""
        if not os.path.exists(self.storage_dir):
            return
        loaded_workflows = self.workflow_storage_service._load_workflows()
        if loaded_workflows:
            self.workflows = {wf.id: wf for wf in loaded_workflows}

    def get_workflows(self) -> List[Workflow]:
        """
        Get all workflows.

        Returns:
            List of all workflows
        """
        return list(self.workflows.values())

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Get a workflow by ID.

        Args:
            workflow_id: ID of the workflow to get

        Returns:
            Workflow or None if not found
        """
        return self.workflows.get(workflow_id)

    def create_workflow(self, workflow: Workflow) -> Workflow:
        """
        Create a new workflow.

        Args:
            workflow: Workflow to create

        Returns:
            Created workflow

        Raises:
            ValueError: If a workflow with the same ID already exists
        """
        if workflow.id in self.workflows:
            raise ValueError(f"Workflow with ID {workflow.id} already exists")

        # Add creation metadata
        if "created_at" not in workflow.metadata:
            workflow.metadata["created_at"] = datetime.now().isoformat()
        workflow.metadata["updated_at"] = datetime.now().isoformat()
        workflow.metadata["version"] = 1

        # Validate the workflow
        validator = WorkflowValidationService()
        validator.validate_workflow(workflow)

        # Store the workflow
        self.workflows[workflow.id] = workflow

        # Save the workflow to disk
        self.workflow_storage_service._save_workflow(workflow) # Delegate to storage service

        self.logger.info(f"Created workflow: {workflow.name} ({workflow.id})")
        return workflow

    def update_workflow(self, workflow: Workflow) -> Workflow:
        """
        Update an existing workflow.

        Args:
            workflow: Workflow to update

        Returns:
            Updated workflow

        Raises:
            ValueError: If the workflow doesn't exist
        """
        if workflow.id not in self.workflows:
            raise ValueError(f"Workflow with ID {workflow.id} not found")

        # Update metadata
        workflow.metadata["updated_at"] = datetime.now().isoformat()

        # Increment version
        if "version" in workflow.metadata:
            workflow.metadata["version"] = workflow.metadata["version"] + 1
        else:
            workflow.metadata["version"] = 1

        # Validate the workflow
        validator = WorkflowValidationService()
        validator.validate_workflow(workflow)

        # Store the workflow
        self.workflows[workflow.id] = workflow

        # Save the workflow to disk
        self.workflow_storage_service._save_workflow(workflow) # Delegate to storage service

        self.logger.info(f"Updated workflow: {workflow.name} ({workflow.id})")
        return workflow

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.

        Args:
            workflow_id: ID of the workflow to delete

        Returns:
            True if the workflow was deleted, False if it wasn't found
        """
        if workflow_id not in self.workflows:
            return False

        # Remove from memory
        workflow = self.workflows.pop(workflow_id)

        # Delete workflow file from disk via storage service
        return self.workflow_storage_service.delete_workflow(workflow_id) # Delegate to storage service

    def execute_workflow(
        self,
        workflow_id: str,
        context: Optional[ExecutionContext] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow.

        Args:
            workflow_id: ID of the workflow to execute
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found")

        # Validate the workflow before execution
        validator = WorkflowValidationService()
        validator.validate_workflow(workflow)

        # Convert workflow to actions
        actions = self._workflow_to_actions(workflow)

        # Execute the workflow
        self.logger.info(f"Executing workflow: {workflow.name} ({workflow.id})")
        return self.workflow_engine.execute_workflow(actions, context, workflow_id)

    def get_node_types(self) -> List[Dict[str, Any]]:
        """
        Get all available node types.

        Returns:
            List of node type definitions
        """
        # This would typically come from a registry of node types
        # For now, we'll return a static list
        return [
            {
                "type": "Start",
                "name": "Start", # Added name
                "category": "Flow Control",
                "description": "Starting point of the workflow",
                "color": "#4CAF50",  # Green
                "properties": {}
            },
            {
                "type": "End",
                "name": "End", # Added name
                "category": "Flow Control",
                "description": "End point of the workflow",
                "color": "#F44336",  # Red
                "properties": {}
            },
            {
                "type": "Click",
                "name": "Click Element", # Added name
                "category": "Actions",
                "description": "Click on an element",
                "color": "#2196F3",  # Blue
                "properties": {
                    "selector": {"type": "string", "default": ""},
                    "wait_time": {"type": "number", "default": 1}
                }
            },
            {
                "type": "Type",
                "name": "Type Text", # Added name
                "category": "Actions",
                "description": "Type text into an element",
                "color": "#9C27B0",  # Purple
                "properties": {
                    "selector": {"type": "string", "default": ""},
                    "text": {"type": "string", "default": ""},
                    "clear_first": {"type": "boolean", "default": True}
                }
            },
            {
                "type": "Wait",
                "name": "Wait", # Added name
                "category": "Flow Control",
                "description": "Wait for a specified time",
                "color": "#FF9800",  # Orange
                "properties": {
                    "seconds": {"type": "number", "default": 1}
                }
            },
            {
                "type": "Condition",
                "name": "Condition (If)", # Added name
                "category": "Flow Control",
                "description": "Branch based on a condition",
                "color": "#FFEB3B",  # Yellow
                "properties": {
                    "condition": {"type": "string", "default": ""}
                }
            },
            {
                "type": "Loop",
                "name": "Loop", # Added name
                "category": "Flow Control",
                "description": "Repeat a sequence of actions",
                "color": "#795548",  # Brown
                "properties": {
                    "iterations": {"type": "number", "default": 1},
                    "variable": {"type": "string", "default": ""}
                }
            }
        ]

    def _workflow_to_actions(self, workflow: Workflow) -> List[BaseAction]:
        """
        Convert a workflow to a list of actions.

        Args:
            workflow: Workflow to convert

        Returns:
            List of actions

        Note:
            This is a placeholder implementation. In a real application,
            this would convert the workflow graph to a linear sequence of actions,
            handling conditions, loops, etc.
        """
        # This is a placeholder implementation
        # In a real application, this would convert the workflow graph to a linear sequence of actions
        return []

```

### src/core/context/execution_context.py

**Created:** 2025-03-28 06:38:08
**Modified:** 2025-03-28 06:38:08
**Size:** 8451 bytes

**Code:**

```python
"""Execution context for the automation system"""
import uuid
from typing import Dict, Any, Optional, List, Set, Callable

from src.core.context.execution_state import ExecutionState, ExecutionStateEnum, StateChangeEvent
from src.core.context.variable_storage import VariableStorage, VariableScope, VariableChangeEvent
from src.core.context.context_options import ContextOptions


class ExecutionContext:
    """Context for executing actions with variable storage and state tracking"""

    def __init__(
        self,
        parent: Optional['ExecutionContext'] = None,
        options: Optional[ContextOptions] = None,
        context_id: Optional[str] = None
    ):
        """
        Initialize the execution context

        Args:
            parent: Optional parent context for inheritance
            options: Configuration options
            context_id: Optional unique identifier (generated if not provided)
        """
        self.id = context_id or str(uuid.uuid4())
        self.options = options or ContextOptions()
        self.parent = parent

        # Initialize variable storage with parent if needed
        parent_storage = parent.variables if parent and self.options.inherit_variables else None
        self.variables = VariableStorage(parent=parent_storage)

        # Initialize execution state
        self.state = ExecutionState()

        # Track child contexts
        self._children: List['ExecutionContext'] = []

        # Add this context as a child of the parent
        if parent:
            parent._add_child(self)

        # Set up event forwarding if tracking is enabled
        if self.options.track_variable_changes:
            self.variables.add_variable_change_listener(self._on_variable_change)

        if self.options.track_state_changes:
            self.state.add_state_change_listener(self._on_state_change)

        # Event history
        self._variable_change_history: List[VariableChangeEvent] = []
        self._state_change_history: List[StateChangeEvent] = []

    def _add_child(self, child: 'ExecutionContext') -> None:
        """
        Add a child context

        Args:
            child: Child context to add
        """
        if child not in self._children:
            self._children.append(child)

    def _remove_child(self, child: 'ExecutionContext') -> None:
        """
        Remove a child context

        Args:
            child: Child context to remove
        """
        if child in self._children:
            self._children.remove(child)

    def create_child(self, options: Optional[ContextOptions] = None) -> 'ExecutionContext':
        """
        Create a child context

        Args:
            options: Optional configuration options for the child

        Returns:
            New child context
        """
        return ExecutionContext(parent=self, options=options)

    def dispose(self) -> None:
        """
        Dispose of the context and clean up resources

        This removes the context from its parent and clears all variables
        """
        # Remove from parent
        if self.parent:
            self.parent._remove_child(self)
            self.parent = None

        # Clear variables
        self.variables.clear_all()

        # Dispose of children
        for child in list(self._children):
            child.dispose()

    def _on_variable_change(self, event: VariableChangeEvent) -> None:
        """
        Handle variable change events

        Args:
            event: Variable change event
        """
        # Add to history
        self._variable_change_history.append(event)

        # Trim history if needed
        if (
            self.options.max_variable_history > 0
            and len(self._variable_change_history) > self.options.max_variable_history
        ):
            self._variable_change_history = self._variable_change_history[-self.options.max_variable_history:]

    def _on_state_change(self, event: StateChangeEvent) -> None:
        """
        Handle state change events

        Args:
            event: State change event
        """
        # Add to history
        self._state_change_history.append(event)

        # Trim history if needed
        if (
            self.options.max_state_history > 0
            and len(self._state_change_history) > self.options.max_state_history
        ):
            self._state_change_history = self._state_change_history[-self.options.max_state_history:]

    def get_variable_change_history(self) -> List[VariableChangeEvent]:
        """
        Get the history of variable changes

        Returns:
            List of variable change events
        """
        return self._variable_change_history.copy()

    def get_state_change_history(self) -> List[StateChangeEvent]:
        """
        Get the history of state changes

        Returns:
            List of state change events
        """
        return self._state_change_history.copy()

    def clone(self, include_children: bool = False) -> 'ExecutionContext':
        """
        Create a clone of this context

        Args:
            include_children: Whether to clone child contexts

        Returns:
            New context with the same state and variables
        """
        # Create new context with same options but no parent
        clone = ExecutionContext(options=self.options)

        # Copy variables
        clone.variables = self.variables.clone()

        # Copy state
        clone.state = ExecutionState.from_dict(self.state.to_dict())

        # Clone children if requested
        if include_children:
            for child in self._children:
                child_clone = child.clone(include_children=True)
                child_clone.parent = clone
                clone._children.append(child_clone)

        return clone

    def to_dict(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Convert the context to a dictionary

        Args:
            include_children: Whether to include child contexts

        Returns:
            Dictionary representation of the context
        """
        result = {
            "id": self.id,
            "options": self.options.to_dict(),
            "variables": self.variables.to_dict(),
            "state": self.state.to_dict()
        }

        if include_children:
            result["children"] = [child.to_dict(include_children=True) for child in self._children]

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional['ExecutionContext'] = None) -> 'ExecutionContext':
        """
        Create a context from a dictionary

        Args:
            data: Dictionary representation of the context
            parent: Optional parent context

        Returns:
            Instantiated context
        """
        # Create options
        options_data = data.get("options", {})
        options = ContextOptions.from_dict(options_data)

        # Create context
        context_id = data.get("id")

        # Create context without parent to avoid automatic child registration
        context = cls(
            parent=None,  # Will set parent later if needed
            options=options,
            context_id=context_id
        )

        # Restore variables
        variables_data = data.get("variables", {})
        context.variables = VariableStorage.from_dict(
            variables_data,
            parent=parent.variables if parent and options.inherit_variables else None
        )

        # Restore state
        state_data = data.get("state", {})
        context.state = ExecutionState.from_dict(state_data)

        # Set parent after initialization to avoid automatic child registration
        if parent:
            context.parent = parent
            parent._add_child(context)

        # Restore children
        children_data = data.get("children", [])
        for child_data in children_data:
            # Create child without setting parent
            child = cls.from_dict(child_data, parent=None)
            # Manually set parent and add to children
            child.parent = context
            context._children.append(child)

        return context

```

## Reference Components (Working Correctly)

The following components are working correctly and can be used as reference for the design patterns and architecture.

### src/core/models.py

**Created:** 2025-04-02 02:20:12
**Modified:** 2025-04-02 02:55:31
**Size:** 10956 bytes

### src/core/workflow/interfaces.py

**Created:** 2025-03-31 18:05:11
**Modified:** 2025-04-02 19:57:49
**Size:** 2701 bytes

### src/core/workflow/workflow_engine_new.py

**Created:** 2025-03-31 18:17:15
**Modified:** 2025-04-03 15:31:12
**Size:** 11588 bytes

### src/core/workflow/workflow_validator.py

**Created:** 2025-03-31 18:06:41
**Modified:** 2025-04-03 15:32:38
**Size:** 8144 bytes

### src/core/events/event_bus.py

**Created:** 2025-03-31 18:05:39
**Modified:** 2025-03-31 18:05:39
**Size:** 4109 bytes

### src/core/events/workflow_events.py

**Created:** 2025-03-31 23:27:24
**Modified:** 2025-04-01 03:08:53
**Size:** 3440 bytes

### src/core/workflow/exceptions.py

**Created:** 2025-03-31 23:27:24
**Modified:** 2025-04-02 19:50:39
**Size:** 4661 bytes

### src/core/workflow/execution_result.py

**Created:** 2025-03-31 18:06:19
**Modified:** 2025-04-02 20:24:32
**Size:** 6003 bytes

## Additional Guidelines

### Key Principles to Follow

-   **Single Responsibility Principle**: Each class should have only one reason to change
-   **Open/Closed Principle**: Classes should be open for extension but closed for modification
-   **Liskov Substitution Principle**: Subtypes must be substitutable for their base types
-   **Interface Segregation Principle**: Clients shouldn't depend on interfaces they don't use
-   **Dependency Inversion Principle**: Depend on abstractions, not concretions
-   **Keep It Simple, Stupid (KISS)**: Avoid unnecessary complexity
-   **Don't Repeat Yourself (DRY)**: Avoid code duplication
-   **Test-Driven Development (TDD)**: Write tests before implementation

### Output File Format

Ideally, provide your response as a single markdown file with the following structure:

````
# AUTOCLICK Project Fixes

## Analysis Summary
[Your overall analysis here]

## Fixed Components

### Component 1: [component name]

#### Analysis
[Your analysis here]

#### Implementation
```python
[Your code here]
````

#### Tests

```python
[Your tests here]
```

#### Explanation

[Your explanation here]

[Repeat for each component]

## Integration Guide

[Your integration instructions here]

## Testing Strategy

[Your testing strategy here]

```

Thank you for your assistance in improving the AUTOCLICK project!
```
