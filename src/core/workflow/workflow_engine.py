"""Implementation of the workflow execution engine"""
import uuid
import logging
import threading
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Callable, Union, Set

from src.core.actions.action_interface import ActionResult
from src.core.actions.base_action import BaseAction
from src.core.context.execution_context import ExecutionContext
from src.core.context.execution_state import ExecutionStateEnum
from src.core.workflow.workflow_engine_interface import WorkflowEngineInterface
from src.core.workflow.workflow_event import (
    WorkflowEvent, WorkflowEventType, WorkflowStateEvent, ActionEvent, EventDispatcher
)
from src.core.workflow.workflow_statistics import WorkflowStatistics


class WorkflowStatus(Enum):
    """Status of a workflow"""
    PENDING = auto()    # Workflow is created but not started
    RUNNING = auto()    # Workflow is currently running
    PAUSED = auto()     # Workflow is paused
    COMPLETED = auto()  # Workflow completed successfully
    FAILED = auto()     # Workflow failed with an error
    ABORTED = auto()    # Workflow was manually aborted


class WorkflowEngine(WorkflowEngineInterface):
    """Engine for executing workflows"""

    def __init__(self):
        """Initialize the workflow engine"""
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._event_dispatcher = EventDispatcher()
        self._workflows: Dict[str, Dict[str, Any]] = {}
        self._running_workflows: Set[str] = set()
        self._paused_workflows: Set[str] = set()
        self._workflow_locks: Dict[str, threading.Lock] = {}
        self._statistics: Dict[str, WorkflowStatistics] = {}

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
        # Convert dictionary context to ExecutionContext if needed
        if isinstance(context, dict):
            execution_context = ExecutionContext()
            for key, value in context.items():
                execution_context.variables.set(key, value)
        else:
            execution_context = context

        # Create a context dictionary for the action
        action_context = execution_context.variables.get_all()

        # Execute the action
        self.logger.info(f"Executing action: {action.description}")
        result = action.execute(action_context)

        # Update the context with any new variables from the result
        if result.success and result.data:
            for key, value in result.data.items():
                execution_context.variables.set(key, value)

        return result

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
        # Generate workflow ID if not provided
        workflow_id = workflow_id or str(uuid.uuid4())

        # Create a lock for this workflow
        self._workflow_locks[workflow_id] = threading.Lock()

        # Create execution context if not provided
        if context is None:
            execution_context = ExecutionContext()
        elif isinstance(context, dict):
            execution_context = ExecutionContext()
            for key, value in context.items():
                execution_context.variables.set(key, value)
        else:
            execution_context = context

        # Initialize workflow state
        self._workflows[workflow_id] = {
            "id": workflow_id,
            "actions": actions,
            "context": execution_context,
            "current_index": 0,
            "status": WorkflowStatus.PENDING,
            "results": []
        }

        # Create statistics collector
        self._statistics[workflow_id] = WorkflowStatistics()

        # Start the workflow
        return self._run_workflow(workflow_id)

    def _run_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Run a workflow with the given ID

        Args:
            workflow_id: ID of the workflow to run

        Returns:
            Dictionary containing workflow execution results
        """
        if workflow_id not in self._workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")

        workflow = self._workflows[workflow_id]
        actions = workflow["actions"]
        context = workflow["context"]
        results = []

        # Mark workflow as running
        with self._workflow_locks[workflow_id]:
            workflow["status"] = WorkflowStatus.RUNNING
            self._running_workflows.add(workflow_id)

        # Transition context to running state
        context.state.transition_to(ExecutionStateEnum.RUNNING)

        # Dispatch workflow started event
        self._dispatch_workflow_event(
            WorkflowEventType.WORKFLOW_STARTED,
            workflow_id,
            {"total_actions": len(actions)}
        )

        # Execute each action in sequence
        success = True
        error_message = None

        for i, action in enumerate(actions):
            # Check if workflow should be paused or aborted
            with self._workflow_locks[workflow_id]:
                if workflow_id in self._paused_workflows:
                    # Workflow is paused, save current index and return
                    workflow["current_index"] = i
                    workflow["status"] = WorkflowStatus.PAUSED
                    return {
                        "workflow_id": workflow_id,
                        "success": None,
                        "message": "Workflow paused",
                        "results": results,
                        "completed": False
                    }
                
                if workflow_id not in self._running_workflows:
                    # Workflow was aborted
                    workflow["status"] = WorkflowStatus.ABORTED
                    context.state.transition_to(ExecutionStateEnum.ABORTED)
                    self._dispatch_workflow_event(
                        WorkflowEventType.WORKFLOW_ABORTED,
                        workflow_id
                    )
                    return {
                        "workflow_id": workflow_id,
                        "success": False,
                        "message": "Workflow aborted",
                        "results": results,
                        "completed": False
                    }

                # Update current index
                workflow["current_index"] = i

            # Dispatch action started event
            self._dispatch_action_event(
                WorkflowEventType.ACTION_STARTED,
                workflow_id,
                action,
                i
            )

            # Execute the action
            try:
                result = self.execute_action(action, context)
                results.append(result)

                if result.success:
                    # Dispatch action completed event
                    self._dispatch_action_event(
                        WorkflowEventType.ACTION_COMPLETED,
                        workflow_id,
                        action,
                        i,
                        result
                    )
                else:
                    # Action failed
                    success = False
                    error_message = f"Action failed: {result.message}"
                    
                    # Dispatch action failed event
                    self._dispatch_action_event(
                        WorkflowEventType.ACTION_FAILED,
                        workflow_id,
                        action,
                        i,
                        result
                    )
                    
                    # Stop execution on first failure
                    break
            except Exception as e:
                # Handle unexpected exceptions
                self.logger.error(f"Error executing action: {str(e)}", exc_info=True)
                success = False
                error_message = f"Error executing action: {str(e)}"
                
                # Create failure result
                failure_result = ActionResult.create_failure(str(e))
                results.append(failure_result)
                
                # Dispatch action failed event
                self._dispatch_action_event(
                    WorkflowEventType.ACTION_FAILED,
                    workflow_id,
                    action,
                    i,
                    failure_result
                )
                
                # Stop execution on exception
                break

        # Update workflow status and context state
        with self._workflow_locks[workflow_id]:
            if success:
                workflow["status"] = WorkflowStatus.COMPLETED
                context.state.transition_to(ExecutionStateEnum.COMPLETED)
                self._dispatch_workflow_event(
                    WorkflowEventType.WORKFLOW_COMPLETED,
                    workflow_id
                )
            else:
                workflow["status"] = WorkflowStatus.FAILED
                context.state.transition_to(ExecutionStateEnum.FAILED)
                self._dispatch_workflow_event(
                    WorkflowEventType.WORKFLOW_FAILED,
                    workflow_id,
                    {"error": error_message}
                )

            # Store results
            workflow["results"] = results
            
            # Remove from running workflows
            if workflow_id in self._running_workflows:
                self._running_workflows.remove(workflow_id)

        # Return workflow results
        return {
            "workflow_id": workflow_id,
            "success": success,
            "message": "Workflow completed successfully" if success else error_message,
            "results": results,
            "completed": True
        }

    def pause_workflow(self, workflow_id: str) -> bool:
        """
        Pause a running workflow

        Args:
            workflow_id: ID of the workflow to pause

        Returns:
            True if the workflow was paused, False otherwise
        """
        if workflow_id not in self._workflows:
            return False

        with self._workflow_locks[workflow_id]:
            if workflow_id not in self._running_workflows:
                return False

            self._paused_workflows.add(workflow_id)
            self._dispatch_workflow_event(
                WorkflowEventType.WORKFLOW_PAUSED,
                workflow_id
            )
            return True

    def resume_workflow(self, workflow_id: str) -> bool:
        """
        Resume a paused workflow

        Args:
            workflow_id: ID of the workflow to resume

        Returns:
            True if the workflow was resumed, False otherwise
        """
        if workflow_id not in self._workflows:
            return False

        with self._workflow_locks[workflow_id]:
            if workflow_id not in self._paused_workflows:
                return False

            self._paused_workflows.remove(workflow_id)
            self._running_workflows.add(workflow_id)
            self._dispatch_workflow_event(
                WorkflowEventType.WORKFLOW_RESUMED,
                workflow_id
            )

        # Continue execution in a new thread
        threading.Thread(
            target=self._run_workflow,
            args=(workflow_id,),
            daemon=True
        ).start()

        return True

    def abort_workflow(self, workflow_id: str) -> bool:
        """
        Abort a running or paused workflow

        Args:
            workflow_id: ID of the workflow to abort

        Returns:
            True if the workflow was aborted, False otherwise
        """
        if workflow_id not in self._workflows:
            return False

        with self._workflow_locks[workflow_id]:
            if (
                workflow_id not in self._running_workflows
                and workflow_id not in self._paused_workflows
            ):
                return False

            # Remove from running and paused workflows
            if workflow_id in self._running_workflows:
                self._running_workflows.remove(workflow_id)
            if workflow_id in self._paused_workflows:
                self._paused_workflows.remove(workflow_id)

            # Update workflow status
            workflow = self._workflows[workflow_id]
            workflow["status"] = WorkflowStatus.ABORTED
            
            # Update context state
            context = workflow["context"]
            context.state.transition_to(ExecutionStateEnum.ABORTED)
            
            # Dispatch workflow aborted event
            self._dispatch_workflow_event(
                WorkflowEventType.WORKFLOW_ABORTED,
                workflow_id
            )

            return True

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            Dictionary containing workflow status or None if not found
        """
        if workflow_id not in self._workflows:
            return None

        workflow = self._workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "status": workflow["status"].name,
            "current_index": workflow["current_index"],
            "total_actions": len(workflow["actions"]),
            "completed_actions": min(workflow["current_index"], len(workflow["actions"])),
            "context_state": workflow["context"].state.current_state.name
        }

    def get_workflow_statistics(self, workflow_id: str) -> Optional[WorkflowStatistics]:
        """
        Get statistics for a workflow

        Args:
            workflow_id: ID of the workflow

        Returns:
            WorkflowStatistics object or None if not found
        """
        return self._statistics.get(workflow_id)

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
        self._event_dispatcher.add_listener(event_type, listener)

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
        self._event_dispatcher.remove_listener(event_type, listener)

    def _dispatch_workflow_event(
        self,
        event_type: WorkflowEventType,
        workflow_id: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Dispatch a workflow state event

        Args:
            event_type: Type of the event
            workflow_id: ID of the workflow
            data: Additional event data
        """
        event = WorkflowStateEvent(event_type, workflow_id, data=data)
        self._event_dispatcher.dispatch(event)
        
        # Record event in statistics
        if workflow_id in self._statistics:
            self._statistics[workflow_id].record_event(event)

    def _dispatch_action_event(
        self,
        event_type: WorkflowEventType,
        workflow_id: str,
        action: BaseAction,
        action_index: int,
        result: Optional[ActionResult] = None
    ) -> None:
        """
        Dispatch an action event

        Args:
            event_type: Type of the event
            workflow_id: ID of the workflow
            action: The action that was executed
            action_index: Index of the action in the workflow
            result: Result of the action execution (for completed/failed events)
        """
        event = ActionEvent(event_type, workflow_id, action, action_index, result)
        self._event_dispatcher.dispatch(event)
        
        # Record event in statistics
        if workflow_id in self._statistics:
            self._statistics[workflow_id].record_event(event)
