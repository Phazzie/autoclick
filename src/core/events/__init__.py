"""
Events module for event-driven communication.

This module provides components for event-driven communication between
different parts of the application.
"""
from .event_bus import EventBus
from .workflow_events import (
    WorkflowEvent, WorkflowStartedEvent, WorkflowCompletedEvent, WorkflowFailedEvent,
    ActionStartedEvent, ActionCompletedEvent, ActionFailedEvent, VariableUpdatedEvent,
    ValidationEvent, EVENT_WORKFLOW_STARTED, EVENT_WORKFLOW_COMPLETED,
    EVENT_WORKFLOW_FAILED, EVENT_ACTION_STARTED, EVENT_ACTION_COMPLETED,
    EVENT_ACTION_FAILED, EVENT_VARIABLE_UPDATED, EVENT_VALIDATION_COMPLETED
)

__all__ = [
    # Event bus
    'EventBus',
    
    # Events
    'WorkflowEvent', 'WorkflowStartedEvent', 'WorkflowCompletedEvent', 'WorkflowFailedEvent',
    'ActionStartedEvent', 'ActionCompletedEvent', 'ActionFailedEvent', 'VariableUpdatedEvent',
    'ValidationEvent',
    
    # Event types
    'EVENT_WORKFLOW_STARTED', 'EVENT_WORKFLOW_COMPLETED', 'EVENT_WORKFLOW_FAILED',
    'EVENT_ACTION_STARTED', 'EVENT_ACTION_COMPLETED', 'EVENT_ACTION_FAILED',
    'EVENT_VARIABLE_UPDATED', 'EVENT_VALIDATION_COMPLETED'
]
