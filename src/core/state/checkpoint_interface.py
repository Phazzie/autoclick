"""Interface for checkpoint operations"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from src.core.context.execution_context import ExecutionContext


class CheckpointInterface(ABC):
    """
    Interface for checkpoint operations
    
    This interface defines methods for creating and managing checkpoints
    during workflow execution.
    """
    
    @abstractmethod
    def get_id(self) -> str:
        """
        Get the ID of the checkpoint
        
        Returns:
            ID of the checkpoint
        """
        pass
    
    @abstractmethod
    def get_workflow_id(self) -> str:
        """
        Get the ID of the workflow
        
        Returns:
            ID of the workflow
        """
        pass
    
    @abstractmethod
    def get_timestamp(self) -> str:
        """
        Get the timestamp of the checkpoint
        
        Returns:
            Timestamp of the checkpoint
        """
        pass
    
    @abstractmethod
    def get_name(self) -> Optional[str]:
        """
        Get the name of the checkpoint
        
        Returns:
            Name of the checkpoint, or None if not named
        """
        pass
    
    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        """
        Get the data associated with the checkpoint
        
        Returns:
            Dictionary with checkpoint data
        """
        pass
    
    @abstractmethod
    def get_context(self) -> ExecutionContext:
        """
        Get the execution context at the checkpoint
        
        Returns:
            Execution context at the checkpoint
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the checkpoint to a dictionary
        
        Returns:
            Dictionary representation of the checkpoint
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any], context: ExecutionContext) -> 'CheckpointInterface':
        """
        Create a checkpoint from a dictionary
        
        Args:
            data: Dictionary representation of the checkpoint
            context: Execution context at the checkpoint
            
        Returns:
            Created checkpoint
        """
        pass
