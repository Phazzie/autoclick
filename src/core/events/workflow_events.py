"""
Workflow-related events for the event bus.

This module defines the events that can be published and subscribed to
during workflow execution, providing a loose coupling between components.
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum, auto


class WorkflowEventType(Enum):
    """Enumeration of workflow event types."""

    WORKFLOW_STARTED = auto()
    WORKFLOW_COMPLETED = auto()
    WORKFLOW_FAILED = auto()
    WORKFLOW_PAUSED = auto()
    WORKFLOW_RESUMED = auto()
    WORKFLOW_ABORTED = auto()
    STEP_STARTED = auto()
    STEP_COMPLETED = auto()
    STEP_FAILED = auto()
    STEP_SKIPPED = auto()
    ACTION_STARTED = auto()
    ACTION_COMPLETED = auto()
    ACTION_FAILED = auto()
    ACTION_SKIPPED = auto()
    VARIABLE_CHANGED = auto()
    CONDITION_EVALUATED = auto()
    ERROR_OCCURRED = auto()


@dataclass(frozen=True)
class WorkflowEvent:
    """Base class for all workflow events."""
    workflow_id: str
    timestamp: float


@dataclass(frozen=True)
class WorkflowStateEvent(WorkflowEvent):
    """Event for workflow state changes."""
    state: str
    previous_state: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class WorkflowStartedEvent(WorkflowEvent):
    """Event published when a workflow execution starts."""
    initial_context: Dict[str, Any]


@dataclass(frozen=True)
class WorkflowCompletedEvent(WorkflowEvent):
    """Event published when a workflow execution completes successfully."""
    final_context: Dict[str, Any]
    execution_time: float


@dataclass(frozen=True)
class WorkflowFailedEvent(WorkflowEvent):
    """Event published when a workflow execution fails."""
    error_message: str
    error_type: str
    context: Dict[str, Any]
    execution_time: float


@dataclass(frozen=True)
class ActionStartedEvent(WorkflowEvent):
    """Event published when an action execution starts."""
    action_id: str
    action_type: str
    action_params: Dict[str, Any]


@dataclass(frozen=True)
class ActionCompletedEvent(WorkflowEvent):
    """Event published when an action execution completes successfully."""
    action_id: str
    action_type: str
    result: Any
    execution_time: float


@dataclass(frozen=True)
class ActionFailedEvent(WorkflowEvent):
    """Event published when an action execution fails."""
    action_id: str
    action_type: str
    error_message: str
    error_type: str
    execution_time: float


@dataclass(frozen=True)
class ActionEvent(WorkflowEvent):
    """Event for action execution."""
    step_id: str
    action_id: str
    action_type: str
    data: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class VariableUpdatedEvent(WorkflowEvent):
    """Event published when a variable is updated during workflow execution."""
    variable_name: str
    old_value: Optional[Any]
    new_value: Any


@dataclass(frozen=True)
class ValidationEvent(WorkflowEvent):
    """Event published when a workflow is validated."""
    is_valid: bool
    validation_errors: List[str]


# Event type constants
EVENT_WORKFLOW_STARTED = "workflow.started"
EVENT_WORKFLOW_COMPLETED = "workflow.completed"
EVENT_WORKFLOW_FAILED = "workflow.failed"
EVENT_ACTION_STARTED = "action.started"
EVENT_ACTION_COMPLETED = "action.completed"
EVENT_ACTION_FAILED = "action.failed"
EVENT_VARIABLE_UPDATED = "variable.updated"
EVENT_VALIDATION_COMPLETED = "validation.completed"

