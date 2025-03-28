"""Tests for the workflow statistics"""
import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.workflow.workflow_event import WorkflowEventType, WorkflowStateEvent, ActionEvent
from src.core.workflow.workflow_statistics import WorkflowStatistics


class TestWorkflowStatistics(unittest.TestCase):
    """Test cases for the workflow statistics"""

    def test_initial_statistics(self):
        """Test initial state of statistics"""
        # Arrange & Act
        stats = WorkflowStatistics()

        # Assert
        self.assertIsNone(stats.start_time)
        self.assertIsNone(stats.end_time)
        self.assertEqual(stats.total_actions, 0)
        self.assertEqual(stats.completed_actions, 0)
        self.assertEqual(stats.failed_actions, 0)
        self.assertEqual(stats.skipped_actions, 0)
        self.assertEqual(stats.action_durations, {})
        self.assertEqual(stats.action_start_times, {})
        self.assertEqual(stats.events, [])
        self.assertIsNone(stats.duration)
        self.assertIsNone(stats.success_rate)
        self.assertFalse(stats.is_completed)

    def test_record_workflow_started(self):
        """Test recording workflow started event"""
        # Arrange
        stats = WorkflowStatistics()
        event = WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        )

        # Act
        stats.record_event(event)

        # Assert
        self.assertEqual(stats.start_time, event.timestamp)
        self.assertIsNone(stats.end_time)
        self.assertEqual(stats.events, [event])

    def test_record_workflow_completed(self):
        """Test recording workflow completed event"""
        # Arrange
        stats = WorkflowStatistics()
        start_event = WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        )
        stats.record_event(start_event)

        # Wait a bit to ensure different timestamps
        end_event = WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_COMPLETED,
            "test-workflow-id"
        )

        # Act
        stats.record_event(end_event)

        # Assert
        self.assertEqual(stats.start_time, start_event.timestamp)
        self.assertEqual(stats.end_time, end_event.timestamp)
        self.assertTrue(stats.is_completed)
        self.assertGreaterEqual(stats.duration.total_seconds(), 0)

    def test_record_action_events(self):
        """Test recording action events"""
        # Arrange
        stats = WorkflowStatistics()
        
        # Create mock action
        mock_action = MagicMock(spec=BaseAction)
        mock_action.id = "test-action-id"
        mock_action.type = "test-action-type"
        mock_action.description = "Test action"
        
        # Create success result
        result = ActionResult.create_success("Test result")

        # Act - Record action started
        start_event = ActionEvent(
            WorkflowEventType.ACTION_STARTED,
            "test-workflow-id",
            mock_action,
            0
        )
        stats.record_event(start_event)
        
        # Record action completed
        complete_event = ActionEvent(
            WorkflowEventType.ACTION_COMPLETED,
            "test-workflow-id",
            mock_action,
            0,
            result
        )
        stats.record_event(complete_event)

        # Assert
        self.assertEqual(stats.total_actions, 1)
        self.assertEqual(stats.completed_actions, 1)
        self.assertEqual(stats.failed_actions, 0)
        self.assertEqual(stats.skipped_actions, 0)
        self.assertEqual(len(stats.action_durations), 1)
        self.assertIn(mock_action.id, stats.action_durations)
        self.assertEqual(stats.success_rate, 100.0)

    def test_record_failed_action(self):
        """Test recording failed action event"""
        # Arrange
        stats = WorkflowStatistics()
        
        # Create mock action
        mock_action = MagicMock(spec=BaseAction)
        mock_action.id = "test-action-id"
        mock_action.type = "test-action-type"
        mock_action.description = "Test action"
        
        # Create failure result
        result = ActionResult.create_failure("Test failure")

        # Act - Record action started
        start_event = ActionEvent(
            WorkflowEventType.ACTION_STARTED,
            "test-workflow-id",
            mock_action,
            0
        )
        stats.record_event(start_event)
        
        # Record action failed
        fail_event = ActionEvent(
            WorkflowEventType.ACTION_FAILED,
            "test-workflow-id",
            mock_action,
            0,
            result
        )
        stats.record_event(fail_event)

        # Assert
        self.assertEqual(stats.total_actions, 1)
        self.assertEqual(stats.completed_actions, 0)
        self.assertEqual(stats.failed_actions, 1)
        self.assertEqual(stats.skipped_actions, 0)
        self.assertEqual(len(stats.action_durations), 1)
        self.assertIn(mock_action.id, stats.action_durations)
        self.assertEqual(stats.success_rate, 0.0)

    def test_record_skipped_action(self):
        """Test recording skipped action event"""
        # Arrange
        stats = WorkflowStatistics()
        
        # Create mock action
        mock_action = MagicMock(spec=BaseAction)
        mock_action.id = "test-action-id"
        mock_action.type = "test-action-type"
        mock_action.description = "Test action"

        # Act - Record action skipped
        skip_event = ActionEvent(
            WorkflowEventType.ACTION_SKIPPED,
            "test-workflow-id",
            mock_action,
            0
        )
        stats.record_event(skip_event)

        # Assert
        self.assertEqual(stats.total_actions, 0)  # Not counted in total
        self.assertEqual(stats.completed_actions, 0)
        self.assertEqual(stats.failed_actions, 0)
        self.assertEqual(stats.skipped_actions, 1)

    def test_multiple_actions_statistics(self):
        """Test statistics with multiple actions"""
        # Arrange
        stats = WorkflowStatistics()
        
        # Create mock actions
        action1 = MagicMock(spec=BaseAction)
        action1.id = "action1"
        action1.type = "test-action-type"
        action1.description = "Action 1"
        
        action2 = MagicMock(spec=BaseAction)
        action2.id = "action2"
        action2.type = "test-action-type"
        action2.description = "Action 2"
        
        # Create results
        success_result = ActionResult.create_success("Success")
        failure_result = ActionResult.create_failure("Failure")

        # Act - Record workflow started
        stats.record_event(WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        ))
        
        # Record action 1 (success)
        stats.record_event(ActionEvent(
            WorkflowEventType.ACTION_STARTED,
            "test-workflow-id",
            action1,
            0
        ))
        stats.record_event(ActionEvent(
            WorkflowEventType.ACTION_COMPLETED,
            "test-workflow-id",
            action1,
            0,
            success_result
        ))
        
        # Record action 2 (failure)
        stats.record_event(ActionEvent(
            WorkflowEventType.ACTION_STARTED,
            "test-workflow-id",
            action2,
            1
        ))
        stats.record_event(ActionEvent(
            WorkflowEventType.ACTION_FAILED,
            "test-workflow-id",
            action2,
            1,
            failure_result
        ))
        
        # Record workflow failed
        stats.record_event(WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_FAILED,
            "test-workflow-id"
        ))

        # Assert
        self.assertEqual(stats.total_actions, 2)
        self.assertEqual(stats.completed_actions, 1)
        self.assertEqual(stats.failed_actions, 1)
        self.assertEqual(stats.skipped_actions, 0)
        self.assertEqual(len(stats.action_durations), 2)
        self.assertEqual(stats.success_rate, 50.0)
        self.assertTrue(stats.is_completed)

    def test_average_action_duration(self):
        """Test calculating average action duration"""
        # Arrange
        stats = WorkflowStatistics()
        
        # Manually set action durations
        stats.action_durations = {
            "action1": timedelta(seconds=1),
            "action2": timedelta(seconds=3)
        }

        # Act
        avg_duration = stats.get_average_action_duration()

        # Assert
        self.assertEqual(avg_duration, timedelta(seconds=2))

    def test_slowest_and_fastest_action(self):
        """Test finding slowest and fastest actions"""
        # Arrange
        stats = WorkflowStatistics()
        
        # Manually set action durations
        stats.action_durations = {
            "action1": timedelta(seconds=1),
            "action2": timedelta(seconds=3),
            "action3": timedelta(seconds=2)
        }

        # Act & Assert
        self.assertEqual(stats.get_slowest_action(), "action2")
        self.assertEqual(stats.get_fastest_action(), "action1")

    def test_to_dict(self):
        """Test converting statistics to dictionary"""
        # Arrange
        stats = WorkflowStatistics()
        
        # Set some values
        stats.start_time = datetime.now()
        stats.end_time = stats.start_time + timedelta(seconds=5)
        stats.total_actions = 2
        stats.completed_actions = 1
        stats.failed_actions = 1
        stats.action_durations = {
            "action1": timedelta(seconds=2),
            "action2": timedelta(seconds=3)
        }

        # Act
        stats_dict = stats.to_dict()

        # Assert
        self.assertIn("start_time", stats_dict)
        self.assertIn("end_time", stats_dict)
        self.assertIn("duration", stats_dict)
        self.assertEqual(stats_dict["total_actions"], 2)
        self.assertEqual(stats_dict["completed_actions"], 1)
        self.assertEqual(stats_dict["failed_actions"], 1)
        self.assertEqual(stats_dict["success_rate"], 50.0)
        self.assertEqual(stats_dict["action_durations"]["action1"], 2.0)
        self.assertEqual(stats_dict["action_durations"]["action2"], 3.0)
        self.assertEqual(stats_dict["average_action_duration"], 2.5)
        self.assertEqual(stats_dict["slowest_action"], "action2")
        self.assertEqual(stats_dict["fastest_action"], "action1")


if __name__ == "__main__":
    unittest.main()
