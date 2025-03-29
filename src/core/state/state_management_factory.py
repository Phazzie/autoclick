"""Factory for creating state management components"""
from typing import Optional

from src.core.state.state_persistence_interface import StatePersistenceInterface
from src.core.state.state_persistence import StatePersistence
from src.core.state.checkpoint_manager_interface import CheckpointManagerInterface
from src.core.state.checkpoint_manager import CheckpointManager
from src.core.state.workflow_state_manager_interface import WorkflowStateManagerInterface
from src.core.state.workflow_state_manager import WorkflowStateManager


class StateManagementFactory:
    """
    Factory for creating state management components
    
    This class provides methods to create instances of state persistence,
    checkpoint manager, and workflow state manager with proper dependencies.
    """
    
    @staticmethod
    def create_state_persistence(state_dir: str = "states") -> StatePersistenceInterface:
        """
        Create a state persistence instance
        
        Args:
            state_dir: Directory to store state files
            
        Returns:
            State persistence instance
        """
        return StatePersistence(state_dir)
    
    @staticmethod
    def create_checkpoint_manager(checkpoint_dir: str = "checkpoints") -> CheckpointManagerInterface:
        """
        Create a checkpoint manager instance
        
        Args:
            checkpoint_dir: Directory to store checkpoint files
            
        Returns:
            Checkpoint manager instance
        """
        return CheckpointManager(checkpoint_dir)
    
    @staticmethod
    def create_workflow_state_manager(
        state_dir: str = "states",
        checkpoint_dir: str = "checkpoints",
        state_persistence: Optional[StatePersistenceInterface] = None,
        checkpoint_manager: Optional[CheckpointManagerInterface] = None
    ) -> WorkflowStateManagerInterface:
        """
        Create a workflow state manager instance
        
        Args:
            state_dir: Directory to store state files
            checkpoint_dir: Directory to store checkpoint files
            state_persistence: Optional state persistence instance
            checkpoint_manager: Optional checkpoint manager instance
            
        Returns:
            Workflow state manager instance
        """
        # Create dependencies if not provided
        if state_persistence is None:
            state_persistence = StateManagementFactory.create_state_persistence(state_dir)
        
        if checkpoint_manager is None:
            checkpoint_manager = StateManagementFactory.create_checkpoint_manager(checkpoint_dir)
        
        # Create and return the workflow state manager
        return WorkflowStateManager(
            state_persistence=state_persistence,
            checkpoint_manager=checkpoint_manager
        )
