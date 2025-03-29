"""
Tests for the report service.
"""
import os
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any

from src.core.reporting.report_service import ReportService


class TestReportService(unittest.TestCase):
    """
    Test cases for the ReportService class.
    """
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary report directory
        self.test_report_dir = "test_reports"
        self.report_service = ReportService(report_dir=self.test_report_dir)
        
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
    
    def test_generate_report(self):
        """Test generating a report."""
        # Generate a report
        report_data = self.report_service.generate_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        # Verify report data
        self.assertIsInstance(report_data, dict)
        self.assertIn("metadata", report_data)
        self.assertIn("data", report_data)
        
        # Verify metadata
        metadata = report_data["metadata"]
        self.assertEqual(metadata["report_type"], "execution")
        self.assertEqual(metadata["title"], "Test Execution Report")
    
    def test_generate_and_save_report(self):
        """Test generating and saving a report."""
        # Generate and save a report
        report_data = self.report_service.generate_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report",
            save=True,
            format_type="json"
        )
        
        # Verify file path is included
        self.assertIn("file_path", report_data)
        file_path = report_data["file_path"]
        
        # Verify file exists
        self.assertTrue(os.path.exists(file_path))
        
        # Verify file content
        with open(file_path, 'r') as f:
            content = f.read()
            self.assertIn("Test Execution Report", content)
            self.assertIn("execution", content)
    
    def test_get_report_summary(self):
        """Test getting a report summary."""
        # Generate a report
        report = self.report_service.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        # Get summary
        summary = self.report_service.get_report_summary(report)
        
        # Verify summary
        self.assertIsInstance(summary, str)
        self.assertIn("Test Execution Report", summary)
        self.assertIn("Actions:", summary)
    
    def test_get_report_metrics(self):
        """Test getting report metrics."""
        # Generate a report
        report = self.report_service.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        # Get metrics
        metrics = self.report_service.get_report_metrics(report)
        
        # Verify metrics
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics["title"], "Test Execution Report")
        self.assertEqual(metrics["type"], "execution")
    
    def test_save_all_reports(self):
        """Test saving all reports."""
        # Create multiple reports
        self.report_service.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report 1"
        )
        
        self.report_service.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report 2"
        )
        
        # Save all reports
        file_paths = self.report_service.save_all_reports(format_type="json")
        
        # Verify files were created
        self.assertEqual(len(file_paths), 2)
        for file_path in file_paths:
            self.assertTrue(os.path.exists(file_path))
    
    def test_clear_all(self):
        """Test clearing all reports."""
        # Create reports
        self.report_service.report_manager.create_report(
            report_type="execution",
            source=self.mock_source,
            title="Test Execution Report"
        )
        
        # Save reports
        self.report_service.save_all_reports()
        
        # Verify reports exist
        self.assertEqual(len(self.report_service.report_manager.get_reports()), 1)
        self.assertTrue(os.path.exists(self.test_report_dir))
        self.assertTrue(len(os.listdir(self.test_report_dir)) > 0)
        
        # Clear all
        self.report_service.clear_all()
        
        # Verify reports are cleared
        self.assertEqual(len(self.report_service.report_manager.get_reports()), 0)
        self.assertEqual(len(os.listdir(self.test_report_dir)), 0)


if __name__ == "__main__":
    unittest.main()
