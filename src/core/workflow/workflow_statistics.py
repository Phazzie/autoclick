"""Statistics collection for workflow execution"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from src.core.workflow.workflow_event import WorkflowEvent, WorkflowEventType, ActionEvent


class WorkflowStatistics:
    """Collects and calculates statistics for workflow execution"""

    def __init__(self):
        """Initialize the statistics collector"""
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_actions: int = 0
        self.completed_actions: int = 0
        self.failed_actions: int = 0
        self.skipped_actions: int = 0
        self.action_durations: Dict[str, timedelta] = {}
        self.action_start_times: Dict[str, datetime] = {}
        self.events: List[WorkflowEvent] = []

    @property
    def duration(self) -> Optional[timedelta]:
        """
        Get the total duration of the workflow execution

        Returns:
            Duration or None if the workflow hasn't started
        """
        if not self.start_time:
            return None

        end = self.end_time or datetime.now()
        return end - self.start_time

    @property
    def success_rate(self) -> Optional[float]:
        """
        Get the success rate of the workflow execution

        Returns:
            Success rate as a percentage or None if no actions were executed
        """
        if self.total_actions == 0:
            return None

        return (self.completed_actions / self.total_actions) * 100

    @property
    def is_completed(self) -> bool:
        """
        Check if the workflow has completed

        Returns:
            True if the workflow has completed, False otherwise
        """
        return self.end_time is not None

    def record_event(self, event: WorkflowEvent) -> None:
        """
        Record a workflow event and update statistics

        Args:
            event: Workflow event to record
        """
        self.events.append(event)

        # Update statistics based on event type
        if event.event_type == WorkflowEventType.WORKFLOW_STARTED:
            self.start_time = event.timestamp
        elif event.event_type in [
            WorkflowEventType.WORKFLOW_COMPLETED,
            WorkflowEventType.WORKFLOW_FAILED,
            WorkflowEventType.WORKFLOW_ABORTED
        ]:
            self.end_time = event.timestamp
        elif event.event_type == WorkflowEventType.ACTION_STARTED:
            if isinstance(event, ActionEvent):
                self.total_actions += 1
                self.action_start_times[event.action.id] = event.timestamp
        elif event.event_type == WorkflowEventType.ACTION_COMPLETED:
            if isinstance(event, ActionEvent):
                self.completed_actions += 1
                self._calculate_action_duration(event)
        elif event.event_type == WorkflowEventType.ACTION_FAILED:
            if isinstance(event, ActionEvent):
                self.failed_actions += 1
                self._calculate_action_duration(event)
        elif event.event_type == WorkflowEventType.ACTION_SKIPPED:
            if isinstance(event, ActionEvent):
                self.skipped_actions += 1

    def _calculate_action_duration(self, event: ActionEvent) -> None:
        """
        Calculate and record the duration of an action

        Args:
            event: Action event with the action ID
        """
        action_id = event.action.id
        if action_id in self.action_start_times:
            start_time = self.action_start_times[action_id]
            duration = event.timestamp - start_time
            self.action_durations[action_id] = duration

    def get_average_action_duration(self) -> Optional[timedelta]:
        """
        Get the average duration of all actions

        Returns:
            Average duration or None if no actions were completed
        """
        if not self.action_durations:
            return None

        total_seconds = sum(duration.total_seconds() for duration in self.action_durations.values())
        average_seconds = total_seconds / len(self.action_durations)
        return timedelta(seconds=average_seconds)

    def get_slowest_action(self) -> Optional[str]:
        """
        Get the ID of the slowest action

        Returns:
            Action ID or None if no actions were completed
        """
        if not self.action_durations:
            return None

        return max(self.action_durations.items(), key=lambda x: x[1])[0]

    def get_fastest_action(self) -> Optional[str]:
        """
        Get the ID of the fastest action

        Returns:
            Action ID or None if no actions were completed
        """
        if not self.action_durations:
            return None

        return min(self.action_durations.items(), key=lambda x: x[1])[0]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the statistics to a dictionary

        Returns:
            Dictionary representation of the statistics
        """
        return {
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration.total_seconds() if self.duration else None,
            "total_actions": self.total_actions,
            "completed_actions": self.completed_actions,
            "failed_actions": self.failed_actions,
            "skipped_actions": self.skipped_actions,
            "success_rate": self.success_rate,
            "action_durations": {
                action_id: duration.total_seconds()
                for action_id, duration in self.action_durations.items()
            },
            "average_action_duration": (
                self.get_average_action_duration().total_seconds()
                if self.get_average_action_duration() else None
            ),
            "slowest_action": self.get_slowest_action(),
            "fastest_action": self.get_fastest_action()
        }
