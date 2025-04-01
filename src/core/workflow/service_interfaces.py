"""
Interfaces for workflow service components.

This module defines the interfaces for workflow service components,
following the Interface Segregation Principle to ensure clients only
depend on the methods they actually use.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Set, Iterator, TypeVar, Generic, Callable, Union

from .interfaces import IWorkflow, IWorkflowStep

# Type variables for generic interfaces
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class IWorkflowQuery(ABC):
    """Interface for workflow queries."""
    
    @abstractmethod
    def matches(self, workflow: IWorkflow) -> bool:
        """
        Check if a workflow matches this query.
        
        Args:
            workflow: Workflow to check
            
        Returns:
            True if the workflow matches, False otherwise
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dictionary representation of the query
        """
        pass
    
    @abstractmethod
    def __and__(self, other: 'IWorkflowQuery') -> 'IWorkflowQuery':
        """
        Combine this query with another using AND logic.
        
        Args:
            other: Another query
            
        Returns:
            A new query that matches workflows matching both queries
        """
        pass
    
    @abstractmethod
    def __or__(self, other: 'IWorkflowQuery') -> 'IWorkflowQuery':
        """
        Combine this query with another using OR logic.
        
        Args:
            other: Another query
            
        Returns:
            A new query that matches workflows matching either query
        """
        pass
    
    @abstractmethod
    def __invert__(self) -> 'IWorkflowQuery':
        """
        Negate this query using NOT logic.
        
        Returns:
            A new query that matches workflows not matching this query
        """
        pass


class IWorkflowDTO(ABC):
    """Interface for workflow data transfer objects."""
    
    @property
    @abstractmethod
    def workflow_id(self) -> str:
        """Get the workflow ID."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the workflow name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        """Get the workflow description."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Get the workflow version."""
        pass
    
    @property
    @abstractmethod
    def enabled(self) -> bool:
        """Check if the workflow is enabled."""
        pass
    
    @property
    @abstractmethod
    def step_count(self) -> int:
        """Get the number of steps in the workflow."""
        pass
    
    @property
    @abstractmethod
    def created_at(self) -> str:
        """Get the creation timestamp."""
        pass
    
    @property
    @abstractmethod
    def updated_at(self) -> str:
        """Get the last update timestamp."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DTO to a dictionary.
        
        Returns:
            Dictionary representation of the DTO
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_workflow(cls, workflow: IWorkflow) -> 'IWorkflowDTO':
        """
        Create a DTO from a workflow.
        
        Args:
            workflow: Workflow to create DTO from
            
        Returns:
            Workflow DTO
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IWorkflowDTO':
        """
        Create a DTO from a dictionary.
        
        Args:
            data: Dictionary to create DTO from
            
        Returns:
            Workflow DTO
        """
        pass


class IWorkflowStepDTO(ABC):
    """Interface for workflow step data transfer objects."""
    
    @property
    @abstractmethod
    def step_id(self) -> str:
        """Get the step ID."""
        pass
    
    @property
    @abstractmethod
    def step_type(self) -> str:
        """Get the step type."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the step name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        """Get the step description."""
        pass
    
    @property
    @abstractmethod
    def enabled(self) -> bool:
        """Check if the step is enabled."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DTO to a dictionary.
        
        Returns:
            Dictionary representation of the DTO
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_step(cls, step: IWorkflowStep) -> 'IWorkflowStepDTO':
        """
        Create a DTO from a workflow step.
        
        Args:
            step: Workflow step to create DTO from
            
        Returns:
            Workflow step DTO
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IWorkflowStepDTO':
        """
        Create a DTO from a dictionary.
        
        Args:
            data: Dictionary to create DTO from
            
        Returns:
            Workflow step DTO
        """
        pass


class IWorkflowSerializer(ABC):
    """Interface for workflow serializers."""
    
    @abstractmethod
    def serialize_workflow(self, workflow: IWorkflow) -> Dict[str, Any]:
        """
        Serialize a workflow to a dictionary.
        
        Args:
            workflow: Workflow to serialize
            
        Returns:
            Serialized workflow
        """
        pass
    
    @abstractmethod
    def deserialize_workflow(self, data: Dict[str, Any]) -> IWorkflow:
        """
        Deserialize a workflow from a dictionary.
        
        Args:
            data: Serialized workflow
            
        Returns:
            Deserialized workflow
        """
        pass
    
    @abstractmethod
    def serialize_step(self, step: IWorkflowStep) -> Dict[str, Any]:
        """
        Serialize a workflow step to a dictionary.
        
        Args:
            step: Workflow step to serialize
            
        Returns:
            Serialized workflow step
        """
        pass
    
    @abstractmethod
    def deserialize_step(self, data: Dict[str, Any]) -> IWorkflowStep:
        """
        Deserialize a workflow step from a dictionary.
        
        Args:
            data: Serialized workflow step
            
        Returns:
            Deserialized workflow step
        """
        pass


class IWorkflowRepository(ABC):
    """Interface for workflow repositories."""
    
    @abstractmethod
    def get_workflow(self, workflow_id: str) -> Optional[IWorkflow]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow or None if not found
        """
        pass
    
    @abstractmethod
    def get_workflows(self, query: Optional[IWorkflowQuery] = None) -> List[IWorkflow]:
        """
        Get workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            List of workflows
        """
        pass
    
    @abstractmethod
    def save_workflow(self, workflow: IWorkflow) -> None:
        """
        Save a workflow.
        
        Args:
            workflow: Workflow to save
        """
        pass
    
    @abstractmethod
    def delete_workflow(self, workflow_id: str) -> None:
        """
        Delete a workflow.
        
        Args:
            workflow_id: ID of the workflow to delete
        """
        pass
    
    @abstractmethod
    def count_workflows(self, query: Optional[IWorkflowQuery] = None) -> int:
        """
        Count workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            Number of workflows
        """
        pass


class IWorkflowService(ABC):
    """Interface for workflow services."""
    
    @abstractmethod
    def get_workflow(self, workflow_id: str) -> Optional[IWorkflowDTO]:
        """
        Get a workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow DTO or None if not found
        """
        pass
    
    @abstractmethod
    def get_workflows(self, query: Optional[IWorkflowQuery] = None) -> List[IWorkflowDTO]:
        """
        Get workflows matching a query.
        
        Args:
            query: Optional query to filter workflows
            
        Returns:
            List of workflow DTOs
        """
        pass
    
    @abstractmethod
    def create_workflow(self, workflow_data: Dict[str, Any]) -> IWorkflowDTO:
        """
        Create a new workflow.
        
        Args:
            workflow_data: Workflow data
            
        Returns:
            Created workflow DTO
        """
        pass
    
    @abstractmethod
    def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Optional[IWorkflowDTO]:
        """
        Update a workflow.
        
        Args:
            workflow_id: Workflow ID
            workflow_data: Workflow data
            
        Returns:
            Updated workflow DTO or None if not found
        """
        pass
    
    @abstractmethod
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.
        
        Args:
            workflow_id: ID of the workflow to delete
            
        Returns:
            True if the workflow was deleted, False if not found
        """
        pass
    
    @abstractmethod
    def execute_workflow(self, workflow_id: str, context_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a workflow.
        
        Args:
            workflow_id: Workflow ID
            context_data: Optional context data
            
        Returns:
            Result of the workflow execution
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
