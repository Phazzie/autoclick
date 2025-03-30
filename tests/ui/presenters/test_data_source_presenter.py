"""Tests for the DataSourcePresenter class."""
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List

from src.core.models import DataSourceConfig
from src.ui.presenters.data_source_presenter import DataSourcePresenter
from src.ui.adapters.data_source_adapter import DataSourceAdapter

class TestDataSourcePresenter(unittest.TestCase):
    """Test cases for the DataSourcePresenter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=DataSourceAdapter)
        
        # Create the presenter
        self.presenter = DataSourcePresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service
        )
        
        # Set up mock data
        self.mock_data_sources = [
            DataSourceConfig(
                id="csv_example",
                name="Example CSV",
                type="CSV File",
                config_params={
                    "file_path": "data/example.csv",
                    "has_header": True,
                    "delimiter": ","
                }
            ),
            DataSourceConfig(
                id="json_example",
                name="Example JSON",
                type="JSON File",
                config_params={
                    "file_path": "data/example.json",
                    "root_element": "items"
                }
            )
        ]
        
        # Configure mock service
        self.mock_service.get_all_data_sources.return_value = self.mock_data_sources
    
    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()
        
        # Verify the service was called
        self.mock_service.get_all_data_sources.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_data_source_list.assert_called_once_with(self.mock_data_sources)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_load_data_sources(self):
        """Test loading data sources."""
        # Call the method
        self.presenter.load_data_sources()
        
        # Verify the service was called
        self.mock_service.get_all_data_sources.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_data_source_list.assert_called_once_with(self.mock_data_sources)
    
    def test_filter_data_sources_by_type(self):
        """Test filtering data sources by type."""
        # Set up the presenter with data sources
        self.presenter.data_sources = self.mock_data_sources
        
        # Call the method
        self.presenter.filter_data_sources_by_type("CSV File")
        
        # Verify the view was updated with only CSV sources
        expected_filtered = [self.mock_data_sources[0]]  # Only the CSV example
        self.mock_view.update_data_source_list.assert_called_once_with(expected_filtered)
    
    def test_filter_data_sources_by_type_all(self):
        """Test filtering data sources by 'All' type."""
        # Set up the presenter with data sources
        self.presenter.data_sources = self.mock_data_sources
        
        # Call the method
        self.presenter.filter_data_sources_by_type("All")
        
        # Verify the view was updated with all sources
        self.mock_view.update_data_source_list.assert_called_once_with(self.mock_data_sources)
    
    def test_select_data_source(self):
        """Test selecting a data source."""
        # Set up mock service
        self.mock_service.get_data_source.return_value = self.mock_data_sources[0]
        
        # Call the method
        self.presenter.select_data_source("csv_example")
        
        # Verify the service was called
        self.mock_service.get_data_source.assert_called_once_with("csv_example")
        
        # Verify the view was updated
        self.mock_view.populate_editor.assert_called_once_with(self.mock_data_sources[0])
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_select_data_source_not_found(self):
        """Test selecting a data source that doesn't exist."""
        # Set up mock service
        self.mock_service.get_data_source.return_value = None
        
        # Call the method
        self.presenter.select_data_source("nonexistent")
        
        # Verify the service was called
        self.mock_service.get_data_source.assert_called_once_with("nonexistent")
        
        # Verify the view was cleared
        self.mock_view.clear_editor.assert_called_once()
        self.mock_view.set_editor_state.assert_called_once_with(False)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_add_data_source(self):
        """Test adding a new data source."""
        # Set up mock service
        new_source = DataSourceConfig(
            id="new_source",
            name="New Source",
            type="CSV File",
            config_params={
                "file_path": "data/new.csv",
                "has_header": True,
                "delimiter": ","
            }
        )
        self.mock_service.add_data_source.return_value = new_source
        
        # Call the method
        self.presenter.add_data_source(
            name="New Source",
            type_name="CSV File",
            config_params={
                "file_path": "data/new.csv",
                "has_header": True,
                "delimiter": ","
            }
        )
        
        # Verify the service was called
        self.mock_service.add_data_source.assert_called_once_with(
            name="New Source",
            type_name="CSV File",
            config_params={
                "file_path": "data/new.csv",
                "has_header": True,
                "delimiter": ","
            }
        )
        
        # Verify the view was updated
        self.mock_view.add_data_source_to_list.assert_called_once_with(new_source)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_update_data_source(self):
        """Test updating a data source."""
        # Set up mock service
        updated_source = DataSourceConfig(
            id="csv_example",
            name="Updated CSV",
            type="CSV File",
            config_params={
                "file_path": "data/updated.csv",
                "has_header": False,
                "delimiter": ";"
            }
        )
        self.mock_service.update_data_source.return_value = updated_source
        
        # Call the method
        self.presenter.update_data_source(
            source_id="csv_example",
            name="Updated CSV",
            type_name="CSV File",
            config_params={
                "file_path": "data/updated.csv",
                "has_header": False,
                "delimiter": ";"
            }
        )
        
        # Verify the service was called
        self.mock_service.update_data_source.assert_called_once_with(
            source_id="csv_example",
            name="Updated CSV",
            type_name="CSV File",
            config_params={
                "file_path": "data/updated.csv",
                "has_header": False,
                "delimiter": ";"
            }
        )
        
        # Verify the view was updated
        self.mock_view.update_data_source_in_list.assert_called_once_with(updated_source)
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_data_source(self):
        """Test deleting a data source."""
        # Set up mock service
        self.mock_service.get_data_source.return_value = self.mock_data_sources[0]
        self.mock_service.delete_data_source.return_value = True
        
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = True
        
        # Call the method
        self.presenter.delete_data_source("csv_example")
        
        # Verify the service was called
        self.mock_service.delete_data_source.assert_called_once_with("csv_example")
        
        # Verify the view was updated
        self.mock_view.remove_data_source_from_list.assert_called_once_with("csv_example")
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_delete_data_source_cancelled(self):
        """Test cancelling data source deletion."""
        # Set up mock service
        self.mock_service.get_data_source.return_value = self.mock_data_sources[0]
        
        # Set up mock view
        self.mock_view.ask_yes_no.return_value = False
        
        # Call the method
        self.presenter.delete_data_source("csv_example")
        
        # Verify the service was not called
        self.mock_service.delete_data_source.assert_not_called()
    
    def test_get_data_preview(self):
        """Test getting a data preview."""
        # Set up mock service
        headers = ["Column1", "Column2", "Column3"]
        rows = [
            ["Value1", "Value2", "Value3"],
            ["Value4", "Value5", "Value6"]
        ]
        self.mock_service.get_data_preview.return_value = (headers, rows)
        
        # Call the method
        self.presenter.get_data_preview("csv_example")
        
        # Verify the service was called
        self.mock_service.get_data_preview.assert_called_once_with("csv_example")
        
        # Verify the view was updated
        self.mock_view.display_data_preview.assert_called_once_with(headers, rows)
    
    def test_save_data_source_from_editor_new(self):
        """Test saving a new data source from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "id": "",  # Empty ID indicates a new source
            "name": "New Source",
            "type": "CSV File",
            "config_params": {
                "file_path": "data/new.csv",
                "has_header": True,
                "delimiter": ","
            }
        }
        
        # Set up mock service
        new_source = DataSourceConfig(
            id="new_source",
            name="New Source",
            type="CSV File",
            config_params={
                "file_path": "data/new.csv",
                "has_header": True,
                "delimiter": ","
            }
        )
        self.mock_service.add_data_source.return_value = new_source
        
        # Call the method
        self.presenter.save_data_source_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.add_data_source.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.add_data_source_to_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()
    
    def test_save_data_source_from_editor_update(self):
        """Test updating a data source from the editor."""
        # Set up mock view
        self.mock_view.get_editor_data.return_value = {
            "id": "csv_example",  # Existing ID
            "name": "Updated CSV",
            "type": "CSV File",
            "config_params": {
                "file_path": "data/updated.csv",
                "has_header": False,
                "delimiter": ";"
            }
        }
        
        # Set up mock service
        updated_source = DataSourceConfig(
            id="csv_example",
            name="Updated CSV",
            type="CSV File",
            config_params={
                "file_path": "data/updated.csv",
                "has_header": False,
                "delimiter": ";"
            }
        )
        self.mock_service.update_data_source.return_value = updated_source
        
        # Call the method
        self.presenter.save_data_source_from_editor()
        
        # Verify the view was called
        self.mock_view.get_editor_data.assert_called_once()
        
        # Verify the service was called
        self.mock_service.update_data_source.assert_called_once()
        
        # Verify the view was updated
        self.mock_view.update_data_source_in_list.assert_called_once()
        
        # Verify the status was updated
        self.mock_app.update_status.assert_called()

if __name__ == "__main__":
    unittest.main()
