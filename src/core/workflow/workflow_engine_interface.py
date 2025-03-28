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
