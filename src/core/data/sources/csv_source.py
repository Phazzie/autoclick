"""CSV data source implementation"""
import csv
from typing import Dict, Any, List, Iterator, Optional
import logging

from src.core.data.sources.base import DataSource


class CsvDataSource(DataSource):
    """
    Data source that reads from a CSV file
    
    This data source reads records from a CSV file, where each row
    represents a record and columns represent fields.
    """
    
    def __init__(self, file_path: str, delimiter: str = ',', has_header: bool = True):
        """
        Initialize the CSV data source
        
        Args:
            file_path: Path to the CSV file
            delimiter: Field delimiter
            has_header: Whether the CSV file has a header row
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.has_header = has_header
        self.file = None
        self.reader = None
        self.field_names = []
        self.records = []
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def open(self) -> None:
        """
        Open the CSV file and read its contents
        
        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If the file cannot be read
        """
        try:
            self.file = open(self.file_path, 'r', newline='')
            self.reader = csv.reader(self.file, delimiter=self.delimiter)
            
            # Read the header row if present
            if self.has_header:
                self.field_names = next(self.reader)
            else:
                # Generate field names (Field1, Field2, etc.)
                first_row = next(self.reader)
                self.field_names = [f"Field{i+1}" for i in range(len(first_row))]
                # Reset the file to read all rows
                self.file.seek(0)
                self.reader = csv.reader(self.file, delimiter=self.delimiter)
                # Skip the header row if we just read it
                if self.has_header:
                    next(self.reader)
                    
            # Read all records into memory
            self.records = []
            for row in self.reader:
                record = {}
                for i, value in enumerate(row):
                    if i < len(self.field_names):
                        record[self.field_names[i]] = value
                self.records.append(record)
                
            self.logger.info(f"Loaded {len(self.records)} records from {self.file_path}")
            
        except (FileNotFoundError, IOError) as e:
            self.logger.error(f"Failed to open CSV file {self.file_path}: {str(e)}")
            raise
            
    def close(self) -> None:
        """Close the CSV file"""
        if self.file:
            self.file.close()
            self.file = None
            self.reader = None
            
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
