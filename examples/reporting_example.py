"""
Example demonstrating the use of the reporting system.
"""
import os
import sys
from typing import Dict, Any, List
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.reporting.report_service import ReportService
from src.core.reporting.report_factory import ReportFactory


class MockWorkflow:
    """Mock workflow for demonstration purposes."""
    
    def __init__(self, workflow_id: str, actions: List[Dict[str, Any]]):
        """
        Initialize the mock workflow.
        
        Args:
            workflow_id: Workflow ID
            actions: List of action results
        """
        self.id = workflow_id
        self.status = "completed"
        self.results = actions
        self.start_time = datetime.now().isoformat()
        self.end_time = datetime.now().isoformat()
        
        # Calculate statistics
        self.statistics = MockStatistics(actions)


class MockStatistics:
    """Mock statistics for demonstration purposes."""
    
    def __init__(self, actions: List[Dict[str, Any]]):
        """
        Initialize the mock statistics.
        
        Args:
            actions: List of action results
        """
        self.action_durations = {
            action["action_id"]: action.get("execution_time_ms", 0)
            for action in actions
        }
        self.total_duration_ms = sum(self.action_durations.values())


def create_mock_workflow() -> MockWorkflow:
    """
    Create a mock workflow for demonstration.
    
    Returns:
        Mock workflow instance
    """
    actions = [
        {
            "action_id": "action-1",
            "action_type": "click",
            "description": "Click login button",
            "success": True,
            "message": "Action completed successfully",
            "execution_time_ms": 120,
            "timestamp": datetime.now().isoformat()
        },
        {
            "action_id": "action-2",
            "action_type": "input",
            "description": "Enter username",
            "success": True,
            "message": "Action completed successfully",
            "execution_time_ms": 80,
            "timestamp": datetime.now().isoformat()
        },
        {
            "action_id": "action-3",
            "action_type": "input",
            "description": "Enter password",
            "success": True,
            "message": "Action completed successfully",
            "execution_time_ms": 75,
            "timestamp": datetime.now().isoformat()
        },
        {
            "action_id": "action-4",
            "action_type": "click",
            "description": "Click submit button",
            "success": True,
            "message": "Action completed successfully",
            "execution_time_ms": 150,
            "timestamp": datetime.now().isoformat()
        },
        {
            "action_id": "action-5",
            "action_type": "wait",
            "description": "Wait for dashboard",
            "success": False,
            "message": "Timeout waiting for element",
            "execution_time_ms": 5000,
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    return MockWorkflow("workflow-123", actions)


def create_mock_test_data() -> Dict[str, Any]:
    """
    Create mock test data for demonstration.
    
    Returns:
        Mock test data
    """
    return {
        "name": "Login Test Suite",
        "data_source": "login_credentials.csv",
        "results": [
            {
                "record_index": 0,
                "success": True,
                "message": "Login successful",
                "execution_time_ms": 1200,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "username": "user1",
                    "password": "********",
                    "expected_result": "success"
                }
            },
            {
                "record_index": 1,
                "success": False,
                "message": "Login failed: Invalid credentials",
                "execution_time_ms": 950,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "username": "user2",
                    "password": "********",
                    "expected_result": "failure"
                }
            },
            {
                "record_index": 2,
                "success": True,
                "message": "Login successful",
                "execution_time_ms": 1100,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "username": "user3",
                    "password": "********",
                    "expected_result": "success"
                }
            }
        ],
        "get_fields": lambda: ["username", "password", "expected_result"],
        "get_sample": lambda n: [{"username": "user1", "password": "********", "expected_result": "success"}]
    }


def main() -> None:
    """Main function demonstrating the reporting system."""
    # Create report service
    report_service = ReportService(report_dir="example_reports")
    
    print("=== Reporting System Example ===\n")
    
    # Create mock data
    workflow = create_mock_workflow()
    test_data = create_mock_test_data()
    
    print("1. Generating Execution Report...")
    execution_report_data = report_service.generate_report(
        report_type="execution",
        source=workflow,
        title="Login Workflow Execution",
        description="Execution report for login workflow",
        tags=["login", "workflow", "example"],
        save=True
    )
    
    print("\nExecution Report Summary:")
    execution_report = report_service.report_manager.get_reports(report_type="execution")[0]
    print(report_service.get_report_summary(execution_report))
    
    print("\n2. Generating Test Case Report...")
    test_report_data = report_service.generate_report(
        report_type="test_case",
        source=test_data,
        title="Login Test Cases",
        description="Test report for login credentials",
        tags=["login", "test", "example"],
        save=True
    )
    
    print("\nTest Case Report Summary:")
    test_report = report_service.report_manager.get_reports(report_type="test_case")[0]
    print(report_service.get_report_summary(test_report))
    
    print("\n3. Generating Summary Report...")
    # Create a list of workflows for the summary report
    workflows = [workflow]
    
    summary_report_data = report_service.generate_report(
        report_type="summary",
        source=workflows,
        title="Daily Execution Summary",
        description="Summary of all workflow executions",
        tags=["summary", "daily", "example"],
        save=True,
        time_period="daily"
    )
    
    print("\nSummary Report Summary:")
    summary_report = report_service.report_manager.get_reports(report_type="summary")[0]
    print(report_service.get_report_summary(summary_report))
    
    print("\n4. Report Metrics:")
    metrics = report_service.get_report_metrics(execution_report)
    print(json.dumps(metrics, indent=2))
    
    print("\nReports saved to directory:", report_service.report_storage.report_dir)
    print("Files:")
    for file_path in report_service.report_storage.list_reports():
        print(f"- {os.path.basename(file_path)}")


if __name__ == "__main__":
    main()
