"""Tests for data sources"""
import unittest
import os
import tempfile
import csv
import json
from typing import Dict, Any, List

from src.core.data.sources.base import DataSource, DataSourceFactory
from src.core.data.sources.csv_source import CsvDataSource
from src.core.data.sources.json_source import JsonDataSource
from src.core.data.sources.memory_source import MemoryDataSource


class TestCsvDataSource(unittest.TestCase):
    """Test cases for the CSV data source"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary CSV file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.temp_file.close()
        
        # Write test data to the file
        with open(self.temp_file.name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "age", "city"])
            writer.writerow(["Alice", "30", "New York"])
            writer.writerow(["Bob", "25", "Los Angeles"])
            writer.writerow(["Charlie", "35", "Chicago"])
            
    def tearDown(self):
        """Clean up test environment"""
        # Remove the temporary file
        os.unlink(self.temp_file.name)
        
    def test_open_close(self):
        """Test opening and closing the data source"""
        # Create a data source
        source = CsvDataSource(self.temp_file.name)
        
        # Open the data source
        source.open()
        
        # Check that the file was opened
        self.assertIsNotNone(source.file)
        self.assertIsNotNone(source.reader)
        
        # Close the data source
        source.close()
        
        # Check that the file was closed
        self.assertIsNone(source.file)
        self.assertIsNone(source.reader)
        
    def test_get_field_names(self):
        """Test getting field names"""
        # Create a data source
        source = CsvDataSource(self.temp_file.name)
        
        # Open the data source
        source.open()
        
        # Check the field names
        self.assertEqual(source.get_field_names(), ["name", "age", "city"])
        
        # Close the data source
        source.close()
        
    def test_get_record_count(self):
        """Test getting the record count"""
        # Create a data source
        source = CsvDataSource(self.temp_file.name)
        
        # Open the data source
        source.open()
        
        # Check the record count
        self.assertEqual(source.get_record_count(), 3)
        
        # Close the data source
        source.close()
        
    def test_get_records(self):
        """Test getting all records"""
        # Create a data source
        source = CsvDataSource(self.temp_file.name)
        
        # Open the data source
        source.open()
        
        # Get all records
        records = list(source.get_records())
        
        # Check the records
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["name"], "Alice")
        self.assertEqual(records[0]["age"], "30")
        self.assertEqual(records[0]["city"], "New York")
        
        # Close the data source
        source.close()
        
    def test_get_record(self):
        """Test getting a specific record"""
        # Create a data source
        source = CsvDataSource(self.temp_file.name)
        
        # Open the data source
        source.open()
        
        # Get a specific record
        record = source.get_record(1)
        
        # Check the record
        self.assertEqual(record["name"], "Bob")
        self.assertEqual(record["age"], "25")
        self.assertEqual(record["city"], "Los Angeles")
        
        # Get a non-existent record
        record = source.get_record(10)
        
        # Check that the record is None
        self.assertIsNone(record)
        
        # Close the data source
        source.close()
        
    def test_context_manager(self):
        """Test using the data source as a context manager"""
        # Use the data source as a context manager
        with CsvDataSource(self.temp_file.name) as source:
            # Check that the file was opened
            self.assertIsNotNone(source.file)
            self.assertIsNotNone(source.reader)
            
            # Get a record
            record = source.get_record(0)
            
            # Check the record
            self.assertEqual(record["name"], "Alice")
            
        # Check that the file was closed
        self.assertIsNone(source.file)
        self.assertIsNone(source.reader)


class TestJsonDataSource(unittest.TestCase):
    """Test cases for the JSON data source"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary JSON file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        
        # Write test data to the file
        data = {
            "people": [
                {"name": "Alice", "age": 30, "city": "New York"},
                {"name": "Bob", "age": 25, "city": "Los Angeles"},
                {"name": "Charlie", "age": 35, "city": "Chicago"}
            ]
        }
        
        with open(self.temp_file.name, 'w') as file:
            json.dump(data, file)
            
    def tearDown(self):
        """Clean up test environment"""
        # Remove the temporary file
        os.unlink(self.temp_file.name)
        
    def test_open_close(self):
        """Test opening and closing the data source"""
        # Create a data source
        source = JsonDataSource(self.temp_file.name, "people")
        
        # Open the data source
        source.open()
        
        # Check that the records were loaded
        self.assertEqual(len(source.records), 3)
        
        # Close the data source
        source.close()
        
    def test_get_field_names(self):
        """Test getting field names"""
        # Create a data source
        source = JsonDataSource(self.temp_file.name, "people")
        
        # Open the data source
        source.open()
        
        # Check the field names
        self.assertEqual(set(source.get_field_names()), {"name", "age", "city"})
        
        # Close the data source
        source.close()
        
    def test_get_record_count(self):
        """Test getting the record count"""
        # Create a data source
        source = JsonDataSource(self.temp_file.name, "people")
        
        # Open the data source
        source.open()
        
        # Check the record count
        self.assertEqual(source.get_record_count(), 3)
        
        # Close the data source
        source.close()
        
    def test_get_records(self):
        """Test getting all records"""
        # Create a data source
        source = JsonDataSource(self.temp_file.name, "people")
        
        # Open the data source
        source.open()
        
        # Get all records
        records = list(source.get_records())
        
        # Check the records
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["name"], "Alice")
        self.assertEqual(records[0]["age"], 30)
        self.assertEqual(records[0]["city"], "New York")
        
        # Close the data source
        source.close()
        
    def test_get_record(self):
        """Test getting a specific record"""
        # Create a data source
        source = JsonDataSource(self.temp_file.name, "people")
        
        # Open the data source
        source.open()
        
        # Get a specific record
        record = source.get_record(1)
        
        # Check the record
        self.assertEqual(record["name"], "Bob")
        self.assertEqual(record["age"], 25)
        self.assertEqual(record["city"], "Los Angeles")
        
        # Get a non-existent record
        record = source.get_record(10)
        
        # Check that the record is None
        self.assertIsNone(record)
        
        # Close the data source
        source.close()
        
    def test_context_manager(self):
        """Test using the data source as a context manager"""
        # Use the data source as a context manager
        with JsonDataSource(self.temp_file.name, "people") as source:
            # Get a record
            record = source.get_record(0)
            
            # Check the record
            self.assertEqual(record["name"], "Alice")


class TestMemoryDataSource(unittest.TestCase):
    """Test cases for the in-memory data source"""
    
    def setUp(self):
        """Set up test environment"""
        # Create test data
        self.data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Los Angeles"},
            {"name": "Charlie", "age": 35, "city": "Chicago"}
        ]
        
    def test_open_close(self):
        """Test opening and closing the data source"""
        # Create a data source
        source = MemoryDataSource(self.data)
        
        # Open the data source
        source.open()
        
        # Check that the data source is open
        self.assertTrue(source.is_open)
        
        # Close the data source
        source.close()
        
        # Check that the data source is closed
        self.assertFalse(source.is_open)
        
    def test_get_field_names(self):
        """Test getting field names"""
        # Create a data source
        source = MemoryDataSource(self.data)
        
        # Open the data source
        source.open()
        
        # Check the field names
        self.assertEqual(set(source.get_field_names()), {"name", "age", "city"})
        
        # Close the data source
        source.close()
        
    def test_get_record_count(self):
        """Test getting the record count"""
        # Create a data source
        source = MemoryDataSource(self.data)
        
        # Open the data source
        source.open()
        
        # Check the record count
        self.assertEqual(source.get_record_count(), 3)
        
        # Close the data source
        source.close()
        
    def test_get_records(self):
        """Test getting all records"""
        # Create a data source
        source = MemoryDataSource(self.data)
        
        # Open the data source
        source.open()
        
        # Get all records
        records = list(source.get_records())
        
        # Check the records
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["name"], "Alice")
        self.assertEqual(records[0]["age"], 30)
        self.assertEqual(records[0]["city"], "New York")
        
        # Close the data source
        source.close()
        
    def test_get_record(self):
        """Test getting a specific record"""
        # Create a data source
        source = MemoryDataSource(self.data)
        
        # Open the data source
        source.open()
        
        # Get a specific record
        record = source.get_record(1)
        
        # Check the record
        self.assertEqual(record["name"], "Bob")
        self.assertEqual(record["age"], 25)
        self.assertEqual(record["city"], "Los Angeles")
        
        # Get a non-existent record
        record = source.get_record(10)
        
        # Check that the record is None
        self.assertIsNone(record)
        
        # Close the data source
        source.close()
        
    def test_context_manager(self):
        """Test using the data source as a context manager"""
        # Use the data source as a context manager
        with MemoryDataSource(self.data) as source:
            # Check that the data source is open
            self.assertTrue(source.is_open)
            
            # Get a record
            record = source.get_record(0)
            
            # Check the record
            self.assertEqual(record["name"], "Alice")
            
        # Check that the data source is closed
        self.assertFalse(source.is_open)


class TestDataSourceFactory(unittest.TestCase):
    """Test cases for the data source factory"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary CSV file
        self.csv_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.csv_file.close()
        
        # Write test data to the CSV file
        with open(self.csv_file.name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "age", "city"])
            writer.writerow(["Alice", "30", "New York"])
            
        # Create a temporary JSON file
        self.json_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.json_file.close()
        
        # Write test data to the JSON file
        data = {"people": [{"name": "Alice", "age": 30, "city": "New York"}]}
        with open(self.json_file.name, 'w') as file:
            json.dump(data, file)
            
    def tearDown(self):
        """Clean up test environment"""
        # Remove the temporary files
        os.unlink(self.csv_file.name)
        os.unlink(self.json_file.name)
        
    def test_create_csv_source(self):
        """Test creating a CSV data source"""
        # Create a CSV data source
        source = DataSourceFactory.create_csv_source(self.csv_file.name)
        
        # Check the type
        self.assertIsInstance(source, CsvDataSource)
        
        # Open the data source
        source.open()
        
        # Check the field names
        self.assertEqual(source.get_field_names(), ["name", "age", "city"])
        
        # Close the data source
        source.close()
        
    def test_create_json_source(self):
        """Test creating a JSON data source"""
        # Create a JSON data source
        source = DataSourceFactory.create_json_source(self.json_file.name, "people")
        
        # Check the type
        self.assertIsInstance(source, JsonDataSource)
        
        # Open the data source
        source.open()
        
        # Check the field names
        self.assertEqual(set(source.get_field_names()), {"name", "age", "city"})
        
        # Close the data source
        source.close()
        
    def test_create_memory_source(self):
        """Test creating an in-memory data source"""
        # Create test data
        data = [{"name": "Alice", "age": 30, "city": "New York"}]
        
        # Create an in-memory data source
        source = DataSourceFactory.create_memory_source(data)
        
        # Check the type
        self.assertIsInstance(source, MemoryDataSource)
        
        # Open the data source
        source.open()
        
        # Check the field names
        self.assertEqual(set(source.get_field_names()), {"name", "age", "city"})
        
        # Close the data source
        source.close()


if __name__ == "__main__":
    unittest.main()
