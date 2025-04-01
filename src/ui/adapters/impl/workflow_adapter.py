"""
Workflow adapter implementation.

This module provides a concrete implementation of the workflow adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.workflow.workflow_service_new import WorkflowService
from src.core.workflow.workflow_query import WorkflowQueryBuilder
from src.ui.adapters.base.base_workflow_adapter import BaseWorkflowAdapter


class WorkflowAdapter(BaseWorkflowAdapter):
    """Concrete implementation of workflow adapter."""
    
    def __init__(self, workflow_service: Optional[WorkflowService] = None):
        """
        Initialize the adapter with a WorkflowService instance.
        
        Args:
            workflow_service: Optional workflow service to use
        """
        self._workflow_service = workflow_service or WorkflowService()
    
    def get_workflow_types(self) -> List[Dict[str, Any]]:
        """
        Get all available workflow types.
        
        Returns:
            List of workflow types with metadata
        """
        # Currently there's only one workflow type
        return [{
            "id": "standard",
            "name": "Standard Workflow",
            "description": "Standard workflow with steps and actions",
            "icon": "workflow"
        }]
    
    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """
        Get all workflows.
        
        Returns:
            List of workflows in the UI-expected format
        """
        # Get all workflows from the service
        workflow_dtos = self._workflow_service.get_workflows()
        
        # Convert to UI format
        return [self._convert_workflow_to_ui_format(dto) for dto in workflow_dtos]
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow in the UI-expected format, or None if not found
        """
        # Get the workflow from the service
        workflow_dto = self._workflow_service.get_workflow(workflow_id)
        
        # Return None if not found
        if workflow_dto is None:
            return None
        
        # Convert to UI format
        return self._convert_workflow_to_ui_format(workflow_dto)
    
    def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new workflow.
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            Created workflow in the UI-expected format
            
        Raises:
            ValueError: If the workflow data is invalid
        """
        # Validate the workflow data
        errors = self.validate_workflow(workflow_data)
        if errors:
            raise ValueError(f"Invalid workflow data: {', '.join(errors)}")
        
        # Convert from UI format to service format
        service_data = self._convert_workflow_from_ui_format(workflow_data)
        
        # Create the workflow
        workflow_dto = self._workflow_service.create_workflow(service_data)
        
        # Convert back to UI format
        return self._convert_workflow_to_ui_format(workflow_dto)
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a workflow.
        
        Args:
            workflow_id: Workflow ID
            workflow_data: Workflow data
            
        Returns:
            Updated workflow in the UI-expected format, or None if not found
            
        Raises:
            ValueError: If the workflow data is invalid
        """
        # Validate the workflow data
        errors = self.validate_workflow(workflow_data)
        if errors:
            raise ValueError(f"Invalid workflow data: {', '.join(errors)}")
        
        # Convert from UI format to service format
        service_data = self._convert_workflow_from_ui_format(workflow_data)
        
        # Update the workflow
        workflow_dto = self._workflow_service.update_workflow(workflow_id, service_data)
        
        # Return None if not found
        if workflow_dto is None:
            return None
        
        # Convert back to UI format
        return self._convert_workflow_to_ui_format(workflow_dto)
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            True if the workflow was deleted, False if not found
        """
        # Delete the workflow
        return self._workflow_service.delete_workflow(workflow_id)
    
    def execute_workflow(self, workflow_id: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a workflow.
        
        Args:
            workflow_id: Workflow ID
            context_data: Optional context data
            
        Returns:
            Result of the workflow execution
            
        Raises:
            ValueError: If the workflow is not found or cannot be executed
        """
        # Execute the workflow
        try:
            result = self._workflow_service.execute_workflow(workflow_id, context_data)
            return result
        except Exception as e:
            raise ValueError(f"Error executing workflow: {str(e)}")
    
    def validate_workflow(self, workflow_data: Dict[str, Any]) -> List[str]:
        """
        Validate a workflow.
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            List of validation errors, empty if valid
        """
        # Convert from UI format to service format
        service_data = self._convert_workflow_from_ui_format(workflow_data)
        
        # Validate the workflow
        return self._workflow_service.validate_workflow(service_data)
    
    def _convert_workflow_to_ui_format(self, workflow_dto: Any) -> Dict[str, Any]:
        """
        Convert a workflow DTO to UI format.
        
        Args:
            workflow_dto: Workflow DTO from the service
            
        Returns:
            Workflow in UI format
        """
        return {
            "id": workflow_dto.workflow_id,
            "name": workflow_dto.name,
            "description": workflow_dto.description,
            "version": workflow_dto.version,
            "enabled": workflow_dto.enabled,
            "steps": workflow_dto.steps,
            "stepCount": workflow_dto.step_count,
            "createdAt": workflow_dto.created_at,
            "updatedAt": workflow_dto.updated_at
        }
    
    def _convert_workflow_from_ui_format(self, ui_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert workflow data from UI format to service format.
        
        Args:
            ui_data: Workflow data in UI format
            
        Returns:
            Workflow data in service format
        """
        return {
            "workflow_id": ui_data.get("id"),
            "name": ui_data.get("name"),
            "description": ui_data.get("description"),
            "version": ui_data.get("version", "1.0.0"),
            "enabled": ui_data.get("enabled", True),
            "steps": ui_data.get("steps", [])
        }
