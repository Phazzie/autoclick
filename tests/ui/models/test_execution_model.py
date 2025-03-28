"""Tests for the ExecutionModel class"""
import unittest
from src.ui.models.execution_model import ExecutionModel


class TestExecutionModel(unittest.TestCase):
    """Test cases for the ExecutionModel class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = ExecutionModel()
        self.test_workflow = {
            "name": "Test Workflow",
            "actions": [
                {
                    "type": "click",
                    "selector": "#test-button",
                    "description": "Click test button"
                }
            ]
        }

    def test_start_execution(self) -> None:
        """Test starting execution"""
        # Start execution
        self.model.start_execution(self.test_workflow)
        
        # Verify execution state
        self.assertTrue(self.model.is_execution_running())
        
        # Verify log entries
        log_entries = self.model.get_log_entries()
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0]["level"], "info")
        self.assertEqual(log_entries[0]["message"], "Execution started")

    def test_stop_execution(self) -> None:
        """Test stopping execution"""
        # Start execution
        self.model.start_execution(self.test_workflow)
        
        # Stop execution
        self.model.stop_execution()
        
        # Verify execution state
        self.assertFalse(self.model.is_execution_running())
        
        # Verify log entries
        log_entries = self.model.get_log_entries()
        self.assertEqual(len(log_entries), 2)
        self.assertEqual(log_entries[1]["level"], "info")
        self.assertEqual(log_entries[1]["message"], "Execution stopped")

    def test_add_log_entry(self) -> None:
        """Test adding log entries"""
        # Add log entries
        self.model.add_log_entry("info", "Info message")
        self.model.add_log_entry("warning", "Warning message")
        self.model.add_log_entry("error", "Error message")
        
        # Verify log entries
        log_entries = self.model.get_log_entries()
        self.assertEqual(len(log_entries), 3)
        self.assertEqual(log_entries[0]["level"], "info")
        self.assertEqual(log_entries[0]["message"], "Info message")
        self.assertEqual(log_entries[1]["level"], "warning")
        self.assertEqual(log_entries[1]["message"], "Warning message")
        self.assertEqual(log_entries[2]["level"], "error")
        self.assertEqual(log_entries[2]["message"], "Error message")

    def test_get_log_entries(self) -> None:
        """Test getting log entries"""
        # Add log entries
        self.model.add_log_entry("info", "Test message")
        
        # Get log entries
        log_entries = self.model.get_log_entries()
        
        # Verify log entries
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0]["level"], "info")
        self.assertEqual(log_entries[0]["message"], "Test message")
        
        # Verify that modifying the returned list doesn't affect the original
        log_entries.pop(0)
        self.assertEqual(len(self.model._log_entries), 1)

    def test_is_execution_running(self) -> None:
        """Test checking if execution is running"""
        # Verify initial state
        self.assertFalse(self.model.is_execution_running())
        
        # Start execution
        self.model.start_execution(self.test_workflow)
        
        # Verify running state
        self.assertTrue(self.model.is_execution_running())
        
        # Stop execution
        self.model.stop_execution()
        
        # Verify stopped state
        self.assertFalse(self.model.is_execution_running())

    def test_set_option(self) -> None:
        """Test setting options"""
        # Set options
        self.model.set_option("browser_type", "firefox")
        self.model.set_option("headless", True)
        self.model.set_option("timeout", 60)
        
        # Verify options
        options = self.model.get_options()
        self.assertEqual(options["browser_type"], "firefox")
        self.assertEqual(options["headless"], True)
        self.assertEqual(options["timeout"], 60)

    def test_get_options(self) -> None:
        """Test getting options"""
        # Get options
        options = self.model.get_options()
        
        # Verify default options
        self.assertEqual(options["browser_type"], "chrome")
        self.assertEqual(options["headless"], False)
        self.assertEqual(options["timeout"], 30)
        
        # Verify that modifying the returned dictionary doesn't affect the original
        options["browser_type"] = "firefox"
        self.assertEqual(self.model._options["browser_type"], "chrome")


if __name__ == "__main__":
    unittest.main()
