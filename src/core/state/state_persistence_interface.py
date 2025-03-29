"""Interface for state persistence operations"""
from abc import ABC, abstractmethod
from typing import Optional, List

from src.core.context.execution_context import ExecutionContext


class StatePersistenceInterface(ABC):
    """
    Interface for persisting and loading execution state
    
    This interface defines methods for saving execution context to files
    and loading it back, enabling workflow pause and resume functionality.
    """
    
    @abstractmethod
    def save_state(self, workflow_id: str, context: ExecutionContext) -> str:
        """
        Save execution context to a file
        
        Args:
            workflow_id: ID of the workflow
            context: Execution context to save
            
        Returns:
            Path to the saved state file
            
        Raises:
            IOError: If the state cannot be saved
        """
        pass
    
    @abstractmethod
    def load_state(self, file_path: str) -> ExecutionContext:
        """
        Load execution context from a file
        
        Args:
            file_path: Path to the state file
            
        Returns:
            Loaded execution context
            
        Raises:
            FileNotFoundError: If the state file doesn't exist
            ValueError: If the state file is invalid
        """
        pass
    
    @abstractmethod
    def get_state_files(self, workflow_id: str) -> List[str]:
        """
        Get all state files for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            List of state file paths, sorted by timestamp (newest first)
        """
        pass
    
    @abstractmethod
    def get_latest_state_file(self, workflow_id: str) -> Optional[str]:
        """
        Get the latest state file for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Path to the latest state file, or None if no state files exist
        """
        pass
    
    @abstractmethod
    def cleanup_old_states(self, workflow_id: str, max_states: int = 10) -> int:
        """
        Clean up old state files for a workflow
        
        Args:
            workflow_id: ID of the workflow
            max_states: Maximum number of state files to keep
            
        Returns:
            Number of state files removed
        """
        pass
