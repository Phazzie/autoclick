"""Tests for the workflow event system"""
import unittest
from unittest.mock import MagicMock
from datetime import datetime

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.workflow.workflow_event import (
    WorkflowEventType, WorkflowEvent, WorkflowStateEvent, ActionEvent, EventDispatcher
)


class TestWorkflowEvents(unittest.TestCase):
    """Test cases for the workflow event system"""

    def test_workflow_event_creation(self):
        """Test creating a workflow event"""
        # Arrange & Act
        event = WorkflowEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        )

        # Assert
        self.assertEqual(event.event_type, WorkflowEventType.WORKFLOW_STARTED)
        self.assertEqual(event.workflow_id, "test-workflow-id")
        self.assertIsInstance(event.timestamp, datetime)
        self.assertEqual(event.data, {})

    def test_workflow_event_with_data(self):
        """Test creating a workflow event with data"""
        # Arrange
        data = {"key": "value"}

        # Act
        event = WorkflowEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id",
            data=data
        )

        # Assert
        self.assertEqual(event.data, data)

    def test_workflow_state_event_creation(self):
        """Test creating a workflow state event"""
        # Arrange & Act
        event = WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        )

        # Assert
        self.assertEqual(event.event_type, WorkflowEventType.WORKFLOW_STARTED)
        self.assertEqual(event.workflow_id, "test-workflow-id")

    def test_workflow_state_event_invalid_type(self):
        """Test creating a workflow state event with invalid type"""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            WorkflowStateEvent(
                WorkflowEventType.ACTION_STARTED,
                "test-workflow-id"
            )

    def test_action_event_creation(self):
        """Test creating an action event"""
        # Arrange
        mock_action = MagicMock(spec=BaseAction)
        mock_action.id = "test-action-id"
        mock_action.type = "test-action-type"
        mock_action.description = "Test action"

        # Act
        event = ActionEvent(
            WorkflowEventType.ACTION_STARTED,
            "test-workflow-id",
            mock_action,
            0
        )

        # Assert
        self.assertEqual(event.event_type, WorkflowEventType.ACTION_STARTED)
        self.assertEqual(event.workflow_id, "test-workflow-id")
        self.assertEqual(event.action, mock_action)
        self.assertEqual(event.action_index, 0)
        self.assertIsNone(event.result)

    def test_action_event_with_result(self):
        """Test creating an action event with result"""
        # Arrange
        mock_action = MagicMock(spec=BaseAction)
        mock_action.id = "test-action-id"
        mock_action.type = "test-action-type"
        mock_action.description = "Test action"

        result = ActionResult.create_success("Test result")

        # Act
        event = ActionEvent(
            WorkflowEventType.ACTION_COMPLETED,
            "test-workflow-id",
            mock_action,
            0,
            result
        )

        # Assert
        self.assertEqual(event.result, result)
        self.assertTrue(event.data["result_success"])
        self.assertEqual(event.data["result_message"], "Test result")

    def test_action_event_invalid_type(self):
        """Test creating an action event with invalid type"""
        # Arrange
        mock_action = MagicMock(spec=BaseAction)
        mock_action.id = "test-action-id"
        mock_action.type = "test-action-type"
        mock_action.description = "Test action"

        # Act & Assert
        with self.assertRaises(ValueError):
            ActionEvent(
                WorkflowEventType.WORKFLOW_STARTED,
                "test-workflow-id",
                mock_action,
                0
            )

    def test_event_to_dict(self):
        """Test converting an event to a dictionary"""
        # Arrange
        event = WorkflowEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id",
            data={"key": "value"}
        )

        # Act
        event_dict = event.to_dict()

        # Assert
        self.assertEqual(event_dict["event_type"], "WORKFLOW_STARTED")
        self.assertEqual(event_dict["workflow_id"], "test-workflow-id")
        self.assertIn("timestamp", event_dict)
        self.assertEqual(event_dict["data"], {"key": "value"})

    def test_event_dispatcher_add_listener(self):
        """Test adding a listener to the event dispatcher"""
        # Arrange
        dispatcher = EventDispatcher()
        listener = MagicMock()

        # Act
        dispatcher.add_listener(WorkflowEventType.WORKFLOW_STARTED, listener)

        # Assert
        self.assertIn(listener, dispatcher._listeners[WorkflowEventType.WORKFLOW_STARTED])

    def test_event_dispatcher_add_global_listener(self):
        """Test adding a global listener to the event dispatcher"""
        # Arrange
        dispatcher = EventDispatcher()
        listener = MagicMock()

        # Act
        dispatcher.add_listener(None, listener)

        # Assert
        self.assertIn(listener, dispatcher._global_listeners)

    def test_event_dispatcher_remove_listener(self):
        """Test removing a listener from the event dispatcher"""
        # Arrange
        dispatcher = EventDispatcher()
        listener = MagicMock()
        dispatcher.add_listener(WorkflowEventType.WORKFLOW_STARTED, listener)

        # Act
        dispatcher.remove_listener(WorkflowEventType.WORKFLOW_STARTED, listener)

        # Assert
        self.assertNotIn(listener, dispatcher._listeners[WorkflowEventType.WORKFLOW_STARTED])

    def test_event_dispatcher_remove_global_listener(self):
        """Test removing a global listener from the event dispatcher"""
        # Arrange
        dispatcher = EventDispatcher()
        listener = MagicMock()
        dispatcher.add_listener(None, listener)

        # Act
        dispatcher.remove_listener(None, listener)

        # Assert
        self.assertNotIn(listener, dispatcher._global_listeners)

    def test_event_dispatcher_dispatch(self):
        """Test dispatching an event"""
        # Arrange
        dispatcher = EventDispatcher()
        listener = MagicMock()
        dispatcher.add_listener(WorkflowEventType.WORKFLOW_STARTED, listener)

        event = WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        )

        # Act
        dispatcher.dispatch(event)

        # Assert
        listener.assert_called_once_with(event)

    def test_event_dispatcher_dispatch_global(self):
        """Test dispatching an event to global listeners"""
        # Arrange
        dispatcher = EventDispatcher()
        global_listener = MagicMock()
        specific_listener = MagicMock()
        
        dispatcher.add_listener(None, global_listener)
        dispatcher.add_listener(WorkflowEventType.WORKFLOW_STARTED, specific_listener)

        event = WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        )

        # Act
        dispatcher.dispatch(event)

        # Assert
        global_listener.assert_called_once_with(event)
        specific_listener.assert_called_once_with(event)

    def test_event_dispatcher_listener_error(self):
        """Test handling errors in event listeners"""
        # Arrange
        dispatcher = EventDispatcher()
        
        # Create a listener that raises an exception
        def error_listener(event):
            raise ValueError("Test error")
        
        dispatcher.add_listener(WorkflowEventType.WORKFLOW_STARTED, error_listener)

        event = WorkflowStateEvent(
            WorkflowEventType.WORKFLOW_STARTED,
            "test-workflow-id"
        )

        # Act & Assert - Should not raise an exception
        dispatcher.dispatch(event)


if __name__ == "__main__":
    unittest.main()
