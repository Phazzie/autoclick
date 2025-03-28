"""Event system for workflow execution"""
from abc import ABC
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction


class WorkflowEventType(Enum):
    """Types of workflow events"""
    WORKFLOW_STARTED = auto()
    WORKFLOW_COMPLETED = auto()
    WORKFLOW_FAILED = auto()
    WORKFLOW_PAUSED = auto()
    WORKFLOW_RESUMED = auto()
    WORKFLOW_ABORTED = auto()
    ACTION_STARTED = auto()
    ACTION_COMPLETED = auto()
    ACTION_FAILED = auto()
    ACTION_SKIPPED = auto()


class WorkflowEvent(ABC):
    """Base class for all workflow events"""

    def __init__(
        self,
        event_type: WorkflowEventType,
        workflow_id: str,
        timestamp: Optional[datetime] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the workflow event

        Args:
            event_type: Type of the event
            workflow_id: ID of the workflow
            timestamp: Time of the event (defaults to now)
            data: Additional event data
        """
        self.event_type = event_type
        self.workflow_id = workflow_id
        self.timestamp = timestamp or datetime.now()
        self.data = data or {}

    def __str__(self) -> str:
        """String representation of the event"""
        return f"{self.event_type.name} at {self.timestamp}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary

        Returns:
            Dictionary representation of the event
        """
        return {
            "event_type": self.event_type.name,
            "workflow_id": self.workflow_id,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data
        }


class WorkflowStateEvent(WorkflowEvent):
    """Event for workflow state changes"""

    def __init__(
        self,
        event_type: WorkflowEventType,
        workflow_id: str,
        timestamp: Optional[datetime] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the workflow state event

        Args:
            event_type: Type of the event (must be a workflow state event)
            workflow_id: ID of the workflow
            timestamp: Time of the event (defaults to now)
            data: Additional event data
        """
        if event_type not in [
            WorkflowEventType.WORKFLOW_STARTED,
            WorkflowEventType.WORKFLOW_COMPLETED,
            WorkflowEventType.WORKFLOW_FAILED,
            WorkflowEventType.WORKFLOW_PAUSED,
            WorkflowEventType.WORKFLOW_RESUMED,
            WorkflowEventType.WORKFLOW_ABORTED
        ]:
            raise ValueError(f"Invalid event type for WorkflowStateEvent: {event_type}")

        super().__init__(event_type, workflow_id, timestamp, data)


class ActionEvent(WorkflowEvent):
    """Event for action execution"""

    def __init__(
        self,
        event_type: WorkflowEventType,
        workflow_id: str,
        action: BaseAction,
        action_index: int,
        result: Optional[ActionResult] = None,
        timestamp: Optional[datetime] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the action event

        Args:
            event_type: Type of the event (must be an action event)
            workflow_id: ID of the workflow
            action: The action that was executed
            action_index: Index of the action in the workflow
            result: Result of the action execution (for completed/failed events)
            timestamp: Time of the event (defaults to now)
            data: Additional event data
        """
        if event_type not in [
            WorkflowEventType.ACTION_STARTED,
            WorkflowEventType.ACTION_COMPLETED,
            WorkflowEventType.ACTION_FAILED,
            WorkflowEventType.ACTION_SKIPPED
        ]:
            raise ValueError(f"Invalid event type for ActionEvent: {event_type}")

        event_data = data or {}
        event_data.update({
            "action_id": action.id,
            "action_type": action.type,
            "action_description": action.description,
            "action_index": action_index
        })

        if result is not None:
            event_data.update({
                "result_success": result.success,
                "result_message": result.message,
                "result_data": result.data
            })

        super().__init__(event_type, workflow_id, timestamp, event_data)

        self.action = action
        self.action_index = action_index
        self.result = result


class EventDispatcher:
    """Dispatches workflow events to registered listeners"""

    def __init__(self):
        """Initialize the event dispatcher"""
        self._listeners: Dict[WorkflowEventType, List[Callable[[WorkflowEvent], None]]] = {
            event_type: [] for event_type in WorkflowEventType
        }
        self._global_listeners: List[Callable[[WorkflowEvent], None]] = []

    def add_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """
        Add a listener for a specific event type or all events

        Args:
            event_type: Type of event to listen for, or None for all events
            listener: Callback function that will be called when events occur
        """
        if event_type is None:
            # Global listener for all events
            if listener not in self._global_listeners:
                self._global_listeners.append(listener)
        else:
            # Specific event type listener
            if listener not in self._listeners[event_type]:
                self._listeners[event_type].append(listener)

    def remove_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """
        Remove a listener

        Args:
            event_type: Type of event the listener was registered for, or None for all events
            listener: Listener to remove
        """
        if event_type is None:
            # Remove from global listeners
            if listener in self._global_listeners:
                self._global_listeners.remove(listener)
        else:
            # Remove from specific event type listeners
            if listener in self._listeners[event_type]:
                self._listeners[event_type].remove(listener)

    def dispatch(self, event: WorkflowEvent) -> None:
        """
        Dispatch an event to all registered listeners

        Args:
            event: Event to dispatch
        """
        # Notify specific event type listeners
        for listener in self._listeners[event.event_type]:
            try:
                listener(event)
            except Exception as e:
                # In a real application, you might want to log this error
                print(f"Error in event listener: {str(e)}")

        # Notify global listeners
        for listener in self._global_listeners:
            try:
                listener(event)
            except Exception as e:
                # In a real application, you might want to log this error
                print(f"Error in global event listener: {str(e)}")
