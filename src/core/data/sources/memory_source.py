"""In-memory data source implementation"""
from typing import Dict, Any, List, Iterator, Optional
import logging

from src.core.data.sources.base import DataSource


class MemoryDataSource(DataSource):
    """
    Data source that reads from an in-memory list of records
    
    This data source is useful for testing or for cases where
    the data is generated programmatically.
    """
    
    def __init__(self, records: List[Dict[str, Any]]):
        """
        Initialize the in-memory data source
        
        Args:
            records: List of records, where each record is a dictionary
        """
        self.records = records
        self.field_names = []
        self.is_open = False
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def open(self) -> None:
        """
        Open the data source
        
        For an in-memory data source, this just extracts the field names
        from the first record.
        """
        if self.records:
            first_record = self.records[0]
            if isinstance(first_record, dict):
                self.field_names = list(first_record.keys())
                
        self.is_open = True
        self.logger.info(f"Opened in-memory data source with {len(self.records)} records")
            
    def close(self) -> None:
        """Close the data source"""
        self.is_open = False
            
    def get_field_names(self) -> List[str]:
        """
        Get the names of all fields in the data source
        
        Returns:
            List of field names
        """
        return self.field_names.copy()
        
    def get_record_count(self) -> int:
        """
        Get the total number of records in the data source
        
        Returns:
            Number of records
        """
        return len(self.records)
        
    def get_records(self) -> Iterator[Dict[str, Any]]:
        """
        Get all records from the data source
        
        Returns:
            Iterator over records
        """
        for record in self.records:
            yield record.copy()
            
    def get_record(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific record by index
        
        Args:
            index: Zero-based index of the record to get
            
        Returns:
            Record as a dictionary, or None if the index is out of range
        """
        if 0 <= index < len(self.records):
            return self.records[index].copy()
        return None
