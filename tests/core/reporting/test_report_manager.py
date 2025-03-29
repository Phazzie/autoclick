"""
Tests for the report manager.
"""
import os
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.reporting.report_manager import ReportManager
from src.core.reporting.report_interface import ReportInterface
from src.core.reporting.execution_report import ExecutionReport


class TestReportManager(unittest.TestCase):
    """
    Test cases for the ReportManager class.
    """
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary report directory
        self.test_report_dir = "test_reports"
        self.report_manager = ReportManager(report_dir=self.test_report_dir)
        
        # Create a mock data source
        self.mock_source = MagicMock()
        self.mock_source.id = "test-workflow-123"
        self.mock_source.status = "completed"
        self.mock_source.results = [
            {
                "action_id": "action-1",
                "action_type": "click",
                "description": "Click button",
                "success": True,
                "message": "Action completed successfully",
                "execution_time_ms": 100
            },
            {
                "action_id": "action-2",
                "action_type": "input",
                "description": "Enter text",
                "success": True,
                "message": "Action completed successfully",
                "execution_time_ms": 50
            }
        ]
        
        # Create mock statistics
        self.mock_source.statistics = MagicMock()
        self.mock_source.statistics.total_duration_ms = 150
        self.mock_source.statistics.action_durations = {
            "action-1": 100,
            "action-2": 50
        }
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test report directory and files
        if os.path.exists(self.test_report_dir):
            for file in os.listdir(self.test_report_dir):
                os.remove(os.path.join(self.test_report_dir, file))
            os.rmdir(self.test_report_dir)
    
    def test_create_report(self):
        """Test creating a report."""
        # Create a report
        report = self.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        # Verify report was created and added to the manager
        self.assertIsInstance(report, ReportInterface)
        self.assertEqual(len(self.report_manager.reports), 1)
        
        # Verify report metadata
        metadata = report.get_metadata()
        self.assertEqual(metadata["report_type"], "execution")
        self.assertEqual(metadata["title"], "Test Execution Report")
    
    def test_save_report(self):
        """Test saving a report to disk."""
        # Create a report
        report = self.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        # Save the report
        file_path = self.report_manager.save_report(
            report=report,
            format_type="json",
            filename="test_report.json"
        )
        
        # Verify file was created
        self.assertTrue(os.path.exists(file_path))
        
        # Verify file content
        with open(file_path, 'r') as f:
            content = f.read()
            self.assertIn("Test Execution Report", content)
            self.assertIn("execution", content)
    
    def test_get_reports(self):
        """Test getting reports by type."""
        # Create reports of different types
        execution_report = self.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        test_case_report = self.report_manager.create_report(
            report_type="test_case",
            source=self.mock_source,
            title="Test Case Report"
        )
        
        # Get all reports
        all_reports = self.report_manager.get_reports()
        self.assertEqual(len(all_reports), 2)
        
        # Get reports by type
        execution_reports = self.report_manager.get_reports(report_type="execution")
        self.assertEqual(len(execution_reports), 1)
        self.assertEqual(execution_reports[0], execution_report)
        
        test_case_reports = self.report_manager.get_reports(report_type="test_case")
        self.assertEqual(len(test_case_reports), 1)
        self.assertEqual(test_case_reports[0], test_case_report)
    
    def test_clear_reports(self):
        """Test clearing reports."""
        # Create some reports
        self.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        self.report_manager.create_report(
            report_type="test_case",
            source=self.mock_source,
            title="Test Case Report"
        )
        
        # Verify reports were created
        self.assertEqual(len(self.report_manager.reports), 2)
        
        # Clear reports
        self.report_manager.clear_reports()
        
        # Verify reports were cleared
        self.assertEqual(len(self.report_manager.reports), 0)


if __name__ == "__main__":
    unittest.main()
