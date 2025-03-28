"""Interface definitions for UI components"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class RecorderInterface(ABC):
    """Interface for recording browser actions"""
    
    @abstractmethod
    def start_recording(self) -> None:
        """Start recording user actions"""
        pass
    
    @abstractmethod
    def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return captured actions"""
        pass

class ElementSelectorInterface(ABC):
    """Interface for selecting elements on a page"""
    
    @abstractmethod
    def select_element(self, browser_instance: Any) -> Dict[str, Any]:
        """Allow user to select an element and return its properties"""
        pass
    
    @abstractmethod
    def highlight_element(self, browser_instance: Any, selector: str) -> None:
        """Highlight an element on the page"""
        pass

class WorkflowBuilderInterface(ABC):
    """Interface for building automation workflows"""
    
    @abstractmethod
    def add_action(self, action: Dict[str, Any]) -> str:
        """Add an action to the workflow and return its ID"""
        pass
    
    @abstractmethod
    def remove_action(self, action_id: str) -> bool:
        """Remove an action from the workflow"""
        pass
    
    @abstractmethod
    def reorder_actions(self, action_ids: List[str]) -> bool:
        """Reorder actions in the workflow"""
        pass
    
    @abstractmethod
    def export_workflow(self) -> Dict[str, Any]:
        """Export the workflow as a configuration"""
        pass

class ExecutionInterface(ABC):
    """Interface for executing automation workflows"""
    
    @abstractmethod
    def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow and return results"""
        pass
    
    @abstractmethod
    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get the status of an execution"""
        pass
