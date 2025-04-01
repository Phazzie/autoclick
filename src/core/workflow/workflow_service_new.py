"""
Workflow service implementation.

This module provides an implementation of the workflow service,
for managing and executing workflows.
"""
from typing import Dict, Any, List, Optional
import uuid
import datetime
import logging

from src.core.context.interfaces import IExecutionContext
from src.core.context.context_factory import ContextFactory

from .service_interfaces import IWorkflowService, IWorkflowQuery, IWorkflowDTO, IWorkflowRepository
from .interfaces import IWorkflow, IWorkflowEngine, IWorkflowValidator, IWorkflowExecutor
from .service_exceptions import (
    WorkflowNotFoundError, WorkflowValidationError, WorkflowExecutionError,
    WorkflowRepositoryError
)
from .workflow_dto import WorkflowDTO


class WorkflowService(IWorkflowService):
    """
    Implementation of a workflow service.
    
    This class provides an implementation of the IWorkflowService interface,
    for managing and executing workflows.
    """
    
    def __init__(self, repository: IWorkflowRepository, engine: IWorkflowEngine,
                validator: IWorkflowValidator, executor: IWorkflowExecutor,
                context_factory: Optional[ContextFactory] = None):
        """
        Initialize a workflow service.
        
        Args:
            repository: Workflow repository to use
            engine: Workflow engine to use
            validator: Workflow validator to use
            executor: Workflow executor to use
            context_factory: Optional context factory to use
        """
        self._repository = repository
        self._engine = engine
        self._validator = validator
        self._executor = executor
        self._context_factory = context_factory or ContextFactory()
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def get_workflow(self, workflow_id: str) -> Optional[IWorkflowDTO]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow DTO or None if not found
            
        Raises:
            WorkflowRepositoryError: If there is an error retrieving the workflow
        """
        try:
            # Get the workflow from the repository
            workflow = self._repository.get_workflow(workflow_id)
            
            # Return None if the workflow is not found
            if workflow is None:
                return None
            
            # Convert the workflow to a DTO
            return WorkflowDTO.from_workflow(workflow)
        except WorkflowRepositoryError:
            raise
        except Exception as e:
            raise WorkflowRepositoryError(f"Error retrieving workflow '{workflow_id}'", e)
    
    def get_workflows(self, query: Optional[IWorkflowQuery] = None) -> List[IWorkflowDTO]:
        """
        Get workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            List of workflow DTOs
            
        Raises:
            WorkflowRepositoryError: If there is an error retrieving the workflows
        """
        try:
            # Get the workflows from the repository
            workflows = self._repository.get_workflows(query)
            
            # Convert the workflows to DTOs
            return [WorkflowDTO.from_workflow(workflow) for workflow in workflows]
        except WorkflowRepositoryError:
            raise
        except Exception as e:
            raise WorkflowRepositoryError("Error retrieving workflows", e)
    
    def create_workflow(self, workflow_data: Dict[str, Any]) -> IWorkflowDTO:
        """
        Create a new workflow.
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            Created workflow DTO
            
        Raises:
            WorkflowValidationError: If the workflow data is invalid
            WorkflowRepositoryError: If there is an error saving the workflow
        """
        try:
            # Validate the workflow data
            errors = self.validate_workflow(workflow_data)
            if errors:
                raise WorkflowValidationError(
                    workflow_data.get("workflow_id", "unknown"),
                    errors
                )
            
            # Generate a workflow ID if not provided
            if "workflow_id" not in workflow_data:
                workflow_data["workflow_id"] = str(uuid.uuid4())
            
            # Add timestamps if not provided
            now = datetime.datetime.now().isoformat()
            if "created_at" not in workflow_data:
                workflow_data["created_at"] = now
            if "updated_at" not in workflow_data:
                workflow_data["updated_at"] = now
            
            # Create the workflow
            workflow = self._engine.create_workflow(workflow_data)
            
            # Add steps if provided
            for step_data in workflow_data.get("steps", []):
                step = self._engine.create_step(step_data)
                workflow.add_step(step)
            
            # Save the workflow
            self._repository.save_workflow(workflow)
            
            # Return the workflow DTO
            return WorkflowDTO.from_workflow(workflow)
        except WorkflowValidationError:
            raise
        except WorkflowRepositoryError:
            raise
        except Exception as e:
            raise WorkflowRepositoryError(f"Error creating workflow", e)
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Optional[IWorkflowDTO]:
        """
        Update a workflow.
        
        Args:
            workflow_id: Workflow ID
            workflow_data: Workflow data
            
        Returns:
            Updated workflow DTO or None if not found
            
        Raises:
            WorkflowValidationError: If the workflow data is invalid
            WorkflowRepositoryError: If there is an error saving the workflow
        """
        try:
            # Get the existing workflow
            workflow = self._repository.get_workflow(workflow_id)
            if workflow is None:
                return None
            
            # Validate the workflow data
            errors = self.validate_workflow(workflow_data)
            if errors:
                raise WorkflowValidationError(workflow_id, errors)
            
            # Update the workflow ID
            workflow_data["workflow_id"] = workflow_id
            
            # Update the timestamps
            workflow_data["created_at"] = getattr(workflow, "created_at", datetime.datetime.now().isoformat())
            workflow_data["updated_at"] = datetime.datetime.now().isoformat()
            
            # Create a new workflow
            updated_workflow = self._engine.create_workflow(workflow_data)
            
            # Add steps if provided
            for step_data in workflow_data.get("steps", []):
                step = self._engine.create_step(step_data)
                updated_workflow.add_step(step)
            
            # Save the workflow
            self._repository.save_workflow(updated_workflow)
            
            # Return the workflow DTO
            return WorkflowDTO.from_workflow(updated_workflow)
        except WorkflowValidationError:
            raise
        except WorkflowRepositoryError:
            raise
        except Exception as e:
            raise WorkflowRepositoryError(f"Error updating workflow '{workflow_id}'", e)
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.
        
        Args:
            workflow_id: ID of the workflow to delete
            
        Returns:
            True if the workflow was deleted, False if not found
            
        Raises:
            WorkflowRepositoryError: If there is an error deleting the workflow
        """
        try:
            # Check if the workflow exists
            workflow = self._repository.get_workflow(workflow_id)
            if workflow is None:
                return False
            
            # Delete the workflow
            self._repository.delete_workflow(workflow_id)
            
            return True
        except WorkflowNotFoundError:
            return False
        except WorkflowRepositoryError:
            raise
        except Exception as e:
            raise WorkflowRepositoryError(f"Error deleting workflow '{workflow_id}'", e)
    
    def execute_workflow(self, workflow_id: str, context_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a workflow.
        
        Args:
            workflow_id: Workflow ID
            context_data: Optional context data
            
        Returns:
            Result of the workflow execution
            
        Raises:
            WorkflowNotFoundError: If the workflow is not found
            WorkflowExecutionError: If there is an error executing the workflow
        """
        try:
            # Get the workflow
            workflow = self._repository.get_workflow(workflow_id)
            if workflow is None:
                raise WorkflowNotFoundError(workflow_id)
            
            # Create a context
            context = self._context_factory.create_context(
                initial_variables=context_data or {}
            )
            
            # Execute the workflow
            return self._executor.execute_workflow(workflow, context)
        except WorkflowNotFoundError:
            raise
        except Exception as e:
            raise WorkflowExecutionError(workflow_id, str(e), e)
    
    def validate_workflow(self, workflow_data: Dict[str, Any]) -> List[str]:
        """
        Validate a workflow.
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            List of validation errors, empty if valid
        """
        try:
            # Create a temporary workflow
            workflow = self._engine.create_workflow(workflow_data)
            
            # Add steps if provided
            for step_data in workflow_data.get("steps", []):
                step = self._engine.create_step(step_data)
                workflow.add_step(step)
            
            # Validate the workflow
            return self._validator.validate_workflow(workflow)
        except Exception as e:
            return [f"Error validating workflow: {str(e)}"]
