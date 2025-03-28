"""Checkpoint management for workflow execution"""
import os
import json
import logging
import threading
import time
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import uuid

from src.core.context.execution_context import ExecutionContext
from src.core.workflow.workflow_serializer import WorkflowSerializer


class CheckpointManager:
    """
    Manager for creating and restoring workflow checkpoints
    
    This class provides functionality to:
    1. Create checkpoints of workflow state at regular intervals
    2. Restore workflow execution from a checkpoint
    3. Manage checkpoint files and cleanup
    """
    
    def __init__(
        self,
        checkpoint_dir: str = "checkpoints",
        max_checkpoints: int = 10,
        auto_checkpoint_interval: int = 60  # seconds
    ) -> None:
        """
        Initialize the checkpoint manager
        
        Args:
            checkpoint_dir: Directory to store checkpoint files
            max_checkpoints: Maximum number of checkpoints to keep per workflow
            auto_checkpoint_interval: Interval in seconds for automatic checkpoints
        """
        self.checkpoint_dir = checkpoint_dir
        self.max_checkpoints = max_checkpoints
        self.auto_checkpoint_interval = auto_checkpoint_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        self.serializer = WorkflowSerializer()
        
        # Create checkpoint directory if it doesn't exist
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # Dictionary to track checkpoint threads
        self._checkpoint_threads: Dict[str, threading.Thread] = {}
        self._stop_events: Dict[str, threading.Event] = {}
        
        # Lock for thread-safe operations
        self._lock = threading.Lock()

    def create_checkpoint(
        self,
        workflow_id: str,
        actions: List[Any],
        context: ExecutionContext,
        current_index: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a checkpoint of the current workflow state
        
        Args:
            workflow_id: ID of the workflow
            actions: List of actions in the workflow
            context: Current execution context
            current_index: Index of the current action
            metadata: Optional metadata to include in the checkpoint
            
        Returns:
            ID of the created checkpoint
        """
        self.logger.info(f"Creating checkpoint for workflow {workflow_id}")
        
        # Generate checkpoint ID
        checkpoint_id = str(uuid.uuid4())
        
        # Create checkpoint directory for this workflow if it doesn't exist
        workflow_checkpoint_dir = os.path.join(self.checkpoint_dir, workflow_id)
        os.makedirs(workflow_checkpoint_dir, exist_ok=True)
        
        # Create checkpoint metadata
        checkpoint_metadata = {
            "checkpoint_id": checkpoint_id,
            "workflow_id": workflow_id,
            "created_at": datetime.now().isoformat(),
            "current_index": current_index
        }
        
        # Add user metadata if provided
        if metadata:
            checkpoint_metadata.update(metadata)
        
        # Create checkpoint file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_file = os.path.join(
            workflow_checkpoint_dir,
            f"checkpoint_{timestamp}_{checkpoint_id}.json"
        )
        
        # Save checkpoint
        self.serializer.save_workflow_to_file(
            checkpoint_file,
            actions,
            context,
            checkpoint_metadata
        )
        
        self.logger.debug(f"Checkpoint {checkpoint_id} created at {checkpoint_file}")
        
        # Clean up old checkpoints
        self._cleanup_old_checkpoints(workflow_id)
        
        return checkpoint_id
    
    def restore_checkpoint(self, checkpoint_path: str) -> Dict[str, Any]:
        """
        Restore a workflow from a checkpoint
        
        Args:
            checkpoint_path: Path to the checkpoint file
            
        Returns:
            Dictionary containing the restored workflow state:
            {
                "actions": List of actions,
                "context": Execution context,
                "metadata": Checkpoint metadata,
                "current_index": Index of the current action
            }
            
        Raises:
            IOError: If the checkpoint file cannot be read
            ValueError: If the checkpoint is invalid
        """
        self.logger.info(f"Restoring checkpoint from {checkpoint_path}")
        
        # Load checkpoint
        checkpoint_data = self.serializer.load_workflow_from_file(checkpoint_path)
        
        # Extract checkpoint metadata
        metadata = checkpoint_data.get("metadata", {})
        current_index = metadata.get("current_index", 0)
        
        # Return restored workflow state
        return {
            "actions": checkpoint_data["actions"],
            "context": checkpoint_data["context"],
            "metadata": metadata,
            "current_index": current_index
        }
    
    def list_checkpoints(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        List all checkpoints for a workflow
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            List of checkpoint metadata dictionaries
        """
        self.logger.debug(f"Listing checkpoints for workflow {workflow_id}")
        
        # Get checkpoint directory for this workflow
        workflow_checkpoint_dir = os.path.join(self.checkpoint_dir, workflow_id)
        
        # Check if directory exists
        if not os.path.exists(workflow_checkpoint_dir):
            return []
        
        # Get all checkpoint files
        checkpoint_files = [
            os.path.join(workflow_checkpoint_dir, f)
            for f in os.listdir(workflow_checkpoint_dir)
            if f.startswith("checkpoint_") and f.endswith(".json")
        ]
        
        # Sort by modification time (newest first)
        checkpoint_files.sort(
            key=lambda f: os.path.getmtime(f),
            reverse=True
        )
        
        # Extract metadata from each checkpoint
        checkpoints = []
        for checkpoint_file in checkpoint_files:
            try:
                with open(checkpoint_file, 'r') as f:
                    data = json.load(f)
                    metadata = data.get("metadata", {})
                    metadata["file_path"] = checkpoint_file
                    metadata["file_size"] = os.path.getsize(checkpoint_file)
                    metadata["modified_at"] = datetime.fromtimestamp(
                        os.path.getmtime(checkpoint_file)
                    ).isoformat()
                    checkpoints.append(metadata)
            except Exception as e:
                self.logger.warning(
                    f"Error reading checkpoint file {checkpoint_file}: {str(e)}"
                )
        
        return checkpoints
    
    def delete_checkpoint(self, checkpoint_path: str) -> bool:
        """
        Delete a checkpoint file
        
        Args:
            checkpoint_path: Path to the checkpoint file
            
        Returns:
            True if the checkpoint was deleted, False otherwise
        """
        self.logger.info(f"Deleting checkpoint {checkpoint_path}")
        
        try:
            if os.path.exists(checkpoint_path):
                os.remove(checkpoint_path)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting checkpoint {checkpoint_path}: {str(e)}")
            return False
    
    def start_auto_checkpointing(
        self,
        workflow_id: str,
        actions: List[Any],
        context_provider: Callable[[], ExecutionContext],
        index_provider: Callable[[], int],
        metadata_provider: Optional[Callable[[], Dict[str, Any]]] = None
    ) -> None:
        """
        Start automatic checkpointing for a workflow
        
        Args:
            workflow_id: ID of the workflow
            actions: List of actions in the workflow
            context_provider: Function that returns the current execution context
            index_provider: Function that returns the current action index
            metadata_provider: Optional function that returns metadata to include
        """
        self.logger.info(
            f"Starting auto-checkpointing for workflow {workflow_id} "
            f"at {self.auto_checkpoint_interval}s intervals"
        )
        
        with self._lock:
            # Stop existing thread if any
            self.stop_auto_checkpointing(workflow_id)
            
            # Create stop event
            stop_event = threading.Event()
            self._stop_events[workflow_id] = stop_event
            
            # Create and start thread
            thread = threading.Thread(
                target=self._auto_checkpoint_worker,
                args=(
                    workflow_id,
                    actions,
                    context_provider,
                    index_provider,
                    metadata_provider,
                    stop_event
                ),
                daemon=True
            )
            self._checkpoint_threads[workflow_id] = thread
            thread.start()
    
    def stop_auto_checkpointing(self, workflow_id: str) -> None:
        """
        Stop automatic checkpointing for a workflow
        
        Args:
            workflow_id: ID of the workflow
        """
        with self._lock:
            if workflow_id in self._stop_events:
                self.logger.info(f"Stopping auto-checkpointing for workflow {workflow_id}")
                self._stop_events[workflow_id].set()
                if workflow_id in self._checkpoint_threads:
                    thread = self._checkpoint_threads[workflow_id]
                    if thread.is_alive():
                        thread.join(timeout=1.0)
                    del self._checkpoint_threads[workflow_id]
                del self._stop_events[workflow_id]
    
    def _auto_checkpoint_worker(
        self,
        workflow_id: str,
        actions: List[Any],
        context_provider: Callable[[], ExecutionContext],
        index_provider: Callable[[], int],
        metadata_provider: Optional[Callable[[], Dict[str, Any]]],
        stop_event: threading.Event
    ) -> None:
        """
        Worker function for automatic checkpointing
        
        Args:
            workflow_id: ID of the workflow
            actions: List of actions in the workflow
            context_provider: Function that returns the current execution context
            index_provider: Function that returns the current action index
            metadata_provider: Optional function that returns metadata to include
            stop_event: Event to signal thread to stop
        """
        self.logger.debug(f"Auto-checkpoint worker started for workflow {workflow_id}")
        
        while not stop_event.is_set():
            try:
                # Get current state
                context = context_provider()
                current_index = index_provider()
                metadata = metadata_provider() if metadata_provider else None
                
                # Create checkpoint
                self.create_checkpoint(
                    workflow_id,
                    actions,
                    context,
                    current_index,
                    metadata
                )
                
                # Wait for next checkpoint or until stopped
                stop_event.wait(self.auto_checkpoint_interval)
            except Exception as e:
                self.logger.error(
                    f"Error in auto-checkpoint worker for workflow {workflow_id}: {str(e)}"
                )
                # Wait a bit before retrying
                stop_event.wait(5.0)
    
    def _cleanup_old_checkpoints(self, workflow_id: str) -> None:
        """
        Clean up old checkpoints for a workflow
        
        Args:
            workflow_id: ID of the workflow
        """
        # Get all checkpoints
        checkpoints = self.list_checkpoints(workflow_id)
        
        # If we have more than max_checkpoints, delete the oldest ones
        if len(checkpoints) > self.max_checkpoints:
            # Sort by creation time (oldest first)
            checkpoints.sort(key=lambda c: c.get("created_at", ""))
            
            # Delete oldest checkpoints
            for checkpoint in checkpoints[:-self.max_checkpoints]:
                file_path = checkpoint.get("file_path")
                if file_path:
                    self.delete_checkpoint(file_path)
