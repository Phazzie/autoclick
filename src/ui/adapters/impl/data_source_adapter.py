"""
Data source adapter implementation.

This module provides a concrete implementation of the data source adapter interface.
"""
from typing import List, Dict, Any, Optional

from src.core.data.data_source_manager import DataSourceManager
from src.ui.adapters.base.base_data_source_adapter import BaseDataSourceAdapter


class DataSourceAdapter(BaseDataSourceAdapter):
    """Concrete implementation of data source adapter."""
    
    def __init__(self, data_source_manager: Optional[DataSourceManager] = None):
        """
        Initialize the adapter with a DataSourceManager instance.
        
        Args:
            data_source_manager: Optional data source manager to use
        """
        self._data_source_manager = data_source_manager or DataSourceManager()
    
    def get_data_source_types(self) -> List[Dict[str, Any]]:
        """
        Get all available data source types.
        
        Returns:
            List of data source types with metadata
        """
        # Get all data source types from the manager
        data_source_types = self._data_source_manager.get_data_source_types()
        
        # Convert to UI format
        return [self._get_data_source_type_metadata(data_source_type) for data_source_type in data_source_types]
    
    def get_all_data_sources(self) -> List[Dict[str, Any]]:
        """
        Get all data sources.
        
        Returns:
            List of data sources in the UI-expected format
        """
        # Get all data sources from the manager
        data_sources = self._data_source_manager.get_all_data_sources()
        
        # Convert to UI format
        return [self._convert_data_source_to_ui_format(data_source) for data_source in data_sources]
    
    def get_data_source(self, data_source_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a data source by ID.
        
        Args:
            data_source_id: Data source ID
            
        Returns:
            Data source in the UI-expected format, or None if not found
        """
        # Get the data source from the manager
        data_source = self._data_source_manager.get_data_source(data_source_id)
        
        # Return None if not found
        if data_source is None:
            return None
        
        # Convert to UI format
        return self._convert_data_source_to_ui_format(data_source)
    
    def create_data_source(self, data_source_type: str, data_source_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a data source.
        
        Args:
            data_source_type: Data source type
            data_source_data: Data source data
            
        Returns:
            Created data source in the UI-expected format
            
        Raises:
            ValueError: If the data source data is invalid
        """
        try:
            # Create the data source
            data_source = self._data_source_manager.create_data_source(data_source_type, data_source_data)
            
            # Convert to UI format
            return self._convert_data_source_to_ui_format(data_source)
        except Exception as e:
            raise ValueError(f"Error creating data source: {str(e)}")
    
    def update_data_source(self, data_source_id: str, data_source_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a data source.
        
        Args:
            data_source_id: Data source ID
            data_source_data: Data source data
            
        Returns:
            Updated data source in the UI-expected format, or None if not found
            
        Raises:
            ValueError: If the data source data is invalid
        """
        try:
            # Update the data source
            data_source = self._data_source_manager.update_data_source(data_source_id, data_source_data)
            
            # Return None if not found
            if data_source is None:
                return None
            
            # Convert to UI format
            return self._convert_data_source_to_ui_format(data_source)
        except Exception as e:
            raise ValueError(f"Error updating data source: {str(e)}")
    
    def delete_data_source(self, data_source_id: str) -> bool:
        """
        Delete a data source.
        
        Args:
            data_source_id: Data source ID
            
        Returns:
            True if the data source was deleted, False if not found
        """
        try:
            # Delete the data source
            return self._data_source_manager.delete_data_source(data_source_id)
        except Exception as e:
            raise ValueError(f"Error deleting data source: {str(e)}")
    
    def get_data_source_schema(self, data_source_id: str) -> Dict[str, Any]:
        """
        Get the schema for a data source.
        
        Args:
            data_source_id: Data source ID
            
        Returns:
            Schema for the data source
            
        Raises:
            ValueError: If the data source is not found
        """
        try:
            # Get the data source
            data_source = self._data_source_manager.get_data_source(data_source_id)
            
            # Raise error if not found
            if data_source is None:
                raise ValueError(f"Data source not found: {data_source_id}")
            
            # Get the schema
            schema = data_source.get_schema()
            
            # Convert to UI format if needed
            return schema
        except Exception as e:
            raise ValueError(f"Error getting data source schema: {str(e)}")
    
    def query_data_source(self, data_source_id: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query a data source.
        
        Args:
            data_source_id: Data source ID
            query: Query parameters
            
        Returns:
            Query results
            
        Raises:
            ValueError: If the data source is not found or the query is invalid
        """
        try:
            # Get the data source
            data_source = self._data_source_manager.get_data_source(data_source_id)
            
            # Raise error if not found
            if data_source is None:
                raise ValueError(f"Data source not found: {data_source_id}")
            
            # Execute the query
            results = data_source.query(query)
            
            # Convert to UI format if needed
            return results
        except Exception as e:
            raise ValueError(f"Error querying data source: {str(e)}")
    
    def _get_data_source_type_metadata(self, data_source_type: str) -> Dict[str, Any]:
        """
        Get metadata for a data source type.
        
        Args:
            data_source_type: Data source type
            
        Returns:
            Data source type metadata
        """
        # Define metadata for known data source types
        metadata = {
            "csv": {
                "id": "csv",
                "name": "CSV File",
                "description": "Data from a CSV file",
                "icon": "file-csv",
                "category": "file"
            },
            "json": {
                "id": "json",
                "name": "JSON File",
                "description": "Data from a JSON file",
                "icon": "file-json",
                "category": "file"
            },
            "excel": {
                "id": "excel",
                "name": "Excel File",
                "description": "Data from an Excel file",
                "icon": "file-excel",
                "category": "file"
            },
            "database": {
                "id": "database",
                "name": "Database",
                "description": "Data from a database",
                "icon": "database",
                "category": "database"
            },
            "api": {
                "id": "api",
                "name": "API",
                "description": "Data from an API",
                "icon": "api",
                "category": "web"
            }
        }
        
        # Return metadata for the data source type, or a default if not found
        return metadata.get(data_source_type, {
            "id": data_source_type,
            "name": data_source_type.capitalize(),
            "description": f"{data_source_type.capitalize()} data source",
            "icon": "data-source",
            "category": "other"
        })
    
    def _convert_data_source_to_ui_format(self, data_source: Any) -> Dict[str, Any]:
        """
        Convert a data source to UI format.
        
        Args:
            data_source: Data source object
            
        Returns:
            Data source in UI format
        """
        return {
            "id": data_source.id,
            "name": data_source.name,
            "type": data_source.type,
            "description": data_source.description,
            "config": data_source.config,
            "status": data_source.status,
            "createdAt": data_source.created_at,
            "updatedAt": data_source.updated_at
        }
