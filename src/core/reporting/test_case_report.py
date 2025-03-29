"""
Test case report for data-driven testing results.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.core.reporting.base_report import BaseReport


class TestCaseReport(BaseReport):
    """
    Report for data-driven test case results.
    
    This report provides detailed information about data-driven test execution,
    including test case pass/fail statistics, test step details, and data visualization.
    """
    
    def __init__(
        self,
        title: str = "Data-Driven Test Report",
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize the test case report.
        
        Args:
            title: Report title
            description: Optional report description
            tags: Optional list of tags for categorization
        """
        super().__init__(
            report_type="test_case",
            title=title,
            description=description,
            tags=tags
        )
        self.data = {
            "test_info": {
                "name": "",
                "data_source": "",
                "total_records": 0,
                "execution_time": ""
            },
            "test_cases": [],
            "statistics": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "pass_rate": 0,
                "average_execution_time_ms": 0
            },
            "data_summary": {
                "fields": [],
                "sample_values": {}
            }
        }
    
    def collect_data(self, source: Any) -> None:
        """
        Collect data from data-driven test execution.
        
        Args:
            source: The data-driven test execution context
        """
        super().collect_data(source)
        
        # Extract test information
        if hasattr(source, "name"):
            self.data["test_info"]["name"] = source.name
        
        # Extract data source information
        if hasattr(source, "data_source"):
            data_source = source.data_source
            if hasattr(data_source, "name"):
                self.data["test_info"]["data_source"] = data_source.name
        
        # Extract test case results
        if hasattr(source, "results"):
            self._process_test_results(source.results)
        
        # Extract data summary if available
        if hasattr(source, "data_source") and hasattr(source.data_source, "get_fields"):
            self._process_data_summary(source.data_source)
    
    def _process_test_results(self, results: List[Dict[str, Any]]) -> None:
        """
        Process test case results from data-driven execution.
        
        Args:
            results: List of test case execution results
        """
        self.data["test_cases"] = []
        passed_tests = 0
        failed_tests = 0
        total_execution_time = 0
        
        for result in results:
            test_case = {
                "record_index": result.get("record_index", 0),
                "success": result.get("success", False),
                "message": result.get("message", ""),
                "execution_time_ms": result.get("execution_time_ms", 0),
                "timestamp": result.get("timestamp", datetime.now().isoformat()),
                "data": result.get("data", {})
            }
            
            self.data["test_cases"].append(test_case)
            
            if test_case["success"]:
                passed_tests += 1
            else:
                failed_tests += 1
            
            total_execution_time += test_case["execution_time_ms"]
        
        # Update statistics
        total_tests = len(results)
        self.data["statistics"]["total"] = total_tests
        self.data["statistics"]["passed"] = passed_tests
        self.data["statistics"]["failed"] = failed_tests
        
        if total_tests > 0:
            self.data["statistics"]["pass_rate"] = (passed_tests / total_tests) * 100
            self.data["statistics"]["average_execution_time_ms"] = total_execution_time / total_tests
        
        self.data["test_info"]["total_records"] = total_tests
        self.data["test_info"]["execution_time"] = datetime.now().isoformat()
    
    def _process_data_summary(self, data_source: Any) -> None:
        """
        Process data source summary information.
        
        Args:
            data_source: The data source object
        """
        # Get field names
        if hasattr(data_source, "get_fields"):
            fields = data_source.get_fields()
            self.data["data_summary"]["fields"] = fields
        
        # Get sample values for each field
        if hasattr(data_source, "get_sample") and fields:
            sample = data_source.get_sample(1)
            if sample and len(sample) > 0:
                for field in fields:
                    if field in sample[0]:
                        self.data["data_summary"]["sample_values"][field] = sample[0][field]
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate the test case report.
        
        Returns:
            A dictionary containing the test case report data
        """
        # Update metadata before generating
        self.metadata.update()
        
        # Generate base report
        report = super().generate()
        
        # Add test-specific sections
        report["pass_rate"] = self.data["statistics"]["pass_rate"]
        
        # Add visualization data
        report["visualization"] = {
            "pass_fail_ratio": {
                "passed": self.data["statistics"]["passed"],
                "failed": self.data["statistics"]["failed"]
            }
        }
        
        return report
