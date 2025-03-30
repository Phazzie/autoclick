"""
Adapter for data source management to provide the interface expected by the UI.
SOLID: Single responsibility - adapting data source operations.
KISS: Simple implementation with basic data source configuration.
"""
import uuid
import csv
import json
import os
from typing import List, Dict, Any, Optional, Tuple

from src.core.models import DataSourceConfig as UIDataSourceConfig

class DataSourceAdapter:
    """Adapter for data source management to provide the interface expected by the UI."""
    
    def __init__(self):
        """Initialize the adapter."""
        self.data_sources: Dict[str, UIDataSourceConfig] = {}
        self._load_default_sources()
    
    def _load_default_sources(self):
        """Load default data sources."""
        default_sources = [
            UIDataSourceConfig(
                id="csv_example",
                name="Example CSV",
                type="CSV File",
                config_params={
                    "file_path": "data/example.csv",
                    "has_header": True,
                    "delimiter": ","
                }
            ),
            UIDataSourceConfig(
                id="json_example",
                name="Example JSON",
                type="JSON File",
                config_params={
                    "file_path": "data/example.json",
                    "root_element": "items"
                }
            )
        ]
        
        for source in default_sources:
            self.data_sources[source.id] = source
    
    def get_all_data_sources(self) -> List[UIDataSourceConfig]:
        """
        Get all data sources.
        
        Returns:
            List of data sources in the UI-expected format.
        """
        return list(self.data_sources.values())
    
    def get_data_source(self, source_id: str) -> Optional[UIDataSourceConfig]:
        """
        Get a data source by ID.
        
        Args:
            source_id: Data source ID
            
        Returns:
            Data source in the UI-expected format, or None if not found.
        """
        return self.data_sources.get(source_id)
    
    def add_data_source(self, name: str, type_name: str, config_params: Dict[str, Any] = None) -> UIDataSourceConfig:
        """
        Add a new data source.
        
        Args:
            name: Data source name
            type_name: Data source type (CSV File, JSON File, Database, API Endpoint)
            config_params: Configuration parameters
            
        Returns:
            The new data source in the UI-expected format.
        """
        source_id = str(uuid.uuid4())
        source = UIDataSourceConfig(
            id=source_id,
            name=name,
            type=type_name,
            config_params=config_params or {}
        )
        
        self.data_sources[source_id] = source
        return source
    
    def update_data_source(self, source_id: str, name: Optional[str] = None, type_name: Optional[str] = None, config_params: Optional[Dict[str, Any]] = None) -> Optional[UIDataSourceConfig]:
        """
        Update an existing data source.
        
        Args:
            source_id: Data source ID
            name: Data source name
            type_name: Data source type (CSV File, JSON File, Database, API Endpoint)
            config_params: Configuration parameters
            
        Returns:
            The updated data source in the UI-expected format, or None if not found.
        """
        source = self.data_sources.get(source_id)
        if not source:
            return None
        
        if name is not None:
            source.name = name
        
        if type_name is not None:
            source.type = type_name
        
        if config_params is not None:
            source.config_params = config_params
        
        return source
    
    def delete_data_source(self, source_id: str) -> bool:
        """
        Delete a data source.
        
        Args:
            source_id: Data source ID
            
        Returns:
            True if the data source was deleted, False if not found.
        """
        if source_id in self.data_sources:
            del self.data_sources[source_id]
            return True
        return False
    
    def get_data_preview(self, source_id: str, max_rows: int = 10) -> Tuple[List[str], List[List[Any]]]:
        """
        Get a preview of the data from a data source.
        
        Args:
            source_id: Data source ID
            max_rows: Maximum number of rows to return
            
        Returns:
            Tuple of (column names, data rows)
        """
        source = self.data_sources.get(source_id)
        if not source:
            return [], []
        
        if source.type == "CSV File":
            return self._preview_csv(source, max_rows)
        elif source.type == "JSON File":
            return self._preview_json(source, max_rows)
        else:
            return [], []
    
    def _preview_csv(self, source: UIDataSourceConfig, max_rows: int) -> Tuple[List[str], List[List[Any]]]:
        """
        Get a preview of CSV data.
        
        Args:
            source: Data source configuration
            max_rows: Maximum number of rows to return
            
        Returns:
            Tuple of (column names, data rows)
        """
        file_path = source.config_params.get("file_path", "")
        has_header = source.config_params.get("has_header", True)
        delimiter = source.config_params.get("delimiter", ",")
        
        if not os.path.exists(file_path):
            # Return dummy data for demonstration
            return ["Column1", "Column2", "Column3"], [
                ["Value1", "Value2", "Value3"],
                ["Value4", "Value5", "Value6"]
            ]
        
        try:
            with open(file_path, 'r', newline='') as f:
                reader = csv.reader(f, delimiter=delimiter)
                
                if has_header:
                    headers = next(reader)
                else:
                    # Generate column names if no header
                    first_row = next(reader)
                    headers = [f"Column{i+1}" for i in range(len(first_row))]
                    # Reset reader to include first row in data
                    f.seek(0)
                    if has_header:
                        next(reader)  # Skip header again
                
                rows = []
                for i, row in enumerate(reader):
                    if i >= max_rows:
                        break
                    rows.append(row)
                
                return headers, rows
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return [], []
    
    def _preview_json(self, source: UIDataSourceConfig, max_rows: int) -> Tuple[List[str], List[List[Any]]]:
        """
        Get a preview of JSON data.
        
        Args:
            source: Data source configuration
            max_rows: Maximum number of rows to return
            
        Returns:
            Tuple of (column names, data rows)
        """
        file_path = source.config_params.get("file_path", "")
        root_element = source.config_params.get("root_element", "")
        
        if not os.path.exists(file_path):
            # Return dummy data for demonstration
            return ["id", "name", "value"], [
                ["1", "Item 1", "100"],
                ["2", "Item 2", "200"]
            ]
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Navigate to root element if specified
            if root_element:
                for part in root_element.split('.'):
                    if part in data:
                        data = data[part]
            
            # Ensure data is a list
            if not isinstance(data, list):
                return [], []
            
            if not data:
                return [], []
            
            # Get column names from first item
            first_item = data[0]
            if isinstance(first_item, dict):
                headers = list(first_item.keys())
            else:
                return [], []
            
            # Extract rows
            rows = []
            for i, item in enumerate(data):
                if i >= max_rows:
                    break
                
                if isinstance(item, dict):
                    row = [item.get(header, "") for header in headers]
                    rows.append(row)
            
            return headers, rows
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return [], []
