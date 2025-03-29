"""
Summary report for high-level overview of execution results.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import statistics
from collections import Counter

from src.core.reporting.base_report import BaseReport


class SummaryReport(BaseReport):
    """
    Report for high-level overview of execution results.
    
    This report provides a summary of multiple workflow executions,
    including trend analysis, comparison with previous runs, and executive summary.
    """
    
    def __init__(
        self,
        title: str = "Execution Summary Report",
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        time_period: Optional[str] = None
    ):
        """
        Initialize the summary report.
        
        Args:
            title: Report title
            description: Optional report description
            tags: Optional list of tags for categorization
            time_period: Optional time period for the report (e.g., "daily", "weekly")
        """
        super().__init__(
            report_type="summary",
            title=title,
            description=description,
            tags=tags
        )
        self.time_period = time_period
        self.data = {
            "overview": {
                "total_workflows": 0,
                "successful_workflows": 0,
                "failed_workflows": 0,
                "success_rate": 0,
                "time_period": time_period or "all_time",
                "start_time": None,
                "end_time": None
            },
            "action_statistics": {
                "total_actions": 0,
                "successful_actions": 0,
                "failed_actions": 0,
                "action_success_rate": 0,
                "most_common_actions": [],
                "most_failed_actions": []
            },
            "performance": {
                "average_workflow_duration_ms": 0,
                "min_workflow_duration_ms": 0,
                "max_workflow_duration_ms": 0,
                "median_workflow_duration_ms": 0
            },
            "trends": {
                "success_rate_trend": [],
                "duration_trend": [],
                "error_trend": []
            },
            "comparison": {
                "previous_period": {
                    "success_rate_change": 0,
                    "duration_change": 0,
                    "error_rate_change": 0
                }
            },
            "executive_summary": ""
        }
    
    def collect_data(self, source: List[Any]) -> None:
        """
        Collect data from multiple workflow executions.
        
        Args:
            source: List of workflow execution data
        """
        super().collect_data(source)
        
        if not source or not isinstance(source, list):
            self.logger.warning("No workflow data provided or invalid source type")
            return
        
        # Process workflow data
        self._process_workflow_data(source)
        
        # Generate trends
        self._generate_trends(source)
        
        # Compare with previous period if available
        if len(source) > 1:
            self._compare_with_previous(source)
        
        # Generate executive summary
        self._generate_executive_summary()
    
    def _process_workflow_data(self, workflows: List[Any]) -> None:
        """
        Process workflow execution data.
        
        Args:
            workflows: List of workflow execution data
        """
        total_workflows = len(workflows)
        successful_workflows = 0
        failed_workflows = 0
        workflow_durations = []
        
        total_actions = 0
        successful_actions = 0
        failed_actions = 0
        
        action_types = Counter()
        failed_action_types = Counter()
        
        start_times = []
        end_times = []
        
        for workflow in workflows:
            # Extract workflow status
            workflow_success = False
            if hasattr(workflow, "status"):
                workflow_success = str(workflow.status).lower() in ["completed", "success", "successful"]
            
            if workflow_success:
                successful_workflows += 1
            else:
                failed_workflows += 1
            
            # Extract workflow duration
            if hasattr(workflow, "statistics") and hasattr(workflow.statistics, "total_duration_ms"):
                workflow_durations.append(workflow.statistics.total_duration_ms)
            
            # Extract action data
            if hasattr(workflow, "results"):
                for action_result in workflow.results:
                    total_actions += 1
                    
                    action_type = action_result.get("action_type", "unknown")
                    action_types[action_type] += 1
                    
                    if action_result.get("success", False):
                        successful_actions += 1
                    else:
                        failed_actions += 1
                        failed_action_types[action_type] += 1
            
            # Extract timestamps
            if hasattr(workflow, "start_time"):
                start_time = workflow.start_time
                if isinstance(start_time, str):
                    try:
                        start_time = datetime.fromisoformat(start_time)
                    except ValueError:
                        pass
                if isinstance(start_time, datetime):
                    start_times.append(start_time)
            
            if hasattr(workflow, "end_time"):
                end_time = workflow.end_time
                if isinstance(end_time, str):
                    try:
                        end_time = datetime.fromisoformat(end_time)
                    except ValueError:
                        pass
                if isinstance(end_time, datetime):
                    end_times.append(end_time)
        
        # Update overview
        self.data["overview"]["total_workflows"] = total_workflows
        self.data["overview"]["successful_workflows"] = successful_workflows
        self.data["overview"]["failed_workflows"] = failed_workflows
        
        if total_workflows > 0:
            self.data["overview"]["success_rate"] = (successful_workflows / total_workflows) * 100
        
        if start_times:
            self.data["overview"]["start_time"] = min(start_times).isoformat()
        
        if end_times:
            self.data["overview"]["end_time"] = max(end_times).isoformat()
        
        # Update action statistics
        self.data["action_statistics"]["total_actions"] = total_actions
        self.data["action_statistics"]["successful_actions"] = successful_actions
        self.data["action_statistics"]["failed_actions"] = failed_actions
        
        if total_actions > 0:
            self.data["action_statistics"]["action_success_rate"] = (successful_actions / total_actions) * 100
        
        # Most common actions
        most_common = action_types.most_common(5)
        self.data["action_statistics"]["most_common_actions"] = [
            {"type": action_type, "count": count}
            for action_type, count in most_common
        ]
        
        # Most failed actions
        most_failed = failed_action_types.most_common(5)
        self.data["action_statistics"]["most_failed_actions"] = [
            {"type": action_type, "count": count}
            for action_type, count in most_failed
        ]
        
        # Update performance statistics
        if workflow_durations:
            self.data["performance"]["average_workflow_duration_ms"] = sum(workflow_durations) / len(workflow_durations)
            self.data["performance"]["min_workflow_duration_ms"] = min(workflow_durations)
            self.data["performance"]["max_workflow_duration_ms"] = max(workflow_durations)
            self.data["performance"]["median_workflow_duration_ms"] = statistics.median(workflow_durations)
    
    def _generate_trends(self, workflows: List[Any]) -> None:
        """
        Generate trend data from workflow executions.
        
        Args:
            workflows: List of workflow execution data
        """
        # Sort workflows by start time if available
        sorted_workflows = sorted(
            workflows,
            key=lambda w: getattr(w, "start_time", datetime.min) if hasattr(w, "start_time") else datetime.min
        )
        
        # Group by day for trend analysis
        daily_stats = {}
        
        for workflow in sorted_workflows:
            # Get date from workflow
            if hasattr(workflow, "start_time"):
                start_time = workflow.start_time
                if isinstance(start_time, str):
                    try:
                        start_time = datetime.fromisoformat(start_time)
                    except ValueError:
                        start_time = datetime.min
                
                if isinstance(start_time, datetime):
                    date_key = start_time.date().isoformat()
                    
                    if date_key not in daily_stats:
                        daily_stats[date_key] = {
                            "total": 0,
                            "successful": 0,
                            "failed": 0,
                            "durations": []
                        }
                    
                    daily_stats[date_key]["total"] += 1
                    
                    # Check success status
                    workflow_success = False
                    if hasattr(workflow, "status"):
                        workflow_success = str(workflow.status).lower() in ["completed", "success", "successful"]
                    
                    if workflow_success:
                        daily_stats[date_key]["successful"] += 1
                    else:
                        daily_stats[date_key]["failed"] += 1
                    
                    # Add duration if available
                    if hasattr(workflow, "statistics") and hasattr(workflow.statistics, "total_duration_ms"):
                        daily_stats[date_key]["durations"].append(workflow.statistics.total_duration_ms)
        
        # Generate trend data
        success_rate_trend = []
        duration_trend = []
        error_trend = []
        
        for date_key, stats in sorted(daily_stats.items()):
            # Success rate trend
            success_rate = 0
            if stats["total"] > 0:
                success_rate = (stats["successful"] / stats["total"]) * 100
            
            success_rate_trend.append({
                "date": date_key,
                "success_rate": success_rate
            })
            
            # Duration trend
            avg_duration = 0
            if stats["durations"]:
                avg_duration = sum(stats["durations"]) / len(stats["durations"])
            
            duration_trend.append({
                "date": date_key,
                "average_duration_ms": avg_duration
            })
            
            # Error trend
            error_rate = 0
            if stats["total"] > 0:
                error_rate = (stats["failed"] / stats["total"]) * 100
            
            error_trend.append({
                "date": date_key,
                "error_rate": error_rate
            })
        
        # Update trends in data
        self.data["trends"]["success_rate_trend"] = success_rate_trend
        self.data["trends"]["duration_trend"] = duration_trend
        self.data["trends"]["error_trend"] = error_trend
    
    def _compare_with_previous(self, workflows: List[Any]) -> None:
        """
        Compare current period with previous period.
        
        Args:
            workflows: List of workflow execution data
        """
        # Sort workflows by start time
        sorted_workflows = sorted(
            workflows,
            key=lambda w: getattr(w, "start_time", datetime.min) if hasattr(w, "start_time") else datetime.min
        )
        
        # Determine the midpoint to split into current and previous periods
        midpoint = len(sorted_workflows) // 2
        
        previous_workflows = sorted_workflows[:midpoint]
        current_workflows = sorted_workflows[midpoint:]
        
        # Calculate metrics for previous period
        prev_success_rate = 0
        prev_avg_duration = 0
        prev_error_rate = 0
        
        if previous_workflows:
            prev_successful = sum(
                1 for w in previous_workflows
                if hasattr(w, "status") and str(w.status).lower() in ["completed", "success", "successful"]
            )
            prev_success_rate = (prev_successful / len(previous_workflows)) * 100
            
            prev_durations = [
                w.statistics.total_duration_ms
                for w in previous_workflows
                if hasattr(w, "statistics") and hasattr(w.statistics, "total_duration_ms")
            ]
            
            if prev_durations:
                prev_avg_duration = sum(prev_durations) / len(prev_durations)
            
            prev_failed = len(previous_workflows) - prev_successful
            prev_error_rate = (prev_failed / len(previous_workflows)) * 100
        
        # Calculate metrics for current period
        curr_success_rate = 0
        curr_avg_duration = 0
        curr_error_rate = 0
        
        if current_workflows:
            curr_successful = sum(
                1 for w in current_workflows
                if hasattr(w, "status") and str(w.status).lower() in ["completed", "success", "successful"]
            )
            curr_success_rate = (curr_successful / len(current_workflows)) * 100
            
            curr_durations = [
                w.statistics.total_duration_ms
                for w in current_workflows
                if hasattr(w, "statistics") and hasattr(w.statistics, "total_duration_ms")
            ]
            
            if curr_durations:
                curr_avg_duration = sum(curr_durations) / len(curr_durations)
            
            curr_failed = len(current_workflows) - curr_successful
            curr_error_rate = (curr_failed / len(current_workflows)) * 100
        
        # Calculate changes
        success_rate_change = curr_success_rate - prev_success_rate
        duration_change = curr_avg_duration - prev_avg_duration
        error_rate_change = curr_error_rate - prev_error_rate
        
        # Update comparison data
        self.data["comparison"]["previous_period"]["success_rate_change"] = success_rate_change
        self.data["comparison"]["previous_period"]["duration_change"] = duration_change
        self.data["comparison"]["previous_period"]["error_rate_change"] = error_rate_change
    
    def _generate_executive_summary(self) -> None:
        """
        Generate an executive summary based on the collected data.
        """
        overview = self.data["overview"]
        performance = self.data["performance"]
        comparison = self.data["comparison"]["previous_period"]
        
        summary_parts = []
        
        # Overall success rate
        summary_parts.append(
            f"Overall success rate: {overview['success_rate']:.1f}% "
            f"({overview['successful_workflows']} of {overview['total_workflows']} workflows successful)"
        )
        
        # Performance summary
        if performance["average_workflow_duration_ms"] > 0:
            avg_duration_sec = performance["average_workflow_duration_ms"] / 1000
            summary_parts.append(f"Average workflow duration: {avg_duration_sec:.2f} seconds")
        
        # Comparison with previous period
        if comparison["success_rate_change"] != 0:
            direction = "increased" if comparison["success_rate_change"] > 0 else "decreased"
            summary_parts.append(
                f"Success rate has {direction} by {abs(comparison['success_rate_change']):.1f}% "
                f"compared to the previous period"
            )
        
        if comparison["duration_change"] != 0:
            direction = "increased" if comparison["duration_change"] > 0 else "decreased"
            duration_change_sec = abs(comparison["duration_change"]) / 1000
            summary_parts.append(
                f"Average duration has {direction} by {duration_change_sec:.2f} seconds "
                f"compared to the previous period"
            )
        
        # Join all parts
        self.data["executive_summary"] = " ".join(summary_parts)
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate the summary report.
        
        Returns:
            A dictionary containing the summary report data
        """
        # Update metadata before generating
        self.metadata.update()
        
        # Generate base report
        report = super().generate()
        
        # Add summary-specific sections
        report["executive_summary"] = self.data["executive_summary"]
        
        return report
