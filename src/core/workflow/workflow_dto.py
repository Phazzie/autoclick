"""
Workflow DTO implementation.

This module provides implementations of the workflow data transfer objects,
for transferring workflow data between layers.
"""
from typing import Dict, Any, List, Optional
import datetime
import uuid

from .service_interfaces import IWorkflowDTO, IWorkflowStepDTO
from .interfaces import IWorkflow, IWorkflowStep


class WorkflowDTO(IWorkflowDTO):
    """
    Implementation of a workflow data transfer object.
    
    This class provides a data transfer object for workflows,
    with serialization and deserialization.
    """
    
    def __init__(self, workflow_id: str, name: str, description: Optional[str] = None,
                version: str = "1.0.0", enabled: bool = True, step_count: int = 0,
                created_at: Optional[str] = None, updated_at: Optional[str] = None,
                metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a workflow DTO.
        
        Args:
            workflow_id: Workflow ID
            name: Workflow name
            description: Optional workflow description
            version: Workflow version
            enabled: Whether the workflow is enabled
            step_count: Number of steps in the workflow
            created_at: Optional creation timestamp
            updated_at: Optional last update timestamp
            metadata: Optional metadata
        """
        self._workflow_id = workflow_id
        self._name = name
        self._description = description
        self._version = version
        self._enabled = enabled
        self._step_count = step_count
        self._created_at = created_at or datetime.datetime.now().isoformat()
        self._updated_at = updated_at or self._created_at
        self._metadata = metadata or {}
    
    @property
    def workflow_id(self) -> str:
        """Get the workflow ID."""
        return self._workflow_id
    
    @property
    def name(self) -> str:
        """Get the workflow name."""
        return self._name
    
    @property
    def description(self) -> Optional[str]:
        """Get the workflow description."""
        return self._description
    
    @property
    def version(self) -> str:
        """Get the workflow version."""
        return self._version
    
    @property
    def enabled(self) -> bool:
        """Check if the workflow is enabled."""
        return self._enabled
    
    @property
    def step_count(self) -> int:
        """Get the number of steps in the workflow."""
        return self._step_count
    
    @property
    def created_at(self) -> str:
        """Get the creation timestamp."""
        return self._created_at
    
    @property
    def updated_at(self) -> str:
        """Get the last update timestamp."""
        return self._updated_at
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Get the metadata."""
        return self._metadata.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DTO to a dictionary.
        
        Returns:
            Dictionary representation of the DTO
        """
        return {
            "workflow_id": self._workflow_id,
            "name": self._name,
            "description": self._description,
            "version": self._version,
            "enabled": self._enabled,
            "step_count": self._step_count,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
            "metadata": self._metadata.copy()
        }
    
    @classmethod
    def from_workflow(cls, workflow: IWorkflow) -> 'WorkflowDTO':
        """
        Create a DTO from a workflow.
        
        Args:
            workflow: Workflow to create DTO from
            
        Returns:
            Workflow DTO
        """
        return cls(
            workflow_id=workflow.workflow_id,
            name=workflow.name,
            description=workflow.description,
            version=workflow.version,
            enabled=workflow.enabled,
            step_count=len(workflow.get_steps()),
            metadata=getattr(workflow, "metadata", {})
        )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowDTO':
        """
        Create a DTO from a dictionary.
        
        Args:
            data: Dictionary to create DTO from
            
        Returns:
            Workflow DTO
        """
        return cls(
            workflow_id=data.get("workflow_id", str(uuid.uuid4())),
            name=data.get("name", "Unnamed Workflow"),
            description=data.get("description"),
            version=data.get("version", "1.0.0"),
            enabled=data.get("enabled", True),
            step_count=data.get("step_count", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            metadata=data.get("metadata", {})
        )


class WorkflowStepDTO(IWorkflowStepDTO):
    """
    Implementation of a workflow step data transfer object.
    
    This class provides a data transfer object for workflow steps,
    with serialization and deserialization.
    """
    
    def __init__(self, step_id: str, step_type: str, name: str,
                description: Optional[str] = None, enabled: bool = True,
                config: Optional[Dict[str, Any]] = None,
                metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a workflow step DTO.
        
        Args:
            step_id: Step ID
            step_type: Step type
            name: Step name
            description: Optional step description
            enabled: Whether the step is enabled
            config: Optional step configuration
            metadata: Optional metadata
        """
        self._step_id = step_id
        self._step_type = step_type
        self._name = name
        self._description = description
        self._enabled = enabled
        self._config = config or {}
        self._metadata = metadata or {}
    
    @property
    def step_id(self) -> str:
        """Get the step ID."""
        return self._step_id
    
    @property
    def step_type(self) -> str:
        """Get the step type."""
        return self._step_type
    
    @property
    def name(self) -> str:
        """Get the step name."""
        return self._name
    
    @property
    def description(self) -> Optional[str]:
        """Get the step description."""
        return self._description
    
    @property
    def enabled(self) -> bool:
        """Check if the step is enabled."""
        return self._enabled
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the step configuration."""
        return self._config.copy()
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Get the metadata."""
        return self._metadata.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DTO to a dictionary.
        
        Returns:
            Dictionary representation of the DTO
        """
        return {
            "step_id": self._step_id,
            "step_type": self._step_type,
            "name": self._name,
            "description": self._description,
            "enabled": self._enabled,
            "config": self._config.copy(),
            "metadata": self._metadata.copy()
        }
    
    @classmethod
    def from_step(cls, step: IWorkflowStep) -> 'WorkflowStepDTO':
        """
        Create a DTO from a workflow step.
        
        Args:
            step: Workflow step to create DTO from
            
        Returns:
            Workflow step DTO
        """
        return cls(
            step_id=step.step_id,
            step_type=step.step_type,
            name=step.name,
            description=step.description,
            enabled=step.enabled,
            config=getattr(step, "config", {}),
            metadata=getattr(step, "metadata", {})
        )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowStepDTO':
        """
        Create a DTO from a dictionary.
        
        Args:
            data: Dictionary to create DTO from
            
        Returns:
            Workflow step DTO
        """
        return cls(
            step_id=data.get("step_id", str(uuid.uuid4())),
            step_type=data.get("step_type", "unknown"),
            name=data.get("name", "Unnamed Step"),
            description=data.get("description"),
            enabled=data.get("enabled", True),
            config=data.get("config", {}),
            metadata=data.get("metadata", {})
        )
