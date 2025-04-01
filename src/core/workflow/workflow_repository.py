"""
Workflow repository implementation.

This module provides an implementation of the workflow repository,
for storing and retrieving workflows.
"""
from typing import Dict, Any, List, Optional
import os
import json
import logging

from .service_interfaces import IWorkflowRepository, IWorkflowQuery, IWorkflowSerializer
from .interfaces import IWorkflow
from .service_exceptions import WorkflowNotFoundError, WorkflowRepositoryError
from .workflow_query import WorkflowQueryBuilder


class FileSystemWorkflowRepository(IWorkflowRepository):
    """
    Implementation of a workflow repository using the file system.
    
    This class provides an implementation of the IWorkflowRepository interface,
    storing workflows as JSON files in a directory.
    """
    
    def __init__(self, directory: str, serializer: IWorkflowSerializer):
        """
        Initialize a file system workflow repository.
        
        Args:
            directory: Directory to store workflows in
            serializer: Workflow serializer to use
        """
        self._directory = directory
        self._serializer = serializer
        self._logger = logging.getLogger(self.__class__.__name__)
        
        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
    
    def get_workflow(self, workflow_id: str) -> Optional[IWorkflow]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow or None if not found
            
        Raises:
            WorkflowRepositoryError: If there is an error retrieving the workflow
        """
        try:
            # Check if the workflow file exists
            file_path = self._get_workflow_file_path(workflow_id)
            if not os.path.exists(file_path):
                return None
            
            # Load the workflow from the file
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Deserialize the workflow
            return self._serializer.deserialize_workflow(data)
        except Exception as e:
            raise WorkflowRepositoryError(f"Error retrieving workflow '{workflow_id}'", e)
    
    def get_workflows(self, query: Optional[IWorkflowQuery] = None) -> List[IWorkflow]:
        """
        Get workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            List of workflows
            
        Raises:
            WorkflowRepositoryError: If there is an error retrieving the workflows
        """
        try:
            # Use the all query if none is provided
            if query is None:
                query = WorkflowQueryBuilder.all()
            
            # Get all workflow files
            workflows = []
            for file_name in os.listdir(self._directory):
                if file_name.endswith(".json"):
                    try:
                        # Load the workflow from the file
                        file_path = os.path.join(self._directory, file_name)
                        with open(file_path, "r") as f:
                            data = json.load(f)
                        
                        # Deserialize the workflow
                        workflow = self._serializer.deserialize_workflow(data)
                        
                        # Check if the workflow matches the query
                        if query.matches(workflow):
                            workflows.append(workflow)
                    except Exception as e:
                        self._logger.error(f"Error loading workflow from file '{file_name}': {str(e)}")
            
            return workflows
        except Exception as e:
            raise WorkflowRepositoryError("Error retrieving workflows", e)
    
    def save_workflow(self, workflow: IWorkflow) -> None:
        """
        Save a workflow.
        
        Args:
            workflow: Workflow to save
            
        Raises:
            WorkflowRepositoryError: If there is an error saving the workflow
        """
        try:
            # Serialize the workflow
            data = self._serializer.serialize_workflow(workflow)
            
            # Save the workflow to a file
            file_path = self._get_workflow_file_path(workflow.workflow_id)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise WorkflowRepositoryError(f"Error saving workflow '{workflow.workflow_id}'", e)
    
    def delete_workflow(self, workflow_id: str) -> None:
        """
        Delete a workflow.
        
        Args:
            workflow_id: ID of the workflow to delete
            
        Raises:
            WorkflowNotFoundError: If the workflow is not found
            WorkflowRepositoryError: If there is an error deleting the workflow
        """
        try:
            # Check if the workflow file exists
            file_path = self._get_workflow_file_path(workflow_id)
            if not os.path.exists(file_path):
                raise WorkflowNotFoundError(workflow_id)
            
            # Delete the workflow file
            os.remove(file_path)
        except WorkflowNotFoundError:
            raise
        except Exception as e:
            raise WorkflowRepositoryError(f"Error deleting workflow '{workflow_id}'", e)
    
    def count_workflows(self, query: Optional[IWorkflowQuery] = None) -> int:
        """
        Count workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            Number of workflows
            
        Raises:
            WorkflowRepositoryError: If there is an error counting the workflows
        """
        try:
            # Get the workflows matching the query
            workflows = self.get_workflows(query)
            
            # Return the count
            return len(workflows)
        except Exception as e:
            raise WorkflowRepositoryError("Error counting workflows", e)
    
    def _get_workflow_file_path(self, workflow_id: str) -> str:
        """
        Get the file path for a workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            File path for the workflow
        """
        return os.path.join(self._directory, f"{workflow_id}.json")


class InMemoryWorkflowRepository(IWorkflowRepository):
    """
    Implementation of a workflow repository using in-memory storage.
    
    This class provides an implementation of the IWorkflowRepository interface,
    storing workflows in memory.
    """
    
    def __init__(self):
        """Initialize an in-memory workflow repository."""
        self._workflows: Dict[str, IWorkflow] = {}
    
    def get_workflow(self, workflow_id: str) -> Optional[IWorkflow]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow or None if not found
        """
        return self._workflows.get(workflow_id)
    
    def get_workflows(self, query: Optional[IWorkflowQuery] = None) -> List[IWorkflow]:
        """
        Get workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            List of workflows
        """
        # Use the all query if none is provided
        if query is None:
            query = WorkflowQueryBuilder.all()
        
        # Filter the workflows by the query
        return [workflow for workflow in self._workflows.values() if query.matches(workflow)]
    
    def save_workflow(self, workflow: IWorkflow) -> None:
        """
        Save a workflow.
        
        Args:
            workflow: Workflow to save
        """
        self._workflows[workflow.workflow_id] = workflow
    
    def delete_workflow(self, workflow_id: str) -> None:
        """
        Delete a workflow.
        
        Args:
            workflow_id: ID of the workflow to delete
            
        Raises:
            WorkflowNotFoundError: If the workflow is not found
        """
        if workflow_id not in self._workflows:
            raise WorkflowNotFoundError(workflow_id)
        
        del self._workflows[workflow_id]
    
    def count_workflows(self, query: Optional[IWorkflowQuery] = None) -> int:
        """
        Count workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            Number of workflows
        """
        return len(self.get_workflows(query))
