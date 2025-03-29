"""Workflow state management functionality"""
import logging
from typing import Dict, Any, List, Optional, Tuple

from src.core.context.execution_context import ExecutionContext
from src.core.state.workflow_state_manager_interface import WorkflowStateManagerInterface
from src.core.state.state_persistence_interface import StatePersistenceInterface
from src.core.state.checkpoint_manager_interface import CheckpointManagerInterface


class WorkflowStateManager(WorkflowStateManagerInterface):
    """
    Manages workflow state
    
    This class coordinates between state persistence and checkpoint management
    to provide a unified interface for workflow state operations.
    """
    
    def __init__(
        self,
        state_persistence: StatePersistenceInterface,
        checkpoint_manager: CheckpointManagerInterface
    ):
        """
        Initialize the workflow state manager
        
        Args:
            state_persistence: State persistence implementation
            checkpoint_manager: Checkpoint manager implementation
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self._state_persistence = state_persistence
        self._checkpoint_manager = checkpoint_manager
    
    def save_workflow_state(self, workflow_id: str, context: ExecutionContext) -> str:
        """
        Save the current state of a workflow
        
        Args:
            workflow_id: ID of the workflow
            context: Execution context to save
            
        Returns:
            Path to the saved state file
            
        Raises:
            IOError: If the state cannot be saved
        """
        try:
            return self._state_persistence.save_state(workflow_id, context)
        except Exception as e:
            self.logger.error(f"Error saving workflow state: {str(e)}")
            raise IOError(f"Failed to save workflow state: {str(e)}")
    
    def load_workflow_state(self, state_file: str) -> ExecutionContext:
        """
        Load a workflow state from a file
        
        Args:
            state_file: Path to the state file
            
        Returns:
            Loaded execution context
            
        Raises:
            FileNotFoundError: If the state file doesn't exist
            ValueError: If the state file is invalid
        """
        try:
            return self._state_persistence.load_state(state_file)
        except Exception as e:
            self.logger.error(f"Error loading workflow state: {str(e)}")
            raise
    
    def get_latest_state(self, workflow_id: str) -> Optional[str]:
        """
        Get the latest state file for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Path to the latest state file, or None if no state files exist
        """
        return self._state_persistence.get_latest_state_file(workflow_id)
    
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
            
        Raises:
            IOError: If the checkpoint cannot be created
        """
        try:
            return self._checkpoint_manager.create_checkpoint(
                workflow_id, context, data, name
            )
        except Exception as e:
            self.logger.error(f"Error creating checkpoint: {str(e)}")
            raise IOError(f"Failed to create checkpoint: {str(e)}")
    
    def restore_from_checkpoint(self, checkpoint_id: str) -> Tuple[ExecutionContext, Dict[str, Any]]:
        """
        Restore a workflow from a checkpoint
        
        Args:
            checkpoint_id: ID of the checkpoint
            
        Returns:
            Tuple of (restored context, checkpoint data)
            
        Raises:
            FileNotFoundError: If the checkpoint doesn't exist
            ValueError: If the checkpoint is invalid
        """
        try:
            return self._checkpoint_manager.restore_from_checkpoint(checkpoint_id)
        except Exception as e:
            self.logger.error(f"Error restoring from checkpoint: {str(e)}")
            raise
    
    def get_checkpoints(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Get all checkpoints for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            List of checkpoint data dictionaries
        """
        try:
            return self._checkpoint_manager.get_checkpoints_for_workflow(workflow_id)
        except Exception as e:
            self.logger.error(f"Error getting checkpoints: {str(e)}")
            return []
    
    def get_checkpoint_by_name(self, workflow_id: str, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a checkpoint by name
        
        Args:
            workflow_id: ID of the workflow
            name: Name of the checkpoint
            
        Returns:
            Checkpoint data dictionary, or None if not found
        """
        try:
            return self._checkpoint_manager.get_checkpoint_by_name(workflow_id, name)
        except Exception as e:
            self.logger.error(f"Error getting checkpoint by name: {str(e)}")
            return None
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete a checkpoint
        
        Args:
            checkpoint_id: ID of the checkpoint
            
        Returns:
            True if the checkpoint was deleted, False otherwise
        """
        try:
            return self._checkpoint_manager.delete_checkpoint(checkpoint_id)
        except Exception as e:
            self.logger.error(f"Error deleting checkpoint: {str(e)}")
            return False
    
    def cleanup_old_states(self, workflow_id: str, max_states: int = 10) -> int:
        """
        Clean up old state files for a workflow
        
        Args:
            workflow_id: ID of the workflow
            max_states: Maximum number of state files to keep
            
        Returns:
            Number of state files removed
        """
        try:
            return self._state_persistence.cleanup_old_states(workflow_id, max_states)
        except Exception as e:
            self.logger.error(f"Error cleaning up old states: {str(e)}")
            return 0
