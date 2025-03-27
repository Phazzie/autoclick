"""Interfaces for UI views"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ViewInterface(ABC):
    """Base interface for all views"""
    
    @abstractmethod
    def show_message(self, message: str) -> None:
        """
        Show a message to the user
        
        Args:
            message: The message to show
        """
        pass


class WorkflowViewInterface(ViewInterface):
    """Interface for workflow view"""
    
    @abstractmethod
    def display_actions(self, actions: List[Dict[str, Any]]) -> None:
        """
        Display workflow actions
        
        Args:
            actions: List of actions to display
        """
        pass
    
    @abstractmethod
    def get_selected_action_id(self) -> Optional[str]:
        """
        Get the ID of the selected action
        
        Returns:
            The ID of the selected action, or None if no action is selected
        """
        pass


class RecordViewInterface(ViewInterface):
    """Interface for record view"""
    
    @abstractmethod
    def display_recorded_actions(self, actions: List[Dict[str, Any]]) -> None:
        """
        Display recorded actions
        
        Args:
            actions: List of recorded actions to display
        """
        pass
    
    @abstractmethod
    def get_selected_recorded_action_indices(self) -> List[int]:
        """
        Get the indices of selected recorded actions
        
        Returns:
            List of indices of selected recorded actions
        """
        pass


class ElementSelectorViewInterface(ViewInterface):
    """Interface for element selector view"""
    
    @abstractmethod
    def display_element_properties(self, properties: Dict[str, Any]) -> None:
        """
        Display element properties
        
        Args:
            properties: Element properties to display
        """
        pass
    
    @abstractmethod
    def get_url(self) -> str:
        """
        Get the URL entered by the user
        
        Returns:
            The URL
        """
        pass


class ExecutionViewInterface(ViewInterface):
    """Interface for execution view"""
    
    @abstractmethod
    def display_execution_log(self, log: str) -> None:
        """
        Display execution log
        
        Args:
            log: Log text to display
        """
        pass
    
    @abstractmethod
    def get_execution_options(self) -> Dict[str, Any]:
        """
        Get execution options
        
        Returns:
            Dictionary of execution options
        """
        pass
