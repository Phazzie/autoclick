"""Tests for the workflow engine interface"""
import unittest
from unittest.mock import MagicMock
from typing import Dict, Any, List, Optional, Callable, Union

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.context.execution_context import ExecutionContext
from src.core.workflow.workflow_engine_interface import WorkflowEngineInterface
from src.core.workflow.workflow_event import WorkflowEvent, WorkflowEventType
from src.core.workflow.workflow_statistics import WorkflowStatistics


class MockWorkflowEngine(WorkflowEngineInterface):
    """Mock implementation of WorkflowEngineInterface for testing"""

    def __init__(self):
        """Initialize the mock workflow engine"""
        self.execute_action_called = False
        self.execute_workflow_called = False
        self.pause_workflow_called = False
        self.resume_workflow_called = False
        self.abort_workflow_called = False
        self.get_workflow_status_called = False
        self.get_workflow_statistics_called = False
        self.add_event_listener_called = False
        self.remove_event_listener_called = False

    def execute_action(
        self,
        action: BaseAction,
        context: Union[ExecutionContext, Dict[str, Any]]
    ) -> ActionResult:
        """Mock implementation of execute_action"""
        self.execute_action_called = True
        self.last_action = action
        self.last_context = context
        return ActionResult.create_success("Mock action executed")

    def execute_workflow(
        self,
        actions: List[BaseAction],
        context: Optional[Union[ExecutionContext, Dict[str, Any]]] = None,
        workflow_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Mock implementation of execute_workflow"""
        self.execute_workflow_called = True
        self.last_actions = actions
        self.last_context = context
        self.last_workflow_id = workflow_id
        return {
            "workflow_id": workflow_id or "mock-workflow-id",
            "success": True,
            "message": "Mock workflow executed",
            "results": [ActionResult.create_success("Mock action executed")],
            "completed": True
        }

    def pause_workflow(self, workflow_id: str) -> bool:
        """Mock implementation of pause_workflow"""
        self.pause_workflow_called = True
        self.last_workflow_id = workflow_id
        return True

    def resume_workflow(self, workflow_id: str) -> bool:
        """Mock implementation of resume_workflow"""
        self.resume_workflow_called = True
        self.last_workflow_id = workflow_id
        return True

    def abort_workflow(self, workflow_id: str) -> bool:
        """Mock implementation of abort_workflow"""
        self.abort_workflow_called = True
        self.last_workflow_id = workflow_id
        return True

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Mock implementation of get_workflow_status"""
        self.get_workflow_status_called = True
        self.last_workflow_id = workflow_id
        return {
            "workflow_id": workflow_id,
            "status": "COMPLETED",
            "current_index": 1,
            "total_actions": 1,
            "completed_actions": 1,
            "context_state": "COMPLETED"
        }

    def get_workflow_statistics(self, workflow_id: str) -> Optional[WorkflowStatistics]:
        """Mock implementation of get_workflow_statistics"""
        self.get_workflow_statistics_called = True
        self.last_workflow_id = workflow_id
        return WorkflowStatistics()

    def add_event_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """Mock implementation of add_event_listener"""
        self.add_event_listener_called = True
        self.last_event_type = event_type
        self.last_listener = listener

    def remove_event_listener(
        self,
        event_type: Optional[WorkflowEventType],
        listener: Callable[[WorkflowEvent], None]
    ) -> None:
        """Mock implementation of remove_event_listener"""
        self.remove_event_listener_called = True
        self.last_event_type = event_type
        self.last_listener = listener


class TestWorkflowEngineInterface(unittest.TestCase):
    """Test cases for the workflow engine interface"""

    def setUp(self):
        """Set up test environment"""
        self.engine = MockWorkflowEngine()
        self.mock_action = MagicMock(spec=BaseAction)
        self.mock_action.id = "mock-action-id"
        self.mock_action.type = "mock_action"
        self.mock_action.description = "Mock Action"
        self.context = ExecutionContext()

    def test_execute_action(self):
        """Test execute_action method"""
        # Act
        result = self.engine.execute_action(self.mock_action, self.context)

        # Assert
        self.assertTrue(self.engine.execute_action_called)
        self.assertEqual(self.engine.last_action, self.mock_action)
        self.assertEqual(self.engine.last_context, self.context)
        self.assertTrue(result.success)

    def test_execute_workflow(self):
        """Test execute_workflow method"""
        # Arrange
        actions = [self.mock_action]

        # Act
        result = self.engine.execute_workflow(actions, self.context, "test-workflow-id")

        # Assert
        self.assertTrue(self.engine.execute_workflow_called)
        self.assertEqual(self.engine.last_actions, actions)
        self.assertEqual(self.engine.last_context, self.context)
        self.assertEqual(self.engine.last_workflow_id, "test-workflow-id")
        self.assertTrue(result["success"])
        self.assertEqual(result["workflow_id"], "test-workflow-id")

    def test_pause_workflow(self):
        """Test pause_workflow method"""
        # Act
        result = self.engine.pause_workflow("test-workflow-id")

        # Assert
        self.assertTrue(self.engine.pause_workflow_called)
        self.assertEqual(self.engine.last_workflow_id, "test-workflow-id")
        self.assertTrue(result)

    def test_resume_workflow(self):
        """Test resume_workflow method"""
        # Act
        result = self.engine.resume_workflow("test-workflow-id")

        # Assert
        self.assertTrue(self.engine.resume_workflow_called)
        self.assertEqual(self.engine.last_workflow_id, "test-workflow-id")
        self.assertTrue(result)

    def test_abort_workflow(self):
        """Test abort_workflow method"""
        # Act
        result = self.engine.abort_workflow("test-workflow-id")

        # Assert
        self.assertTrue(self.engine.abort_workflow_called)
        self.assertEqual(self.engine.last_workflow_id, "test-workflow-id")
        self.assertTrue(result)

    def test_get_workflow_status(self):
        """Test get_workflow_status method"""
        # Act
        status = self.engine.get_workflow_status("test-workflow-id")

        # Assert
        self.assertTrue(self.engine.get_workflow_status_called)
        self.assertEqual(self.engine.last_workflow_id, "test-workflow-id")
        self.assertIsNotNone(status)
        self.assertEqual(status["workflow_id"], "test-workflow-id")
        self.assertEqual(status["status"], "COMPLETED")

    def test_get_workflow_statistics(self):
        """Test get_workflow_statistics method"""
        # Act
        stats = self.engine.get_workflow_statistics("test-workflow-id")

        # Assert
        self.assertTrue(self.engine.get_workflow_statistics_called)
        self.assertEqual(self.engine.last_workflow_id, "test-workflow-id")
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, WorkflowStatistics)

    def test_add_event_listener(self):
        """Test add_event_listener method"""
        # Arrange
        listener = MagicMock()

        # Act
        self.engine.add_event_listener(WorkflowEventType.WORKFLOW_STARTED, listener)

        # Assert
        self.assertTrue(self.engine.add_event_listener_called)
        self.assertEqual(self.engine.last_event_type, WorkflowEventType.WORKFLOW_STARTED)
        self.assertEqual(self.engine.last_listener, listener)

    def test_remove_event_listener(self):
        """Test remove_event_listener method"""
        # Arrange
        listener = MagicMock()

        # Act
        self.engine.remove_event_listener(WorkflowEventType.WORKFLOW_STARTED, listener)

        # Assert
        self.assertTrue(self.engine.remove_event_listener_called)
        self.assertEqual(self.engine.last_event_type, WorkflowEventType.WORKFLOW_STARTED)
        self.assertEqual(self.engine.last_listener, listener)


if __name__ == "__main__":
    unittest.main()
