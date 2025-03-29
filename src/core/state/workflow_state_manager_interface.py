"""Interface for workflow state management"""
from typing import Dict, Any, List, Optional, Tuple
from abc import ABC, abstractmethod

from src.core.context.execution_context import ExecutionContext


class WorkflowStateManagerInterface(ABC):
    """
    Interface for managing workflow state
    
    This interface defines methods for saving, loading, and managing workflow state,
    including creating and restoring from checkpoints.
    """
    
    @abstractmethod
    def save_workflow_state(self, workflow_id: str, context: ExecutionContext) -> str:
        """
        Save the current state of a workflow
        
        Args:
            workflow_id: ID of the workflow
            context: Execution context to save
            
        Returns:
            Path to the saved state file
        """
        pass
    
    @abstractmethod
    def load_workflow_state(self, state_file: str) -> ExecutionContext:
        """
        Load a workflow state from a file
        
        Args:
            state_file: Path to the state file
            
        Returns:
            Loaded execution context
        """
        pass
    
    @abstractmethod
    def get_latest_state(self, workflow_id: str) -> Optional[str]:
        """
        Get the latest state file for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Path to the latest state file, or None if no state files exist
        """
        pass
    
    @abstractmethod
    def create_checkpoint(
        self, 
        workflow_id: str, 
        context: ExecutionContext, 
        data: Dict[str, Any],
        name: Optional[str] = None
    ) -> str:
        """
        Create a checkpoint for a workflow
        
        Args:
            workflow_id: ID of the workflow
            context: Execution context to save
            data: Additional data to save with the checkpoint
            name: Optional name for the checkpoint
            
        Returns:
            ID of the created checkpoint
        """
        pass
    
    @abstractmethod
    def restore_from_checkpoint(self, checkpoint_id: str) -> Tuple[ExecutionContext, Dict[str, Any]]:
        """
        Restore a workflow from a checkpoint
        
        Args:
            checkpoint_id: ID of the checkpoint
            
        Returns:
            Tuple of (restored context, checkpoint data)
        """
        pass
    
    @abstractmethod
    def get_checkpoints(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get all checkpoints for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            List of checkpoint data dictionaries
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
