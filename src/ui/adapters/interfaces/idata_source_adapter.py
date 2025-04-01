"""
Data source adapter interface.

This module defines the interface for data source adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IDataSourceAdapter(ABC):
    """Interface for data source adapters."""
    
    @abstractmethod
    def get_data_source_types(self) -> List[Dict[str, Any]]:
        """
        Get all available data source types.
        
        Returns:
            List of data source types with metadata
        """
        pass
    
    @abstractmethod
    def get_all_data_sources(self) -> List[Dict[str, Any]]:
        """
        Get all data sources.
        
        Returns:
            List of data sources in the UI-expected format
        """
        pass
    
    @abstractmethod
    def get_data_source(self, data_source_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a data source by ID.
        
        Args:
            data_source_id: Data source ID
            
        Returns:
            Data source in the UI-expected format, or None if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_data_source(self, data_source_id: str) -> bool:
        """
        Delete a data source.
        
        Args:
            data_source_id: Data source ID
            
        Returns:
            True if the data source was deleted, False if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
