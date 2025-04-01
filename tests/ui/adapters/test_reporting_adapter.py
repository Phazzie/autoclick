"""Tests for the ReportingAdapter class."""
import unittest
from unittest.mock import MagicMock, patch

from src.core.reporting.reporting_service import ReportingService
from src.ui.adapters.impl.reporting_adapter import ReportingAdapter


class TestReportingAdapter(unittest.TestCase):
    """Test cases for the ReportingAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_reporting_service = MagicMock(spec=ReportingService)
        self.adapter = ReportingAdapter(self.mock_reporting_service)
    
    def test_get_report_types(self):
        """Test getting report types."""
        # Arrange
        self.mock_reporting_service.get_report_types.return_value = [
            "workflow_summary",
            "execution_details",
            "error_report",
            "performance_metrics"
        ]
        
        # Act
        result = self.adapter.get_report_types()
        
        # Assert
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["id"], "workflow_summary")
        self.assertEqual(result[1]["id"], "execution_details")
        self.assertEqual(result[2]["id"], "error_report")
        self.assertEqual(result[3]["id"], "performance_metrics")
        
        # Verify service was called
        self.mock_reporting_service.get_report_types.assert_called_once()
    
    def test_get_all_reports(self):
        """Test getting all reports."""
        # Arrange
        mock_report1 = MagicMock()
        mock_report1.id = "report1"
        mock_report1.type = "workflow_summary"
        mock_report1.name = "Report 1"
        mock_report1.description = "Test report 1"
        mock_report1.config = {}
        mock_report1.created_at = "2023-01-01T00:00:00Z"
        mock_report1.updated_at = "2023-01-01T00:00:00Z"
        
        mock_report2 = MagicMock()
        mock_report2.id = "report2"
        mock_report2.type = "error_report"
        mock_report2.name = "Report 2"
        mock_report2.description = "Test report 2"
        mock_report2.config = {}
        mock_report2.created_at = "2023-01-01T00:00:00Z"
        mock_report2.updated_at = "2023-01-01T00:00:00Z"
        
        self.mock_reporting_service.get_all_reports.return_value = [mock_report1, mock_report2]
        
        # Act
        result = self.adapter.get_all_reports()
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "report1")
        self.assertEqual(result[0]["type"], "workflow_summary")
        self.assertEqual(result[1]["id"], "report2")
        self.assertEqual(result[1]["type"], "error_report")
        
        # Verify service was called
        self.mock_reporting_service.get_all_reports.assert_called_once()
    
    def test_get_report(self):
        """Test getting a report by ID."""
        # Arrange
        mock_report = MagicMock()
        mock_report.id = "report1"
        mock_report.type = "workflow_summary"
        mock_report.name = "Report 1"
        mock_report.description = "Test report 1"
        mock_report.config = {}
        mock_report.created_at = "2023-01-01T00:00:00Z"
        mock_report.updated_at = "2023-01-01T00:00:00Z"
        
        self.mock_reporting_service.get_report.return_value = mock_report
        
        # Act
        result = self.adapter.get_report("report1")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "report1")
        self.assertEqual(result["type"], "workflow_summary")
        
        # Verify service was called
        self.mock_reporting_service.get_report.assert_called_once_with("report1")
    
    def test_get_report_not_found(self):
        """Test getting a report that doesn't exist."""
        # Arrange
        self.mock_reporting_service.get_report.return_value = None
        
        # Act
        result = self.adapter.get_report("nonexistent")
        
        # Assert
        self.assertIsNone(result)
        
        # Verify service was called
        self.mock_reporting_service.get_report.assert_called_once_with("nonexistent")
    
    def test_create_report(self):
        """Test creating a report."""
        # Arrange
        report_type = "workflow_summary"
        report_data = {
            "name": "New Report",
            "description": "Test new report",
            "config": {
                "workflow_id": "workflow1"
            }
        }
        
        mock_report = MagicMock()
        mock_report.id = "new-report"
        mock_report.type = "workflow_summary"
        mock_report.name = "New Report"
        mock_report.description = "Test new report"
        mock_report.config = {"workflow_id": "workflow1"}
        mock_report.created_at = "2023-01-01T00:00:00Z"
        mock_report.updated_at = "2023-01-01T00:00:00Z"
        
        self.mock_reporting_service.create_report.return_value = mock_report
        
        # Act
        result = self.adapter.create_report(report_type, report_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "new-report")
        self.assertEqual(result["type"], "workflow_summary")
        
        # Verify service was called
        self.mock_reporting_service.create_report.assert_called_once_with(report_type, report_data)
    
    def test_create_report_error(self):
        """Test creating a report that raises an error."""
        # Arrange
        report_type = "workflow_summary"
        report_data = {
            "name": "New Report",
            "description": "Test new report",
            "config": {
                "workflow_id": "workflow1"
            }
        }
        
        self.mock_reporting_service.create_report.side_effect = Exception("Test error")
        
        # Act/Assert
        with self.assertRaises(ValueError) as context:
            self.adapter.create_report(report_type, report_data)
        
        # Verify error message
        self.assertIn("Error creating report", str(context.exception))
        
        # Verify service was called
        self.mock_reporting_service.create_report.assert_called_once_with(report_type, report_data)
    
    def test_update_report(self):
        """Test updating a report."""
        # Arrange
        report_id = "report1"
        report_data = {
            "name": "Updated Report",
            "description": "Test updated report",
            "config": {
                "workflow_id": "workflow1"
            }
        }
        
        mock_report = MagicMock()
        mock_report.id = "report1"
        mock_report.type = "workflow_summary"
        mock_report.name = "Updated Report"
        mock_report.description = "Test updated report"
        mock_report.config = {"workflow_id": "workflow1"}
        mock_report.created_at = "2023-01-01T00:00:00Z"
        mock_report.updated_at = "2023-01-02T00:00:00Z"
        
        self.mock_reporting_service.update_report.return_value = mock_report
        
        # Act
        result = self.adapter.update_report(report_id, report_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "report1")
        self.assertEqual(result["name"], "Updated Report")
        
        # Verify service was called
        self.mock_reporting_service.update_report.assert_called_once_with(report_id, report_data)
    
    def test_update_report_not_found(self):
        """Test updating a report that doesn't exist."""
        # Arrange
        report_id = "nonexistent"
        report_data = {
            "name": "Updated Report",
            "description": "Test updated report",
            "config": {
                "workflow_id": "workflow1"
            }
        }
        
        self.mock_reporting_service.update_report.return_value = None
        
        # Act
        result = self.adapter.update_report(report_id, report_data)
        
        # Assert
        self.assertIsNone(result)
        
        # Verify service was called
        self.mock_reporting_service.update_report.assert_called_once_with(report_id, report_data)
    
    def test_update_report_error(self):
        """Test updating a report that raises an error."""
        # Arrange
        report_id = "report1"
        report_data = {
            "name": "Updated Report",
            "description": "Test updated report",
            "config": {
                "workflow_id": "workflow1"
            }
        }
        
        self.mock_reporting_service.update_report.side_effect = Exception("Test error")
        
        # Act/Assert
        with self.assertRaises(ValueError) as context:
            self.adapter.update_report(report_id, report_data)
        
        # Verify error message
        self.assertIn("Error updating report", str(context.exception))
        
        # Verify service was called
        self.mock_reporting_service.update_report.assert_called_once_with(report_id, report_data)
    
    def test_delete_report(self):
        """Test deleting a report."""
        # Arrange
        self.mock_reporting_service.delete_report.return_value = True
        
        # Act
        result = self.adapter.delete_report("report1")
        
        # Assert
        self.assertTrue(result)
        
        # Verify service was called
        self.mock_reporting_service.delete_report.assert_called_once_with("report1")
    
    def test_delete_report_not_found(self):
        """Test deleting a report that doesn't exist."""
        # Arrange
        self.mock_reporting_service.delete_report.return_value = False
        
        # Act
        result = self.adapter.delete_report("nonexistent")
        
        # Assert
        self.assertFalse(result)
        
        # Verify service was called
        self.mock_reporting_service.delete_report.assert_called_once_with("nonexistent")
    
    def test_delete_report_error(self):
        """Test deleting a report that raises an error."""
        # Arrange
        self.mock_reporting_service.delete_report.side_effect = Exception("Test error")
        
        # Act/Assert
        with self.assertRaises(ValueError) as context:
            self.adapter.delete_report("report1")
        
        # Verify error message
        self.assertIn("Error deleting report", str(context.exception))
        
        # Verify service was called
        self.mock_reporting_service.delete_report.assert_called_once_with("report1")
    
    def test_generate_report(self):
        """Test generating a report."""
        # Arrange
        report_id = "report1"
        parameters = {"start_date": "2023-01-01", "end_date": "2023-01-31"}
        expected_result = {"data": [{"workflow": "workflow1", "executions": 10}]}
        
        self.mock_reporting_service.generate_report.return_value = expected_result
        
        # Act
        result = self.adapter.generate_report(report_id, parameters)
        
        # Assert
        self.assertEqual(result, expected_result)
        
        # Verify service was called
        self.mock_reporting_service.generate_report.assert_called_once_with(report_id, parameters)
    
    def test_generate_report_error(self):
        """Test generating a report that raises an error."""
        # Arrange
        report_id = "report1"
        parameters = {"start_date": "2023-01-01", "end_date": "2023-01-31"}
        
        self.mock_reporting_service.generate_report.side_effect = Exception("Test error")
        
        # Act/Assert
        with self.assertRaises(ValueError) as context:
            self.adapter.generate_report(report_id, parameters)
        
        # Verify error message
        self.assertIn("Error generating report", str(context.exception))
        
        # Verify service was called
        self.mock_reporting_service.generate_report.assert_called_once_with(report_id, parameters)


if __name__ == "__main__":
    unittest.main()
