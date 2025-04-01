"""
Workflow adapter interface.

This module defines the interface for workflow adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IWorkflowAdapter(ABC):
    """Interface for workflow adapters."""
    
    @abstractmethod
    def get_workflow_types(self) -> List[Dict[str, Any]]:
        """
        Get all available workflow types.
        
        Returns:
            List of workflow types with metadata
        """
        pass
    
    @abstractmethod
    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """
        Get all workflows.
        
        Returns:
            List of workflows in the UI-expected format
        """
        pass
    
    @abstractmethod
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow in the UI-expected format, or None if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            True if the workflow was deleted, False if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def validate_workflow(self, workflow_data: Dict[str, Any]) -> List[str]:
        """
        Validate a workflow.
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            List of validation errors, empty if valid
        """
        pass
