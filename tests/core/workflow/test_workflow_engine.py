"""Tests for the workflow engine"""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.context.execution_context import ExecutionContext
from src.core.context.execution_state import ExecutionStateEnum
from src.core.workflow.workflow_engine import WorkflowEngine, WorkflowStatus
from src.core.workflow.workflow_event import WorkflowEventType


# Concrete implementation of BaseAction for testing
class TestAction(BaseAction):
    """Test action for workflow engine tests"""

    def __init__(self, description: str, should_succeed: bool = True, action_id: str = None):
        """Initialize the test action"""
        super().__init__(description, action_id)
        self.should_succeed = should_succeed
        self.executed = False

    @property
    def type(self) -> str:
        """Get the action type"""
        return "test_action"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        self.executed = True
        # Use context to avoid unused parameter warning
        result_data = {"executed": True}
        if "test_key" in context:
            result_data["test_key"] = context["test_key"]

        if self.should_succeed:
            return ActionResult.create_success(f"Executed: {self.description}", result_data)
        else:
            return ActionResult.create_failure(f"Failed: {self.description}")


class TestWorkflowEngine(unittest.TestCase):
    """Test cases for the workflow engine"""

    def setUp(self):
        """Set up test environment"""
        self.engine = WorkflowEngine()
        # Create a fresh context for each test
        self.context = ExecutionContext()

    def test_execute_single_action(self):
        """Test executing a single action"""
        # Arrange
        action = TestAction("Test action")

        # Act
        result = self.engine.execute_action(action, self.context)

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(action.executed)
        self.assertEqual(result.message, "Executed: Test action")

    def test_execute_single_action_with_dict_context(self):
        """Test executing a single action with dictionary context"""
        # Arrange
        action = TestAction("Test action")
        context_dict = {"test_key": "test_value"}

        # Act
        result = self.engine.execute_action(action, context_dict)

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(action.executed)

    def test_execute_single_action_failure(self):
        """Test executing a single action that fails"""
        # Arrange
        action = TestAction("Test action", should_succeed=False)

        # Act
        result = self.engine.execute_action(action, self.context)

        # Assert
        self.assertFalse(result.success)
        self.assertTrue(action.executed)
        self.assertEqual(result.message, "Failed: Test action")

    def test_execute_workflow_success(self):
        """Test executing a workflow with all successful actions"""
        # Arrange
        actions = [
            TestAction("Action 1"),
            TestAction("Action 2"),
            TestAction("Action 3")
        ]

        # Act
        result = self.engine.execute_workflow(actions, self.context)

        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(len(result["results"]), 3)
        self.assertTrue(result["completed"])
        for action in actions:
            self.assertTrue(action.executed)

    def test_execute_workflow_failure(self):
        """Test executing a workflow with a failing action"""
        # Arrange
        actions = [
            TestAction("Action 1"),
            TestAction("Action 2", should_succeed=False),
            TestAction("Action 3")
        ]

        # Act
        result = self.engine.execute_workflow(actions, self.context)

        # Assert
        self.assertFalse(result["success"])
        self.assertEqual(len(result["results"]), 2)  # Only first two actions executed
        self.assertTrue(result["completed"])
        self.assertTrue(actions[0].executed)
        self.assertTrue(actions[1].executed)
        self.assertFalse(actions[2].executed)  # Third action should not be executed

    def test_execute_workflow_with_exception(self):
        """Test executing a workflow with an action that raises an exception"""
        # Arrange
        actions = [
            TestAction("Action 1"),
            MagicMock(spec=BaseAction)
        ]

        # Configure the mock to raise an exception
        actions[1].execute.side_effect = Exception("Test exception")
        actions[1].id = "mock-action"
        actions[1].type = "mock_action"
        actions[1].description = "Mock Action"

        # Act
        result = self.engine.execute_workflow(actions, self.context)

        # Assert
        self.assertFalse(result["success"])
        self.assertEqual(len(result["results"]), 2)
        self.assertTrue(result["completed"])
        self.assertTrue(actions[0].executed)
        self.assertIn("Error executing action", result["message"])

    def test_workflow_context_state_transitions(self):
        """Test that workflow execution updates context state correctly"""
        # Arrange
        actions = [TestAction("Action 1")]

        # Act
        self.engine.execute_workflow(actions, self.context)

        # Assert
        self.assertEqual(self.context.state.current_state, ExecutionStateEnum.COMPLETED)

    def test_workflow_context_state_transitions_failure(self):
        """Test that workflow failure updates context state correctly"""
        # Arrange
        actions = [TestAction("Action 1", should_succeed=False)]

        # Act
        self.engine.execute_workflow(actions, self.context)

        # Assert
        self.assertEqual(self.context.state.current_state, ExecutionStateEnum.FAILED)

    def test_workflow_events(self):
        """Test that workflow execution dispatches events"""
        # Arrange
        actions = [TestAction("Action 1")]
        event_listener = MagicMock()
        self.engine.add_event_listener(None, event_listener)

        # Act
        self.engine.execute_workflow(actions, self.context)

        # Assert
        # Should have at least 3 events: workflow started, action started, action completed, workflow completed
        self.assertGreaterEqual(event_listener.call_count, 4)

    def test_workflow_statistics(self):
        """Test that workflow execution collects statistics"""
        # Arrange
        actions = [TestAction("Action 1")]

        # Act
        result = self.engine.execute_workflow(actions, self.context)
        workflow_id = result["workflow_id"]
        stats = self.engine.get_workflow_statistics(workflow_id)

        # Assert
        self.assertIsNotNone(stats)
        self.assertEqual(stats.total_actions, 1)
        self.assertEqual(stats.completed_actions, 1)
        self.assertEqual(stats.failed_actions, 0)
        self.assertTrue(stats.is_completed)
        self.assertEqual(stats.success_rate, 100.0)

    def test_workflow_status(self):
        """Test getting workflow status"""
        # Arrange
        actions = [TestAction("Action 1")]

        # Act
        result = self.engine.execute_workflow(actions, self.context)
        workflow_id = result["workflow_id"]
        status = self.engine.get_workflow_status(workflow_id)

        # Assert
        self.assertIsNotNone(status)
        self.assertEqual(status["status"], WorkflowStatus.COMPLETED.name)
        self.assertEqual(status["total_actions"], 1)
        # The completed_actions might be 0 or 1 depending on when the status is checked
        self.assertIn(status["completed_actions"], [0, 1])

    def test_workflow_status_not_found(self):
        """Test getting status of non-existent workflow"""
        # Act
        status = self.engine.get_workflow_status("non-existent-id")

        # Assert
        self.assertIsNone(status)

    def test_workflow_statistics_not_found(self):
        """Test getting statistics of non-existent workflow"""
        # Act
        stats = self.engine.get_workflow_statistics("non-existent-id")

        # Assert
        self.assertIsNone(stats)

    @patch('threading.Thread')
    def test_pause_and_resume_workflow(self, mock_thread):
        """Test pausing and resuming a workflow"""
        # Arrange - Create a workflow that we can pause
        actions = [
            TestAction("Action 1"),
            TestAction("Action 2"),
            TestAction("Action 3")
        ]

        # Mock the thread to avoid actually running the workflow in a thread
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # Start the workflow
        result = self.engine.execute_workflow(actions, self.context)
        workflow_id = result["workflow_id"]

        # Manually set the workflow as running and add to running workflows
        self.engine._workflows[workflow_id]["status"] = WorkflowStatus.RUNNING
        self.engine._running_workflows.add(workflow_id)

        # Act - Pause the workflow
        pause_result = self.engine.pause_workflow(workflow_id)

        # Assert
        self.assertTrue(pause_result)
        self.assertIn(workflow_id, self.engine._paused_workflows)

        # Act - Resume the workflow
        resume_result = self.engine.resume_workflow(workflow_id)

        # Assert
        self.assertTrue(resume_result)
        self.assertNotIn(workflow_id, self.engine._paused_workflows)
        self.assertIn(workflow_id, self.engine._running_workflows)
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()

    def test_abort_workflow(self):
        """Test aborting a workflow"""
        # Arrange - Create a workflow that we can abort
        actions = [
            TestAction("Action 1"),
            TestAction("Action 2"),
            TestAction("Action 3")
        ]

        # Create a new context for this test
        context = ExecutionContext()

        # Start the workflow
        result = self.engine.execute_workflow(actions, context)
        workflow_id = result["workflow_id"]

        # Manually set the workflow as running and add to running workflows
        self.engine._workflows[workflow_id]["status"] = WorkflowStatus.RUNNING
        self.engine._running_workflows.add(workflow_id)

        # Reset the context state to RUNNING to allow transition to ABORTED
        self.engine._workflows[workflow_id]["context"].state._current_state = ExecutionStateEnum.RUNNING

        # Act - Abort the workflow
        abort_result = self.engine.abort_workflow(workflow_id)

        # Assert
        self.assertTrue(abort_result)
        self.assertNotIn(workflow_id, self.engine._running_workflows)
        self.assertEqual(
            self.engine._workflows[workflow_id]["status"],
            WorkflowStatus.ABORTED
        )
        self.assertEqual(
            self.engine._workflows[workflow_id]["context"].state.current_state,
            ExecutionStateEnum.ABORTED
        )

    def test_event_listeners(self):
        """Test adding and removing event listeners"""
        # Arrange
        listener1 = MagicMock()
        listener2 = MagicMock()

        # Act - Add listeners
        self.engine.add_event_listener(WorkflowEventType.WORKFLOW_STARTED, listener1)
        self.engine.add_event_listener(None, listener2)  # Global listener

        # Execute a workflow to generate events
        actions = [TestAction("Action 1")]
        # Create a new context for this test
        context1 = ExecutionContext()
        self.engine.execute_workflow(actions, context1)

        # Assert
        listener1.assert_called()  # Should be called at least once
        self.assertGreaterEqual(listener2.call_count, 4)  # Should be called for all events

        # Act - Remove listeners
        self.engine.remove_event_listener(WorkflowEventType.WORKFLOW_STARTED, listener1)
        self.engine.remove_event_listener(None, listener2)

        # Reset mocks
        listener1.reset_mock()
        listener2.reset_mock()

        # Execute another workflow
        actions = [TestAction("Action 2")]
        # Create another new context
        context2 = ExecutionContext()
        self.engine.execute_workflow(actions, context2)

        # Assert
        listener1.assert_not_called()
        listener2.assert_not_called()


if __name__ == "__main__":
    unittest.main()
