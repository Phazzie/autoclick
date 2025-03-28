"""Record presenter implementation"""
import logging
from typing import Any, Dict, List, Optional

from src.ui.models.record_model import RecordModel
from src.ui.interfaces.view_interface import RecordViewInterface


class RecordPresenter:
    """Presenter for record tab"""
    
    def __init__(self, model: RecordModel, view: Optional[RecordViewInterface] = None) -> None:
        """
        Initialize the record presenter
        
        Args:
            model: Record model
            view: Record view
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.view = view
    
    def set_view(self, view: RecordViewInterface) -> None:
        """
        Set the view
        
        Args:
            view: Record view
        """
        self.view = view
    
    def start_recording(self) -> None:
        """Start recording browser actions"""
        self.logger.info("Starting browser recording")
        
        if not self.view:
            return
        
        try:
            # In a real implementation, this would start the browser recorder
            # For now, we'll just update the model
            self.model.start_recording()
            
            self.view.show_message("Recording started")
        except Exception as e:
            self.logger.error(f"Error starting recording: {str(e)}")
            self.view.show_message(f"Error starting recording: {str(e)}")
    
    def stop_recording(self) -> None:
        """Stop recording browser actions"""
        self.logger.info("Stopping browser recording")
        
        if not self.view:
            return
        
        try:
            # In a real implementation, this would stop the browser recorder
            # and get the recorded actions
            # For now, we'll just update the model
            self.model.stop_recording()
            
            # Simulate some recorded actions for testing
            if not self.model.recorded_actions:
                self.model.add_recorded_action({
                    "type": "click",
                    "selector": "#submit-button",
                    "description": "Click submit button"
                })
                self.model.add_recorded_action({
                    "type": "input",
                    "selector": "#email-input",
                    "value": "test@example.com",
                    "description": "Enter email"
                })
            
            # Refresh the view
            self.refresh_view()
            
            self.view.show_message(f"Recording stopped, captured {len(self.model.recorded_actions)} actions")
        except Exception as e:
            self.logger.error(f"Error stopping recording: {str(e)}")
            self.view.show_message(f"Error stopping recording: {str(e)}")
    
    def add_recorded_action(self, action: Dict[str, Any]) -> None:
        """
        Add a recorded action
        
        Args:
            action: The action to add
        """
        self.logger.info("Adding recorded action")
        
        self.model.add_recorded_action(action)
        self.refresh_view()
        
        if self.view:
            self.view.show_message(f"Action added: {action.get('description', 'No description')}")
    
    def clear_recorded_actions(self) -> None:
        """Clear all recorded actions"""
        self.logger.info("Clearing recorded actions")
        
        self.model.clear_recorded_actions()
        self.refresh_view()
        
        if self.view:
            self.view.show_message("Recorded actions cleared")
    
    def set_browser_type(self, browser_type: str) -> None:
        """
        Set the browser type
        
        Args:
            browser_type: The browser type (chrome, firefox, edge)
        """
        self.logger.info(f"Setting browser type to {browser_type}")
        
        self.model.set_browser_type(browser_type)
        
        if self.view:
            self.view.show_message(f"Browser type set to {browser_type}")
    
    def set_headless(self, headless: bool) -> None:
        """
        Set headless mode
        
        Args:
            headless: Whether to use headless mode
        """
        self.logger.info(f"Setting headless mode to {headless}")
        
        self.model.set_headless(headless)
        
        if self.view:
            self.view.show_message(f"Headless mode {'enabled' if headless else 'disabled'}")
    
    def refresh_view(self) -> None:
        """Refresh the view with current model data"""
        self.logger.debug("Refreshing record view")
        
        if self.view:
            self.view.display_recorded_actions(self.model.get_recorded_actions())
