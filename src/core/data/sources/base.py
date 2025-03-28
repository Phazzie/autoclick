"""Base data source interface"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Iterator, Optional


class DataSource(ABC):
    """
    Interface for data sources
    
    A data source provides access to a collection of data records
    that can be used for data-driven testing.
    """
    
    @abstractmethod
    def open(self) -> None:
        """
        Open the data source
        
        This method should be called before accessing any data.
        It initializes the data source and prepares it for reading.
        """
        pass
        
    @abstractmethod
    def close(self) -> None:
        """
        Close the data source
        
        This method should be called after all data has been read.
        It releases any resources used by the data source.
        """
        pass
        
    @abstractmethod
    def get_field_names(self) -> List[str]:
        """
        Get the names of all fields in the data source
        
        Returns:
            List of field names
        """
        pass
        
    @abstractmethod
    def get_record_count(self) -> int:
        """
        Get the total number of records in the data source
        
        Returns:
            Number of records
        """
        pass
        
    @abstractmethod
    def get_records(self) -> Iterator[Dict[str, Any]]:
        """
        Get all records from the data source
        
        Returns:
            Iterator over records, where each record is a dictionary
            mapping field names to values
        """
        pass
        
    @abstractmethod
    def get_record(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific record by index
        
        Args:
            index: Zero-based index of the record to get
            
        Returns:
            Record as a dictionary, or None if the index is out of range
        """
        pass
        
    def __enter__(self) -> 'DataSource':
        """
        Enter context manager
        
        Returns:
            Self
        """
        self.open()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit context manager
        
        Args:
            exc_type: Exception type, if an exception was raised
            exc_val: Exception value, if an exception was raised
            exc_tb: Exception traceback, if an exception was raised
        """
        self.close()


class DataSourceFactory:
    """Factory for creating data sources"""
    
    @staticmethod
    def create_csv_source(file_path: str, delimiter: str = ',', has_header: bool = True) -> DataSource:
        """
        Create a CSV data source
        
        Args:
            file_path: Path to the CSV file
            delimiter: Field delimiter
            has_header: Whether the CSV file has a header row
            
        Returns:
            CSV data source
        """
        from src.core.data.sources.csv_source import CsvDataSource
        return CsvDataSource(file_path, delimiter, has_header)
        
    @staticmethod
    def create_json_source(file_path: str, records_path: str = None) -> DataSource:
        """
        Create a JSON data source
        
        Args:
            file_path: Path to the JSON file
            records_path: JSON path to the records array (e.g., "data.records")
            
        Returns:
            JSON data source
        """
        from src.core.data.sources.json_source import JsonDataSource
        return JsonDataSource(file_path, records_path)
        
    @staticmethod
    def create_memory_source(records: List[Dict[str, Any]]) -> DataSource:
        """
        Create an in-memory data source
        
        Args:
            records: List of records
            
        Returns:
            In-memory data source
        """
        from src.core.data.sources.memory_source import MemoryDataSource
        return MemoryDataSource(records)
