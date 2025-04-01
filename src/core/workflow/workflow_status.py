"""
Workflow status enumeration.

This module defines the possible states of a workflow.
"""
from enum import Enum, auto


class WorkflowStatus(Enum):
    """Enumeration of workflow statuses."""
    
    PENDING = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()
    ABORTED = auto()
    RECOVERING = auto()
