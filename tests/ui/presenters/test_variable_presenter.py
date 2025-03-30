"""Tests for the VariablePresenter class."""
import unittest
from unittest.mock import MagicMock, patch

from src.ui.presenters.variable_presenter import VariablePresenter
from src.ui.adapters.variable_adapter import VariableAdapter
from src.core.models import Variable

class TestVariablePresenter(unittest.TestCase):
    """Test cases for the VariablePresenter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=VariableAdapter)
        
        # Create the presenter
        self.presenter = VariablePresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service
        )
        
        # Set up mock data
        self.mock_variables = {
            "Global": [
                {"name": "global_var", "type": "String", "value": "global value", "scope": "Global"}
            ],
            "Workflow": [
                {"name": "workflow_var", "type": "Integer", "value": 42, "scope": "Workflow"}
            ],
            "Local": [
                {"name": "local_var", "type": "Boolean", "value": True, "scope": "Local"}
            ]
        }
        
        # Configure mock service
        self.mock_service.get_all_variables.return_value = self.mock_variables
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the service was called
        self.mock_service.get_all_variables.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_variable_list.assert_called_once_with(self.mock_variables)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_load_variables(self):
        """Test loading variables."""
        # Call the method
        self.presenter.load_variables()
        
        # Verify the service was called
        self.mock_service.get_all_variables.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_variable_list.assert_called_once_with(self.mock_variables)
    
    def test_filter_variables_all(self):
        """Test filtering variables by 'All' scope."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Call the method
        self.presenter.filter_variables("All")
        
        # Verify the view was updated with all variables
        self.mock_view.update_variable_list.assert_called_once_with(self.mock_variables)
    
    def test_filter_variables_specific_scope(self):
        """Test filtering variables by a specific scope."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Call the method
        self.presenter.filter_variables("Global")
        
        # Verify the view was updated with only Global variables
        expected_filtered = {"Global": self.mock_variables["Global"]}
        self.mock_view.update_variable_list.assert_called_once_with(expected_filtered)
    
    def test_select_variable(self):
        """Test selecting a variable."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Call the method
        self.presenter.select_variable("Workflow:workflow_var")
        
        # Verify the view was updated with the selected variable
        self.mock_view.populate_editor.assert_called_once_with(self.mock_variables["Workflow"][0])
    
    def test_select_variable_not_found(self):
        """Test selecting a variable that doesn't exist."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Call the method
        self.presenter.select_variable("Workflow:nonexistent_var")
        
        # Verify the view was cleared
        self.mock_view.clear_editor.assert_called_once()
        self.mock_view.set_editor_state.assert_called_once_with(False)
    
    def test_select_scope_node(self):
        """Test selecting a scope node."""
        # Call the method
        self.presenter.select_variable("Workflow")
        
        # Verify the view was cleared
        self.mock_view.clear_editor.assert_called_once()
        self.mock_view.set_editor_state.assert_called_once_with(False)
    
    def test_save_variable_new(self):
        """Test saving a new variable."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Set up mock service
        self.mock_service.add_variable.return_value = Variable(
            name="new_var", type="String", value="new value", scope="Workflow"
        )
        
        # Call the method
        self.presenter.save_variable({
            "name": "new_var",
            "type": "String",
            "value": "new value",
            "scope": "Workflow"
        })
        
        # Verify the service was called
        self.mock_service.add_variable.assert_called_once_with(
            name="new_var", value="new value", scope="Workflow"
        )
        
        # Verify variables were reloaded
        self.mock_service.get_all_variables.assert_called_once()
    
    def test_save_variable_update(self):
        """Test updating an existing variable."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Set up mock service
        self.mock_service.update_variable.return_value = Variable(
            name="workflow_var", type="Integer", value=99, scope="Workflow"
        )
        
        # Call the method
        self.presenter.save_variable({
            "name": "workflow_var",
            "type": "Integer",
            "value": 99,
            "scope": "Workflow"
        })
        
        # Verify the service was called
        self.mock_service.update_variable.assert_called_once_with(
            name="workflow_var", value=99, scope="Workflow"
        )
        
        # Verify variables were reloaded
        self.mock_service.get_all_variables.assert_called_once()
    
    def test_save_variable_validation_error(self):
        """Test saving a variable with validation errors."""
        # Call the method with empty name
        self.presenter.save_variable({
            "name": "",
            "type": "String",
            "value": "value",
            "scope": "Workflow"
        })
        
        # Verify validation error was shown
        self.mock_view.show_validation_error.assert_called_once()
        
        # Verify the service was not called
        self.mock_service.add_variable.assert_not_called()
        self.mock_service.update_variable.assert_not_called()
    
    def test_delete_variable_confirmed(self):
        """Test deleting a variable with confirmation."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Set up mock view to confirm deletion
        self.mock_view.ask_yes_no.return_value = True
        
        # Set up mock service
        self.mock_service.delete_variable.return_value = True
        
        # Call the method
        self.presenter.delete_variable("Workflow:workflow_var")
        
        # Verify the service was called
        self.mock_service.delete_variable.assert_called_once_with("workflow_var", "Workflow")
        
        # Verify variables were reloaded
        self.mock_service.get_all_variables.assert_called_once()
        
        # Verify the view was cleared
        self.mock_view.clear_editor.assert_called_once()
        self.mock_view.set_editor_state.assert_called_once_with(False)
    
    def test_delete_variable_cancelled(self):
        """Test cancelling variable deletion."""
        # Set up mock view to cancel deletion
        self.mock_view.ask_yes_no.return_value = False
        
        # Call the method
        self.presenter.delete_variable("Workflow:workflow_var")
        
        # Verify the service was not called
        self.mock_service.delete_variable.assert_not_called()
    
    def test_delete_variable_failed(self):
        """Test failed variable deletion."""
        # Set up the presenter with variables
        self.presenter.variables_by_scope = self.mock_variables
        
        # Set up mock view to confirm deletion
        self.mock_view.ask_yes_no.return_value = True
        
        # Set up mock service to fail
        self.mock_service.delete_variable.return_value = False
        
        # Call the method
        self.presenter.delete_variable("Workflow:workflow_var")
        
        # Verify the service was called
        self.mock_service.delete_variable.assert_called_once_with("workflow_var", "Workflow")
        
        # Verify error was displayed
        self.mock_view.display_error.assert_called_once()

if __name__ == "__main__":
    unittest.main()
