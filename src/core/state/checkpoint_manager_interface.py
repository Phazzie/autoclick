"""Interface for checkpoint management"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple

from src.core.context.execution_context import ExecutionContext
from src.core.state.checkpoint_interface import CheckpointInterface


class CheckpointManagerInterface(ABC):
    """
    Interface for managing checkpoints
    
    This interface defines methods for creating, restoring, and managing
    checkpoints during workflow execution.
    """
    
    @abstractmethod
    def create_checkpoint(
        self, 
        workflow_id: str, 
        context: ExecutionContext, 
        data: Dict[str, Any],
        name: Optional[str] = None
    ) -> str:
        """
        Create a checkpoint
        
        Args:
            workflow_id: ID of the workflow
            context: Execution context to save
            data: Additional data to save with the checkpoint
            name: Optional name for the checkpoint
            
        Returns:
            ID of the created checkpoint
            
        Raises:
            IOError: If the checkpoint cannot be saved
        """
        pass
    
    @abstractmethod
    def restore_from_checkpoint(self, checkpoint_id: str) -> Tuple[ExecutionContext, Dict[str, Any]]:
        """
        Restore from a checkpoint
        
        Args:
            checkpoint_id: ID of the checkpoint
            
        Returns:
            Tuple of (restored context, checkpoint data)
            
        Raises:
            FileNotFoundError: If the checkpoint doesn't exist
            ValueError: If the checkpoint is invalid
        """
        pass
    
    @abstractmethod
    def get_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointInterface]:
        """
        Get a checkpoint by ID
        
        Args:
            checkpoint_id: ID of the checkpoint
            
        Returns:
            Checkpoint, or None if not found
        """
        pass
    
    @abstractmethod
    def get_checkpoints_for_workflow(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get all checkpoints for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            List of checkpoint data dictionaries
        """
        pass
    
    @abstractmethod
    def get_checkpoint_by_name(self, workflow_id: str, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a checkpoint by name
        
        Args:
            workflow_id: ID of the workflow
            name: Name of the checkpoint
            
        Returns:
            Checkpoint data dictionary, or None if not found
        """
        pass
    
    @abstractmethod
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete a checkpoint
        
        Args:
            checkpoint_id: ID of the checkpoint
            
        Returns:
            True if the checkpoint was deleted, False otherwise
        """
        pass
