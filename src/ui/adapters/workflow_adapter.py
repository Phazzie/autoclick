"""
Adapter for WorkflowEngine to provide the interface expected by the UI.
SOLID: Single responsibility - adapting workflow operations.
KISS: Simple delegation to WorkflowEngine.
"""
import uuid
from typing import List, Dict, Any, Optional, Tuple

from src.core.workflow.workflow_engine import WorkflowEngine, WorkflowStatus
from src.core.actions.base_action import BaseAction
from src.core.context.execution_context import ExecutionContext
from src.core.models import Workflow as UIWorkflow, WorkflowNode as UIWorkflowNode, WorkflowConnection as UIWorkflowConnection

class WorkflowAdapter:
    """Adapter for WorkflowEngine to provide the interface expected by the UI."""

    def __init__(self, workflow_engine: Optional[WorkflowEngine] = None):
        """Initialize the adapter with a WorkflowEngine instance."""
        self.workflow_engine = workflow_engine
        self.workflows: Dict[str, UIWorkflow] = {}

    def get_node_types(self) -> List[Dict[str, Any]]:
        """
        Get all available node types.

        Returns:
            List of node types with metadata
        """
        return [
            {"type": "Start", "name": "Start", "description": "Start of workflow"},
            {"type": "Click", "name": "Click", "description": "Click on element"},
            {"type": "Type", "name": "Type", "description": "Type text"},
            {"type": "Wait", "name": "Wait", "description": "Wait for time or element"},
            {"type": "Condition", "name": "Condition", "description": "Branch based on condition"},
            {"type": "Loop", "name": "Loop", "description": "Repeat actions"},
            {"type": "End", "name": "End", "description": "End of workflow"}
        ]

    def get_all_workflows(self) -> List[UIWorkflow]:
        """
        Get all workflows.

        Returns:
            List of workflows in the UI-expected format.
        """
        return list(self.workflows.values())

    def get_workflow(self, workflow_id: str) -> Optional[UIWorkflow]:
        """
        Get a workflow by ID.

        Args:
            workflow_id: Workflow ID

        Returns:
            Workflow in the UI-expected format, or None if not found.
        """
        return self.workflows.get(workflow_id)

    def create_workflow(self, workflow: UIWorkflow) -> UIWorkflow:
        """
        Create a new workflow.

        Args:
            workflow: Workflow to create

        Returns:
            The new workflow in the UI-expected format.
        """
        # Store the workflow
        self.workflows[workflow.id] = workflow

        return workflow

    def update_workflow(self, workflow: UIWorkflow) -> UIWorkflow:
        """
        Update an existing workflow.

        Args:
            workflow: Workflow in the UI-expected format

        Returns:
            The updated workflow in the UI-expected format.
        """
        self.workflows[workflow.id] = workflow
        return workflow

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.

        Args:
            workflow_id: Workflow ID

        Returns:
            True if the workflow was deleted, False if not found.
        """
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
            return True
        return False

    def execute_workflow(self, workflow: UIWorkflow) -> Dict[str, Any]:
        """
        Execute a workflow.

        Args:
            workflow: Workflow in the UI-expected format

        Returns:
            Dictionary containing workflow execution results.
        """
        # Convert UI workflow to backend actions
        actions = self._convert_to_actions(workflow)

        # Create execution context
        context = ExecutionContext()

        # Execute the workflow
        return self.workflow_engine.execute_workflow(actions, context, workflow.id)

    def get_workflow_status(self, workflow_id: str) -> str:
        """
        Get the status of a workflow.

        Args:
            workflow_id: Workflow ID

        Returns:
            Status string.
        """
        if workflow_id in self.workflow_engine._workflows:
            status = self.workflow_engine._workflows[workflow_id]["status"]
            return status.name
        return "Unknown"

    def _convert_to_actions(self, workflow: UIWorkflow) -> List[BaseAction]:
        """
        Convert a UI workflow to a list of backend actions.

        Args:
            workflow: Workflow in the UI-expected format

        Returns:
            List of backend actions.
        """
        # This is a placeholder implementation
        # In a real implementation, we would convert the workflow nodes and connections
        # to a list of actions that the WorkflowEngine can execute
        return []
