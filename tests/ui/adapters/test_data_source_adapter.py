"""Tests for the DataSourceAdapter class."""
import unittest
from unittest.mock import MagicMock, patch
import os

from src.ui.adapters.data_source_adapter import DataSourceAdapter
from src.core.models import DataSourceConfig as UIDataSourceConfig

class TestDataSourceAdapter(unittest.TestCase):
    """Test cases for the DataSourceAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.adapter = DataSourceAdapter()
    
    def test_get_all_data_sources(self):
        """Test getting all data sources."""
        # Act
        result = self.adapter.get_all_data_sources()
        
        # Assert
        self.assertEqual(len(result), 2)  # Default sources
        self.assertIsInstance(result[0], UIDataSourceConfig)
    
    def test_get_data_source(self):
        """Test getting a data source by ID."""
        # Act
        result = self.adapter.get_data_source("csv_example")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "csv_example")
        self.assertEqual(result.name, "Example CSV")
        self.assertEqual(result.type, "CSV File")
        self.assertIn("file_path", result.config_params)
    
    def test_get_data_source_not_found(self):
        """Test getting a data source by ID when it doesn't exist."""
        # Act
        result = self.adapter.get_data_source("nonexistent_source")
        
        # Assert
        self.assertIsNone(result)
    
    def test_add_data_source(self):
        """Test adding a data source."""
        # Act
        result = self.adapter.add_data_source(
            name="Test Source",
            type_name="Database",
            config_params={
                "connection_string": "test_connection",
                "table_name": "test_table"
            }
        )
        
        # Assert
        self.assertEqual(result.name, "Test Source")
        self.assertEqual(result.type, "Database")
        self.assertEqual(result.config_params["connection_string"], "test_connection")
        self.assertEqual(result.config_params["table_name"], "test_table")
        
        # Verify it was added to the dictionary
        self.assertIn(result.id, self.adapter.data_sources)
        self.assertEqual(self.adapter.data_sources[result.id], result)
    
    def test_update_data_source(self):
        """Test updating a data source."""
        # Arrange
        source = self.adapter.add_data_source(
            name="Test Source",
            type_name="Database",
            config_params={
                "connection_string": "test_connection",
                "table_name": "test_table"
            }
        )
        
        # Act
        result = self.adapter.update_data_source(
            source_id=source.id,
            name="Updated Source",
            config_params={
                "connection_string": "updated_connection",
                "table_name": "updated_table"
            }
        )
        
        # Assert
        self.assertEqual(result.name, "Updated Source")
        self.assertEqual(result.type, "Database")  # Unchanged
        self.assertEqual(result.config_params["connection_string"], "updated_connection")
        self.assertEqual(result.config_params["table_name"], "updated_table")
        
        # Verify it was updated in the dictionary
        self.assertEqual(self.adapter.data_sources[source.id].name, "Updated Source")
        self.assertEqual(self.adapter.data_sources[source.id].config_params["connection_string"], "updated_connection")
    
    def test_update_data_source_partial(self):
        """Test partially updating a data source."""
        # Arrange
        source = self.adapter.add_data_source(
            name="Test Source",
            type_name="Database",
            config_params={
                "connection_string": "test_connection",
                "table_name": "test_table"
            }
        )
        
        # Act
        result = self.adapter.update_data_source(
            source_id=source.id,
            name="Updated Source"
        )
        
        # Assert
        self.assertEqual(result.name, "Updated Source")
        self.assertEqual(result.type, "Database")  # Unchanged
        self.assertEqual(result.config_params["connection_string"], "test_connection")  # Unchanged
        self.assertEqual(result.config_params["table_name"], "test_table")  # Unchanged
    
    def test_update_data_source_not_found(self):
        """Test updating a data source that doesn't exist."""
        # Act
        result = self.adapter.update_data_source(
            source_id="nonexistent_source",
            name="Updated Source"
        )
        
        # Assert
        self.assertIsNone(result)
    
    def test_delete_data_source(self):
        """Test deleting a data source."""
        # Arrange
        source = self.adapter.add_data_source(
            name="Test Source",
            type_name="Database"
        )
        
        # Act
        result = self.adapter.delete_data_source(source.id)
        
        # Assert
        self.assertTrue(result)
        self.assertNotIn(source.id, self.adapter.data_sources)
    
    def test_delete_data_source_not_found(self):
        """Test deleting a data source that doesn't exist."""
        # Act
        result = self.adapter.delete_data_source("nonexistent_source")
        
        # Assert
        self.assertFalse(result)
    
    @patch('os.path.exists')
    def test_get_data_preview_csv_file_not_found(self, mock_exists):
        """Test getting a data preview for a CSV file that doesn't exist."""
        # Arrange
        mock_exists.return_value = False
        
        # Act
        columns, rows = self.adapter.get_data_preview("csv_example")
        
        # Assert
        self.assertEqual(len(columns), 3)  # Dummy data
        self.assertEqual(len(rows), 2)  # Dummy data
    
    @patch('os.path.exists')
    def test_get_data_preview_json_file_not_found(self, mock_exists):
        """Test getting a data preview for a JSON file that doesn't exist."""
        # Arrange
        mock_exists.return_value = False
        
        # Act
        columns, rows = self.adapter.get_data_preview("json_example")
        
        # Assert
        self.assertEqual(len(columns), 3)  # Dummy data
        self.assertEqual(len(rows), 2)  # Dummy data

if __name__ == "__main__":
    unittest.main()
