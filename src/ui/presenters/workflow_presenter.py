"""Workflow presenter implementation"""
import logging
from typing import Any, Dict, List, Optional

from src.ui.models.workflow_model import WorkflowModel
from src.ui.interfaces.view_interface import WorkflowViewInterface


class WorkflowPresenter:
    """Presenter for workflow tab"""
    
    def __init__(self, model: WorkflowModel, view: Optional[WorkflowViewInterface] = None) -> None:
        """
        Initialize the workflow presenter
        
        Args:
            model: Workflow model
            view: Workflow view
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.view = view
    
    def set_view(self, view: WorkflowViewInterface) -> None:
        """
        Set the view
        
        Args:
            view: Workflow view
        """
        self.view = view
    
    def add_action(self, action: Dict[str, Any]) -> None:
        """
        Add an action to the workflow
        
        Args:
            action: Action to add
        """
        self.logger.info("Adding action to workflow")
        
        action_id = self.model.add_action(action)
        self.refresh_view()
        
        if self.view:
            self.view.show_message(f"Action added: {action.get('description', 'No description')}")
    
    def remove_action(self) -> None:
        """Remove the selected action"""
        self.logger.info("Removing action from workflow")
        
        if not self.view:
            return
            
        action_id = self.view.get_selected_action_id()
        
        if not action_id:
            self.view.show_message("No action selected")
            return
            
        action = self.model.get_action(action_id)
        
        if not action:
            self.view.show_message("Failed to get action details")
            return
            
        if self.model.remove_action(action_id):
            self.refresh_view()
            self.view.show_message(f"Action removed: {action.get('description', 'No description')}")
        else:
            self.view.show_message("Failed to remove action")
    
    def update_action(self, action_id: str, updated_action: Dict[str, Any]) -> None:
        """
        Update an action
        
        Args:
            action_id: ID of the action to update
            updated_action: Updated action data
        """
        self.logger.info(f"Updating action {action_id}")
        
        if not self.view:
            return
            
        if self.model.update_action(action_id, updated_action):
            self.refresh_view()
            self.view.show_message(f"Action updated: {updated_action.get('description', 'No description')}")
        else:
            self.view.show_message("Failed to update action")
    
    def move_action_up(self) -> None:
        """Move the selected action up"""
        self.logger.info("Moving action up")
        
        if not self.view:
            return
            
        action_id = self.view.get_selected_action_id()
        
        if not action_id:
            self.view.show_message("No action selected")
            return
            
        # Get all actions
        actions = self.model.get_actions()
        action_ids = [action.get("id") for action in actions]
        
        # Find index of selected action
        if action_id not in action_ids:
            self.view.show_message("Failed to find action")
            return
            
        index = action_ids.index(action_id)
        
        # Check if action can be moved up
        if index > 0:
            # Swap with previous action
            action_ids[index], action_ids[index-1] = action_ids[index-1], action_ids[index]
            
            # Reorder actions
            if self.model.reorder_actions(action_ids):
                self.refresh_view()
                self.view.show_message("Action moved up")
            else:
                self.view.show_message("Failed to reorder actions")
        else:
            self.view.show_message("Action is already at the top")
    
    def move_action_down(self) -> None:
        """Move the selected action down"""
        self.logger.info("Moving action down")
        
        if not self.view:
            return
            
        action_id = self.view.get_selected_action_id()
        
        if not action_id:
            self.view.show_message("No action selected")
            return
            
        # Get all actions
        actions = self.model.get_actions()
        action_ids = [action.get("id") for action in actions]
        
        # Find index of selected action
        if action_id not in action_ids:
            self.view.show_message("Failed to find action")
            return
            
        index = action_ids.index(action_id)
        
        # Check if action can be moved down
        if index < len(action_ids) - 1:
            # Swap with next action
            action_ids[index], action_ids[index+1] = action_ids[index+1], action_ids[index]
            
            # Reorder actions
            if self.model.reorder_actions(action_ids):
                self.refresh_view()
                self.view.show_message("Action moved down")
            else:
                self.view.show_message("Failed to reorder actions")
        else:
            self.view.show_message("Action is already at the bottom")
    
    def refresh_view(self) -> None:
        """Refresh the view with current model data"""
        self.logger.debug("Refreshing workflow view")
        
        if self.view:
            self.view.display_actions(self.model.get_actions())
