"""Model for recording browser actions"""
from typing import Dict, List, Any, Optional


class RecordModel:
    """Model for recording browser actions"""
    
    def __init__(self) -> None:
        """Initialize the record model"""
        self.recorded_actions: List[Dict[str, Any]] = []
        self.is_recording: bool = False
        self.browser_type: str = "chrome"
        self.headless: bool = False
    
    def start_recording(self) -> None:
        """Start recording browser actions"""
        self.is_recording = True
    
    def stop_recording(self) -> None:
        """Stop recording browser actions"""
        self.is_recording = False
    
    def add_recorded_action(self, action: Dict[str, Any]) -> None:
        """
        Add a recorded action
        
        Args:
            action: The action to add
        """
        self.recorded_actions.append(action)
    
    def clear_recorded_actions(self) -> None:
        """Clear all recorded actions"""
        self.recorded_actions = []
    
    def get_recorded_actions(self) -> List[Dict[str, Any]]:
        """
        Get all recorded actions
        
        Returns:
            A copy of the recorded actions list
        """
        return self.recorded_actions.copy()
    
    def set_browser_type(self, browser_type: str) -> None:
        """
        Set the browser type
        
        Args:
            browser_type: The browser type (chrome, firefox, edge)
        """
        self.browser_type = browser_type
    
    def set_headless(self, headless: bool) -> None:
        """
        Set headless mode
        
        Args:
            headless: Whether to use headless mode
        """
        self.headless = headless
