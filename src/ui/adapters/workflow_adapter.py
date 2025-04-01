"""
Adapter for WorkflowService to provide the interface expected by the UI.
SOLID: Single responsibility - adapting workflow operations.
KISS: Simple delegation to WorkflowService.
"""
from typing import List, Dict, Any, Optional

from src.core.workflow.workflow_service import WorkflowService, WorkflowValidationError
from src.core.models import Workflow as UIWorkflow

class WorkflowAdapter:
    """Adapter for WorkflowService to provide the interface expected by the UI."""

    def __init__(self, workflow_service: Optional[WorkflowService] = None):
        """Initialize the adapter with a WorkflowService instance."""
        self.workflow_service = workflow_service or WorkflowService()

    def get_node_types(self) -> List[Dict[str, Any]]:
        """
        Get all available node types.

        Returns:
            List of node types with metadata
        """
        return self.workflow_service.get_node_types()

    def get_all_workflows(self) -> List[UIWorkflow]:
        """
        Get all workflows.

        Returns:
            List of workflows in the UI-expected format.
        """
        return self.workflow_service.get_workflows()

    def get_workflow(self, workflow_id: str) -> Optional[UIWorkflow]:
        """
        Get a workflow by ID.

        Args:
            workflow_id: Workflow ID

        Returns:
            Workflow in the UI-expected format, or None if not found.
        """
        return self.workflow_service.get_workflow(workflow_id)

    def create_workflow(self, workflow: UIWorkflow) -> UIWorkflow:
        """
        Create a new workflow.

        Args:
            workflow: Workflow to create

        Returns:
            The new workflow in the UI-expected format.

        Raises:
            ValueError: If a workflow with the same ID already exists
            WorkflowValidationError: If the workflow fails validation
        """
        return self.workflow_service.create_workflow(workflow)

    def update_workflow(self, workflow: UIWorkflow) -> UIWorkflow:
        """
        Update an existing workflow.

        Args:
            workflow: Workflow in the UI-expected format

        Returns:
            The updated workflow in the UI-expected format.

        Raises:
            ValueError: If the workflow doesn't exist
            WorkflowValidationError: If the workflow fails validation
        """
        return self.workflow_service.update_workflow(workflow)

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.

        Args:
            workflow_id: Workflow ID

        Returns:
            True if the workflow was deleted, False if not found.
        """
        return self.workflow_service.delete_workflow(workflow_id)

    def execute_workflow(self, workflow: UIWorkflow) -> Dict[str, Any]:
        """
        Execute a workflow.

        Args:
            workflow: Workflow in the UI-expected format

        Returns:
            Dictionary containing workflow execution results.

        Raises:
            ValueError: If the workflow doesn't exist
            WorkflowValidationError: If the workflow fails validation
        """
        # Make sure the workflow is saved/updated before execution
        if self.workflow_service.get_workflow(workflow.id) is None:
            self.workflow_service.create_workflow(workflow)
        else:
            self.workflow_service.update_workflow(workflow)

        # Execute the workflow
        return self.workflow_service.execute_workflow(workflow.id)

    def get_workflow_status(self, workflow_id: str) -> str:
        """
        Get the status of a workflow.

        Args:
            workflow_id: Workflow ID

        Returns:
            Status string.
        """
        # Check if the workflow exists
        if self.workflow_service.get_workflow(workflow_id):
            # This would need to be implemented in the WorkflowService
            # For now, we'll return a placeholder for existing workflows
            return "Pending"
        return "Unknown"

    def validate_workflow(self, workflow: UIWorkflow) -> List[str]:
        """
        Validate a workflow.

        Args:
            workflow: Workflow to validate

        Returns:
            List of validation errors, empty if valid
        """
        try:
            # Use the service's validation method
            self.workflow_service._validate_workflow(workflow)
            return []
        except WorkflowValidationError as e:
            # Return the validation errors as a list
            return str(e).replace("Workflow validation failed: ", "").split("; ")
