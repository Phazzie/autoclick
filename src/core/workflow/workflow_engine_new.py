"""
Workflow engine implementation.

This module provides the main workflow engine implementation that orchestrates
workflow execution, validation, and event handling.
"""
from typing import Dict, Any, List, Optional, Callable
import logging
import time

from .interfaces import IWorkflowEngine, IWorkflowValidator, IWorkflowExecutor, WorkflowDefinition
from .execution_result import ExecutionResult
from .workflow_validator import WorkflowValidator
from .workflow_executor import WorkflowExecutor
from .exceptions import WorkflowError, WorkflowValidationError
from ..events.event_bus import EventBus
from ..events.workflow_events import (
    WorkflowEvent, EVENT_WORKFLOW_STARTED, EVENT_WORKFLOW_COMPLETED,
    EVENT_WORKFLOW_FAILED, EVENT_ACTION_STARTED, EVENT_ACTION_COMPLETED,
    EVENT_ACTION_FAILED, EVENT_VARIABLE_UPDATED
)


class WorkflowEngine(IWorkflowEngine):
    """
    Engine for executing and validating workflows.

    This class orchestrates workflow execution and validation, delegating
    the actual work to specialized components.
    """

    def __init__(self,
                 validator: Optional[IWorkflowValidator] = None,
                 executor: Optional[IWorkflowExecutor] = None,
                 event_bus: Optional[EventBus] = None,
                 action_resolver = None):
        """
        Initialize the workflow engine.

        Args:
            validator: Optional workflow validator
            executor: Optional workflow executor
            event_bus: Optional event bus for publishing events
            action_resolver: Optional action resolver for creating actions
        """
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.info("Initializing NEW WorkflowEngine implementation")

        # Create components if not provided
        self._event_bus = event_bus or EventBus()

        if executor is None and action_resolver is not None:
            executor = WorkflowExecutor(action_resolver, self._event_bus)

        self._validator = validator or WorkflowValidator()
        self._executor = executor
        self._action_resolver = action_resolver

        # Initialize state
        self._execution_listeners: List[Callable[[str, Dict[str, Any]], None]] = []

    def validate_workflow(self, workflow: WorkflowDefinition) -> List[str]:
        """
        Validate a workflow definition.

        Args:
            workflow: Workflow definition to validate

        Returns:
            List of validation errors, empty if valid
        """
        self.logger.info(f"Validating workflow: {workflow.workflow_id}")
        return self._validator.validate(workflow)

    def create_workflow(self, workflow_data: Dict[str, Any]) -> WorkflowDefinition:
        """
        Create a workflow from data.

        Args:
            workflow_data: Workflow data

        Returns:
            Created workflow definition
        """
        # This is a simple implementation - in a real system, you would create a proper workflow object
        # For now, we'll just create a simple object that satisfies the WorkflowDefinition protocol
        class SimpleWorkflowDefinition:
            def __init__(self, data):
                self.workflow_id = data.get('id', str(time.time()))
                self.name = data.get('name', 'Unnamed Workflow')
                self.nodes = data.get('nodes', {})
                self.connections = data.get('connections', {})

                # Convert nodes to actions format for compatibility with validator
                self.actions = []
                for node_id, node in self.nodes.items():
                    self.actions.append({
                        'id': node_id,
                        'type': node.get('type', 'Unknown'),
                        'properties': node.get('properties', {})
                    })

                # Convert connections to the format expected by validator
                self.connections = []
                for conn_id, conn in data.get('connections', {}).items():
                    self.connections.append({
                        'id': conn_id,
                        'source': conn.get('source_node_id', ''),
                        'target': conn.get('target_node_id', '')
                    })

        return SimpleWorkflowDefinition(workflow_data)

    def add_execution_listener(self, listener: Callable) -> None:
        """
        Add an execution listener.

        Args:
            listener: Listener to add
        """
        if listener not in self._execution_listeners:
            self._execution_listeners.append(listener)
            self.logger.debug(f"Added execution listener: {listener}")

    def remove_execution_listener(self, listener: Callable) -> None:
        """
        Remove an execution listener.

        Args:
            listener: Listener to remove
        """
        if listener in self._execution_listeners:
            self._execution_listeners.remove(listener)
            self.logger.debug(f"Removed execution listener: {listener}")

    def execute_workflow(self, workflow: WorkflowDefinition,
                         initial_context: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """
        Execute a workflow.

        Args:
            workflow: Workflow definition to execute
            initial_context: Optional initial context values

        Returns:
            Result of the execution
        """
        # Validate the workflow first
        self.logger.info(f"Executing workflow: {workflow.workflow_id}")
        validation_errors = self.validate_workflow(workflow)

        if validation_errors:
            # Workflow is invalid, return error result
            error = WorkflowValidationError(
                workflow_id=workflow.workflow_id,
                validation_errors=validation_errors
            )
            self.logger.error(f"Workflow validation failed: {error}")

            # Create a failure result
            return ExecutionResult(
                workflow_id=workflow.workflow_id,
                success=False,
                context=initial_context or {},
                error=error
            )

        # Check if executor is available
        if self._executor is None:
            error = WorkflowError("No workflow executor available")
            self.logger.error(str(error))

            # Create a failure result
            return ExecutionResult(
                workflow_id=workflow.workflow_id,
                success=False,
                context=initial_context or {},
                error=error
            )

        # Execute the workflow
        try:
            result = self._executor.execute(workflow, initial_context)

            # Notify listeners
            self._notify_listeners(
                "workflow.completed" if result.success else "workflow.failed",
                {
                    "workflow_id": workflow.workflow_id,
                    "success": result.success,
                    "context": result.context,
                    "error": str(result.error) if result.error else None,
                    "execution_time": result.execution_time
                }
            )

            return result
        except Exception as e:
            self.logger.error(f"Error executing workflow: {e}", exc_info=True)

            # Create a failure result
            result = ExecutionResult(
                workflow_id=workflow.workflow_id,
                success=False,
                context=initial_context or {},
                error=e
            )

            # Notify listeners
            self._notify_listeners(
                "workflow.failed",
                {
                    "workflow_id": workflow.workflow_id,
                    "success": False,
                    "context": initial_context or {},
                    "error": str(e),
                    "execution_time": 0.0
                }
            )

            return result

    def register_execution_listener(self, listener: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        Register a listener for workflow execution events.

        Args:
            listener: Callback function that receives event name and data
        """
        if listener not in self._execution_listeners:
            self._execution_listeners.append(listener)

            # Register with event bus for specific events
            self._event_bus.subscribe(EVENT_WORKFLOW_STARTED,
                                     lambda event: self._handle_event(EVENT_WORKFLOW_STARTED, event))
            self._event_bus.subscribe(EVENT_WORKFLOW_COMPLETED,
                                     lambda event: self._handle_event(EVENT_WORKFLOW_COMPLETED, event))
            self._event_bus.subscribe(EVENT_WORKFLOW_FAILED,
                                     lambda event: self._handle_event(EVENT_WORKFLOW_FAILED, event))
            self._event_bus.subscribe(EVENT_ACTION_STARTED,
                                     lambda event: self._handle_event(EVENT_ACTION_STARTED, event))
            self._event_bus.subscribe(EVENT_ACTION_COMPLETED,
                                     lambda event: self._handle_event(EVENT_ACTION_COMPLETED, event))
            self._event_bus.subscribe(EVENT_ACTION_FAILED,
                                     lambda event: self._handle_event(EVENT_ACTION_FAILED, event))
            self._event_bus.subscribe(EVENT_VARIABLE_UPDATED,
                                     lambda event: self._handle_event(EVENT_VARIABLE_UPDATED, event))

    def _handle_event(self, event_type: str, event: WorkflowEvent) -> None:
        """
        Handle an event from the event bus.

        Args:
            event_type: Type of the event
            event: Event data
        """
        # Convert event to dictionary for listeners
        event_dict = {
            "workflow_id": event.workflow_id,
            "timestamp": event.timestamp
        }

        # Add event-specific data
        if hasattr(event, 'final_context'):
            event_dict["context"] = event.final_context
        elif hasattr(event, 'initial_context'):
            event_dict["context"] = event.initial_context
        elif hasattr(event, 'context'):
            event_dict["context"] = event.context

        if hasattr(event, 'error_message'):
            event_dict["error"] = event.error_message

        if hasattr(event, 'execution_time'):
            event_dict["execution_time"] = event.execution_time

        if hasattr(event, 'action_id'):
            event_dict["action_id"] = event.action_id
            event_dict["action_type"] = event.action_type

        if hasattr(event, 'result'):
            event_dict["result"] = event.result

        if hasattr(event, 'variable_name'):
            event_dict["variable_name"] = event.variable_name
            event_dict["old_value"] = event.old_value
            event_dict["new_value"] = event.new_value

        # Notify listeners
        self._notify_listeners(event_type, event_dict)

    def _notify_listeners(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Notify all registered listeners of an event.

        Args:
            event_type: Type of the event
            event_data: Event data
        """
        for listener in self._execution_listeners:
            try:
                listener(event_type, event_data)
            except Exception as e:
                self.logger.error(f"Error in event listener: {e}", exc_info=True)
