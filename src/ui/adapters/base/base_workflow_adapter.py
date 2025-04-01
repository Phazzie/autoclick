"""
Base workflow adapter implementation.

This module provides a base implementation of the workflow adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.ui.adapters.interfaces.iworkflow_adapter import IWorkflowAdapter


class BaseWorkflowAdapter(IWorkflowAdapter):
    """Base implementation of workflow adapter."""
    
    def get_workflow_types(self) -> List[Dict[str, Any]]:
        """
        Get all available workflow types.
        
        Returns:
            List of workflow types with metadata
        """
        raise NotImplementedError("Subclasses must implement get_workflow_types")
    
    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """
        Get all workflows.
        
        Returns:
            List of workflows in the UI-expected format
        """
        raise NotImplementedError("Subclasses must implement get_all_workflows")
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow in the UI-expected format, or None if not found
        """
        raise NotImplementedError("Subclasses must implement get_workflow")
    
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
        raise NotImplementedError("Subclasses must implement create_workflow")
    
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
        raise NotImplementedError("Subclasses must implement update_workflow")
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            True if the workflow was deleted, False if not found
        """
        raise NotImplementedError("Subclasses must implement delete_workflow")
    
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
        raise NotImplementedError("Subclasses must implement execute_workflow")
    
    def validate_workflow(self, workflow_data: Dict[str, Any]) -> List[str]:
        """
        Validate a workflow.
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            List of validation errors, empty if valid
        """
        raise NotImplementedError("Subclasses must implement validate_workflow")
