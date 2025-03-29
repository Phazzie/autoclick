"""Checkpoint functionality for workflow execution"""
from typing import Dict, Any, Optional

from src.core.context.execution_context import ExecutionContext
from src.core.state.checkpoint_interface import CheckpointInterface


class Checkpoint(CheckpointInterface):
    """
    Represents a checkpoint in workflow execution
    
    A checkpoint captures the state of a workflow at a specific point in time,
    allowing for resuming execution from that point.
    """
    
    def __init__(
        self,
        checkpoint_id: str,
        workflow_id: str,
        timestamp: str,
        data: Dict[str, Any],
        context: ExecutionContext,
        name: Optional[str] = None
    ):
        """
        Initialize a checkpoint
        
        Args:
            checkpoint_id: Unique ID for the checkpoint
            workflow_id: ID of the workflow
            timestamp: ISO-formatted timestamp
            data: Additional data for the checkpoint
            context: Execution context at the checkpoint
            name: Optional name for the checkpoint
        """
        self._id = checkpoint_id
        self._workflow_id = workflow_id
        self._timestamp = timestamp
        self._name = name
        self._data = data
        self._context = context
    
    def get_id(self) -> str:
        """
        Get the ID of the checkpoint
        
        Returns:
            ID of the checkpoint
        """
        return self._id
    
    def get_workflow_id(self) -> str:
        """
        Get the ID of the workflow
        
        Returns:
            ID of the workflow
        """
        return self._workflow_id
    
    def get_timestamp(self) -> str:
        """
        Get the timestamp of the checkpoint
        
        Returns:
            Timestamp of the checkpoint
        """
        return self._timestamp
    
    def get_name(self) -> Optional[str]:
        """
        Get the name of the checkpoint
        
        Returns:
            Name of the checkpoint, or None if not named
        """
        return self._name
    
    def get_data(self) -> Dict[str, Any]:
        """
        Get the data associated with the checkpoint
        
        Returns:
            Dictionary with checkpoint data
        """
        return self._data
    
    def get_context(self) -> ExecutionContext:
        """
        Get the execution context at the checkpoint
        
        Returns:
            Execution context at the checkpoint
        """
        return self._context
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the checkpoint to a dictionary
        
        Returns:
            Dictionary representation of the checkpoint
        """
        return {
            "id": self._id,
            "workflow_id": self._workflow_id,
            "timestamp": self._timestamp,
            "name": self._name,
            "data": self._data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], context: ExecutionContext) -> 'Checkpoint':
        """
        Create a checkpoint from a dictionary
        
        Args:
            data: Dictionary representation of the checkpoint
            context: Execution context at the checkpoint
            
        Returns:
            Created checkpoint
            
        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        if "id" not in data:
            raise ValueError("Checkpoint data missing required field: id")
        
        if "workflow_id" not in data:
            raise ValueError("Checkpoint data missing required field: workflow_id")
        
        # Create the checkpoint
        return cls(
            checkpoint_id=data["id"],
            workflow_id=data["workflow_id"],
            timestamp=data.get("timestamp", ""),
            name=data.get("name"),
            data=data.get("data", {}),
            context=context
        )
