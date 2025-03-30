"""
Condition Management Presenter for handling condition operations.
SOLID: Single responsibility - business logic for condition management.
KISS: Simple operations with clear error handling.
"""
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.condition_adapter import ConditionAdapter

if TYPE_CHECKING:
    from ..views.condition_view import ConditionView
    from app import AutoClickApp

class ConditionPresenter(BasePresenter[ConditionAdapter]):
    """Presenter for the Condition Management view."""
    
    # Type hints for view and app
    view: 'ConditionView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'ConditionView', app: 'AutoClickApp', service: ConditionAdapter):
        """
        Initialize the condition presenter.
        
        Args:
            view: The condition view
            app: The main application
            service: The condition adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.condition_types = []  # Cache of condition types
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            self.load_condition_types()
            self.update_app_status("Condition management initialized")
        except Exception as e:
            self._handle_error("initializing condition management", e)
    
    def load_condition_types(self):
        """Load condition types from the service and update the view."""
        try:
            # Get all condition types from the service
            self.condition_types = self.service.get_condition_types()
            
            # Update the view
            self.view.update_condition_types(self.condition_types)
            self.update_app_status("Condition types loaded")
        except Exception as e:
            self._handle_error("loading condition types", e)
    
    def select_condition_type(self, condition_type: str):
        """
        Handle condition type selection.
        
        Args:
            condition_type: Type of condition to select
        """
        try:
            # Find the condition type in the cache
            selected_type = None
            for ctype in self.condition_types:
                if ctype["type"] == condition_type:
                    selected_type = ctype
                    break
            
            if selected_type:
                # Update the parameter editors in the view
                self.view.update_parameter_editors(selected_type)
                self.update_app_status(f"Selected condition type: {selected_type['name']}")
            else:
                self.update_app_status(f"Condition type not found: {condition_type}")
        except Exception as e:
            self._handle_error(f"selecting condition type {condition_type}", e)
    
    def select_condition(self, condition_id: str):
        """
        Handle condition selection.
        
        Args:
            condition_id: ID of the condition to select
        """
        try:
            # Get the condition from the service
            condition = self.service.get_condition_by_id(condition_id)
            
            if condition:
                # Populate the editor with the condition data
                self.view.populate_editor(condition)
                self.update_app_status(f"Selected condition: {condition.get('description', condition_id)}")
            else:
                # Condition not found
                self.view.clear_editor()
                self.view.set_editor_state(False)
                self.update_app_status(f"Condition not found: {condition_id}")
        except Exception as e:
            self._handle_error(f"selecting condition {condition_id}", e)
    
    def create_condition(self, condition_data: Dict[str, Any]):
        """
        Create a new condition.
        
        Args:
            condition_data: Dictionary containing condition data
        """
        try:
            # Create the condition
            condition = self.service.create_condition(condition_data)
            
            # Add the condition to the list
            self.view.add_condition_to_list(condition)
            
            self.update_app_status(f"Created condition: {condition.get('description', condition['id'])}")
            
            return condition
        except Exception as e:
            self._handle_error("creating condition", e)
            return None
    
    def update_condition(self, condition_data: Dict[str, Any]):
        """
        Update an existing condition.
        
        Args:
            condition_data: Dictionary containing updated condition data
        """
        try:
            # Update the condition
            condition = self.service.update_condition(condition_data)
            
            # Update the condition in the list
            self.view.update_condition_in_list(condition)
            
            self.update_app_status(f"Updated condition: {condition.get('description', condition['id'])}")
            
            return condition
        except Exception as e:
            self._handle_error("updating condition", e)
            return None
    
    def delete_condition(self, condition_id: str):
        """
        Delete a condition.
        
        Args:
            condition_id: ID of the condition to delete
        """
        try:
            # Get the condition for confirmation
            condition = self.service.get_condition_by_id(condition_id)
            
            if not condition:
                self.update_app_status(f"Condition not found: {condition_id}")
                return False
            
            # Confirm deletion
            description = condition.get("description", condition_id)
            if not self.view.ask_yes_no("Confirm Delete", f"Are you sure you want to delete the condition '{description}'?"):
                return False
            
            # Delete the condition
            success = self.service.delete_condition(condition_id)
            
            if success:
                # Remove the condition from the list
                self.view.remove_condition_from_list(condition_id)
                
                # Clear the editor if the deleted condition was selected
                if self.view.selected_condition == condition_id:
                    self.view.clear_editor()
                    self.view.set_editor_state(False)
                
                self.update_app_status(f"Deleted condition: {description}")
                return True
            else:
                self.view.display_error("Delete Failed", f"Failed to delete condition: {description}")
                return False
        except Exception as e:
            self._handle_error(f"deleting condition {condition_id}", e)
            return False
    
    def test_condition(self, condition_id: str, context: Dict[str, Any]):
        """
        Test a condition with the given context.
        
        Args:
            condition_id: ID of the condition to test
            context: Execution context containing variables, browser, etc.
        """
        try:
            # Evaluate the condition
            result = self.service.evaluate_condition(condition_id, context)
            
            # Display the result
            self.view.display_test_result(
                result["value"],
                result["message"]
            )
            
            self.update_app_status(f"Tested condition: {result['message']}")
            
            return result
        except Exception as e:
            self._handle_error(f"testing condition {condition_id}", e)
            return None
    
    def save_condition_from_editor(self):
        """Save the condition from the editor."""
        try:
            # Get the condition data from the editor
            condition_data = self.view.get_editor_data()
            
            # Check if this is a new condition or an update
            if not condition_data.get("id"):
                # Create a new condition
                condition = self.create_condition(condition_data)
                if condition:
                    # Select the new condition
                    self.select_condition(condition["id"])
            else:
                # Update an existing condition
                condition = self.update_condition(condition_data)
                if condition:
                    # Select the updated condition
                    self.select_condition(condition["id"])
        except Exception as e:
            self._handle_error("saving condition from editor", e)
