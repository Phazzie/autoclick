"""
Loop Configuration Presenter for handling loop operations.
SOLID: Single responsibility - business logic for loop configuration.
KISS: Simple operations with clear error handling.
"""
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.loop_adapter import LoopAdapter

if TYPE_CHECKING:
    from ..views.loop_view import LoopView
    from app import AutoClickApp

class LoopPresenter(BasePresenter[LoopAdapter]):
    """Presenter for the Loop Configuration view."""
    
    # Type hints for view and app
    view: 'LoopView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'LoopView', app: 'AutoClickApp', service: LoopAdapter):
        """
        Initialize the loop presenter.
        
        Args:
            view: The loop view
            app: The main application
            service: The loop adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.loop_types = []  # Cache of loop types
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            self.load_loop_types()
            self.update_app_status("Loop configuration initialized")
        except Exception as e:
            self._handle_error("initializing loop configuration", e)
    
    def load_loop_types(self):
        """Load loop types from the service and update the view."""
        try:
            # Get all loop types from the service
            self.loop_types = self.service.get_loop_types()
            
            # Update the view
            self.view.update_loop_types(self.loop_types)
            self.update_app_status("Loop types loaded")
        except Exception as e:
            self._handle_error("loading loop types", e)
    
    def select_loop_type(self, loop_type: str):
        """
        Handle loop type selection.
        
        Args:
            loop_type: Type of loop to select
        """
        try:
            # Find the loop type in the cache
            selected_type = None
            for ltype in self.loop_types:
                if ltype["type"] == loop_type:
                    selected_type = ltype
                    break
            
            if selected_type:
                # Update the parameter editors in the view
                self.view.update_parameter_editors(selected_type)
                self.update_app_status(f"Selected loop type: {selected_type['name']}")
            else:
                self.update_app_status(f"Loop type not found: {loop_type}")
        except Exception as e:
            self._handle_error(f"selecting loop type {loop_type}", e)
    
    def select_loop(self, loop_id: str):
        """
        Handle loop selection.
        
        Args:
            loop_id: ID of the loop to select
        """
        try:
            # Get the loop from the service
            loop = self.service.get_loop_by_id(loop_id)
            
            if loop:
                # Populate the editor with the loop data
                self.view.populate_editor(loop)
                self.update_app_status(f"Selected loop: {loop.get('description', loop_id)}")
            else:
                # Loop not found
                self.view.clear_editor()
                self.view.set_editor_state(False)
                self.update_app_status(f"Loop not found: {loop_id}")
        except Exception as e:
            self._handle_error(f"selecting loop {loop_id}", e)
    
    def create_loop(self, loop_data: Dict[str, Any]):
        """
        Create a new loop.
        
        Args:
            loop_data: Dictionary containing loop data
        """
        try:
            # Create the loop
            loop = self.service.create_loop(loop_data)
            
            # Add the loop to the list
            self.view.add_loop_to_list(loop)
            
            self.update_app_status(f"Created loop: {loop.get('description', loop['id'])}")
            
            return loop
        except Exception as e:
            self._handle_error("creating loop", e)
            return None
    
    def update_loop(self, loop_data: Dict[str, Any]):
        """
        Update an existing loop.
        
        Args:
            loop_data: Dictionary containing updated loop data
        """
        try:
            # Update the loop
            loop = self.service.update_loop(loop_data)
            
            # Update the loop in the list
            self.view.update_loop_in_list(loop)
            
            self.update_app_status(f"Updated loop: {loop.get('description', loop['id'])}")
            
            return loop
        except Exception as e:
            self._handle_error("updating loop", e)
            return None
    
    def delete_loop(self, loop_id: str):
        """
        Delete a loop.
        
        Args:
            loop_id: ID of the loop to delete
        """
        try:
            # Get the loop for confirmation
            loop = self.service.get_loop_by_id(loop_id)
            
            if not loop:
                self.update_app_status(f"Loop not found: {loop_id}")
                return False
            
            # Confirm deletion
            description = loop.get("description", loop_id)
            if not self.view.ask_yes_no("Confirm Delete", f"Are you sure you want to delete the loop '{description}'?"):
                return False
            
            # Delete the loop
            success = self.service.delete_loop(loop_id)
            
            if success:
                # Remove the loop from the list
                self.view.remove_loop_from_list(loop_id)
                
                # Clear the editor if the deleted loop was selected
                if self.view.selected_loop == loop_id:
                    self.view.clear_editor()
                    self.view.set_editor_state(False)
                
                self.update_app_status(f"Deleted loop: {description}")
                return True
            else:
                self.view.display_error("Delete Failed", f"Failed to delete loop: {description}")
                return False
        except Exception as e:
            self._handle_error(f"deleting loop {loop_id}", e)
            return False
    
    def save_loop_from_editor(self):
        """Save the loop from the editor."""
        try:
            # Get the loop data from the editor
            loop_data = self.view.get_editor_data()
            
            # Check if this is a new loop or an update
            if not loop_data.get("id"):
                # Create a new loop
                loop = self.create_loop(loop_data)
                if loop:
                    # Select the new loop
                    self.select_loop(loop["id"])
            else:
                # Update an existing loop
                loop = self.update_loop(loop_data)
                if loop:
                    # Select the updated loop
                    self.select_loop(loop["id"])
        except Exception as e:
            self._handle_error("saving loop from editor", e)
