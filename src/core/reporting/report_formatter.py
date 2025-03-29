"""
Report formatter for customizing report output.
"""
from typing import Any, Dict, List, Optional
import json


class ReportFormatter:
    """
    Formatter for customizing report output.
    
    This class follows the Single Responsibility Principle by focusing only on
    formatting report data for display, separate from report generation logic.
    """
    
    @staticmethod
    def format_summary(report_data: Dict[str, Any]) -> str:
        """
        Format a simple summary of the report.
        
        Args:
            report_data: Report data dictionary
            
        Returns:
            Formatted summary string
        """
        metadata = report_data.get("metadata", {})
        data = report_data.get("data", {})
        
        # Extract key information
        title = metadata.get("title", "Report")
        report_type = metadata.get("report_type", "unknown")
        created_at = metadata.get("created_at", "")
        
        # Format summary based on report type
        if report_type == "execution":
            summary = data.get("summary", {})
            total_actions = summary.get("total_actions", 0)
            successful_actions = summary.get("successful_actions", 0)
            failed_actions = summary.get("failed_actions", 0)
            
            return (
                f"Execution Report: {title}\n"
                f"Created: {created_at}\n"
                f"Actions: {total_actions} total, {successful_actions} successful, {failed_actions} failed"
            )
            
        elif report_type == "test_case":
            statistics = data.get("statistics", {})
            total = statistics.get("total", 0)
            passed = statistics.get("passed", 0)
            failed = statistics.get("failed", 0)
            pass_rate = statistics.get("pass_rate", 0)
            
            return (
                f"Test Case Report: {title}\n"
                f"Created: {created_at}\n"
                f"Tests: {total} total, {passed} passed, {failed} failed ({pass_rate:.1f}% pass rate)"
            )
            
        elif report_type == "summary":
            overview = data.get("overview", {})
            total_workflows = overview.get("total_workflows", 0)
            success_rate = overview.get("success_rate", 0)
            
            return (
                f"Summary Report: {title}\n"
                f"Created: {created_at}\n"
                f"Workflows: {total_workflows} total, {success_rate:.1f}% success rate"
            )
            
        else:
            # Generic summary for unknown report types
            return (
                f"Report: {title}\n"
                f"Type: {report_type}\n"
                f"Created: {created_at}"
            )
    
    @staticmethod
    def format_json(report_data: Dict[str, Any], indent: int = 2) -> str:
        """
        Format report data as JSON.
        
        Args:
            report_data: Report data dictionary
            indent: Indentation level for JSON formatting
            
        Returns:
            JSON string
        """
        return json.dumps(report_data, indent=indent)
    
    @staticmethod
    def format_table(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> str:
        """
        Format a list of dictionaries as a text table.
        
        Args:
            data: List of dictionaries to format
            columns: Optional list of columns to include (uses all keys if None)
            
        Returns:
            Formatted table string
        """
        if not data:
            return "No data to display"
        
        # Determine columns to display
        if columns is None:
            # Use all unique keys from all dictionaries
            columns = sorted(set().union(*(d.keys() for d in data)))
        
        # Calculate column widths
        widths = {col: len(col) for col in columns}
        for row in data:
            for col in columns:
                if col in row:
                    widths[col] = max(widths[col], len(str(row.get(col, ""))))
        
        # Create header row
        header = " | ".join(col.ljust(widths[col]) for col in columns)
        separator = "-+-".join("-" * widths[col] for col in columns)
        
        # Create data rows
        rows = []
        for row in data:
            formatted_row = " | ".join(
                str(row.get(col, "")).ljust(widths[col]) for col in columns
            )
            rows.append(formatted_row)
        
        # Combine all parts
        return "\n".join([header, separator] + rows)
    
    @staticmethod
    def extract_key_metrics(report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key metrics from a report for quick viewing.
        
        Args:
            report_data: Report data dictionary
            
        Returns:
            Dictionary of key metrics
        """
        metrics = {}
        metadata = report_data.get("metadata", {})
        data = report_data.get("data", {})
        
        # Add basic metadata
        metrics["title"] = metadata.get("title", "Report")
        metrics["type"] = metadata.get("report_type", "unknown")
        metrics["created_at"] = metadata.get("created_at", "")
        
        # Extract metrics based on report type
        report_type = metadata.get("report_type", "unknown")
        
        if report_type == "execution":
            summary = data.get("summary", {})
            performance = data.get("performance", {})
            
            metrics["total_actions"] = summary.get("total_actions", 0)
            metrics["success_rate"] = summary.get("success_rate", 0)
            metrics["total_duration_ms"] = performance.get("total_duration_ms", 0)
            
        elif report_type == "test_case":
            statistics = data.get("statistics", {})
            
            metrics["total_tests"] = statistics.get("total", 0)
            metrics["pass_rate"] = statistics.get("pass_rate", 0)
            metrics["avg_execution_time_ms"] = statistics.get("average_execution_time_ms", 0)
            
        elif report_type == "summary":
            overview = data.get("overview", {})
            performance = data.get("performance", {})
            
            metrics["total_workflows"] = overview.get("total_workflows", 0)
            metrics["success_rate"] = overview.get("success_rate", 0)
            metrics["avg_duration_ms"] = performance.get("average_workflow_duration_ms", 0)
        
        return metrics
