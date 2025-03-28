"""JSON data source implementation"""
import json
from typing import Dict, Any, List, Iterator, Optional
import logging

from src.core.data.sources.base import DataSource


class JsonDataSource(DataSource):
    """
    Data source that reads from a JSON file
    
    This data source reads records from a JSON file, where the file
    contains an array of objects or a nested structure containing
    an array of objects.
    """
    
    def __init__(self, file_path: str, records_path: Optional[str] = None):
        """
        Initialize the JSON data source
        
        Args:
            file_path: Path to the JSON file
            records_path: JSON path to the records array (e.g., "data.records")
                          If None, the file is expected to contain an array of records
        """
        self.file_path = file_path
        self.records_path = records_path
        self.records = []
        self.field_names = []
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def open(self) -> None:
        """
        Open the JSON file and read its contents
        
        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If the file cannot be read
            json.JSONDecodeError: If the file contains invalid JSON
            ValueError: If the records cannot be found at the specified path
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                
            # Get the records from the specified path
            if self.records_path:
                records = self._get_nested_value(data, self.records_path)
                if records is None:
                    raise ValueError(f"Records not found at path '{self.records_path}'")
            else:
                records = data
                
            # Ensure records is a list
            if not isinstance(records, list):
                raise ValueError("Records must be an array")
                
            # Store the records
            self.records = records
            
            # Extract field names from the first record
            if self.records:
                first_record = self.records[0]
                if isinstance(first_record, dict):
                    self.field_names = list(first_record.keys())
                    
            self.logger.info(f"Loaded {len(self.records)} records from {self.file_path}")
            
        except (FileNotFoundError, IOError, json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"Failed to open JSON file {self.file_path}: {str(e)}")
            raise
            
    def _get_nested_value(self, data: Any, path: str) -> Any:
        """
        Get a nested value from a dictionary using a dot-separated path
        
        Args:
            data: Dictionary to get the value from
            path: Dot-separated path to the value (e.g., "data.records")
            
        Returns:
            Value at the specified path, or None if not found
        """
        parts = path.split('.')
        current = data
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
                
        return current
            
    def close(self) -> None:
        """Close the JSON file (no-op for JSON)"""
        pass
            
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
            if isinstance(record, dict):
                yield record.copy()
            else:
                # If the record is not a dictionary, create one with a single field
                yield {"value": record}
            
    def get_record(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific record by index
        
        Args:
            index: Zero-based index of the record to get
            
        Returns:
            Record as a dictionary, or None if the index is out of range
        """
        if 0 <= index < len(self.records):
            record = self.records[index]
            if isinstance(record, dict):
                return record.copy()
            else:
                # If the record is not a dictionary, create one with a single field
                return {"value": record}
        return None
