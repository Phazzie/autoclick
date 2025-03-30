"""
Variable Management Presenter for handling variable operations.
SOLID: Single responsibility - business logic for variable management.
KISS: Simple operations with clear error handling.
"""
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.variable_adapter import VariableAdapter

if TYPE_CHECKING:
    from ..views.variable_view import VariableView
    from app import AutoClickApp

class VariablePresenter(BasePresenter[VariableAdapter]):
    """Presenter for the Variable Management view."""
    
    # Type hints for view and app
    view: 'VariableView'
    app: 'AutoClickApp'
    
    def __init__(self, view: 'VariableView', app: 'AutoClickApp', service: VariableAdapter):
        """
        Initialize the variable presenter.
        
        Args:
            view: The variable view
            app: The main application
            service: The variable adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.variables_by_scope = {}  # Cache of variables by scope
    
    def initialize_view(self):
        """Initialize the view with data."""
        try:
            self.load_variables()
            self.update_app_status("Variable management initialized")
        except Exception as e:
            self._handle_error("initializing variable management", e)
    
    def load_variables(self):
        """Load variables from the service and update the view."""
        try:
            # Get all variables from the service
            self.variables_by_scope = self.service.get_all_variables()
            
            # Update the view
            self.view.update_variable_list(self.variables_by_scope)
            self.update_app_status("Variables loaded")
        except Exception as e:
            self._handle_error("loading variables", e)
    
    def filter_variables(self, scope: str):
        """
        Filter variables by scope.
        
        Args:
            scope: Scope to filter by ("All", "Global", "Workflow", "Local")
        """
        try:
            if scope == "All":
                # Show all variables
                self.view.update_variable_list(self.variables_by_scope)
            else:
                # Show only variables in the selected scope
                filtered_variables = {
                    scope: self.variables_by_scope.get(scope, [])
                }
                self.view.update_variable_list(filtered_variables)
            
            self.update_app_status(f"Filtered variables by {scope} scope")
        except Exception as e:
            self._handle_error(f"filtering variables by {scope}", e)
    
    def select_variable(self, variable_id: str):
        """
        Handle variable selection.
        
        Args:
            variable_id: ID of the selected variable (format: "scope:name")
        """
        try:
            # Parse the variable ID
            if ":" not in variable_id:
                # This is a scope node, not a variable
                self.view.clear_editor()
                self.view.set_editor_state(False)
                return
            
            scope, name = variable_id.split(":", 1)
            
            # Find the variable in the cache
            variable = None
            for var in self.variables_by_scope.get(scope, []):
                if var["name"] == name:
                    variable = var
                    break
            
            if variable:
                # Populate the editor with the variable data
                self.view.populate_editor(variable)
                self.update_app_status(f"Selected variable: {name}")
            else:
                # Variable not found
                self.view.clear_editor()
                self.view.set_editor_state(False)
                self.update_app_status(f"Variable not found: {name}")
        except Exception as e:
            self._handle_error(f"selecting variable {variable_id}", e)
    
    def save_variable(self, variable_data: Dict[str, Any]):
        """
        Save a variable.
        
        Args:
            variable_data: Dictionary containing the variable data
        """
        try:
            # Validate the variable data
            name = variable_data.get("name", "").strip()
            if not name:
                self.view.show_validation_error("Variable name is required")
                return
            
            # Check if this is a new variable or an update
            scope = variable_data.get("scope", "Workflow")
            is_new = True
            
            # Check if the variable already exists in this scope
            for var in self.variables_by_scope.get(scope, []):
                if var["name"] == name:
                    is_new = False
                    break
            
            # Save the variable
            if is_new:
                # Create a new variable
                self.service.add_variable(
                    name=name,
                    value=variable_data.get("value", ""),
                    scope=scope
                )
                self.update_app_status(f"Created variable: {name}")
            else:
                # Update an existing variable
                self.service.update_variable(
                    name=name,
                    value=variable_data.get("value", ""),
                    scope=scope
                )
                self.update_app_status(f"Updated variable: {name}")
            
            # Reload variables to refresh the view
            self.load_variables()
            
            # Select the saved variable
            self.select_variable(f"{scope}:{name}")
        except Exception as e:
            self._handle_error(f"saving variable {variable_data.get('name', '')}", e)
    
    def delete_variable(self, variable_id: str):
        """
        Delete a variable.
        
        Args:
            variable_id: ID of the variable to delete (format: "scope:name")
        """
        try:
            # Parse the variable ID
            if ":" not in variable_id:
                # This is a scope node, not a variable
                return
            
            scope, name = variable_id.split(":", 1)
            
            # Confirm deletion
            if not self.view.ask_yes_no("Confirm Delete", f"Are you sure you want to delete the variable '{name}'?"):
                return
            
            # Delete the variable
            success = self.service.delete_variable(name, scope)
            
            if success:
                self.update_app_status(f"Deleted variable: {name}")
                
                # Reload variables to refresh the view
                self.load_variables()
                
                # Clear the editor
                self.view.clear_editor()
                self.view.set_editor_state(False)
            else:
                self.view.display_error("Delete Failed", f"Failed to delete variable: {name}")
        except Exception as e:
            self._handle_error(f"deleting variable {variable_id}", e)
